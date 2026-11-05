"""Derived numbers quoted in the text (from the result files) -> results/summary.json."""
import json, math
from common import RES

D = json.load(open(f'{RES}/descriptives.json')); B = json.load(open(f'{RES}/build.json')); K = json.load(open(f'{RES}/break.json'))
E = json.load(open(f'{RES}/estimates.json'))['estimates']
pct = lambda a, b: round(100 * (b / a - 1), 2)
out = {}
for ind in ['722', '722511', '722513', '10']:
    li, ros = D[ind]['LI'], D[ind]['ROS_donors']
    out[ind] = {'emp_change_2016_2025_pct': {'LI': pct(li['2016']['emp'], li['2025']['emp']), 'ROS': pct(ros['2016']['emp'], ros['2025']['emp'])},
                'estabs_change_2016_2025_pct': {'LI': pct(li['2016']['estabs'], li['2025']['estabs']), 'ROS': pct(ros['2016']['estabs'], ros['2025']['estabs'])},
                'aww_2016': {'LI': round(li['2016']['aww'], 0), 'ROS': round(ros['2016']['aww'], 0)},
                'aww_2025': {'LI': round(li['2025']['aww'], 0), 'ROS': round(ros['2025']['aww'], 0)},
                'aww_ratio_LI_ROS': {'2016': round(li['2016']['aww'] / ros['2016']['aww'], 3), '2025': round(li['2025']['aww'] / ros['2025']['aww'], 3)},
                'emp_2016': {'LI': round(li['2016']['emp']), 'ROS': round(ros['2016']['emp'])},
                'emp_2025': {'LI': round(li['2025']['emp']), 'ROS': round(ros['2025']['emp'])},
                'estabs_2016': {'LI': round(li['2016']['estabs']), 'ROS': round(ros['2016']['estabs'])}}
    for o in ['emp', 'estabs', 'wage']:
        m = E[ind][o]['main']
        out[ind][f'{o}_windows_pct'] = {k: round(100 * (math.exp(m[k]['est']) - 1), 2) for k in ['post_2017_2019', 'y2022', 'y2023', 'post_2024_2026']}
# 2017Q1 jump in establishment counts (Q4 2016 -> Q1 2017) versus the median Q4->Q1 change in other years
for key in ['722_LI', '722_WES', '722_NYC', '722_ROS', '722_PA', '10_LI', '10_ROS']:
    other = sorted(v['estabs'] for y, v in K[key].items() if y not in ('2017', '2020', '2021'))
    oe = sorted(v['emp'] for y, v in K[key].items() if y not in ('2017', '2020', '2021'))
    med = lambda s: (s[len(s) // 2] + s[(len(s) - 1) // 2]) / 2
    out.setdefault('break_2017Q1', {})[key] = {'estabs_2017': K[key]['2017']['estabs'], 'estabs_median_other_years': round(med(other), 5),
                                                'emp_2017': K[key]['2017']['emp'], 'emp_median_other_years': round(med(oe), 5)}
# minimum-wage increase on 31 Dec 2016, in percent, by region
out['mw_increase_2017Q1_pct'] = {'NYC_large': round(100 * (11.0 / 9.0 - 1), 1), 'LI_WES': round(100 * (10.0 / 9.0 - 1), 1), 'ROS': round(100 * (9.70 / 9.0 - 1), 1), 'PA': 0.0}
sched = B['schedule_by_year_q4']
out['gap_dollars'] = {y: round(v['mw_li'] - v['mw_ros'], 2) for y, v in sched.items()}
out['gap_pct'] = {y: round(100 * (math.exp(v['gap_general']) - 1), 2) for y, v in sched.items()}
out['li_share_of_li_plus_ros_722_emp_2016_pct'] = round(100 * D['722']['LI']['2016']['emp'] / (D['722']['LI']['2016']['emp'] + D['722']['ROS_donors']['2016']['emp']), 1)
out['ros_to_li_722_emp_ratio_2016'] = round(D['722']['ROS_donors']['2016']['emp'] / D['722']['LI']['2016']['emp'], 2)
json.dump(out, open(f'{RES}/summary.json', 'w'), indent=1)
print(json.dumps(out, indent=1)[:4000])
