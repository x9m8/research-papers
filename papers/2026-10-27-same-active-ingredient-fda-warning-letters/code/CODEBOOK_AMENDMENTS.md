# Codebook amendments (after coding; CODEBOOK.md itself is left unchanged so that its recorded hash still matches)

Recorded 22 October 2026, after the independent number/methods audit.

1. **File name.** The rule-based coder is `code/02_rules.py` (CODEBOOK.md says `code/rules.py`).
2. **F_closeout.** Close-out status is taken from the FDA index metadata (`closeout_letter` in `results/corpus_index.csv`) and reported descriptively; it is not one of the 22 coded variables.
3. **X2 (incidental) wording.** As applied, X2 also excludes letters about products marketed with "GLP-1" in the name or claims but with no semaglutide, tirzepatide or other incretin ingredient attributed to them (oral drops, an eBay oral solution, a dietary supplement), as well as letters in which a GLP-1 drug is mentioned only incidentally.
4. **F_shortage.** Operational definition: the letter states the drug-shortage-list status of the recipient's own GLP-1/incretin product (e.g. that tirzepatide was not on the shortage list when compounded, or that retatrutide "is not used to compound a drug that appears on the drug shortage list"). General statements of the 503B shortage-list condition, or FDA contact lines for its Drug Shortages Staff, do not count. Table label: "Shortage-list status of recipient's product".
5. **V_rx_503b1.** Operational definition: the letter cites section 503(b) / 503(b)(1) as a provision violated (in the opening list or the body). The explicit allegation of sale without a prescription is coded separately as C_no_rx. The statutory definition of a prescription drug and the 21 CFR 201.1 labelling note do not count.
6. **V_503A_conditions / V_503B_conditions.** A general footnote stating that repackaged drugs are not eligible for the 503A/503B exemptions does not count as a finding that the conditions were not met.
7. **V_sterility.** Requires a sterility-assurance problem with a drug product (aseptic processing, sterility testing or failures, media fills, endotoxin in a product). Endotoxin control of process water for a non-sterile API does not count.
8. **Eligibility (E1).** A product attributed to the recipient counts even if named once (e.g. a semaglutide lot listed in a disposition table).
