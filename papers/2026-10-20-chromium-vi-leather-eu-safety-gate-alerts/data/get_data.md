# Data retrieval

Source: EU Safety Gate (rapid alert system for dangerous non-food products), public search service used by
https://ec.europa.eu/safety-gate-alerts/screen/search. Retrieved 20 October 2026 (snapshot timestamp 2026-10-20T11:28:38Z).

1. Search: POST https://ec.europa.eu/safety-gate-alerts/public/api/search with body
   {"criteria": {"fullTextSearch": "<term>", "year": [2026, 2025, ..., 2003]}, "pagination": {"sortField": "PUBLICATION_DATE",
   "sortOrder": "DESC", "numberElements": 100, "page": <n>}, "language": "en", ...}
   for the terms "chromium" (758 notifications), "hexavalent" (37) and "leather" (874); union = 1,089 distinct notifications.
   Years 2003-2004 returned no notifications; the archive starts in 2005.
2. Detail: GET https://ec.europa.eu/safety-gate-alerts/public/api/notification/<id>?language=en for each of the 1,089 ids.
   Stored as raw/safetygate_20261020.json ({retrieved, queries, years, ids: {id: [matching terms]}, totals, det: {id: record}}).
3. Denominators: totalElements of the same search with criteria {year: [y]} (all alerts) and {year: [y], riskType: ["CHEMICAL"]}
   (chemical-risk alerts), y = 2005..2026. Stored as raw/denominators_20261020.json.

Safety Gate content is published by the European Commission; reuse is subject to the Commission's reuse policy
(Decision 2011/833/EU). The Commission is not responsible for this analysis.
