# Number and methods audit — paper 14, "Where the cattle were raised"

Auditor: independent number/methods audit (Claude, 22 Oct 2026). No package file was edited. Scratch work: `/tmp/claude-0/-home-claude/e77537ee-4bde-5960-ac22-2794b7601af1/scratchpad/p14audit` (full copy of the package, plus check scripts in `chk/`).

## 1. Reproduction

The full pipeline (build, trace, analysis, diagnostics, figures, tables, graphical_abstract) was re-run on a clean copy with `__pycache__` removed. It exited 0 in 3 min 42 s. That is longer than the README's "about two minutes", so the README should say 4 minutes.

Byte-identical to the package: `analysis.json`, `build_info.json`, `gap_*`, every result CSV and CSV.gz (compared decompressed), `tables.md`, all four PNGs, and `manuscript.md` (tables.py rewrite). The PDFs differ only in their embedded timestamps. **Verdict: reproduces.**

## 2. Methods and algebra

| Item | Finding | Verdict |
|---|---|---|
| Kastner step | `R = (I − T diag(x)^-1)^-1 P`, T[importer, exporter], x = production + imports. The row sums of R equal x, so the identity holds. | OK |
| Stage chaining | `P_{s+1} = d_s · mix_s`, where d = supply − exports and mix = R/x. A country's stage-s+1 output therefore inherits the origin mix of its total stage-s supply, as the text states. | OK |
| Mass balance | World stage-4 use equals world hide output plus a residual of at most 1.1 kt a year (<0.02%), for 2015, 2018 and 2020. The residual exists because clipping is done in one pass: after exports are scaled down, some importers' supply falls below their own exports, and `np.clip(x−exp,0)` then hides it. It is negligible, but say so or iterate the clip. | OK (minor) |
| Exports > supply ("clip") | Exports are scaled to supply once per stage. The `clipped` total is recorded before propagation and after earlier stages have been clipped, which matches "before correction" in the Table 2 caption only stage by stage. | OK |
| Top-up | Adds the missing supply with the country's existing mix. This creates hides that FAOSTAT does not record, so world mass is not conserved by design. Fine as a sensitivity, but say that it adds mass. | OK |
| EU final use net of exports | `eu_use = d[e]·mix[e]` at stage 4. Bridge identity: EU hides + Σ_s imports traced − Σ_s exports traced = d4. | OK |
| Reconciliation 20,950 + 492 + 11,149 + 248 − 15,259 | Exact in the model: the JSON `Sum` and the model value are both 17,581. The rounded terms add to 17,580 (rounding only). The 492 "re-attribution" term includes the effect of clipping EU suppliers' exports (EU hide and leather imports fall from 816.4 to 807.6 kt RHE). In hectares that effect is only −28 ha, so the label is fine; the pure re-attribution is ≈ +520 ha. | OK |
| Pooled replication | Matches `trace.origins` in Laroche `01_calculations.R`: all stages up to level 4 go into one matrix, one Kastner solve, and `R_bar = diag(ac/x) R`, with negative ac kept. Differences from Laroche: (i) missing q is imputed here, while Laroche drop it; (ii) Laroche's intensity denominator is traced level-1 output, not FAOSTAT production; (iii) HS12/v202401 and DeDuCE v1.0 there. | OK |
| HS lists | 35 subheadings at stages 1–4 plus 3 extra. They match the Laroche CF file, plus 640330 (HS02 only, given the 640399 factor). One problem: **411520 is "parings and other waste … leather dust, powder and flour", not composition leather**, yet the sensitivity treats it as finished leather at 4.02 RHE. The methods text ("patent and composition leather (4114.20, 4115)") hides this. Drop 411520 or describe it correctly. | FIX (minor) |
| Factor sets | Laroche: 1.00 (4101, wet-blue 410411/19), 4.02 (crust 410441/49 and 4107), articles 1.03–4.02. Commission: 1/2.33/4.20, with crust at 2.33. UNIDO: 1000/350 = 2.857 and 1000/255 = 3.92. Articles in the Commission and UNIDO sets = Laroche factor/4.02 × the set's finished factor. All as described. **Laroche min/mean/max differ only for articles**, so "five factor sets" is really three for hides and leather. This is why Table 2's direct-import column is 20,950 in all three Laroche rows. State this. | OK + clarify |
| Allocation | Fixed shares 2.5/3.5/5/8/10%. Economic = p_hide·h/(p_hide·h + p_beef·0.70·carcass). Mass = h/(h+carcass). Missing values filled with the year's hide-weighted mean. DeDuCE v2.1 leather share = 0.0500 in all 2,867 country-years. | OK |
| Units | FAOSTAT hides are fresh weight, while the RHE is defined as "wet-salted". Laroche make the same equivalence. Mention it. | Note |
| India | FAOSTAT has no cattle-hide output for India (flag M). The denominator is buffalo hides only (909 kt), while D is all cattle-pasture deforestation (74,274 ha a year). This probably overstates India's ha/t and its 4.1% share. Note it as a limitation. | FLAG |

