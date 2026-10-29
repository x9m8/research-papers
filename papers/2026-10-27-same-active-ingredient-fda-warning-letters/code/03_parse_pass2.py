"""Convert the pass-2 reading log (data/coding/pass2_reader_log.txt) to data/coding/pass2_reader.csv.
Log format: index | eligible | exclusion | seller_type | space-separated codes present | note
(index = row of results/corpus_index.csv, which is sorted by issue date then company)."""
import pandas as pd
from common import RES, CODING, CODES

idx = pd.read_csv(f'{RES}/corpus_index.csv')
rows = []
for line in open(f'{CODING}/pass2_reader_log.txt'):
    if not line[:1].isdigit():
        continue
    i, el, ex, st, codes, note = [x.strip() for x in line.rstrip('\n').split('|', 5)]
    cs = set(codes.split())
    bad = cs - set(CODES)
    assert not bad, (i, bad)
    r = dict(slug=idx.slug[int(i)], eligible=int(el), exclusion=ex, seller_type=st, note=note)
    r.update({c: int(c in cs) for c in CODES})
    rows.append(r)
df = pd.DataFrame(rows)
assert len(df) == len(idx) and df.slug.is_unique
df.to_csv(f'{CODING}/pass2_reader.csv', index=False)
print(df.eligible.value_counts().to_dict(), df.seller_type.value_counts().to_dict())
