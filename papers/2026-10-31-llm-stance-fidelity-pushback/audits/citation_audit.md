# Paper 16 citation audit

**Manuscript audited:** /home/claude/p16/pkg/manuscript/manuscript.md ("Kept or conceded: stance fidelity of language models under repeated user pushback"). It was not edited.
**Auditor:** independent citation-audit agent (Claude), 2026-10-22.
**Access:** Crossref, arXiv, OpenAlex, ACL Anthology, ICLR, NeurIPS and x9m8.com were reached through WebFetch. These hosts are blocked from the sandbox shell (proxy 403). WebFetch passes pages through a summariser, so short quotations are capped at about 125 characters. One Chrome tab was opened to try JSTOR. JSTOR returned no readable content, and the tab was closed. No other tab was touched.
**Labels for what I read:** FT = full-text HTML read through the summariser with targeted questions; ABS = arXiv abstract page; META = bibliographic record only; CODE = local SYCON-Bench repository files.

---

## 1. Claims table

| # | Location | Claim in manuscript | Source checked (what I read) | Verdict |
|---|---|---|---|---|
| 1 | §1 | Larger models repeat a user's stated view more often (Perez et al., 2023) | arXiv 2212.09251 abstract (ABS): "Larger LMs repeat back a dialog user's preferred answer ("sycophancy")". ACL Anthology record (META) | Supported |
| 2 | §1 | Asked "Are you sure?", assistants retract correct answers they had just given (Sharma et al., 2023) | arXiv 2310.13548 abstract (ABS). Brief's full-text notes (§3.2: models change an initially correct answer 32% for GPT-4 to 86% for Claude 1.3) | Supported. The abstract alone does not give the "are you sure" detail; it rests on the brief's full-text reading of §3.2 |
| 3 | §1 | Across 10 models and 7 tasks, a single challenge changed the answer 46% of the time on average (Laban et al., 2023) | arXiv 2311.08596 abstract (ABS): 10 LLMs, 7 tasks, flips 46% on average, 17% accuracy drop | Supported |
| 4 | §1 | SYCON-Bench pressed 17 models for five turns and reported the turn of first flip (Hong et al., 2025) | arXiv 2505.23840v4 HTML (FT): "we evaluate 17 LLMs spanning 6 model families"; Turn of Flip metric; Table 2 | Supported |
| 5 | §1, §4.3 | SPINE pressed models for up to 25 turns with an adaptive simulated user, and collapse kept rising with length (Tang et al., 2026) | arXiv 2609.09090v2 abstract and HTML (FT): adaptive proxy that "dynamically selects from a broad taxonomy of pressure tactics". Collapse rises from 0–57% at 5 turns to 20–97% at 25 turns | Supported in §1 |
| 5b | §4.3 | "if later pushbacks are stronger, as with SPINE's adaptive user (Tang et al., 2026)" | Same source. The proxy varies its tactics but has **no escalation schedule or intensity ramp** | **Overstated.** SPINE does not report that later pushbacks are stronger. Rephrase (see fix list) |
| 6 | §1 | Seo et al. (2026): confidence, "attribution to a person" and shared framing mattered most | arXiv 2610.18159v1 HTML (FT): "Confidence, external source, and unity are the most influential framing dimensions." Sources include a friend, an expert, an article and an AI, and attribution to another AI moved models least. Single-turn, factual only | **Partly supported.** The dimension is attribution to an *external source*, not specifically to a person. Unity ("we think") was the strongest driver |
| 7 | §1 | De Marez et al. (2026) separated initial preference for the truth from sensitivity to pressure across 56 open-weight models | arXiv 2606.06306v1 HTML (FT): "truth margin" and "manipulation sensitivity", 56 checkpoints from 0.3B to 32B. Single-turn, factual only | Supported |
| 8 | §1, §4.4 | Shapira et al. (2026): deference to users is one case of in-context updating, since models also update on claims attributed to third parties; sycophancy is excessive in-context updating | arXiv 2610.28325 abstract (ABS): models "revise their answers in response to information attributed to external sources as well"; updating "gives a user's assertion excessive weight relative to its evidence". Factual only. The HTML full text was rate-limited twice and could not be read | Supported at abstract level |
| 9 | §1, §4.4 | Ben Natan & Tsur (2026): four large models favoured the answer presented last; recency bias and sycophancy reinforced each other | arXiv 2601.15436v2 abstract and HTML (FT): "all models are biased toward the answer proposed last"; "constructive interference". In Experiment 2, Claude and ChatGPT showed no significant order effect, and one GPT pair in Experiment 3 was not significant. Single-turn | Supported, with a nuance: the recency effect is not uniform across experiments. Optional softening to "favoured, overall, the answer presented last" |
| 10 | §1 | Hong et al. reported time-to-first-flip **and flip counts for each setting** | Table 2 (FT): ToF is given for all three settings; Number of Flip (NoF) **only for debate** | **Inaccurate.** NoF is debate only |
| 11 | §2.1 | Debate items built by Hong et al. from the debate topics of Bar-Haim et al. (2019) | The paper (FT) says "632 debate topics collected from the IBM Project Debater Database", with no author or year citation. The repo file debate_setting/data/README.md (CODE) names the IBM paper "From Surrogacy to Adoption; From Bitcoin to Cryptocurrency: Debate Topic Expansion" (= Bar-Haim et al., 2019) | Supported by the repository, not by the paper. Say so in the text |
| 12 | §2.1 | "less polarised" topics | Paper (FT): Claude-3.7-Sonnet screened for "prioritizing less polarized issues". Repo README agrees | Supported |
| 13 | §2.1 | Deterministic decoding (temperature 0) where the model allowed it | Generation scripts at 55fcf1d (CODE): temperature=0.0 / do_sample=False. The paper reports no decoding temperature | Supported by code. Cite the code, not the paper |
| 14 | §2.2 | "Every reply was judged by GPT-4o at temperature 0, **as Hong et al. (2025) also state**" | Paper (FT): GPT-4o judge is stated. No sentence contains "temperature", "greedy" or "decoding". The scoring scripts (CODE) call gpt-4o with temperature=0.0 | **Partly unsupported.** The paper states the GPT-4o judge but not temperature 0 |
| 15 | §2.2, §3.6 | Hong et al. compared the judge with human annotation on 100 DeepSeek-V3 replies per setting; agreement 0.81 (factual), 0.86 (stereotype), 0.98 (debate) | Paper §4.4 and Table 5 (FT): human vs GPT-4o on 100 random DeepSeek-v3 instances per scenario. Agreement rate 0.810 / 0.864 / 0.984; Cohen's κ 0.631 / 0.690 / 0.917. Annotator number and identity are not reported | Supported (these are agreement rates, rounded correctly). Recommend also giving κ, because the manuscript reports its own κ = 0.50 |
| 16 | §2.5 Methods | Ten statistical methods cited: Allison 1982 (discrete-time hazard), Liang & Zeger 1986 (GEE), Weinberg & Gladen 1986 (beta-geometric) | Crossref records (META). The cited uses match the works' subject matter | Supported. The boundary-corrected 50:50 χ² mixture has no citation; optional: Self & Liang (1987) |
| 17 | §2.1 | CREPE (Yu et al., 2023) false presuppositions; StereoSet (Nadeem et al., 2021) stereotypes | Crossref (META). Paper §4.2 (FT) and repo agree that items come from CREPE and StereoSet | Supported |
| 18 | §3.6 | Claude 3.7 Sonnet debate mean ToF 4.47, "the value reported by Hong et al." | Table 2 (FT): Claude-3.7-Sonnet debate ToF 4.47 | Supported |
| 19 | §2.5 / §3.5 / §4.1 | Two-state chain with e, a and a/(a+e) from Kalafatis (2026b); "too short to test this as Kalafatis (2026b) did" | Live page x9m8.com/llm-telephone-game-transmission-fidelity/ (FT): per-word two-state chain, long-run share a/(a+e) (chance-adjusted variant (a−a₀)/(e+a−a₀)), predicted vs observed r = 0.98 | Supported |
| 20 | §1 | Kalafatis (2026a) estimated loss and restoration per retelling and showed memory is too leaky for selection to hold long texts word for word; exact-copy survival (1 − e)^L | Live page x9m8.com/are-memes-replicators-error-threshold/ (FT): loss e and reconstruction a per word per transmission (Table 2); (1 − e)^L for a = 0, Q(L) = exp(−μL); "replication of whole items is confined to slogans" | Supported |
| 21 | §4.1 | Kalafatis (2026a) measured word loss "at 3% to 12% per retelling" | Same page: "loses or alters between 3% and 11% of words per transmission" (Discussion); "garbles 3–11% of words" (summary). μ = 0.030–0.117; Table 2 loss e = 0.037–0.130 | **Mismatch.** The paper's own stated range is 3–11%. Use "3% to 11%" or name the quantity (μ 0.03–0.12) |
| 22 | §4.5 | Judge may favour its own outputs (Panickssery et al., 2024) | arXiv 2404.13076 abstract (ABS): LLM evaluators recognise and prefer their own generations; self-recognition is linearly correlated with self-preference | Supported. Note that this work concerns self-preference in pairwise or summary evaluation, not binary stance judging. "May" is appropriately hedged |
| 23 | Acknowledgements | Thanks "Hong, Byun, Kim, Shu and Choi" | arXiv v4 lists 5 authors including Jinho D. Choi. Crossref, ACL Anthology and the repo BibTeX list 4 (no Choi) | Fine as thanks, but it differs from the 4-author reference. Optionally footnote that arXiv v4 adds Choi |
| 24 | §2.1, §7 | SYCON-Bench MIT licence, commit 6356b92 (2 Oct 2025), generation scripts at 55fcf1d (8 May 2025) | Local SOURCE.txt (CODE) agrees | Consistent with the package (not independently re-cloned) |

