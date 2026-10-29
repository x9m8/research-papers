# Citation audit: validated-exoplanet track-record paper

Independent fact-check, 2026-10-15. Sources used: arXiv abstract/HTML pages, ADS abstract pages, institutional repositories (PSU, Chalmers, Caltech, MIT DSpace, ANU, DOAJ), and the NASA Exoplanet Archive (NEA) System Overview pages and docs. doi.org could not be fetched (rate-limited / blocked), so a DOI is marked verified when a repository record or the arXiv/ADS page for the paper shows that same DOI.

Verdicts: VERIFIED / CORRECTED / UNVERIFIABLE / NOTE (true, but needs a wording caveat).

---

## Section 1. Overturned planets (overturn_reasons.csv)

| Planet | Refuting paper (authors, year) | DOI matches paper | Paper shows what CSV says | Validated by (per NEA) | Verdict |
|---|---|---|---|---|---|
| Kepler-469 b (KOI-126.01) | Carter, Fabrycky, Ragozzine et al. 2011, Science 331, 562 | Yes, 10.1126/science.1201274 (PSU Pure) | Yes. KOI-126 is a triply eclipsing hierarchical triple: two ~0.2–0.25 Msun M dwarfs (1.77 d) orbiting a 1.35 Msun primary every ~34 d (arXiv 1102.0562). NEA lists Kepler-469 b = K00126.01, P = 33.80 d, which is the outer A–BC orbit. | NEA cites Morton+2016 for the parameters only. The page lists the Q1–Q6 KOI table (2013) as first disposition and shows DR25 = FALSE POSITIVE, with no demotion note or refuting reference. | VERIFIED (refuting paper, DOI, predates Morton 2016, same KOI). NOTE: (1) NEA does not cite Carter 2011 as the refutation. (2) exoplanet.eu labels Kepler-469 b as KOI-126.02, which conflicts with NEA's K00126.01. Use NEA. |
| Kepler-470 b (KOI-129.01) | Cañas et al. 2023, ApJS 265, 50 | Yes, 10.3847/1538-4365/acbcbe (arXiv 2302.07713) | Yes. 103 (+4/−7) MJup. NEA note: "Confirmed planet demoted after planet mass revised >30 MJup in ref." | Morton+2016 | VERIFIED |
| Kepler-486 b (KOI-189.01) | Díaz et al. 2014, A&A 572, A109 | Yes, 10.1051/0004-6361/201424406 (arXiv 1410.5248) | Yes. KOI-189 B = 0.0745 ± 0.0033 Msun ≈ 78 MJup, a very-low-mass star. | Morton+2016 | VERIFIED. Refutation (2014) predates Morton 2016; same KOI. |
| Kepler-488 b (KOI-194.01) | Li & Shporer 2024, AJ 167, 245 | Yes, 10.3847/1538-3881/ad3807 (DOAJ) | Mostly. The secondary eclipse is "unphysically large for a planet", so the object is "likely" a misclassified red dwarf. The paper's wording is hedged. NEA: "Confirmed planet signal refuted in ref." | Morton+2016 | VERIFIED. NOTE: the paper says "likely", so soften "self-luminous companion (M dwarf)" to "likely M dwarf". |
| Kepler-492 b (KOI-205.01) | Díaz et al. 2013, A&A 551, L9 | Yes, 10.1051/0004-6361/201321124 (arXiv 1302.2628) | Yes. Brown dwarf, 39.9 ± 1.0 MJup. | Morton+2016 | VERIFIED. Refutation (2013) predates Morton 2016; same KOI. |
| Kepler-494 b (KOI-219.01) | Cañas et al. 2023 | Yes | Yes. 37 (+4/−2) MJup per NEA. | Morton+2016 | VERIFIED |
| Kepler-503 b (KOI-242.01) | Cañas et al. 2018, ApJL 861, L4 | Yes, 10.3847/2041-8213/aacbc5 (PSU Pure) | Yes. 0.075 ± 0.003 Msun ≈ 78.6 ± 3.1 MJup, at the H-burning limit. | NEA overview gives the Q1–Q6 KOI table (2013) as first-listing reference; Morton+2016 supplies the radius. | VERIFIED (~79 MJup is fine). NOTE: the NEA page I read did not explicitly credit Morton+2016 as the validation paper. Check the archive's `disc_refname` field. |
| Kepler-628 b (KOI-631.01) | Cañas et al. 2023 | Yes | Yes. 92 ± 3 MJup. | Morton+2016 | VERIFIED |
| Kepler-699 b (KOI-846.01) | Niraula, Shporer, Wong & de Wit 2022, AJ 163, 172 | Yes, 10.3847/1538-3881/ac4f64 (MIT DSpace) | Yes. Inferred radius is too large for a planet given the irradiation. | Morton+2016 | VERIFIED. NOTE: NEA's demotion note uses the boilerplate "mass revised >30 MJup", but the paper's argument is the radius/irradiation one. The CSV is correct; flag the inconsistency if you quote NEA. |
| Kepler-706 b (KOI-855.01) | Cañas et al. 2023 | Yes | Yes. 93 (+2/−1) MJup. | Morton+2016 | VERIFIED |
| Kepler-807 b (KOI-1288.01) | Cañas et al. 2023 | Yes | Yes. 78 ± 4 MJup. | Morton+2016 | VERIFIED |
| Kepler-840 b (KOI-1416.01) | Niraula et al. 2022 | Yes | Yes. Same radius/irradiation argument. | Morton+2016 | VERIFIED. Same NEA boilerplate caveat as Kepler-699 b. |
| Kepler-854 b (KOI-1450.01) | Niraula et al. 2022 | Yes | Yes. Radius argument, plus a non-planetary mass from ellipsoidal variation. | Morton+2016 | VERIFIED |
| K2-51 b | Shporer et al. 2017, ApJL 847, L18 | Yes, 10.3847/2041-8213/aa8bff (ANU repository) | Yes. Companion is 0.146 Msun. | Shporer+2017 says "validated by Crossfield et al. 2016". NEA discovery credit is Vanderburg+2016. | VERIFIED |
| K2-67 b | Shporer et al. 2017 | Yes | Yes. 0.161 Msun. | As above. NEA credits Vanderburg+2016. | VERIFIED |
| K2-76 b | Shporer et al. 2017 | Yes | Yes. 0.094 Msun (0.0942 ± 0.0019). | As above. NEA credits Vanderburg+2016 (ApJS 222, 14). | VERIFIED. NOTE: Vanderburg+2016 is a candidate catalog ("234 planetary candidates") and validates nothing. The archive's "discovery" credit is the detection, not the validation. Say so explicitly. |
| K2-78 b | Cabrera et al. 2017, A&A 606, A75 | Yes, 10.1051/0004-6361/201731233 | Yes. Background eclipsing binaries inside the K2 aperture but outside the high-resolution imaging field. | Crossfield+2016 | VERIFIED |
| K2-82 b | Cabrera et al. 2017 | Yes | Yes | Crossfield+2016 | VERIFIED |
| K2-92 b | Cabrera et al. 2017 | Yes | Yes | Crossfield+2016 | VERIFIED |
| K2-256 b | Lehmann & Vanderburg 2024, Open J. Astrophys. | 10.33232/001c.117415. The article ID 117415 matches astro.theoj.org/article/117415 (same title). | Yes. The signal comes from the bright (Kp = 10.4) eclipsing binary EPIC 228967671, 78.1″ away (19.5 pixels). | Livingston+2018a (AJ 156, 78) | VERIFIED |
| K2-399 b | Lillo-Box et al. 2024, A&A 689, L8 | Yes, 10.1051/0004-6361/202451398 (Chalmers) | Yes. Hierarchical eclipsing binary: an early G dwarf plus an eclipsing M-dwarf pair (~846.6 d outer period). The original validation FPP was 0.078%. | Christiansen+2022 (AJ 163, 244) | VERIFIED |

