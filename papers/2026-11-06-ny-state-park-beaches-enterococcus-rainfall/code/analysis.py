# analysis.py — exceedance trends, closure/advisory-day accounting, and the
# rainfall-exceedance association with beach fixed effects.
# Reads data/derived/{samples,status_timeline}.csv (from build_panel.py), writes
# results/*.json.

import json
import os
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from common import DERIVED, RESULTS, WATERBODIES

RNG_SEED = 20261102


def jd(obj, name):
    with open(os.path.join(RESULTS, name), 'w') as f:
        json.dump(obj, f, indent=2, default=float)


def load():
    samples = pd.read_csv(os.path.join(DERIVED, 'samples.csv'), parse_dates=['date_sample_taken'])
    timeline = pd.read_csv(os.path.join(DERIVED, 'status_timeline.csv'), parse_dates=['status_start', 'status_end'])
    return samples, timeline


def descriptives(samples):
    out = {
        'n_samples': int(len(samples)),
        'n_exceeded': int(samples['exceeded'].sum()),
        'exceedance_rate': float(samples['exceeded'].mean()),
        'years': [int(samples['year'].min()), int(samples['year'].max())],
        'n_beach_stations': int(samples['state_park_beach'].nunique()),
    }
    by_beach = (samples.groupby('state_park_beach')
                .agg(n=('exceeded', 'size'), n_exceeded=('exceeded', 'sum'), rate=('exceeded', 'mean'),
                     waterbody=('waterbody', 'first'))
                .reset_index().sort_values('rate', ascending=False))
    by_waterbody = (samples.groupby('waterbody')
                    .agg(n=('exceeded', 'size'), n_exceeded=('exceeded', 'sum'), rate=('exceeded', 'mean'))
                    .reset_index().sort_values('rate', ascending=False))
    by_year = (samples.groupby('year')
               .agg(n=('exceeded', 'size'), n_exceeded=('exceeded', 'sum'), rate=('exceeded', 'mean'))
               .reset_index())
    by_beach_year = (samples.groupby(['state_park_beach', 'year'])
                     .agg(n=('exceeded', 'size'), n_exceeded=('exceeded', 'sum'), rate=('exceeded', 'mean'))
                     .reset_index())
    out['by_beach'] = by_beach.to_dict('records')
    out['by_waterbody'] = by_waterbody.to_dict('records')
    out['by_year'] = by_year.to_dict('records')
    out['samples_per_beach_year_median'] = float(by_beach_year['n'].median())
    out['samples_per_beach_year_min_max'] = [int(by_beach_year['n'].min()), int(by_beach_year['n'].max())]
    return out


def trend_models(samples):
    d = samples.copy()
    d['year_c'] = d['year'] - d['year'].mean()
    d['exceeded'] = d['exceeded'].astype(int)
    out = {}

    # Pooled trend, beach fixed effects, cluster-robust by beach (n=15 clusters).
    m = smf.logit('exceeded ~ year_c + C(state_park_beach)', data=d).fit(disp=0)
    mc = smf.logit('exceeded ~ year_c + C(state_park_beach)', data=d).fit(
        disp=0, cov_type='cluster', cov_kwds={'groups': d['state_park_beach']})
    out['pooled_fe'] = {
        'n': int(m.nobs), 'n_clusters': int(d['state_park_beach'].nunique()),
        'year_coef': float(mc.params['year_c']), 'year_se_cluster': float(mc.bse['year_c']),
        'year_p_cluster': float(mc.pvalues['year_c']),
        'year_odds_ratio_per_year': float(np.exp(mc.params['year_c'])),
        'or_ci95_cluster': [float(np.exp(mc.conf_int().loc['year_c', 0])),
                             float(np.exp(mc.conf_int().loc['year_c', 1]))],
        'year_se_model': float(m.bse['year_c']),
    }

    # By waterbody: separate trend, beach fixed effects within group, cluster by beach.
    by_wb = {}
    for wb in WATERBODIES:
        sub = d[d['waterbody'] == wb]
        n_beach = sub['state_park_beach'].nunique()
        if n_beach > 1:
            mm = smf.logit('exceeded ~ year_c + C(state_park_beach)', data=sub).fit(
                disp=0, cov_type='cluster', cov_kwds={'groups': sub['state_park_beach']})
        else:
            mm = smf.logit('exceeded ~ year_c', data=sub).fit(disp=0)
        by_wb[wb] = {
            'n': int(len(sub)), 'n_beach_stations': int(n_beach), 'n_exceeded': int(sub['exceeded'].sum()),
            'rate': float(sub['exceeded'].mean()),
            'year_coef': float(mm.params['year_c']), 'year_se': float(mm.bse['year_c']),
            'year_odds_ratio_per_year': float(np.exp(mm.params['year_c'])),
        }
    out['by_waterbody'] = by_wb

    # Weighted-least-squares check on annual rates (no fixed effects), as a
    # transparent cross-check of the logistic trend.
    by_year = d.groupby('year').agg(n=('exceeded', 'size'), rate=('exceeded', 'mean')).reset_index()
    by_year['year_c'] = by_year['year'] - by_year['year'].mean()
    wls = smf.wls('rate ~ year_c', data=by_year, weights=by_year['n']).fit()
    out['annual_rate_wls_check'] = {
        'slope_per_year': float(wls.params['year_c']), 'slope_se': float(wls.bse['year_c']),
        'slope_p': float(wls.pvalues['year_c']),
    }
    return out


