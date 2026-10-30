"""Shared paths, pre-specified text rules and constants for paper 12 (protein-marketed foods)."""
import os, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
RAW = os.path.join(ROOT, 'data', 'raw'); DER = os.path.join(ROOT, 'data', 'derived')
RES = os.path.join(ROOT, 'results'); FIG = os.path.join(ROOT, 'figures')
os.makedirs(DER, exist_ok=True); os.makedirs(RES, exist_ok=True); os.makedirs(FIG, exist_ok=True)
SEED = 20261022
MIN_E2_PER_CATEGORY = 20          # categories analysed: >= 20 protein-named products (US, not discontinued)
US = {'United States', 'US'}

# ---- Exposure tiers (applied to description + brand_name + subbrand_name, case-insensitive) ----
# E2: protein-branded name: the word "protein" anywhere in the product name, brand or sub-brand.
E2_RE = re.compile(r'protein', re.I)
# E1: explicit claim-like wording in the name (a subset of E2).
E1_RE = re.compile(r'high[\s-]*protein|\b\d+(?:\.\d+)?\s*(?:g|gr|gm|grams?)\b\.?\s*(?:of\s+)?protein|protein\s*(?:\+|plus\b)'
                   r'|(?:good|excellent|great|rich)\s+source\s+of\s+protein|(?:extra|added|more|max|double|triple|mega|super)\s+protein'
                   r'|protein[\s-]*(?:rich|packed|powered|boost)', re.I)

# ---- Ingredient markers (lower-cased ingredient statement). Operationalisation informed by the NOVA
# ultra-processed group (Monteiro et al., 2019): substances rarely used in kitchens and cosmetic additive classes.
MARK = {
    'isolate':   r'protein isolate|protein concentrate|isolated (?:soy|pea|whey|milk) protein|whey protein|milk protein|soy protein|pea protein|rice protein'
                 r'|potato protein|wheat protein|egg white protein|beef protein|faba (?:bean )?protein|casein|caseinate|collagen|hydroly[sz]ed (?:\w+ )?protein|protein hydroly[sz]ate',
    'sweetener': r'sucralose|acesulfame|aspartame|saccharin|neotame|advantame|stevia|steviol|rebaudioside|\breb [am]\b|monk ?fruit|luo han guo|mogroside|siraitia'
                 r'|erythritol|maltitol|sorbitol|xylitol|isomalt|lactitol|mannitol|polyglycitol|hydrogenated starch hydrolysate',
    'flavour':   r'flavou?r',
    'enhancer':  r'monosodium glutamate|\bmsg\b|disodium (?:inosinate|guanylate|5)|yeast extract|autoly[sz]ed yeast|hydroly[sz]ed yeast',
    'colour':    r'colou?r|\b(?:red|yellow|blue|green)\s*(?:no\.?\s*|#\s*)?\d+\b|annatto|titanium dioxide|carmine|cochineal|fd ?& ?c',
    'emulsifier': r'lecithin|mono-? ?(?:and|&) ?di-? ?glycerides|monoglyceride|diglyceride|polysorbate|stearoyl lactylate|\bdatem\b|diacetyl tartaric|sucrose esters?'
                  r'|polyglycerol|sorbitan|emulsifier',
    'thickener': r'(?:xanthan|guar|gellan|acacia|arabic|locust bean|carob bean|tara|konjac|cellulose) gum|gum (?:arabic|acacia)|carrageenan|carboxymethyl ?cellulose'
                 r'|methylcellulose|microcrystalline cellulose|cellulose gel|hydroxypropyl|modified (?:food |corn |tapioca |potato |wheat )?starch|\bagar\b|alginate|pectin|thickener|gelling agent',
    'sugar_type': r'high[\s-]fructose corn syrup|maltodextrin|dextrose|invert sugar|\bfructose\b|corn syrup solids|glucose syrup|isoglucose|polydextrose|soluble (?:corn )?fib(?:er|re)'
                  r'|\binulin\b|chicory root fib(?:er|re)|resistant (?:dextrin|starch|maltodextrin)|isomalto-?oligosaccharide|oligofructose',
    'hydrog_oil': r'(?<!starch )\bhydrogenated (?!starch)|interesterified',
}
MARK_RE = {k: re.compile(v, re.I) for k, v in MARK.items()}
COLLAGEN_RE = re.compile(r'collagen|gelatin', re.I)
UPF_CLASSES = ['sweetener', 'flavour', 'enhancer', 'colour', 'emulsifier', 'thickener', 'sugar_type', 'hydrog_oil', 'isolate']

