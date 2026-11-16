---
type: llm
focus: trace
weight: 1
---

rest-design.md lists orders with GET /v1/customers/{customer}/orders (or equivalent collection path under the customer) using page size + page token query params and a next page token in the response (AIP-132/158)