def rainfall_model(samples):
    d = samples.dropna(subset=['rain_48h']).copy()
    d['exceeded'] = d['exceeded'].astype(int)
    d['year_c'] = d['year'] - d['year'].mean()
    d['rain_48h_cm'] = d['rain_48h'] / 10.0  # per cm, for a readable coefficient
    d['rain_0_cm'] = d['rain_0'].fillna(0) / 10.0
    d['rain_72h_cm'] = d['rain_72h'] / 10.0

    out = {'n': int(len(d))}

    def fit(formula, label):
        m = smf.logit(formula, data=d).fit(disp=0, maxiter=100)
        mc = smf.logit(formula, data=d).fit(disp=0, cov_type='cluster',
                                             cov_kwds={'groups': d['state_park_beach']}, maxiter=100)
        key = [k for k in mc.params.index if k.startswith('rain')][0]
        return {
            'formula': formula, 'n': int(m.nobs),
            'coef': float(mc.params[key]), 'se_cluster': float(mc.bse[key]),
            'p_cluster': float(mc.pvalues[key]),
            'odds_ratio_per_unit': float(np.exp(mc.params[key])),
            'or_ci95_cluster': [float(np.exp(mc.conf_int().loc[key, 0])),
                                 float(np.exp(mc.conf_int().loc[key, 1]))],
        }

    out['main_48h'] = fit('exceeded ~ rain_48h_cm + year_c + C(state_park_beach)', 'rain_48h_cm')
    out['robustness_sameday'] = fit('exceeded ~ rain_0_cm + year_c + C(state_park_beach)', 'rain_0_cm')
    out['robustness_72h'] = fit('exceeded ~ rain_72h_cm + year_c + C(state_park_beach)', 'rain_72h_cm')
    out['robustness_48h_no_fe'] = fit('exceeded ~ rain_48h_cm + year_c', 'rain_48h_cm (no beach FE)')

    # By waterbody (does rain predict exceedance differently for bay vs. sound vs. ocean beaches?)
    by_wb = {}
    for wb in WATERBODIES:
        sub = d[d['waterbody'] == wb]
        if sub['state_park_beach'].nunique() > 1 and sub['exceeded'].sum() >= 5:
            mm = smf.logit('exceeded ~ rain_48h_cm + year_c + C(state_park_beach)', data=sub).fit(disp=0, maxiter=100)
            by_wb[wb] = {'n': int(len(sub)), 'n_exceeded': int(sub['exceeded'].sum()),
                         'coef': float(mm.params['rain_48h_cm']),
                         'odds_ratio_per_cm': float(np.exp(mm.params['rain_48h_cm']))}
        else:
            by_wb[wb] = {'n': int(len(sub)), 'n_exceeded': int(sub['exceeded'].sum()), 'note': 'too few exceedances to fit'}
    out['by_waterbody'] = by_wb

    # Descriptive: exceedance rate by 48h-rain bucket.
    bins = [-0.01, 0, 10, 25, 1000]
    labels = ['0 mm', '0-10 mm', '10-25 mm', '>25 mm']
    d['rain_bucket'] = pd.cut(d['rain_48h'], bins=bins, labels=labels)
    bucket = d.groupby('rain_bucket', observed=True).agg(n=('exceeded', 'size'), rate=('exceeded', 'mean')).reset_index()
    out['exceedance_by_rain_bucket'] = bucket.to_dict('records')
    return out


