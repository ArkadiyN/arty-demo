---
name: sciencedirect
description: Search Scopus/ScienceDirect for scientific articles and fetch full-text XML via the Elsevier API. Use when looking up or downloading articles by topic or DOI.
allowed-tools: Bash
---

Search and retrieve articles from the Elsevier Scopus/ScienceDirect API.

## Prerequisites

`ELSEVIER_API_KEY` must be in the environment:

```bash
set -a; source .env; set +a
```

## Search by topic

```bash
curl -s "https://api.elsevier.com/content/search/scopus?query=TITLE-ABS-KEY(<terms>)&count=10" \
  -H "X-ELS-APIKey: $ELSEVIER_API_KEY" \
  -H "Accept: application/json"
```

**Useful response fields:** `dc:title`, `prism:doi`, `dc:identifier` (Scopus ID), `openaccess` (1 = OA), `prism:publicationName`, `prism:coverDate`.

> Note: Use the **Scopus** endpoint, not ScienceDirect search — the Scopus API is accessible with a developer key; ScienceDirect search requires institutional access.

## Fetch full-text XML (open-access articles)

```bash
set -a; source .env; set +a
curl -s "https://api.elsevier.com/content/article/doi/<DOI>" \
  -H "X-ELS-APIKey: $ELSEVIER_API_KEY" \
  -H "Accept: text/xml" -o article.xml
```

Returns HTTP 200 with full article XML for OA articles. Closed-access articles return an empty PDF body — check `openaccess: 1` before fetching.

## Fetch article figures

Each `<ce:figure>` in the XML has a `locator` (e.g. `gr1`). Fetch the image as:

```bash
PII="S0263224126005622"   # from <pii> in coredata, stripped of dashes/parens
REF="gr1"
curl -s "https://api.elsevier.com/content/object/eid/1-s2.0-${PII}-${REF}.jpg" \
  -H "X-ELS-APIKey: $ELSEVIER_API_KEY" -o fig1.jpeg
```

## Process the XML

```bash
uv run src/utils/elsevier-xml-processor.py <doi_or_xml_path> --output-dir <dir> --markdown
```

This extracts all figures and generates a `.md` file with LaTeX formulas and inline image references.

## Scopus abstract retrieval (metadata only)

```bash
SCOPUS_ID="105030847008"
curl -s "https://api.elsevier.com/content/abstract/scopus_id/${SCOPUS_ID}" \
  -H "X-ELS-APIKey: $ELSEVIER_API_KEY" \
  -H "Accept: application/json"
```
