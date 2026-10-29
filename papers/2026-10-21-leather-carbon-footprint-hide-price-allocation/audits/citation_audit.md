# Citation audit: "Leather's carbon bill follows the hide price, not the cow"

Auditor: independent agent (did not write the manuscript). Date: 2026-10-20. Manuscript audited: `/home/claude/p7/pkg/manuscript/manuscript.md` (not edited).

**Reading methods.** For each source the method is listed below. "Browser" means the raw page text or the PDF text (extracted with pdf.js) was read in Chrome, so the quotes are exact. "WebFetch" means a fetch that summarises: its quotes were requested verbatim, but they may be lightly normalised. The literature briefs (`/home/claude/p7/lit/brief.md`, `/home/claude/p5/lit/brief.md`) were used only as a map. Every verdict below rests on my own reading, except where it is marked otherwise.

**Checks resting on abstracts or secondary sources (stated plainly):**
- **Rotz et al. 2019.** Only the abstract was read (IDEAS/RePEc). ScienceDirect was not accessed.
- **LWG 1.8%, UNIDO 1.5% and the US study's 1% / 4.8%.** These were read only on LHCA's own web pages, which are an interested party. The underlying reports were not read.
- **LHCA's ~15% hides wasted in 2024.** Read in the leatherbiz feature via WebFetch, because the browser hit a login wall. It is corroborated by World Footwear (11 Dec 2024), which is also secondary.
- **ISO 14044.** Paywalled and not read. FAO LEAP (2016) cites ISO 14044:2006 4.3.4.2 for the stepwise procedure, which is secondary support only.
- **Roncevich et al. 2026.** The full main text was read in the browser. The Supporting Information was not read. The identities of refs 9, 24, 25 and 26 come from the Crossref reference metadata, because the reference list did not render on the page.
- **Mekonnen & Hoekstra 2010.** The main report was read via WebFetch. Appendix V (the price basis) was not read.
- **leatherbiz pages.** All were read via WebFetch (the browser asks for a login, and I did not sign in).

---

## 1. Claim-by-claim table

