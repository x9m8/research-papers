# Number audit, round 2: revised manuscript

Auditor: independent second-round check, 2026-10-20. Nothing was edited and `tables.py` was not run. Checked against `results/*.json` and `*.csv` as shipped (with `summary.py` now using price averaging: roll3 0.905%, roll5 1.248%, roll5/early 0.257).

**Bottom line.** Almost all round-1 fixes were made correctly. Every number in the abstract, social summary, §2.1–2.4, §3.1–3.5, §4.1–4.3, §5, Table 2 and the captions matches the result files. The §4.2 figure of 9.3% is correct. The open items are listed below.

## Still wrong or not done

| Location | Issue | Fix |
|---|---|---|
| §4.2, para 3 | The range was widened to "roughly 5% to 8%", but the sentence still says "roughly eight times today's economic value". 4.8–8% ÷ 0.62% = 7.7–12.9× | "roughly 8 to 13 times today's economic value", or keep "about eight times" and tie it to the 4.8% US mass fraction (7.7×, §3.5) |
| §1, last sentence of para 2 | "industry sources quote 7% to 7.8% **for other methods**". The PEFCR 7%, UNIDO 7.33% and LWG 7.8% that LHCA (2026) reports are **mass** fractions, not other methods | "…and industry figures reported by LHCA (2026) put the mass fraction at 7% to 7.8%" |
| §4.3 | The output-value variant was "almost the same in 2023–2025". The late mean is 0.89% vs 0.94%, which is 5% lower (8% lower early). Only the 2025 value is nearly equal (0.61 vs 0.62) | "about 8% lower in 2002–2013 and 5% lower in 2023–2025" |
| §2.1, end of para 1 | Round-1 fix 6b was not made. "This index is available from June 2001, which sets the start of the study" still stands, although WPU0419 is WPU041 rebased (constant ratio) and WPU041 runs from 1926 | Drop the causal clause, or say why WPU041 was not used to extend the series (e.g. no pre-2015 anchors) |
| Table 2, row 6 | Still "Choice cutout **x** carcass weight". The label comes from `code/tables.py` line 17, so editing the manuscript alone would be undone the next time tables.py runs | Change to × in `tables.py` (and in the manuscript) |
| README.md line 18 | Round-1 item 12: it says tables are "also inserted into the manuscript" but does not warn that this **overwrites** manual edits to the `## Tables` section | Add an explicit warning, or have tables.py write only to `results/tables.md` |
| Fig 3A | Labels: "Roncevich et al." and "Italy mass" run past the right end of the axes (xlim 2031) and survive only through bbox_inches='tight', the same problem round 1 found in 3B. "US LCA" sits under its marker and touches the end of the blue US line at 2025. "Mekonnen & Hoekstra" is centred about 3 years right of its 2010 marker with no leader line. (Fixed since round 1: 8.1% is now plotted, ylim 8.8, and the 3B PEFCR label is inside the axes.) | Move the Roncevich and Italy-mass labels left of their markers or widen xlim. Shift "US LCA" right or up, clear of the line. Left-align the M&H label at its marker or add a leader line |

## Minor or optional

| Location | Issue | Fix |
|---|---|---|
| §3.3 | "The difference comes from live weight." In Aug 2025 the direct/model ratio is 1.093: weight (1,503 vs 1,400 lb) accounts for 1.074 and hide price (19.25 vs 18.98) for 1.014. Weight is the main cause but not the only one. Values 1,503 and 1,529 lb are correct | "comes mainly from live weight" |
| §4.2, para 2 | "I cannot say how … the 8.1% was obtained." The citation audit (Note A) found that the paper's own methods sentence applies weights 0.34/0.58/0.08 to (6.8, 8, 14)%, which gives 8.07%. So the 8.1% is reproducible from the main text, and the inconsistency is between the two weightings | e.g. "The paper's later weight vector (0.34, 0.58, 0.08) reproduces 8.1%, which suggests the weights were paired with the wrong regions" |
| §4.2, para 1 | "a factor of about five within twenty-five years" uses period means (5.2×). Annual 2002→2025 is 9.4× | Acceptable. Could say "about fivefold between period means" |
| §2.2 | The cutout series is still unnamed (Choice 1–3, 600–900 lb) | Optional |

## Check of the §4.2 Roncevich arithmetic (task 3)

Weights normalised over the three regions: 18.4 + 2.7 + 10.6 = 31.7.
(18.4 × 6.8 + 2.7 × 8 + 10.6 × 14) / 31.7 = (125.12 + 21.60 + 148.40) / 31.7 = 295.12 / 31.7 = **9.31%**. The "9.3%" is **correct**. The shares cover only 31.7% of world exports, so the sentence implicitly renormalises them. Optionally write "applying the stated export shares as relative weights". Without renormalising, the sum is 2.95%.

## Round-1 fixes confirmed as made correctly

- **Number audit:** §3.1 "five of the six"; §2.3(f), §3.3, §4.2 and Table 2 now use price averaging, and the code matches (0.91% / 1.25%; "about one-quarter" = 0.257); §3.4 "2022–2024"; §3.3 cross-checks reframed (anchors flagged as non-independent, April 2020 +81%); §4.3 −22% / +12%, anchors "three from 2025, none before 2015", PPI-tracking caveat; §2.1 report and weight classes of anchors; §2.3(b) 35–65% Choice; §2.4 3.3–4.0 m², UNIDO wording, raw vs cured basis, constant ≈2,330 (2,329.7), mass/PEFCR "by construction"; social summary; abstract "consistent with readings", "nine published figures", explicit periods; §4.1 "between 2002–2013 and 2023–2025"; §5 "heavier cattle"; Italian clause removed; "factor of 2.3" (2.26/0.97 = 2.33); unsupported herd claim removed; Fig 1 caption (6 of 9 plotted; the code excludes the three multi-month averages); Fig 3B PEFCR label.
- **Citation audit:** AMS 2019 and LHCA 2025 titles; leatherbiz 2020a in the text and dated 6 May; UNIDO 4 m² wording; "from AMS data" dropped and Peel 2019 reference corrected; "just over $18" quote replaced by paraphrase; Chinese demand described as a decade-long decline; placeholder titles replaced; Roncevich and Hinestroza middle initials added; LHCA 2026 date and author added; Mekonnen & Hoekstra, Muhammad & Griffith and FAO references completed.