def n_ingredients(s):
    """Approximate count of top-level ingredients: commas outside parentheses/brackets."""
    if not isinstance(s, str) or not s.strip(): return np.nan
    depth, n = 0, 1
    for ch in s:
        if ch in '([{': depth += 1
        elif ch in ')]}': depth = max(0, depth - 1)
        elif ch == ',' and depth == 0: n += 1
    return n

# ---- Package weight parsing -> (amount, kind) in grams ('mass') or millilitres ('volume') ----
UNIT = {'kg': (1000, 'mass'), 'g': (1, 'mass'), 'gm': (1, 'mass'), 'gr': (1, 'mass'), 'grm': (1, 'mass'), 'grams': (1, 'mass'),
        'mg': (0.001, 'mass'), 'ml': (1, 'volume'), 'mlt': (1, 'volume'), 'l': (1000, 'volume'), 'ltr': (1000, 'volume'),
        'oz': (28.349523, 'mass'), 'onz': (28.349523, 'mass'), 'ozn': (28.349523, 'mass'), 'lb': (453.59237, 'mass'), 'lbs': (453.59237, 'mass'),
        'lbr': (453.59237, 'mass'), 'floz': (29.57353, 'volume'), 'fz': (29.57353, 'volume'), 'oza': (29.57353, 'volume'), 'gal': (3785.41, 'volume'),
        'gll': (3785.41, 'volume'), 'qt': (946.353, 'volume'), 'quart': (946.353, 'volume'), 'pt': (473.176, 'volume'), 'pint': (473.176, 'volume')}
PW_RE = re.compile(r'(\d+(?:\.\d+)?)\s*(fl\.?\s*oz|kg|grams|grm|gm|gr|g|mg|mlt|ml|ltr|l|onz|ozn|oza|oz|lbs|lbr|lb|gal|gll|quart|qt|pint|pt|fz)\b', re.I)
METRIC = ('kg', 'g', 'gm', 'gr', 'grm', 'grams', 'ml', 'mlt', 'l', 'ltr')

def parse_package(s):
    if not isinstance(s, str) or not s.strip(): return (np.nan, None)
    hits = [(float(a), re.sub(r'[\s.]', '', u.lower())) for a, u in PW_RE.findall(s)]
    hits = [(a, u) for a, u in hits if u in UNIT and a > 0]
    if not hits: return (np.nan, None)
    met = [h for h in hits if h[1] in METRIC]
    a, u = (met or hits)[0]
    f, kind = UNIT[u]
    return (a * f, kind)

# ---- Whole-food benchmarks: BLS Average Price item -> SR Legacy composition ----
# grams_per_unit: edible grams per BLS pricing unit. SR Legacy portions: large egg 50 g; milk 1 quart = 976 g; yogurt 8 oz container 227 g.
WHOLE = [
    # key, label, BLS item code, unit grams, SR Legacy fdc_ids (protein averaged), benchmark?
    ('eggs', 'Eggs, grade A large (per dozen)', '708111', 12 * 50, ['171287'], True),
    ('milk_whole', 'Milk, whole (per gallon)', '709112', 4 * 976, ['171265'], True),
    ('beans_dry', 'Beans, dried (per lb)', '714233', 453.59237, ['175199', '173734', '173744', '173745', '175190'], True),
    ('chicken_breast', 'Chicken breast, boneless (per lb)', 'FF1101', 453.59237, ['171077'], True),
    ('milk_lowfat', 'Milk, low-fat/reduced/skim (per gallon); 2% composition', 'FJ1101', 4 * 976, ['171267'], False),
    ('ground_beef', 'Ground beef, 100% beef (per lb); 80% lean composition', '703112', 453.59237, ['174036'], False),
    ('ground_beef_lean', 'Ground beef, lean/extra lean (per lb); 90% lean composition', '703113', 453.59237, ['174030'], False),
    ('cheddar', 'Cheddar cheese (per lb)', '710212', 453.59237, ['173414'], False),
    ('yogurt', 'Yogurt (per 8 oz); plain low-fat composition', 'FJ4101', 227, ['170886'], False),
    ('bread_white', 'Bread, white pan (per lb)', '702111', 453.59237, ['174924'], False),
    ('rice_white', 'Rice, white long grain uncooked (per lb)', '701312', 453.59237, ['169756'], False),
]
PRICE_WINDOW = [('2025', 'M10'), ('2025', 'M11'), ('2025', 'M12')] + [('2026', f'M{m:02d}') for m in range(1, 10)]
# Price premium scenarios per 100 g (non-US): news report, consumer organisation, peer-reviewed study
PREMIUM_SCENARIOS = {'The Journal (Ireland, 10 products)': 0.31, 'CHOICE (Australia, 175 products)': 0.50, 'Koop et al. 2024 (Germany, mean, 299 vs 286 products)': 1.32}
