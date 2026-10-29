"""Search over ratio constructions for the one matching the original's descriptive statistics for the traditional RFEI
(Table 3: median 3.5, SD 1.86, all counties; Table 4: mean 3.89, used as cut-off, N = 3,108).
Numerators: every set of 1-4 outlet types from FFR, CONVS, GROC, SUPERC, SPECS, FMRKT, FSR (98 sets);
denominators: every set of 1-3 of GROC, SUPERC, SPECS, FMRKT (14 sets); 98 x 14 = 1,372 constructions (sets that share
an outlet type in numerator and denominator are kept). 2007 counts, 2009 farmers' markets.
Writes results/construction_search.csv and results/construction_search.json."""
import itertools, numpy as np, pandas as pd
from common import DER, RES, dump
d = pd.read_csv(f'{DER}/county_base.csv')
V = {'FFR': d.ffr, 'CONVS': d.convs, 'GROC': d.groc, 'SUPERC': d.superc, 'SPECS': d.specs, 'FMRKT': d.fmrkt, 'FSR': d.fsr}
cont = d.natamen.notna()
rows = []
for nk in range(1, 5):
    for nn in itertools.combinations(V, nk):
        for dk in range(1, 4):
            for dd in itertools.combinations(['GROC', 'SUPERC', 'SPECS', 'FMRKT'], dk):
                num = sum(V[k] for k in nn); den = sum(V[k] for k in dd)
                x = num / den.where(den > 0)
                a = x.dropna(); c = x[cont].dropna()
                rows.append({'numerator': '+'.join(nn), 'denominator': '+'.join(dd), 'median_all': a.median(), 'sd_all': a.std(),
                             'mean_all': a.mean(), 'mean_contig': c.mean(), 'n_contig': len(c)})
R = pd.DataFrame(rows)
R['distance'] = (R.median_all - 3.5).abs() + (R.sd_all - 1.86).abs() + (R.mean_contig - 3.89).abs()
R = R.sort_values('distance'); R.to_csv(f'{RES}/construction_search.csv', index=False)
best = R.iloc[0]; second = R.iloc[1]
dump({'n_constructions': len(R), 'best': best.to_dict(), 'second': second.to_dict(),
      'table1_traditional': R[(R.numerator == 'FFR+CONVS') & (R.denominator == 'GROC')].iloc[0].to_dict()}, 'construction_search.json')
print(len(R)); print(R.head(5).round(3).to_string())
