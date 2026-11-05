"""Step 3b (Python equivalent of fetch_openalex.js, which is the version actually run): OpenAlex lookups for the citation sample.
Needs internet access and `requests`. Writes data/derived/openalex.json."""
import os, json, time, datetime
import requests
from common import *

recs = json.load(open(os.path.join(DER, 'citation_dois.json')))
dois = sorted(set(x['doi'] for x in recs))
dois = [d for d in dois if ',' not in d and '|' not in d]
out = {'works': {}, 'skipped': len(recs) - len(dois), 'failed': [], 'retrieved': datetime.datetime.utcnow().isoformat()}
for i in range(0, len(dois), 50):
    b = dois[i:i + 50]
    for t in range(5):
        try:
            j = requests.get('https://api.openalex.org/works', params={'per_page': 50, 'filter': 'doi:' + '|'.join(b),
                             'select': 'doi,publication_year,cited_by_count,counts_by_year,is_retracted'}, timeout=60).json()
            for w in j['results']:
                d = (w.get('doi') or '').lower().replace('https://doi.org/', '')
                out['works'][d] = {'cited_by_count': w['cited_by_count'], 'is_retracted': w['is_retracted'],
                                   'publication_year': w['publication_year'],
                                   'counts_by_year': {str(c['year']): c['cited_by_count'] for c in w['counts_by_year']}}
            break
        except Exception:
            time.sleep(2 * (t + 1))
    else:
        out['failed'] += b
json.dump(out, open(os.path.join(DER, 'openalex.json'), 'w'))
print(len(out['works']))
