# Citation audit: "What chrome buys" (Paper 15)

Independent citation audit of `pkg/manuscript/manuscript.md` (version 1, October 2026). The auditor did not write the paper. Audit date: 28 October 2026.

Methods: every DOI was checked against the Crossref REST API (`api.crossref.org/works/{DOI}`) through WebFetch, or against DataCite for the Zenodo DOI. Crossref `relation`, `update-to` and `updated-by` fields were checked for corrections, retractions and expressions of concern. Claims were re-read against the saved full texts in `/home/claude/p15/fulltext`, abstracts in the search exports (`pkg/data/raw/search_*.jsonl`), and, for Oliveira et al. (2023), the institutional repository record. Nothing was invented. Anything that could not be checked is marked **unverified**.

---

## 1. Summary

| Severity | Count | Items |
|---|---|---|
| Must fix | 6 | Huang (2022) missing from References; Esquerra-Resa misreported (a chrome ISO 20136 value exists); Aguilar reference (wrong 4th author, no pages, DOI not registered) plus an undisclosed duplicate publication; Discussion overstates the LCA "cattle and liming" point for Oliveira; "mostly written by developers" contradicts 11 of 24; §2.9 says every DOI was checked against Crossref, which is not true for Aguilar |
| Should fix | 6 | Oliveira wording ("all categories" and "about" are not in the abstract) and its "Source read" label; Zuriaga-Agustí (2015) listed but never cited; Gómez-García (2026) has generated-text and editing residue like Atinafu but is not flagged; inconsistent year convention for online-first articles; Evans page range; journal name in the Atinafu reference |
| Minor | 4 | "Gomez-Garcia" without diacritics in Table 2; suggested primary source for the EU Cr(VI) limit; caveat on Ferraris total-Cr units; blanket Collagen and Leather competing-interests correction (Huang 2022, Xiao 2023, Navarro 2020) |

- **Builder's open items:** Aguilar DOI: confirmed it does not resolve (Crossref and doi.org both return an error). PRISMA 2020 volume 372: **confirmed** (Europe PMC: BMJ 2021;372:n71, PMID 33782057). Chakraborty year 2008: **confirmed** from the article's running header; Crossref's 1970 is a placeholder. Valeika (2010) authors: **confirmed** as Valeika, Širvaitytė & Beleška from the article (Crossref lists "Author"). Hoch (2009) author order: the **manuscript is correct**. The article byline puts Hoch first; Crossref wrongly puts do Prado first.
- **Retractions and expressions of concern:** Crossref metadata shows none for any included study or cited source. Aguilar (2023) cannot be checked because its DOI is not registered. Atinafu (2026) shows none in DataCite. PubPeer and Retraction Watch were not searched directly (**unverified** beyond Crossref).
- **Novelty:** the claim holds as worded ("not aware of a synthesis that pools within-study contrasts"). It should cite and set aside two narrative reviews that tabulate property values without pooling (§6).

---

## 2. In-text citations against the reference list

| Issue | Detail | Fix |
|---|---|---|
| **Cited, not listed** | Huang (2022) is in Table 2 and the analysis (`study_characteristics.csv`: huang2022, DOI 10.1186/s42825-022-00089-0), but it has no reference entry | Add the entry (§5) |
| **Listed, not cited** | Zuriaga-Agustí et al. (2015), J. Clean. Prod. 87, 874–881. It is not cited anywhere in the text or tables | Cite it in §3.5 or Table 4 (chrome-free tanning plus composting of tanned wastes; read the source first) or delete it |
| Spelling mismatch | Table 2 has "Gomez-Garcia (2026)"; the text and References have "Gómez-García" | Use "Gómez-García" |
| Everything else | All other 48 author–year pairs match one to one, including Shi et al. (2016, 2024), Hedges et al. (1999, 2010), Valeika (2010, 2020), and the ISO standard and PRISMA (Page et al., 2021) | — |

---

## 3. Claims table

"Read" means what the auditor read for this check.

