"""Step 0: download retraction_watch.csv at the commit used in the paper (needs internet and `requests`) and check its hash.
Equivalent: git clone https://gitlab.com/crossref/retraction-watch-data && git -C retraction-watch-data checkout 827665a."""
import os, hashlib, requests
from common import RAW, DATA_COMMIT
url = f'https://gitlab.com/api/v4/projects/61336882/repository/files/retraction_watch.csv/raw?ref={DATA_COMMIT}'
os.makedirs(os.path.dirname(RAW), exist_ok=True)
b = requests.get(url, timeout=600).content
open(RAW, 'wb').write(b)
h = hashlib.sha256(b).hexdigest()
print(len(b), h, 'OK' if h == '7020113802228518d52d8da3b64ed3a30c59e37e828d8377bce72a5cbad7c303' else 'HASH DIFFERS')
