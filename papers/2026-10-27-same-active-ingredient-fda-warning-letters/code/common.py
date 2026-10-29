import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW = os.path.join(ROOT, 'data', 'raw')
RES = os.path.join(ROOT, 'results')
FIG = os.path.join(ROOT, 'figures')
CODING = os.path.join(ROOT, 'data', 'coding')
LETTERS = os.path.join(ROOT, 'data', 'letters')
os.makedirs(RES, exist_ok=True); os.makedirs(FIG, exist_ok=True); os.makedirs(CODING, exist_ok=True)

# Policy events (FDA, "FDA clarifies policies for compounders as national GLP-1 supply begins to stabilize")
EVENTS = [
    ('2024-10-02', 'Tirzepatide shortage declared resolved'),
    ('2024-12-19', 'Tirzepatide resolution reaffirmed'),
    ('2025-02-18', 'Tirzepatide 503A grace period: announced date (extended to the court ruling of 5 Mar 2025)'),
    ('2025-02-21', 'Semaglutide shortage declared resolved'),
    ('2025-03-19', 'Tirzepatide 503B grace period ends'),
    ('2025-04-22', 'Semaglutide 503A grace period: announced date (extended to the court ruling of 24 Apr 2025)'),
    ('2025-05-22', 'Semaglutide 503B grace period ends'),
]
SELLER_TYPES = ['telehealth', '503A', '503B', 'research_chem', 'online_pharmacy', 'clinic_medspa', 'api_supplier', 'other']
SELLER_LABEL = {'telehealth': 'Telehealth platform', '503A': '503A pharmacy', '503B': '503B outsourcing facility',
                'research_chem': 'Research-chemical seller', 'online_pharmacy': 'Online pharmacy', 'clinic_medspa': 'Clinic / med spa',
                'api_supplier': 'API supplier', 'other': 'Other'}
CODES = ['V_unapproved', 'V_misbrand_502bb', 'V_misbrand_502a', 'V_misbrand_502f1', 'V_rx_503b1', 'V_cgmp', 'V_sterility',
         'V_503A_conditions', 'V_503B_conditions', 'V_salt_form', 'V_other_peptide',
         'C_sameness', 'C_generic', 'C_fda_approved', 'C_firm_branded', 'C_research_disguise', 'C_no_rx', 'C_brand_names',
         'F_telehealth_feature', 'F_inspection', 'F_website_review', 'F_shortage']
CODE_LABEL = {
    'V_unapproved': 'Unapproved new drug (505(a))', 'V_misbrand_502bb': 'False/misleading compounded-drug advertising or promotion (502(bb))',
    'V_misbrand_502a': 'False/misleading labeling (502(a))', 'V_misbrand_502f1': 'Inadequate directions for use (502(f)(1))',
    'V_rx_503b1': 'Prescription requirement cited (503(b))', 'V_cgmp': 'CGMP / insanitary conditions (501(a)(2)(B)/(A))', 'V_sterility': 'Sterility assurance',
    'V_503A_conditions': '503A conditions not met', 'V_503B_conditions': '503B conditions not met', 'V_salt_form': 'Salt form / ineligible API',
    'V_other_peptide': 'Retatrutide or other unapproved incretin',
    'C_sameness': '"Same as" / same active ingredient claim', 'C_generic': '"Generic" claim', 'C_fda_approved': 'Implied FDA approval claim',
    'C_firm_branded': 'Firm-branded product', 'C_research_disguise': '"Research use" / not for human consumption', 'C_no_rx': 'Offered without prescription',
    'C_brand_names': 'Use of approved brand names', 'F_telehealth_feature': 'Telehealth / online prescribing features',
    'F_inspection': 'Inspection-based', 'F_website_review': 'Website / social media review', 'F_shortage': 'Shortage-list status of recipient\'s product'}
