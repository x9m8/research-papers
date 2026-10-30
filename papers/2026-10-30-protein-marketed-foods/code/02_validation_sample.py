"""Draw the pre-registered random sample of 300 protein-named (E2) products for manual coding of name precision."""
import pandas as pd
from common import *
d = pd.read_pickle(f'{DER}/products.pkl')
s = d[d.E2].sample(300, random_state=SEED)[['fdc_id', 'branded_food_category', 'description', 'brand_name', 'subbrand_name', 'E1']]
s.to_csv(f'{RES}/validation_sample.csv', index=False)
print(len(s))
