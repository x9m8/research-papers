# Too leaky to replicate — reproducibility package

Code and derived results for "Too leaky to replicate: an error threshold for memes in human memory".

## Raw data (not redistributed; fetch from the original repositories)
- Gistr experiments 1–3 (Lerique, 2017): https://github.com/interpretation-experiment/analysis (commit 72c3ed0), GPL-3.0
- Meylan, Nair & Griffiths (2021): https://github.com/smeylan/telephone-analysis-public (commit 46784a1)
- Cornish, Dale, Kirby & Christiansen (2017): https://github.com/racdale/cornish-strings

Edit the paths at the top of code/data_load.py to point at your clones, create a figures/ folder next to code/, and run the scripts from inside code/.

## Run order
python fidelity.py; python restoration.py; python heterogeneity.py; python theory.py; python sensitivity.py; python figures.py; python graphical_abstract.py

Python 3 with numpy, scipy, pandas, matplotlib. Bootstrap seed 20261011.
