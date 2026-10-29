"""Build the letter corpus from the frozen FDA snapshot.

Input : data/raw/fda_wl_snapshot_2026-10-21.json  (index query results + article HTML of every letter)
Output: data/letters/<slug>.txt  (plain text of each letter body)
        results/corpus_index.csv (one row per unique letter URL: index metadata, matched terms, SHA-256 of text)
        results/snapshot_manifest.json
"""
import json, hashlib, re, os, html
import pandas as pd
from bs4 import BeautifulSoup
from common import RAW, RES, ROOT

SNAP = f'{RAW}/fda_wl_snapshot_2026-10-21.json'
LET = os.path.join(ROOT, 'data', 'letters'); os.makedirs(LET, exist_ok=True)
d = json.load(open(SNAP))

def cell_text(c): return BeautifulSoup(c or '', 'html.parser').get_text(' ', strip=True)

rows = {}
for term, q in d['queries'].items():
    for r in q['data']:
        href = re.search(r'href="([^"]+)"', r[2]).group(1)
        if href not in rows:
            rows[href] = dict(url='https://www.fda.gov' + href, slug=href.rstrip('/').split('/')[-1],
                              posted=cell_text(r[0]), issued=cell_text(r[1]), company=cell_text(r[2]),
                              office=cell_text(r[3]), subject=cell_text(r[4]),
                              response_letter=cell_text(r[5]), closeout_letter=cell_text(r[6]),
                              closeout_href=(re.search(r'href="([^"]+)"', r[6] or '') or [None, None])[1] if r[6] else None,
                              terms=[])
        rows[href]['terms'].append(term)

def letter_text(article_html):
    s = BeautifulSoup(article_html, 'html.parser')
    for t in s.select('script, style, nav, .lcds-metadata-list, .usa-sr-only'): t.decompose()
    txt = s.get_text('\n', strip=True)
    return re.sub(r'\n{2,}', '\n', txt)

letters = {l['href']: l for l in d['letters']}
out = []
for href, m in rows.items():
    L = letters[href]
    txt = letter_text(L['article_html'])
    open(f"{LET}/{m['slug']}.txt", 'w').write(txt)
    m.update(http_status=L['status'], fetched_utc=L['fetched'], raw_html_sha256=L['raw_sha256'], raw_html_len=L['raw_len'],
             text_sha256=hashlib.sha256(txt.encode()).hexdigest(), text_len=len(txt), terms=';'.join(m['terms']))
    out.append(m)
df = pd.DataFrame(out)
df['issued_date'] = pd.to_datetime(df['issued'], format='%m/%d/%Y')
df['posted_date'] = pd.to_datetime(df['posted'], format='%m/%d/%Y')
df = df.sort_values(['issued_date', 'company']).reset_index(drop=True)
df.to_csv(f'{RES}/corpus_index.csv', index=False)
man = dict(snapshot_file=os.path.basename(SNAP), snapshot_sha256=hashlib.sha256(open(SNAP, 'rb').read()).hexdigest(),
           source=d['pulled_from'], pull_started_utc=d['started'], pull_finished_utc=d['finished'],
           query_counts={k: v['recordsTotal'] for k, v in d['queries'].items()},
           unique_urls=len(df), unique_company_date=int(df[['company', 'issued']].drop_duplicates().shape[0]),
           letters_fetched_ok=int((df.http_status == 200).sum()))
json.dump(man, open(f'{RES}/snapshot_manifest.json', 'w'), indent=1)
print(json.dumps(man, indent=1)); print(df[['issued', 'company', 'subject']].to_string()[:200])
