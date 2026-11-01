"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
R = json.load(open(f'{RES}/meta.json')); P = json.load(open(f'{RES}/prisma.json'))
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
t, s, ts, rep = R['models']['tensile'], R['sensitivity']['tensile']['in_study_comparator_only'], R['ts'], R['reporting']
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'What chrome buys', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, 'Chrome-free vs chrome-tanned leather in the same study: a meta-analysis of laboratory tests', fontsize=11, color=MUTED)
rows = [('Tensile strength, chrome-free / chrome', f"{t['est']:.2f}", f"95% CI {t['lo']:.2f}–{t['hi']:.2f} ({t['k_studies']} studies)", BLUE),
        ('Shrinkage temperature', f"{ts['md_median_arm']:.0f} °C", f"median; chrome-free lower in all {ts['n_arms']} arms", GREEN),
        ('Studies stating hide matching', f"{rep['matched_stated']} of {rep['n_studies']}", f"n stated for every arm in {rep['n_stated_all_arms']}", ORANGE)]
for i, (k, v, sub, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10, color=MUTED); fig.text(x, 0.48, v, fontsize=24, weight='bold', color=col); fig.text(x, 0.41, sub, fontsize=9, color=MUTED)
fig.text(0.04, 0.24, f"{P['studies_included']} studies from {P['records_identified']:,} records. With an in-study chrome control the tensile ratio was {s['est']:.2f} ({s['lo']:.2f}–{s['hi']:.2f}).", fontsize=10.5, color=INK)
fig.text(0.04, 0.18, 'Elongation and tear: too few studies to pool with confidence. Life-cycle studies are too unlike to pool.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Preprint, not peer reviewed · Author owns a leather-goods business (see COI)', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
