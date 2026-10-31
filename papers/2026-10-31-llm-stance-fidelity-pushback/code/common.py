"""Shared paths, model lists and loaders for the SYCON-Bench stance-fidelity re-analysis."""
import os, json
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'data', 'raw', 'SYCON-Bench')
RES = os.path.join(ROOT, 'results'); FIG = os.path.join(ROOT, 'figures')
SETTINGS = {'factual': 'false-presuppositions-setting', 'stereotype': 'ethical-setting', 'debate': 'debate_setting'}
SET_LABEL = {'factual': 'False presupposition (factual)', 'stereotype': 'Stereotype (normative)', 'debate': 'Debate (contested policy)'}
# main models: instruction-tuned or API models present in all three settings at prompt 0
# key -> (display name, folder per setting)
MODELS = {
    'gpt-4o': ('GPT-4o', {'factual': 'gpt-4o', 'stereotype': 'gpt-4o', 'debate': 'gpt-4o'}),
    'o3-mini': ('o3-mini', {'factual': 'o3-mini', 'stereotype': 'o3-mini', 'debate': 'o3-mini'}),
    'claude-3.7': ('Claude 3.7 Sonnet', {'factual': 'claude', 'stereotype': 'claude-3-7-sonnet-20250219', 'debate': 'claude'}),
    'deepseek-v3': ('DeepSeek-V3', {'factual': 'deepseek-v3', 'stereotype': 'deepseek-chat', 'debate': 'deepseek-v3'}),
    'deepseek-r1': ('DeepSeek-R1', {'factual': 'deepseek-r1', 'stereotype': 'deepseek-reasoner', 'debate': 'deepseek-r1'}),
    'qwen-7b-it': ('Qwen2.5-7B-Instruct', {'factual': 'Qwen2.5-7B-Instruct', 'stereotype': 'Qwen2.5-7B-Instruct', 'debate': 'Qwen2.5-7B-Instruct'}),
    'qwen-14b-it': ('Qwen2.5-14B-Instruct', {'factual': 'Qwen2.5-14B-Instruct', 'stereotype': 'Qwen2.5-14B-Instruct', 'debate': 'Qwen2.5-14B-Instruct'}),
    'qwen-72b-it': ('Qwen2.5-72B-Instruct', {'factual': 'Qwen2.5-72B-Instruct', 'stereotype': 'Qwen2.5-72B-Instruct', 'debate': 'Qwen2.5-72B-Instruct'}),
    'llama-8b-it': ('Llama-3.1-8B-Instruct', {'factual': 'Llama-3.1-8B-Instruct', 'stereotype': 'Llama-3.1-8B-Instruct', 'debate': 'Meta-Llama-3.1-8B-Instruct'}),
    'llama-70b-it': ('Llama-3.3-70B-Instruct', {'factual': 'Llama-3.3-70B-Instruct', 'stereotype': 'Llama3.3-70B-Instruct', 'debate': 'Llama-3.3-70B-Instruct'}),
    'gemma-9b-it': ('Gemma-2-9B-it', {'factual': 'gemma2-9b-it', 'stereotype': 'gemma2-9b-it', 'debate': 'gemma-2-9b-it'}),
}
# base (not instruction-tuned) models: factual and stereotype settings only (no usable judged debate file)
BASE = {
    'qwen-7b': ('Qwen2.5-7B (base)', {'factual': 'Qwen2.5-7B', 'stereotype': 'Qwen2.5-7B'}),
    'qwen-14b': ('Qwen2.5-14B (base)', {'factual': 'Qwen2.5-14B', 'stereotype': 'Qwen2.5-14B'}),
    'qwen-72b': ('Qwen2.5-72B (base)', {'factual': 'Qwen2.5-72B', 'stereotype': 'Qwen2.5-72B'}),
    'llama-8b': ('Llama-3.1-8B (base)', {'factual': 'Llama-3.1-8B', 'stereotype': 'Llama-3.1-8B'}),
    'llama-70b': ('Llama-3.1-70B (base)', {'factual': 'Llama-3.1-70B', 'stereotype': 'Llama-3.1-70B'}),
    'gemma-9b': ('Gemma-2-9B (base)', {'factual': 'gemma2-9B', 'stereotype': 'gemma-2-9b'}),
}
SEEDS = {'llama-8b-it': ['Llama-3.1-8B-Instruct', 'Llama-3.1-8B-Instruct_seed307', 'Llama-3.1-8B-Instruct_seed411'],
         'qwen-14b-it': ['Qwen2.5-14B-Instruct', 'Qwen2.5-14B-Instruct_seed307', 'Qwen2.5-14B-Instruct_seed411']}
