#!/usr/bin/env python3
"""Check that the google-aip skill is internally consistent.

build_references.py checks the references/ tree when it is regenerated. This
script checks what sits on top of that tree and can drift away from it as
upstream changes or files are edited by hand:

  frontmatter   SKILL.md frontmatter parses as strict YAML (the failure fixed in
                c18e0b1) and meets the Agent Skills limits on name/description.
  paths         every `references/...` or `guides/...` path that SKILL.md and
                the guides mention exists.
  links         every relative Markdown link in the skill resolves.
  routing       every AIP in references/INDEX.md is named in SKILL.md's routing
                table, so the map has no holes.
  states        the list of non-approved AIPs in SKILL.md ground rule 2 matches
                the State: line in each reference file's header.
  counts        the "N AIPs" totals in SKILL.md and README.md are correct.
  sections      every "AIP-N § Heading" citation names a heading that exists in
                that AIP's reference file.
  evals         every eval case has a prompt, a parseable case.yaml, at least
                one grader, and any scaffold script it declares.
  manifests     plugin and marketplace manifests parse and agree on the name.

Usage:
  python3 scripts/validate_skill.py

Needs PyYAML (`pip install pyyaml`). Exits 1 and lists every problem it finds.
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("validate_skill.py needs PyYAML: pip install pyyaml")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(REPO_ROOT, "skills", "google-aip")
REF_DIR = os.path.join(SKILL_DIR, "references")
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")

# Limits from the Agent Skills specification.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESCRIPTION_MAX = 1024

problems: list[str] = []


def problem(check: str, msg: str) -> None:
    problems.append(f"[{check}] {msg}")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def rel(path: str) -> str:
    return os.path.relpath(path, REPO_ROOT)


def skill_markdown_files() -> list[str]:
    """SKILL.md plus every hand-written guide. references/ is generated."""
    return [SKILL_MD] + sorted(glob.glob(os.path.join(SKILL_DIR, "guides", "*.md")))


# --- reference corpus -------------------------------------------------------

HEADER_RE = re.compile(r"^# AIP-(\d+): .*\n\n> (.*)$", re.M)


def load_aips() -> dict[int, dict]:
    """Map AIP number -> {path, state, headings} from the reference files."""
    aips: dict[int, dict] = {}
    for path in glob.glob(os.path.join(REF_DIR, "*", "aip-*.md")):
        text = read(path)
        m = HEADER_RE.match(text)
        if not m:
            problem("references", f"{rel(path)}: missing provenance header")
            continue
        state = re.search(r"\*\*State:\*\* (\w+)", m.group(2))
        headings = []
        in_fence = False
        for line in text.splitlines():
            if line.startswith("```"):
                in_fence = not in_fence
            elif not in_fence and re.match(r"#{2,6} ", line):
                headings.append(line.lstrip("#").strip())
        aips[int(m.group(1))] = {
            "path": path,
            "state": state.group(1) if state else "",
            "headings": headings,
        }
    return aips


# --- checks -----------------------------------------------------------------


def check_frontmatter(skill: str) -> None:
    m = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    if not m:
        problem("frontmatter", "SKILL.md does not start with a --- frontmatter block")
        return
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        problem("frontmatter", f"SKILL.md frontmatter is not valid YAML: {e}")
        return
    if not isinstance(fm, dict):
        problem("frontmatter", "SKILL.md frontmatter is not a mapping")
        return
    name, desc = fm.get("name"), fm.get("description")
    if name != os.path.basename(SKILL_DIR):
        problem("frontmatter", f"name {name!r} must match the directory name")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > NAME_MAX:
        problem("frontmatter", f"name {name!r} must be lower-case words joined by '-', <= {NAME_MAX} chars")
    if not isinstance(desc, str) or not desc.strip():
        problem("frontmatter", "description must be a non-empty string")
    elif len(desc) > DESCRIPTION_MAX:
        problem("frontmatter", f"description is {len(desc)} chars; the limit is {DESCRIPTION_MAX}")


def check_paths() -> None:
    for md in skill_markdown_files():
        for p in re.findall(r"`((?:references|guides)/[^`\s]+)`", read(md)):
            if "…" in p or p.endswith("/"):
                if p.endswith("/") and not os.path.isdir(os.path.join(SKILL_DIR, p)):
                    problem("paths", f"{rel(md)}: directory {p} does not exist")
                continue
            if not os.path.exists(os.path.join(SKILL_DIR, p)):
                problem("paths", f"{rel(md)}: {p} does not exist")


LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def check_links() -> None:
    files = skill_markdown_files() + glob.glob(os.path.join(REF_DIR, "**", "*.md"), recursive=True)
    for md in files:
        text = re.sub(r"```.*?```", "", read(md), flags=re.S)
        text = re.sub(r"`[^`\n]*`", "", text)
        for target in LINK_RE.findall(text):
            if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if not os.path.exists(os.path.join(os.path.dirname(md), path)):
                problem("links", f"{rel(md)}: broken link {target}")


def check_routing(skill: str, aips: dict[int, dict]) -> None:
    m = re.search(r"^## Routing table.*?(?=^## )", skill, re.S | re.M)
    if not m:
        problem("routing", "SKILL.md has no '## Routing table' section")
        return
    named = {int(n) for n in re.findall(r"(?<![\d.])(\d{1,4})(?![\d.])", m.group(0))}
    for n in sorted(set(aips) - named):
        problem("routing", f"AIP-{n} is in references/ but not in the SKILL.md routing table")


def expand(numbers: str) -> set[int]:
    out: set[int] = set()
    for part in re.split(r",\s*", numbers):
        part = part.strip().removeprefix("AIP-")
        if re.fullmatch(r"\d+[–-]\d+", part):
            a, b = map(int, re.split(r"[–-]", part))
            out.update(range(a, b + 1))
        elif part.isdigit():
            out.add(int(part))
    return out


def check_states(skill: str, aips: dict[int, dict]) -> None:
    m = re.search(r"`draft` or `reviewing` state\s*\(([^)]*)\)", skill)
    if not m:
        problem("states", "could not find the non-approved AIP list in SKILL.md ground rule 2")
        return
    listed = expand(m.group(1))
    actual = {n for n, a in aips.items() if a["state"] != "approved"}
    for n in sorted(actual - listed):
        problem("states", f"AIP-{n} is {aips[n]['state']} but missing from SKILL.md ground rule 2")
    for n in sorted(listed - actual):
        problem("states", f"AIP-{n} is listed as non-approved in SKILL.md but is {aips.get(n, {}).get('state', 'absent')}")


def check_counts(aips: dict[int, dict]) -> None:
    total = len(aips)
    for path in (SKILL_MD, os.path.join(REPO_ROOT, "README.md")):
        for n in re.findall(r"\b[Aa]ll (\d+) AIPs\b", read(path)):
            if int(n) != total:
                problem("counts", f"{rel(path)} says 'all {n} AIPs'; references/ has {total}")
    general = len(glob.glob(os.path.join(REF_DIR, "general", "aip-*.md")))
    m = re.search(r"general/\s+#.*\((\d+) AIPs\)", read(os.path.join(REPO_ROOT, "README.md")))
    if m and int(m.group(1)) != general:
        problem("counts", f"README.md says general/ has {m.group(1)} AIPs; it has {general}")


# Lookahead so that several citations on one line are each matched.
SECTION_RE = re.compile(r"AIP-(\d+) § (?=([^\n]+))")


def check_sections(aips: dict[int, dict]) -> None:
    for md in skill_markdown_files():
        for n, rest in SECTION_RE.findall(read(md)):
            n = int(n)
            if n not in aips:
                problem("sections", f"{rel(md)}: cites AIP-{n} §, but there is no AIP-{n}")
                continue
            rest = rest.replace("**", "")
            if not any(rest.startswith(h) for h in aips[n]["headings"]):
                problem("sections", f"{rel(md)}: 'AIP-{n} § {rest[:40]}' matches no heading in {rel(aips[n]['path'])}")


def check_evals() -> None:
    eval_dir = os.path.join(SKILL_DIR, "evals")
    for case in sorted(glob.glob(os.path.join(eval_dir, "*", "case.yaml"))):
        d = os.path.dirname(case)
        name = os.path.basename(d)
        try:
            cfg = yaml.safe_load(read(case)) or {}
        except yaml.YAMLError as e:
            problem("evals", f"{name}: case.yaml is not valid YAML: {e}")
            continue
        if cfg.get("name") != name:
            problem("evals", f"{name}: case.yaml name {cfg.get('name')!r} does not match its directory")
        if not os.path.isfile(os.path.join(d, "prompt.md")):
            problem("evals", f"{name}: missing prompt.md")
        if not glob.glob(os.path.join(d, "graders", "*.md")):
            problem("evals", f"{name}: no graders")
        script = (cfg.get("context") or {}).get("scaffold_script")
        if script:
            sp = os.path.join(d, script)
            if not os.path.isfile(sp):
                problem("evals", f"{name}: scaffold_script {script} does not exist")
            elif not os.access(sp, os.X_OK):
                problem("evals", f"{name}: scaffold_script {script} is not executable")


def check_manifests() -> None:
    try:
        plugin = json.loads(read(os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")))
        market = json.loads(read(os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")))
    except (OSError, json.JSONDecodeError) as e:
        problem("manifests", str(e))
        return
    names = {p.get("name") for p in market.get("plugins", [])}
    if plugin.get("name") not in names:
        problem("manifests", f"plugin.json name {plugin.get('name')!r} is not listed in marketplace.json")


def main() -> None:
    skill = read(SKILL_MD)
    aips = load_aips()
    check_frontmatter(skill)
    check_paths()
    check_links()
    check_routing(skill, aips)
    check_states(skill, aips)
    check_counts(aips)
    check_sections(aips)
    check_evals()
    check_manifests()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(f"\n{len(problems)} problem(s) found")
    print(f"ok: {len(aips)} AIPs, {len(skill_markdown_files())} skill file(s), all checks passed")


if __name__ == "__main__":
    main()
