---
name: google-aip
description: "Google API Improvement Proposals (google.aip.dev), verbatim. Use to design or review REST/gRPC/proto APIs: resources, methods, fields, pagination, LROs, errors, versioning, or any AIP-N."
---

# Google API Improvement Proposals (AIPs)

This skill packages **every AIP published at <https://google.aip.dev>**: all 118 AIPs
across all scopes, the site's FAQ, Adopting, Licensing, Contributing and News pages,
and the AIP-160 filtering grammar. Each one lives in `references/` as an unmodified copy
of the upstream source (<https://github.com/aip-dev/google.aip.dev>, revision in
`references/UPSTREAM_REVISION`). The changes are limited to: the front matter was
replaced by a provenance header; cross-links were rewritten to local files; and a short
"skill packaging" note was added to each draft/reviewing AIP and to the news archive.

`guides/` holds working aids written for this skill, not upstream text. They point into
`references/` and never override it.

**The reference files are the authority. This file is a map.** Before you state what an
AIP requires, open the relevant reference file and read the section itself. The quick
reference below only exists to point you at the right file faster.

## Ground rules for applying AIPs

1. **Requirement keywords.** AIPs use **must**, **must not**, **should**, **should not**
   and **may** in lower-case bold, interpreted as described in RFC 2119 (AIP-8). Keep the
   strength as written when you report a rule: never present a **should** as a **must**,
   and never weaken a **must**. Where an AIP uses **should**, AIP-8 requires it to give
   valid examples of concerns that can override the guidance. Surface those exceptions.
2. **AIP state.** The `State:` line in each file's header tells you how much weight it
   carries. Per AIP-1, approved AIPs are "best current practice" and "API producers should
   rely primarily on AIPs in the 'approved' state". AIPs in `draft` or `reviewing` state
   (AIP-162, 182, 2715, 2717, 2718, 3201, 3260, 3270–3276, 4116, 4118, 4119) are not
   approved. Say so whenever you rely on one.
3. **Cite precisely.** Name the AIP number and section, e.g. "AIP-158 § Opacity: page
   tokens **must** be opaque". Point to `https://google.aip.dev/<n>` (general scope) or
   `https://google.aip.dev/<scope>/<n>` (other scopes) when the user wants a link.
4. **Do not invent guidance.** If no AIP covers a question, say so, and don't extrapolate
   a rule. Clearly label any engineering opinion of your own as yours, not as AIP
   guidance.
5. **Documented deviations.** Under AIP-200, when an API violates the AIP standards
   "there **must** be an internal comment linking to this document using its descriptive
   link (aip.dev/not-precedent)"; per AIP-200 the comment should also explain what
   violates standards and why it is necessary. When you recommend or accept a deviation,
   use that form, e.g.
   `// (-- aip.dev/not-precedent: <reason>. --)`.
6. **Scope.** AIP-2 recognizes these blocks. Generally applicable: 1–99 for meta-AIPs and
   100–999 for general API design guidance. Product areas: 2500–2599 Cloud, 2700–2799
   Apps (Google Workspace), 3000–3099 Actions on Google, 3200–3299 Firebase, 4100–4199
   Auth libraries, 4200–4299 Client libraries, and 4600–4699 Geo. The published Cloud
   scope also contains the Cloud SDK AIPs 2602–2604. Scoped AIPs apply to their own area.
   The 9000 block (AIP-9000 through AIP-9999) is reserved for internal use by
   organizations writing their own AIPs (`references/site/adopting.md`).
7. **Outside Google / without protobuf.** The FAQ (`references/site/faq.md`) says that if
   you are not using protos you won't be able to follow the example snippets exactly, but
   you can "follow the _spirit_ of the API guidance". Map proto concepts (RPC,
   `google.api.http`, field behavior) to the user's IDL, such as OpenAPI, accordingly.

## How to work

