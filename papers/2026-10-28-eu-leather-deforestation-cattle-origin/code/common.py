import os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
RAW = os.path.join(ROOT, 'data', 'raw'); DER = os.path.join(ROOT, 'data', 'derived'); RES = os.path.join(ROOT, 'results'); FIG = os.path.join(ROOT, 'figures')
os.makedirs(DER, exist_ok=True); os.makedirs(RES, exist_ok=True); os.makedirs(FIG, exist_ok=True)
YEARS = list(range(2005, 2024))          # years with DeDuCE v2.1 amortised deforestation
EU = 'EU27'
EU27_ISO2 = 'AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE'.split()

# Stage of each HS02 subheading kept in the analysis.
# 1 raw hides, 2 tanned/crust, 3 finished leather, 4 articles.
STAGE = {}
for k in ['410120', '410150', '410190']: STAGE[k] = 1
for k in ['410411', '410419', '410441', '410449']: STAGE[k] = 2
for k in ['410711', '410712', '410719', '410791', '410792', '410799']: STAGE[k] = 3
for k in ['420100', '420211', '420221', '420231', '420291', '420310', '420321', '420329', '420330', '420340', '420500',
          '640312', '640319', '640320', '640330', '640340', '640351', '640359', '640391', '640399', '640420', '640510']: STAGE[k] = 4
EXTRA3 = ['411420', '411510']   # patent leather and composition leather (411520, leather waste and dust, is left out): stage 3 only in a sensitivity run
BR_YIELDS = [26, 30, 34]   # assumed Brazilian hide yields, kg per head slaughtered (sensitivity; FAOSTAT's imputed yield is 16-27 kg)

# Laroche et al. (2024) supplement, input_data/conversion_factors_leather.csv (Zenodo 10.5281/zenodo.11085413), tonnes raw hide per tonne product.
# HS02 640330 (wooden-base footwear with leather uppers) is not in the HS12 list; it takes the factor of 640399.
def laroche_cf(which='mean'):
    import pandas as pd
    d = pd.read_csv(os.path.join(ROOT, 'data', 'laroche', 'conversion_factors_leather.csv'), dtype={'code.HS6': str})
    cf = dict(zip(d['code.HS6'], d['CF' + which])); cf['640330'] = cf['640399']
    return cf

def cf_set(name):
    """Raw-hide-equivalent factors by HS6 for one named set. Article factors are Laroche's, expressed as finished-leather content
    (Laroche factor / 4.02) times the set's finished-leather factor, so that every set treats an article as its leather content."""
    lm = laroche_cf('mean')
    if name.startswith('Laroche'):
        w = name.split()[-1]; cf = laroche_cf(w); return {k: cf[k] for k in list(STAGE) + EXTRA3 if k in cf}
    if name == 'Commission SWD':
        f = {1: 1.00, 2: 2.33, 3: 4.20}
    elif name == 'UNIDO mass balance':
        f = {1: 1.00, 2: 1000 / 350, 3: 1000 / 255}
    out = {}
    for k, s in STAGE.items():
        if s < 4: out[k] = f[s]
        else: out[k] = lm[k] / 4.02 * f[3]
    for k in EXTRA3: out[k] = f[3] * lm[k] / 4.02
    # crust (dry state, 410441/410449): Laroche treat it as finished-leather weight; the SWD and UNIDO sets use their tanned factor.
    return out
CF_SETS = ['Commission SWD', 'UNIDO mass balance', 'Laroche mean', 'Laroche min', 'Laroche max']
CORE_CF = 'Laroche mean'

RULES = {'By-product (SWD), 2.5%': 0.025, 'PEFCR, 3.5%': 0.035, 'DeDuCE / SWD co-product, 5%': 0.05, 'Mass (SWD), 8%': 0.08,
         'Mass (Laroche et al.), 10%': 0.10}
VAR_RULES = ['Economic, price of the year', 'Mass, FAOSTAT weights']
ALL_RULES = list(RULES) + VAR_RULES
CORE_RULE = 'DeDuCE / SWD co-product, 5%'