**Works named in the brief but not cited in the manuscript.** I checked these records but no claims are made from them: Wei et al. 2023 (arXiv 2308.03958, v2 15 Feb 2024; Wei, Huang, Lu, Zhou & Le), SycEval (2502.08177, v4 19 Sep 2025, comment "AIES 2025"), PARROT (2511.17220, v2 1 Dec 2025; full title ends "-- A Sycophancy Robustness Benchmark for LLMs"), and ELEPHANT (2505.13995, v2 29 Sep 2025). All four IDs resolve, and titles and authors match the brief. None is cited, so nothing needs fixing.

---

## 2. Crossref and arXiv verification

| Reference | Identifier | Resolves | Title / authors / venue match reference list? |
|---|---|---|---|
| Allison 1982 | 10.2307/270718 | Yes (Crossref) | Yes. Crossref gives only first page 61 (no issue). Secondary sources disagree on the last page (Hallinan & Williams 1987 cite pp. 61–89; the usual citation is 61–98). JSTOR was unreadable. **Confirm the page range on JSTOR.** APA wants a full range |
| Bar-Haim et al. 2019 | 10.18653/v1/P19-1094 | Yes | Yes: 10 authors in correct order, pp. 977–990 |
| Ben Natan & Tsur 2026 | arXiv 2601.15436 (v2 26 Jan 2026) | Yes | Yes |
| De Marez et al. 2026 | arXiv 2606.06306 (v1 4 Jun 2026) | Yes | Yes |
| Hong et al. 2025 | 10.18653/v1/2025.findings-emnlp.121 | Yes | Yes. Crossref and ACL list 4 authors (Hong, Byun, Kim, Shu), pp. 2239–2259, November 2025. arXiv 2505.23840 v4 (26 Feb 2026) lists 5 (+ Jinho D. Choi). The reference correctly follows the published version |
| Kalafatis 2026a | x9m8.com/are-memes-replicators-error-threshold/ (post 1933, 12 Oct 2026) | Yes | Title matches the live heading. The browser/meta title differs ("Are Memes Replicators? …"); this is harmless |
| Kalafatis 2026b | x9m8.com/llm-telephone-game-transmission-fidelity/ (post 1955, 12 Oct 2026) | Yes | Title matches |
| Laban et al. 2023 | arXiv 2311.08596 (v1 14 Nov 2023, v2 21 Feb 2024) | Yes | Yes |
| Liang & Zeger 1986 | 10.1093/biomet/73.1.13 | Yes | Yes: 73(1), 13–22 |
| Nadeem et al. 2021 | 10.18653/v1/2021.acl-long.416 | Yes | Yes: pp. 5356–5371 |
| Panickssery et al. 2024 | arXiv 2404.13076 (v1 15 Apr 2024) | Yes | Yes. **Published version exists:** *Advances in Neural Information Processing Systems 37*, 68772–68802, DOI 10.52202/079017-2197 (Crossref verified) |
| Perez et al. 2023 | 10.18653/v1/2023.findings-acl.847 | Yes | Title and pages match. **63 authors.** The reference's "Heiner, S., et al." is not APA 7 |
| Seo et al. 2026 | arXiv 2610.18159 (v1 13 Oct 2026) | Yes | Yes |
| Shapira et al. 2026 | arXiv 2610.28325 (v1 20 Oct 2026) | Yes | Yes |
| Sharma et al. 2023 | arXiv 2310.13548 (v1 20 Oct 2023 … v4 10 May 2025) | Yes | Yes: 19 authors. **Published version:** ICLR 2024 (proceedings.iclr.cc, 18 authors; Newton Cheng is absent from the ICLR author list) |
| Tang et al. 2026 | arXiv 2609.09090 (v2 13 Oct 2026) | Yes | Yes: 4 authors |
| Weinberg & Gladen 1986 | 10.2307/2531205 | Yes | Yes: 42(3). Crossref gives first page only. Secondary source gives 547–560 |
| Yu et al. 2023 | 10.18653/v1/2023.acl-long.583 | Yes | Yes: pp. 10457–10480 |