Extra Section 1 finding: Niraula et al. 2022 also say Kepler-747 b is "possibly" not a planet. Check whether NEA has demoted it. If it has, the CSV is missing a row.

---

## Section 2. Validation papers: bibliography and method

| Paper | Bibliographic check | Method check | Verdict |
|---|---|---|---|
| Rowe et al. 2014 | ApJ 784, 45; DOI 10.1088/0004-637X/784/1/45 | Multiplicity boost: 851 planets in 340 systems, >99% confidence, no spectroscopy or imaging required. | VERIFIED |
| Morton et al. 2016 | ApJ 822, 86; DOI 10.3847/0004-637X/822/2/86 | vespa. Validated if FPP < 1%. 1,935 KOIs pass, of which 1,284 are new. | VERIFIED |
| Armstrong, Gamper & Damoulas 2021 | MNRAS 504, 5327–5344; DOI 10.1093/mnras/staa2498 | Machine learning (Gaussian process classifier plus others), 50 new Kepler planets, cross-checked against vespa. | VERIFIED |
| Valizadegan et al. 2022 | ApJ 926, 120; DOI 10.3847/1538-4357/ac4399 | ExoMiner deep learning, 301 new planets. | VERIFIED |
| Valizadegan et al. 2023 | AJ 166, 28; DOI 10.3847/1538-3881/acd344 | ExoMiner score plus a multiplicity boost (logistic regression). Validated if the boosted score is > 0.99. 69 new planets. | VERIFIED (exactly 69) |
| Montet et al. 2015 | ApJ 809, 25; DOI 10.1088/0004-637X/809/1/25 | vespa. 21 validated, 17 for the first time. | VERIFIED |
| Crossfield et al. 2016 | ApJS 226, 7; DOI 10.3847/0067-0049/226/1/7 | vespa, FPP < 0.01 (arXiv 1607.05263). 104 validated. | VERIFIED |
| Vanderburg et al. 2016 | ApJS 222, 14; DOI 10.3847/0067-0049/222/1/14 | Candidate catalog only (234 candidates). No statistical validation. | CORRECTED if the paper lists it as a validation paper. It is a detection/candidate paper. |
| Sinukoff et al. 2016 | ApJ 827, 78; DOI 10.3847/0004-637X/827/1/78. Title: "Eleven Multiplanet Systems from K2 Campaigns 1 and 2…" | 24 validated at >99% confidence and 2 confirmed by mass. The abstract names no tool. | PARTLY VERIFIED. Tool UNVERIFIABLE from the abstract. |
| Dressing et al. 2017 | AJ 154, 207; DOI 10.3847/1538-3881/aa89f2 | vespa. 18 validated (8 new). | VERIFIED |
| Mayo et al. 2018 | AJ 155, 136; DOI 10.3847/1538-3881/aaadff | vespa. Threshold is FPP < 0.1% (stricter than 1%). 149 validated. | VERIFIED. CORRECT any text that gives this paper a 1% threshold. |
| Livingston et al. 2018a | AJ 156, 78; DOI 10.3847/1538-3881/aaccde | 44 validated in C10. The abstract says "statistical false positive probabilities" without naming a tool. Same group and pipeline as 2018b (vespa). | VERIFIED (bibliography). Tool is likely vespa, but not confirmed from the abstract. |
| Livingston et al. 2018b | AJ 156, 277 | vespa, FPP < 1% (multiplicity boost available but not needed). 60 validated. | VERIFIED |
| Hirano et al. 2018 | AJ 155, 127; DOI 10.3847/1538-3881/aaa9c1 | 16 validated (12 new) around low-mass stars. vespa appears in the software credits, but I could not read the validation section. | PARTLY VERIFIED |
| Heller, Hippke & Rodenbeck 2019 | A&A 627, A66; DOI 10.1051/0004-6361/201935600 | vespa, FPP < 1%. 17 new planets. | VERIFIED |
| Castro González et al. 2020 | MNRAS 499, 5416; DOI 10.1093/mnras/staa2353. Title: "Planetary candidates transiting cool dwarf stars from Campaigns 12 to 15 of K2" | vespa, FPP < 1% plus SNR > 10. 12 validated. | VERIFIED |
| de Leon et al. 2021 | MNRAS 508, 195–218; DOI 10.1093/mnras/stab2305. "37 new validated planets in overlapping K2 campaigns" | vespa, FPP < 1%. | VERIFIED |
| Christiansen et al. 2022 | AJ 163, 244; DOI 10.3847/1538-3881/ac5c4c | vespa (v0.6), FPP < 1%. 60 new. Includes K2-399 b. | VERIFIED |
| Giacalone et al. 2021 | AJ 161, 24; DOI 10.3847/1538-3881/abc6af. Title: "Vetting of 384 TESS Objects of Interest with TRICERATOPS and Statistical Validation of 12 Planet Candidates" | TRICERATOPS. Validated if FPP < 0.015 and NFPP < 10⁻³. | VERIFIED. Note the threshold is 1.5%, not 1%. |
| Giacalone et al. 2022 | AJ 163, 99; DOI 10.3847/1538-3881/ac4334. "Validation of 13 Hot and Potentially Terrestrial TESS Planets" | TRICERATOPS plus DAVE. | VERIFIED |
| Mistry et al. 2023 (VaTEST I) | MNRAS 521, 1066; DOI 10.1093/mnras/stad543. TOI-181 b. | Both vespa and TRICERATOPS. | NOTE: label it "vespa + TRICERATOPS", not TRICERATOPS alone. |
| Mistry et al. 2023 (VaTEST II) | AJ 166, 9; DOI 10.3847/1538-3881/acd548 | TRICERATOPS. 11 planets. | VERIFIED |
| Mistry et al. 2024 (VaTEST III) | PASA 41, e030; DOI 10.1017/pasa.2024.29 | TRICERATOPS. 8 planets. | VERIFIED |
| Hord et al. 2024 | AJ 167, 233; DOI 10.3847/1538-3881/ad3068 | Both vespa and TRICERATOPS, with TRICERATOPS weighted more when they disagree. Published: 18 validated, 31 marginal. arXiv v1 had 23 and 33. | NOTE: label it "vespa + TRICERATOPS". Use the published counts. |
| Lafarga et al. 2026 | arXiv:2603.22597 (v2, Apr 2026). No journal reference found. | RAVEN: a machine-learning classifier trained on simulations, then statistical validation. 118 validated (31 newly detected). | VERIFIED as a preprint. Method is ML (RAVEN), not vespa or TRICERATOPS. |
| Collier et al. 2026 | arXiv:2608.21560 (v1 21 Aug 2026, v3 exists). No journal reference found. | Automated TRICERATOPS pipeline. 64 new TESS planets. About 72% of 68 imaging-dependent validations fail without contrast curves. | VERIFIED as a preprint |

