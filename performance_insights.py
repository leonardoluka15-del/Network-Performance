"""Deterministic, explainable KPI analysis. No predictions or inferred root causes."""
import pandas as pd

AVAILABILITY = ['availability_2g', 'availability_3g', 'availability_4g', 'availability_5g', 'availability_volte']
ACCESSIBILITY = ['cssr_2g', 'cssr_3g', 'rrc_success_4g', 'rrc_success_5g', 'cssr_volte']
DROP = ['drop_call_rate_2g', 'dcr_volte']
MOBILITY = ['hosr_3g', 'hosr_4g', 'hosr_5g', 'hosr_volte']
DATA = ['data_2g_mb', 'data_3g_mb', 'data_4g_mb', 'data_5g_mb']
VOICE = ['tch_erlang_2g', 'erlang_3g', 'voice_traffic_volte_erlang']
PERCENTAGES = list(dict.fromkeys(AVAILABILITY + ACCESSIBILITY + DROP + MOBILITY))
POLICIES = {
    'availability': {'threshold': 99.0, 'direction': 'below', 'owner': 'RAN / Transmission',
                     'action': 'Check site power, transport reachability and radio availability counters.'},
    'drop_rate': {'threshold': 2.0, 'direction': 'above', 'owner': 'RAN Optimization',
                  'action': 'Review RF quality, interference and handover failure counters.'},
    'accessibility': {'threshold': 98.0, 'direction': 'below', 'owner': 'RAN / Capacity',
                      'action': 'Review setup failures, congestion and resource availability.'},
}


def numeric(frame, columns, percentage=False):
    """Coerce measurements; never turn missing counters into zero."""
    values = frame.reindex(columns=columns).apply(pd.to_numeric, errors='coerce')
    values = values.replace([float('inf'), float('-inf')], float('nan'))
    if percentage:
        values = values.where((values >= 0) & (values <= 100))
    return values


def summarize(frame, groups=None):
    groups = groups or {'availability': AVAILABILITY, 'accessibility': ACCESSIBILITY,
                        'drop_rate': DROP, 'mobility': MOBILITY, 'data_mb': DATA, 'voice_erlang': VOICE}
    result = {}
    for key, columns in groups.items():
        values = numeric(frame, columns, percentage=key not in ('data_mb', 'voice_erlang'))
        if key in ('data_mb', 'voice_erlang'):
            values = values.where(values >= 0)
            value = values.sum(min_count=1).sum(min_count=1)
        else:
            value = values.mean().mean()  # Equal weight for each available technology.
        result[key] = float(value) if pd.notna(value) else None
    return result


def prepare(frame):
    frame = frame.copy()
    frame['report_day'] = pd.to_datetime(frame.get('time', pd.Series(index=frame.index, dtype='object')), errors='coerce', utc=True).dt.normalize()
    return frame


def compare_days(frame):
    """Compare two most recent reporting dates on common nonempty site IDs and metric columns."""
    if frame.empty or 'time' not in frame or 'ihs_id' not in frame:
        return {'available': False, 'reason': 'Reporting dates and site identifiers are required.'}
    data = prepare(frame)
    dates = sorted(data['report_day'].dropna().unique())
    if len(dates) < 2:
        return {'available': False, 'reason': 'Upload at least two reporting dates to enable comparisons.'}
    previous, latest = dates[-2:]
    before, after = [data[data['report_day'] == day].copy() for day in (previous, latest)]
    def sites(df):
        return set(df['ihs_id'].dropna().astype(str).str.strip()) - {''}
    before_sites, after_sites = sites(before), sites(after)
    common = before_sites & after_sites
    if not common:
        return {'available': False, 'reason': 'The two reporting dates have no common site IDs.'}
    before = before[before['ihs_id'].astype(str).str.strip().isin(common)]
    after = after[after['ihs_id'].astype(str).str.strip().isin(common)]
    # Each metric uses exactly the same site/column pairs on both days. Aggregate
    # duplicate source records per site before comparing, rather than counting them twice.
    groups = {'availability': AVAILABILITY, 'accessibility': ACCESSIBILITY, 'drop_rate': DROP,
              'mobility': MOBILITY, 'data_mb': DATA, 'voice_erlang': VOICE}
    comparisons = {}
    for metric, columns in groups.items():
        percent = metric not in ('data_mb', 'voice_erlang')
        pairs = []
        for df in (before, after):
            vals = numeric(df, columns, percentage=percent)
            if not percent: vals = vals.where(vals >= 0)
            vals.index = df['ihs_id'].astype(str).str.strip()
            pairs.append(vals.groupby(level=0).mean().reindex(sorted(common)))
        mask = pairs[0].notna() & pairs[1].notna()
        a, b = [p.where(mask) for p in pairs]
        if not mask.any().any():
            comparisons[metric] = {'previous': None, 'current': None, 'delta': None, 'pairs': 0}
            continue
        old, new = [(p.mean().mean() if percent else p.sum(min_count=1).sum(min_count=1)) for p in (a, b)]
        delta = float(new-old) if percent else (float((new-old)/old*100) if old else None)
        comparisons[metric] = dict(previous=float(old), current=float(new), delta=delta,
                                   pairs=int(mask.sum().sum()))
    return dict(available=True, previous_day=str(pd.Timestamp(previous).date()),
                latest_day=str(pd.Timestamp(latest).date()), matched_sites=len(common),
                added_sites=len(after_sites-before_sites), removed_sites=len(before_sites-after_sites),
                gap_days=(pd.Timestamp(latest)-pd.Timestamp(previous)).days, metrics=comparisons)


