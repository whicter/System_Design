"""Build this repo as a MkDocs Material site.

Copies the Markdown into _site_src/, turns SUMMARY.md into the sidebar
navigation, strips hand-written tables of contents (the site has its own),
and runs `mkdocs build` into site/. Used by .github/workflows/pages.yml.

SUMMARY.md format (GitBook-compatible):
  ## Section                 -> top-level sidebar section
  * [Title](path.md)         -> page
    * [Child](child.md)      -> nested under the page above (2-space indent)
  * Group name               -> a group without its own page
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse

SRC = "_site_src"
INDEX = "__index__"
SKIP = {".git", ".github", SRC, "site", "mkdocs.yml", "_mkdocs.yml"}
MATHJAX = """window.MathJax = {
  tex: {inlineMath: [["\\\\(", "\\\\)"]], displayMath: [["\\\\[", "\\\\]"]], processEscapes: true, processEnvironments: true},
  options: {ignoreHtmlClass: ".*|", processHtmlClass: "arithmatex"}
};
document$.subscribe(() => {
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
"""
TOC_TITLE = re.compile(r'^\s*(#{1,6}\s*)?(\*\*)?\s*目录\s*(\*\*)?\s*(<a id="[^"]*"></a>)?\s*(\[↑[^\]]*\]\(#[^)]*\))?\s*$')
TOC_ITEM = re.compile(r'^\s*([-*+]|\d+\.)\s+\[[^\]]*\]\(#[^)]*\)\s*$')
BACKLINK = re.compile(r'\s*\[↑\s*目录\]\(#[^)]*\)')


def strip_manual_toc(text):
    """Remove '目录' blocks made only of in-page anchor links, and '↑ 目录' backlinks."""
    lines = text.split("\n")
    out, i, in_code = [], 0, False
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and TOC_TITLE.match(line):
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            k = j
            while k < len(lines) and (TOC_ITEM.match(lines[k]) or not lines[k].strip()):
                k += 1
            if k > j and all(TOC_ITEM.match(l) or not l.strip() for l in lines[j:k]):
                i = k
                continue
        out.append(line if in_code else BACKLINK.sub("", line))
        i += 1
    return "\n".join(out)


def nest_extra_h1(text):
    """If a page has several '# ' headings, keep the first as the title and
    push every later heading one level down so the outline nests under it."""
    lines = text.split("\n")
    in_code, count = False, 0
    for line in lines:
        if line.lstrip().startswith("```"):
            in_code = not in_code
        elif not in_code and re.match(r'^# ', line):
            count += 1
    if count < 2:
        return text
    in_code, h1_seen = False, False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r'^(#{1,6}) ', line)
        if not m:
            continue
        if len(m.group(1)) == 1 and not h1_seen:
            h1_seen = True
            continue
        if h1_seen and len(m.group(1)) < 6:
            lines[i] = "#" + line
    return "\n".join(lines)


def copy_sources():
    shutil.rmtree(SRC, ignore_errors=True)
    os.makedirs(SRC)
    for name in os.listdir("."):
        if name in SKIP or name.startswith("._") or name == ".DS_Store":
            continue
        if os.path.isdir(name):
            shutil.copytree(name, os.path.join(SRC, name),
                            ignore=shutil.ignore_patterns("._*", ".DS_Store"))
        else:
            shutil.copy2(name, os.path.join(SRC, name))
    for root, _, files in os.walk(SRC):
        for f in files:
            if f.endswith(".md"):
                p = os.path.join(root, f)
                with open(p, encoding="utf-8") as fh:
                    text = fh.read()
                new = nest_extra_h1(strip_manual_toc(text))
                if new != text:
                    with open(p, "w", encoding="utf-8") as fh:
                        fh.write(new)
    os.makedirs(os.path.join(SRC, "javascripts"), exist_ok=True)
    with open(os.path.join(SRC, "javascripts", "mathjax.js"), "w", encoding="utf-8") as f:
        f.write(MATHJAX)


def parse_summary():
    """SUMMARY.md -> MkDocs nav."""
    if not os.path.exists("SUMMARY.md"):
        return None
    nav, section, stack = [], None, []
    link_item = re.compile(r'^(\s*)[*-]\s+\[(.+)\]\(([^)]+)\)\s*$')
    group_item = re.compile(r'^(\s*)[*-]\s+([^\[\s].*?)\s*$')
    for line in open("SUMMARY.md", encoding="utf-8"):
        heading = re.match(r'^#{2,3}\s+(.+)$', line)
        if heading:
            section = []
            nav.append({heading.group(1).strip(): section})
            stack = []
            continue
        m = link_item.match(line)
        g = None if m else group_item.match(line)
        if not m and not g:
            continue
        indent = len((m or g).group(1).replace("\t", "    "))
        title = re.sub(r"\\(.)", r"\1", (m or g).group(2)).strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1] if stack else (section if section is not None else nav)
        children = []
        if m:
            path = urllib.parse.unquote(m.group(3).split("#")[0])
            if not os.path.exists(path):
                continue
            children.append({INDEX: path})
        parent.append({title: children})
        stack.append((indent, children))

    def tidy(entries):
        out = []
        for entry in entries:
            (title, value), = entry.items()
            if isinstance(value, list):
                value = tidy(value)
                if not value:
                    continue
                if len(value) == 1 and isinstance(list(value[0].values())[0], str):
                    out.append({title: list(value[0].values())[0]})
                    continue

            out.append({title: value})
        return out
    return tidy(nav)


LINK = re.compile(r'(!?\[[^\]]*\]\()([^)\s]+)(\))')


def promote_indexes(nav):
    """A page that has children becomes the section's index page (no duplicate entry)."""
    moves = {}

    def walk(entries):
        for entry in entries:
            (title, value), = entry.items()
            if not isinstance(value, list):
                continue
            first = value[0] if value else None
            if first and INDEX in first:
                old = first[INDEX]
                base = os.path.basename(old).lower()
                if base in ("readme.md", "index.md"):
                    new = old
                else:
                    new = os.path.join(os.path.splitext(old)[0], "index.md")
                    if os.path.exists(os.path.join(SRC, new)) or old in moves:
                        new = old
                if new != old:
                    moves[old] = new
                value[0] = {title: new}
            walk(value)
    walk(nav)
    if not moves:
        return nav
    for old, new in moves.items():
        src_path, dst_path = os.path.join(SRC, old), os.path.join(SRC, new)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.move(src_path, dst_path)
    rev = {v: k for k, v in moves.items()}
    for root, _, files in os.walk(SRC):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel_now = os.path.relpath(path, SRC)
            rel_before = rev.get(rel_now, rel_now)
            dir_before, dir_now = os.path.dirname(rel_before), os.path.dirname(rel_now)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            parts = re.split(r'(```.*?```)', text, flags=re.S)

            def fix(match):
                target = match.group(2)
                if re.match(r'^[a-z]+:|^#|^/', target):
                    return match.group(0)
                file_part, sep, anchor = target.partition("#")
                resolved = os.path.normpath(os.path.join(dir_before, urllib.parse.unquote(file_part)))
                resolved = moves.get(resolved, resolved)
                new_rel = os.path.relpath(resolved, dir_now or ".")
                if new_rel == os.path.normpath(urllib.parse.unquote(file_part)) and dir_before == dir_now:
                    return match.group(0)
                return match.group(1) + urllib.parse.quote(new_rel) + (sep + anchor) + match.group(3)
            for i in range(0, len(parts), 2):
                parts[i] = LINK.sub(fix, parts[i])
            new_text = "".join(parts)
            if new_text != text:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new_text)
    return nav


def main():
    copy_sources()
    nav = parse_summary()
    if nav:
        nav = promote_indexes(nav)
    lines = ["INHERIT: mkdocs.yml", f"docs_dir: {SRC}"]
    if nav:
        lines.append("nav: " + json.dumps(nav, ensure_ascii=False))
    with open("_mkdocs.yml", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    sys.exit(subprocess.call(["mkdocs", "build", "-f", "_mkdocs.yml", "-d", "site"]))


if __name__ == "__main__":
    main()