## 3. Number check (against results/analysis.json)

Unless noted, the figures below are 2015–2020 means at 5% with core factors.

| Location | Claim | Correct value | Verdict | Fix |
|---|---|---|---|---|
| Abstract | 1.33 Mt RHE | 1,330,375 t | OK | – |
| Abstract | 17,581 ha; 72% Brazil | 17,581; 0.7228 | OK | – |
| Abstract | +11,149; 20,950; −15,259; 0.84× | same; 0.8392 | OK | – |
| Abstract | ratio 0.44–0.93 over factor and balance | 0.444–0.933 | OK | – |
| Abstract | rule range 8,790–35,424 | same | OK | – |
| Abstract | 41% via third country, mostly goods, China and Viet Nam | 0.4117; articles 6,649 of 7,237 indirect ha (92%) | OK | – |
| Abstract | "With the Commission's factors, recorded exports … exceeded the hides … reported to produce" | true for the Commission and UNIDO factor sets | OK as fact; see §4 | Add "FAOSTAT's imputed" before "hides" |
| Social summary | ~17,600 ha; 41% | OK | OK | – |
| §1 | Commission 19,500–39,000 ha | 19,504–39,005 (paper 8 audit) | OK | – |
| §1 | Laroche: 1,220 kt; one-third EU, 13% BR, 12% CN, 8% IN; 1,200–31,000 ha | rds: 1,220; 34.5/12.7/12.3/**8.5**%; 30,979 | Minor | §3.6 gives 8.5%, which rounds to 9%. Make the two consistent or attribute the intro figures to the article text. |
| §2.1 | 35 subheadings + 3 | 35 + 3 | OK | Correct the description of 411520 |
| §2.1 | 7.6% of 2.19 million flows | 166,700 / 2,190,511 = 7.61% | OK | – |
| §2.1 | BACI/Comext medians 1.12, 1.03, 1.15 | 1.1168, 1.0296, 1.1452 | OK | Note that BACI exceeds Comext by 3–15%, which inflates EU imports |
| §2.1 | no official FAOSTAT production flags; almost all imputed | flags I 3,732, E 40, M 75; no A | OK | – |
| §2.2 | factors | see §2 | OK | Say that min/max differ only for articles |
| §3.1 | ≈14% of 9.22 Mt "(Table 1)" | 0.1442; 9,224 kt | OK | Table 1 holds neither 9.22 Mt nor the origin shares; cite Table 3 or "results" |
| §3.1 | EU 22.8, IN 13.5, BR 11.8, CN 11.1, US 8.4% | 22.78/13.46/11.83/11.11/8.38 | OK | – |
| §3.1 | direct 0.82 Mt H&L, 1.15 Mt articles | 816; 1,148 kt | OK | – |
| §3.1 | 1.50 Mt (2005–09), 1.23 Mt (2021–23) | 1,503; 1,233 kt | OK | – |
| §3.2 | 17,581; 20,950; 0.84; pooled 19,428; all direct 26,087 | same | OK | – |
| §3.2 | +492, +11,149 ("more than half"), +248, −15,259 | same; 11,149/20,950 = 0.53 | OK | – |
| §3.2 | exports 5,924 / 6,877 / 2,335 / 123 | same (sum 15,259) | OK | – |
| §3.2 | 1.30 Mt exported, 158 kt BR+PY | 1,297 kt; 158.4 kt | OK | – |
| §3.2 | ratio 0.73–0.94, no trend | 0.733–0.938; slope 0.00016/yr | OK | – |
| §3.2 | 26,521 (2005), 30,352 (2006), 12,104 (2023); 13,553 vs 15,649 (2021–23) | same | OK | – |
| §3.3 | Commission factors 37,727, "close to 39,005"; UNIDO 44,270; Laroche 20,950 | same | OK, but | Not like for like: with DeDuCE v2.0 (the companion paper's data) the same calculation gives 43,008, and paper 8 gave 42,216. Add this. |
| §3.3 | traced "moved much less, from 17,490 to 30,907 … because tracing cannot assign more hides … than reported" | range correct | **Misleading** | 30,907 is a top-up run, in which tracing *does* add hides. Clip-only range is 17,490–20,288 (+16%) vs exporter 20,950–44,270 (×2.1). Restate. |
| §3.3 | ratio 0.44–0.93 over ten combinations | OK | OK | – |
| §3.3 / Table 2 | gaps: Commission 11.1/20.3%; UNIDO 21.6/21.7%; Laroche 0.5/0.5%; articles 3.8–7.5% | same | OK | Stage-1 gap (2.2%, 38 kt: Canada, Iraq, Norway) is not reported; add one sentence |
| §3.3 | largest gaps: BR, US, NZ (tanned); BR (finished); VN, KH, BD (articles) | gap_top_countries.json agrees | OK | – |
| §3.4 | BR 72.3, PY 8.5, IN 4.1, BO 3.2%; exporter BR 76.6, PY 11.8% | 72.28/8.49/4.10/3.16; 76.61/11.80 | OK | – |
| §3.4 | IN/CN 179 and 148 kt vs 40 and 2 | 179.1/147.8 vs 39.7/1.8 | OK | – |
| §3.4 | 41%; 6,649 as articles; BR+PY 42% | 0.4117; 6,649; 0.4241 | OK | – |
| §3.4 + Fig 3B | China **32%**, VN 17, UK 9, IN 7, Indonesia **6%** | exact: China 31.48%, Indonesia 5.48% | **WRONG (double rounding)** | China 31%, Indonesia 5%. figures.py uses JSON values rounded to 3 dp (0.315, 0.055), and `.0f` then rounds them up. Use unrounded shares. |
| §3.4 | indirect 38–46% every year | 0.382–0.462 | OK | – |
| §3.5 | 8,790–35,424; econ 15,705; econ 41,175 (05–09) and 8,840 (21–23) | same | OK | – |
| §3.5 / Table 4 | China ½: +4%, China 0: +9%, 4114/4115: −7%, 0.75 bovine: −4%, top-up: +8%, v2.0 18,731 (+7%) | +4.3/+8.7/−7.0/−3.7/+7.8/+6.5% | OK | – |
| §3.6 | 1,381 vs 1,220 kt; 39,302 vs 30,979 ha; shares 34.5/12.7/12.3/8.5 | same | OK | The +27% ha gap is attributed to versions and cleaning without a test (see §5) |
| §4.1 | "about one-sixth smaller" | 1 − 0.839 = 16% | OK | – |
| §4.1 | smaller "under every factor set" | max ratio 0.933 | OK | – |
| §4.2 | "about 10% less" than pooled | pooled/stage-wise 1.105, i.e. 9.5% less | OK | – |
| §4.3 | exporter estimate "roughly doubling" (Laroche to Commission) | 37,727/20,950 = 1.80 | Overstated | Say "80% higher" (UNIDO: 2.1×) |
| §4.4 | removing China +9%; rules fourfold; factor sets under two | 4.03×; 30,907/17,490 = 1.77× | OK | – |
| §5 | ~17,600; ~13,600; two-fifths; "nearly double" | 17,581; 13,553; 0.41; 1.80 | OK | – |
| Table 1–4 | all cells | regenerated from JSON, identical | OK | – |
| Fig 1 | series, band = 10 combinations | matches JSON and CSV | OK | Panel B articles line reuses the orange of panel A's "all stages" line; use a different colour |
| Fig 2 | bridge values | match | OK | – |
| Fig 3A | caption: EU hides "not visible" | EU-hides route (75 ha) is not plotted at all | Minor | Say "omitted (75 ha a year)" |
| Graphical abstract | 21.0k, +11.1k, −15.3k, 17.6k | the terms shown add to 16.8k; the +0.5k and +0.2k terms are omitted | Misleading arithmetic | Add a "+0.7k other" tile or a footnote |

## 4. Plausibility

**EU final use of 1.33 Mt RHE (14% of world hides).** This is within range. Laroche's published level-4 figure is 1.15–1.41 Mt a year over 2012–2022, and the EU's per-capita use is ≈3.0 kg RHE against a world ≈1.2 kg. Two biases push it up, and the paper should name both:

- The stage-4 domestic use includes all EU finished-leather use, including leather in EU-made cars and furniture that are then exported (the paper does state this). Given the EU's net exports of vehicles, this overstates *consumption*.
- BACI quantities exceed Comext by 3–15% for EU imports of 4101 and 4107.

Read the figure as "use in EU manufacturing and final demand", not consumption.

**Origin shares.** The tonnage shares (EU 23%, India 13%, Brazil 12%, China 11%) are close to Laroche's. The hectare shares are dominated by Brazil (72%) because of Brazil's intensity: 1.62 ha/t at 100% allocation. **This intensity depends on FAOSTAT's imputed Brazilian hide output.**

FAOSTAT's Brazilian hide yield (flag E) is 16–18 kg/head in 2005–2012, then 20–24 kg, then 26–27 kg from 2020, with unexplained step changes. Peers report 33–37 kg/head (US, Uruguay, Argentina, China); paper 8 already noted the level break. As an illustrative check, I set Brazil's hide output to FAOSTAT slaughter × 30 kg/head (an assumption, not a sourced figure). The results:

- Stage-wise falls from 17,581 to **13,931 ha (−21%)**.
- Exporter H&L falls from 20,950 to 16,239.
- Brazil's share falls to 65%.
- The ratio stays at 0.86.

So the *ratio* conclusion holds up, but the *levels* and the Brazil share carry an unreported ±20% uncertainty from FAOSTAT imputation. Add this as a Table 4 row and a limitation. India's share is probably overstated (buffalo-only denominator, §2).

**"Commission factors are inconsistent with FAOSTAT production."** This is only partly robust; a good part of it is a FAOSTAT artefact. Brazil's 2015–2020 exports were 372 kt wet-blue, 21.5 kt crust and 60 kt finished leather. Under the Commission's factors that implies ≈1,170 kt RHE, against FAOSTAT's 786 kt. With Brazil at peer-like yields the Commission-factor gaps shrink:

| Brazil hide yield | Tanned-hide gap | Finished-leather gap |
|---|---|---|
| FAOSTAT as is | 11.1% | 20.3% |
| 28 kg/head | 7.6% | 8.0% |
| 33 kg/head | 7.3% | 2.9% |

The remainder is mostly the US and New Zealand in wet-blue. New Zealand's FAOSTAT yield of 15–16 kg reflects bobby calves; the US yield of 33–34 kg looks sound, so the US wet-blue gap looks genuine and does suggest 2.33 is high for US wet-blue.

The test is also one-sided. A low factor can never produce a gap, so Laroche's ≈0.5% does not show that their factors are right. Their wet-blue factor of 1.00, which treats wet-blue as weighing the same as salted raw hide, is physically a lower bound.

Reword the abstract, §1 ("test those factors") and §3.3 as a *joint* inconsistency between the factors and FAOSTAT's imputed output, concentrated in Brazil (where FAOSTAT's yield is anomalous) and, for wet-blue, the US. §4.3 already gives both explanations; the abstract and the results should do the same.

## 5. Overstatements and novelty relative to Laroche et al. (2024)

1. **Novelty is understated in the abstract and overstated in §4.2.** The abstract and title present tracing hides through manufacturing countries to EU use as if it were new, and never mention Laroche et al. (2024). Laroche et al. already did this for the EU, with goods, using the same Kastner method and BACI (1.22 Mt; ≈31,000 ha at 10%). Add one clause to the abstract. §4.2's "whose code, I found, already attributes goods made in third countries…" frames as a discovery what is the stated aim of their paper (its title is about derived products). Delete "I found".
2. The genuine contributions are: the stage-wise variant (≈10% lower, which the text rightly calls "modest"); the extension to 2005–2023 with DeDuCE v2.1 (Laroche's supplement covers 2012–2022); the term-by-term reconciliation with the Commission's exporter method (new and the most useful part); and the factor-set and rule grid. The "mass-balance test" has partial precedent: Laroche's code reports the share of negative flows. Say so.
3. §3.6 "the gaps reflect different BACI and DeDuCE versions and quantity cleaning": this was not tested. Moving to DeDuCE v2.0 makes the pooled 2018–20 figure larger, not smaller (≈41,300 ha at 10%), so the 27% excess is unexplained. Write "may reflect", or run the HS12 and drop-missing-q variant.
4. §3.3: "the traced figure moved much less … because tracing cannot assign more hides …" (see table above).
5. "Roughly doubling" (§4.3) should be 1.8×.
6. "Last country before the EU" / "last shipped": BACI partner attribution is largely by country of origin of the goods, not of consignment. Say "recorded exporting country". This matters for the UK's 9%.
7. §4.1/§5 "Leaving out EU exports overstates consumption": this is correct within the model, but the EU-use figure itself still includes leather in exported EU-made vehicles (see §4), so the direction of residual bias is upward.

## 6. Prioritised fix list

1. **High.** Add a Brazil hide-yield sensitivity: levels −21%, Brazil share 65%, ratio robust. Reword the "Commission factors inconsistent with FAOSTAT" claim (abstract, §1, §3.3) as a joint factor/FAOSTAT inconsistency, largely driven by FAOSTAT's anomalous imputed Brazilian yield. Note that the test cannot validate low factors.
2. **High.** Acknowledge Laroche et al. (2024) in the abstract. Remove "I found" in §4.2. Note the precedent of their negative-flow check.
3. **High.** Correct §3.3: the traced-range explanation and the clip-only range (17,490–20,288).
4. **Medium.** Fix the China 32% → 31% and Indonesia 6% → 5% double rounding in the text and Fig 3B (`figures.py` should use unrounded shares).
5. **Medium.** In §3.6, soften or test the explanation of the 13% (RHE) and 27% (ha) gaps to Laroche.
6. **Medium.** Make the graphical abstract's arithmetic add up (show "+0.7k other").
7. **Medium.** In §3.3, give the Commission-factor exporter figure with DeDuCE v2.0 (43,008 ha) next to the 39,005 comparison, consistent with paper 8 (42,216).
8. **Low.** Correct the description of 411520 (leather waste/dust), or drop it from the sensitivity. State that Laroche min/max differ only for articles. Add the India buffalo-only denominator and the fresh vs wet-salted units to the limitations. Say "§3.1 (Table 1)" refers to the wrong table. Reconcile Laroche's India share (8% vs 8.5%). Mention the stage-1 gap (2.2%). Fig 3A: EU hides "omitted". Fig 1B: use a distinct colour. Say "recorded exporting country". Change the README run time to about 4 minutes. Note or iterate the one-pass clipping residual (≤1.1 kt).
