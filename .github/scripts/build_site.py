"""Build this repo as a MkDocs Material site.

Copies the Markdown into _site_src/, turns SUMMARY.md into the navigation,
and runs `mkdocs build` into site/. Used by .github/workflows/pages.yml.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse

SRC = "_site_src"
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
    os.makedirs(os.path.join(SRC, "javascripts"), exist_ok=True)
    with open(os.path.join(SRC, "javascripts", "mathjax.js"), "w", encoding="utf-8") as f:
        f.write(MATHJAX)


def parse_summary():
    """SUMMARY.md (GitBook format) -> MkDocs nav."""
    if not os.path.exists("SUMMARY.md"):
        return None
    nav = []
    section = None
    stack = []  # (indent, children list)
    item = re.compile(r'^(\s*)[*-]\s+\[(.+)\]\(([^)]+)\)\s*$')
    for line in open("SUMMARY.md", encoding="utf-8"):
        heading = re.match(r'^#{2,3}\s+(.+)$', line)
        if heading:
            section = []
            nav.append({heading.group(1).strip(): section})
            stack = []
            continue
        m = item.match(line)
        if not m:
            continue
        indent = len(m.group(1).replace("\t", "    "))
        title = re.sub(r"\\(.)", r"\1", m.group(2)).strip()
        path = urllib.parse.unquote(m.group(3).split("#")[0])
        if not os.path.exists(path):
            continue
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1] if stack else (section if section is not None else nav)
        children = [{title: path}]
        parent.append({title: children})
        stack.append((indent, children))
    # collapse groups that ended up with a single page
    def tidy(entries):
        out = []
        for entry in entries:
            (title, value), = entry.items()
            if isinstance(value, list):
                value = tidy(value)
                if len(value) == 1 and isinstance(list(value[0].values())[0], str):
                    out.append(value[0])
                    continue
            out.append({title: value})
        return out
    return tidy(nav)


def main():
    copy_sources()
    nav = parse_summary()
    lines = ["INHERIT: mkdocs.yml", f"docs_dir: {SRC}"]
    if nav:
        lines.append("nav: " + json.dumps(nav, ensure_ascii=False))
    with open("_mkdocs.yml", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    sys.exit(subprocess.call(["mkdocs", "build", "-f", "_mkdocs.yml", "-d", "site"]))


if __name__ == "__main__":
    main()