| # | Location | Claim | Source | Read | Verdict |
|---|---|---|---|---|---|
| C1 | §1 | Cr(III) in leather can oxidise to Cr(VI), a skin sensitiser; the EU restricts Cr(VI) in leather articles | Hedberg et al. 2014 | Abstract | **Supported.** The abstract states that 1–3% of European adults are allergic to Cr, that "the Cr(VI) content in leather was recently restricted in the European Union", and that Cr(VI) was found on surfaces and in solution. Optional: add the regulation itself as the primary source (Commission Regulation (EU) No 301/2014; **verify before adding**). |
| C2 | §1 | "Most leather is tanned with basic chromium sulfate"; Cr in effluent, sludge, shavings | uncited | — | Uncited but uncontroversial. Ciurli et al. (2025, abstract) give "90 % of leather production still relies on WB tanning", and Esquerra-Resa et al. (2022, full text) give "About 85% of the world's hides". Either could be cited. |
| C3 | §1 | Comparisons "are mostly written by the people who developed the agent being tested" | own data | Manuscript | **Contradicted by the paper's own data.** Eleven of 24 studies (46%) were by developers. §5 repeats "mostly written by the developers". Change to "often" or "nearly half". |
| C4 | §1 | Nugraha et al. (2025) pooled 13 studies of vegetable tanning with mimosa, not chrome, as comparator | Nugraha 2025 | Full text | **Supported** ("data from thirteen peer-reviewed publications"; "employing mimosa tannin as the control"). |
| C5 | §2.5–2.6 | Methods citations: lnRR variance (Hedges 1999), shared-control covariance (Lajeunesse 2011), RVE (Hedges 2010), prediction interval (Riley 2011), I² (Higgins & Thompson 2002), Egger test (1997), PRISMA 2020 (Page 2021) | — | Crossref metadata; standard content | Correctly attributed. |
| C6 | §2.4 | ISO 3380 covers Ts up to 100 °C | ISO 3380:2015 | Title only | Supported by the standard's title. Ferraris (full text) also cites ISO 3380:2015 (IULTCS/IUP 16). |
| C7 | §2.7, Table 2 note | Atinafu & Teferi (2026) contain "user's anticipated benefits", "the user's enzyme-activated system" and an unfilled template header | Atinafu 2026 | Full text | **Supported and fairly described.** Both phrases are present (lines 279 and 314 of the saved text). The header reads "2024, Volume 1, Issue 2. Page: XXX-XXX" next to the real "Volume 3, Issue 3, 2026". Other residue that could be mentioned: a garbled reference ("Connective Tissue Research, 2001; 42(2): 8 (4): 103889"), and the journal name is spelled two ways ("Advance" on the masthead, "Advanced" in the footer). Its exclusion from the primary analyses is proportionate. |
| C8 | §3.2 | Tilapia: mimosa 5.8 vs chrome 26.8 N/mm²; chrome is an external benchmark | Gómez-García 2026 | Full text | **Supported** (5.8 ± 1.7; 26.8 ± 2.7; "used exclusively as an external benchmark"). **See C20** for integrity residue. |
| C9 | §3.2 | Aguilar: chrome leather supplied by a company; silica-sol arms 1.37 and 1.63 times chrome | Aguilar 2023 | Full text (values from `replicates.csv`, not recomputed) | Comparator description consistent. Ratios not re-derived by this audit. **See C19.** |
| C10 | §3.4 | Ferraris: chrome Ts "> 95 °C"; tilapia chrome Ts 80 vs mimosa 77.9 °C | Ferraris 2025; Gómez-García 2026 | Full text | **Supported** (Ferraris Table 1: "> 95"; Gómez-García: 77.9 ± 2.0 vs 80 ± 5.1). |
| C11 | §3.5, Table 4 | Daddi: PM −25%, non-carc. tox −31%, carc. tox −56%, acidification −29%, single score −18.4%, cattle breeding largest contributor to several categories | Daddi 2024 | Abstract (Europe PMC export) | **Supported verbatim.** |
| C12 | §3.5, Table 4 | Oliveira: vegetable route "lower than chrome across impact categories, by about 20% for ozone depletion up to about 100% for human carcinogenic toxicity"; Table 4: "lower in all categories" | Oliveira 2023 | Abstract via institutional repository record (ricerca.uniparthenope.it/handle/11367/139151), read through a retrieval tool that quoted the key sentence verbatim. The publisher page was blocked. | **Numbers supported; framing overstated.** The abstract says: "The vegetable option shows substantial impact reductions, ranging from 20% in ozone depletion potential to 100% in human carcinogenic toxicity potential." The figures are exact, so "about" is unnecessary. The abstract does **not** say the reduction applies in "all" categories. "In all impact categories" appears only for the circular scenarios. Hotspots are supported: retanning or tanning for chrome; pickling for vegetable, with liming as its largest contributor. **Fix:** "reported substantial reductions for the vegetable route, ranging from 20% (ozone depletion) to 100% (human carcinogenic toxicity)". Drop "in all categories" from Table 4 and change "Source read" to "abstract (institutional repository record)". |
| C13 | §3.5, Table 4 | Blas García: two chrome-free techniques better than chrome; best technique 30.0 m³ water, 2022.7 kWh, 105.5 kg solid waste, Cr not detectable | Blas García 2022 | Abstract (OpenAlex export) | **Supported.** Pilot scale (CITEccal Lima). |
| C14 | §3.5, Table 4 | Xiao: Cl⁻ 3.2 vs 11.3; TDS 8.5 vs 13.5; COD 13.2 vs 19.7 g/L; BOD₅/COD 0.35 vs 0.19 | Xiao 2023 | Full text, Table 3 | **Supported** (all values marked "~" in the source). Note that these are for the SACC + tannic-acid system, and that the lower chloride reflects the omitted NaCl pickle ("no NaCl was used for the pickling process"), a process difference rather than the tanning agent alone. Consider saying so. |
| C15 | §3.5, Table 4 | Inbasekar: BOD/COD of the oxazolidine process lower than chrome ("the opposite") | Inbasekar 2021 | Abstract (OpenAlex export) | **Supported** ("relatively less compared to the conventional chrome tanning process"). Note that the same abstract reports physical strength "better than those of the chrome-tanned leather". The study is a paired physical comparison that was presumably not retrieved (ACS, closed); no change needed beyond the existing limitation. |
| C16 | §3.5, Table 4 | Tariq: soils near chrome tanneries well above background; near vegetable tanneries close to background | Tariq 2009 | Abstract (Europe PMC export) | **Supported.** The two clusters (Kasur vs Mian Channun, 16 + 16 tanneries) differ in location as well as tannage. |
| C17 | §3.5, Table 4 | Dhayalan: vegetable-tanned leather produced more gas than chrome under anaerobic digestion | Dhayalan 2007 | Abstract (Europe PMC export) | **Supported verbatim.** |
| C18 | §3.5, Table 4 | Pourrasoul Sardroudi: wet-blue fully degraded in 31–35 days; vegetable-tanned leather first degraded at 60 days, not fully at 90 | Pourrasoul Sardroudi 2024 | Abstract (OpenAlex export; Crossref) | **Supported** ("total degradation after 31 to 35 days"; "initial signs of degradation after 60 days … even after a protracted 90-day incubation period"). |
| C19 | §3.5, Table 4 | Esquerra-Resa: zeolite hide visibly more degraded than chrome and aluminium hide after burial; "ISO 20136 for the new system only … (no ISO 20136 value for chrome)"; 74.4% relative biodegradability for the shoe-upper retannage | Esquerra-Resa 2022 | Full text | **Burial claim supported** ("the cow hide tanned with the new biodegradable system show a higher level of biodegradation than those tanned with chrome and aluminum salts"). **ISO 20136 statement is wrong.** The test compared the samples "with pure collagen, cow hide tanned with Sertan WT, leather tanned with chromium and with oxazolidine (INESCOP control)". Table XI gives relative biodegradability of **chrome tanning 0.5%** (absolute 0.4%), Sertan WT on cow hide 91.0%, shoe upper 74.4%, leather goods 45.0% and vegetable retannage 10.3%. The text says chrome "shows 99.5% less biodegradability than pure collagen". Whether the chrome leather was tanned in the study or was a reference sample is not stated (**unverified**). **Fix Table 4 and §3.5.** The paper's statement that "the direction depended on the test" still holds (compare Pourrasoul Sardroudi). Also note that the zeolite (sodium aluminosilicate) leathers contained ">12000 mg/kg of aluminum" and the authors say they "cannot be considered as metal-free". |
| C20 | §3.5, Table 4 | Constantinescu: six tannages, EN ISO 20200, all biodegraded at different rates | Constantinescu 2015 | Full text (abstract section) | **Supported.** |
| C21 | §3.5, Table 4 | Ciurli: both released 40–45% of N in 42 days; DTPA-Cr increased but stayed low in wet-blue soil; Cr not bioavailable to tomato | Ciurli 2025 | Abstract (OpenAlex export) | **Supported verbatim.** |
| C22 | §3.5, Table 4 | Ferraris: total Cr 111.73 (zeolite) and 53.72 mg/kg (aluminium) in nominally chrome-free leathers; Cr(VI) entry < 3.0 mg/kg | Ferraris 2025 | Full text, Table 1 | **Supported as tabulated.** Caveat: the same row gives the wet-blue chrome leather 2.965 "mg/kg s.s." total Cr, alongside "total tanning metals" of 0.3%. This suggests mixed units in that row. The chrome-free values are plausible but should be quoted "as reported". |
| C23 | §3.5, Table 4 | Ercegović Ražić: all tannages caused primary DNA damage; vegetable > synthetic > chrome | Ercegović Ražić 2022 | Full text | **Supported** ("highest after vegetable tanning, followed by synthetic tanning and chrome tanning"). Correctly labelled a pilot study. |
| C24 | §3.5 | Navarro: 39 LCA papers of four distinct types | Navarro 2020 | Abstract (via Crossref) | **Supported** (39 papers in four groups). |
| C25 | §3.5 | Reetz 2026; Shi 2016, 2024 identified but not retrieved | — | Crossref metadata only | Metadata correct; content not assessed (consistent with the text). |
| C26 | §4.2 | "The two LCAs with primary data … both found that the cattle and liming stages weigh heavily, which limits how much any tanning change can move a leather's footprint" | Daddi; Oliveira | Abstracts | **Overstated for Oliveira.** Daddi supports cattle breeding. Oliveira found the **tanning or retanning phase** to be the main hotspot for chrome leather, with liming the largest contributor to the vegetable route's pickling hotspot, and reported reductions of up to 100% in one category. That cuts against "limits how much any tanning change can move". Revise to: "Daddi et al. found cattle breeding the largest contributor to several categories, and Oliveira et al. found the beamhouse (liming) the main hotspot of the vegetable route, while the tanning stage was the hotspot of the chrome route." |
| C27 | §4.2 | "Biodegradation results reverse with the method" | Pourrasoul Sardroudi; Dhayalan; Esquerra-Resa | as above | Supported, but should now also note that the only ISO 20136 respirometry result (Esquerra-Resa) strongly favours the chrome-free leather (91.0% vs 0.5%). |
| C28 | §2.9 | "Every DOI cited was checked against Crossref (or DataCite)" | — | — | **Not accurate as written.** Aguilar's DOI is not registered. Add "except Aguilar et al. (2023), whose printed DOI is not registered". |
| C29 | §5 | "mostly written by the developers of the chrome-free agents" | own data | — | Same as C3: 11 of 24. |

