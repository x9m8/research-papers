"""Build the county-quarter panel from the QCEW extract -> data/derived/panel.csv, results/build.json."""
import os, json
import numpy as np
import pandas as pd
from common import RAW, DER, RES, QCEW_FILE, QUARTERS, INDUSTRIES, qindex, region_of, schedule


def main():
    os.makedirs(DER, exist_ok=True); os.makedirs(RES, exist_ok=True)
    d = pd.read_csv(os.path.join(RAW, QCEW_FILE), dtype=str)
    n_raw = len(d)
    d = d[d.area_fips.str.match(r'^(36|42)\d{3}$') & ~d.area_fips.str.endswith('000') & ~d.area_fips.str.endswith('999')]
    d = d[(d.own_code == '5') & d.industry_code.isin(list(INDUSTRIES))].copy()
    for c in ['qtrly_estabs', 'month1_emplvl', 'month2_emplvl', 'month3_emplvl', 'total_qtrly_wages']:
        d[c] = pd.to_numeric(d[c], errors='coerce')
    d['qi'] = [qindex(y, q) for y, q in zip(d.year, d.qtr)]
    d = d[d.qi.between(qindex(*QUARTERS[0]), qindex(*QUARTERS[-1]))]
    d['emp'] = d[['month1_emplvl', 'month2_emplvl', 'month3_emplvl']].mean(axis=1)
    d['estabs'] = d.qtrly_estabs; d['wages'] = d.total_qtrly_wages
    d['disclosed'] = (d.disclosure_code.fillna('') != 'N') & (d.emp > 0) & (d.estabs > 0) & (d.wages > 0)
    d['region'] = d.area_fips.map(region_of)
    nq = len(QUARTERS)
    full = d[d.disclosed].groupby(['area_fips', 'industry_code']).qi.nunique().eq(nq)
    full = full[full].reset_index()[['area_fips', 'industry_code']].assign(balanced=True)
    d = d.merge(full, on=['area_fips', 'industry_code'], how='left'); d['balanced'] = d.balanced.fillna(False).astype(bool)
    keep = ['area_fips', 'region', 'industry_code', 'year', 'qtr', 'qi', 'emp', 'estabs', 'wages', 'disclosed', 'balanced']
    d[keep].sort_values(['industry_code', 'area_fips', 'qi']).to_csv(os.path.join(DER, 'panel.csv'), index=False)
    s = schedule(); s.to_csv(os.path.join(DER, 'schedule_quarterly.csv'), index=False)
    b = {'n_raw_rows': int(n_raw), 'n_quarters': nq, 'first_quarter': '%dQ%d' % QUARTERS[0], 'last_quarter': '%dQ%d' % QUARTERS[-1],
         'counties': {r: int(d[d.region == r].area_fips.nunique()) for r in ['LI', 'WES', 'NYC', 'ROS', 'PA']}, 'balanced': {}}
    for ind in INDUSTRIES:
        x = d[(d.industry_code == ind) & d.balanced]
        b['balanced'][ind] = {r: int(x[x.region == r].area_fips.nunique()) for r in ['LI', 'WES', 'NYC', 'ROS', 'PA']}
        y16 = d[(d.industry_code == ind) & (d.year.astype(int) == 2016)]
        b['balanced'][ind]['emp2016_LI'] = float(y16[y16.region == 'LI'].groupby('qi').emp.sum().mean())
        b['balanced'][ind]['emp2016_ROS_balanced'] = float(y16[(y16.region == 'ROS') & y16.balanced].groupby('qi').emp.sum().mean())
        b['balanced'][ind]['emp2016_ROS_all_disclosed'] = float(y16[(y16.region == 'ROS') & y16.disclosed].groupby('qi').emp.sum().mean())
        b['balanced'][ind]['emp2016_PA_balanced'] = float(y16[(y16.region == 'PA') & y16.balanced].groupby('qi').emp.sum().mean())
    b['schedule_by_year_q4'] = {int(y): {k: (None if pd.isna(g[k].iloc[-1]) else round(float(g[k].iloc[-1]), 4)) for k in ['mw_li', 'mw_ros', 'tip_li', 'tip_ros', 'ff_li', 'ff_ros', 'gap_general', 'gap_tip', 'gap_ff']}
                                 for y, g in s.groupby('year')}
    json.dump(b, open(os.path.join(RES, 'build.json'), 'w'), separators=(',', ':'))
    print(json.dumps(b['balanced'], indent=1))


if __name__ == '__main__':
    main()
