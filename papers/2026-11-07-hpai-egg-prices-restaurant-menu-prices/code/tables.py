"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md."""
import json, os, math
from common import *
A1 = json.load(open(f'{RES}/a1_hpai_to_prices.json')); A2 = json.load(open(f'{RES}/a2_passthrough.json'))
def pc(b): return 100 * (math.exp(10 * b) - 1)
t1 = ['**Table 1.** Data series used. All are public. Monthly, January 2005 to September 2026 unless noted; October 2025 is missing from every BLS CPI and average-price series.', '',
 '| Series | BLS or APHIS identifier | Use |', '|:--|:--|:--|',
 '| CPI-U, eggs, US city average, not seasonally adjusted | CUUR0000SEFH | Retail egg price index |',
 '| Average price, eggs, Grade A, large, per dozen, US city average | APU0000708111 | Retail egg price (dollars) |',
 '| PPI, farm products: eggs, large; and chicken eggs | WPU01710703; WPU0171 | Producer-level (wholesale) egg price index |',
 '| CPI-U, food at home | CUUR0000SAF11 | Control |', '| CPI-U, food away from home | CUUR0000SEFV | Outcome |',
 '| CPI-U, full service meals and snacks | CUUR0000SEFV01 | Outcome (from December 1997) |', '| CPI-U, limited service meals and snacks | CUUR0000SEFV02 | Outcome (from December 1997) |',
 '| CPI-U, food away from home and food at home, New York-Newark-Jersey City | CUURS12ASEFV; CUURS12ASAF11 | Regional outcome and control |',
 '| Average hourly earnings, production and nonsupervisory employees, food services and drinking places, seasonally adjusted | CES7072200008 | Wage control (through August 2026) |',
 '| Average hourly earnings, all employees, total private (sensitivity) | CES0500000003 | Alternative wage control (from March 2006) |',
 '| Confirmed HPAI detections in commercial and backyard flocks, USDA APHIS dashboard | HPAI 2022 Confirmed Detections (2,297 records, 8 February 2022 to 30 October 2026) | Birds affected in commercial table-egg layer flocks |']
L = A1['layers']; be = L['by_event']
t2 = ['**Table 2.** Commercial table-egg layers confirmed with HPAI (APHIS), February 2022 to September 2026, and the retail egg price around each wave.', '',
 '| Period | Layers confirmed (millions) | Retail average price, Grade A large, per dozen |', '|:--|--:|:--|',
 f"| 2022 (from 8 February) | {be['2022']:.1f} | ${A1['retail_levels']['2022-01']:.2f} in January 2022; peak ${A1['peaks']['avg_price_egg_wave2022']['max']:.2f} in {A1['peaks']['avg_price_egg_wave2022']['month']} |",
 f"| 2023 | {be['2023']:.1f} | |", f"| 2024 | {be['2024']:.1f} | |",
 f"| 2025 | {be['2025']:.1f} | peak ${A1['peaks']['avg_price_egg_wave2024_25']['max']:.2f} in {A1['peaks']['avg_price_egg_wave2024_25']['month']}; ${A1['retail_levels']['2025-09']:.2f} in September 2025 |",
 f"| 2026, January to September | {be['2026_to_sep']:.1f} | ${A1['retail_levels']['2026-09']:.2f} in September 2026 |",
 f"| *March to April 2022* | {be['mar_apr2022']:.1f} | |", f"| *November 2023 to January 2024* | {be['nov2023_jan2024']:.1f} | |", f"| *December 2024 to February 2025* | {be['dec2024_feb2025']:.1f} | |",
 f"| **Total, February 2022 to September 2026** | **{L['total_M']:.1f}** ({L['n_flocks']} flocks; detections in {L['months_with_detection']} of {L['months']} months; largest month {L['peak_month']}, {L['peak_M']:.1f}) | |"]
t3 = ['**Table 3.** Local projections: percent change in egg prices after 10 million commercial table-egg layers are confirmed with HPAI in a month (change from the month before detection to *h* months after, 95% confidence interval from HAC standard errors). February 2022 to September 2026; *n* = 45 to 56.', '',
 '| Months after | PPI, large eggs | Retail average price | CPI, eggs |', '|:--|--:|--:|--:|']
for h in range(0, 7):
    row = []
    for y in ['ppi_egg_large', 'avg_price_egg', 'cpi_egg']:
        r = A1['main'][y][h]; row.append(f"{pc(r['b']):.1f} ({pc(r['lo']):.1f} to {pc(r['hi']):.1f})")
    t3.append(f'| {h} | ' + ' | '.join(row) + ' |')
def cell(r, sc=10): return f"{sc*r['cum']:+.3f} ({sc*r['cum_lo']:+.3f} to {sc*r['cum_hi']:+.3f})"
t4 = ['**Table 4.** Pass-through of egg price changes to restaurant menu prices. Column 2: distributed-lag model (egg CPI lags 0 to 6, with food-at-home, wage, own-lag and month controls), January 2005 to August 2026, *n* = 245; cumulative response in percentage points of the menu-price level per 10% rise in the egg CPI (95% CI). Column 3: p-value of a joint test that all seven egg-lag coefficients are zero. Column 4: p-value of a test that the sum of three *lead* egg coefficients is zero (falsification). Column 5: the same model, simplified, on the HPAI period only (February 2022 on, *n* = 50). Column 6: reduced-form local projection, change in menu price 12 months after 10 million layers are confirmed (percentage points).', '',
 '| Outcome | Cumulative response, % points per 10% egg rise (95% CI) | Joint test, egg lags (*p*) | Egg leads (*p*) | HPAI period only | Menu price 12 months after 10M layers |', '|:--|--:|--:|--:|--:|--:|']
for y in ['cpi_fafh', 'cpi_fsr', 'cpi_lsr', 'ny_fafh']:
    m = A2['main'][y]; rf = A2['rf_lp'][y][12]
    t4.append(f"| {A2['labels']['out'][y]} | {cell(m)} | {m['joint_p']:.2f} | {A2['leads'][y]['leads_p']:.2f} | {cell(A2['hpai_period'][y])} | {100*10*rf['b']:+.2f} (p = {rf['p']:.2f}) |")
rf = A2['rf_lp']['cpi_fah'][12]
t4.append(f"| *Comparison: food at home (US)* | | | | | {100*10*rf['b']:+.2f} (p = {rf['p']:.2f}) |")
t5 = ['**Table 5.** Sensitivity of the cumulative pass-through (percentage points per 10% rise in the egg price; 95% CI), US full-service and limited-service meals.', '', '| Specification | *n* | Full-service meals | Limited-service meals |', '|:--|--:|--:|--:|']
for lab, v in A2['sens'].items():
    t5.append(f"| {lab} | {v['cpi_fsr']['n']} | {cell(v['cpi_fsr'])} | {cell(v['cpi_lsr'])} |")
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n\n' + '\n'.join(t4) + '\n\n' + '\n'.join(t5) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
