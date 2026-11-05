"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
C = json.load(open(f'{RES}/comparison.json')); Z = json.load(open(f'{RES}/citations.json')); S = json.load(open(f'{RES}/selection.json'))
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
R = C['journal_only_vs_rest']['reasons']
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Retractions in nutrition and obesity research', fontsize=19, weight='bold', color=INK)
fig.text(0.04, 0.83, f"{S['n_primary']} retracted papers in the Crossref Retraction Watch database, compared with the other {C['primary_vs_rest']['n_comp']:,}",
         fontsize=10.5, color=MUTED)
rows = [('Any misconduct flagged', f"{100 * R['misconduct']['p']:.0f}% vs {100 * R['misconduct']['p_comp']:.0f}%", 'journal articles: nutrition vs rest', BLUE),
        ('Error, no misconduct flag', f"{100 * R['error_only']['p']:.0f}% vs {100 * R['error_only']['p_comp']:.0f}%", 'journal articles: nutrition vs rest', ORANGE),
        ('Still cited after retraction', f"{100 * Z['field']['any_post']:.0f}%", f"retracted 2012–2023; matched sample {100 * Z['comparison']['any_post']:.0f}%", GREEN)]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=24, weight='bold', color=col); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.26, 'Among journal articles, nutrition retractions are less often misconduct, paper-mill or peer-review cases', fontsize=10.5, color=INK)
fig.text(0.04, 0.20, 'and more often errors, ethics or authorship problems. About three in four were cited again after the', fontsize=10.5, color=INK)
fig.text(0.04, 0.14, 'retraction year, much as matched biomedical retractions were.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Data to 28 Oct 2026 · Citation counts from OpenAlex · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