### Integrity observations on included studies (task item 4)

- **Atinafu & Teferi (2026).** The concern is confirmed and fairly described (C7). No retraction or other notice appears in DataCite.
- **Aguilar et al. (2023): undisclosed duplicate publication.** The same article, with the same title, authors and tables, appears twice in the same issue of *Journal of Pharmaceutical Negative Results* 14(Special Issue 2): pp. 159–172 (DOI as printed …S02.23; landing page pnrjournal.com/…/view/6619) and pp. 269–282 (DOI as printed …S02.34; view/6684). Neither DOI resolves in Crossref or doi.org. The builder treated the second copy as a duplicate report, which is correct, but the manuscript does not disclose the duplication, the unregistered DOIs, or that a leather study appeared in a pharmacy journal. This is the only zeolite/silicate study, and it is a tensile outlier (1.54). **Recommend** applying the same integrity flag as Atinafu, or at least disclosing this and reporting tensile without it. (Whether the journal was delisted from Scopus: **unverified**, not found.)
- **Gómez-García et al. (2026): editing residue.** The text contains "correcting previous inconsistencies in how these values had been presented in earlier drafts", "consistent with previous Q1 studies", a duplicated clause ("(p = .049). was significant"), unattributed "(Citation2022)" scales, and fish-leather thickness given as "70–80 mm" (implausible; probably 0.70–0.80 mm). Values used by the review (5.8 vs 26.8 N/mm²; Ts 77.9 vs 80) are internally consistent. However, the residue is of the same kind that led to Atinafu being flagged, and this study is the other tensile outlier (0.22). **Recommend** mentioning it in §2.7 and either flagging it consistently or explaining why it is not flagged. Leave-one-out already covers it numerically.
- **Corrections:** Huang 2022, Xiao 2023 and Navarro 2020 are among 55 *Collagen and Leather* / *J. Leather Sci. Eng.* articles covered by a blanket "Correction to Competing Interests" (10.1186/s42825-023-00121-x, 6 May 2023). It does not affect the data. Mentioning it is optional.
- **No retractions or expressions of concern** were found in Crossref or DataCite metadata for any of the 24 included studies or 26 other references.

