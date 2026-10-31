**Table 1.** Initial stance and per-turn retention by model and setting (SYCON-Bench, default prompt). p₁: share of items on which the first answer held the stance (factual: identified the false presupposition; stereotype: challenged the stereotype; debate: aligned with the assigned stance). r: probability of still holding it after each further pushback, given that it was held so far, pooled over turns 2–5, with 95% cluster-bootstrap intervals over items (2,000 resamples). Content-filter notices and API error strings are treated as censoring. Five-turn survival is shown in Figure 1. Models are ordered by factual r.

| Model | Factual p₁ | Factual r | Stereotype p₁ | Stereotype r | Debate p₁ | Debate r |
|:--|--:|--:|--:|--:|--:|--:|
| GPT-4o | 0.64 | 0.96 (0.95–0.98) | 0.38 | 0.81 (0.75–0.86) | 0.95 | 0.99 (0.99–1.00) |
| DeepSeek-R1 | 0.70 | 0.95 (0.93–0.97) | 0.66 | 0.92 (0.89–0.94) | 0.99 | 0.99 (0.97–1.00) |
| o3-mini | 0.68 | 0.94 (0.92–0.96) | 0.58 | 0.88 (0.85–0.91) | 1.00 | 1.00 (0.99–1.00) |
| DeepSeek-V3 | 0.70 | 0.90 (0.87–0.92) | 0.54 | 0.86 (0.82–0.90) | 0.99 | 0.93 (0.90–0.96) |
| Claude 3.7 Sonnet | 0.72 | 0.89 (0.86–0.91) | 0.69 | 0.90 (0.87–0.93) | 1.00 | 0.99 (0.99–1.00) |
| Qwen2.5-72B-Instruct | 0.64 | 0.85 (0.81–0.89) | 0.47 | 0.71 (0.65–0.77) | 0.98 | 1.00 (1.00–1.00) |
| Qwen2.5-14B-Instruct | 0.64 | 0.83 (0.80–0.87) | 0.48 | 0.62 (0.54–0.69) | 0.93 | 0.87 (0.83–0.90) |
| Qwen2.5-7B-Instruct | 0.57 | 0.81 (0.76–0.85) | 0.34 | 0.56 (0.47–0.64) | 0.62 | 0.26 (0.10–0.39) |
| Llama-3.3-70B-Instruct | 0.58 | 0.78 (0.73–0.82) | 0.47 | 0.73 (0.68–0.79) | 0.99 | 0.99 (0.97–1.00) |
| Llama-3.1-8B-Instruct | 0.48 | 0.73 (0.68–0.78) | 0.36 | 0.62 (0.54–0.69) | 1.00 | 0.68 (0.58–0.76) |
| Gemma-2-9B-it | 0.64 | 0.72 (0.67–0.76) | 0.69 | 0.83 (0.79–0.86) | 0.95 | 0.80 (0.75–0.84) |
| Mean of 11 models | 0.64 | 0.85 (0.83–0.87) | 0.51 | 0.77 (0.73–0.80) | 0.95 | 0.86 (0.84–0.88) |

**Table 2.** Is per-turn retention constant? Pooled retention at each pushback turn (all 11 models; chains still holding the stance at the previous turn), the GEE Wald test of turn effects (3 df), the number of models for which a turn-specific model fits better than a constant r (likelihood-ratio test, p < 0.05), the number for which a beta-geometric model (item-to-item variation in r) fits better than a constant r (p < 0.05, boundary-corrected), and the split-half reliability of item fragility across models (Spearman–Brown corrected). Chains at risk at turns 2–5: factual 1,398, 1,234, 1,066, 850; stereotype 1,128, 892, 667, 553; debate 1,030, 887, 823, 789.

| Setting | r, turn 2 | r, turn 3 | r, turn 4 | r, turn 5 | Turn effect, χ² (p) | Turn-specific better | Beta-geometric better | Item fragility reliability |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| Factual | 0.88 | 0.86 | 0.80 | 0.93 | 69.8 (p < 0.001) | 7 of 11 | 1 of 11 | 0.77 |
| Stereotype | 0.79 | 0.75 | 0.83 | 0.92 | 32.5 (p < 0.001) | 6 of 11 | 7 of 11 | 0.72 |
| Debate | 0.86 | 0.93 | 0.96 | 0.96 | 78.3 (p < 0.001) | 4 of 11 | 4 of 10 | 0.34 |

**Table 3.** Robustness. (A) AI audit of the automated judge: a random sample of 100 judged responses (34 factual, 33 stereotype, 33 debate), relabelled blind to the judge by the Anthropic model that assisted this study, not by a human. One debate response was an API error message, not a model response, and is excluded. (B) Base versus instruction-tuned versions of six open models (mean r over the six pairs). (C) Mean r over the 11 models under SYCON-Bench's mitigation system prompts.

| | Factual | Stereotype | Debate | All |
|:--|--:|--:|--:|--:|
| *(A) Audit* | | | | |
| Responses compared | 34 | 33 | 32 | 99 |
| Agreement, % (95% CI) | 71 (54–83) | 82 (66–91) | 97 (84–99) | 83 (74–89) |
| Prevalence-adjusted κ (PABAK) | 0.41 | 0.64 | 0.94 | 0.66 |
| Cohen's κ | 0.40 | 0.51 | 0.00 | 0.50 |
| Judge holds, audit does not | 8 | 1 | 0 | 9 |
| Audit holds, judge does not | 2 | 5 | 1 | 8 |
| *(B) Base vs instruction-tuned, mean r* | | | | |
| Base models | 0.89 | 0.87 | – | |
| Instruction-tuned versions | 0.79 | 0.68 | – | |
| Pairs with base r higher | 6 of 6 | 6 of 6 | – | |
| *(C) System prompt, mean r (models with r above default)* | | | | |
| Default | 0.85 | 0.77 | – | |
| Independent thinker | 0.85 (7 of 11) | 0.77 (5 of 11) | – | |
| Third person ("Andrew") | 0.86 (8 of 11) | 0.82 (9 of 11) | – | |
| Non-sycophantic instruction | 0.87 (10 of 11) | 0.83 (11 of 11) | – | |
| Third person + non-sycophantic | 0.88 (9 of 11) | 0.86 (10 of 11) | – | |
