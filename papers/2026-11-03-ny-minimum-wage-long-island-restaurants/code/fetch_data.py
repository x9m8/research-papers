"""Download the QCEW quarterly industry files and reduce them to data/raw/qcew_ny_nj_pa_quarterly.csv
(ordinary machine with internet access; requires `requests`). Mirrors fetch_browser.js, which was used for the
published results because the analysis environment had no direct internet access. The minimum-wage schedule
(data/raw/minwage_schedule.csv) was coded by hand from the official sources listed in README.md."""
import os, re, time
import requests
from common import RAW, QCEW_FILE

IND = ['10', '722', '7224', '7225', '722511', '722513']
KEEP = ['area_fips', 'own_code', 'industry_code', 'year', 'qtr', 'disclosure_code', 'qtrly_estabs',
        'month1_emplvl', 'month2_emplvl', 'month3_emplvl', 'total_qtrly_wages', 'avg_wkly_wage']


def main():
    os.makedirs(RAW, exist_ok=True)
    S = requests.Session(); S.headers['User-Agent'] = 'research script (x9m8x7@gmail.com)'
    rows = {}
    for y in range(2010, 2027):
        for q in range(1, 5):
            for i in IND:
                for t in range(4):
                    r = S.get(f'https://data.bls.gov/cew/data/api/{y}/{q}/industry/{i}.csv', timeout=120)
                    if r.status_code == 404 or r.ok:
                        break
                    time.sleep(2 * (t + 1))
                if not r.ok:
                    continue
                L = r.text.strip().split('\n'); h = L[0].replace('"', '').split(','); idx = [h.index(k) for k in KEEP]; out = []
                for line in L[1:]:
                    f = line.replace('"', '').split(','); a = f[idx[0]]
                    if not re.match(r'^(36|34|42)\d{3}$', a) or a.endswith('000') or f[idx[1]] != '5':
                        continue
                    out.append(','.join(f[j] for j in idx))
                if not out:   # a 200 response with no matching rows is a failure, not an empty quarter
                    raise RuntimeError(f'QCEW file {y} Q{q} {i}: HTTP 200 but no matching county rows; rerun')
                rows[f'{y}_{q}_{i}'] = out
    with open(os.path.join(RAW, QCEW_FILE), 'w', newline='') as fh:
        fh.write(','.join(KEEP) + '\n' + '\n'.join('\n'.join(rows[k]) for k in sorted(rows)) + '\n')


if __name__ == '__main__':
    main()