FPP2 column, Livingston et al. 2018b (VizieR J/AJ/156/277): UNVERIFIABLE. The VizieR ReadMe was blocked (robots / Anubis). The published Table 2 (MIT DSpace PDF) has a single "FPP" column. The paper does describe a multiplicity boost (×25 for 2-candidate systems, ×100 for ≥3) applied to the planet prior. FPP2 is therefore plausibly the multiplicity-boosted FPP, but I could not confirm this. Read the ReadMe by hand before using the column.

---

## Section 3. NASA Exoplanet Archive criteria

| Claim | Finding | Verdict |
|---|---|---|
| NEA mass ceiling: 30 MJup, mass or minimum mass, "plus uncertainties" | https://exoplanetarchive.ipac.caltech.edu/docs/exoplanet_criteria.html (last update 6 Dec 2024): "The mass (or minimum mass) is equal to or less than 30 Jupiter masses." The page says nothing about uncertainties near this criterion. | CORRECTED. Drop "plus uncertainties", or cite a different source for it. |
| 13 MJup deuterium-burning limit, IAU working definition | Lecavelier des Etangs & Lissauer 2022 (arXiv 2203.09520) give the IAU Commission F2 definition as amended in Aug 2018: the deuterium-fusion limit is "currently calculated to be 13 Jupiter masses for objects of solar metallicity", plus a mass ratio < ~1/25 (L4/L5 stability). | VERIFIED. Journal reference not confirmed from the page (Elsevier template; likely New Astron. Rev.). |

