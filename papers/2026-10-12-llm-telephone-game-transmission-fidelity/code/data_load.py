"""Load LLM transmission chains (Perez et al., 2024/2025) into the same format used in
Kalafatis (2026, "Too leaky to replicate"): each chain = dict(tree, chain, texts=[seed, gen1, ..., gen50]).

Source (open data, not redistributed): github.com/flowersteam/TelephoneGameLLM (also reachable as jeremyperez2/TelephoneGameLLM)
  Results/<model>/<task>/<seed text>/seed_<k>/output0.json
  'initial_story' is the human-written seed; 'stories' holds the 50 successive model outputs.
Tokenisation (lowercase alphanumeric runs) and the content-word definition (tokens of >= 3 alphanumeric
characters not on the stop list) are copied unchanged from paper 1 so that human and
model rates are measured identically.

Note: Results/Meta-Llama-3-8B-Instruct and Results/Meta-Llama-3-8B-Instruct_Temp0.8 are byte-identical
(checked by MD5 over all chain files); we use the _Temp0.8 copy only.
"""
import re, json, glob, os

TELEPHONE = os.environ.get('TELEPHONE_LLM', 'PATH/TO/TelephoneGameLLM')  # clone of github.com/flowersteam/TelephoneGameLLM

STOP = set("""a about above after again against all am an and any are as at be because been before being below between both but by can could did do does doing down during each few for from further had has have having he her here hers herself him himself his how i if in into is it its itself just me more most my myself no nor not now of off on once only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who whom why will with would you your yours yourself yourselves also may might must shall s t ll re ve d m one two new like get got make made us""".split())

def toks(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())

def content(text):
    return set(w for w in toks(text) if len(w) >= 3 and w not in STOP)

# Conditions analysed (directory name -> label). Order is used in tables and figures.
CONDITIONS = [
    ('gpt-3.5-turbo-0125', 'GPT-3.5 Turbo'),
    ('Meta-Llama-3-70B-Instruct', 'Llama 3 70B Instruct'),
    ('Meta-Llama-3-8B-Instruct_Temp0.8', 'Llama 3 8B Instruct'),
    ('Mixtral-8x7B-Instruct-v0.1', 'Mixtral 8x7B Instruct'),
    ('Mistral-7B-Instruct-v0.2', 'Mistral 7B Instruct'),
    ('Meta-Llama-3-70B-Base', 'Llama 3 70B Base'),
    ('Mixtral-8x7B-Base-v0.1', 'Mixtral 8x7B Base'),
]
TEMPERATURES = [(0.0, 'Meta-Llama-3-8B-Instruct_Temp0'), (0.4, 'Meta-Llama-3-8B-Instruct_Temp0.4'),
                (0.8, 'Meta-Llama-3-8B-Instruct_Temp0.8'), (1.2, 'Meta-Llama-3-8B-Instruct_Temp1.2'),
                (1.6, 'Meta-Llama-3-8B-Instruct_Temp1.6')]

def _t(x):
    return x[0] if isinstance(x, list) else x

def llm_chains(model, task='rephrase', dedupe=True):
    """Chains for one condition. With dedupe=True, a chain whose full text sequence repeats an earlier chain of the
    same seed text is dropped. This only happens at temperature 0, where decoding is deterministic and all five
    chains per seed are byte-identical (80 duplicate chains removed; 20 distinct chains remain)."""
    out, seen = [], set()
    for f in sorted(glob.glob(f'{TELEPHONE}/Results/{model}/{task}/*/seed_*/output0.json')):
        d = json.load(open(f))
        parts = f.split('/')
        texts = [d['initial_story']] + [_t(s) for s in d['stories']]
        key = (parts[-3], tuple(texts))
        if dedupe and key in seen: continue
        seen.add(key)
        out.append(dict(tree=parts[-3], chain=parts[-2], texts=texts))
    return out
