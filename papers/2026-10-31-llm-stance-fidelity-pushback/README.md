# Kept or conceded — reproducibility package

Kalafatis, P. (2026). *Kept or conceded: Stance fidelity of language models under repeated user pushback* [Preprint]. x9m8.com.

A secondary analysis of the released, already-judged transcripts of SYCON-Bench (Hong et al., 2025). No language model was run for this study.

## Data source
- SYCON-Bench, https://github.com/JiseungHong/SYCON-Bench, commit `6356b923905ff5b05877ac7bb65e5207be00e1c2` (2 October 2025), MIT licence (copyright notice in `data/raw/SYCON-Bench/LICENSE`). Copied 21 October 2026.
- Used: `*/results/<model>/prompt{0-4}_result_all.csv` (factual and stereotype settings) and `debate_setting/results/<model>/prompt0.csv` (per-turn judge labels); `*/output/<model>/prompt{0-4}.csv` (the model responses, used to map rows to items, to detect content-filter notices and API error strings, and for the audit); `*/data/` (items, presuppositions, corrections, stereotypes, assigned stances, scripted pushbacks); the judge scripts (`evaluate_ToF.py`, `evaluate_oscillate.py`).
- `data/raw/SYCON-Bench/original_generation_scripts_55fcf1d/`: the generation scripts at historical commit `55fcf1d` (8 May 2025), the version under which the released outputs were produced. They show that each turn's prompt contained the model's own earlier answers; the later refactored `run_benchmark.py` for the ethical setting does not.
- The raw SYCON-Bench files (about 310 MB) are not included in the code archive; clone the repository at the commit above and copy the three setting folders into `data/raw/SYCON-Bench/`. SYCON-Bench items derive from CREPE (false presuppositions), StereoSet (stereotypes) and IBM debate topics; their own licences apply.

## Code (Python 3.13; pandas, NumPy, SciPy, statsmodels, matplotlib)
- `common.py` — paths, model lists, loaders; maps each model's output rows to canonical items (rows are not always in the same order); censors content-filter notices and API error strings.
- `fidelity.py` — initial stance p₁, per-turn retention r and r_t, constancy tests (likelihood ratio; beta-geometric), cluster bootstrap over items (2,000 resamples, seed 16), contrasts between settings, debate two-state chain, seed replicates → `results/fidelity.json`, `results/chains_long.csv`.
- `gee.py` — pooled discrete-time hazard model (logistic GEE, clusters = items) → `results/gee.json`.
- `extras.py` — base vs instruction-tuned, mitigation prompts, item-fragility reliability, debate change probabilities → `results/extras.json`.
- `audit_sample.py` — the frozen, stratified random sample of 100 judged responses (seed 2026), drawn with only content-filter notices censored, as on the day it was labelled; writes `results/audit_blind.md` and `results/audit_key.csv` (reproduced byte for byte). `results/audit_ai_labels.csv` holds the blind relabelling with setting, model, item and turn; `audit_score.py` merges on all of these and stops if the sample differs → `results/audit.json`, `results/audit_merged.csv`.
- `check_published.py` — API error strings in the Claude 3.7 Sonnet debate run and their effect on Turn of Flip → `results/published_check.json`.
- `data_notes.py` — pushback-script keyword shares, restated pushbacks, short refusals → `results/data_notes.json`.
- `figures.py`, `tables.py` (→ `results/tables.md`, `results/derived.json`), `graphical_abstract.py`, `style.py`.

## Run
    cd code && python3 fidelity.py && python3 gee.py && python3 extras.py && python3 audit_sample.py && python3 audit_score.py && python3 check_published.py && python3 data_notes.py && python3 figures.py && python3 tables.py && python3 graphical_abstract.py

## AI use
Analysis code, the audit relabelling and drafting were done with Claude (Anthropic, claude-opus-5-5) in October 2026 under the author's direction; the author reviewed the outputs. The audit is an AI audit, not a human one. Claude 3.7 Sonnet is one of the models analysed.
