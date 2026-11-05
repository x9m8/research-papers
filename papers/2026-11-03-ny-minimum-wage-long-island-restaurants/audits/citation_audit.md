# Citation audit — Paper 20

**Paper:** Kalafatis, P. (2026). *Regional minimum wages and restaurant employment on Long Island, New York* (preprint, v1).
**Manuscript audited:** `pkg/manuscript/manuscript.md` (with `pkg/README.md`, `lit/brief.md`).
**Auditor:** independent citation audit (Claude, Anthropic). I did not write the paper. 29 October 2026.
**Methods:** All 22 DOIs were resolved against the Crossref REST API (`api.crossref.org/works/{DOI}`), read in a browser tab I opened and then closed. Abstracts were read from Crossref, publisher, NBER, RePEc/EconPapers or the preprint servers. I read the full text of Ahn (2026), through the OSF viewer. I read the Aaronson et al. (2018) full text only for its data source. Official NYSDOL and USDOL pages and PDFs were fetched directly on 29 October 2026. For novelty, I ran Crossref and OpenAlex keyword queries and general web searches.

---

## 1. Summary

- **All 30 references exist.** All 22 DOIs resolve, and their authors, titles, journals, volumes, issues and pages match the reference list. In-text citations and the reference list match one to one: 30 cited and 30 listed, with no orphans in either direction.
- **There are no fabricated sources.** Most characterisations are accurate. Four need correcting:
  1. **Addison et al. (2012) is described as a county-pair (cross-border) design, twice (§1 and §4.2).** Its abstract and the IZA working-paper summary describe county-level panels with county-specific sectoral trends, not contiguous cross-border pairs.
  2. **Luca & Luca (2019) is grouped with studies "that use administrative establishment counts" (§4.2).** It uses Yelp data and studies exit only. Aaronson et al. (2018) does use establishment-level QCEW data, so that half of the sentence is correct.
  3. **"fast-food chains have had their own wage order since 2016" (§1), and Table 1's 2016 fast-food rate of $9.00, are wrong.** The fast-food order's first increase took effect on 31 December 2015, at $9.75 outside New York City. The source for this is secondary (an Ogletree Deakins law-firm summary) and needs confirming against an official document. The LI–rest-of-state gap is unaffected (zero), but the 2016 level in Table 1 and Figure 1 is wrong.
  4. **"Studies of Seattle reached different conclusions" cites only one Seattle study (Jardim et al., 2022).** Either cite the other side or rephrase.
- **Card & Krueger:** the paper should cite the 1994 *American Economic Review* article, 84(4), 772–793, JSTOR 2118030, verified on JSTOR. The 1993 NBER working paper should not be the citation. The corrected entry is below.
- **NY DOL sources:** all rates in Table 1 for the general minimum and the tipped cash wage match the official documents, as do the fast-food rates from 2017 on. Three date and labelling fixes are needed: the minimum-wage page is undated, so it should be "n.d.", not "2026a"; the USDOL history table was revised in January 2025; and the CR146 PDF carries form code "CR 146 (09/24)". The fast-food definition should be cited to §146-3.13(b).
- **Novelty:** the four contributions claimed in §1 hold as far as I can find. The framing should still acknowledge three pieces of related work the paper does not cite: (a) the NY Division of the Budget's statutory minimum-wage reports, which describe QCEW leisure-and-hospitality trends for Long Island–Westchester against upstate; (b) Bram, Karahan & Moore (2019, Federal Reserve Bank of New York), a NY–PA border-county QCEW comparison directly relevant to §3.4; and (c) Ahn's (2026) own upstate/downstate comparison. The statement that the search covered only Crossref and OpenAlex should be updated.

---

## 2. Claims table

Verdicts: **S** = supported; **P** = partly supported or needs rewording; **X** = not supported or wrong; **U** = not verified.