---

## 4. Reference table (Crossref or DataCite check)

✓ = matches the registry. Δ = discrepancy. All DOIs not otherwise noted resolve.

| Reference (as in manuscript) | DOI resolves | Metadata check | Action |
|---|---|---|---|
| Aguilar et al. 2023 | **No** (Crossref and doi.org error, both copies) | Landing page lists **3 authors** (Aguilar, Chariguaman Maurisaca, Mejia Peñafiel); "García Veloz" comes from OpenAlex only and is not on the PDF byline. Pages 159–172 missing | **Correct** (§5) |
| Anggriyani et al. 2020 | ✓ | ✓ LFJ 20(2), 153–160 | — |
| Atinafu & Teferi 2026 | ✓ DataCite | DataCite: publisher WJAMR, 2026, JournalArticle, no container data. PDF: Vol 3, Issue 3, pp. 13–20, ISSN 3050-9491. Masthead "Advance", footer "Advanced" | Optional: note the spelling; consider adding "[Archived on Zenodo]" |
| Bielak & Zielińska 2022 | ✓ | ✓ 22(1), 3–16 | — |
| Blas García et al. 2022 | ✓ | ✓ 23(10), 11–24 | — |
| Cavali et al. 2022 | ✓ | ✓ PLOS ONE 17(1) e0261781 | — |
| Chakraborty et al. 2008 | ✓ | Crossref year 1970 (placeholder); article header "43(4), 553-558, 2008" ✓ | Keep 2008 |
| Ciurli et al. 2025 | ✓ | ✓ 13(5) 118990 | — |
| Constantinescu et al. 2015 | ✓ | ✓ | — |
| Daddi et al. 2024 | ✓ | Online 16 Dec 2024; vol. 32, issue 54 (2025), 29995–30012 | Year convention (see note) |
| Dhayalan et al. 2007 | ✓ | ✓ | — |
| Egger et al. 1997 | ✓ | ✓ | — |
| Ercegović Ražić et al. 2022 | ✓ | ✓ | — |
| Esquerra-Resa et al. 2022 | ✓ | ✓ 117(6), 251–261 | — |
| Evans & Critchfield 1933 | ✓ | Crossref gives start page 147 only; PDF runs 147–162 (RP583, July 1933) | Add "147–162" |
| Fatama et al. 2025 | ✓ | ✓ 9 authors, 60(4), 287–296 | — |
| Ferraris et al. 2025 | ✓ | ✓ 11 authors, 15, 10608 | — |
| Girmay et al. 2024 | ✓ | ✓ Heliyon 10(1) e23141 (print 2024-01) | — |
| Gómez-García et al. 2026 | ✓ | ✓ 23(1) 2724460 | — |
| Hedberg et al. 2014 | ✓ | ✓ | — |
| Hedges et al. 1999 | ✓ | ✓ | — |
| Hedges et al. 2010 | ✓ | ✓ | — |
| Higgins & Thompson 2002 | ✓ | ✓ | — |
| Hoch et al. 2009 | ✓ | Crossref order wrong (do Prado first). **Article byline: Hoch, do Prado, Franco, Scapinello, Franco, Gasparino**, so the manuscript is correct; pages 411–415 from the running footer ✓ | — |
| **Huang et al. 2022** | ✓ | **Missing from References** | **Add** (§5) |
| Inbasekar et al. 2021 | ✓ | ✓ 9(44), 15053–15062 | — |
| ISO 3380:2015 | n/a | Title as on the standard | — |
| Jia et al. 2022 | ✓ | Crossref has no pages; PDF 141–152 ✓ | — |
| Jiang et al. 2023 | ✓ | ✓ | — |
| Lajeunesse 2011 | ✓ | ✓ | — |
| Nasr et al. 2020 | ✓ | Crossref lists only "Nasr AI"; PDF byline Nasr AI, Azzam AH, Abdelsalam MM ✓ | — |
| Navarro et al. 2020 | ✓ | ✓ 2, 26 | — |
| Nugraha et al. 2025 | ✓ | ✓ 35(3), 271–285 | — |
| Oliveira et al. 2023 | ✓ | Online 25 Sep 2023; vol. 29(2), 153–173 is the Feb 2024 issue | Year convention (see note) |
| Page et al. 2021 | ✓ | **Volume 372 confirmed** (Europe PMC); 26 authors; APA 7 truncation (19 + … + last) ✓ | — |
| Pourrasoul Sardroudi et al. 2024 | ✓ | ✓ 16(6) 2324 | — |
| Qiao et al. 2025 | ✓ | ✓ 7, 9 | — |
| Reetz et al. 2026 | ✓ | ✓ 30, 101124 (third author "Grau Baquero" in Crossref) | — |
| Riley et al. 2011 | ✓ | ✓ | — |
| Rosiati et al. 2024 | ✓ | Crossref page 284 only; PDF 284–294 ✓ | — |
| Shi et al. 2016 | ✓ | ✓ | — |
| Shi et al. 2024 | ✓ | ✓ | — |
| Tariq et al. 2009 | ✓ | ✓ | — |
| Tian 2025 | ✓ | ✓ 8, 1060–1073 | — |
| Uddin et al. 2020 | ✓ | ✓ 3(3), 135–145 | — |
| Valeika 2020 | ✓ | ✓ 26(3), 333–336 | — |
| Valeika et al. 2010 | ✓ | Crossref author "Author" (placeholder); PDF byline Valeika, Širvaitytė, Beleška ✓ | — |
| Xiao et al. 2023 | ✓ | ✓ 5, 2; competing-interests correction (blanket) | Optional note |
| Yorgancioglu et al. 2022 | ✓ | ✓ 66(2), 215–226 (online 2021, issue 2022) | — |
| Zhu et al. 2022 | ✓ | ✓ 12(12), 7506–7515 | — |
| Zuriaga-Agustí et al. 2015 | ✓ | ✓ 87, 874–881 | **Not cited**: cite or delete |

