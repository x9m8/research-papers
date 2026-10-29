"""Build the planet-level master table and the per-paper validation lists.

Outputs
  results/planets.csv      one row per transiting planet ever named in the archive's Kepler, K2 or current tables:
                           current planets (pscomppars, discoverymethod == Transit) plus named planets that the archive
                           has since removed (Kepler: named KOIs absent from pscomppars; K2: k2pandc REFUTED).
  results/batches.csv      one row per (validation paper, planet) with the paper's own false-positive probability.

Definitions
  mass_at_disc   the discovery paper's solution (ps row whose bibcode equals the discovery bibcode) reports a
                 measured mass (pl_bmassprov == 'Mass').
  later_mass     a solution from a different publication reports a measured mass (RV or TTV).
  status         'listed' (in pscomppars), 'removed' (Kepler-named KOI absent from pscomppars),
                 'refuted' (k2pandc disposition REFUTED, absent from pscomppars).
"""
import numpy as np, pandas as pd, json
from common import nea, vizier, norm_k2, mission, RES

comp, ps, cum, kn, k2 = nea('comp'), nea('ps'), nea('cum'), nea('knames'), nea('k2pc')

# ---------- current transiting planets ----------
tr = comp[comp.discoverymethod == 'Transit'].copy()
tr['mission'] = tr.disc_facility.map(mission)
dr = ps.merge(tr[['pl_name', 'disc_bib']], on='pl_name')
disc_rows = dr[dr.pl_bib == dr.disc_bib]
tr['disc_row'] = tr.pl_name.isin(disc_rows.pl_name)
mad = disc_rows.groupby('pl_name').pl_bmassprov.apply(lambda s: bool((s == 'Mass').any()))
tr['mass_at_disc'] = tr.pl_name.map(mad).fillna(False).astype(bool)
later = dr[(dr.pl_bib != dr.disc_bib) & (dr.pl_bmassprov == 'Mass') & dr.pl_bib.notna()]
first_later = later.groupby('pl_name').pl_pubdate.min()
tr['later_mass'] = tr.pl_name.isin(later.pl_name)
tr['later_mass_date'] = tr.pl_name.map(first_later)
tr['status'] = 'listed'
tr['controv'] = tr.pl_controv_flag.fillna(0).astype(int)
planets = tr[['pl_name', 'hostname', 'mission', 'disc_ref', 'disc_bib', 'disc_year', 'disc_pubdate', 'pl_orbper', 'pl_rade',
              'sy_pnum', 'mass_at_disc', 'later_mass', 'later_mass_date', 'controv', 'status', 'disc_row']].copy()

# ---------- removed Kepler-named planets ----------
named = cum[cum.kepler_name.notna()].merge(kn[['koi_name', 'pl_name']], left_on='kepoi_name', right_on='koi_name', how='left')
named['arch'] = named.pl_name.fillna(named.kepler_name)
gone = named[~named.arch.isin(comp.pl_name)]
mort = vizier('J/ApJ/822/86/table6'); mort = mort[mort.Kepler != '']
mort['kepoi_name'] = mort.KOI.apply(lambda k: 'K%08.2f' % float(k))
gone = gone[gone.kepoi_name.isin(mort.kepoi_name)]   # removed planets that were validated by Morton+2016
rem = pd.DataFrame({'pl_name': gone.kepler_name.values, 'hostname': gone.kepler_name.str.rsplit(' ', n=1).str[0].values,
                    'mission': 'Kepler', 'disc_ref': 'Morton et al. 2016', 'disc_bib': '2016ApJ...822...86M', 'disc_year': 2016,
                    'disc_pubdate': '2016-05', 'pl_orbper': gone.koi_period.values, 'pl_rade': gone.koi_prad.values,
                    'sy_pnum': np.nan, 'mass_at_disc': False, 'later_mass': False, 'later_mass_date': np.nan, 'controv': 0,
                    'status': 'removed', 'disc_row': True, 'kepoi_name': gone.kepoi_name.values})

# ---------- refuted K2 planets ----------
ref = k2[(k2.disposition == 'REFUTED') & (k2.default_flag == 1)].drop_duplicates('pl_name')
ref = ref[~ref.pl_name.isin(comp.pl_name)]
k2rows = pd.DataFrame({'pl_name': ref.pl_name.values, 'hostname': ref.pl_name.str.rsplit(' ', n=1).str[0].values, 'mission': 'K2',
                       'disc_ref': ref.disc_ref.values, 'disc_bib': ref.disc_bib.values, 'disc_year': np.nan, 'disc_pubdate': np.nan,
                       'pl_orbper': np.nan, 'pl_rade': np.nan, 'sy_pnum': np.nan, 'mass_at_disc': False, 'later_mass': False,
                       'later_mass_date': np.nan, 'controv': 0, 'status': 'refuted', 'disc_row': True,
                       'refuted_by': ref.disp_ref.values})
