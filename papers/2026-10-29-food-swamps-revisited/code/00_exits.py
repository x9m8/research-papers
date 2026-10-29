"""Count OpenStreetMap highway=motorway_junction nodes per county (public substitute for the ESRI StreetMap
highway-exit counts used by the original study). Input: raw/osm/motorway_junction_qlever.tsv (all OSM nodes tagged
highway=motorway_junction west of 60W and north of 15N, from the QLever SPARQL endpoint over the OSM planet file of
21 Sep 2026; first line holds the endpoint's index statistics) and raw/geo/geojson-counties-fips.json (Census 2010
cartographic county boundaries, 1:500k, as redistributed by plotly/datasets). Output: derived/exits_osm.csv."""
import os, json
import pandas as pd, geopandas as gpd
from common import RAW, DER, RES, dump
pts = pd.read_csv(f'{RAW}/osm/motorway_junction_qlever.tsv', sep='\t', skiprows=1, dtype=str, quoting=3)
pts.columns = ['node', 'wkt', 'ref', 'name']
pts['osm_id'] = pts.node.str.extract(r'node/(\d+)').astype('int64')
xy = pts.wkt.str.extract(r'POINT\(([-\d.]+) ([-\d.]+)\)').astype(float); pts['lon'], pts['lat'] = xy[0], xy[1]
strip = lambda s: s.str.replace(r'^"(.*)"(@\w+)?$', r'\1', regex=True)
pts['ref'] = strip(pts.ref); pts['name'] = strip(pts.name)
pts = pts.drop_duplicates('osm_id')
g = gpd.read_file(f'{RAW}/geo/geojson-counties-fips.json')
g['fips'] = g['id'].astype(int)
gp = gpd.GeoDataFrame(pts, geometry=gpd.points_from_xy(pts.lon, pts.lat), crs=g.crs)
j = gpd.sjoin(gp, g[['fips', 'geometry']], how='left', predicate='within')
j = j[~j.index.duplicated()]
unassigned = int(j.fips.isna().sum())
# points just outside a generalised coastline/border: assign to the nearest county within ~2 km
if unassigned:
    miss = j[j.fips.isna()].drop(columns=['fips', 'index_right'])
    gm = gpd.sjoin_nearest(miss.to_crs(5070), g[['fips', 'geometry']].to_crs(5070), how='left', max_distance=2000)
    gm = gm[~gm.index.duplicated()]
    j.loc[gm.index, 'fips'] = gm.fips
cnt = j.dropna(subset=['fips']).groupby('fips').size().rename('exits_osm')
# distinct exit refs per county (a single interchange usually has one node per carriageway)
j['refkey'] = j['ref'].fillna('') + '|' + j['name'].fillna('')
uniq = j.dropna(subset=['fips']).query("refkey != '|'").groupby('fips').refkey.nunique().rename('exits_osm_uniqref')
out = pd.DataFrame({'fips': g.fips}).merge(cnt, on='fips', how='left').merge(uniq, on='fips', how='left').fillna(0)
out.to_csv(f'{DER}/exits_osm.csv', index=False)
dump({'nodes_total': len(pts), 'nodes_unassigned_initial': unassigned, 'nodes_unassigned_final': int(j.fips.isna().sum()),
      'counties': len(out), 'counties_zero': int((out.exits_osm == 0).sum()), 'nodes_with_ref_or_name': int((j.refkey != '|').sum())}, 'exits_meta.json')
print(out.describe())

# cross-check: node counts per state from the Overpass API (16 states and DC fetched on 22 Oct 2026 before the public
# Overpass servers became saturated) against the QLever-derived counts assigned to counties of the same state
import re
ST = {'AL': 1, 'AK': 2, 'AZ': 4, 'AR': 5, 'CA': 6, 'CT': 9, 'DE': 10, 'DC': 11, 'FL': 12, 'GA': 13, 'HI': 15, 'ID': 16, 'IN': 18, 'IA': 19, 'KS': 20, 'KY': 21, 'LA': 22}
txt = open(f'{RAW}/osm/overpass_17states_2026-10-22.txt').read(); b = re.split(r'^#state (\w\w)\n', txt, flags=re.M)[1:]
ov = {s: len([l for l in body.split('\n') if l and not l.startswith('@id')]) for s, body in zip(b[::2], b[1::2])}
ql = out.assign(st=out.fips // 1000).groupby('st').exits_osm.sum()
cmp = {s: [ov[s], int(ql.get(ST[s], 0))] for s in ov}
tot_o = sum(v[0] for v in cmp.values()); tot_q = sum(v[1] for v in cmp.values())
m = json.load(open(f'{RES}/exits_meta.json')); m['overpass_crosscheck'] = {'by_state_overpass_vs_qlever': cmp, 'total_overpass': tot_o, 'total_qlever': tot_q}
dump(m, 'exits_meta.json'); print(cmp, tot_o, tot_q)