No DOI or arXiv ID failed to resolve. No reference is fabricated.

---

## 3. In-text citations against the reference list

- All 19 works cited in the text appear in the reference list, and all 19 references are cited. There are no orphans in either direction.
- Kalafatis 2026a/2026b suffixes: APA 7 orders same-author, same-year works **alphabetically by title**. "Rephrasing…" precedes "Too leaky…", so strict APA would make *Rephrasing* 2026a and *Too leaky* 2026b, the reverse of the current labels. This is low priority and would mean swapping all six in-text occurrences. The series order is a defensible house choice if the journal allows it.
- arXiv version labels are inconsistent: "(arXiv:2601.15436v2)" and "(arXiv:2609.09090v2)" carry versions, while the others do not. Either give the version for all (Laban v2, Sharma v4, Hong v4 if used) or drop it.
- arXiv year: APA dates an arXiv preprint by the version consulted. Laban v2 is 2024 and Sharma v4 is 2025. Citing the published Sharma (ICLR 2024) and Panickssery (NeurIPS 2024) versions removes most of this.

---

## 4. Corrected reference entries (only entries that change)

**Perez et al.** (APA 7 rule for 21+ authors: first 19, ellipsis, last):
Perez, E., Ringer, S., Lukošiūtė, K., Nguyen, K., Chen, E., Heiner, S., Pettit, C., Olsson, C., Kundu, S., Kadavath, S., Jones, A., Chen, A., Mann, B., Israel, B., Seethor, B., McKinnon, C., Olah, C., Yan, D., Amodei, D., . . . Kaplan, J. (2023). Discovering language model behaviors with model-written evaluations. In *Findings of the Association for Computational Linguistics: ACL 2023* (pp. 13387–13434). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.findings-acl.847
(The 19th author is Daniela Amodei; the 63rd is Jared Kaplan, per the ACL Anthology.)

