# Applying the AIPs to plain REST/JSON

> **Not upstream content.** This guide was written for this skill. The AIPs are written
> in protobuf, and the FAQ (`references/site/faq.md`) tells teams without protos to
> "follow the _spirit_ of the API guidance". This guide shows what that looks like on
> the wire. Each statement carries one of three labels:
>
> - `AIP-N § Section`: the AIP text says it. Read that section before relying on it.
> - **Proto JSON**: the Protocol Buffers canonical JSON encoding, which AIP-127 §
>   HTTP method and path names as the body encoding. It is an external spec, not an AIP.
> - **Skill note**: an engineering mapping this skill suggests. It is not AIP guidance,
>   and you should present it to users as a suggestion.

## How one method becomes an HTTP request

AIP-127 § HTTP method and path sets three binding rules. Every endpoint below follows
them:

1. **Path.** Variables capture the *entire* resource name, not just the ID. So
   `GET /v1/{name=publishers/*/books/*}` binds `name = "publishers/123/books/les-miserables"`.
   The `name` field in the JSON body holds that same string, with no leading slash and
   no version (AIP-122 § Resource URIs).
2. **Body.** Exactly one top-level request field becomes the body: the resource for
   Create and Update, the whole request (`*`) for custom methods. `GET` and `DELETE`
   **must not** have a body.
3. **Query.** Every other request field becomes a query parameter, named in camelCase
   (`?bookId=…`, `?pageSize=…`).

## Standard methods on the wire

Example resource: `publishers/{publisher}/books/{book}`.

| Method | HTTP | Body | Success response |
|---|---|---|---|
| Get (AIP-131) | `GET /v1/publishers/123/books/456` | none | the `Book` itself, not wrapped |
| List (AIP-132) | `GET /v1/publishers/123/books?pageSize=50&pageToken=…&filter=…&orderBy=…` | none | `{"books": […], "nextPageToken": "…"}` |
| Create (AIP-133) | `POST /v1/publishers/123/books?bookId=les-miserables` | the `Book` | the created `Book` |
| Update (AIP-134) | `PATCH /v1/publishers/123/books/456?updateMask=displayName,author` | the `Book` | the updated `Book` |
| Delete (AIP-135) | `DELETE /v1/publishers/123/books/456` | none | `{}`, or the `Book` if soft-deleted |
| Custom (AIP-136) | `POST /v1/publishers/123/books/456:archive` | the request minus `name` | defined by the method |

Points that are easy to get wrong:

- **List** responses use the plural resource field and `nextPageToken`, which is set
  only while more pages remain (AIP-132 § Response message). An `int32 totalSize`
  **may** be added, and it **may** be an estimate (AIP-158 § Guidance). Tokens are
  opaque (AIP-158 § Opacity).
- **Create** takes the ID as the `bookId` query parameter, not as a field in the body.
  The server ignores `name` in the body (AIP-133 § User-specified IDs).
- **Update** `updateMask` is a comma-separated list of field paths. Under **Proto JSON**
  the paths are camelCase (`displayName`). Update masks **must** support `*` for full
  replacement, though "in general, it is safest to explicitly specify the fields"
  (AIP-134 § Request message).
- **Custom methods** use `:verb`, not `/verb` (AIP-136 § HTTP path). **Skill note:**
  test that your router doesn't match `456:archive` as a book ID on the plain
  `/books/{book}` route. IDs that follow AIP-122 § Resource ID segments (RFC-1034:
  letters, digits, hyphens) can never contain `:`, so you can reject it.

## JSON value encoding

**Proto JSON** rules that cover the types the field AIPs prescribe:

| Field type (AIP) | JSON form | Example |
|---|---|---|
| Field names (AIP-140) | lowerCamelCase of the `snake_case` name | `create_time` → `"createTime"` |
| `Timestamp` (AIP-142) | RFC 3339 string, UTC `Z` | `"2026-11-16T06:42:45Z"` |
| `Duration` (AIP-142) | decimal seconds with `s` suffix | `"3.5s"` |
| `int64` / `uint64` | string | `"9007199254740993"` |
| `bytes` | base64 string | `"aGVsbG8="` |
| enum (AIP-126, 216) | the value name as a string | `"ACTIVE"` |
| `FieldMask` (AIP-161) | comma-separated camelCase paths | `"displayName,author"` |
| `google.protobuf.Empty` | empty object | `{}` |

## Errors

AIP-193 § HTTP/1.1+JSON representation defines the error body. Note that `code` is the
**HTTP** status, and `status` is the `google.rpc.Code` name:

```json
{
  "error": {
    "code": 404,
    "message": "Order 'customers/42/orders/1001' was not found.",
    "status": "NOT_FOUND",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "ORDER_NOT_FOUND",
        "domain": "orders.example.com",
        "metadata": { "order": "customers/42/orders/1001" }
      }
    ]
  }
}
```

Every error **must** include an `ErrorInfo`. Its `reason` is `UPPER_SNAKE_CASE` and at
most 63 characters, and each (reason, domain) pair means exactly one thing
(AIP-193 § ErrorInfo). Before you return `NOT_FOUND`, check permissions: a caller who
can't see the resource gets `PERMISSION_DENIED` whether or not it exists
(AIP-193 § Permission Denied).

The status-to-HTTP mapping comes from `google/rpc/code.proto`, which is external to the
AIPs:

| `status` | HTTP | | `status` | HTTP |
|---|---|---|---|---|
| `INVALID_ARGUMENT` | 400 | | `ABORTED` (etag mismatch, AIP-154) | 409 |
| `FAILED_PRECONDITION` | 400 | | `ALREADY_EXISTS` | 409 |
| `OUT_OF_RANGE` | 400 | | `RESOURCE_EXHAUSTED` | 429 |
| `UNAUTHENTICATED` | 401 | | `INTERNAL` | 500 |
| `PERMISSION_DENIED` | 403 | | `UNIMPLEMENTED` | 501 |
| `NOT_FOUND` | 404 | | `UNAVAILABLE` | 503 |

## Field behavior in OpenAPI

**Skill note.** OpenAPI has no `google.api.field_behavior`, so this mapping is a
suggestion, not AIP guidance. Keep the AIP-203 vocabulary in each field's description
as well, so reviewers can still check it.

| AIP-203 behavior | OpenAPI |
|---|---|
| `OUTPUT_ONLY` | `readOnly: true` |
| `IDENTIFIER` (`name`) | `readOnly: true` in the body schema; the path carries it on Get, Update and Delete |
| `INPUT_ONLY` | `writeOnly: true` |
| `REQUIRED` | listed in the schema's `required` (on the Create request schema; Update uses `updateMask`) |
| `IMMUTABLE` | no equivalent: state it in `description`, or use an `x-` extension such as `x-immutable: true` |
| `OPTIONAL` | omitted from `required` |

## Long-running operations

A method that returns an operation responds with an `Operation` resource. Clients poll
it with the `Operations` service's `GetOperation` (the binding is per-API, for example
`GET /v1/{name=operations/*}`) until `done` is `true`, and then read either
`response` or `error` (an AIP-193 error object). The API **must** implement the standard
`Operations` service rather than inventing its own polling endpoint
(AIP-151 § Guidance).

```json
{ "name": "operations/abc123", "done": false,
  "metadata": { "@type": "type.googleapis.com/acme.library.v1.ExportBooksMetadata", "progressPercent": 40 } }
```
