"""Farm-to-slaughter emissions carried by one hide and by 1 m2 of leather made from it, under the annual economic
allocation factor, holding the per-kg-carcass emission factor fixed so that only prices move the result.
kg CO2e per hide = share x EF x carcass weight; m2 per hide = hide weight x m2 per kg raw hide."""
import json, numpy as np, pandas as pd
from common import RES, DATA
P = json.load(open(f'{DATA}/params.json')); Y = pd.read_csv(f'{RES}/allocation_annual.csv').set_index('year')
ef = P['ef_kgco2e_per_kg_cw']['value']; LB = 0.45359237
Y['cw_kg'] = Y.steer_dw * LB; Y['animal_kg'] = ef * Y.cw_kg
Y['hide_kg'] = P['hide_yield_lb_per_cwt_live']['value'] / 100 * Y.steer_lw * LB; Y['m2_hide'] = Y.hide_kg * P['m2_per_kg_raw_hide']['value']
for nm, s in [('econ', Y.share), ('mass', P['mass_alloc_us']['value']), ('pefcr', P['pefcr_econ']['value'])]:
    Y[f'kg_hide_{nm}'] = s * Y.animal_kg; Y[f'kg_m2_{nm}'] = Y[f'kg_hide_{nm}'] / Y.m2_hide
Y['kg_m2_econ_roll5'] = Y.kg_m2_econ.rolling(5).mean()
Y['kg_m2_per_unit_share'] = Y.animal_kg / Y.m2_hide  # constant by construction: EF x CW / (yield x LW x m2/kg), CW/LW fixed at 0.63
Y[['cw_kg', 'animal_kg', 'hide_kg', 'm2_hide', 'kg_hide_econ', 'kg_m2_econ', 'kg_m2_mass', 'kg_m2_pefcr', 'kg_m2_econ_roll5']].to_csv(f'{RES}/carbon_annual.csv')
e, l = Y.loc[2002:2013], Y.loc[2023:2025]
o = dict(ef=ef, animal_kg_2025=float(Y.animal_kg[2025]), m2_hide_2025=float(Y.m2_hide[2025]), hide_kg_2025=float(Y.hide_kg[2025]),
         kg_m2_econ_early=float(e.kg_m2_econ.mean()), kg_m2_econ_late=float(l.kg_m2_econ.mean()), kg_m2_econ_2025=float(Y.kg_m2_econ[2025]),
         kg_m2_econ_max=float(Y.kg_m2_econ.max()), kg_m2_econ_max_year=int(Y.kg_m2_econ.idxmax()),
         kg_m2_mass_2025=float(Y.kg_m2_mass[2025]), kg_m2_pefcr_2025=float(Y.kg_m2_pefcr[2025]),
         kg_hide_econ_early=float(e.kg_hide_econ.mean()), kg_hide_econ_2025=float(Y.kg_hide_econ[2025]),
         kg_m2_mass_mean=float(Y.kg_m2_mass.mean()), kg_m2_econ_roll5_2025=float(Y.kg_m2_econ_roll5[2025]))
# carbon "subsidy" vs mass allocation, national total, 2025: (mass - econ) x hides from steer-type animals, illustrative
o['kg_m2_per_unit_share'] = float(Y.kg_m2_per_unit_share.mean()); o['m2_hide_min'] = float(Y.m2_hide.min()); o['m2_hide_max'] = float(Y.m2_hide.max())
o['ratio_mass_to_econ_2025'] = float(Y.kg_m2_mass[2025] / Y.kg_m2_econ[2025])
json.dump(o, open(f'{RES}/carbon.json', 'w'), indent=1)
print(Y[['cw_kg', 'animal_kg', 'hide_kg', 'm2_hide', 'kg_hide_econ', 'kg_m2_econ', 'kg_m2_mass', 'kg_m2_pefcr']].round(1).to_string()); print(json.dumps(o, indent=1))
