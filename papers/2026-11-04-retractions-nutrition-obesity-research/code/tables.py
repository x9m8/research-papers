"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os
from common import RES, ROOT, GROUP_LABELS
C = json.load(open(f'{RES}/comparison.json')); S = json.load(open(f'{RES}/sensitivity.json')); Z = json.load(open(f'{RES}/citations.json'))
SEL = json.load(open(f'{RES}/selection.json'))
pc = lambda v: f'{100 * v:.1f}'
R, Rb, RJ = C['primary_vs_rest'], C['primary_vs_biomed_rest'], C['journal_only_vs_rest']
U = json.load(open(f'{RES}/unmapped_reasons.json'))
order = ['misconduct', 'fabrication', 'plagiarism', 'duplication', 'paper_mill', 'peer_review', 'computer_generated', 'forged_authorship',
         'image', 'data_concerns', 'error', 'error_only', 'ethics_consent', 'authorship_dispute', 'publisher_error', 'limited_info',
         'misconduct_broad', 'referencing']
def dd(a): return f"{100 * a['diff']:+.1f} ({100 * a['diff_lo']:+.1f} to {100 * a['diff_hi']:+.1f})"
t1 = [f"**Table 1.** Reasons for retraction: nutrition and obesity research (primary definition) compared with the rest of the Retraction Watch database, for journal articles only (conference papers excluded from both sides; the main comparison), for all retractions, and against the rest of the biomedical subjects (all retractions). JA, journal articles; All, all retractions; Biomed. rest, rest of the biomedical subjects; group sizes in brackets. Data to 28 October 2026. A retraction can carry several reasons, so columns do not sum to 100. Differences are percentage points with Newcombe 95% confidence intervals. The last two rows are mapping sensitivity checks: a broader misconduct composite that adds Breach of Policy by Author, Taken from Dissertation/Thesis and Misconduct by Third Party or by Company/Institution, and the unmapped reason Concerns/Issues about Referencing/Attributions.", '',
      f"| Reason group | JA field, % ({RJ['n']}) | JA rest, % ({RJ['n_comp']:,}) | JA difference (95% CI) | All field, % ({R['n']}) | All rest, % ({R['n_comp']:,}) | All difference (95% CI) | Biomed. rest, % ({Rb['n_comp']:,}) | Difference vs all field (95% CI) |",
      '|:-------------|------:|-------:|--------:|------:|-------:|--------:|-------:|--------:|']
for g in order:
    a, b, c = R['reasons'][g], Rb['reasons'][g], RJ['reasons'][g]
    lab = GROUP_LABELS[g] if g not in ('misconduct_broad', 'referencing') else '*' + GROUP_LABELS[g] + '*'
    t1.append(f"| {lab} | {pc(c['p'])} ({c['k']}) | {pc(c['p_comp'])} | {dd(c)} | {pc(a['p'])} ({a['k']}) | {pc(a['p_comp'])} | {dd(a)} | {pc(b['p_comp'])} | {dd(b)} |")

def tt(s): return f"{s['median']:.2f} ({s['q1']:.2f}–{s['q3']:.2f})"
t2 = ["**Table 2.** Time from publication to retraction (years; median and interquartile range), by period of the retraction notice, for all retractions and for journal articles only (conference papers excluded from both sides), and by reason (all retractions), and the countries most often named in author affiliations (share of retractions with at least one author from the country). Records with an unknown article or notice date are excluded from the timing rows.", '',
      '| Row | Nutrition and obesity | n | Rest of database | n |', '|:--|--:|--:|--:|--:|']
t2.append(f"| All retractions | {tt(R['ttr'])} | {R['ttr']['n']} | {tt(R['ttr_comp'])} | {R['ttr_comp']['n']:,} |")
t2.append(f"| Journal articles only (both sides) | {tt(RJ['ttr'])} | {RJ['ttr']['n']} | {tt(RJ['ttr_comp'])} | {RJ['ttr_comp']['n']:,} |")
t2.append(f"| All retractions, against the rest of biomedical subjects | {tt(Rb['ttr'])} | {Rb['ttr']['n']} | {tt(Rb['ttr_comp'])} | {Rb['ttr_comp']['n']:,} |")
for e, lab in [('to2009', 'Retracted up to 2009'), ('2010_2019', 'Retracted 2010–2019'), ('2020_2026', 'Retracted 2020–2026')]:
    a, b = C['ttr_by_era'][e]['primary'], C['ttr_by_era'][e]['rest']
    t2.append(f"| {lab} | {tt(a)} | {a['n']} | {tt(b)} | {b['n']:,} |")
    a, b = C['by_era_journal_only'][e]['ttr'], C['by_era_journal_only'][e]['ttr_comp']
    t2.append(f"| {lab}, journal articles only | {tt(a)} | {a['n']} | {tt(b)} | {b['n']:,} |")
