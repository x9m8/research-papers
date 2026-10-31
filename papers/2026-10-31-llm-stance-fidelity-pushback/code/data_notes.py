"""Descriptive notes on the SYCON-Bench pushback scripts -> results/data_notes.json"""
from common import *
pb = pd.read_csv(os.path.join(RAW, SETTINGS['factual'], 'data', 'push_back.csv'))
q = pb['Question'].astype(str).str.strip()
cols = [f'Pushback_{i}' for i in range(1, 5)]
repeat = pb[cols].apply(lambda c: c.astype(str).str.contains(r"I still don't understand why", regex=False))
out = dict(factual_items=len(pb),
           factual_items_all_pushbacks_restate_question=int(repeat.all(axis=1).sum()),
           factual_items_any_pushback_restates_question=int(repeat.any(axis=1).sum()),
           factual_share_pushbacks_restating_by_turn={c: float(repeat[c].mean()) for c in cols})
dump(out, 'data_notes.json'); print(out)
# keyword shares by turn (simple regular expressions; descriptive only)
s_pat = {'experience_or_expertise': r"friend|experience|expert|teacher|works|professor|doctor|my dad|my mom|someone who",
         'are_you_sure_or_certain': r"sure|certain", 'heard_or_read': r"heard|read"}
out['factual_pushback_keyword_share'] = {c: {k: float(pb[c].astype(str).str.contains(p, case=False).mean()) for k, p in s_pat.items()} for c in cols}
e = pd.read_csv(os.path.join(RAW, SETTINGS['stereotype'], 'data', 'stereoset_intra_user_queries_api_over45.csv'))
e_pat = {'personal_or_friend': r"personal|friend|experience|witness|met|seen", 'many_or_common': r"\bmany\b|several|common",
         'articles_reports_studies': r"article|report|stud", 'natural_or_inherent': r"natural|inherent|genetic|innate"}
out['stereotype_followup_keyword_share'] = {c: {k: float(e[c].astype(str).str.contains(p, case=False).mean()) for k, p in e_pat.items()} for c in ['question2', 'question3', 'question4', 'question5']}
dump(out, 'data_notes.json'); print(out['factual_pushback_keyword_share'], out['stereotype_followup_keyword_share'])
# short refusals stored as genuine model output (not censored), prompt 0, main models
ref = {}
for s in SETTINGS:
    for k, (n, f) in MODELS.items():
        R = load_responses(s, f[s])[[f'Response_{t}' for t in TURNS]].astype(str)
        c = int(R.apply(lambda col: col.str.strip().str.match(r"^I'?m sorry,? but I can'?t (help|assist)")).to_numpy().sum())
        if c: ref[f'{s}/{k}'] = c
out['short_refusals_prompt0'] = ref
dump(out, 'data_notes.json'); print(ref)
