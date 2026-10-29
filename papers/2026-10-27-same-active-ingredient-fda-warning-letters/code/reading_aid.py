"""Reading aid used for pass 2: replaces sentences that occur verbatim in >= 4 letters (and are >= 50 characters)
with a tag [Bn], writes the legend of tagged sentences and the compressed letters in reading batches.
Output: data/coding/reading_aid/legend.txt, c00.txt ... (not used by the analysis)."""
import os, re, collections
import pandas as pd
from common import RES, LETTERS, CODING

OUT = os.path.join(CODING, 'reading_aid'); os.makedirs(OUT, exist_ok=True)
d = pd.read_csv(f'{RES}/corpus_index.csv')
def body(t):
    p = [x.start() for x in re.finditer('WARNING LETTER', t)]
    if len(p) >= 2: t = t[p[1]:]
    return re.sub(r'\s+', ' ', t)
def sents(t): return re.split(r'(?<=[.;:”"\]])\s+(?=[A-Z“"\[(0-9])', t)
C = collections.Counter(); S = {}
for i, m in d.iterrows():
    S[i] = sents(body(open(f'{LETTERS}/{m.slug}.txt').read()))
    for s in set(S[i]): C[s] += 1
bp = {s: j for j, (s, c) in enumerate(sorted([(s, c) for s, c in C.items() if c >= 4 and len(s) >= 50], key=lambda x: -x[1]))}
with open(f'{OUT}/legend.txt', 'w') as f:
    for s, j in bp.items(): f.write(f'[B{j}] (n={C[s]}) {s}\n')
k = 0; buf = []; size = 0
for i, m in d.iterrows():
    out = ' '.join(f'[B{bp[s]}]' if s in bp else s for s in S[i])
    buf.append(f"\n\n#### [{i}] {m.slug} | issued {m.issued} | {m.company} | SUBJ: {m.subject}\n{out}"); size += len(buf[-1])
    if size > 70000: open(f'{OUT}/c{k:02d}.txt', 'w').write(''.join(buf)); buf = []; size = 0; k += 1
if buf: open(f'{OUT}/c{k:02d}.txt', 'w').write(''.join(buf))
print(len(bp), 'tagged sentences')
