# Review checklist

> **Not upstream content.** This guide was written for this skill. It is a coverage
> list, so a review doesn't skip a whole category. It is not a restatement of the AIPs.
> Each item points to the section that governs it (`AIP-N § Section`, checked by
> `scripts/validate_skill.py`). **Open that section before you report a finding**,
> because the conditions and exceptions live there.

## How to run a review

1. **Establish context first.** Is the surface new or already GA? (Compatibility rules
   only bind an existing surface.) Is it management plane or data plane (AIP-111)?
   Is it declarative-friendly (AIP-128)? Several rules change with these answers.
2. **Walk the file top-down** in the order below: package, then resources, methods,
   fields, and errors. Use the tables as a checklist, not as the source of truth.
3. **Write each finding** as: location → `AIP-N § Section` → the quoted rule, with its
   **must**/**should** strength unchanged → a concrete fix.
4. **Rank** **must** violations first, then **should** deviations, then observations.
   Treat code that carries an `aip.dev/not-precedent` comment as a documented deviation
   (AIP-200), and don't report it as a defect.
5. **Before you finish**, re-read the "Commonly misreported" table at the end. It lists
   the mistakes an unaided review made most often in this skill's evals.

## Package and file

| Check | Where |
|---|---|
| `proto3` syntax; one package per API, ending in a version component (`acme.library.v1`) | AIP-191 § Syntax, AIP-191 § Single package |
| Components in the prescribed order: services, then resource messages (parents before children), then request and response messages | AIP-191 § File layout |
| Every RPC has a `google.api.http` binding (except bidi streaming) | AIP-127 § Guidance |
| Path variables use `{name=publishers/*/books/*}` and capture the whole resource name | AIP-127 § HTTP method and path |

## Resources

| Check | Where |
|---|---|
| Each resource has `google.api.resource` with type `{service}/{Type}`, pattern(s), `singular`, `plural` | AIP-123 § Annotating resource types |
| Type name matches the message name | AIP-123 § Type and message name alignment |
| `string name` is the only identifier; no tuples, self-links or numeric IDs | AIP-122 § Guidance |
| Collection identifiers are plural, camelCase, and unique within the name | AIP-122 § Collection identifiers |
| References to other resources are `string` names with `google.api.resource_reference`, not embedded messages | AIP-122 § Fields representing another resource |
| List/Create requests take `string parent` with a `resource_reference` to the parent type (`child_type` when there are several parent types) | AIP-122 § Fields representing a resource's parent |
| Every resource supports Get, and List unless it is a singleton | AIP-121 § Methods |
| Same resource schema in every method that returns or accepts it | AIP-121 § Resources |

## Methods

Check every standard method against its AIP's **Request message** and **Errors**
sections, not only its HTTP verb.

| Check | Where |
|---|---|
| Get returns the resource itself (no `Get…Response` wrapper); `GET`, no body | AIP-131 § Guidance |
| List has `page_size`/`page_token` on the request and `next_page_token` on the response | AIP-132 § Request message, AIP-132 § Response message, AIP-158 § Guidance |
| Page tokens are opaque | AIP-158 § Opacity |
| `filter` and `order_by` are strings with AIP-160 / AIP-132 semantics | AIP-132 § Filtering, AIP-132 § Ordering |
| Create takes `parent`, the resource, and `{resource}_id`; `POST`, body = the resource | AIP-133 § Request message, AIP-133 § User-specified IDs |
| Update takes the resource and a `FieldMask update_mask`; `PATCH`, body = the resource | AIP-134 § Request message, AIP-134 § PATCH and PUT |
| Update does not set `state` or trigger side effects | AIP-134 § Side effects, AIP-216 § Output only |
| Delete has no body; children → `FAILED_PRECONDITION` unless `force` | AIP-135 § Guidance, AIP-135 § Cascading delete |
| Custom methods use `:verb` in the URI, `POST` for mutations and `GET` for reads | AIP-136 § HTTP path, AIP-136 § HTTP methods |
| Custom method names: verb + noun, no prepositions, no `Async` | AIP-136 § Guidance |
| State changes go through transition methods (`:publish`, `:archive`), not Update | AIP-216 § State transition methods |
| Slow methods return `google.longrunning.Operation` with `operation_info` | AIP-151 § Guidance, AIP-151 § Standard methods |
| Request messages contain no required fields beyond the ones the method AIP lists | AIP-131 § Request message (and 132–135) |

## Fields

| Check | Where |
|---|---|
| `lower_snake_case`; repeated fields plural; no verbs or prepositions | AIP-140 § Case, AIP-140 § Repeated fields, AIP-140 § Verbs, AIP-140 § Prepositions |
| Booleans omit `is_` | AIP-140 § Booleans |
| Every field has `google.api.field_behavior`; `IDENTIFIER` on `name` only | AIP-203 § Guidance, AIP-203 § Identifier |
| Times are `google.protobuf.Timestamp` named `*_time`; durations are `Duration` | AIP-142 § Timestamps, AIP-142 § Durations |
| Standard names where they apply: `create_time`, `update_time`, `display_name`, `etag`, `uid` | AIP-148 § Guidance |
| Enums: `UPPER_SNAKE_CASE`, zero value `<ENUM>_UNSPECIFIED` | AIP-126 § Guidance |
| `state` is an output-only enum named `State` | AIP-216 § Guidance, AIP-216 § Output only |
| `etag` is a `string` named `etag`; mismatches → `ABORTED` | AIP-154 § Guidance |
| `request_id` (if present) guarantees idempotency | AIP-155 § Guidance |

## Errors

| Check | Where |
|---|---|
| `google.rpc.Status` with canonical codes | AIP-193 § Guidance |
| Every error has exactly one `ErrorInfo` with a stable `reason` and `domain` | AIP-193 § ErrorInfo |
| Permission and existence checks don't leak whether a resource exists | AIP-193 § Permission Denied, AIP-211 § Guidance |

## Compatibility (existing surface only)

| Check | Where |
|---|---|
| No new required fields on existing requests or resources | AIP-180 § Adding components |
| No renames or removals (add the new field alongside the old one instead) | AIP-180 § Removing or renaming components |
| No type changes and no moves into or out of a oneof | AIP-180 § Changing the type of fields, AIP-180 § Moving into oneofs |
| No change to resource name format or default values | AIP-180 § Changing resource names, AIP-180 § Default values must not change |

## Commonly misreported

An unaided review got these wrong most often in this skill's evals. Before reporting any
of them, check the strength and currency against the source.

| Claim | What the AIP actually says | Where |
|---|---|---|
| "Update **must** use PATCH" | **should**; Google APIs generally don't support `PUT` | AIP-134 § Guidance, AIP-134 § PATCH and PUT |
| "User-specified IDs must not be UUIDs" | That guidance was **dropped** on 2025-03-10 | AIP-122 § Disallowing UUIDs in user-specified IDs |
| "Every resource **must** have a `uid`" | `uid` is output only; *when provided* it **must** be a UUID4; declarative-friendly resources **should** include it | AIP-148 § uid |
| "Changing the default `page_size` is breaking" | The default **may** change over time | AIP-132 § Request message |
| "`is_` prefix / `_at` suffix is a violation" | Both are **should** rules, not **must** | AIP-140 § Booleans, AIP-142 § Timestamps |
| "Enum zero value **must** be `_UNSPECIFIED`" | **should**; a meaningful zero value such as `UNKNOWN` is a stated exception | AIP-126 § Guidance |
| "`etag` on a resource needs `field_behavior`" | The AIP-154 `etag` field on a resource **should not** carry it | AIP-203 § Guidance |
