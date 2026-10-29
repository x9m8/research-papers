"""Which Food Environment Atlas release and year of store counts match the original's Table 3?
Lists the store-count years in each release and compares medians/SDs of counts with the published Table 3.
Writes results/vintage_check.json."""
import re, pandas as pd, numpy as np
from common import RAW, dump
pub = {'FFR': (15.0, 228.60), 'GROC': (6.0, 76.80), 'SUPERC': (0.0, 2.64), 'CONVS': (16.0, 87.50), 'SPECS': (1.0, 37.95)}
out = {}
for f in ['atlas_nov2012.xls', 'atlas_feb2014.xls', 'atlas_aug2015.xls']:
    s = pd.read_excel(f'{RAW}/{f}', 'STORES').drop_duplicates('FIPS'); r = pd.read_excel(f'{RAW}/{f}', 'RESTAURANTS').drop_duplicates('FIPS')
    m = s.merge(r, on='FIPS')
    years = sorted({c[-2:] for c in m.columns if re.fullmatch(r'(GROC|FFR)\d\d', c)})
    out[f] = {'count_years': ['20' + y for y in years]}
    for y in years:
        out[f]['20' + y] = {v: {'median': float(m[v + y].median()), 'sd': float(m[v + y].std()), 'pub': pub[v]} for v in pub}
dump(out, 'vintage_check.json')
for f, v in out.items():
    print(f, v['count_years'])
    for y in v['count_years']: print('  ', y, {k: (round(x['median'], 1), round(x['sd'], 2)) for k, x in v[y].items()})
