---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Our v1 Books API is GA. Product wants three changes in the same v1: (1) add a new required field isbn to CreateBookRequest, (2) rename the Book field title to display_name, (3) bump the default page_size of ListBooks from 50 to 100 since clients complain about too many round trips. Which of these are OK per the AIPs and which break compatibility? What should we do instead for the ones that aren't OK? Put the answer in answer.md.
