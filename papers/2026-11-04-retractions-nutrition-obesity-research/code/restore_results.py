"""Helper used once: rewrite compact JSON copied back from the browser as results/<name> with the same formatting as common.dump,
and print its SHA-256 so it can be compared with the hash computed in the browser."""
import sys, json
from common import dump, sha256
src, name = sys.argv[1], sys.argv[2]
p = dump(json.load(open(src)), name)
print(name, sha256(p))
