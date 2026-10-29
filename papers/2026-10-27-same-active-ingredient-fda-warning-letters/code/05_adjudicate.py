"""Adjudication of pass-1/pass-2 disagreements, after re-reading each disputed passage
(the rule's matched text and the surrounding letter text). Decisions are recorded per disagreement in
data/coding/adjudication_log.csv; the final codes are written to results/final_codes.csv.

Reasons by cluster (from re-reading):
"""
import pandas as pd
from common import RES, CODING, CODES

REASON = {
    'V_rx_503b1': 'Rule matched the statutory definition of a prescription drug or the 21 CFR 201.1 labeling note; the letter does not allege dispensing without a prescription (or vice versa).',
    'C_fda_approved': 'Rule matched FDA boilerplate ("imply ... the same as an FDA-approved product", "FDA-approved versions ... on the market") or brand-holder text; or rule missed a quoted approval/authorisation claim or FDA\'s "represent ... FDA-approved" finding (non-ASCII hyphen, "authorized by the FDA", "approval from").',
    'C_sameness': 'Rule matched boilerplate ("same assurances", "the same as an FDA-approved product") rather than a quoted recipient claim; or missed claims phrased "active ingredient in", "main ingredient in", "bioidentical".',
    'C_brand_names': 'Brand names appear only in FDA\'s description of approved products or in a brand-holder letter, not in the recipient\'s marketing.',
    'seller_type': 'Codebook hierarchy applied on re-reading (registered outsourcing facility; med spa/clinic named; research-use labels; API manufacturer).',
    'eligible': 'Letter attributes a semaglutide/tirzepatide/other incretin product to the recipient although named fewer than 3 times (or by code name).',
    'V_cgmp': 'Rule matched the definitional description of the 503A exemptions, not an alleged CGMP violation.',
    'F_shortage': 'Rule matched the general 503B bulks/shortage-list condition or a drug-shortage contact line, not the shortage status of the recipient\'s product.',
    'V_salt_form': 'Salt-form footnote is general, not attributed to the recipient.',
    'V_unapproved': 'Definitional mention of section 505 within the 503A framework; no unapproved-drug charge.',
    'V_misbrand_502f1': 'Definitional mention of 502(f)(1) within the 503A framework; no 502(f)(1) charge.',
    'C_generic': '"generic" appears in a company name or in an unrelated (non-GLP-1) product description.',
    'C_research_disguise': 'Rule missed "in vitro research and educational purposes only"/"Research, Development use only", or matched an unrelated use of "research".',
    'C_firm_branded': 'Rule match was not a firm-branding allegation.',
    'F_telehealth_feature': 'Telehealth appears only in the company name.',
    'F_website_review': 'Review of an eBay storefront counts as website review.',
}
# Cases where re-reading sided with pass 1 (rules) rather than pass 2.
OVERRIDE_PASS1 = {
    ('ralph-defronzo-md-716773-09172025', 'F_inspection'): 'Letter follows an FDA inspection with Form 483.',
    ('guangzhou-huli-technology-co-ltd-dba-fantasy-face-722228-03312026', 'seller_type'): 'eBay storefront = online marketplace, coded online_pharmacy per codebook.',
}
# Post-audit corrections (independent audit, 22 Oct 2026): F_shortage applied consistently -- coded 1 where the letter states
# the shortage-list status of the recipient's own product (ProRx 2026 for tirzepatide; six letters stating retatrutide
# "is not used to compound a drug that appears on the drug shortage list").
for s_ in ['asn-labs-716459-09092025', 'amazing-meds-715506-09092025', 'ea-works-limited-liability-company-dba-trust-labs-715798-09092025',
           'glp-1-solution-715883-09092025', 'genlabmeds-713650-09092025', 'medclub-dr-jenn-712126-09092025']:
    OVERRIDE_PASS1[(s_, 'F_shortage')] = 'Post-audit: letter states retatrutide is not used to compound a drug on the drug shortage list (shortage-list status of the recipient\'s product), consistent with ProRx 2026.'
# Post-audit recodes of codes where both passes agreed (not disagreements): footnote/peripheral bases removed.
POST_AUDIT = {
    ('harbin-jixianglong-biotech-co-ltd-723330-05012026', 'V_sterility'): (0, 'Only basis was endotoxin control of process water for a non-sterile API; not a sterility-assurance failure of a product.'),
}
REASON['F_inspection'] = 'see override'
REASON['V_503A_conditions'] = 'Footnote stating that repackaged drugs are not eligible for the 503A/503B exemptions is a general statement, not a finding that the conditions were not met (reading pass retained; post-audit decision).'
REASON['V_503B_conditions'] = REASON['V_503A_conditions']

p1 = pd.read_csv(f'{CODING}/pass1_rules.csv').set_index('slug')
p2 = pd.read_csv(f'{CODING}/pass2_reader.csv').set_index('slug').loc[p1.index]
dis = pd.read_csv(f'{CODING}/disagreements.csv')
final = p2[['eligible', 'exclusion', 'seller_type'] + CODES].copy()
log = []
for _, r in dis.iterrows():
    key = (r.slug, r.variable)
    if key in OVERRIDE_PASS1:
        val, who, why = p1.at[r.slug, r.variable], 'pass1', OVERRIDE_PASS1[key]
    else:
        val, who, why = p2.at[r.slug, r.variable], 'pass2', REASON[r.variable]
    final.at[r.slug, r.variable] = val
    log.append(dict(slug=r.slug, variable=r.variable, pass1=r.pass1, pass2=r.pass2, final=val, sided_with=who, reason=why))
for (s_, v_), (val_, why_) in POST_AUDIT.items():
    log.append(dict(slug=s_, variable=v_, pass1=p1.at[s_, v_], pass2=p2.at[s_, v_], final=val_, sided_with='post-audit', reason=why_)); final.at[s_, v_] = val_
log = pd.DataFrame(log)
log.to_csv(f'{CODING}/adjudication_log.csv', index=False)
final.loc[final.eligible == 0, 'exclusion'] = final.loc[final.eligible == 0, 'exclusion'].fillna('')
final.reset_index().to_csv(f'{RES}/final_codes.csv', index=False)
print(log.sided_with.value_counts().to_dict(), len(log))
