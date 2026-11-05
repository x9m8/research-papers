"""Shared paths, field-definition rules, reason groups and helpers (paper 18: retractions in nutrition and obesity research)."""
import os, re, json, hashlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RAW = os.path.join(ROOT, 'data', 'raw', 'retraction_watch.csv')
DER = os.path.join(ROOT, 'data', 'derived')
RES = os.path.join(ROOT, 'results')
FIG = os.path.join(ROOT, 'figures')
SEED = 20261029
DATA_COMMIT = '827665ab699e4a798060b95c40268de417b7f2e1'   # crossref/retraction-watch-data, "Retraction Watch data for 2026-10-28"
DATA_CUTOFF = '2026-10-28'

# ---- field definitions -------------------------------------------------------------------------------------------
# S: Retraction Watch subject code "(BLS) Nutrition" or "(HSC) Nutrition".
SUBJ = re.compile(r'\((?:BLS|HSC)\) Nutrition')
# J: journal title names nutrition, diet, obesity or eating; animal, plant, soil and feed journals excluded.
JOUR_INC = re.compile(r'nutri|dietet|\bdiet\b|\bdietary\b|obes|adipos|appetite|\beating\b|bariatric|vitamin|breastfeed', re.I)
JOUR_EXC = re.compile(r'animal|plant|soil|crop|mycorrhiza|nutrient use|nutrient uptake|livestock|poultry|aquacult|veterinar|\bfeed\b', re.I)
# F: food science/technology journals (title contains "food", "dairy" or "beverage"), used only in a sensitivity check.
JOUR_FOOD = re.compile(r'\bfoods?\b|dairy|beverage', re.I)
# K: article title names a nutrition, diet or obesity topic.
TITLE_KW = re.compile(r'\bnutrition|\bnutritional|\bnutrients?\b|\bdiets?\b|\bdietary\b|\bobes|\boverweight\b|body mass index|\bbmi\b|'
                      r'weight loss|weight gain|weight management|\bcalori|energy intake|\bvitamins?\b|micronutrient|malnutrition|'
                      r'undernutrition|\bstunting\b|\bbreastfe|food intake|food insecurity|\beating\b|\bappetite\b|\bketogenic\b', re.I)
# GLP-1 receptor agonists and other anti-obesity drugs, matched on article titles across the whole database.
GLP1 = re.compile(r'semaglutide|liraglutide|tirzepatide|exenatide|dulaglutide|lixisenatide|\bglp-?1\b|glucagon-like peptide|'
                  r'anti-?obesity (?:drug|medication|agent|pharmaco)|orlistat|phentermine|lorcaserin|naltrexone.?bupropion|sibutramine|rimonabant', re.I)

# ---- reason groups (a record can fall in several) ----------------------------------------------------------------
REASON_GROUPS = {
    'fabrication': ['Falsification/Fabrication of Data', 'Falsification/Fabrication of Image', 'Falsification/Fabrication of Results',
                    'Manipulation of Images', 'Manipulation of Results', 'Manipulation of Data', 'Misconduct by Author',
                    'Misconduct - Official Investigation(s) and/or Finding(s)', 'Investigation by ORI', 'Euphemisms for Misconduct'],
    'plagiarism': ['Plagiarism of/in Article', 'Plagiarism of Text', 'Plagiarism of Data', 'Plagiarism of Image', 'Euphemisms for Plagiarism'],
    'duplication': ['Duplication of/in Article', 'Duplication of Data', 'Duplication of Text', 'Euphemisms for Duplication', 'Salami Slicing'],
    'paper_mill': ['Paper Mill'],
    'peer_review': ['Compromised Peer Review', 'Concerns/Issues about Peer Review', 'Rogue Editor', 'Taken via Peer Review'],
    'computer_generated': ['Computer-Aided Content or Computer-Generated Content'],
    'image': ['Duplication of/in Image', 'Concerns/Issues about Image', 'Manipulation of Images', 'Falsification/Fabrication of Image',
              'Unreliable Image', 'Error in Image', 'Plagiarism of Image'],
    'forged_authorship': ['False/Forged Authorship', 'False/Forged Affiliation'],
    'error': ['Error in Data', 'Error in Analyses', 'Error in Methods', 'Error in Results and/or Conclusions', 'Error in Text',
              'Error in Materials', 'Error in Image', 'Results Not Reproducible', 'Contamination of Cell Lines/Tissues',
              'Error in Cell Lines/Tissues', 'Contamination of Materials'],
    'data_concerns': ['Concerns/Issues about Data', 'Unreliable Data', 'Unreliable Results and/or Conclusions',
                      'Original Data and/or Images not Provided and/or not Available'],
    'ethics_consent': ['Lack of IRB/IACUC Approval and/or Compliance', 'Informed/Patient Consent - None/Withdrawn',
                       'Concerns/Issues about Human Subject Welfare', 'Concerns/Issues about Animal Welfare', 'Ethical Violations by Author'],
    'authorship_dispute': ['Concerns/Issues about Authorship/Affiliation', 'Lack of Approval from Author', 'Lack of Approval from Third Party',
                           'Lack of Approval from Company/Institution', 'Objections by Author(s)'],
    'publisher_error': ['Error by Journal/Publisher', 'Duplication of Content through Error by Journal/Publisher'],
    'limited_info': ['Notice - Limited or No Information', 'Notice - Lack of'],
}
MISCONDUCT_GROUPS = ['fabrication', 'plagiarism', 'duplication', 'paper_mill', 'peer_review', 'computer_generated', 'forged_authorship']
# Mapping sensitivity: reasons added to the composite in the broader misconduct mapping, and one unmapped reason reported on its own.
MISCONDUCT_BROAD_EXTRA = ['Breach of Policy by Author', 'Taken from Dissertation/Thesis', 'Misconduct by Third Party', 'Misconduct by Company/Institution']
REFERENCING = ['Concerns/Issues about Referencing/Attributions']
GROUP_LABELS = {'misconduct': 'Any misconduct (composite)', 'fabrication': 'Fabrication, falsification or manipulation',
                'plagiarism': 'Plagiarism', 'duplication': 'Duplicate publication', 'paper_mill': 'Paper mill',
                'peer_review': 'Compromised peer review or rogue editor', 'computer_generated': 'Computer-generated content',
                'image': 'Image problems', 'forged_authorship': 'Forged authorship or affiliation', 'error': 'Honest error',
                'error_only': 'Error, no misconduct flag', 'data_concerns': 'Data concerns or unreliable results',
                'ethics_consent': 'Ethics approval or consent', 'authorship_dispute': 'Authorship dispute or approval',
                'publisher_error': 'Publisher error', 'limited_info': 'Limited or no information in notice',
                'misconduct_broad': 'Any misconduct, broader mapping', 'referencing': 'Concerns about referencing or attributions (unmapped)'}


def split(v):
    return [x.strip() for x in str(v).split(';') if x.strip()]


def sha256(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def dump(obj, name):
    os.makedirs(RES, exist_ok=True)
    p = os.path.join(RES, name)
    with open(p, 'w') as f:
        json.dump(obj, f, indent=1, sort_keys=True)
        f.write('\n')
    return p
