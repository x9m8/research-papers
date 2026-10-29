# Search log: "Bags and the body" pooled analysis

Searcher: Claude (agent run), 2026-10-20.

## Sources and access

- **Europe PMC REST API** (`/webservices/rest/search`, `resultType=lite`, `pageSize=1000`), queried with `fetch()` from a Chrome tab on www.ebi.ac.uk. Direct curl access to Europe PMC and NCBI E-utilities was refused by the network proxy (HTTP 403 on CONNECT), so PubMed was not queried separately. Europe PMC indexes all of MEDLINE/PubMed plus PMC, Agricola, patents and some preprints, so PubMed records are covered.
- **Full texts:**
  - Europe PMC `fullTextXML` for PMC open-access articles.
  - Publisher, repository or proceedings PDFs, parsed in-browser with pdf.js. These covered ISBS proceedings (ojs.ub.uni-konstanz.de), Motricidade, J-STAGE, the Hacettepe repository and the uOttawa repository.
  - Full texts were not retrieved when a site showed a bot check (Cloudflare) or a paywall. This affected the Teesside and Cumbria Pure portals and degruyter.com. No bot check was bypassed.
- **Web search** (general engine) for grey literature and existing reviews.
- **Unpaywall API**, used to locate open-access copies of the non-PMC DOIs.
  - Note: Unpaywall requires an email parameter. Future runs use a placeholder address.

## Europe PMC queries (run 2026-10-20)

| # | Query string | Hits |
|---|---|---|
| Q1 | `(TITLE_ABS:("shoulder bag" OR "single strap" OR "one-strap" OR "one strap" OR "single-strap" OR briefcase OR handbag OR "messenger bag" OR "cross-body" OR "crossbody" OR "hand-carried" OR "carrying a bag" OR "shoulder bags" OR "one-shoulder" OR "single shoulder" OR "unilateral load" OR "asymmetric load" OR "asymmetrical load")) AND (TITLE_ABS:(gait OR posture OR EMG OR electromyography OR trunk OR "load carriage" OR discomfort OR pressure OR "muscle activity" OR spine OR walking))` | 281 |
| Q2 | `TITLE_ABS:("bag" AND ("asymmetric" OR "asymmetrical" OR "unilateral" OR "one shoulder" OR "single shoulder" OR "side-carried" OR "hand carry" OR "hand-held") AND (gait OR posture OR electromyography OR walking))` | 28 |
| Q3 | `TITLE_ABS:(("carrying" OR "carriage") AND ("bag" OR "bags" OR "satchel" OR "purse" OR "tote") AND ("backpack") AND (gait OR posture OR electromyography OR trunk OR walking))` | 24 |
| Q4 | `TITLE_ABS:(("unilateral load carriage" OR "unilateral load carrying" OR "asymmetric load carriage" OR "asymmetrical load carriage" OR "asymmetric load carrying" OR "asymmetrical load carrying" OR "single-sided load" OR "one-sided load" OR "hand-held load" OR "hand carried load" OR "carrying a load in one hand"))` | 57 |
| Q5 | `TITLE_ABS:(("satchel" OR "purse" OR "tote bag" OR "shopping bag" OR "side bag" OR "sling bag" OR "laptop bag" OR "computer bag" OR "school bag" OR "schoolbag") AND ("one shoulder" OR "single shoulder" OR "one-shoulder" OR "unilateral" OR "asymmetric" OR "single strap" OR "hand"))` | 189 (noisy: "purse-string" surgery) |
| Q6 | `TITLE_ABS:(("asymmetric" OR "asymmetrical" OR "unilateral" OR "shoulder bag" OR "single strap" OR handbag) AND ("load carriage" OR "load carrying" OR "bag carrying") AND ("systematic review" OR "meta-analysis" OR "scoping review" OR review))` | 1 |
| Q7 | `TITLE:(bag OR bags OR handbag OR satchel OR briefcase OR purse) AND TITLE:(carrying OR carriage OR carry OR wearing OR "carrying method" OR "carrying style" OR strap)` | 129 |
| Q8 | `TITLE_ABS:("bag" AND ("strap" OR "carrying method" OR "carrying methods" OR "carrying style" OR "carrying type" OR "carrying position") AND ("muscle" OR "gait" OR "posture" OR "shoulder" OR "pressure" OR "trunk"))` | 97 |
| Q9 | `TITLE_ABS:(("shoulder strap" OR "strap pressure" OR "contact pressure" OR "interface pressure") AND ("one strap" OR "single strap" OR "one-strap" OR "single-strap" OR "shoulder bag" OR "one shoulder" OR "messenger" OR "satchel" OR "unilateral"))` | 51 |
| Q10 | `TITLE_ABS:(("oxygen consumption" OR "energy expenditure" OR "metabolic cost" OR "energy cost" OR "heart rate") AND ("shoulder bag" OR "single strap" OR "single-strap" OR "one strap" OR "satchel" OR handbag OR briefcase OR "hand-carried" OR "one hand" OR "unilateral load") AND (walking OR carriage OR carrying))` | 21 |
| Q11 | `TITLE_ABS:(("cross bag" OR "crossbody" OR "cross-body bag" OR "sling bag" OR "side bag" OR "single-strap bag" OR "one-strap bag" OR "single strap bag" OR "shoulder-bag"))` | 56 |
| Q12 | `TITLE:"letter-carrier satchels"` (follow-up to a Q9 hit) | 2 |

