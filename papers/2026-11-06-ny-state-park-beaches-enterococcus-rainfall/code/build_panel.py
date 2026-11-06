# build_panel.py — builds the sample-level panel (exceedances + rainfall) and the
# daily beach-status timeline (closures/advisories) from the raw JSON pulled from
# data.ny.gov (dataset wwwd-za77) and NOAA NCEI (stations USW00094789, USW00004781).
#
# Run in a Pyodide session in a Chrome tab on data.ny.gov (see results/provenance.md
# and README.md); fetch_browser.js is the JavaScript that produced data/raw/*.json.

import json
import os
import numpy as np
import pandas as pd
from common import (RAW, DERIVED, ENTEROCOCCUS_THRESHOLD, beach_station,
                     RAIN_RELATED_REASONS)


def load_beach():
    with open(os.path.join(RAW, 'beach_water_testing_li.json')) as f:
        rows = json.load(f)
    df = pd.DataFrame(rows)
    df['date_sample_taken'] = pd.to_datetime(df['date_sample_taken']).dt.normalize()
    df['results'] = pd.to_numeric(df.get('results'), errors='coerce')
    df['category'] = pd.to_numeric(df.get('category'), errors='coerce')
    df['year'] = df['date_sample_taken'].dt.year
    df['month'] = df['date_sample_taken'].dt.month
    df['station'] = df['state_park_beach'].map(beach_station)
    return df


def load_rain(filename, station_id):
    with open(os.path.join(RAW, filename)) as f:
        rows = json.load(f)
    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['DATE']).dt.normalize()
    df['prcp_mm'] = pd.to_numeric(df['PRCP'], errors='coerce').fillna(0.0)
    df = df[['date', 'prcp_mm']].drop_duplicates('date').set_index('date').sort_index()
    df = df.reindex(pd.date_range(df.index.min(), df.index.max(), freq='D'))
    df['prcp_mm'] = df['prcp_mm'].fillna(0.0)
    df['station'] = station_id
    return df


def attach_rain(df, rain_jfk, rain_isp):
    rain = {'USW00094789': rain_jfk, 'USW00004781': rain_isp}
    out = {'rain_0': [], 'rain_lag1': [], 'rain_48h': [], 'rain_72h': []}
    for _, r in df.iterrows():
        series = rain[r['station']]['prcp_mm']
        d = r['date_sample_taken']
        r0 = series.get(d, np.nan)
        r1 = series.get(d - pd.Timedelta(days=1), np.nan)
        r2 = series.get(d - pd.Timedelta(days=2), np.nan)
        r3 = series.get(d - pd.Timedelta(days=3), np.nan)
        out['rain_0'].append(r0)
        out['rain_lag1'].append(r1)
        out['rain_48h'].append(np.nansum([r1, r2]) if pd.notna(r1) or pd.notna(r2) else np.nan)
        out['rain_72h'].append(np.nansum([r1, r2, r3]) if any(pd.notna(x) for x in (r1, r2, r3)) else np.nan)
    for k, v in out.items():
        df[k] = v
    return df


def classify_exceedance(df):
    # Only rows with a bacterial indicator and a numeric result are samples.
    has_sample = df['indicator_bacteria'].isin(['Enterococcus', 'Enterococci']) & df['results'].notna()
    exceeded = np.where(
        has_sample,
        np.where(df['results_modifier'] == '<', False,
                 df['results'] >= ENTEROCOCCUS_THRESHOLD),
        np.nan,
    )
    df = df.copy()
    df['has_sample'] = has_sample
    df['exceeded'] = exceeded
    return df


def build_status_timeline(df):
    """Forward-fills each beach station's reported Beach Status over calendar days
    between consecutive status entries, to approximate closure/advisory day counts.
    Per the OPRHP data dictionary: when a sample result is present, the reported
    status applies to the day *after* the sample date (results take ~24h); when no
    result is present (a pure status-change entry), it applies to the listed date
    itself. Forward-fill stops at the next recorded event for that beach station, so
    a long gap between samples (e.g., over winter) is bounded by the next explicit
    'Off-Season'/'Preseason'/'Open' entry actually present in the data, not assumed.
    """
    d = df.copy()
    is_result_entry = d['indicator_bacteria'].isin(['Enterococcus', 'Enterococci']) & d['results'].notna()
    d['status_date'] = d['date_sample_taken'] + pd.to_timedelta(is_result_entry.astype(int), unit='D')

    events = []
    for beach, g in d.sort_values('status_date').groupby('state_park_beach'):
        g = g.drop_duplicates('status_date', keep='last').reset_index(drop=True)
        for i in range(len(g)):
            start = g.loc[i, 'status_date']
            end = g.loc[i + 1, 'status_date'] if i + 1 < len(g) else start + pd.Timedelta(days=1)
            span = max((end - start).days, 0)
            # Cap any single span at 45 days: a season-to-season gap (e.g. the last
            # closure before 'Off-Season') should not be counted as closure days; a
            # cap this short cannot straddle an actual within-season gap larger than
            # 45 days, which the weekly sampling schedule does not otherwise produce.
            span = min(span, 45)
            events.append({
                'state_park_beach': beach,
                'waterbody': g.loc[i, 'waterbody'],
                'status_start': start,
                'status_end': start + pd.Timedelta(days=span),
                'days': span,
                'beach_status': g.loc[i, 'beach_status'],
                'status_reason': g.loc[i, 'status_reason'],
                'year': start.year,
            })
    return pd.DataFrame(events)


def main():
    beach = load_beach()
    rain_jfk = load_rain('ncei_jfk_USW00094789.json', 'USW00094789')
    rain_isp = load_rain('ncei_isp_USW00004781.json', 'USW00004781')

    beach = classify_exceedance(beach)
    beach = attach_rain(beach, rain_jfk, rain_isp)

    samples = beach[beach['has_sample']].copy()
    samples['rain_related_sample'] = False  # placeholder, not used downstream

    timeline = build_status_timeline(beach)
    timeline['rain_related'] = timeline['status_reason'].isin(RAIN_RELATED_REASONS)
    # 'Closed' beach-status events reported with reason 'Closed for end of season' or
    # 'Preseason' mark the facility as not operating (administrative/seasonal), not a
    # water-quality closure of an open beach; they are excluded from is_closure and
    # reported separately. 'Open with Advisory' events are always reason 'Exceedance'
    # in this dataset and need no such filter.
    SEASONAL_REASONS = {'Closed for end of season', 'Preseason'}
    timeline['is_seasonal_admin'] = timeline['status_reason'].isin(SEASONAL_REASONS)
    timeline['is_closure'] = (timeline['beach_status'] == 'Closed') & (~timeline['is_seasonal_admin'])
    timeline['is_advisory'] = timeline['beach_status'] == 'Open with Advisory'

    samples.to_csv(os.path.join(DERIVED, 'samples.csv'), index=False)
    timeline.to_csv(os.path.join(DERIVED, 'status_timeline.csv'), index=False)
    beach.to_csv(os.path.join(DERIVED, 'beach_all_rows.csv'), index=False)

    return {
        'n_rows': len(beach),
        'n_samples': len(samples),
        'n_timeline_events': len(timeline),
        'n_exceeded': int(samples['exceeded'].sum()),
    }


if __name__ == '__main__':
    print(main())