**Year-convention note.** The list mixes conventions for online-first articles. Yorgancioglu (online 2021) and Girmay (DOI 2023) use the issue year; Daddi (issue 2025) and Oliveira (issue 2024) use the online year. APA 7 cites the final published version by its issue year. For consistency, use **Daddi et al. (2025)** and **Oliveira et al. (2024)** and update the in-text citations and Table 4. Alternatively, keep the online years and state the convention. Either way, apply it consistently.

---

## 5. Corrected or added entries (APA 7)

**Add:**

Huang, Y., Xiao, H., Pu, H., Xue, N., Hao, B., Huang, X., & Shi, B. (2022). Self-driven directional dehydration enabled eco-friendly manufacture of chrome-free leather. *Journal of Leather Science and Engineering, 4*, 17. https://doi.org/10.1186/s42825-022-00089-0

**Replace Aguilar** (3 authors per landing page and PDF byline; pages added; DOI not registered, so give the landing-page URL):

Aguilar, J. E., Chariguaman Maurisaca, N. E., & Mejia Peñafiel, E. F. (2023). Determination of the best treatment for the tannery industry using sodium silicate (Na~2~SiO~3~) with sulfuric acid (H~2~SO~4~). *Journal of Pharmaceutical Negative Results, 14*(Special Issue 2), 159–172. https://pnrjournal.com/index.php/home/article/view/6619