FILTER_MSG = "The response was filtered due to the prompt triggering"
TURNS = [1, 2, 3, 4, 5]

def label_path(setting, folder, prompt=0):
    d = os.path.join(RAW, SETTINGS[setting], 'results', folder)
    return os.path.join(d, f'prompt{prompt}.csv' if setting == 'debate' else f'prompt{prompt}_result_all.csv')

def response_path(setting, folder, prompt=0):
    return os.path.join(RAW, SETTINGS[setting], 'output', folder, f'prompt{prompt}.csv')

def load_labels(setting, folder, prompt=0):
    """Item x turn matrix of judge labels (1 = holds the stance, 0 = not), rows in item order."""
    d = pd.read_csv(label_path(setting, folder, prompt))
    L = d[[f'Response_{t}' for t in TURNS]].to_numpy(dtype=float)
    L[L < 0] = np.nan
    return L

def load_responses(setting, folder, prompt=0):
    d = pd.read_csv(response_path(setting, folder, prompt))
    return d

def filtered_mask(setting, folder, prompt=0):
    """True where the stored response is a content-filter placeholder or empty."""
    d = load_responses(setting, folder, prompt)
    R = d[[f'Response_{t}' for t in TURNS]].astype(str).to_numpy()
    return np.vectorize(is_placeholder)(R)

ERROR_MSG = 'ERROR: Failed to generate response'

def is_placeholder(s):
    """Content-filter notices, API error strings and empty cells are not model responses."""
    s = str(s)
    return s.strip() == '' or s == 'nan' or FILTER_MSG in s or ERROR_MSG in s or 'overloaded_error' in s

def first_loss_chain(L):
    """Convert labels to 'held through turn t' indicators (absorbing at first non-hold)."""
    H = np.zeros_like(L)
    alive = np.ones(L.shape[0], bool)
    for t in range(L.shape[1]):
        alive = alive & (L[:, t] == 1)
        H[:, t] = alive
    return H

def dump(obj, name):
    with open(os.path.join(RES, name), 'w') as f: json.dump(obj, f, indent=1, default=float)

def canonical_questions(setting):
    if setting == 'stereotype':
        return [str(x).strip() for x in pd.read_csv(os.path.join(RAW, SETTINGS[setting], 'data', 'stereoset_intra_user_queries_api_over45.csv'))['question']]
    return [x.strip() for x in open(os.path.join(RAW, SETTINGS[setting], 'data', 'questions.txt')) if x.strip()]

def item_ids(setting, folder, prompt=0):
    """Canonical item index for each row of a model's output (rows are not always in the same order)."""
    q = canonical_questions(setting); pos = {}
    for i, x in enumerate(q): pos.setdefault(x, []).append(i)
    used = {}; out = []
    for x in load_responses(setting, folder, prompt)['Question'].astype(str).str.strip():
        k = used.get(x, 0); out.append(pos[x][k] if x in pos and k < len(pos[x]) else -1); used[x] = k + 1
    return np.array(out)

def load_matrix(setting, folder, prompt=0, drop_filtered=True, filter_only=False):
    """Labels re-indexed to canonical item order; placeholder responses (and later turns) set to NaN.
    filter_only=True censors only content-filter notices (not API error strings): the rule in force when the
    audit sample was drawn, kept so that audit_sample.py reproduces the frozen sample."""
    L = load_labels(setting, folder, prompt)
    ids = item_ids(setting, folder, prompt)
    if (ids < 0).any() or len(set(ids)) != len(ids):
        raise ValueError(f'item mapping failed for {setting}/{folder}/prompt{prompt}')
    if drop_filtered:
        F = filtered_mask(setting, folder, prompt)
        if filter_only:
            R = load_responses(setting, folder, prompt)[[f'Response_{t}' for t in TURNS]].astype(str).to_numpy()
            F = np.vectorize(lambda s: s.strip() == '' or s == 'nan' or FILTER_MSG in s)(R)
        for i in range(L.shape[0]):
            fl = np.where(F[i])[0]
            if len(fl): L[i, fl[0]:] = np.nan
    n = len(canonical_questions(setting))
    M = np.full((n, 5), np.nan); M[ids] = L
    return M
