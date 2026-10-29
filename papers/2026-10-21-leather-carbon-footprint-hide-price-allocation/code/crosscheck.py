"""Independent checks of the monthly share against values that do not depend on the PPI scaling.
(1) AMS drop-value reports state the hide's value in $/cwt live; dividing by the monthly Nebraska steer price gives the share directly.
(2) Peel (2024): by-products 6.4% of fed-steer value and the hide 18.4% of by-products on 1 March 2024 (product = 1.18%).
(3) LHCA via trade press: hide 'closer to 1%' of animal value in late April 2020."""
import json, pandas as pd
from common import RES
M = pd.read_csv(f'{RES}/allocation_monthly.csv', index_col=0)
o = {'ams_2025_08': dict(direct=1.38 / M.loc['2025-08', 'ne'], model=M.loc['2025-08', 'share']),
     'ams_2025_09': dict(direct=1.36 / M.loc['2025-09', 'ne'], model=M.loc['2025-09', 'share']),
     'peel_2024_03': dict(direct=0.064 * 0.184, model=M.loc['2024-03', 'share']),
     'lhca_2020_04': dict(direct=0.01, model=M.loc['2020-04', 'share'])}
o = {k: {kk: float(vv) for kk, vv in v.items()} for k, v in o.items()}
json.dump(o, open(f'{RES}/crosscheck.json', 'w'), indent=1); print(json.dumps(o, indent=1))
