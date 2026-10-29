import os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
RAW = os.path.join(ROOT, 'data', 'raw'); RES = os.path.join(ROOT, 'results'); FIG = os.path.join(ROOT, 'figures')
# EAR (NASEM; NCBI Bookshelf NBK545442 Table J-1). Keys: nutrient -> {(sex, ageband): value}; sex 1=male 2=female; ageband 19-30,31-50,51-70,71+
EAR = {
 'VARA': {'M': [625]*4, 'F': [500]*4}, 'VC': {'M': [75]*4, 'F': [60]*4}, 'VD': {'M': [10]*4, 'F': [10]*4}, 'ATOC': {'M': [12]*4, 'F': [12]*4},
 'VB12': {'M': [2.0]*4, 'F': [2.0]*4}, 'FDFE': {'M': [320]*4, 'F': [320]*4}, 'CALC': {'M': [800, 800, 800, 1000], 'F': [800, 800, 1000, 1000]},
 'IRON': {'M': [6]*4, 'F': [8.1, 8.1, 5, 5]}, 'MAGN': {'M': [330, 350, 350, 350], 'F': [255, 265, 265, 265]}, 'ZINC': {'M': [9.4]*4, 'F': [6.8]*4}}
AI = {'POTA': {'M': 3400, 'F': 2600}, 'FIBE': {'M': [38, 38, 30, 30], 'F': [25, 25, 21, 21]}, 'CHL': {'M': 550, 'F': 425}, 'VK': {'M': 120, 'F': 90}}
LABEL = {'PROT': 'Protein', 'VARA': 'Vitamin A', 'VC': 'Vitamin C', 'VD': 'Vitamin D', 'ATOC': 'Vitamin E', 'VB12': 'Vitamin B12', 'FDFE': 'Folate',
         'CALC': 'Calcium', 'IRON': 'Iron', 'MAGN': 'Magnesium', 'ZINC': 'Zinc', 'POTA': 'Potassium', 'FIBE': 'Fibre', 'CHL': 'Choline', 'VK': 'Vitamin K', 'KCAL': 'Energy'}
NUTS = ['KCAL', 'PROT'] + list(EAR) + list(AI)
SCEN = {'Baseline': 0.0, 'Liraglutide, −16%': 0.16, 'Semaglutide 1 mg, −24%': 0.24, 'Semaglutide 2.4 mg, −35%': 0.35, 'Oral semaglutide 50 mg, −39%': 0.39}
def ageband(a): return 0 if a < 31 else 1 if a < 51 else 2 if a < 71 else 3