---

## Section 4. Prior work

| Item | Finding | Verdict |
|---|---|---|
| Morton & Johnson 2011, ApJ 738, 170 | DOI 10.1088/0004-637X/738/2/170. "Almost every candidate has FPP <10%, and over half have FPP <5%." | VERIFIED |
| Fressin et al. 2013, ApJ 766, 81 | DOI 10.1088/0004-637X/766/2/81. Global FP rate 9.4%, peaking at 17.7% for giants (6–22 R⊕). | VERIFIED |
| Santerne et al. 2012, A&A 545, A76 | DOI 10.1051/0004-6361/201219608. FP rate 34.8 ± 6.5% for close-in giant candidates (depth > 0.4%, P < 25 d, Kp < 14.7). | VERIFIED |
| Santerne et al. 2016, A&A 587, A64 | DOI 10.1051/0004-6361/201527329. FP rate 54.6 ± 6.5% for giant candidates "within 400 days of period". | CORRECTED wording. The sample is giants with P < 400 d, not "close-in". The ~55% figure is right. |
| Burke et al. 2019, AJ 157, 143 | DOI 10.3847/1538-3881/aafb79. Authors: Burke, Mullally, Thompson, Coughlin, Rowe. Using DR25 and systematic false alarms, Kepler-452 b and Kepler-186 f no longer reach 99% confidence. Kepler-443 b, 441 b, 1633 b, 1178 b and 1653 b have a non-negligible chance of dropping below 99%. Argues that validation must model systematic false alarms near the detection threshold. | VERIFIED (both Kepler-452 b and Kepler-186 f). NOTE: NEA kept Kepler-452 b in the confirmed table, flagged "Controversial" (docs/kepler452b.html). |
| Mullally et al. 2018, AJ 155, 210 | DOI 10.3847/1538-3881/aabae3. Title: "Kepler's Earth-like Planets Should Not Be Confirmed without Independent Detection: The Case of Kepler-452b". Instrumental false alarms dominate at low SNR, so Kepler-452 b cannot be statistically validated. Argues that confidence for other small habitable-zone validated planets is likely overstated. | VERIFIED. The paper is specifically about Kepler-452 b; cite it for that. |
| Morton 2012, ApJ 761, 6 | DOI 10.1088/0004-637X/761/1/6. "An Efficient Automated Validation Procedure for Exoplanet Transit Candidates". Introduces the FPP framework. | VERIFIED, with a NOTE: the name "vespa" does not appear in the 2012 paper. vespa is the later public package (Morton 2015, ASCL). Say "framework later released as vespa". |
| Stanford 2006 | Exceeding Our Grasp: Science, History, and the Problem of Unconceived Alternatives, Oxford UP, 2006. | VERIFIED |
| Mayo 2018 | Statistical Inference as Severe Testing: How to Get Beyond the Statistics Wars, Cambridge UP, 2018. | VERIFIED (add the subtitle) |
| Douglas 2000 | Philosophy of Science 67(4): 559–579; DOI 10.1086/392855. | VERIFIED |
| Leonelli 2016 | Data-Centric Biology: A Philosophical Study, University of Chicago Press, 2016. | VERIFIED |
| Archive reference | Akeson et al. 2013, PASP 125, 989; DOI 10.1086/672273 (VERIFIED). Newer: Christiansen et al. 2025, "The NASA Exoplanet Archive and Exoplanet Follow-up Observing Program: Data, Tools, and Usage", PSJ 6, 186; DOI 10.3847/PSJ/ade3c2 (VERIFIED). | Cite both, or Christiansen 2025 as the current reference. |