- **Total hits:** 936.
- **Unique records after de-duplication** (by DOI, else source+ID): 789. Patents and conference duplicates were included in the hits and removed at title screening.

## Other sources (web search, 2026-10-20)

Queries run:

- `systematic review one-shoulder bag OR "single-strap" bag carriage posture gait muscle activity adults`
- `"shoulder bag" carrying "upper trapezius" electromyography walking J Phys Ther Sci`
- `"cross-body bag" OR "messenger bag" carrying gait posture study healthy adults shoulder height`
- Targeted title searches for Ozgul 2012, Bettany-Saltikov 2012, Bampouras 2016 and Corrigan (hockey bag)
- `systematic review meta-analysis asymmetric unilateral load carriage gait posture shoulder bag handbag adults`

Nine additional records:

- Sussman 2001 (ISBS proceedings)
- Mache et al. (ISBS proceedings)
- Rodrigues 2020 (Motricidade)
- Corrigan 2012 MSc thesis (uOttawa)
- Corrigan & Li 2012 (ISBS progress report)
- Simpson et al. (ISB 2005 abstract; backpack only)
- Gai et al. 2025 systematic review
- SSRC conference systematic review (asymmetrical load-carrying)
- ClinicalTrials.gov NCT06992518 ("The Effect of Bag Carrying Style on Gait Parameters in Healthy Adults"; registry entry, no results seen)

## PRISMA-style flow

| Stage | n |
|---|---|
| Records identified, Europe PMC (unique) | 789 |
| Records identified, other sources | 9 |
| Records screened (title/abstract) | 798 |
| Excluded at title/abstract (off-topic, patents, surgery "purse-string", children-only surveys, models, duplicates, non-asymmetric load) | 733 |
| Reports sought for detailed assessment | 65 |
| Reports not retrieved (abstract only: paywalled, bot-checked, or not located) | 41 |
| Reports assessed for eligibility (18 in full text, 6 from abstract or partial text) | 24 |
| Excluded at full text (reasons in studies.csv) | 11 |
| **Studies included** | **13** |
| — adult studies with extractable mean + dispersion | 9 (Hardie2015, Yoon2014, Hyung2016, Hyun2018, Shin2016, Sussman2001, Rodrigues2020, Corrigan2012 [SE], Tseng2011 [marginal SDs]) |
| — adult study, means only (no SD/SE) | 1 (Tajik2026) |
| — adult study, figures only (not digitised) | 1 (Suzuki2025) |
| — adolescent subgroup (flagged), extractable | 2 (Negrini2007, Ozgul2012) |

Full-text exclusions (11):

- No eligible comparator: Son2013, Cho2013, Ramadan2018, deVette2014
- Comparator or outcome outside protocol: Wang2021, Mache_ISBS
- Model or single case: Zhao2023, Presta2020
- Duplicate: CorriganLi2012_ISBS
- Reviews: Guleria2023, Ellapen2021

The 41 abstract-only reports are mostly potentially eligible. Priority retrievals, ideally through library access:

- An2010
- Zhang2010
- Shi2015
- Yoon2012
- Bettany-Saltikov2012
- O'Shea2006
- Motmans2006
- Pascoe1997 (adolescent)
- Bampouras2016
- Phonpichit2016
- Matsuo2008
- DeVita1991
- Ikeda2008
- Holland2019
- Bloswick1994
- Lin1996 (shoulder strap soft-tissue pressure)
- Takehana1994
- Kellis2009 (children)
- Cottalorda2003 (children)
- Mandrekar2019 (adolescent)
- Park2018

## Extraction conventions

- Numbers were extracted only from tables or text actually read in full text. Nothing was digitised from figures.
- Superscript significance markers were stripped.
- SE, marginal SD and change-score SD are labelled in the `carry_dispersion` and `comparison_dispersion` fields of `extraction.csv`.
- Within-subject correlations were not reported in any included study.