### Designing a new API or resource
1. Follow the order in AIP-121: resources (nouns) → relationships and hierarchy →
   resource schema → methods (prefer standard methods).
2. Read AIP-121, 122, 123, then each standard method you need (131–135), then the field
   AIPs (140, 202, 203, plus any of 141–149 and 216 that apply).
3. Add each pattern you need: pagination 158, filtering 160, field masks 161, long-running
   operations 151, request IDs 155, etags 154, soft delete 164, and so on (see the
   routing table).
4. Finish with polish: naming 190, file structure 191, documentation 192, errors 193,
   retries 194, versioning 185 and 184, compatibility 180 and stability 181.

### Reviewing an API, `.proto` or OpenAPI spec for compliance
Work through `guides/review-checklist.md`. It lists, construct by construct, what to check
and which `AIP-N § Section` governs it. It also lists the claims reviewers most often
get wrong (a **should** reported as a **must**, or guidance that has since been dropped).
For each resource, method, field and message, check it against the applicable AIPs.
Report each finding with: location → AIP-N § section → quoted rule (keeping its
**must**/**should** strength) → concrete fix. Rank **must** violations above **should**
deviations. Note any `aip.dev/not-precedent` comments as deliberate, documented
deviations (AIP-200). The API Linter (<https://linter.aip.dev/>) enforces many of these
rules mechanically. Mention it, but don't claim a lint rule exists unless you know it
does.

### Answering a question about an AIP
Open the reference file and answer from its text. Quote the operative sentence. Check
the file's "Changelog" section when recency matters.

## Routing table: which AIP to read

All paths are relative to this skill's directory. `references/INDEX.md` is the complete
catalog, with state and file for every AIP.

### General: meta and process
| Topic | AIP | File |
|---|---|---|
| What AIPs are, states, workflow | 1 | `references/general/aip-0001-aip-purpose-and-guidelines.md` |
| Numbering and blocks | 2 | `references/general/aip-0002-aip-numbering.md` |
| AIP versioning | 3 | `references/general/aip-0003-aip-versioning.md` |
| AIP style, requirement keywords | 8 | `references/general/aip-0008-aip-style-and-guidance.md` |
| Glossary (API, service name, endpoint, declarative clients, etc.) | 9 | `references/general/aip-0009-glossary.md` |
| API design review FAQ | 100 | `references/general/aip-0100-api-design-review-faq.md` |
| Precedent / `aip.dev/not-precedent` | 200 | `references/general/aip-0200-precedent.md` |
| Beta-blocking changes | 205 | `references/general/aip-0205-beta-blocking-changes.md` |

### General: concepts and resource design
| Topic | AIP | File |
|---|---|---|
| Management vs data plane | 111 | `references/general/aip-0111-planes.md` |
| Resource-oriented design | 121 | `references/general/aip-0121-resource-oriented-design.md` |
| Resource names, IDs, `name`/`parent`, references | 122 | `references/general/aip-0122-resource-names.md` |
| Resource types, `google.api.resource`, patterns | 123 | `references/general/aip-0123-resource-types.md` |
| Resource association (one canonical parent; many-to-one, many-to-many) | 124 | `references/general/aip-0124-resource-association.md` |
| Enumerations | 126 | `references/general/aip-0126-enumerations.md` |
| HTTP/gRPC transcoding, `google.api.http` | 127 | `references/general/aip-0127-http-and-grpc-transcoding.md` |
| Declarative-friendly interfaces (IaC) | 128 | `references/general/aip-0128-declarative-friendly-interfaces.md` |
| Server-modified values and defaults | 129 | `references/general/aip-0129-server-modified-values-and-defaults.md` |
| Singleton resources | 156 | `references/general/aip-0156-singleton-resources.md` |
| Policy preview | 236 | `references/general/aip-0236-policy-preview.md` |

### General: methods (operations)
| Topic | AIP | File |
|---|---|---|
| Method categories and choosing one (standard, custom, stateless, etc.) | 130 | `references/general/aip-0130-methods.md` |
| Get | 131 | `references/general/aip-0131-standard-methods-get.md` |
| List | 132 | `references/general/aip-0132-standard-methods-list.md` |
| Create (incl. user-specified IDs) | 133 | `references/general/aip-0133-standard-methods-create.md` |
| Update (PATCH, `update_mask`, upsert) | 134 | `references/general/aip-0134-standard-methods-update.md` |
| Delete (cascading, `force`, etag, `allow_missing`) | 135 | `references/general/aip-0135-standard-methods-delete.md` |
| Custom methods (`:verb`) | 136 | `references/general/aip-0136-custom-methods.md` |
| Long-running operations | 151 | `references/general/aip-0151-long-running-operations.md` |
| Batch Get / Create / Update / Delete | 231 / 233 / 234 / 235 | `references/general/aip-0231-batch-methods-get.md`, `aip-0233-…`, `aip-0234-…`, `aip-0235-…` |

### General: fields
| Topic | AIP | File |
|---|---|---|
| Field names | 140 | `references/general/aip-0140-field-names.md` |
| Quantities (units, sizes, counts) | 141 | `references/general/aip-0141-quantities.md` |
| Time and duration | 142 | `references/general/aip-0142-time-and-duration.md` |
| Standardized codes (language, currency, region, etc.) | 143 | `references/general/aip-0143-standardized-codes.md` |
| Repeated fields | 144 | `references/general/aip-0144-repeated-fields.md` |
| Ranges | 145 | `references/general/aip-0145-ranges.md` |
| Generic fields (`Struct`, `Any`, maps, oneof) | 146 | `references/general/aip-0146-generic-fields.md` |
| Sensitive fields | 147 | `references/general/aip-0147-sensitive-fields.md` |
| Standard fields (`create_time`, `display_name`, `uid`, etc.) | 148 | `references/general/aip-0148-standard-fields.md` |
| Unset field values / `optional` | 149 | `references/general/aip-0149-unset-field-values.md` |
| Fields (general rules) | 202 | `references/general/aip-0202-fields.md` |
| Field behavior (`REQUIRED`, `OUTPUT_ONLY`, `IDENTIFIER`, etc.) | 203 | `references/general/aip-0203-field-behavior-documentation.md` |
| States (`state` enums) | 216 | `references/general/aip-0216-states.md` |

### General: design patterns
| Topic | AIP | File |
|---|---|---|
| Jobs | 152 | `references/general/aip-0152-jobs.md` |
| Import and export | 153 | `references/general/aip-0153-import-and-export.md` |
| Resource freshness validation (etags) | 154 | `references/general/aip-0154-resource-freshness-validation.md` |
| Request identification (`request_id`) | 155 | `references/general/aip-0155-request-identification.md` |
| Partial responses (view enums, field-mask parameter) | 157 | `references/general/aip-0157-partial-responses.md` |
| Pagination | 158 | `references/general/aip-0158-pagination.md` |
| Reading across collections (`-` wildcard) | 159 | `references/general/aip-0159-reading-across-collections.md` |
| Filtering (grammar: `references/assets/ebnf-filtering.txt`) | 160 | `references/general/aip-0160-filtering.md` |
| Field masks | 161 | `references/general/aip-0161-field-masks.md` |
| Resource revisions (**draft**) | 162 | `references/general/aip-0162-resource-revisions.md` |
| Change validation (`validate_only`) | 163 | `references/general/aip-0163-change-validation.md` |
| Soft delete / undelete | 164 | `references/general/aip-0164-soft-delete.md` |
| Criteria-based delete (Purge) | 165 | `references/general/aip-0165-criteria-based-delete.md` |
| Unicode | 210 | `references/general/aip-0210-unicode.md` |
| Authorization checks | 211 | `references/general/aip-0211-authorization-checks.md` |
| Resource expiration | 214 | `references/general/aip-0214-resource-expiration.md` |
| Unreachable resources | 217 | `references/general/aip-0217-unreachable-resources.md` |

### General: compatibility, versioning, polish, protobuf
| Topic | AIP | File |
|---|---|---|
| Backwards compatibility | 180 | `references/general/aip-0180-backwards-compatibility.md` |
| Stability levels (alpha/beta/GA) | 181 | `references/general/aip-0181-stability-levels.md` |
| External software dependencies (**reviewing**) | 182 | `references/general/aip-0182-external-software-dependencies.md` |
| API version identifiers | 184 | `references/general/aip-0184-api-version-identifiers.md` |
| API versioning | 185 | `references/general/aip-0185-api-versioning.md` |
| Naming conventions | 190 | `references/general/aip-0190-naming-conventions.md` |
| File and directory structure (proto packages) | 191 | `references/general/aip-0191-file-and-directory-structure.md` |
| Documentation (comments) | 192 | `references/general/aip-0192-documentation.md` |
| Errors (`google.rpc.Status`, `ErrorInfo`) | 193 | `references/general/aip-0193-errors.md` |
| Automatic retry configuration | 194 | `references/general/aip-0194-automatic-retry-configuration.md` |
| Common components (`google.type`, etc.) | 213 | `references/general/aip-0213-common-components.md` |
| API-specific protos | 215 | `references/general/aip-0215-api-specific-protos.md` |

### Other scopes
| Scope | AIPs | Directory |
|---|---|---|
| Google Cloud Platform | 2510 Project identifiers; Cloud SDK: 2602 Parameter-dependent arguments, 2603 List command arguments, 2604 Numeric arguments | `references/cloud/` |
| Auth | 4110 Application Default Credentials, 4111 Self-signed JWT, 4112 Service Account Keys, 4113 gcloud CLI Integration, 4114 Device Certificate Authentication via Mutual TLS, 4115 Default Credentials For Google Cloud Virtual Environments, 4116 Identity Tokens (**draft**), 4117 External Account Credentials (Workload Identity Federation), 4118 Mutual Authentication Using Workload Credentials (**draft**), 4119 mTLS Token Binding (**draft**) | `references/auth/` |
| Client libraries | 4210 Client library generators, 4221 Client-side retry, 4222 Routing headers, 4223 Client-side payload validation, 4231 Parsing resource names, 4232 Method signatures, 4233 Automatic pagination, 4234 Common service client mixins, 4235 Automatically populate fields in the request message, 4236 Version-aware clients, 4290 Docker interface | `references/client-libraries/` |
| Workspace | 2712 API completeness, 2713 One team owns each type, 2715 Documenting authorization changes (**reviewing**), 2716 Standard terms in names, 2717 Patterns for generic fields (**reviewing**), 2718 References to objects in other APIs (**draft**) | `references/apps/` |
| Actions on Google | 3001 Actions on Google AIP Process, 3010 Vertical Integration Webhook Format, 3020 BII Schema Principles, 3021 Type protos in Actions on Google APIs, 3022 Built-in intent arguments and fulfillment APIs | `references/aog/` |
| Firebase (hidden from site nav; all **draft**) | 3201 Projects and Apps, 3260 Firebase CLI, 3270 JavaScript APIs, 3271 Android APIs, 3272 iOS APIs, 3273 C++ APIs, 3274 .NET APIs, 3275 Python APIs, 3276 Go APIs | `references/firebase/` |

Site pages: `references/site/faq.md`, `adopting.md`, `licensing.md`, `contributing.md`,
`news.md` (historical newsletter archive).

## Quick reference: the most-used rules

These are condensed from the reference files, which remain the authority. Each item names
its source AIP. **Read the source before relying on a rule**, because each AIP carries
conditions, exceptions and examples that are omitted here.

### Resources (AIP-121, 122, 123)
- A resource-oriented API **should** generally be modeled as a resource hierarchy. A
  resource **must** support Get, and **must**
  support List except for singleton resources. APIs **should** prefer standard methods
  over custom methods. (121)
- A resource's schema **must** be the same across all methods whose request or response
  is or contains that resource. (121)
- Management-plane operation completion **must** mean the resource's existence and all
  user-settable values have reached a steady state (strong consistency). The protocol
  **must** be stateless. Resource relationships **must** be representable as a directed
  acyclic graph (this does not apply to relationships expressed via output-only fields),
  and the parent-child relationship **must** be acyclic. (121)
- Resource names are like `publishers/123/books/les-miserables`: no leading slash,
  segments separated by `/`, unique within the API. Resources **must** expose a `string
  name` field, and **must not** expose tuples, self-links, or other forms of resource
  identification. ID fields **should** be strings. (122)
- Collection identifiers **must** be plural, `camelCase`, match `/[a-z][a-zA-Z0-9]*/`, be
  concise American English, and be unique within a resource name. (122)
- User-specified IDs **should** conform to RFC-1034 and **should** restrict letters to
  lower-case: `^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$`. The API **must** document allowed
  formats. (122)
- Fields **must not** be called `name` except for the resource name. A request's
  collection field **should** be `string parent`. A field referencing another resource
  **should** be a `string` holding its resource name, with
  `google.api.resource_reference`. It **should not** embed the other resource's message,
  except in the two listed cases. (122)
- Resource type `{Service Name}/{Type}`, e.g. `pubsub.googleapis.com/Topic`. The type
  **must** match the message name, be singular, and use PascalCase. Annotate it with
  `google.api.resource` (**should**). Pattern variables **must** be `snake_case` without
  an `_id` suffix. `singular` / `plural` **must** be lower camel case. New patterns
  **must** be appended, never reordered or removed. (123)

### Standard methods (AIP-131 to 135)
| | Get (131) | List (132) | Create (133) | Update (134) | Delete (135) |
|---|---|---|---|---|---|
| RPC name | `Get<Resource>` | `List<Resources>` | `Create<Resource>` | `Update<Resource>` | `Delete<Resource>` |
| HTTP verb | `GET` (**must**) | `GET` (**must**) | `POST` (**must**) | `PATCH` (**should**; `PUT` strongly discouraged) | `DELETE` (**must**) |
| URI variable | `name` | `parent` | `parent` | `{resource}.name` | `name` |
| `body` | none (**must not**) | none (**must** be omitted) | resource field (**must**) | resource field (**must**) | none (**must not**) |
| `method_signature` (**should**) | `"name"` | `"parent"` (top-level: none or `""`) | `"parent,{resource},{resource}_id"`; for top-level resources see AIP-133 | `"{resource},update_mask"` | `"name"` |
| Response | the resource (**must**) | `List…Response` with one repeated resource field plus `next_page_token` | the resource (**must**), or LRO resolving to it | the resource (**must**), or LRO resolving to it | `google.protobuf.Empty` (**should**); the resource if soft-deleted |

Key details. Each method's AIP has more:
- **List:** `page_size` and `page_token` **must** be on the request. `next_page_token`
  **must** be set if there are subsequent pages and **must not** be set on the final page.
  Ordering uses `string order_by`, filtering uses `string filter` (AIP-160). (132)
- **Create:** On the management plane, an API **must** let the user specify the ID (the
  `{resource}_id` field on the request message, not the resource). On the data plane it
  **should**. The `name` field on the resource **must** be ignored. A duplicate name
  **must** error with `ALREADY_EXISTS`, or `PERMISSION_DENIED` when the user can't see the
  duplicate. (133)
- **Update:** If partial update is supported, the request **must** have an optional
  `google.protobuf.FieldMask update_mask`. An omitted mask means all populated fields, an
  empty mask **should** be a no-op, and `*` **must** be supported as full replacement.
  Update **should not** trigger side effects. State fields **must not** be directly
  updatable. On etag mismatch the request **must** fail with `ABORTED`. (134, 154)
- **Delete:** The API **must** fail with `FAILED_PRECONDITION` if child resources are
  present, unless the only children are singletons. For cascading delete, it **should**
  provide `bool force`. (135)
- Request messages for all five **must not** contain other required fields, and **should
  not** contain other optional fields except those described in that method's AIP or in
  another AIP (Get: "described in another AIP").

### Custom methods (AIP-136)
- Custom methods **should** only be used for functionality that can not be easily
  expressed via standard methods. The name **should** be a verb followed by a noun. It
  **must not** contain prepositions or the term `Async`, and the verb **should not**
  contain any of the standard method verbs.
- HTTP `GET` or `POST` only. `POST` **must** be used for side effects or mutations, and
  `GET` **must** be used for data retrieval (with stated exceptions for `POST`). The URI
  **must** use `:` plus the custom verb in camelCase (e.g. `:archive`). `body`
  **should** be `"*"`.

### Long-running operations (AIP-151)
- Return `google.longrunning.Operation`. Never copy the `Operation` proto, and don't
  stream the response. The method **must** have `google.longrunning.operation_info` with
  both `response_type` and `metadata_type`. APIs returning `Operation` **must** implement
  the `Operations` service, and **must not** define their own interfaces for it.

### Pagination (AIP-158)
- Collections **must** be paginated from the outset. `page_size` and `page_token`
  **must not** be required. A `page_size` of 0 means the server default; above the
  maximum, the API **should** coerce down; a negative value **must** return
  `INVALID_ARGUMENT`.
- Page tokens **must** be opaque, URL-safe and not user-parseable, and **must not**
  grant authorization. An empty `next_page_token` is the only end-of-collection signal.
  Streaming responses **must not** be used.

### Fields (AIP-140, 203, and others)
- Proto field names **must** be `lower_snake_case`. Repeated fields **must** use the
  plural form. Names **should not** include prepositions and **must not** be verbs.
  Booleans **should** omit `is`. Display labels **should** be `display_name`. Use `uri`
  for arbitrary URIs and `url` for URL-only fields (**should**). (140)
- Apply `google.api.field_behavior` to every field on a message or sub-message used in
  a request (**must**),
  except the AIP-154 `etag` field on a resource message (**should not**). `oneof`
  fields **may** omit it. Use at least one of `REQUIRED`, `OPTIONAL`, `OUTPUT_ONLY`
  (**must**), and never `FIELD_BEHAVIOR_UNSPECIFIED`. `IDENTIFIER` **must** be attached
  to the `name` field and nowhere else. (203)
- Timestamps, durations, quantities, codes, ranges, enums, states and standard field
  names each have their own AIP. See the fields table above.

### Errors (AIP-193)
- Return `google.rpc.Status` with canonical `google.rpc.Code` codes. Every error response
  **must** include an `ErrorInfo` in `details`. Its `reason` **must** be at most 63
  characters and match `[A-Z][A-Z0-9_]+[A-Z0-9]`. Services **must** use the same
  (reason, domain) pair for the same error, and **must not** use the same pair for
  logically different errors. Each detail type **must** appear at most once.

### Compatibility (AIP-180)
- Within a major version, don't break existing clients. You **must not**: add required
  fields to existing requests; remove or rename components; change field types; move
  components between files; move fields into or out of a oneof; change a resource's name
  or a default value; or change value formats.

## Maintenance

To regenerate `references/` from a newer upstream revision, run
`scripts/build_references.py` from the repository that ships this skill (see its
README). The script copies content verbatim and fails if any internal link can't be
resolved.

Content © Google, licensed under CC BY 4.0. Code samples are licensed under Apache 2.0.
Portions of this skill are reproduced from work created and shared by Google
(<https://google.aip.dev/licensing>).