def closures(timeline):
    out = {}
    tl = timeline.copy()
    closure_adv = tl[tl['is_closure'] | tl['is_advisory']]

    cdays = tl[tl['is_closure']].groupby('state_park_beach')['days'].sum()
    adays = tl[tl['is_advisory']].groupby('state_park_beach')['days'].sum()
    wb_map = tl.drop_duplicates('state_park_beach').set_index('state_park_beach')['waterbody']
    beach_tbl = pd.DataFrame({'closure_days': cdays, 'advisory_days': adays}).fillna(0)
    beach_tbl['total_days'] = beach_tbl['closure_days'] + beach_tbl['advisory_days']
    beach_tbl['waterbody'] = wb_map
    beach_tbl = beach_tbl.reset_index().rename(columns={'index': 'state_park_beach'}).sort_values('total_days', ascending=False)
    total_closure_days = float(tl.loc[tl['is_closure'], 'days'].sum())
    total_advisory_days = float(tl.loc[tl['is_advisory'], 'days'].sum())
    beach_tbl['pct_of_total_closure_days'] = beach_tbl['closure_days'] / total_closure_days * 100 if total_closure_days else 0

    out['total_closure_days'] = total_closure_days
    out['total_advisory_days'] = total_advisory_days
    out['by_beach'] = beach_tbl.to_dict('records')
    out['top5_beaches_share_of_closure_days'] = float(
        beach_tbl.sort_values('closure_days', ascending=False).head(5)['closure_days'].sum() / total_closure_days * 100
    ) if total_closure_days else None

    cdays_wb = tl[tl['is_closure']].groupby('waterbody')['days'].sum()
    adays_wb = tl[tl['is_advisory']].groupby('waterbody')['days'].sum()
    out['by_waterbody'] = pd.DataFrame({'closure_days': cdays_wb, 'advisory_days': adays_wb}).fillna(0).reset_index().to_dict('records')

    cdays_yr = tl[tl['is_closure']].groupby('year')['days'].sum()
    adays_yr = tl[tl['is_advisory']].groupby('year')['days'].sum()
    out['by_year'] = pd.DataFrame({'closure_days': cdays_yr, 'advisory_days': adays_yr}).fillna(0).reset_index().to_dict('records')

    # Reason breakdown for closures/advisories.
    reason_tbl = closure_adv.groupby('status_reason').agg(n_events=('days', 'size'), total_days=('days', 'sum')).reset_index()
    out['reason_breakdown'] = reason_tbl.sort_values('total_days', ascending=False).to_dict('records')
    out['n_rain_related_events'] = int(closure_adv['rain_related'].sum())
    out['n_closure_advisory_events'] = int(len(closure_adv))
    out['pct_events_rain_related'] = float(closure_adv['rain_related'].mean() * 100)

    # Seasonal/administrative 'Closed' events (end-of-season, preseason) excluded
    # from is_closure above; reported separately, not as water-quality closures.
    admin = tl[tl['is_seasonal_admin']]
    out['seasonal_admin_days_excluded'] = float(admin['days'].sum())
    out['seasonal_admin_events_excluded'] = int(len(admin))
    return out


def rain_at_closures(samples, timeline):
    # Of the closures triggered specifically by an 'Exceedance' status reason, how
    # many followed a wet 48 hours at the assigned station?
    tl = timeline[(timeline['is_closure']) & (timeline['status_reason'] == 'Exceedance')]
    exc = samples[samples['exceeded'] == True].copy()
    # Merge the exceedance's own rain_48h onto the closure event it produced (closure
    # start date == sample's status_date; approximate by matching beach + nearest
    # status_start to date_sample_taken + 0/1 day).
    exc['status_date_est'] = exc['date_sample_taken'] + pd.to_timedelta(1, unit='D')
    merged = tl.merge(exc[['state_park_beach', 'status_date_est', 'rain_48h', 'rain_0']],
                       left_on=['state_park_beach', 'status_start'],
                       right_on=['state_park_beach', 'status_date_est'], how='left')
    matched = merged.dropna(subset=['rain_48h'])
    out = {
        'n_exceedance_closures': int(len(tl)),
        'n_matched_to_a_sample_with_rain_data': int(len(matched)),
        'share_with_any_rain_48h': float((matched['rain_48h'] > 0).mean()) if len(matched) else None,
        'median_rain_48h_mm': float(matched['rain_48h'].median()) if len(matched) else None,
        'share_with_rain_48h_over_10mm': float((matched['rain_48h'] > 10).mean()) if len(matched) else None,
    }
    # Compare with the background rate of >10mm-in-48h across all samples.
    all_bg = samples['rain_48h'].dropna()
    out['background_share_days_with_rain_48h_over_10mm'] = float((all_bg > 10).mean())
    return out


def main():
    samples, timeline = load()
    jd(descriptives(samples), 'descriptives.json')
    jd(trend_models(samples), 'trends.json')
    jd(rainfall_model(samples), 'rainfall.json')
    jd(closures(timeline), 'closures.json')
    jd(rain_at_closures(samples, timeline), 'rain_at_closures.json')
    return 'ok'


if __name__ == '__main__':
    print(main())