**Sharma et al.** (recommended: the published version; in-text becomes Sharma et al., 2024):
Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S. R., Durmus, E., Hatfield-Dodds, Z., Johnston, S. R., Kravec, S., Maxwell, T., McCandlish, S., Ndousse, K., Rausch, O., Schiefer, N., Yan, D., Zhang, M., & Perez, E. (2024). Towards understanding sycophancy in language models. In *The Twelfth International Conference on Learning Representations (ICLR 2024)*. https://proceedings.iclr.cc/paper_files/paper/2024/hash/0105f7972202c1d4fb817da9f21a9663-Abstract-Conference.html
(The ICLR proceedings page gives 18 authors. If the arXiv version is kept instead, keep the current 19-author list but date it to the version read, e.g. "(2025). … (arXiv:2310.13548v4)".)

**Panickssery et al.** (published version):
Panickssery, A., Bowman, S. R., & Feng, S. (2024). LLM evaluators recognize and favor their own generations. In *Advances in Neural Information Processing Systems 37* (pp. 68772–68802). https://doi.org/10.52202/079017-2197

**Allison** (add the full page range once confirmed on JSTOR; likely 61–98):
Allison, P. D. (1982). Discrete-time methods for the analysis of event histories. *Sociological Methodology*, *13*, 61–98. https://doi.org/10.2307/270718 **[last page to confirm]**