(Optionally add a note: "DOI printed on the article, 10.47750/pnr.2023.14.S02.23, was not registered with Crossref or doi.org as of October 2026. The same article also appears at pp. 269–282 of the same issue." The PDF spells "Mejia" without an accent.)

**Evans:** … *Bureau of Standards Journal of Research, 11*(1), 147–162. https://doi.org/10.6028/jres.011.013

**If the APA issue-year convention is adopted:**
- Daddi, T., Ahmad, S., & Albano, F. (2025). … *Environmental Science and Pollution Research, 32*(54), 29995–30012. https://doi.org/10.1007/s11356-024-35625-4
- Oliveira, M., Zucaro, A., Passaro, R., & Ulgiati, S. (2024). … *The International Journal of Life Cycle Assessment, 29*(2), 153–173. https://doi.org/10.1007/s11367-023-02232-3

**Optional, if novelty paragraph expanded (§6):**
- Hassan, M. M., Harris, J., Busfield, J. J. C., & Bilotti, E. (2023). A review of the green chemistry approaches to leather tanning in imparting sustainable leather manufacturing. *Green Chemistry, 25*(19), 7441–7469. https://doi.org/10.1039/d3gc02948d
- Ding, W., Remón, J., & Jiang, Z. (2025). Environmentally-friendly tanning for leather production: A review. *Environmental Chemistry Letters, 23*(3), 839–864. https://doi.org/10.1007/s10311-025-01827-6

