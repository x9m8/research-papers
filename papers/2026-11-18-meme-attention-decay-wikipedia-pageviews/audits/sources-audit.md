# Sources/Citations Audit — "How memes fade" (independent review)

Scope: citations and data-source claims only (numbers audited separately). Package checked:
/home/claude/p30/pkg/ (manuscript/manuscript.md, README.md). **Note: `lit/brief.md` referenced
by the task brief does not exist in this package** — only README.md and manuscript.md were found.

## CONFIRMED ISSUES

1. **Ratkiewicz et al. (2010) is mischaracterized.** The manuscript (Introduction, p.1) describes
   this paper as finding "a small number of recurring popularity-dynamics 'classes' — mostly
   single, double, or power-law-tailed peaks — across very different kinds of online content,
   from Twitter hashtags to Digg stories to YouTube videos." I pulled the actual paper (same DOI
   cited, 10.1103/PhysRevLett.105.158701, confirmed via Crossref and the arXiv preprint
   1005.2704, same title/authors/journal/year as cited). Its actual subject is bursty popularity
   dynamics on **Wikipedia and the Chilean Web** (not Twitter/Digg/YouTube), explaining heavy-tailed
   burst-magnitude and inter-event-time distributions with a preferential-growth-plus-random-shock
   (rank-shift) model. It does not identify single/double/power-law-tailed "classes" of temporal
   curves. The description in the manuscript instead matches a different, well-known paper (Yang &
   Leskovec 2011, "Patterns of Temporal Variation in Online Media," which does classify Twitter/
   YouTube/etc. time series into ~6 shape classes including single- and double-peak). This looks
   like a citation mix-up, not a minor imprecision, and should be corrected or the citation dropped.

2. **Wu & Huberman (2007) characterization is subtly wrong on the metric.** The manuscript says
   they found "a stretched exponential for the rate at which new **comments** arrive on Digg
   stories." The actual paper (arXiv 0704.1158, same DOI/title/authors/journal/year as cited)
   studies the rate of new **diggs** (votes), not comments; comments are not discussed. The
   stretched-exponential finding and the heterogeneity-across-stories explanation are otherwise
   accurately represented.

3. **Inconsistent citation form for the two prior series papers.** Both x9m8.com posts give their
   own "Cite as" line with a Zenodo DOI: paper 1 ("Too leaky to replicate," https://x9m8.com/are-memes-replicators-error-threshold/)
   should be cited as https://doi.org/10.5281/zenodo.23751533; paper 2 ("Rephrasing without
   replicating") as https://doi.org/10.5281/zenodo.23751529. This manuscript's reference list cites
   paper 2 by its DOI but cites paper 1 by its plain x9m8.com URL instead of its DOI — an
   inconsistency within the same reference list, not a broken link (the URL used does work and the
   title/author match), but it should be made consistent.

4. **ORCID is new to the series.** Neither prior series post (ids 1933, 1955) contains the string
   "ORCID" anywhere in its body text, while this manuscript lists ORCID 0009-0000-1637-7142 and a
   slightly different affiliation string ("New York, NY, USA" vs. the prior papers' "New York,
   USA"). Not an error, but flagging since the audit asked for cross-series consistency — this is
   the first paper in the series to carry an ORCID.

## CHECKED OUT FINE

- All four prior-literature DOIs (Wu & Huberman 10.1073/pnas.0704916104; Crane & Sornette
  10.1073/pnas.0803685105; Weng et al. 10.1038/srep00335; Ratkiewicz et al.
  10.1103/PhysRevLett.105.158701) resolve via Crossref to exactly the titles, authors, journals,
  volumes/issues and years cited in the manuscript and reference list. No orphaned or mismatched
  in-text citations: all 8 reference-list entries (Crane & Sornette, Dawkins, Kalafatis 2026a,
  Kalafatis 2026b, Ratkiewicz et al., Weng et al., Wikimedia Foundation, Wu & Huberman) are cited
  in the body at least once, and every in-text citation has a matching reference entry.
- Crane & Sornette (2008) characterization ("power-law-like response functions... for YouTube view
  counts") is a reasonable simplified gloss of the actual finding (burst relaxation following
  power-law classes within an epidemic/Hawkes-process model); not a mischaracterization.
- Weng et al. (2012) characterization (limited-attention model producing meme fading) matches the
  paper's actual subject.
- Both prior-series papers (Kalafatis 2026a, 2026b) exist live on x9m8.com with exactly the titles
  given in the manuscript's reference list, confirmed via the WP REST API (post ids 1933 and
  1955), and their content/abstracts match how this manuscript characterizes them in the
  Introduction and §4.4.
- Wikipedia's "List of Internet phenomena" is a real, existing list article of the right kind to
  source ~309 candidate titles.
- Spot-checked meme titles are real, existing Wikipedia articles about genuine phenomena:
  "Goncharov (meme)" (confirmed — the real Tumblr-invented-film meme), "Harlem Shake (meme)".
  (Doge, Salt Bae, Mannequin Challenge appeared in search results as expected topics but I could
  not independently confirm their exact current Wikipedia article titles/existence beyond search
  snippets — treat as likely-fine but not as rigorously confirmed as Goncharov/Harlem Shake.)
- Exclusion-criteria rule (dedicated meme-specific article vs. ordinary film-release article) is
  coherent and consistently applied on the facts stated: Goncharov (meme) does have its own
  dedicated Wikipedia article distinct from the fictional film, supporting the stated rationale
  for keeping Barbenheimer/Goncharov/Doge while excluding Morbius/Dear Evan Hansen/West Side
  Story/Saltburn.
- Wikimedia pageview data licensing: Wikimedia's own documentation (meta.wikimedia.org/wiki/Research:Data)
  confirms pageview-derived datasets are released under CC0. The manuscript makes no specific
  license claim (only "free," "no-authentication," "public"), which is accurate and not an
  overclaim either way.
- Novelty framing: a WP REST search of x9m8.com found no existing post specifically on meme
  decay/virality/Wikipedia-pageview modeling other than this series' own two fidelity papers; no
  prior post pre-empts this one.

## Not independently verifiable from this environment

- Could not reach pnas.org or journals.aps.org directly (provenance/permission blocks), so journal
  abstracts for Crane & Sornette and Weng et al. were read via secondary sources (PMC mirror, arXiv,
  IU ScholarWorks) rather than the publisher page directly; Crossref metadata (title/author/journal/
  year) was still confirmed directly for all four.
- Could not independently re-verify the AI-model name claimed in §2.6 ("claude-opus-5-5") against
  any external record — this is an internal authorial claim outside the scope of citation checking.