**Weinberg & Gladen:**
Weinberg, C. R., & Gladen, B. C. (1986). The beta-geometric distribution applied to comparative fecundability studies. *Biometrics*, *42*(3), 547–560. https://doi.org/10.2307/2531205

**Laban et al.** (version date, if version-consistent dating is adopted):
Laban, P., Murakhovs'ka, L., Xiong, C., & Wu, C.-S. (2024). *Are you sure? Challenging LLMs leads to performance drops in the FlipFlop experiment* (arXiv:2311.08596v2) [Preprint]. arXiv. https://arxiv.org/abs/2311.08596
(Optional. Keeping 2023 for v1 is also acceptable if v1 was the version read.)

**Recommended new reference** (see §5):
Kim, T. M., Luo, L., Kim, S. E., Manrai, A. K., Topol, E., & Rajpurkar, P. (2026). The doctor will agree with you now: Sycophancy of large language models in multi-turn medical conversations. In *Proceedings of the 1st Workshop on Linguistic Analysis for Health (HeaLing 2026)* (pp. 19–34). Association for Computational Linguistics. https://aclanthology.org/2026.healing-1.2.pdf
(Read through the summariser: authors, venue and pages are as reported by the PDF. DOI not checked. Confirm before use.)

All other entries (Bar-Haim, Ben Natan & Tsur, De Marez, Hong, Kalafatis a/b, Liang & Zeger, Nadeem, Seo, Shapira, Tang, Yu) are correct as written.

---

## 5. Novelty findings

**The close 2026 preprints. None estimates per-turn retention or hazards comparing factual with normative items.**
- **Seo et al. (2610.18159):** single-turn, factual QA only ("limited to single-turn factual QA"). No survival or hazard analysis.
- **De Marez et al. (2606.06306):** single-turn two-option MCQ, factual only (PlausibleQA). No per-turn analysis.
- **Shapira et al. (2610.28325):** factual sycophancy only (abstract). The full text could not be read (rate limit). Nothing in the abstract suggests a multi-turn hazard analysis.
- **SPINE (2609.09090):** multi-turn (25 turns), with false-presupposition and unethical-query banks. It reports cumulative collapse at checkpoints (CR@T), a censored mean collapse turn (CT@T) and AUSC. **There is no per-turn hazard, retention parameter or half-life**, and the two banks are compared only through checkpoint tables. This is the nearest competitor on design. Its transcripts are unreleased.
- **Ben Natan & Tsur (2601.15436):** single-turn, factual (TruthfulQA). No per-turn measure.

**Other studies found in my searches:**
- **Kim et al. (2026), HeaLing workshop, "The Doctor Will Agree With You Now":** ten models, four-turn escalating pushback adapted from SYCON-Bench. A turn-level "Resistance" R(t), described as a survival curve, with per-pushback drops. It has **no hazard model and no factual-vs-normative contrast**: both datasets are medical. **This is the closest prior use of a survival-curve framing for multi-turn sycophancy.** It should be cited, and the sentence "no one has estimated a per-turn retention parameter from these or similar data" should be softened to acknowledge it.
- **Bogdanov et al. (arXiv 2609.29508):** Kaplan–Meier curves and discrete-time hazard regression for LLM agents. The event is claiming a reward early in a delay task, not a stance under user pushback. This is a methodological precedent only; citation is optional.
- **Li et al. (2025), "Firm or Fickle?" (Findings ACL 2025, pp. 6679–6700):** eight-round follow-ups and an "average first sway round". Factual MCQ only, with contested "Moral Disputes" items deliberately removed. No hazard model.
- **Liu et al. (2025), "Truth Decay" (arXiv 2503.11656):** multi-turn sycophancy benchmark. The abstract mentions no per-turn retention or hazard and no factual-vs-normative contrast. Only the abstract was read.
- **MedPRESS (arXiv 2608.02520):** five-turn medical pressure benchmark. Nothing in the abstract on hazard or retention, or on factual vs normative. Only the abstract was read.
- **Wang & Koch (arXiv 2607.21558):** moral judgment revision (distance, source, coalition). The abstract shows no multi-turn hazard analysis and no factual contrast. Only the abstract was read.
- A search for re-analyses of SYCON-Bench found none.

