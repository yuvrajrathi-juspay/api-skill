# Changelog

## 1.1.0

- **Eval suite** (`skills/google-aip/evals/`). Five `claude plugin eval` cases cover
  design, review, compatibility, REST without protobuf, and recency. Each case has a
  grader that checks for contradictions of the AIP text.
- **`scripts/validate_skill.py`** and CI. These check that `SKILL.md` stays consistent
  with `references/`: routing coverage, draft/approved states, counts, `AIP-N § Section`
  citations, links, strict-YAML frontmatter, and eval structure. A weekly job warns when
  upstream AIPs move past `UPSTREAM_REVISION`.
- **`guides/review-checklist.md`**. A construct-by-construct review pass with pointers
  to the governing AIP sections, plus a table of the claims reviewers most often get
  wrong.
- **`guides/rest-json-mapping.md`**. The AIPs on the wire for teams without protobuf:
  HTTP bindings, JSON encoding, the error body, OpenAPI field behavior, and LROs.

## 1.0.0

- The complete AIP corpus from `aip-dev/google.aip.dev@2ccc61a4` (118 AIPs, site pages,
  and the AIP-160 grammar), copied verbatim with provenance headers and local links.
- `SKILL.md` with ground rules, workflows, a routing table, and a quick reference.
- Frontmatter description quoted so that strict YAML parsers load the skill.