def quality(frame, now=None):
    if frame.empty:
        return {'rows': 0, 'percent_completeness': None, 'invalid_percentages': 0, 'duplicates': 0,
                'missing_site_ids': 0, 'latest_day': None, 'age_days': None}
    present = [c for c in PERCENTAGES if c in frame and frame[c].notna().any()]
    raw = frame[present].apply(pd.to_numeric, errors='coerce')
    valid = (raw >= 0) & (raw <= 100)
    invalid = raw.notna() & ~valid
    time = pd.to_datetime(frame.get('time', pd.Series(index=frame.index, dtype='object')), errors='coerce', utc=True)
    latest = time.max()
    age = None
    if pd.notna(latest):
        timestamp = pd.Timestamp(now) if now is not None else pd.Timestamp.now(tz='UTC')
        timestamp = timestamp.tz_localize('UTC') if timestamp.tzinfo is None else timestamp.tz_convert('UTC')
        age = (timestamp.normalize()-latest.normalize()).days
    identifiers = frame.get('ihs_id', pd.Series(index=frame.index, dtype='object'))
    missing = identifiers.isna() | identifiers.astype(str).str.strip().eq('')
    keys = pd.DataFrame({'time':time, 'site':identifiers.astype(str).str.strip()})
    has_key = time.notna() & ~missing
    return dict(rows=len(frame), percent_completeness=round(valid.sum().sum()/raw.size*100, 1) if raw.size else None,
                invalid_percentages=int(invalid.sum().sum()), duplicates=int(keys[has_key].duplicated().sum()),
                missing_site_ids=int(missing.sum()), latest_day=str(latest.date()) if pd.notna(latest) else None,
                age_days=age)


def exceptions(frame, policies=None):
    policies = policies or POLICIES
    columns = ['Site', 'Priority', 'Signal', 'Observed', 'Threshold', 'Owner', 'Suggested investigation']
    if frame.empty or 'time' not in frame or 'ihs_id' not in frame:
        return pd.DataFrame(columns=columns)
    data = prepare(frame)
    data = data[data['report_day'] == data['report_day'].max()]
    data = data[data['ihs_id'].notna() & data['ihs_id'].astype(str).str.strip().ne('')]
    results = []
    for site, group in data.groupby('ihs_id'):
        stats = summarize(group)
        for metric, policy in policies.items():
            value = stats.get(metric)
            if value is None: continue
            threshold = policy['threshold']
            breached = value < threshold if policy['direction'] == 'below' else value > threshold
            if breached:
                severity = 'P1' if (metric == 'availability' and value < 95) or (metric == 'drop_rate' and value > 5) else 'P2'
                results.append({'Site':str(site), 'Priority':severity, 'Signal':metric.replace('_', ' ').title(),
                                'Observed':round(value, 2), 'Threshold':f"{policy['direction']} {threshold:g}%",
                                'Owner':policy['owner'], 'Suggested investigation':policy['action']})
    return pd.DataFrame(results, columns=columns).sort_values(['Priority', 'Site', 'Signal']).reset_index(drop=True)
