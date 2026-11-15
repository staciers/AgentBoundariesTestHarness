"""Build the arXiv source bundle: the paper and supplement as one document.

    python3 paper/latex/make_arxiv.py        (from the repo root)

Writes paper/arxiv/source/ (a flat copy that builds on its own) and paper/arxiv/arxiv-source.tar.gz
(the upload). arXiv compiles the LaTeX itself, so the bundle holds main.tex, the bibliography
already processed (main.bbl, which arXiv uses instead of running BibTeX), the style file and the
figures, with figure paths rewritten to figures/ (arXiv rejects paths outside the bundle).
The bundle is test-built with Tectonic; arXiv builds with pdfLaTeX, whose line breaks can differ
slightly.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tarfile

sys.path.insert(0, os.path.dirname(__file__))
import md2tex  # noqa: E402

OUT = "paper/arxiv"
SRC = os.path.join(OUT, "source")
TECTONIC = os.path.expanduser("~/.local/bin/tectonic")


def main() -> None:
    with open("paper/full.md") as f, open("paper/supplements.md") as g:
        tex = md2tex.convert(f.read(), anonymous=False, supplement=g.read())

    if os.path.isdir(SRC):
        shutil.rmtree(SRC)
    os.makedirs(os.path.join(SRC, "figures"))

    # Copy each figure into figures/ and point \includegraphics at the copy.
    def relocate(m: re.Match) -> str:
        path = os.path.normpath(os.path.join("paper/latex", m.group(2)))
        shutil.copy(path, os.path.join(SRC, "figures", os.path.basename(path)))
        return m.group(1) + "figures/" + os.path.basename(path) + "}"

    tex = re.sub(r"(\\includegraphics\[[^\]]*\]\{)([^}]+)\}", relocate, tex)
    tex = tex.replace("% Generated from paper/full.md by paper/latex/md2tex.py. Edit the draft and regenerate,\n"
                      "% or stop regenerating and edit this file directly once the draft is frozen.\n", "")
    with open(os.path.join(SRC, "main.tex"), "w") as f:
        f.write(tex)
    for name in ("usenix2019_v3.sty", "references.bib"):
        shutil.copy(os.path.join("paper/latex", name), SRC)

    # Test build; keep the .bbl for arXiv.
    build = os.path.join(OUT, "build")
    if os.path.isdir(build):
        shutil.rmtree(build)
    os.makedirs(build)
    r = subprocess.run([TECTONIC, "-k", "-o", os.path.abspath(build), "main.tex"], cwd=SRC,
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-3000:])
    for line in r.stderr.splitlines():
        if re.search(r"error|overfull|undefined", line, re.I):
            print(line)
    shutil.copy(os.path.join(build, "main.bbl"), SRC)
    shutil.copy(os.path.join(build, "main.pdf"), os.path.join(OUT, "arxiv-preview.pdf"))

    tar = os.path.join(OUT, "arxiv-source.tar.gz")
    with tarfile.open(tar, "w:gz") as t:
        for root, _, files in os.walk(SRC):
            for name in sorted(files):
                full = os.path.join(root, name)
                t.add(full, arcname=os.path.relpath(full, SRC))
    names = sorted(tarfile.open(tar).getnames())
    print(f"wrote {tar} ({os.path.getsize(tar) / 1e6:.1f} MB, {len(names)} files) and "
          f"{os.path.join(OUT, 'arxiv-preview.pdf')}")
    print("\n".join("  " + n for n in names))


if __name__ == "__main__":
    main()