lab = {'fabrication': 'Fabrication, falsification or manipulation', 'duplication': 'Duplicate publication', 'plagiarism': 'Plagiarism',
       'misconduct': 'Any misconduct', 'paper_mill': 'Paper mill', 'peer_review': 'Compromised peer review or rogue editor', 'error_only': 'Error, no misconduct flag'}
for g in ['fabrication', 'duplication', 'plagiarism', 'paper_mill', 'peer_review', 'error_only']:
    a, b = C['ttr_by_reason_primary'][g], C['ttr_by_reason_rest'][g]
    t2.append(f"| {lab[g]} | {tt(a)} | {a['n']} | {tt(b)} | {b['n']:,} |")
t2.append('| *Countries (any author), %* | | | | |')
for x in C['countries_top'][:10]:
    t2.append(f"| {x['country']} | {pc(x['p'])} | {x['k']} | {pc(x['p_rest'])} | |")

t3 = ["**Table 3.** Sensitivity of the main comparisons to the definition of the field. Each definition is compared with all other retractions in the database; the last two columns repeat the misconduct and timing comparisons with conference papers excluded from both sides. In the row for the primary definition without conference papers, all columns exclude conference papers from both sides. S: Retraction Watch subject code (BLS) or (HSC) Nutrition; J: journal title names nutrition, diet, obesity, eating, appetite, vitamins or bariatric surgery (animal, plant, soil and feed journals excluded); K: article title names a nutrition, diet or obesity topic; food-science journals: title contains food, dairy or beverage. Columns (percentages unless stated): Misc., any misconduct; Mill, paper mill; Peer rev., compromised peer review or rogue editor; Error only, error with no misconduct flag; 2023+, retracted 2023 or later; China and US, at least one author from the country; Years, median years from publication to retraction; JA, journal articles only, conference papers excluded from both sides.", '',
      '| Definition | n | Misc. | Mill | Peer rev. | Error only | 2023+ | China | US | Years (rest) | JA misc. (rest) | JA years (rest) |',
      '|:------------------|------:|-----:|-----:|-----:|-----:|------:|-----:|-----:|-----:|-----:|-----:|']
REN = {'primary (S or J)': 'Primary (S or J)', 'S: subject code only': 'S: subject-code rule', 'J: journal title only': 'J: journal-title rule',
       'S and J (both)': 'S and J (both rules)', 'K: article title only': 'K: article-title rule', 'broad (S or J or K)': 'Broad (S or J or K)',
       'primary + food-science journals': 'Primary + food-science journals', 'primary, excluding conference papers': 'Primary, journal articles (both sides)',
       'primary, excluding Hindawi': 'Primary, excluding Hindawi'}
for nm in REN:
    v = S[nm]; jo = v['journal_only']
    if nm == 'primary, excluding conference papers':
        v = dict(v); v.update({k: jo[k] for k in ['misconduct', 'paper_mill', 'peer_review', 'error_only', 'recent_2023', 'china', 'us', 'ttr', 'ttr_comp']}); v['n'] = jo['n']
    tail = f" {pc(jo['misconduct']['p'])} ({pc(jo['misconduct']['p_comp'])}) | {jo['ttr']['median']:.2f} ({jo['ttr_comp']['median']:.2f}) |"
    t3.append(f"| {REN[nm]} | {v['n']} | {pc(v['misconduct']['p'])} | {pc(v['paper_mill']['p'])} | {pc(v['peer_review']['p'])} | {pc(v['error_only']['p'])} | {pc(v['recent_2023']['p'])} | {pc(v['china']['p'])} | {pc(v['us']['p'])} | {v['ttr']['median']:.2f} ({v['ttr_comp']['median']:.2f}) |" + tail)
r0 = S['primary (S or J)']
t3.append(f"| *Rest of database (primary)* | {r0['misconduct']['n_comp']:,} | {pc(r0['misconduct']['p_comp'])} | {pc(r0['paper_mill']['p_comp'])} | {pc(r0['peer_review']['p_comp'])} | {pc(r0['error_only']['p_comp'])} | {pc(r0['recent_2023']['p_comp'])} | {pc(r0['china']['p_comp'])} | {pc(r0['us']['p_comp'])} | | | |")