(Both verified in Crossref. Content judged from abstracts or landing pages and the UAL repository PDF, not a full read: **partly unverified**.)

**Suggested replacement text:**
- §3.5 Oliveira: "Oliveira et al. (2023), according to the abstract, reported substantial reductions for the vegetable route, ranging from 20% in ozone depletion to 100% in human carcinogenic toxicity."
- Table 4 Esquerra-Resa, result: "zeolite-tanned cow hide visibly more degraded than chrome- and aluminium-tanned hide after burial; ISO 20136 relative biodegradability (vs collagen) 91.0% for zeolite-tanned cow hide and 74.4% for the shoe-upper retannage vs 0.5% for chrome-tanned leather". Method: "burial in compost (photographs); ISO 20136 respirometry".
- §3.5 End of life: add "Under ISO 20136 respirometry, zeolite-tanned hide reached 91% of the biodegradation of pure collagen against 0.5% for chrome-tanned leather (Esquerra-Resa et al., 2022)."

---

## 6. Novelty assessment

**Claim (§1):** "I am not aware of a synthesis that pools within-study contrasts between chrome-free and chrome-tanned leather."

**Searches (28 October 2026):** web search (standard and extended) for meta-analyses or systematic reviews of chrome-free (vegetable, aldehyde, synthetic, metal-free, wet-white) versus chrome-tanned leather properties, plus checks of the hits. OpenAlex API search through WebFetch was blocked. The builder's own OpenAlex and Europe PMC searches (3,567 records) are the main systematic coverage.

**Found:**
1. **Nugraha et al. (2025)**, a meta-analysis of 13 vegetable-tanning studies with **mimosa** as the control (full text read). Already cited and correctly distinguished.
2. **Hassan et al. (2023)**, *Green Chemistry*, a critical narrative review. It tabulates shrinkage temperature, tensile and tear strength and Cr uptake across tanning methods (Tables 1–5). It has no systematic search and no pooling (judged from the repository PDF summary; tables not inspected).
3. **Ding, Remón & Jiang (2025)**, *Environmental Chemistry Letters*, a narrative review of greener tanning (chrome-free organic, combination, nanomaterial, agent-free). It shows no systematic method or pooling (abstract only).
4. Several primary studies (Ferraris 2025; Bielak 2022; Uddin 2020; JALCA 120(9) 2025; Collagen and Leather 7:16 2025) compare agents but are not syntheses.

**Verdict:** the novelty claim **holds** as worded. No meta-analysis or systematic review pooling within-study chrome-free vs chrome contrasts was found. **Recommended narrowing:** (a) keep the hedge ("I am not aware"). (b) Add one sentence acknowledging that narrative reviews tabulate reported property values across tanning systems without a systematic search or pooling (Hassan et al., 2023; Ding et al., 2025). (c) Avoid any "first" claim in the abstract, social summary or posting copy unless it is qualified as "to the author's knowledge, the first meta-analysis of paired chrome-free vs chrome laboratory tests". Coverage of the Chinese-language literature (for example, *China Leather*) was not searched (**unverified**).

---

## 7. What was read

- **Full text (saved copies):** Atinafu, Aguilar (both copies), Chakraborty, Constantinescu, Ercegović Ražić, Esquerra-Resa, Evans, Ferraris (incl. Table 1), Gómez-García, Hoch, Jia (pages), Nasr, Nugraha, Rosiati (pages), Valeika 2010 and 2020 (headers), Xiao (Table 3 and text).
- **Abstract only:** Daddi, Blas García, Inbasekar, Dhayalan, Pourrasoul Sardroudi, Ciurli, Tariq, Hedberg (search exports); Navarro and Nugraha (Crossref summaries; Nugraha also full text); Oliveira (institutional repository record via a retrieval tool, with the key sentence quoted verbatim; publisher page and Semantic Scholar unavailable).
- **Metadata only:** all DOIs via Crossref (DataCite for Zenodo), plus Reetz, Shi 2016, Shi 2024 and Zuriaga-Agustí (content not assessed).
- **Not checked:** PubPeer; Retraction Watch database directly; Chinese-language literature; Aguilar ratio recomputation.
