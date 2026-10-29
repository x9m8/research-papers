"""Graphical abstract, 900 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
M = json.load(open(f'{RES}/map_summary.json'))
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Bags and the body', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, 'One-shoulder, cross-body and hand-carried bags in adults: what the evidence covers', fontsize=11, color=MUTED)
rows = [('Records mapped', f"{M['n_records']}", f"{M['by_evidence']['Full text, included']} included in full text", BLUE),
        ('Median sample size', f"{M['n_reported']['median']:g}", 'young students, lab walking, minutes', ORANGE),
        ('Records measuring pain', '0', 'of 60 charted (40 from abstracts)', GREEN)]
for i, (k, v, s, c) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=26, weight='bold', color=c); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.24, 'Most consistent finding: a one-shoulder bag at 10% of body weight raises strap-side upper trapezius', fontsize=10.5, color=INK)
fig.text(0.04, 0.18, 'activity (g = 0.94 to 1.25) and opposite-side back-muscle activity (g = 0.59 to 0.95) in two studies.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Scoping review, Europe PMC + grey literature, searched 20 Oct 2026', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