| # | Location | Claim (paraphrased) | Source | What the source says (checked) | Verdict |
|---|---|---|---|---|---|
| 1 | §1 ¶3 | NJ vs PA fast food after NJ's 1992 increase; no employment loss | Card & Krueger (1993) | AER 1994 abstract (JSTOR): NJ minimum rose from $4.25 to $5.05 on 1 April 1992; 410 restaurants surveyed; "no indication that the rise in the minimum wage reduced employment." | S (but cite the 1994 AER article) |
| 2 | §1 ¶3 | County-pair cross-border designs found no adverse restaurant employment effects | Dube et al. (2010) | RePEc abstract: all contiguous cross-state county pairs, 1990–2006, restaurants and other low-wage sectors; no job losses. | S |
| 3 | §1 ¶3; §4.2 | Same, and "border-county literature" | Addison et al. (2012) | Crossref abstract: county-level restaurant-and-bar data; no disemployment once county-level sectoral trends are controlled. Neither the abstract nor the IZA DP 3300 summary mentions contiguous cross-border pairs. | X as worded. Recharacterise as "county panels with county-specific trends", unless the full text (not read) shows a border-pair specification |
| 4 | §1 ¶3 | Neumark et al. argued such designs have problems isolating reliable identifying information and reported teen disemployment | Neumark et al. (2014) | Abstract: "explore the ability of the new research designs to isolate reliable identifying information… reveals problems"; teen elasticities near −0.15. | S (wording is very close to the abstract; consider paraphrasing) |
| 5 | §1 ¶3 | Number of low-wage jobs essentially unchanged five years after 138 state increases | Cengiz et al. (2019) | Abstract: 138 state-level changes, 1979–2016; low-wage jobs "remained essentially unchanged over the five years." | S |
| 6 | §1 ¶3 | "Studies of Seattle reached different conclusions"; Jardim found reductions in hours at low wages | Jardim et al. (2022) | Abstract: hours worked at wages below twice the old minimum declined; elasticities −0.2 to −2.0, mostly on the intensive margin. | P. Jardim is correctly described, but "studies… different conclusions" has only one citation. Add the contrasting study (candidate found in OpenAlex: Reich, Allegretto & Godøy, 2017, *Seattle's minimum wage experience 2015–16*, SSRN, DOI 10.2139/ssrn.3043388; **not verified, check before use**) or rephrase |
| 7 | §1 ¶3 | Reviews disagree about what the literature says | Manning (2021); Neumark & Shirley (2022) | N&S abstract is about disagreement over what the literature says; Manning: "elusive employment effect." | S |
| 8 | §1 ¶3 | N&S: low-wage-industry evidence less one-sided than for teenagers | Neumark & Shirley (2022) | Abstract: (ii) stronger for teens, young adults, less educated; (iv) "evidence from studies of low-wage industries is less one-sided." | S |
| 9 | §1 ¶3 | Restaurants adjust through prices | Aaronson (2001); Allegretto & Reich (2018); Ashenfelter & Jurajda (2022) | Titles and abstracts: price pass-through; San Jose menus (prices rose 1.45%); McDonald's pass-through. | S |
| 10 | §1 ¶3 | …and through exit and entry of establishments | Aaronson et al. (2018); Luca & Luca (2019) | Aaronson et al.: exit and entry both rise. Luca & Luca (NBER): exit of lower-rated (Yelp) restaurants; does not study entry. | S (jointly) |
| 11 | §1 ¶4 | Even & Macpherson: reducing the tip credit lowered full-service employment | Even & Macpherson (2014) | Abstract: a reduction in the tip credit "increases weekly earnings but reduces employment in the full-service restaurant industry." | S |
| 12 | §1 ¶4 | Allegretto & Nadler: small, insignificant effects in preferred models | Allegretto & Nadler (2015) | Abstract: "In our preferred models, we find small, insignificant effects of the tipped wage on FSR employment." | S |
| 13 | §1 ¶4 | "fast-food chains have had their own wage order since 2016" | none cited | Fast-food rates first took effect on 31 Dec 2015 ($10.50 NYC; $9.75 outside NYC), according to Ogletree Deakins (30 Dec 2015), a secondary source. The current NYSDOL history page lists fast-food rates from 31 Dec 2016 only. | X. Should read "since 31 December 2015". Confirm with an official source (the 2015 Commissioner's order or NYSDOL archive) |
| 14 | §1 ¶5 | Sabia et al.: large negative effects of the 2004–06 NY increase on young, less-educated workers | Sabia et al. (2012) | Abstract: 16–29-year-olds without a high-school diploma; 20.2–21.8% employment reduction; elasticity about −0.7. | S |
| 15 | §1 ¶5 | Hoffman: no negative effect with the full CPS | Hoffman (2016) | Abstract: re-analysis with the full CPS "finds no evidence of a negative employment impact." | S |
| 16 | §1 ¶5; §4.2 | Ahn: within-state DiD; county limited-service employment; NY 2010s–2020s; broadly stable | Ahn (2026) | Full text read: QCEW NAICS 722513 county-quarters; regression of employment on a Post_t indicator with county and time FE, SE clustered by county; reports Post coefficient −9.16 (SE 45.69). Also compares "downstate metropolitan" with upstate counties descriptively. | S as a summary. Note for the authors: Ahn's Post_t varies only over time and is entered alongside time fixed effects, so its identification is unclear. Ahn does not model the LI–upstate gap or the 2023 narrowing. The OSF record also states that no analysis is reported, which conflicts with the text. Describe it with "reports" and do not lean on it as validation |
| 17 | §1 ¶5 | Baker: NY's Jan 2025 increase vs Texas; monthly state data; no significant food-service change over a short window | Baker (2025) | Abstract: DiD using monthly FRED data, Texas as control; CA −42,580 food-service jobs; NY ($0.50, Jan 2025) no significant change, "limited post-treatment period." | S |
| 18 | §1 ¶6; §2.4 | Placebo inference for one treated region | Conley & Taber (2011); Ferman & Pinto (2019) | Titles: DiD inference with few policy changes; few treated groups and heteroskedasticity. | S |
| 19 | §1 ¶6; §2.3; §3.3 | Synthetic control | Abadie et al. (2010) | Method paper. | S |
| 20 | §1 ¶1; §2.1; Table 1 | Regional general-minimum schedule, LI & Westchester vs rest of state, 2016–2026 | NYSDOL (n.d.-a); CR146 §146-1.2 | Fetched 29 Oct 2026: LI/W 10, 11, 12, 13, 14, 15 (31 Dec 2016–2021), 16 / 16.50 / 17 (1 Jan 2024–26). Rest of state 9.70 … 13.20, 14.20 (31 Dec 2022), 15 / 15.50 / 16. Statewide 8.00 / 8.75 / 9.00 (31 Dec 2013–15). | S |
| 21 | §2.1; Table 1 | Tipped food-service cash wage by region | CR146 §146-1.3(b)(2), (3); Part 146 summary rev. 02/26 | LI/W 7.50, 7.50, 8.00, 8.65, 9.35, 10.00, then 10.65 / 11.00 / 11.35. Rest of state 7.50 ×3, 7.85, 8.35, 8.80, 9.45, then 10.00 / 10.35 / 10.70. The summary confirms 2025–26. | S |
| 22 | §2.1; Table 1 | Fast-food rate outside NYC; chains of 30 or more establishments nationally | CR146 §146-1.2(a)(2); NYSDOL (n.d.-a) | Outside NYC 10.75, 11.75, 12.75, 13.75, 14.50, 15.00 (1 Jul 2021), 15.50 (2025), 16.00 (2026). The 30-establishment threshold is in **§146-3.13(b)**, not §146-1.2. The Part 146 summary lists fast food at $16.50 / $17.00 on LI and $15.50 / $16.00 for the rest of state in 2025–26, consistent with the "effective" column. | S for 2017–2026. Add §146-3.13(b). The 2016 entry is wrong (claim 13) |
| 23 | §1 ¶1 | 2027: neither rate will rise | NYSDOL (2026a) | dol.ny.gov/minimum-wage: "On January 1, 2027, New York's minimum wage will stay the same"; off-ramp met; $17 / $16. The page shows no date. | S. Date should be n.d. |
| 24 | §2.1 | Pennsylvania $7.25 throughout | USDOL WHD (2024, 2026) | History table "Selected Years 1968 to 2024", "last revised in January 2025": PA $7.25 in 2014–2024. State table "updated July 1, 2026": PA $7.25. | S. Year of the first source should be 2025 |
| 25 | §2.2 | QCEW concepts and county files | BLS (2026) | Data-set citation; not content-checked by this audit. | U (not in scope) |
| 26 | §4.1 | Intervals within the literature's range: about zero (Dube 2010; Cengiz 2019) to modest negative for low-wage groups (Neumark 2014) | as cited | Neumark et al. report teen elasticities near −0.15. | P. Say "for teenagers (about −0.15)" rather than "low-wage groups" |
| 27 | §4.2 | Establishment-count results relevant to entry/exit studies "that use administrative establishment counts" | Aaronson et al. (2018); Luca & Luca (2019) | Aaronson et al.: establishment-level QCEW (UCL full text, data section). Luca & Luca: Yelp listings. | X for Luca & Luca. Reword (see §4 below) |
| 28 | §4.2 | NY+PA panel similar in sign to near-zero border-county estimates | Dube et al. (2010); Addison et al. (2012) | See claim 3. A directly relevant NY–PA study is not cited: Bram, Karahan & Moore (2019), QCEW border counties; leisure-and-hospitality employment showed no relative decline while wages rose. | P. Drop or reword Addison; add Bram et al. |
| 29 | §1 ¶1 | "Legislation passed in 2016" set the regional paths | none | True (the 2016 state budget legislation amending Labor Law §652), but uncited. | U. Add a citation (NY Labor Law §652 or the NYSDOL history page) |

---

## 3. Reference table

Crossref columns are as returned by `api.crossref.org/works/{DOI}` on 29 Oct 2026.

| Reference | DOI or URL | Resolves | Metadata vs Crossref or source | Issues |
|---|---|---|---|---|
| Aaronson (2001) | 10.1162/003465301750160126 | Yes | REStat 83(1), 158–169, 2001 | None |
| Aaronson, French, Sorkin & To (2018) | 10.1111/iere.12262 | Yes | IER 59(1), 51–84, 2018 | None |
| Abadie, Diamond & Hainmueller (2010) | 10.1198/jasa.2009.ap08746 | Yes | JASA 105(490), 493–505, 2010 | None |
| Addison, Blackburn & Cotti (2012) | 10.1111/j.1467-8543.2010.00819.x | Yes | BJIR 50(3), 412–435; issue 2012 (online 2010) | Metadata OK; mischaracterised in text (claim 3) |
| Ahn (2026) | 10.31235/osf.io/chktv_v1 | Yes | posted-content, Jayden Ahn, 28 Mar 2026, SocArXiv | OK. OSF shows a version 2 (last edited 28 Mar 2026); the DOI cited is v1, which is acceptable |
| Allegretto & Nadler (2015) | 10.1111/irel.12108 | Yes | Ind. Relations 54(4), 622–647, 2015 | None |
| Allegretto & Reich (2018) | 10.1177/0019793917713735 | Yes | ILR Review 71(1), 35–63, 2018 | None |
| Ashenfelter & Jurajda (2022) | 10.1086/718190 | Yes | JOLE 40(S1), S179–S201, 2022 | None |
| Baker (2025) | 10.21203/rs.3.rs-7889672/v1 | Yes | posted-content, Peter Baker, 21 Oct 2025, Research Square | None |
| Card & Krueger (1993) | 10.3386/w4509 | Yes | NBER report, Oct 1993 | Initial should be "Krueger, A. B." **Replace with the 1994 AER article** (§4) |
| Cengiz, Dube, Lindner & Zipperer (2019) | 10.1093/qje/qjz014 | Yes | QJE 134(3), 1405–1454, 2019 | None |
| Conley & Taber (2011) | 10.1162/REST_a_00049 | Yes | REStat 93(1), 113–125, 2011 | None |
| Dube, Lester & Reich (2010) | 10.1162/REST_a_00039 | Yes | REStat 92(4), 945–964, 2010 | None |
| Even & Macpherson (2014) | 10.4284/0038-4038-2012.283 | Yes | SEJ 80(3), 633–655, 2014 | None |
| Ferman & Pinto (2019) | 10.1162/rest_a_00759 | Yes | REStat 101(3), 452–467, 2019 | None |
| Hoffman (2016) | 10.1177/0019793915610558 | Yes | ILR Review 69(2), 295–311, 2016 | None |
| Jardim et al. (2022) | 10.1257/pol.20180578 | Yes | AEJ: Policy 14(2), 263–314, 2022; six authors match | None |
| Luca & Luca (2019) | 10.3386/w25806 | Yes | NBER WP 25806, May 2019 | Metadata OK; mischaracterised in §4.2 (claim 27) |
| Manning (2021) | 10.1257/jep.35.1.3 | Yes | JEP 35(1), 3–26, 2021 | None |
| Neumark, Salas & Wascher (2014) | 10.1177/00197939140670s307 | Yes | ILR Review 67(3_suppl), 608–648, 2014 | APA form for the issue: *67*(3, Suppl.). Crossref title uses an em dash ("Minimum Wage—Employment") |
| Neumark & Shirley (2022) | 10.1111/irel.12306 | Yes | Ind. Relations 61(4), 384–417, 2022 | None |
| Sabia, Burkhauser & Hansen (2012) | 10.1177/001979391206500207 | Yes | ILR Review 65(2), 350–376, 2012 | None |
| NYSDOL (n.d.-a) History of the minimum wage | dol.ny.gov/history-minimum-wage-new-york-state | Yes | Title matches ("History of the Minimum Wage in New York State"); undated | None |
| NYSDOL (n.d.-b) CR146 | forms.labor.ny.gov/WP/CR146.pdf | Yes | 12 NYCRR Part 146, Hospitality Industry Wage Order, "As Amended", form code "CR 146 (09/24)" | Exact title wording on the cover not verified. Consider dating 2024 from the form code. Add §146-3.13(b) for the fast-food definition |
| NYSDOL (2026a) Minimum wage | dol.ny.gov/minimum-wage | Yes | Page heading "Your New York State Minimum Wage"; no date shown | Should be **n.d.-c** (or n.d.-a/b/c re-lettered in APA order) |
| NYSDOL (2026b) Part 146 summary | forms.labor.ny.gov/WP/Part146.pdf | Yes | "Wage Order Summary, Hospitality Industry", rev. 02/26 | None |
| BLS (2026) QCEW | bls.gov/cew/ | Not checked | Data set | Not in scope |
| USDOL WHD (2024) history table | dol.gov/agencies/whd/state/minimum-wage/history | Yes | Title verified; "last revised in January 2025" | Year should be **2025** |
| USDOL WHD (2026) State minimum wage laws | dol.gov/agencies/whd/minimum-wage/state | Yes | "Updated July 1, 2026" verified | None |

**In-text and reference-list match:** every in-text citation (body, tables and figure captions) has a reference entry, and every entry is cited. When the dates change (n.d.-c; USDOL 2025), update the in-text forms to match.

---

## 4. Corrected entries and suggested wording

**Card & Krueger: replace the NBER working paper with the journal article.** Verified on JSTOR 29 Oct 2026. Crossref has no DOI for the 1994 AER article (a bibliographic query returns only the NBER paper and the 2000 reply), so the stable URL is used.

> Card, D., & Krueger, A. B. (1994). Minimum wages and employment: A case study of the fast-food industry in New Jersey and Pennsylvania. *American Economic Review*, *84*(4), 772–793. https://www.jstor.org/stable/2118030

In-text: "Card and Krueger (1994)". The 1993 working paper is a pre-publication version of the same study. The peer-reviewed article is the standard citation, and the brief's reason for citing the WP ("AER 1994 version not in Crossref") is not a reason under APA.

**NYSDOL minimum wage page:**
> New York State Department of Labor. (n.d.-c). *Minimum wage*. Retrieved October 28, 2026, from https://dol.ny.gov/minimum-wage

Re-letter n.d. entries in alphabetical order of title, per APA 8.15: "History…" = a, "Minimum wage" = b, "Minimum wage order…/Hospitality…" = c. Update the citations in §1, §2.1 and the Figure 1 caption to match.

**USDOL history table:**
> U.S. Department of Labor, Wage and Hour Division. (2025). *Changes in basic minimum wages in non-farm employment under state law: Selected years 1968 to 2024*. Retrieved October 28, 2026, from https://www.dol.gov/agencies/whd/state/minimum-wage/history

**CR146 (optional):** date it 2024 from the form code "CR 146 (09/24)" and use the document's own title, *Hospitality industry wage order (12 NYCRR Part 146)*. Check the cover-page wording before changing it.

**Neumark et al. (2014):** change "*67*(3_suppl)" to "*67*(3, Suppl.)".

**§1 ¶3, Addison:** suggested wording: "County-pair designs that compare neighbouring counties across state borders found no adverse employment effects in restaurants (Dube et al., 2010), as did county panels that control for county-specific trends in restaurant-and-bar employment (Addison et al., 2012)…"

**§4.2, entry and exit:** suggested wording: "…relevant to studies of minimum wages and restaurant entry and exit, especially those that use administrative establishment counts (Aaronson et al., 2018); Luca and Luca (2019) studied exit using Yelp listings."

**§4.2, NY–PA:** add the following, after verifying the APA blog format:
> Bram, J., Karahan, F., & Moore, B. (2019, September 25). Minimum wage impacts along the New York–Pennsylvania border. *Liberty Street Economics*, Federal Reserve Bank of New York. https://libertystreeteconomics.newyorkfed.org/2019/09/minimum-wage-impacts-along-the-new-york-pennsylvania-border/

(URL from the search result, which the fetch resolved to the post. QCEW border counties; leisure and hospitality and retail; wages rose faster on the NY side, with "no discernible effect on employment".)

**§1 ¶4 and Table 1, fast food:** "since 31 December 2015". In Table 1, 2016 fast-food columns = 9.75 (both regions), with a source note. **Unverified against an official source:** confirm with NYSDOL's 2015 fast-food order or archived history before editing. If the code uses 9.00 for fast food in 2016, check `minwage_schedule.csv` and the effective-rate robustness row. The gap is zero either way, so the estimates should not change.

**§1 ¶3, Seattle:** either "A study of Seattle found reductions in hours worked at low wages (Jardim et al., 2022)", or add a verified contrasting Seattle study.

**§4.1:** "…to modest negative values for teenagers (about −0.15; Neumark et al., 2014)".

---

## 5. Novelty assessment

**Claim in the paper (§1 ¶6):** four contributions:

1. LI vs the rest of the state with the official quarterly schedule, including the 2023 narrowing.
2. Full-service vs limited-service, with the tipped and fast-food exposure coded.
3. Placebo inference and synthetic control.
4. The 2017Q1 establishment-count break.

The paper adds the hedge "not aware of an earlier study of the Long Island schedule that does these things; search limited to Crossref and OpenAlex."

**Searches run (29 Oct 2026):**
- Crossref bibliographic queries.
- OpenAlex queries, 2016 onward: "minimum wage New York upstate downstate employment", "…restaurants county employment", "New York $15 minimum wage employment effects", "regional minimum wage New York Long Island Westchester", "…fast food wage order employment", "…tipped restaurants employment".
- Web searches for LI/Westchester/upstate restaurant studies, NY within-state variation, and Empire Center, Fiscal Policy Institute and Employment Policies Institute analyses.

**Related work found:**

| Work | What it does | Bearing on novelty |
|---|---|---|
| Ahn (2026), SocArXiv (cited) | County QCEW NAICS 722513, NY 2010s–2020s; a Post_t indicator with county and time FE; descriptive upstate vs "downstate metropolitan" comparison | Closest. It does not model the LI–upstate gap, the 2023 narrowing, full-service, wages or establishments. Contributions 1–3 survive. The paper should say that Ahn already compares upstate and downstate, descriptively |
| NY Division of the Budget, *Report on New York State minimum wage increases scheduled for 2021* (undated; c. Dec 2020; ny.gov PDF) and *…scheduled for 2023* (30 Sep 2022; hosted at dol.ny.gov) (not cited) | Statutory reports: regional (NYC / LI–Westchester / upstate) labour-market trends, including QCEW leisure and hospitality by region; no causal estimate; no NAICS 722 | Official descriptive LI–Westchester vs upstate comparisons exist. Cite them as context; they do not undercut the causal or design contributions |
| Bram, Karahan & Moore (2019), NY Fed *Liberty Street Economics* (not cited) | NY–PA border counties, QCEW, leisure and hospitality and retail; wages up, no employment effect | Prior evidence for the §3.4 NY+PA comparison. Should be cited |
| Reich, Allegretto & Jacobs (2016), *The effects of a $15 minimum wage in New York State* (found in OpenAlex; not otherwise verified) | Ex-ante simulation | Optional context; not ex-post |
| minimumwage.com (Employment Policies Institute), "New data: NY restaurants lost 10K jobs since last summer" (Jan 2026; web result only, not read) | Advocacy data note | Not research. Note only if the paper engages with public claims |

**Verdict:** the novelty claim **holds in substance**: I found no study that uses the Long Island–upstate regional gap, its 2023 narrowing, or the 2017Q1 QCEW establishment break. It **needs narrowing and updating in three respects:**

1. Acknowledge that official DOB reports have tracked LI–Westchester vs upstate trends descriptively, and that Ahn (2026) compared downstate with upstate counties, descriptively.
2. Cite Bram et al. (2019) for the NY–PA comparison.
3. Update the search statement, e.g. "Crossref and OpenAlex queries and web searches for grey literature."

The 2017Q1 break claim is appropriately hedged ("I have not been able to confirm the cause"). I found no prior documentation of it, but the search was not exhaustive (for example, I did not search BLS QCEW revision notes).

---

## 6. Items not verified
- The full text of Addison et al. (2012): whether any border-pair specification appears.
- An official source for the 31 Dec 2015 fast-food rate ($9.75 outside NYC); only a law-firm summary was read.
- The exact cover title of CR146.pdf.
- The BLS QCEW data-set citation; QCEW methodology claims in §2.2 were out of scope.
- The Reich, Allegretto & Godøy (2017) and Reich, Allegretto & Jacobs (2016) metadata: OpenAlex hits only.
