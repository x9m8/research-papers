"""Pass 1: deterministic rule-based coder (regular expressions) for the codebook in CODEBOOK.md.

Written and frozen before pass 2 (the reading pass) and not run until pass 2 was complete.
Every rule is a case-insensitive regex applied to the full letter text (data/letters/<slug>.txt)
and, where stated, to the FDA index 'subject' string and company name. No rule was tuned on the
pass-2 codes. Output: data/coding/pass1_rules.csv
"""
import re
import pandas as pd
from common import RES, CODING, LETTERS

I = re.I
GLP_SUBST = r'semaglutide|tirzepatide|retatrutide|cagrilintide|survodutide|mazdutide|liraglutide|dulaglutide|exenatide'
GLP_BRAND = r'ozempic|wegovy|rybelsus|mounjaro|zepbound|saxenda|victoza'
BRAND_HOLDER = r'novo nordisk|eli lilly'

R = {
    # B. violations
    'V_unapproved': r'505\(a\)|355\(a\)|unapproved new drug',
    'V_misbrand_502bb': r'502\(bb\)|352\(bb\)|(502|352)\(a\) and \(bb\)',
    'V_misbrand_502a': r'502\(a\)|352\(a\)',
    'V_misbrand_502f1': r'502\(f\)\(1\)|352\(f\)\(1\)',
    'V_rx_503b1': r'503\(b\)\(1\)|353\(b\)\(1\)',
    'V_cgmp': r'\bCGMP\b|current good manufacturing practice|501\(a\)\(2\)\(B\)|351\(a\)\(2\)\(B\)|insanitary',
    'V_sterility': r'sterility|aseptic|endotoxin|media fill',
    'V_503A_conditions': r'(not|fail\w*)\s+(to\s+)?(meet|satisf\w*|qualify|eligible)[^.]{0,160}503A|503A[^.]{0,160}(not\s+(met|eligible|qualify|satisf)|ineligible)',
    'V_503B_conditions': r'(not|fail\w*)\s+(to\s+)?(meet|satisf\w*|qualify|eligible)[^.]{0,160}503B|503B[^.]{0,160}(not\s+(met|eligible|qualify|satisf)|ineligible)',
    'V_salt_form': r'(semaglutide|tirzepatide)\s+(sodium|acetate)|salt form',
    'V_other_peptide': r'retatrutide|cagrilintide|survodutide|mazdutide',
    # C. claims
    'C_sameness': r'same (active )?ingredients?|same as|identical to|same medication|same medicine|same molecule',
    'C_generic': r'\bgeneric\b',
    'C_fda_approved': r'impl\w*[^.]{0,120}FDA[- ]approv|“[^”]{0,250}FDA[- ](approved|registered|regulated)[^”]{0,250}”|"[^"]{0,250}FDA[- ](approved|registered|regulated)[^"]{0,250}"',
    'C_firm_branded': r'is the compounder|suggesting [^.]{0,80} compounder|obscur\w*|branded with',
    'C_research_disguise': r'research (use|purposes?)|for research|not for human (consumption|use)|research peptides?|research chemicals?',
    'C_no_rx': r'without (a |requiring a |the need for a )?(valid )?prescription|no prescription|prescription (is )?not required',
    'C_brand_names': r'\b(' + GLP_BRAND + r')\b',
    # D. context
    'F_telehealth_feature': r'telehealth|telemedicine|online (consultation|visit|questionnaire|assessment)|affiliated (provider|prescriber|physician)',
    'F_inspection': r'inspect(ed|ion of) your|form fda[- ]?483|fda[- ]?483',
    'F_website_review': r'review(ed)? (of )?your website|internet address|social media|your website',
    'F_shortage': r'shortage',
}
RX = {k: re.compile(v, I) for k, v in R.items()}

def seller_type(company, subject, t):
    c, s = company.lower(), subject.lower()
    if re.search(BRAND_HOLDER, c): return 'brand_holder'
    if 'outsourcing' in s or re.search(r'(you|your (firm|facility|company))[^.]{0,80}register\w*[^.]{0,60}outsourcing facilit', t, I): return '503B'
    if 'compounding' in s or 'pharmacy compounding' in s or re.search(r'inspect\w* your (pharmacy|facility)[^.]{0,200}', t, I) and re.search(r'503A', t): return '503A'
    if 'telehealth' in s or re.search(r'telehealth|telemedicine', t, I): return 'telehealth'
    if re.search(R['C_research_disguise'], t, I): return 'research_chem'
    if 'internet' in s or re.search(r'online pharmacy|internet pharmacy|over the internet', t, I): return 'online_pharmacy'
    if re.search(r'med ?spa|medical spa|wellness (clinic|center)|weight[- ]loss clinic', t, I): return 'clinic_medspa'
    if re.search(r'active pharmaceutical ingredient', t, I) and re.search(r'\bAPI\b', t): return 'api_supplier'
    return 'other'

def main():
    idx = pd.read_csv(f'{RES}/corpus_index.csv')
    out = []
    for _, m in idx.iterrows():
        t = open(f'{LETTERS}/{m.slug}.txt').read()
        n_glp = len(re.findall(GLP_SUBST + '|' + GLP_BRAND, t, I))
        st = seller_type(m.company, m.subject, t)
        # eligibility rule: not the brand holder and at least 3 mentions of a GLP-1 substance or brand name
        elig = int(st != 'brand_holder' and n_glp >= 3)
        reason = 'X1_brand_holder' if st == 'brand_holder' else ('X2_incidental' if n_glp < 3 else '')
        row = dict(slug=m.slug, eligible=elig, exclusion=reason, n_glp_mentions=n_glp, seller_type=st)
        row.update({k: int(bool(rx.search(t))) for k, rx in RX.items()})
        out.append(row)
    pd.DataFrame(out).to_csv(f'{CODING}/pass1_rules.csv', index=False)
    print(pd.DataFrame(out).seller_type.value_counts())

if __name__ == '__main__':
    main()
