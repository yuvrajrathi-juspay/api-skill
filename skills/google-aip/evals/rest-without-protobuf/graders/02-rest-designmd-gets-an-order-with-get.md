---
type: llm
focus: trace
weight: 1
---

rest-design.md gets an order with GET on the order's resource path and returns the order object directly, which carries a resource name like customers/{customer}/orders/{order} in a name field (AIP-131/122)
