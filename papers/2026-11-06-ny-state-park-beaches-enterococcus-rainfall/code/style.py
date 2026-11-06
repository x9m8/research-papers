import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker

BLUE, ORANGE, GREEN, YELLOW, INK, MUTED, GRID, LIGHT = (
    '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#0b0b0b', '#52514e', '#e4e3df', '#c9c7c0')
# Waterbody palette used consistently across figures.
WATERBODY_COLOR = {'Atlantic Ocean': BLUE, 'Great South Bay': ORANGE, 'Long Island Sound': GREEN}

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                      'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False,
                      'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'legend.frameon': False,
                      'axes.axisbelow': True})


def save(fig, n, FIG):
    fig.savefig(f'{FIG}/{n}.png', dpi=300, bbox_inches='tight')
    fig.savefig(f'{FIG}/{n}.pdf', bbox_inches='tight')
    plt.close(fig)
