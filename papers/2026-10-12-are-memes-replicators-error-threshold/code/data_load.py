"""Load transmission-chain data into a common format.
Each chain = list of texts [seed, gen1, gen2, ...] (index = generation), plus metadata.
Sources (all open data, cloned from GitHub):
  Gistr exps 1-3   github.com/interpretation-experiment/analysis
  Meylan et al.    github.com/smeylan/telephone-analysis-public (output/all_runs.csv)
  Cornish et al.   github.com/racdale/cornish-strings (data/chain*.chain)
"""
import re, pandas as pd, numpy as np
GISTR = 'PATH/TO/interpretation-experiment/analysis'  # clone of github.com/interpretation-experiment/analysis
MEYLAN = 'PATH/TO/telephone-analysis-public/output/all_runs.csv'
CORNISH = 'PATH/TO/cornish-strings/data'

STOP = set("""a about above after again against all am an and any are as at be because been before being below between both but by can could did do does doing down during each few for from further had has have having he her here hers herself him himself his how i if in into is it its itself just me more most my myself no nor not now of off on once only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who whom why will with would you your yours yourself yourselves also may might must shall s t ll re ve d m one two new like get got make made us""".split())

def toks(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())

def content(text):
    return set(w for w in toks(text) if len(w) >= 3 and w not in STOP)

def gistr_chains(exp):
    """Return list of dicts: tree, branch, texts (seed..last). Built by walking parent links."""
    cod = pd.read_csv(f'{GISTR}/data/codings/spreadr_exp_{exp}/spam/sebastien-lerique.csv')
    st = pd.read_pickle(f'{GISTR}/notebooks/exp_{exp}/stability.pkl.bz2')
    text = dict(zip(cod['id'], cod['text']))
    spam = dict(zip(cod['id'], cod['spam']))
    st = st[st['sentence id'].isin(text)]
    chains = []
    for (tree, br), g in st.groupby(['tree id', 'branch id']):
        g = g.sort_values('depth')
        # reconstruct root text from depth-1 parent
        first = g.iloc[0]
        if first['depth'] != 1: continue
        root_id = first['parent id']
        root_txt = cod.loc[cod['id'] == first['sentence id'], 'parent_text']
        if root_txt.empty: continue
        texts = [root_txt.iloc[0]]; ids = [int(root_id)]
        ok = True; prev = first['parent id']
        for _, r in g.iterrows():
            sid = r['sentence id']
            if spam.get(sid, 0) == 1: ok = False; break
            texts.append(text[sid]); ids.append(int(sid))
        if ok and len(texts) >= 2:
            chains.append(dict(source=f'Gistr exp {exp}', tree=int(tree), chain=f'{tree}-{br}', texts=texts, ids=ids))
    return chains

def meylan_chains():
    d = pd.read_csv(MEYLAN, low_memory=False)
    chains = []
    for tid, g in d.groupby('thread_id', sort=False):
        texts = [str(x) for x in g['user_candidate_transcription'].tolist()]
        ids = [f'{tid}:{i}' for i in g['Unnamed: 0'].tolist()]
        ids[0] = 'seed:' + str(texts[0]).strip().lower()
        chains.append(dict(source='Meylan et al.', tree=str(texts[0]).strip().lower(), chain=str(tid), texts=texts, ids=ids))
    return chains

def cornish_sets():
    """Each chain: list of generations, each a list of 15 strings (seed = gen 0)."""
    out = []
    for ch in range(1, 9):
        rows = [l.rstrip('\n').split('\t') for l in open(f'{CORNISH}/chain{ch}.chain').read().strip('\n').split('\n')]
        cols = [list(c) for c in zip(*rows)]
        out.append(dict(source='Cornish et al.', chain=ch, gens=cols))
    return out
