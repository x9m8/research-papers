# NAICS 316 employer vs nonemployer dataset (Census Bureau public files)

Public domain (CC0 1.0). Source data are US Census Bureau files (works of the US government). Retrieved 2 November 2026; see `source_files.csv` for the URL, size, SHA-256 hash and Last-Modified header of each of the 41 source files.

## cbp_naics316_us_2004_2023.csv (County Business Patterns, national)
Rows: NAICS 00 (all industries), 31-33 (manufacturing; the files code it 31), and every 316 code published in the year. Legal-form-of-organisation breakdown rows (2008+ files) are not included; rows are the all-forms ("-") rows.
- year; naics (trailing "-" and "/" removed; "31" recoded 31-33; blank code recoded 00)
- empflag (employment-size-range flag, 2004-2017 files; "r" on 2014 all-industry row, meaning not found), emp_nf / qp1_nf / ap_nf (noise flags G/H/J, D = withheld; blank before 2007)
- emp (employment, pay period incl. 12 March), qp1 (first-quarter payroll, $1,000), ap (annual payroll, $1,000), est (establishments)
- n_lt5 (1-4 in 2004-2016 files, "under 5" later), n_5_9, n_10_19, n_20_49, n_50_99, n_100_249, n_250_499, n_500_999, n_1000plus: establishments by employment-size class; "N" = code in the source with no value (treated as missing).

## nonemp_naics316_us_2004_2024.csv (Nonemployer Statistics, national)
- year; naics (00 all industries, 31-33, 316, 3161, 31611, 3162, 31621, 3169, 31699); estab_f / estab (firms); rcptot_n_f / rcptot_f / rcptot (receipts, $1,000, noise flag G from 2008)
- source: "us" = national file; "sum_of_states_51_flagged_N" = 2007 values summed from the state file because the 2007 national file was rejected by the server (N states with a withheld cell; lower bound).
- Only the all-receipts-size row (rcptot_size 001) and all legal forms are kept.

## concordance_observed_codes.csv
6-digit CBP codes present in each reference-year block (the 2012 consolidation: 316211-316219 -> 316210; 316991/316993/316999 -> 316998; 316110 and 316992 unchanged). NAICS vintage by year is an assumption (2002 for 2004-2007, 2007 for 2008-2011, 2012 for 2012-2016, 2017 for 2017-2021, 2022 for 2022+).
