---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

We're a Python/FastAPI shop, no protobuf at all, but leadership wants our public REST API to follow Google's AIPs. For our orders API (orders belong to customers) give me: the endpoints (HTTP method + path) and JSON request/response shapes for listing a customer's orders with pagination, getting a single order, and cancelling an order, plus the exact JSON error body we should return when an order isn't found. Write it up in rest-design.md.
