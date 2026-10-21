# Network Performance — engineering case study

**Author:** Leonard Oluka  
**Stack:** Python, Streamlit, Pandas, Plotly, SQLite, OpenPyXL, ReportLab  
**Evidence:** working source, a sample database, calculation tests, interface regression tests, and reproducible screenshots. This is a portfolio demonstration, not a claim of production customer results.

## Problem and intended user

A radio-network engineer receives daily KPI files covering multiple technologies and sites. Reviewing averages alone can hide changes in measurement coverage, missing counters, and sites that need attention. The dashboard combines a network overview with traceable measurements and portable reporting.

## Implemented workflow

1. Import supported KPI files through the existing schema validation workflow.
2. Review the latest reporting date and network KPIs.
3. Compare the latest two available reporting dates using common site/counter pairs.
4. Inspect a prioritized rule-based queue, select a flagged site, and inspect source availability trends and recent records.
5. Check percentage-cell coverage, out-of-range values, repeated site/timestamp keys, and missing site IDs.
6. Export the investigation queue or use the existing filtered CSV, Excel and PDF report workflows.

## Engineering decisions

### Matched measurements instead of raw deltas

Adding a site can increase total traffic even when every existing site's volume stays unchanged. `compare_days` restricts both reporting dates to common nonempty site IDs and valid counters on both dates. Percentage KPIs average site values within a technology, then weight technologies equally. Traffic totals use the matched site/counter measurements.

Repeated records are averaged per site before this new comparison rather than multiplied into totals. Repeated keys are surfaced for review; this is not a general-purpose source deduplication policy. Existing headline cards retain the legacy aggregations and therefore may differ from the matched-cohort table.

For example, if site A moves from 100 MB to 120 MB while a new site B contributes 900 MB, matched-site growth is **20%**, not **920%**. This is an illustrative fixture verified by the tests, not a business result.

### Missing measurements remain missing

A missing counter is not zero traffic and is not a passing health check. Invalid percentage values are excluded from new investigations/comparisons. A zero traffic baseline makes a relative percentage change undefined. The UI explains each case.

### Transparent policies

The queue flags latest-day site averages below 99% availability, below 98% accessibility or above 2% drop rate. P1 escalation uses availability below 95% or drop rate above 5%. Thresholds are demonstration policies, not approved operator SLAs. Suggested investigations do not prove a cause, dispatch work or execute remediation.

### Presentation shared across pages

`navigation.py`, `sentinel_theme.py` and `assets/sentinel.css` share the navigation shell, chart styling and palette. Dark and Light appearances remain available. New analytical logic is separated from Streamlit rendering to allow deterministic tests.

## Architecture

- `data/database.py`: existing import schema, SQLite operations and overview aggregates.
- `performance_insights.py`: pure comparisons, quality assessment and investigation rules.
- `portfolio_components.py`: Streamlit operational briefing and source drill-down.
- `pages/1_Overview.py`: integrates legacy views with the new briefing.
- `pages/8_Project.py`: an in-app walkthrough and transparent case study.
- `tests/`: isolated page execution, routing, theme controls and analytical edge cases.
- `.github/`: regression CI and real browser screenshot verification.

## Validation and practical limits

The suite includes 13 tests and renders all 12 functional dashboard pages. It checks changes in site coverage, missing counters, zero baselines, duplicate records, invalid values, reporting gaps, thresholds, sidebar routing, chart rendering and theme controls. Interface tests run in a temporary copy so they do not modify the repository database.

A separate GitHub Actions job exercises the real browser and captures desktop/mobile images. Its outcome must be checked in Actions; a configured workflow alone does not establish a passed browser test.

The portfolio does not claim live device collection, per-user access control, predictive AI, validated causal diagnosis or demonstrated financial savings. Some technology, site and alarm views can use generated or session-based demo datasets; they are not automatically the same dataset as the overview. Production use would require coherent data contracts across pages, durable hosted storage, identity and permissions, telemetry integration, and operational validation.

## Demonstration script

Open Command centre → read the source date → inspect What changed → explain matched coverage → inspect a queue item → review its source trend → export the queue → review Data trust → open Project case study. This shows analytical judgment and engineering scope in a short, repeatable walkthrough.