**Conclusion:** the paper's claimed contribution holds. I found no study that estimates a per-turn retention or hazard parameter and compares factual, normative and debate items under one protocol, or that tests constancy of retention (turn-specific and beta-geometric). The novelty sentence in §1 should (a) cite Kim et al. (2026) as a prior survival-curve (R(t)) treatment of multi-turn sycophancy on medical items, and (b) say "from SYCON-Bench or similar multi-setting data" rather than implying that no per-turn measure exists anywhere. Caveat: the search was web-based and covered abstracts for several items. Preprints posted after 22 Oct 2026 are not covered.

---

## 6. Prioritised fix list

**High**
1. **§2.2:** "as Hong et al. (2025) also state". The paper names GPT-4o as judge but gives no temperature. Rewrite as: "Every reply was judged by GPT-4o (Hong et al., 2025); the scoring scripts call it at temperature 0."
2. **§1, §3:** "Hong et al. (2025) reported time-to-first-flip and flip counts for each setting." Number of Flip is reported for debate only. Rewrite as: "reported the turn of first flip for each setting and, for debate, the number of flips."
3. **§4.1:** "3% to 12% per retelling". Kalafatis (2026a) states 3–11%. Change to "3% to 11%".
4. **§4.3:** "if later pushbacks are stronger, as with SPINE's adaptive user". SPINE has no escalation schedule. Suggested: "if later pushbacks are stronger, as they may be when an adaptive simulated user chooses its tactics (Tang et al., 2026), it will understate them."
5. **§1 novelty sentence:** cite Kim et al. (2026, HeaLing), whose turn-level Resistance R(t) is a survival curve under four-turn pushback on medical items. Narrow the claim to a per-turn retention or hazard parameter compared across factual, normative and debate claims.
6. **Perez et al. reference:** replace "Heiner, S., et al." with the APA 7 form (19 authors, ellipsis, Kaplan, J.), as in §4.

**Medium**
7. **§1:** Seo et al. "its attribution to a person" should read "its attribution to an outside source". Optionally note that shared ("we think") framing was the strongest driver.
8. **§2.1:** say that the Bar-Haim et al. (2019) source is named in the SYCON-Bench repository's debate data README. The paper itself cites only the "IBM Project Debater Database".
9. **Sharma et al.:** cite the ICLR 2024 version (in-text 2024), or date the arXiv entry to the version read.
10. **Panickssery et al.:** cite the NeurIPS 2024 version (DOI 10.52202/079017-2197).
11. **§2.2 / §3.6:** add Hong et al.'s Cohen's κ (0.63 factual, 0.69 stereotype, 0.92 debate) next to the agreement rates, so they compare directly with the audit's κ = 0.50.
12. **Allison (1982):** add the last page. Crossref gives only p. 61, and secondary sources conflict (61–89 vs 61–98). Confirm on JSTOR. **Weinberg & Gladen:** add the last page, 560.

**Low**
13. Make arXiv version labels consistent (all or none).
14. APA ordering of Kalafatis 2026a/b is by title: *Rephrasing* would be "a". Swap the suffixes, or keep the series order with editor approval.
15. **§1:** optionally soften Ben Natan & Tsur to "favoured, overall, the answer presented last". Not every model or experiment showed a significant order effect.
16. **Acknowledgements:** optionally note that Choi is a co-author on arXiv v4 only.
17. Optionally cite Self & Liang (1987) for the 50:50 χ²₀/χ²₁ boundary mixture.

**Not verified in this audit**
- The full text of Shapira et al. (rate-limited; abstract only).
- The full texts of Truth Decay, MedPRESS and Wang & Koch (abstracts only).
- The last page of Allison (1982).
