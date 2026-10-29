# Codebook: FDA warning letters on compounded and unapproved GLP-1 drugs (paper 13)

Version 1.0, frozen 2026-10-21 before coding of the full corpus. Not pre-registered.

Unit of analysis: one posted FDA warning letter (one letter URL). Every code is binary
(1 = present in the letter text, 0 = absent) except seller type (one category per letter).
Codes describe what **FDA alleged or stated** in the letter. They do not establish that any
violation occurred.

## Eligibility (applied before coding)

- E1 Include: the letter alleges a violation involving a semaglutide-, tirzepatide-, retatrutide-
  or other GLP-1/incretin-containing product that the recipient sold, offered, marketed,
  compounded, repackaged, distributed or supplied.
- X1 Exclude: letter to the NDA/BLA holder of an approved GLP-1 brand (Novo Nordisk, Eli Lilly)
  about its own approved product (promotion, adverse-event reporting). Kept as a comparison set.
- X2 Exclude: GLP-1 term is incidental (mentioned only as background, e.g. in a list of
  unrelated products or a general warning, with no GLP-1 product attributed to the recipient).
- X3 Exclude: duplicate posting of the same letter.

## A. Seller type (single category; hierarchical rule, first match wins)

1. `brand_holder` (excluded set only)
2. `503B` — the letter is addressed to, or treats the firm as, a registered outsourcing facility.
3. `503A` — a compounding pharmacy (state-licensed pharmacy that compounds), not 503B.
4. `telehealth` — a telehealth / online prescribing platform, or a firm marketing compounded
   GLP-1s to consumers via websites where prescriptions are written through affiliated
   prescribers. Telehealth firms that also own a pharmacy are coded `telehealth` if the letter
   is about their consumer marketing and `503A` if it is inspection-based about compounding.
5. `research_chem` — seller of "research peptides" / "research chemicals" / products labelled
   for research use or not for human consumption.
6. `online_pharmacy` — internet pharmacy or website selling drugs to US consumers without the
   telehealth-platform model (often foreign, "rogue" pharmacies), or a marketplace.
7. `clinic_medspa` — med spa, weight-loss clinic or physician practice.
8. `api_supplier` — manufacturer, importer or distributor of active pharmaceutical ingredient.
9. `other`.

## B. Violation codes (FDCA provisions or allegations cited)

- `V_unapproved` — unapproved new drug: section 505(a) / 301(d), "unapproved new drug".
- `V_misbrand_502bb` — section 502(bb): false or misleading advertising/promotion of a
  compounded drug.
- `V_misbrand_502a` — section 502(a): labeling false or misleading in any particular.
- `V_misbrand_502f1` — section 502(f)(1): inadequate directions for use.
- `V_rx_503b1` — section 503(b)(1): prescription drug dispensed without prescription /
  prescription-drug status issue.
- `V_cgmp` — CGMP / insanitary conditions / adulteration under 501(a)(2)(A) or (B).
- `V_sterility` — sterility-assurance problems (aseptic processing, sterility testing,
  endotoxin, media fills, "sterile" products produced without assurance).
- `V_503A_conditions` — FDA states that conditions of section 503A were not met
  (e.g. bulk substance not eligible, "essentially a copy", no valid patient-specific prescription).
- `V_503B_conditions` — FDA states that conditions of section 503B were not met.
- `V_salt_form` — semaglutide/tirzepatide salt forms (sodium, acetate) or API that is not the
  approved component.
- `V_other_peptide` — retatrutide, cagrilintide, survodutide, mazdutide or another
  investigational incretin product attributed to the recipient.

## C. Claim / marketing features (as described or quoted by FDA)

- `C_sameness` — FDA cites claims that the product is the same as, identical to, or contains
  the same active ingredient as an approved brand (Ozempic, Wegovy, Mounjaro, Zepbound).
- `C_generic` — FDA cites the product being called "generic" (e.g. "generic semaglutide").
- `C_fda_approved` — FDA cites claims implying FDA approval, or "FDA-approved",
  "FDA-registered", "FDA-regulated" claims about the product.
- `C_firm_branded` — FDA cites the product being presented under the seller's own name or
  trademark (obscuring the compounder/source).
- `C_research_disguise` — "research use only", "for research purposes", "not for human
  consumption" language attributed to the recipient's products.
- `C_no_rx` — FDA states products were offered without requiring a prescription.
- `C_brand_names` — FDA cites the seller's use of approved brand names or images
  (e.g. "Ozempic", "Wegovy") in marketing a non-approved product.

## D. Context / process codes

- `F_telehealth_feature` — the letter describes the firm's telehealth/online prescribing
  features (online consultation, affiliated prescribers, subscription).
- `F_inspection` — letter based on an FDA inspection (Form 483 cited / "inspected your facility").
- `F_website_review` — letter based on review of a website or social media.
- `F_shortage` — the letter mentions the drug shortage (list) status.
- `F_closeout` — FDA index shows a close-out letter (taken from index metadata, not coded from text).

## Coding procedure

- Pass 1 (rule-based): `code/rules.py`, regular expressions applied to the letter text, fully
  deterministic. Rules are documented inline.
- Pass 2 (reader): the AI model read each letter and recorded codes in
  `data/coding/pass2_reader.csv` without looking at pass-1 output. Where blinding was not fully
  possible (the same model wrote the rules), this is stated in the manuscript.
- Agreement: percent agreement and Cohen's kappa per code (kappa undefined when both passes
  are constant).
- Adjudication: every disagreement was re-read and resolved; decisions logged in
  `data/coding/adjudication_log.csv`. Final codes in `results/final_codes.csv`.
