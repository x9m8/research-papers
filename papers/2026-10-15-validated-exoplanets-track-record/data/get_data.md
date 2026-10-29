# Data retrieval

Snapshot: NASA Exoplanet Archive TAP service (https://exoplanetarchive.ipac.caltech.edu/TAP/sync), 15 October 2026, CSV format; VizieR ASU-TSV (https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=<table>&-out.all&-out.max=unlimited), same date.

The exact query strings were not preserved in the working log. The statements below are reconstructed from the column header of each saved file, which records exactly what was returned. Row counts are given so a re-run can be checked. The raw files themselves are in `raw/`, and the analysis reads only those files. The Kepler archive tables q1_q6 to q1_q17_dr25_sup were retrieved but are not used, because their disposition columns are synced to current status and do not preserve history.

| File | Rows | ADQL |
|---|---:|---|
| raw/comp.csv | 6,445 | `select pl_name, hostname, disc_refname, disc_pubdate, disc_year, discoverymethod, disc_facility, pl_controv_flag, pl_orbper, pl_rade, pl_bmasse, pl_bmassprov, sy_snum, sy_pnum, st_teff, sy_kepmag, sy_tmag from pscomppars` |
| raw/ps.csv | 40,336 | `select pl_name, pl_refname, pl_pubdate, soltype, default_flag, pl_bmassprov, pl_bmasse, pl_bmasseerr1, pl_controv_flag, discoverymethod from ps` |
| raw/cum.csv | 9,564 | `select kepoi_name, kepler_name, koi_disposition, koi_pdisposition, koi_score, koi_disp_prov, koi_vet_date, koi_period, koi_prad, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec from cumulative` |
| raw/q6.csv | 2,935 | `select kepoi_name, kepler_name, koi_disposition, koi_pdisposition, koi_score, koi_disp_prov, koi_vet_date, koi_period, koi_prad, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec from q1_q6_koi` |
| raw/q8.csv | 3,865 | `select kepoi_name, kepler_name, koi_disposition, koi_pdisposition, koi_score, koi_disp_prov, koi_vet_date, koi_period, koi_prad, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec from q1_q8_koi` |
| raw/q12.csv | 5,855 | `select kepoi_name, kepler_name, koi_disposition, koi_pdisposition, koi_score, koi_disp_prov, koi_vet_date, koi_period, koi_prad, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec from q1_q12_koi` |
| raw/q16.csv | 7,348 | `select kepoi_name, kepler_name, koi_disposition, koi_pdisposition, koi_score, koi_disp_prov, koi_vet_date, koi_period, koi_prad, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec from q1_q16_koi` |
| raw/dr24.csv | 7,470 | `select kepoi_name, kepler_name, koi_disposition, koi_pdisposition, koi_score, koi_disp_prov, koi_vet_date, koi_period, koi_prad, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec from q1_q17_dr24_koi` |
| raw/dr25.csv | 8,054 | `select kepoi_name, kepler_name, koi_disposition, koi_pdisposition, koi_score, koi_disp_prov, koi_vet_date, koi_period, koi_prad, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec from q1_q17_dr25_koi` |
| raw/dr25sup.csv | 9,564 | `select kepoi_name, kepler_name, koi_disposition, koi_pdisposition, koi_score, koi_disp_prov, koi_vet_date, koi_period, koi_prad, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec from q1_q17_dr25_sup_koi` |
| raw/knames.csv | 2,818 | `select kepid, koi_name, kepler_name, pl_name from keplernames` |
| raw/k2names.csv | 583 | `select k2_name, pl_name from k2names` |
| raw/k2pc.csv | 4,077 | `select pl_name, k2_name, epic_candname, epic_hostname, disposition, disp_refname, disc_refname, pl_refname, default_flag from k2pandc` |
| raw/toi.csv | 8,148 | `select toi, tid, tfopwg_disp, toi_created, rowupdate, pl_orbper, pl_rade from toi` |
| raw/toi2.csv | 8,148 | `select toi, tid, toipfx, ctoi_alias, pl_pnum, tfopwg_disp, toi_created, rowupdate, pl_orbper, pl_rade from toi` |
| raw/cid.csv | 6,445 | `select pl_name, tic_id, hd_name, hip_name from pscomppars` |

VizieR tables (raw/vizier/):

- J/AJ/155/136_Planets
- J/AJ/156/277_table23
- J/AJ/156/78_table4
- J/AJ/156/78_table5
- J/AJ/156/78_vespa
- J/AJ/166/28_table13
- J/AJ/167/233_table4
- J/ApJS/226/7_table8
- J/ApJS/226/7_table9
- J/ApJ/784/45_table3
- J/ApJ/809/25_table3
- J/ApJ/809/25_table5
- J/ApJ/822/86_table3
- J/ApJ/822/86_table6
