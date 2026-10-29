import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = f'{ROOT}/data/raw'; RES = f'{ROOT}/results'; FIG = f'{ROOT}/figures'
# DRI reference body weights used to set the protein RDA (0.8 g/kg -> 56 g men, 46 g women)
REFWT = {'M': 70.0, 'F': 57.0}
# RDA/AI adults 31-50 (NASEM DRI summary tables). nutrient column -> (men, women)
MIN = {
 'Vitamin A, RAE (mcg_RAE)': (900, 700), 'Vitamin C (mg)': (90, 75), 'Vitamin D (D2 + D3) (mcg)': (15, 15),
 'Vitamin E (alpha-tocopherol) (mg)': (15, 15), 'Vitamin K (phylloquinone) (mcg)': (120, 90), 'Thiamin (mg)': (1.2, 1.1),
 'Riboflavin (mg)': (1.3, 1.1), 'Niacin (mg)': (16, 14), 'Vitamin B-6 (mg)': (1.3, 1.3), 'Folate, DFE (mcg_DFE)': (400, 400),
 'Vitamin B-12 (mcg)': (2.4, 2.4), 'Choline, total (mg)': (550, 425), 'Calcium (mg)': (1000, 1000), 'Phosphorus (mg)': (700, 700),
 'Magnesium (mg)': (420, 320), 'Iron\n(mg)': (8, 18), 'Zinc\n(mg)': (11, 8), 'Copper (mg)': (0.9, 0.9), 'Selenium (mcg)': (55, 55),
 'Potassium (mg)': (3400, 2600), '18:2\n(g)': (17, 12), '18:3\n(g)': (1.6, 1.1)}
# Upper limits (UL; sodium = CDRR) applied to food intake
MAX = {'Sodium (mg)': 2300, 'Retinol (mcg)': 3000, 'Calcium (mg)': 2500, 'Iron\n(mg)': 45, 'Zinc\n(mg)': 40, 'Copper (mg)': 10,
       'Selenium (mcg)': 400, 'Folic acid (mcg)': 1000, 'Vitamin C (mg)': 2000, 'Phosphorus (mg)': 4000}
FIBRE_PER_1000 = 14.0; FIBRE_AI = {'M': 38, 'F': 25}
TFP_WEEK_JUNE2026 = {'M': 73.50, 'F': 58.50}   # USDA Thrifty Food Plan, June 2026, age 20-50
EXCL_MAIN = {7208, 5404, 9802, 7804, 7502, 7504, 7506, 7702, 7704, 7802, 9602, 9999} | set(range(9002, 9407))
EXCL_SENS = {7804, 7502, 7504, 7506, 7702, 7704, 7802, 9602, 9999} | set(range(9002, 9407))
BEVERAGE = set(range(1002, 1405)) | set(range(7002, 7305))
BEV_GROUPS = {10, 12, 14, 70, 71, 72, 73}
# Thrifty Food Plan, June 2026, weekly cost for individuals in four-person families; one-person households +20% (report footnote).
TFP_WEEK_51_70 = {'M': 64.80, 'F': 54.50}
TFP_DAY_SINGLE = {s: (TFP_WEEK_51_70[s] * 1.2 / 7, TFP_WEEK_JUNE2026[s] * 1.2 / 7) for s in 'MF'}   # (ages 51-70, ages 20-50)
