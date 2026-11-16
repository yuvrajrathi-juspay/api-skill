# AIP-3201: Projects and Apps

> **Source:** <https://google.aip.dev/firebase/3201> · **Scope:** Firebase · **State:** draft · **Created:** 2020-06-11
>
> **Note (skill packaging):** this AIP is in the `draft` state, not
> `approved`. See AIP-1 ("States") for what that means before relying on it.

## Guidance

### Resource Hierarchy

APIs that utilize an App ID as part of a resource name **must** include a
Project identifier in the parent:

```
apps/*/items
```

Must instead be:

```
projects/*/apps/*/items
```

Project identifiers **must** follow [Cloud guidance][aip-2510]. As App IDs are
globally unique, Firebase APIs **should** allow the [unique resource
lookup][aip-159-unique] pattern, allowing a `-` in place of a Project
ID/Number. For example:

```
projects/-/apps/1:111222333444:web:abcdef0123456789/things
```

### Referencing App IDs

When referencing an App ID in an SDK or API field, method, or parameter, the
platform-correct initialism of `app_id` **must** be used (as opposed to e.g.
`app`, `application_id`, or `gmp_app_id`).

[aip-2510]: ../cloud/aip-2510-project-identifiers.md
[aip-159-unique]: ../general/aip-0159-reading-across-collections.md#unique-resource-lookup