planets = pd.concat([planets, rem, k2rows], ignore_index=True)
planets['validated_class'] = planets.disc_row & ~planets.mass_at_disc.astype(bool)

# ---------- per-paper validation lists with each paper's own FPP ----------
B = []
def add(paper, bib, df, name_col, fpp_col, is_val):
    for _, r in df.iterrows():
        if not is_val(r): continue
        B.append(dict(paper=paper, bib=bib, pl_name=r[name_col], fpp=pd.to_numeric(str(r[fpp_col]).replace('<', ''), errors='coerce'),
                      fpp_upper=str(r.get('l_FPP', '')).strip() == '<'))
mort['pl_name'] = 'Kepler-' + mort.Kepler.str.replace(r'([a-z])$', r' \1', regex=True)
add('Morton et al. 2016', '2016ApJ...822...86M', mort, 'pl_name', 'FPP', lambda r: True)
c16 = vizier('J/ApJS/226/7/table8')
# VizieR lists EPIC 206209135.04 as 'K2-7de' (a typo); that EPIC candidate is K2-72 e in the archive (k2pandc)
c16.loc[c16.EPIC == '206209135.04', 'Kepler'] = 'K2-72 e'
c16['pl_name'] = c16.Kepler.map(norm_k2)
add('Crossfield et al. 2016', '2016ApJS..226....7C', c16, 'pl_name', 'FPP', lambda r: r.Disp == 'Planet' and isinstance(r.pl_name, str))
m18 = vizier('J/AJ/155/136/Planets'); m18['pl_name'] = m18.K2.map(norm_k2)
add('Mayo et al. 2018', '2018AJ....155..136M', m18, 'pl_name', 'FPP', lambda r: r.Disp == 'Planet' and isinstance(r.pl_name, str))
l18a = vizier('J/AJ/156/78/table5'); l18a['pl_name'] = l18a.Name.map(norm_k2)
add('Livingston et al. 2018a', '2018AJ....156...78L', l18a, 'pl_name', 'FPP', lambda r: r.Disp == 'VP' and isinstance(r.pl_name, str))
l18b = vizier('J/AJ/156/277/table23'); l18b['pl_name'] = l18b.Name.map(norm_k2)
add('Livingston et al. 2018b', '2018AJ....156..277L', l18b, 'pl_name', 'FPP2', lambda r: r.Disp == 'VP' and isinstance(r.pl_name, str))
m15 = vizier('J/ApJ/809/25/table5'); m15['pl_name'] = m15.Other.map(norm_k2)
add('Montet et al. 2015', '2015ApJ...809...25M', m15, 'pl_name', 'FPP', lambda r: r.Disp == 'Planet' and isinstance(r.pl_name, str))
batches = pd.DataFrame(B)
batches = batches[batches.pl_name.notna()].copy()
k2n = nea('k2names').set_index('k2_name').pl_name.to_dict()          # K2 designation -> archive name (e.g. K2-96 b -> HD 3167 b)
batches['k2_name'] = batches.pl_name
batches['pl_name'] = batches.pl_name.map(lambda n: k2n.get(n, n))
st = planets.set_index('pl_name').status
batches['status'] = batches.pl_name.map(st)
batches['later_mass'] = batches.pl_name.map(planets.set_index('pl_name').later_mass)

planets.to_csv(f'{RES}/planets.csv', index=False)
batches.to_csv(f'{RES}/batches.csv', index=False)
summary = dict(n_current_transit=int((planets.status == 'listed').sum()), n_removed_kepler=int((planets.status == 'removed').sum()),
               n_refuted_k2=int((planets.status == 'refuted').sum()), unmatched_batch_rows=int(batches.status.isna().sum()),
               batch_counts=batches.groupby('paper').size().to_dict())
json.dump(summary, open(f'{RES}/build_summary.json', 'w'), indent=1)
print(json.dumps(summary, indent=1))
print(batches[batches.status.isna()].groupby('paper').pl_name.apply(lambda s: list(s)[:12]).to_dict())