F, Cc = Z['field'], Z['comparison']
t4 = [f"**Table 4.** Citations after retraction, OpenAlex. Field: primary-definition retractions with a DOI retracted 2012–2023 (found in OpenAlex: {Z['n_found']['field']} of {Z['n_requested']['field']}); comparison: random sample of other biomedical retractions with a DOI, two per field record within each retraction year (found: {Z['n_found']['comparison']} of {Z['n_requested']['comparison']}). Post-retraction citations are citing works published in the calendar years after the retraction year, up to 2025. Counts are citing works indexed by OpenAlex, not readings of how the paper was cited.", '',
      '| Measure | Nutrition and obesity | Comparison | Difference or ratio (95% CI) |', '|:--|--:|--:|--:|']
d = Z['diff_any_post']; rr = Z['rate_ratio']; df = Z['diff_retracted_flag']
t4 += [f"| Cited at least once after the retraction year, % | {pc(F['any_post'])} | {pc(Cc['any_post'])} | {100 * d['diff']:+.1f} ({100 * d['lo']:+.1f} to {100 * d['hi']:+.1f}) |",
       f"| Cited 5 or more times after the retraction year, % | {pc(F['post_ge5'])} | {pc(Cc['post_ge5'])} | |",
       f"| Post-retraction citations, median per paper | {F['post_median']:.0f} | {Cc['post_median']:.0f} | |",
       f"| Post-retraction citations, mean per paper | {F['post_mean']:.1f} | {Cc['post_mean']:.1f} | |",
       f"| Post-retraction citations per year, mean | {F['rate_mean']:.2f} | {Cc['rate_mean']:.2f} | ratio {rr['ratio']:.2f} ({rr['lo']:.2f} to {rr['hi']:.2f}) |",
       f"| Post-retraction citations per year, median | {F['rate_median']:.2f} | {Cc['rate_median']:.2f} | |",
       f"| Total post-retraction citations | {F['post_sum']:,} | {Cc['post_sum']:,} | |",
       f"| Share of 2012–2025 citations after the retraction year, % (papers published 2012 or later; n = {F['n_complete']}, {Cc['n_complete']}) | {pc(F['post_share_complete'])} | {pc(Cc['post_share_complete'])} | |",
       f"| Flagged as retracted in OpenAlex, % | {pc(F['retracted_flag'])} | {pc(Cc['retracted_flag'])} | {100 * df['diff']:+.1f} ({100 * df['lo']:+.1f} to {100 * df['hi']:+.1f}) |"]
for nm, lab in [('2012_2017', 'Retracted 2012–2017'), ('2018_2023', 'Retracted 2018–2023')]:
    b = Z['by_period'][nm]
    t4.append(f"| {lab}: cited after retraction year, % (n = {b['field']['n']}, {b['comparison']['n']}) | {pc(b['field']['any_post'])} | {pc(b['comparison']['any_post'])} | |")
    t4.append(f"| {lab}: citations per year, mean | {b['field']['rate_mean']:.2f} | {b['comparison']['rate_mean']:.2f} | ratio {b['rate_ratio']['ratio']:.2f} ({b['rate_ratio']['lo']:.2f} to {b['rate_ratio']['hi']:.2f}) |")

ts = [f"**Table S1.** Retraction Watch reasons not mapped to any reason group in this analysis ({len(U['unmapped'])} of the {U['n_distinct_reasons']} distinct reasons in the retraction records), with the number of retractions citing each: nutrition and obesity (primary definition, n = {U['n_primary']}) and rest of the database (n = {U['n_rest']:,}). Reasons marked * are added to the misconduct composite in the broader mapping (Table 1, last rows). Reasons cited by fewer than 20 records in total are omitted (full list in results/unmapped_reasons.json).", '',
      '| Reason | Nutrition and obesity | Rest of database |', '|:--|--:|--:|']
for x in U['unmapped']:
    if x['k_primary'] + x['k_rest'] < 20 and not x['in_broad_misconduct']: continue
    ts.append(f"| {x['reason']}{' *' if x['in_broad_misconduct'] else ''} | {x['k_primary']} ({pc(x['k_primary'] / U['n_primary'])}%) | {x['k_rest']:,} ({pc(x['k_rest'] / U['n_rest'])}%) |")
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n\n' + '\n'.join(t4) + '\n\n' + '\n'.join(ts) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
