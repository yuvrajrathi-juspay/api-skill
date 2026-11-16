#!/usr/bin/env python3
"""Regenerate the google-aip skill reference files from the upstream AIP source.

The AIP content published at https://google.aip.dev is authored in the
https://github.com/aip-dev/google.aip.dev repository. This script converts that
source, *verbatim*, into the reference files that ship with the skill:

  * every AIP in every scope  -> skills/google-aip/references/<scope>/aip-<NNNN>-<slug>.md
  * the site pages (FAQ, Adopting, Licensing, Contributing, News)
                              -> skills/google-aip/references/site/*.md
  * the AIP-160 filtering grammar (served by the site at
    /assets/misc/ebnf-filtering.txt)
                              -> skills/google-aip/references/assets/ebnf-filtering.txt
  * a complete catalog        -> skills/google-aip/references/INDEX.md

The body of every document is copied unchanged. The only transformations are:

  1. The YAML front matter is replaced by a short provenance header (source URL,
     scope, category, state, dates, redirect aliases).
  2. Links that point at other AIPs / site pages are rewritten to relative
     links to the corresponding local reference file, so the skill works
     offline. Links to external sites are left untouched.
  3. `<!-- prettier-ignore-start/end -->` formatter directives are dropped.

Usage:
  git clone --depth 1 https://github.com/aip-dev/google.aip.dev /tmp/aip
  curl -sSfL https://google.aip.dev/assets/misc/ebnf-filtering.txt -o /tmp/ebnf-filtering.txt
  python3 scripts/build_references.py /tmp/aip /tmp/ebnf-filtering.txt

The script exits non-zero if any internal link cannot be resolved.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(REPO_ROOT, "skills", "google-aip")
REF_DIR = os.path.join(SKILL_DIR, "references")
SITE = "https://google.aip.dev"

# Category display titles. Categories without an explicit title in
# aip/general/scope.yaml are displayed by the site as the capitalized code.
GENERAL_CATEGORY_TITLES = {
    "meta": "Meta",
    "process": "Process",
    "api-concepts": "API Concepts",
    "resource-design": "Resource Design",
    "operations": "Operations",
    "fields": "Fields",
    "design-patterns": "Design Patterns",
    "compatibility": "Compatibility and Versioning",
    "polish": "Polish",
    "protobuf": "Protocol buffers",
    "misc": "Miscellaneous",
}
CLOUD_CATEGORY_TITLES = {"gcp": "Google Cloud Platform APIs", "sdk": "Cloud SDK"}

# Known defects in upstream link targets, keyed by (source AIP id, target).
# AIP-4115 links "Device Certificate Authentication (DCA)" to the bare target
# "4", which does not resolve on the site; DCA is specified in AIP-4114
# ("Device Certificate Authentication via Mutual TLS").
LINK_FIXES = {(4115, "4"): 4114}


@dataclass
class Doc:
    src: str
    out: str  # path relative to REF_DIR
    title: str
    body: str
    meta: dict = field(default_factory=dict)
    aip_id: int | None = None
    scope: str = ""


def parse_front_matter(text: str) -> tuple[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def fm_value(fm: str, key: str) -> str:
    m = re.search(r"^\s*%s:\s*(.*)$" % re.escape(key), fm, re.M)
    return m.group(1).strip() if m else ""


def fm_list(fm: str, key: str) -> list[str]:
    m = re.search(r"^%s:[ \t]*(.*)$" % re.escape(key), fm, re.M)
    if not m:
        return []
    inline = m.group(1).strip()
    if inline:
        return [inline]
    items = []
    for line in fm[m.end():].splitlines()[1:]:
        mm = re.match(r"^\s+-\s+(.*)$", line)
        if not mm:
            break
        items.append(mm.group(1).strip())
    return items


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60].rstrip("-")


def load_aips(src_root: str) -> dict[int, Doc]:
    aips: dict[int, Doc] = {}
    aip_root = os.path.join(src_root, "aip")
    for scope in sorted(os.listdir(aip_root)):
        sdir = os.path.join(aip_root, scope)
        if not os.path.isdir(sdir):
            continue
        scope_yaml = open(os.path.join(sdir, "scope.yaml")).read()
        scope_title = fm_value(scope_yaml, "title")
        scope_hidden = fm_value(scope_yaml, "hidden") == "true"
        for name in sorted(os.listdir(sdir)):
            if not name.endswith(".md"):
                continue
            text = open(os.path.join(sdir, name)).read()
            fm, body = parse_front_matter(text)
            aip_id = int(fm_value(fm, "id"))
            m = re.match(r"\s*# (.+)\n", body)
            if not m:
                raise SystemExit(f"{scope}/{name}: no H1 title")
            title = m.group(1).strip()
            body = body[m.end():]
            category = fm_value(fm, "category")
            if scope == "general":
                cat_title = GENERAL_CATEGORY_TITLES.get(category or "misc", category)
            elif scope == "cloud":
                cat_title = CLOUD_CATEGORY_TITLES.get(category, category)
            else:
                cat_title = ""
            url = f"{SITE}/{aip_id}" if scope == "general" else f"{SITE}/{scope}/{aip_id}"
            out = f"{scope}/aip-{aip_id:04d}-{slugify(title)}.md"
            if aip_id in aips:
                raise SystemExit(f"duplicate AIP id {aip_id}")
            aips[aip_id] = Doc(
                src=os.path.join(sdir, name),
                out=out,
                title=title,
                body=body,
                aip_id=aip_id,
                scope=scope,
                meta=dict(
                    url=url,
                    scope_title=scope_title,
                    scope_hidden=scope_hidden,
                    category=category,
                    category_title=cat_title,
                    state=fm_value(fm, "state"),
                    created=fm_value(fm, "created"),
                    updated=fm_value(fm, "updated"),
                    redirect_from=fm_list(fm, "redirect_from"),
                ),
            )
    return aips


SITE_PAGES = [
    # (source path relative to upstream root, output name, site URL)
    ("pages/general/faq.md", "site/faq.md", f"{SITE}/faq"),
    ("pages/general/adopting.md", "site/adopting.md", f"{SITE}/adopting"),
    ("pages/general/licensing.md", "site/licensing.md", f"{SITE}/licensing"),
    ("CONTRIBUTING.md", "site/contributing.md", f"{SITE}/contributing"),
]


def load_pages(src_root: str) -> list[Doc]:
    docs = []
    for rel, out, url in SITE_PAGES:
        text = open(os.path.join(src_root, rel)).read()
        _, body = parse_front_matter(text)
        m = re.match(r"\s*# (.+)\n", body)
        title = m.group(1).strip()
        body = body[m.end():]
        footer = ""
        yaml_path = os.path.join(src_root, rel[:-3] + ".yaml")
        if os.path.exists(yaml_path):
            y = open(yaml_path).read()
            fm = re.search(r"^footer: \|\n((?:  .*\n|\n)*)", y, re.M)
            if fm:
                footer = "\n".join(l[2:] for l in fm.group(1).splitlines()).strip()
        if footer:
            body = body.rstrip("\n") + "\n\n---\n\n" + footer + "\n"
        docs.append(Doc(src=rel, out=out, title=title, body=body, meta=dict(url=url)))
    return docs


def load_news(src_root: str) -> Doc:
    """Concatenate the AIP newsletter archive (newest first), as /news renders it."""
    ndir = os.path.join(src_root, "pages", "news")
    codes = sorted({n[:-3] for n in os.listdir(ndir) if n.endswith(".md")}, reverse=True)
    parts = [
        "Want to keep up with the AIP system, and what we are working on? Welcome to the\n"
        "**AIP newsletter**, a monthly publication covering new AIP guidance, and any\n"
        "other developments useful to API producers.\n",
        "> **Note (skill packaging):** The newsletter is a historical archive. The\n"
        "> AIP documents themselves are authoritative; where a newsletter describes\n"
        "> guidance that was later changed, follow the current AIP.\n",
    ]
    for code in codes:
        md = open(os.path.join(ndir, code + ".md")).read()
        y = open(os.path.join(ndir, code + ".yaml")).read()
        _, md = parse_front_matter(md)
        m = re.match(r"\s*# (.+)\n", md)
        ntitle, md = m.group(1).strip(), md[m.end():]
        month, year = fm_value(y, "month"), fm_value(y, "year")
        reviewing = fm_value(y, "reviewing")
        others = fm_list(y, "  other") or re.findall(r"^    - (.*)$", y, re.M)
        parts.append(f"## {month} {year}: {ntitle}\n")
        parts.append(f"> Source: <{SITE}/news/{code}>\n")
        if reviewing or others:
            hl = ["Highlights:"]
            if reviewing:
                nums = [x.strip() for x in reviewing.strip("[]").split(",") if x.strip()]
                hl.append("- Reviewing: " + ", ".join(f"[AIP-{n}](/{n})" for n in nums))
            for o in others:
                hl.append(f"- {o}")
            parts.append("\n".join(hl) + "\n")
        # Demote the newsletter's own headings by one level so they nest.
        md = re.sub(r"^(#+) ", lambda mm: "#" + mm.group(1) + " ", md, flags=re.M)
        parts.append(md.strip() + "\n")
    return Doc(src="pages/news", out="site/news.md", title="News (AIP newsletter archive)",
               body="\n".join(parts), meta=dict(url=f"{SITE}/news"))


class LinkError(Exception):
    pass


def resolve(target: str, doc: Doc, aips: dict[int, Doc]) -> str | None:
    """Return the rewritten target, or None to leave the target unchanged."""
    path, sep, anchor = target.partition("#")
    frag = sep + anchor
    here = os.path.dirname(doc.out)

    def rel(out: str) -> str:
        return os.path.relpath(out, here) + frag

    def aip(n: int) -> str:
        if doc.aip_id is not None and (doc.aip_id, path) in LINK_FIXES:
            n = LINK_FIXES[(doc.aip_id, path)]
        if n not in aips:
            raise LinkError(f"{doc.out}: link to unknown AIP-{n} ({target})")
        return rel(aips[n].out)

    if path == "":
        return None  # same-page anchor
    if re.match(r"^(mailto:|https?://(?!(google\.)?aip\.dev))", path):
        return None  # external
    m = re.match(r"^https?://(?:google\.)?aip\.dev/(?:[a-z-]+/)?0*(\d+)/?$", path)
    if m:
        return aip(int(m.group(1)))
    if re.match(r"^https?://(?:google\.)?aip\.dev/(general)?/?$", path):
        return rel("INDEX.md")
    if path == "/":
        return rel("INDEX.md")
    m = re.match(r"^/0*(\d+)$", path)
    if m:
        return aip(int(m.group(1)))
    if path == "/assets/misc/ebnf-filtering.txt":
        return rel("assets/ebnf-filtering.txt")
    if path.startswith("/sdk/"):
        return "https://cloud.google.com" + path + frag
    if path in ("./licensing.md", "licensing.md"):
        return rel("site/licensing.md")
    m = re.match(r"^(?:\.\./|\./)?(?:[a-z-]+/)?0*(\d+)(?:\.md)?$", path)
    if m:
        return aip(int(m.group(1)))
    raise LinkError(f"{doc.out}: unresolvable relative link {target!r}")


def rewrite_links(doc: Doc, aips: dict[int, Doc], errors: list[str]) -> str:
    out_lines = []
    in_fence = False
    for line in doc.body.splitlines(keepends=True):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        if re.match(r"^\s*<!-- prettier-ignore-(start|end) -->\s*$", line):
            continue

        def sub_def(m):
            try:
                new = resolve(m.group(2), doc, aips)
            except LinkError as e:
                errors.append(str(e))
                return m.group(0)
            return m.group(0) if new is None else f"{m.group(1)}{new}{m.group(3)}"

        def sub_inline(m):
            try:
                new = resolve(m.group(2), doc, aips)
            except LinkError as e:
                errors.append(str(e))
                return m.group(0)
            return m.group(0) if new is None else f"{m.group(1)}{new}{m.group(3)}"

        line = re.sub(r"^(\s*\[[^\]]+\]:\s*)(\S+)(.*)$", sub_def, line, flags=re.S)
        # Rewrite inline links only outside of inline code spans.
        pieces = re.split(r"(`+[^`]*`+)", line)
        for i in range(0, len(pieces), 2):
            pieces[i] = re.sub(r"(\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))", sub_inline, pieces[i])
        out_lines.append("".join(pieces))
    return "".join(out_lines)


def header_for(doc: Doc) -> str:
    m = doc.meta
    if doc.aip_id is None:
        return f"# {doc.title}\n\n> Source: <{m['url']}>\n"
    fields = [f"**Source:** <{m['url']}>", f"**Scope:** {m['scope_title']}"]
    if m["category_title"]:
        fields.append(f"**Category:** {m['category_title']}")
    fields.append(f"**State:** {m['state']}")
    if m["created"]:
        fields.append(f"**Created:** {m['created']}")
    if m["updated"]:
        fields.append(f"**Updated:** {m['updated']}")
    if m["redirect_from"]:
        fields.append("**Also reachable at:** " + ", ".join(f"`{r}`" for r in m["redirect_from"]))
    lines = [f"# AIP-{doc.aip_id}: {doc.title}", "", "> " + " · ".join(fields)]
    if m["state"] != "approved":
        lines += [
            ">",
            f"> **Note (skill packaging):** this AIP is in the `{m['state']}` state, not",
            "> `approved`. See AIP-1 (\"States\") for what that means before relying on it.",
        ]
    return "\n".join(lines) + "\n"


def render_index(aips: dict[int, Doc], upstream_rev: str) -> str:
    lines = [
        "# AIP index",
        "",
        f"Complete catalog of every AIP published at <{SITE}>, generated from upstream",
        f"revision `{upstream_rev}` of <https://github.com/aip-dev/google.aip.dev>.",
        "Each link opens the full, verbatim text of that AIP.",
        "",
        "States: `approved` = in effect; `reviewing` / `draft` = not yet approved",
        "(see [AIP-1](" + aips[1].out + ")).",
        "",
    ]
    scopes: dict[str, list[Doc]] = {}
    for d in aips.values():
        scopes.setdefault(d.scope, []).append(d)
    order = ["general", "cloud", "auth", "client-libraries", "firebase", "apps", "aog"]
    for scope in order:
        docs = sorted(scopes.pop(scope), key=lambda d: d.aip_id)
        st = docs[0].meta["scope_title"]
        hidden = " (hidden from the site navigation; reachable by direct URL)" if docs[0].meta["scope_hidden"] else ""
        url = f"{SITE}/general" if scope == "general" else f"{SITE}/{scope}"
        lines += [f"## {st}{hidden}", "", f"Site listing: <{url}>", ""]
        cats: dict[str, list[Doc]] = {}
        for d in docs:
            cats.setdefault(d.meta["category_title"], []).append(d)
        if scope == "general":
            cat_order = [GENERAL_CATEGORY_TITLES[k] for k in GENERAL_CATEGORY_TITLES]
        elif scope == "cloud":
            cat_order = list(CLOUD_CATEGORY_TITLES.values())
        else:
            cat_order = [""]
        for ct in cat_order:
            if ct not in cats:
                continue
            if ct:
                lines += [f"### {ct}", ""]
            lines += ["| AIP | Title | State | File |", "|---|---|---|---|"]
            for d in cats.pop(ct):
                lines.append(
                    f"| AIP-{d.aip_id} | {d.title} | {d.meta['state']} | [{os.path.basename(d.out)}]({d.out}) |"
                )
            lines.append("")
        if cats:
            raise SystemExit(f"uncategorised AIPs in {scope}: {list(cats)}")
    if scopes:
        raise SystemExit(f"unknown scopes: {list(scopes)}")
    lines += [
        "## Site pages",
        "",
        "| Page | File |",
        "|---|---|",
        "| Frequently asked questions | [site/faq.md](site/faq.md) |",
        "| Adopting AIPs in your company (the 9000 block) | [site/adopting.md](site/adopting.md) |",
        "| Content licensing | [site/licensing.md](site/licensing.md) |",
        "| Contributing | [site/contributing.md](site/contributing.md) |",
        "| News (AIP newsletter archive) | [site/news.md](site/news.md) |",
        "| AIP-160 filtering EBNF grammar | [assets/ebnf-filtering.txt](assets/ebnf-filtering.txt) |",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    src_root, ebnf = sys.argv[1], sys.argv[2]
    try:
        rev = subprocess.check_output(["git", "-C", src_root, "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        rev = "unknown"

    aips = load_aips(src_root)
    docs = list(aips.values()) + load_pages(src_root) + [load_news(src_root)]

    if os.path.isdir(REF_DIR):
        shutil.rmtree(REF_DIR)
    errors: list[str] = []
    for d in docs:
        body = rewrite_links(d, aips, errors)
        text = header_for(d) + "\n" + body.lstrip("\n")
        path = os.path.join(REF_DIR, d.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text.rstrip("\n") + "\n")
    os.makedirs(os.path.join(REF_DIR, "assets"), exist_ok=True)
    shutil.copyfile(ebnf, os.path.join(REF_DIR, "assets", "ebnf-filtering.txt"))
    with open(os.path.join(REF_DIR, "INDEX.md"), "w") as f:
        f.write(render_index(aips, rev))
    with open(os.path.join(REF_DIR, "UPSTREAM_REVISION"), "w") as f:
        f.write(rev + "\n")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"wrote {len(aips)} AIPs and {len(docs) - len(aips)} site pages from {rev}")


if __name__ == "__main__":
    main()
