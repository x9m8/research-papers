"""Shared paths and helpers."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get('P4_RAW', os.path.join(HERE, '..', 'raw'))
RES = os.path.join(HERE, '..', 'results')
FIG = os.path.join(HERE, '..', 'figures')
SNAPSHOT = os.path.join(RAW, 'safetygate_20261020.json')
def load():
    return json.load(open(SNAPSHOT))
def en(versions, field):
    """Text of `field` in the English version (fallback: first non-empty)."""
    vs = versions or []
    for v in vs:
        if (v.get('language') or {}).get('key') == 'EN' and v.get(field): return v[field]
    for v in vs:
        if v.get(field): return v[field]
    return None
