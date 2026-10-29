# Rephrasing without replicating — reproducibility package

Code and derived results for "Rephrasing without replicating: transmission fidelity in language-model telephone chains" (Kalafatis, 2026).

## Raw data (not redistributed; fetch from the original repository)
- Language-model telephone chains (Perez et al., 2025): https://github.com/jeremyperez2/TelephoneGameLLM (commit 1b43c3d4c11922e8e4308cf95d1318882ea7e1cd)

Clone it and set the environment variable `TELEPHONE_LLM` to the clone's path (or edit the path at the top of `code/data_load.py`).

## Human comparison values
`paper1_results/` holds two results files from the reproducibility package of Kalafatis (2026), "Too leaky to replicate" (https://x9m8.com/are-memes-replicators-error-threshold/). Their raw data sources are listed in that package:
- Gistr experiments 1–3: https://github.com/interpretation-experiment/analysis (commit 72c3ed0)
- Meylan, Nair & Griffiths (2021): https://github.com/smeylan/telephone-analysis-public (commit 46784a1)

## Run order (from inside `code/`)
python restoration.py; python fidelity.py; python length_effect.py; python heterogeneity.py; python compare.py; python sensitivity.py; python figures.py

Python 3 with numpy, scipy, statsmodels, matplotlib. Random seed 20261012. Outputs go to `results/` and `figures/`.

## Note on the source data
`Results/Meta-Llama-3-8B-Instruct` and `Results/Meta-Llama-3-8B-Instruct_Temp0.8` in the source repository are byte-identical; the analysis uses the `_Temp0.8` copy once.