| # | Claim in manuscript (section) | Source | Supporting quote (verbatim) | Verdict | Suggested fix |
|---|---|---|---|---|---|
| 1 | PEFCR: hides and skins 3.5%, fresh meat and edible offal 92.9%, "no change of allocation factors is allowed" (§1) | De Rosa-Giglio et al. 2018, Table 19 (PDF p.83, "Page \| 65"); browser, pdf.js | "Fresh meat and edible offal: 92,9% Hides and skins: 3,5% … Cat 1/2 material & waste: 0,0% No change of allocation factors is allowed." Table caption (PDF p.82): "Table 19 Allocation rules" | SUPPORTED | Optionally give pages: "Table 19, pp. 64–65". |
| 2 | PEFCR allocates at the slaughterhouse among meat, hide, fat, bones and other outputs (§2.2) | same | "upstream burden shall be allocated to slaughterhouse and rendering outputs using the economic allocation method" (list as in #1) | SUPPORTED | – |
| 3 | PEFCR gives 0% to hides that are legally waste (§4.1) | same, lines 529–533 | "if it can be demonstrated that the hides or skins are obtained from animals that have been killed for eradicating a disease or that died at the farm or that were stillborn, then such animal by-products are legally treated as waste and they shall carry a 0% allocation." | SUPPORTED | – |
| 4 | Lunesu: 2.68% average using 2023 prices (§1, §3.4) | Lunesu et al. 2025, PMC12729734; browser | "Economic allocation of hide … shows markedly lower values for all animal categories … averaging 2.68% for 2023." Table 3: "Economic allocation of raw hide in the INALCA system (average prices in 2023)." | SUPPORTED | – |
| 5 | Lunesu: mass 5.88% (§1, §3.4) | same | "Physical allocation of hide ranges from a minimum of 4.2% in cull dairy cows … to a maximum of 6.9% in semi-heavy young bulls …, with a mean of 5.88%" | SUPPORTED | – |
| 6 | Lunesu: 0.12 m² per kg raw hide, average for Vicenza tanneries (§2.4) | same, Table 5 | "Table 5 reports the data of Vicenza tanning district [32], calculated as m2 of processed leather, on minimum, maximum and average yields"; Table 5 row: "Economic … Average (m2/kg) 0.12" | SUPPORTED | – |
| 7 | Lunesu: economic allocation "tends to fall" over 2015–2023 Italian prices, not tabulated (§1) | same | "these values, if recalculated over the historical series in Table 4, tend to fall due to the relative loss of hide value compared with meat: for dairy cows, for example, the ratio was 0.70 in 2015, falling to 0.19 in 2023." | SUPPORTED | – |
| 8 | Italian 2.68% above US because the Italian hide-to-meat price ratio is higher (§3.4) | author's inference | none | Inference (not a citation claim) | Make it a hedged inference, e.g. "plausibly reflecting …". |
| 9 | Desjardins: 6.8% economic using 2006 US prices; 6.2% mass (§1, §3.4) | Desjardins et al. 2012, MDPI full text; browser | Table 3 row: "Hide, raw 4.9% 6.2% 6.8%" (columns % SLW / Mass / Economic). "Unit prices for meat, products for rendering, raw hide (uncured, unsalted) and offal have been gathered, for the year 2006, from USDA market statistics [58] and are respectively 3.07, 0.29, 1.93, and 1.19 US$ per kg product." | SUPPORTED | – |
| 10 | Desjardins: hide prices roughly halved 2006–2009 (§1) | same | "However, between 2006 and 2009, the value of hides almost decreased by half whereas the price of meat remained relatively constant." | SUPPORTED | "almost halved" would be closer to the source. |
| 11 | Roncevich: 8.1%, from 6.8/8/14% for Italy/India/North America weighted by 2022 export shares, assuming US = Canada (§1, §4.2) | Roncevich et al. 2026, ACS full text; browser | "The global production-weighted average economic allocation was 8.1%. This amount was based on reported values of 6.8%, 8%, and 14% for Italy, India, and North America, respectively, (9,24,25) weighted by each region's share of global raw hide exports in 2022, which were 18.4%, 2.7%, and 10.6%, respectively (26) …, with the assumption that the US would exhibit the same economic allocation ratio as Canada." | SUPPORTED | See note A below. |
| 12 | Roncevich quoted: allocation should "accurately reflect changes in this allocation across time" (§1) | same | "the allocation should accurately reflect changes in this allocation across time and regions globally, from both dairy and non-dairy producing systems, as we have done in our top-down analysis" | SUPPORTED (quote exact) | For fairness, add that the authors say they did this: "…, which they state their top-down analysis does, although it applies a single factor." |
| 13 | Roncevich: footprint "far above earlier estimates" (§1) | same, abstract | "The revised analysis produces a farming-phase carbon footprint that is more than double that of prior estimates." | SUPPORTED | – |
| 14 | Roncevich gives no prices or price year for the 14%; Desjardins is the only North American source cited for the factor (§4.2) | same, plus Crossref reference metadata | Refs (9, 24, 25) = Joseph & Nithya 2009 (doi:10.1016/j.jclepro.2008.11.018), Desjardins 2012 (doi:10.3390/su4123279), Notarnicola 2011 (Afinidad 68(553):167). No price or price year for the 14% in the main text. | SUPPORTED for the main text (SI not read) | The manuscript already says the SI was not read. Keep that. |
| 15 | LHCA critique rebuttal "centred largely on that factor" (§1) | LHCA 2026; browser | "That twelvefold gap rests on one input more than any other: an 8.1% economic allocation of farm-stage emissions to hides" | SUPPORTED | – |
| 16 | LWG 1.8% (§1, §3.4) | LHCA 2026; browser | "The Leather Working Group's own 2024 LCA … lands in the same range: an average economic allocation of 1.8% and a mass fraction of 7.8%" | SUPPORTED (secondary) | Already flagged as LHCA-only in §4.3. |
| 17 | UNIDO 2026 guidance 1.5% (§1, §3.4) | LHCA 2026; browser | "UNIDO's 2026 Guidelines for Assessing the Environmental Footprint of Leather, built on 299 primary-data studies across 87 tanneries in 26 countries, sets that allocation at 1.50% instead" | SUPPORTED (secondary) | – |
| 18 | Industry-funded US study tested 1% economic and 4.8% mass (§1, §2.4) | LHCA 2025; browser | "Three different allocation scenarios were used: The current, European-standard Product Environmental Footprint (PEF) economic value of the hide (3.5%) as a percentage of the cow's value, the U.S. hide mass fraction (4.8%), and the US economic value of the hide (1%)." | SUPPORTED | – |
| 19 | "Physical allocation by mass gives about 5% to 6%" (Desjardins; Lunesu; LHCA 2025) (§1); "a physical basis … gives the hide 5% to 6%" (§4.2) | Desjardins 6.2%; Lunesu 5.88% (range 4.2–6.9%); LHCA 2025 4.8%. LHCA 2026 also reports industry mass factors of 7–7.8%. | LHCA 2026: "PEFCR's 7% becomes UNIDO's 7.33%"; LWG "a mass fraction of 7.8%" | PARTLY | Write "about 5% to 6% in the studies cited here (4.8–6.2%), and up to 7–8% in industry figures reported by LHCA (2026)", or change the range to "5% to 8%". Note the PEFCR 7% mass figure was not found in the 2018 PEFCR text, so attribute it to LHCA. |
| 20 | LHCA: about 15% of US hides wasted in 2024 (§4.1) | leatherbiz 2024 "A startling revelation" (WebFetch; login wall in browser); World Footwear, 11 Dec 2024 | leatherbiz: "from a figure of 7% in 2023, the percentage of hides going to waste in the US" is "closer to 15%" (as stated by LHCA). World Footwear: "The proportion of wasted hides more than doubled in the US from 7% in 2023 to 15% in 2024." | SUPPORTED (secondary) | – |
| 21 | Rotz: 21.3 kg CO2e per kg carcass, cradle to farm gate, whole US herd including dairy culls (§2.4) | Rotz et al. 2019, abstract only (IDEAS) | "Environmental intensities expressed per kg of carcass weight produced were 21.3 ± 2.3 kg CO2e"; the LCA covered "all production systems including traditional beef breeds and cull animals from the dairy industry." | SUPPORTED (abstract) | – |
| 22 | FAO LEAP recommends economic allocation among slaughter products serving different markets; economic value "possibly over a 5-year time frame" (§2.3, §4.2) | FAO 2016, full PDF; browser, pdf.js | p.xxxvii summary (PDF p.39): "9.3.2 Meat processing Revenue based allocation is recommended for products which serve different markets (e.g., edible products vs. rendering products vs. hides)." Glossary (PDF p.27): "Economic value Average market value of a product at the point of production possibly over a 5-year time frame. – Adapted from: PAS 2050:2011, 3.17" | SUPPORTED | Note: the 5-year wording is in the glossary, not the slaughter section. The manuscript's "define economic value as" is accurate. |
| 23 | UNIDO mass balance assumes 4 m² per hide (§2.4) | Buljan et al. 2000; WebFetch | "1000 kg of wet salted cattle hides (39 pieces, green weight 1100 kg)"; "25 - 29.5 kg green weight, about 25.6 kg salted weight per hide"; "average area 4 m2/hide" | PARTLY | The 4 m² in UNIDO is the area of a raw 25.6 kg salted hide. The manuscript's 4.0 m² is finished leather from a ~33 kg US hide. UNIDO's own finished yield is 138 m² grain + 60 m² split per 39 hides (≈3.5 m² grain, ≈5.1 m² total per hide, per the brief). Fix: "close to the 4 m² hide area in UNIDO's mass balance (Buljan et al., 2000), which yields about 3.5 m² of grain leather per hide". |
| 24 | Mekonnen & Hoekstra: 5% value fraction for leather in a worked example (§3.4) | Mekonnen & Hoekstra 2010, Vol. 1; WebFetch | Table 5 ("The components of the water footprint of a beef cow and its derived products"): "… of which 5% is attributed to the 6.1 kg of resultant leather". Other fractions: beef 83%, offal 10%, semen 2%. | SUPPORTED (value). Price basis not checked (Appendix V not read). | Optionally say that the price period and region are given in their Appendix V. Matching it to "the US share of the 2000s" is the author's comparison. |
| 25 | Muhammad & Griffith: hide prices fell after 2014 as leather demand weakened and US exports to China contracted (§1); loss of Chinese demand after 2018 (§4.1) | Muhammad & Griffith 2023; browser | "In 2013, raw cattle hides and skins were a major agricultural export for the U.S., reaching $2.3 billion, with China accounting for 63%." "…exports were only $876 million" (2022). "…exports to China have been declining for nearly a decade." China's imports from the US "fell by 66% during this period" (2018–19 trade war). Causes include "growing competition from synthetic materials, rising labor costs, and stricter environmental regulations." | SUPPORTED (§1); PARTLY (§4.1) | The source does not discuss hide prices directly. In §4.1, "loss of Chinese demand after 2018" understates the source, which says the decline predates the trade war. Suggest "a decade-long fall in Chinese demand, sharpened by the 2018–19 trade war". |
| 26 | Hide share of packer by-product value about two-thirds in 2000, under a fifth by 2020 (LHCA via leatherbiz) (§1) | leatherbiz 2020a ("'Staggering decline' in the hide's share of cattle value"); WebFetch | "Between 1980 and 2011, hides averaged 58.3% of the total value of cattle by-products"; "This reached a high of 67% in 2000."; "Hides presently constitute only 15%-20% of the total by-product value of the animal" | SUPPORTED, with minor wording issue | "Under a fifth" holds at the upper bound only. Use "15–20% in 2020". The in-text citation reads "(LHCA, as reported in leatherbiz, 2020)", which is missing the suffix. Change it to "leatherbiz, 2020a". |
| 27 | LHCA: hide "closer to 1%" of the animal's value in late April 2020 (§2.3, §3.3) | leatherbiz 2020a | "At the end of April, a US steer hide had a value closer to 1% of the entire value of the animal." | SUPPORTED | The source says "a US steer hide", which supports the comparison. |
| 28 | Peel 2024: by-products 6.4% of fed steer value and hide 18.4% of by-products, 1 March 2024 (§2.3, §3.3) | Peel 2024, Farm Progress; browser | "The steer by-product value for Friday, March 1, was $11.64/cwt. and shows that tallow is the largest contributor … hides were second at 18.4 percent … by-products currently represent a smaller percentage of total cattle value (6.4 percent) than the long-term average (9.5 percent)." | SUPPORTED | – |
| 29 | Peel 2019: butt-branded steer hide averages $74.36 (2013–17), $47.93 (2018), $34.46 (H1 2019), $27.60 (June 2019), "from AMS data" (§2.1) | Drovers page (dated 19 Nov 2020) and original OSU Cow-Calf Corner, 24/29 July 2019 (TSCRA repost); WebFetch | "In the period 2013-2017, hide values (butt-branded, steer) averaged $74.36/piece (animal)"; "In 2018, hides represented 45.6 percent of by-product value with an average value of $47.93/piece."; "In the first half of 2019, hides have averaged $34.46/piece"; "The June monthly average hide value was $27.60/piece." | PARTLY | The numbers are correct. (a) Neither version names AMS as the data source, so drop "from AMS data" or write "(butt-branded steer)". (b) The Drovers URL is stamped 19 Nov 2020, while the column dates from July 2019. Cite the original or give both dates (see the references section). |
| 30 | Brester & Swanser: $36.50 at start of 2020 to just over $18 in April 2020 (§2.1, §3.1); quantified the price effect (§1) | Brester & Swanser 2021, AgEcon PDF; WebFetch | "By April of 2020, hide values had declined from $36.50 per steer at the start of the year … just to over $18 per steer -- a decrease of 50.3%." "cattle prices declined by 6.5% (or $6.30/cwt) as the result of lower hide values." Hide series: "Price of Butt Branded Steer Hides" (USDA AMS). | SUPPORTED | The source reads "just to over $18". The manuscript's "just over $18" in quotation marks (§3.1) is a slight misquote. Drop the quotation marks or quote exactly. |
| 31 | Kay 2020: butt-branded steer hide $30 at end of September 2020, citing USDA (§2.1) | Kay 2020, WLJ; WebFetch | "USDA at the end of September reported a butt-branded steer hide brought $30." | SUPPORTED | – |
| 32 | leatherbiz 2020b: a 2020 trade quote citing USDA (§2.1) | leatherbiz Intelligence 156430, 24/11/2020; WebFetch | "$33 for a butt-branded steer hide weighing 64-66 pounds"; "The source of these figures is the US Department of Agriculture." (described as "ballpark" figures) | SUPPORTED | Fix the reference title (see below). |
| 33 | Peck 2025: hide $25.04 in AMS drop value (§2.1) | Peck 2025, Beef Magazine; WebFetch | "USDA's Agricultural Marketing Service recently reported that of the $161.42 per head byproduct credit based on a 1,400 lb. steer, $25.04 can be attributed to the hide." | SUPPORTED | The report date is not given ("recently", article dated 17 Feb 2025). The manuscript should say how it dated this quote, e.g. assumed to be February 2025. |
| 34 | Branded cow hides $1 a piece in May 2025 (§4.3) | leatherbiz 2025; WebFetch | USDA's major packer hide report lists "branded south-west cow hides, each weighing 50-52 pounds (22.7-23.6 kilos), with a weighted average price of $1 per piece" (report dated May 8, 2025) | SUPPORTED | Optionally "branded south-west cow hides". |
| 35 | AMS 28 Apr 2015: butt-branded steer hide $95.75; hide 4.80 lb per cwt live, cured and fleshed; 63% dressing (§2.1, §2.2, §2.4) | USDA AMS 2015 overview PDF; WebFetch | "Steer hide, butt brand/Pc 4.80 95.75 - 6.96 50.58%"; "The weight for the butt branded steer hide reflects a cured and fleshed basis and a per piece price."; "a 1375 pound live steer at 63% dressing percent" | SUPPORTED | – |
| 36 | AMS 27 Oct 2017: $56.00 (§2.1) | NW_LS441 TXT; WebFetch | "Steer hide, butt brand/Pc 4.82 56.00 - 4.00" | SUPPORTED | – |
| 37 | AMS 8 Nov 2019: $36.00–36.50 (§2.1) | NW_LS448 TXT (Major Packer Hide Report); WebFetch | "BUTT BRAND STR … 62-64# 36.00 A … 64-66# 36.50 D" | SUPPORTED (price). The reference title is WRONG. | This is the Major Packer Hide Report, not a "National Weekly Hide and Offal Report". The letters A/D mean days since the last actual trade, so these are partly carried-forward quotes. Consider noting that. |
| 38 | AMS 23 May 2025: $15.25 (§2.1, §3.1) | AMS_2830 PDF (NW_LS448); WebFetch | "Branded (Butt) 60 - 62 lbs 1.00 15.25 15.25 F.O.B." (one load) | SUPPORTED | Add the title (below). Note it is a single-load trade at 60–62 lb, which may help explain the 29% miss. |
| 39 | AMS 26 Aug 2025: $19.25; $1.38/cwt live (§2.1, §3.3) | AMS_2829 PDF; WebFetch | "Steer Hides, Branded (Butt) 4.70 19.25 UNCH 1.38" | SUPPORTED | – |
| 40 | AMS 30 Sep 2025: $19.00; $1.36/cwt live (§2.1, §3.3) | AMS_2829 PDF; WebFetch | "Steer Hides, Branded (Butt) 4.77 19.00 UNCH 1.36" | SUPPORTED | – |
| 41 | BLS PPI WPU0419, Jun 2001 = 100, monthly, NSA (§2.1) | FRED; WebFetch | "Producer Price Index by Commodity: Hides, Skins, Leather, and Related Products: Hides and Skins, Including Cattle"; "Index Jun 2001=100"; "Monthly"; "Not Seasonally Adjusted" | SUPPORTED | – |
| 42 | ISO 14044 hierarchy: avoid allocation, then physical, then economic (§1) | ISO 2006 (not read; paywalled) | Secondary only: FAO LEAP (2016) §9.1–9.2 cites ISO 14044:2006 4.3.4.2 | UNVERIFIABLE (primary) | The claim is standard and uncontroversial. Optionally add "clause 4.3.4.2". |
| 43 | ERS Livestock and Meat Domestic Data, machine-readable files (§2.2) | ERS page; WebFetch | Page title "Livestock and Meat Domestic Data"; "Livestock domestic data machine-readable files" (ZIP of CSVs); last updated 9/29/2026 | SUPPORTED (page loads, title matches) | – |

**Note A (Roncevich arithmetic: a finding for the author, not an error in the manuscript).** Roncevich et al. give two weightings. The export shares they state (Italy 18.4%, India 2.7%, North America 10.6%) normalise to weights of 0.58 / 0.085 / 0.334, which would give **9.3%**. A later sentence in their methods applies weights "0.34, 0.58, and 0.08" to the factor vector (6.8%, 8%, 14%), which gives **8.07% ≈ 8.1%**. The published 8.1% therefore appears to pair the weights with the wrong regions. My arithmetic: 6.8×0.34 + 8×0.58 + 14×0.08 = 8.07. The verbatim sentence reads: "Regional annual emissions per animal are multiplied by a vector of the economic allocation ratio for hides (6.8%, 8%, and 14% allocation with weights reflecting regional contributions toward the global total of 0.34, 0.58, and 0.08, respectively)". The manuscript's description of the 8.1% matches the paper's own wording, so no fix is required. The author may wish to mention this internal inconsistency in §4.2.

**Note B (date of leatherbiz 2020a).** The page prints "06/05/2020". leatherbiz prints dates as DD/MM/YYYY elsewhere (for example "24/11/2020" and "14/05/2025"), so this most likely means **6 May 2020**, not June. The text's "At the end of April" fits either. The page could not be opened in the browser (login wall) or on the Wayback Machine (blocked) to confirm.

**Note C (citation key collisions).** The in-text citation "(LHCA, as reported in leatherbiz, 2020)" in §1 needs "2020a". The in-text citation "(LHCA, 2025, 2026)" for the LWG, UNIDO and US factors is accurate: the 2026 page states all three and the 2025 page states the US 1%.

---

## 2. Crossref / DOI table

| Reference | DOI | Resolves | Registry metadata | Manuscript entry | Mismatch |
|---|---|---|---|---|---|
| Desjardins et al. 2012 | 10.3390/su4123279 | Yes (Crossref) | Raymond Desjardins, Devon Worth, Xavier Vergé, Dominique Maxime, Jim Dyer, Darrel Cerkowniak; "Carbon Footprint of Beef Cattle"; *Sustainability* 4(12): 3279–3301; 2012 | same | None |
| Lunesu et al. 2025 | 10.3390/ani15243546 | Yes (Crossref) | Mondina Francesca Lunesu, Fabio Correddu, Silvia Carta, Sara Sechi, Marco Farina, Giuseppe Pulina; "Attributing Farm-to-Slaughter Emissions to Hides: Evidence from Beef Supply Chains"; *Animals* 15(24): 3546; published online 2025-12-09 | same | None |
| Roncevich et al. 2026 | 10.1021/acssuschemeng.5c12631 | Yes (Crossref) | Mikaila K. Roncevich, Matthew N. Hayek, Juan P. Hinestroza; "The Carbon Footprint of Leather: A Comprehensive Reassessment Using Global Livestock Data and Meta-Analysis"; *ACS Sustainable Chemistry & Engineering* 14(27): 12580–12589; online 2026-07-02, print 2026-07-13 | "Roncevich, M., Hayek, M. N., & Hinestroza, J." | Minor: the first and last authors' middle initials are missing (Roncevich, M. K.; Hinestroza, J. P.) |
| Rotz et al. 2019 | 10.1016/j.agsy.2018.11.005 | Yes (Crossref) | C. Alan Rotz, Senorpe Asem-Hiablie, Sara Place, Greg Thoma; "Environmental footprints of beef cattle production in the United States"; *Agricultural Systems* 169: 1–13; Feb 2019; no issue number | same | None |
| Brester & Swanser 2021 | 10.22004/ag.econ.309621 | Not in Crossref (the Crossref fetch failed). It is a **DataCite** DOI and resolves there. | DataCite: Gary W. Brester, Kole Swanser; "The Impact of Cattle Hide and Byproduct Values on Cattle Price Declines in 2020"; publicationYear 2021; publisher "Unknown"; URL ageconsearch.umn.edu/record/309621. IDEAS: "MSU Staff Papers", Montana State University, Department of Agricultural Economics and Economics (undated). | same | None. The PDF itself prints no date, number or affiliation, so the year 2021 rests on DataCite. |

## 3. References without DOI: URL and metadata check

| Reference | URL loads? | Title/author/date check | Issue |
|---|---|---|---|
| Buljan, Reich & Ludvik 2000 | Yes (WebFetch) | "MASS BALANCE IN LEATHER PROCESSING"; "Prepared by J. Buljan, G. Reich, J. Ludvik"; US/RAS/92/120; dated 9 August 2000 | OK. Could add the date 9 August 2000. |
| De Rosa-Giglio et al. 2018 (PEFCR) | Yes (Wayback, raw PDF) | Cover: authors as listed, "on behalf of the Leather Pilot Technical Secretariat", "Final version 25 April 2018", "Valid until 31 December 2020" | OK |
| FAO 2016 (LEAP) | Yes | "Environmental performance of large ruminant supply chains: Guidelines for assessment", Version 1 | OK. Could add "Rome" and "Version 1". |
| ISO 2006 | not checked (paywalled) | – | – |
| Kay 2020 | Yes | "Kay's Korner: Hides take a tanning", Steve Kay, Oct. 02, 2020, WLJ | OK |
| LHCA 2025 | Yes | Page H1/title: **"LCA IS LEATHER REPORTING GAMECHANGER"**, October 8, 2025; no byline | **Title wrong.** The manuscript uses the URL slug, not the headline. |
| LHCA 2026 | Yes | "The Carbon Footprint of Leather: A Critical Review of Roncevich et al. (2026)", **August 27, 2026, Karl Flowers** | Missing "(2026)" in the title, the date and the author |
| leatherbiz 2020a | Yes (WebFetch) | Headline **"'Staggering decline' in the hide's share of cattle value"**, dated 06/05/2020 (probably 6 May 2020; see Note B) | Placeholder title; date is probably wrong (June) |
| leatherbiz 2020b | Yes (WebFetch) | Headline **"US Perspective—24.11.20"**, Intelligence section, 24/11/2020 | Placeholder title; no date |
| leatherbiz 2024 | Yes (WebFetch; login wall in browser) | "A startling revelation"; no date or author shown; context late 2024 (World Footwear restates it on 11 Dec 2024) | OK. Mark as "(2024)" with no exact date. |
| leatherbiz 2025 | Yes | "US cow hides for $1", 14/05/2025 | OK |
| Mekonnen & Hoekstra 2010 | Yes (ayhoekstra.nl PDF) | "The green, blue and grey water footprint of farm animals and animal products", Volume 1: Main Report; M.M. Mekonnen and A.Y. Hoekstra; Value of Water Research Report Series No. 48; December 2010; UNESCO-IHE Institute for Water Education, Delft | OK. Add Delft, the month and a URL. |
| Muhammad & Griffith 2023 | Yes | "Can Chinese Demand for U.S. Hides and Skins Recover?", *Southern Ag Today* 3(42.4), October 19, 2023. The page's suggested citation spells the second author "Andrew **Giffith**", and the byline shows only Andrew Muhammad. | Keep "Griffith" (almost certainly a typo on the page), but add the date. |
| Peck 2025 | Yes | "Cowhides count", Clint Peck, February 17, 2025 | OK |
| Peel 2019 | Yes | Drovers page stamped **November 19, 2020**. The original column is OSU *Cow-Calf Corner*, 29 July 2019 (article dateline 24 July 2019, TSCRA repost: https://tscra.org/cow-calf-corner-7-29-19-weak-hide-values-late-summer-gestation-rates/) | The year conflicts with the URL's date stamp. |
| Peel 2024 | Yes | "Understanding beef by-product values", Derrell Peel, March 5, 2024 | OK |
| BLS/FRED WPU0419 | Yes | Title matches exactly | OK |
| USDA AMS 2015 | Yes | Printed title "USDA BY-PRODUCT DROP VALUE (STEER) – An Overview"; example report "Tue, Apr 28, 2015" | Minor title wording |
| USDA AMS 2017 | Yes | "NW_LS441 … Fri, Oct 27, 2017 … USDA BY-PRODUCT DROP VALUE (STEER) FOB CENTRAL U.S." | OK |
| USDA AMS 2019 | Yes | "NW_LS448 … Fri, Nov 08, 2019 … USDA MAJOR PACKER HIDE REPORT – FOB CENTRAL U.S." | **Title wrong** ("National Weekly Hide and Offal Report") |
| USDA AMS 2025a | Yes | "Major Packer Hide Report (NW_LS448)", "Fri May 23, 2025", "Report for 05-23-25 - Final" | Placeholder title |
| USDA AMS 2025b | Yes | "By-Product Drop Value (Steers) (Cattle) (NW_LS441 / 447)", "Tue Aug 26, 2025" | OK (code could be NW_LS441/447) |
| USDA AMS 2025c | Yes | same title, "Tue Sep 30, 2025" | OK |
| USDA ERS 2026 | Yes | "Livestock and Meat Domestic Data", updated 9/29/2026 | OK |

---

## 4. Corrected reference entries (APA 7). Only changed entries are listed.

Brester, G. W., & Swanser, K. (2021). *The impact of cattle hide and byproduct values on cattle price declines in 2020* (MSU Staff Paper). Department of Agricultural Economics and Economics, Montana State University. https://doi.org/10.22004/ag.econ.309621
*(No change needed. Year per DataCite; the PDF is undated.)*

Buljan, J., Reich, G., & Ludvik, J. (2000, August 9). *Mass balance in leather processing* (Regional Programme for Pollution Control in the Tanning Industry in South-East Asia, US/RAS/92/120). United Nations Industrial Development Organization. https://downloads.unido.org/ot/48/13/4813527/20001-_22423.PDF

FAO. (2016). *Environmental performance of large ruminant supply chains: Guidelines for assessment* (Version 1). Livestock Environmental Assessment and Performance (LEAP) Partnership, Food and Agriculture Organization of the United Nations. https://openknowledge.fao.org/handle/20.500.14283/i6494en

Leather and Hide Council of America. (2025, October 8). *LCA is leather reporting gamechanger*. https://usleather.org/news-events/example-2-lhca-funded-independent-life-cycle-assessment

Flowers, K. (2026, August 27). *The carbon footprint of leather: A critical review of Roncevich et al. (2026)*. Leather and Hide Council of America. https://usleather.org/news-events/the-carbon-footprint-of-leather-a-critical-review-of-roncevich-et-al.-2026
*(If the corporate author is kept for in-text "LHCA, 2026", use: Leather and Hide Council of America. (2026, August 27). The carbon footprint of leather: A critical review of Roncevich et al. (2026) [K. Flowers]. …)*

leatherbiz. (2020a, May 6). 'Staggering decline' in the hide's share of cattle value. https://leatherbiz.com/News/154398
*(The page prints 06/05/2020. The site's format elsewhere is DD/MM/YYYY. Confirm the date if possible.)*

leatherbiz. (2020b, November 24). US perspective—24.11.20. https://leatherbiz.com/Intelligence/156430

leatherbiz. (2024). A startling revelation. https://leatherbiz.com/Features/170285
*(No date is printed. It was published before 11 December 2024.)*

Mekonnen, M. M., & Hoekstra, A. Y. (2010). *The green, blue and grey water footprint of farm animals and animal products: Vol. 1. Main report* (Value of Water Research Report Series No. 48). UNESCO-IHE Institute for Water Education. https://ayhoekstra.nl/pubs/Report48-WaterFootprintAnimalProducts-Vol1.pdf

Muhammad, A., & Griffith, A. (2023, October 19). Can Chinese demand for U.S. hides and skins recover? *Southern Ag Today*, *3*(42.4). https://sat-wp.afpc.tamu.edu/2023/10/19/can-chinese-demand-for-u-s-hides-and-skins-recover

Peel, D. (2019, July 29). Weak hide values. *Cow-Calf Corner*, Oklahoma State University Extension. Reprinted in *Drovers* (2020, November 19) as "Weak hide values impacting cattle prices." https://www.drovers.com/news/weak-hide-values-impacting-cattle-prices
*(An alternative is to cite the Drovers page as Peel, D. (2020, November 19), and say in the text that the data run to June 2019.)*

Roncevich, M. K., Hayek, M. N., & Hinestroza, J. P. (2026). The carbon footprint of leather: A comprehensive reassessment using global livestock data and meta-analysis. *ACS Sustainable Chemistry & Engineering*, *14*(27), 12580–12589. https://doi.org/10.1021/acssuschemeng.5c12631

USDA Agricultural Marketing Service. (2015). *USDA by-product drop value (steer): An overview* [NW_LS441; includes report of 28 April 2015]. https://www.ams.usda.gov/sites/default/files/media/ByProduct%20DropValue%28Steer%29Overview.pdf

USDA Agricultural Marketing Service. (2017, October 27). *USDA by-product drop value (steer), FOB Central U.S.* [NW_LS441]. https://mymarketnews.ams.usda.gov/filerepo/sites/default/files/2829/2017-10-27/785671/NW_LS44120171027.TXT

USDA Agricultural Marketing Service. (2019, November 8). *USDA major packer hide report, FOB Central U.S.* [NW_LS448]. https://esmis.nal.usda.gov/sites/default/release-files/kw52j805z/bg257v377/v405sq61v/NW_LS448.TXT

USDA Agricultural Marketing Service. (2025a, May 23). *Major packer hide report* [NW_LS448; AMS_2830]. https://esmis.nal.usda.gov/sites/default/release-files/kw52j805z/v118tc775/h702s430s/AMS_2830.PDF

USDA Agricultural Marketing Service. (2025b, August 26). *By-product drop value (steers) (cattle)* [NW_LS441/447; AMS_2829]. https://esmis.nal.usda.gov/sites/default/release-files/p5547r46g/1257cs964/z316s222h/AMS_2829.PDF

USDA Agricultural Marketing Service. (2025c, September 30). *By-product drop value (steers) (cattle)* [NW_LS441/447; AMS_2829]. https://esmis.nal.usda.gov/sites/default/release-files/p5547r46g/cr56q013x/1r66m2528/AMS_2829.PDF

All other entries (De Rosa-Giglio et al. 2018; Desjardins et al. 2012; ISO 2006; Kay 2020; leatherbiz 2025; Lunesu et al. 2025; Peck 2025; Peel 2024; Rotz et al. 2019; BLS 2026; USDA ERS 2026) were checked and need no change.

## 5. Text fixes in priority order

1. Reference USDA AMS 2019: wrong report title. It is the Major Packer Hide Report (NW_LS448).
2. Reference LHCA 2025: wrong title. It is "LCA is leather reporting gamechanger".
3. §1: "(LHCA, as reported in leatherbiz, 2020)" should be "2020a". The leatherbiz 2020a date is probably 6 May, not June.
4. §1 and §4.2: the mass range "5% to 6%" omits the industry figures of 7–7.8% reported by LHCA (2026), and LHCA 2025's own figure is 4.8%.
5. §2.4: the UNIDO 4 m² is raw hide area for a 25.6 kg salted hide, not finished leather area.
6. §2.1: Peel does not name AMS as the source. The Peel 2019 citation year conflicts with the URL's November 2020 stamp.
7. §3.1: the quotation "just over $18" should be "just to over $18", or drop the quotation marks.
8. §4.1: Muhammad & Griffith describe a decade-long decline in Chinese demand, not one beginning in 2018.
9. Placeholder titles for leatherbiz 2020a, leatherbiz 2020b and AMS 2025a need replacing. Add middle initials for Roncevich and Hinestroza.
10. Optional: mention the weighting inconsistency in Roncevich (Note A).