### Prior systematic studies of overturned validated planets (novelty check)

I searched with extended web search across arXiv, ADS and journal sites, using phrasings such as "how many statistically validated planets were later refuted", "validated planets later shown false positive", "track record / reliability / census of validation", "overturned / demoted". No paper turned up that systematically counts, across validation papers, how many statistically validated planets were later overturned.

The nearest related work:
- Shporer et al. 2017; Cabrera et al. 2017; Niraula et al. 2022; Lillo-Box et al. 2024. Case refutations, each arguing that statistical validation can mislead.
- Lehmann & Vanderburg 2024. Ephemeris matching across all K2 candidates finds 43 false positives (~2% of candidates), of which exactly one (K2-256 b) had been validated. Covers one mission and one failure mode, and gives no validated-planet failure rate.
- Burke et al. 2019 and Mullally et al. 2018. Re-evaluate small long-period Kepler planets against systematic false alarms. Not a census of overturned planets.
- Robnik & Seljak 2025 (arXiv 2509.07409). Re-evaluate 47 habitable-zone Kepler candidates with null-signal templates and call Kepler-186 f "marginal or likely false alarm" (20% FAP). Relevant to the discussion; not a census.
- Collier et al. 2026. Counterfactual measure: 72% of imaging-dependent validations would fail without contrast curves. Does not count real-world overturns.

The novelty claim appears to hold, with the caveat that ADS full-text search was not directly available. Cite the papers above as the closest prior work. Robnik & Seljak 2025 in particular is not in the reference list given to me.

## Resolution (15 Oct 2026)
Method labels corrected (VaTEST II/III TRICERATOPS; Hord 2024 vespa + TRICERATOPS; Lafarga 2026 RAVEN; Collier 2026 automated TRICERATOPS). Vanderburg et al. 2016 catalogue no longer treated as a validation paper. Archive criterion cited without "plus uncertainties". Santerne 2016 described as periods below 400 days; Burke 2019 and Mullally 2018 described as in the audit; Kepler-488 b described as "likely" a red dwarf; Kepler-747 b noted in Limitations; Christiansen et al. 2025 added. FPP2 identified from the VizieR column description as the FPP of Livingston et al. 2018b table 2. All references then checked against Crossref (titles, authors, volumes, pages, DOIs); Christiansen et al. 2022 DOI corrected to 10.3847/1538-3881/ac5c4c; Li & Shporer 2024 first author is Li, C.
