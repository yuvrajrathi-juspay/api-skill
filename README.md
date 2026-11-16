# api-skill: Google AIPs as a Claude skill

An [Agent Skill](https://code.claude.com/docs/en/skills) that gives Claude and Claude
Code the **complete Google API Improvement Proposals (AIPs)** published at
<https://google.aip.dev>. Use it to design, write, and review APIs
(resource-oriented REST, gRPC, protobuf, and OpenAPI in the spirit of the AIPs) that
adhere strictly to the AIP guidance.

## What's inside

```
skills/google-aip/
├── SKILL.md                     # How to apply AIPs, routing table, quick reference
├── guides/
│   ├── review-checklist.md      # Construct-by-construct review pass, AIP § pointers
│   └── rest-json-mapping.md     # The AIPs on the wire for REST/JSON and OpenAPI users
└── references/
    ├── INDEX.md                 # Catalog of every AIP: number, title, state, file
    ├── general/                 # AIP-1 … AIP-236 (73 AIPs)
    ├── cloud/                   # AIP-2510, 2602–2604
    ├── auth/                    # AIP-4110 … 4119
    ├── client-libraries/        # AIP-4210 … 4290
    ├── apps/                    # AIP-2712 … 2718 (Workspace)
    ├── aog/                     # AIP-3001 … 3022 (Actions on Google)
    ├── firebase/                # AIP-3201 … 3276
    ├── site/                    # FAQ, Adopting, Licensing, Contributing, News
    ├── assets/ebnf-filtering.txt  # AIP-160 filter grammar
    └── UPSTREAM_REVISION        # aip-dev/google.aip.dev commit the files came from
```

- **All 118 AIPs from every scope**, plus the site pages and the filtering grammar.
- **Content is copied verbatim** from the upstream source
  ([aip-dev/google.aip.dev](https://github.com/aip-dev/google.aip.dev)). Each file
  begins with a provenance header (source URL, scope, category, state, dates).
  Cross-AIP links are rewritten to point at the local files, so the skill works offline.
  Nothing else changes.
- **Guides** written for the skill (kept separate from the verbatim references). The
  review checklist walks a `.proto` or spec construct by construct and points every
  check to its `AIP-N § Section`; CI verifies that each of those sections exists.
  The REST/JSON guide is for teams without protobuf. It shows each standard method as
  an HTTP request and response, plus JSON encoding, the AIP-193 error body, and
  OpenAPI field behavior. It separates AIP text from suggestions of its own.
- `SKILL.md` tells Claude to treat the reference files as the authority, preserve the
  RFC 2119 requirement strength (**must** / **should** / **may**), flag draft and
  reviewing AIPs, and cite the AIP and section for every rule it applies.

## Install

### Claude Code: plugin (recommended)

```
/plugin marketplace add yuvrajrathi-juspay/api-skill
/plugin install api-skill@api-skill
```

Claude loads the skill automatically when it's relevant, or you can invoke it explicitly
with `/api-skill:google-aip`.

### Claude Code: manual

```bash
git clone https://github.com/yuvrajrathi-juspay/api-skill.git
# personal (all projects):
mkdir -p ~/.claude/skills && cp -R api-skill/skills/google-aip ~/.claude/skills/
# or project-only (commit it with your repo):
mkdir -p .claude/skills && cp -R api-skill/skills/google-aip .claude/skills/
```

### Claude.ai (web / desktop)

1. Build the ZIP. The skill folder must be the top level of the archive:
   ```bash
   cd api-skill/skills && zip -r google-aip.zip google-aip
   ```
2. In Claude, open **Customize → Skills**, click **+ → Create skill → Upload a skill**,
   and select `google-aip.zip`. Then toggle the skill on.

Skills on claude.ai require code execution to be enabled. On Team and Enterprise plans,
an owner may need to allow skills.

## Usage examples

- "Design the API for a library service with publishers and books, following the AIPs."
- "Review this `.proto` for AIP compliance." (attach or point at the file)
- "What does AIP-158 say about page tokens?"
- "Is adding a required field to `CreateBookRequest` a breaking change?"
- "How should I name a boolean field that says whether a book is archived?"

## Evaluation

`skills/google-aip/evals/` holds an eval suite for
[`claude plugin eval`](https://code.claude.com/docs/en/plugins). It has five cases, and
each one tests a different way the skill gets used:

| Case | What it checks |
|---|---|
| `design-library-proto` | Greenfield design: standard methods, HTTP mappings, field behavior, a custom method |
| `review-legacy-proto` | Review: finds 12 seeded violations in `files/books.proto`, each tied to its AIP |
| `breaking-change-check` | Compatibility: tells breaking changes (AIP-180) apart from permitted ones (AIP-132) |
| `rest-without-protobuf` | Applying the AIPs to plain REST/JSON (FastAPI) with no protos |
| `uuid-user-ids` | Recency: catches guidance that changed upstream (AIP-122 changelog, 2025-03-10) |

Every case has a "no contradictions of AIP text" grader, because the main failure we
want to catch is a confident answer that misstates a rule's strength, cites the wrong
AIP, or repeats outdated guidance.

```bash
claude plugin eval . --eval-dir skills/google-aip/evals --scaffold
```

`--scaffold` is needed for `review-legacy-proto`, which copies `books.proto` into the
workspace. By default the run includes a no-skill baseline arm. On the first iteration
(one run per configuration), the skill passed 100% of grader checks and the baseline
passed 73%. The baseline failed the no-contradictions grader in all five cases. For
example, it upgraded AIP-134's **should** use PATCH to a **must**, and it repeated the
UUID rule that was dropped from AIP-122.
Results are written to `skills/google-aip/evals/results/`, which is git-ignored.

## Updating to a newer AIP revision

```bash
git clone --depth 1 https://github.com/aip-dev/google.aip.dev /tmp/aip
curl -sSfL https://google.aip.dev/assets/misc/ebnf-filtering.txt -o /tmp/ebnf-filtering.txt
python3 scripts/build_references.py /tmp/aip /tmp/ebnf-filtering.txt
```

The script regenerates `skills/google-aip/references/` deterministically and exits with
an error if any internal link can't be resolved. If upstream adds AIPs or categories,
also update the routing table in `SKILL.md`. Then run:

```bash
pip install pyyaml
python3 scripts/validate_skill.py
```

The validator catches the places where `SKILL.md` can fall out of step with a fresh
`references/` tree. It reports an AIP that is missing from the routing table, a change in
an AIP's draft or approved state, stale AIP counts, and `AIP-N § Section` citations
whose heading no longer exists. It also checks that the frontmatter parses as strict
YAML, that every path and link resolves, and that each eval case is well-formed. CI runs
the validator on every push and pull request. Each Monday, CI also warns if
`aip-dev/google.aip.dev` has moved past `UPSTREAM_REVISION`.

### Packaging notes

- `AIP-4115` links "Device Certificate Authentication (DCA)" to a target that does not
  resolve on the live site. The link is pointed at AIP-4114 ("Device Certificate
  Authentication via Mutual TLS"), the AIP that specifies DCA. See `LINK_FIXES` in the
  build script.
- Non-approved AIPs (`draft` / `reviewing`) carry a one-line note in their header that
  refers the reader to AIP-1's definition of states.

## License and attribution

Portions of this repository are reproduced from work created and
[shared by Google](https://google.aip.dev/licensing) and used according to terms
described in the [Creative Commons 4.0 Attribution License](https://creativecommons.org/licenses/by/4.0/).
Code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
See [LICENSE.md](LICENSE.md). Source: <https://google.aip.dev> /
<https://github.com/aip-dev/google.aip.dev>.

This project is not affiliated with or endorsed by Google.
