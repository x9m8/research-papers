"""Pooled discrete-time hazard model of stance retention: logistic GEE, clusters = items (each item's chains
for all 11 models share a cluster). Outputs results/gee.json."""
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf
from scipy import stats
from common import *

d = pd.read_csv(os.path.join(RES, 'chains_long.csv'))
d['setting'] = pd.Categorical(d['setting'], ['stereotype', 'factual', 'debate'])
d['model'] = pd.Categorical(d['model'], list(MODELS))
d['pb'] = d['turn'] - 1  # pushback number 1..4
out = {'n_obs': len(d), 'n_clusters': int(d['item'].nunique()), 'n_chains': int(d.groupby(['model', 'item']).ngroups)}
fam = sm.families.Binomial(); cs = sm.cov_struct.Exchangeable()

def fit(formula):
    m = smf.gee(formula, 'item', d, family=fam, cov_struct=cs).fit()
    return m

# A: setting + model + setting-specific pushback-turn effects
mA = fit('keep ~ C(setting) + C(model) + C(setting):C(pb)')
ci = mA.conf_int()
out['A'] = {}
for term in ['C(setting)[T.factual]', 'C(setting)[T.debate]']:
    out['A'][term] = dict(logOR=mA.params[term], OR=np.exp(mA.params[term]), OR_ci=np.exp(ci.loc[term]).tolist(), p=mA.pvalues[term])
out['A']['exch_corr'] = float(mA.cov_struct.dep_params)
# turn effect test within each setting (Wald, 3 df): is retention constant across pushback turns?
names = list(mA.params.index)
for s in ['stereotype', 'factual', 'debate']:
    idx = [i for i, n in enumerate(names) if n.startswith(f'C(setting)[{s}]:C(pb)')]
    # parameterisation from patsy: C(setting)[s]:C(pb)[T.k]
    R = np.zeros((len(idx), len(names)))
    for j, i in enumerate(idx): R[j, i] = 1
    if len(idx):
        w = mA.wald_test(R, scalar=True, use_f=False)
        out['A'][f'turn_effect_{s}'] = dict(chi2=float(w.statistic), df=len(idx), p=float(w.pvalue),
                                            ORs={names[i]: float(np.exp(mA.params.iloc[i])) for i in idx})
# B: add setting x model interaction; Wald test of interaction (does the factual-normative gap differ by model?)
d2b = d[d['setting'] != 'debate'].copy(); d2b['setting'] = d2b['setting'].cat.remove_unused_categories()
mB = smf.gee('keep ~ C(setting) * C(model) + C(setting):C(pb)', 'item', d2b, family=fam, cov_struct=cs).fit()  # debate excluded: Qwen2.5-72B never lost the stance (separation)
namesB = list(mB.params.index)
idx = [i for i, n in enumerate(namesB) if 'C(setting)[T.' in n and ':C(model)[T.' in n]
R = np.zeros((len(idx), len(namesB)))
for j, i in enumerate(idx): R[j, i] = 1
w = mB.wald_test(R, scalar=True, use_f=False)
out['B_interaction_factual_vs_stereotype'] = dict(chi2=float(w.statistic), df=len(idx), p=float(w.pvalue))
# C: factual vs stereotype only, restricted to models (sensitivity: drop the debate setting)
d2 = d[d['setting'] != 'debate'].copy(); d2['setting'] = d2['setting'].cat.remove_unused_categories()
mC = smf.gee('keep ~ C(setting) + C(model) + C(setting):C(pb)', 'item', d2, family=fam, cov_struct=cs).fit()
t = 'C(setting)[T.factual]'
out['C_factual_vs_stereotype_only'] = dict(OR=float(np.exp(mC.params[t])), OR_ci=np.exp(mC.conf_int().loc[t]).tolist(), p=float(mC.pvalues[t]))
# D: independence working correlation (sensitivity)
mD = smf.gee('keep ~ C(setting) + C(model) + C(setting):C(pb)', 'item', d, family=fam, cov_struct=sm.cov_struct.Independence()).fit()
out['D_independence'] = {term: dict(OR=float(np.exp(mD.params[term])), OR_ci=np.exp(mD.conf_int().loc[term]).tolist(), p=float(mD.pvalues[term]))
                         for term in ['C(setting)[T.factual]', 'C(setting)[T.debate]']}
dump(out, 'gee.json')
print(json.dumps(out, indent=1, default=float)[:3000])
