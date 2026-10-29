"""Counts for the evidence map: all records assessed in detail (full text or abstract), excluding reviews, models and duplicates."""
import json, pandas as pd
from common import DATA, RES
m = pd.read_csv(f'{DATA}/map_coding.csv')
m = m[~m.population.isin(['review', 'model']) & (m.status != 'duplicate report')].copy()
m['evidence'] = m.status.map({'included': 'Full text, included', 'excluded': 'Full text, excluded', 'abstract only': 'Abstract only'})
popg = lambda p: 'Children/adolescents' if any(k in p for k in ('child', 'adolescent')) else ('Older adults' if 'older' in p else 'Adults')
m['popg'] = m.population.map(popg)
rows = []
for r in m.itertuples():
    for b in str(r.bag).split(';'):
        for o in str(r.outcomes).split(';'):
            if b == 'nan' or o == 'nan': continue
            rows.append(dict(id=r.id, evidence=r.evidence, popg=r.popg, bag=b.strip(), outcome=o.strip()))
L = pd.DataFrame(rows); L.to_csv(f'{RES}/map_long.csv', index=False)
cell = L.groupby(['bag', 'outcome', 'evidence']).id.nunique().unstack(fill_value=0); cell.to_csv(f'{RES}/map_cells.csv')
o = dict(n_records=int(len(m)), by_evidence=m.evidence.value_counts().to_dict(), by_pop=m.popg.value_counts().to_dict(),
         by_bag={b: int(L[L.bag == b].id.nunique()) for b in L.bag.unique()}, by_outcome={k: int(L[L.outcome == k].id.nunique()) for k in L.outcome.unique()},
         pain_or_symptom_outcomes=int(L.outcome.isin(['pain', 'discomfort']).sum()),
         n_reported=dict(median=float(m.n.median()), min=float(m.n.min()), max=float(m.n.max()), k=int(m.n.notna().sum())),
         field_studies=int(m.population.str.contains('own bag|mail carriers|postal|firefighters|workers').sum()))
json.dump(o, open(f'{RES}/map_summary.json', 'w'), indent=1); print(json.dumps(o, indent=1)); print(cell)
