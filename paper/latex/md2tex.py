"""Convert the paper draft (Markdown) to LaTeX for the USENIX template.

    python3 paper/latex/md2tex.py [paper/full.md] [paper/latex/main.tex] [--anonymous]
                                  [--supplement[=paper/supplements.md]] [--repo-url=URL]

--repo-url replaces every link to the project's GitHub repository with URL (for the OSDI version,
an anonymized link such as https://anonymous.4open.science/r/<id>). With --anonymous, the build
fails if the output still contains anything that identifies the author (name, GitHub user,
repository name, email), so a missed link can't slip into a double-blind submission.

--supplement appends the supplement (S1, S2, ...) after the references as one-column
appendices, so the paper and supplement build as a single PDF (the arXiv version). In it,
"Supplement S1", "Figure S1" and "Table S1" become links, and figures and tables are numbered
S1, S2, ... as in the Markdown.

An "Author: Name" line under the title sets the author (one line per author); --anonymous
replaces it with "Anonymous submission" for double-blind venues.

Handles the subset of Markdown the draft uses: headings, paragraphs, bullet and numbered
lists (nested by indentation), tables, code blocks, block quotes, figures with a following
"**Figure N.**" caption, tables with a "**Table N.**" caption before or after them, inline
bold/italic/code, links (kept as text), citations such as "[Lee et al. 2015; Jena and Dalal
2025]" (mapped to BibTeX keys in references.bib), section references such as "§4.3",
footnotes ("text.[^name]" with a "[^name]: note" line anywhere in the file; indented lines
continue the note), and "[TODO]" markers (shown in red). Paragraphs between the title and the
abstract (e.g. a disclosure note) are kept, under the title. The draft's own reference list is
replaced by BibTeX.

Figures and tables keep labels based on their number in the draft (fig:o2, tab:oA1), and
LaTeX renumbers them in the order they appear.
"""
from __future__ import annotations

import re
import sys

CITES = {
    "Anthropic 2026a": "anthropic2026automode", "PagerDuty 2021": "pagerduty2021digitalops",
    "VOID 2022": "verica2022void", "Anthropic 2026b": "anthropic2026unintended",
    "Anthropic 2026c": "anthropic2026evals", "Bailis et al. 2012": "bailis2012pbs",
    "Birrell and Nelson 1984": "birrell1984rpc", "Burckhardt et al. 2021": "burckhardt2021durable",
    "Chaudhry et al. 2026": "chaudhry2026murakkab", "Chow 1970": "chow1970reject",
    "Cutler et al. 2024": "cutler2024cedar", "Ferreira et al. 2026": "ferreira2026aletheia",
    "Fischer et al. 1985": "fischer1985flp", "Garcia-Molina and Salem 1987": "garciamolina1987sagas",
    "Geifman and El-Yaniv 2017": "geifman2017selective", "Gray and Cheriton 1989": "gray1989leases",
    "Gray and Reuter 1993": "gray1993transaction", "Horvitz 1999a": "horvitz1999principles",
    "Horvitz 1999b": "horvitz1999uncertainty", "Jena and Dalal 2025": "jena2025idempotency",
    "Kadavath et al. 2022": "kadavath2022know", "Kim et al. 2025": "kim2025scaling", "South et al. 2025": "south2025delegation",
    "Kleppmann 2017": "kleppmann2017ddia", "Lamport 1978": "lamport1978clocks",
    "LeBlanc et al. 2025": "leblanc2025power", "Lee et al. 2015": "lee2015rifl",
    "Li et al. 2026": "li2026dse", "Lou et al. 2025": "lou2025t2c", "MCP": "mcp",
    "Madras et al. 2018": "madras2018defer", "OpenAI 2026a": "openai2026coding",
    "OpenAI 2026b": "openai2026longhorizon", "Qi et al. 2023": "qi2023halfmoon",
    "Ren et al. 2023": "ren2023knowno", "Ruan et al. 2024": "ruan2024toolemu",
    "Scerri et al. 2002": "scerri2002adjustable", "Schick et al. 2023": "schick2023toolformer",
    "Sclar et al. 2024": "sclar2024formatting", "Setty et al. 2016": "setty2016olive",
    "Stripe": "stripe", "Temporal": "temporal", "Terry et al. 1994": "terry1994session",
    "Trivedi et al. 2024": "trivedi2024appworld", "Xie et al. 2026": "xie2026incr",
    "Xiong et al. 2024": "xiong2024uncertainty", "Yao et al. 2025": "yao2025taubench",
    "Yao et al. 2023": "yao2023react", "Zhang et al. 2020": "zhang2020beldi",
    "Zhou et al. 2024": "zhou2024webarena",
}
WIDE_FIGURES = {"1", "3", "4", "5", "6", "7", "A1"}
UNICODE = {"±": r"$\pm$", "²": r"$^2$", "×": r"$\times$", "τ": r"$\tau$", "–": "--", "—": "---",
           "−": r"$-$", "→": r"$\rightarrow$", "↳": r"$\hookrightarrow$", "·": r"$\cdot$", "≥": r"$\geq$",
           "≤": r"$\leq$", "…": r"\ldots{}", "§": r"\S{}", "é": r"\'e", "’": "'", "‘": "`", "“": "``", "”": "''", "ã": r"\~a",
           "÷": r"$\div$", "Σ": r"$\Sigma$", "≈": r"$\approx$", "⁻¹⁶": r"$^{-16}$"}

REPO_URL = "https://github.com/staciers/AgentBoundariesTestHarness"
# Strings that identify the author; an --anonymous build containing any of them is refused.
IDENTIFYING = ("staciers", "AgentBoundariesTestHarness", "Stacie", "Riddle", "histacie")

labels: set = set()
with_supplement = False  # set by convert(); turns "Figure S1" etc. into links
footnotes: dict = {}  # name -> Markdown text of the note, collected before conversion
FOOTNOTE_DEF = re.compile(r"^\[\^([\w-]+)\]:\s*(.*)$")


def escape(t: str) -> str:
    t = t.replace("\\", r"\textbackslash{}")
    for a, b in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")):
        t = t.replace(a, b)
    return t


def code(t: str) -> str:
    out = escape(t)
    for a, b in UNICODE.items():
        out = out.replace(a, b)
    return r"\texttt{" + out + "}"


def cite(m: re.Match) -> str:
    parts = [p.strip() for p in re.sub(r"\s+", " ", m.group(1)).split(";")]
    if all(p in CITES for p in parts):
        return "~\\cite{" + ",".join(CITES[p] for p in parts) + "}"
    return m.group(0)


def cite_with_space(m: re.Match) -> str:
    """A citation absorbs the space before it (it carries its own tie)."""
    inner = re.match(r"\s*(\[.*\])$", m.group(0), re.S).group(1)
    c = cite(re.match(r"\[([^\]]+)\]", inner))
    return c if c != inner else m.group(0)


def section_ref(m: re.Match) -> str:
    num, trail = m.group(1), (m.group(2) or "").replace("–", "--")
    if num in labels:
        return r"\S\ref{sec:" + num + "}" + trail
    return r"\S{}" + num + trail


def footnote(name: str) -> str:
    if name not in footnotes:
        print(f"warning: footnote [^{name}] has no definition", file=sys.stderr)
        return r"\todo{}"
    return r"\footnote{" + inline(footnotes[name]) + "}"


def collect_footnotes(lines):
    """Remove "[^name]: text" definitions (and their indented continuation lines) from the
    document and store them; the reference "[^name]" becomes a \\footnote where it appears."""
    footnotes.clear()
    kept, k = [], 0
    while k < len(lines):
        m = FOOTNOTE_DEF.match(lines[k])
        if not m:
            kept.append(lines[k])
            k += 1
            continue
        text = [m.group(2)]
        k += 1
        while k < len(lines) and lines[k].startswith(("    ", "\t")) and lines[k].strip():
            text.append(lines[k].strip())
            k += 1
        footnotes[m.group(1)] = " ".join(text)
    return kept


def inline(t: str) -> str:
    """Markdown inline text to LaTeX."""
    t = re.sub(r"\s+", " ", t).strip()
    spans = []

    def keep(s: str) -> str:
        spans.append(s)
        return f"\x00{len(spans) - 1}\x00"

    t = re.sub(r"\[\^([\w-]+)\]", lambda m: keep(footnote(m.group(1))), t)
    t = re.sub(r"`([^`]+)`", lambda m: keep(code(m.group(1))), t)
    t = re.sub(r"\*\*\[TODO\]\*\*", lambda m: keep(r"\todo{}"), t)
    t = re.sub(r"\[TODO\]", lambda m: keep(r"\todo{}"), t)
    t = re.sub(r"\s?\[([^\]]+)\](?!\()",
               lambda m: keep(cite_with_space(m)) if cite_with_space(m) != m.group(0) else m.group(0), t)
    t = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", t)  # links: keep the text
    t = re.sub(r"https?://[^\s)\]]*[^\s)\].,;:]", lambda m: keep(r"\url{" + m.group(0) + "}"), t)  # bare URLs
    t = re.sub(r"\(\*\*Fig\. (\d+|A1)([a-c]?)\*\*\)|\*\*\(Fig\. (\d+|A1)([a-c]?)\)\*\*",
               lambda m: keep(f"(Fig.~\\ref{{fig:o{m.group(1) or m.group(3)}}}{m.group(2) or m.group(4) or ''})"), t)
    t = re.sub(r"\*\*\((Table) (\w+)\)\*\*", lambda m: keep(f"(Table~\\ref{{tab:o{m.group(2)}}})"), t)
    t = re.sub(r"\bFig\. (\d+|A1)([a-c]?)", lambda m: keep(f"Fig.~\\ref{{fig:o{m.group(1)}}}{m.group(2)}"), t)
    t = re.sub(r"\bFigure (\d+|A1)\b", lambda m: keep(f"Figure~\\ref{{fig:o{m.group(1)}}}"), t)
    t = re.sub(r"\bTable (\d+|A1)\b", lambda m: keep(f"Table~\\ref{{tab:o{m.group(1)}}}"), t)
    t = re.sub(r"\bAppendix A\b", lambda m: keep(r"Appendix~\ref{sec:A}"), t)
    if with_supplement:
        t = re.sub(r"\b(Figure|Table) (S\d+)\b",
                   lambda m: keep(f"{m.group(1)}~\\ref{{{'fig' if m.group(1) == 'Figure' else 'tab'}:o{m.group(2)}}}"), t)
        t = re.sub(r"\bSupplement (S\d+)\b", lambda m: keep(f"Supplement~\\ref{{sec:{m.group(1)}}}"), t)
    t = re.sub(r"§(\d+(?:\.\d+)?)(–\d+)?", lambda m: keep(section_ref(m)), t)
    t = escape(t)
    for a, b in UNICODE.items():
        t = t.replace(a, b)
    t = re.sub(r'"([^"]*)"', r"``\1''", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\\emph{\1}", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], t)
    return t


# ----------------------------------------------------------------------------- tables
def table_rows(lines):
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows


def render_table(lines, caption=None, label=None, appendix=False):
    rows = table_rows(lines)
    ncol = len(rows[0])
    width = [max(len(r[i]) if i < len(r) else 0 for r in rows) for i in range(ncol)]
    wide = ncol >= 5 or sum(width) > 90
    spec = "".join("X" if w > 22 else "l" for w in width)
    if not wide:
        # In a single column, long headers over short values need to wrap, so make those columns X.
        spec = "".join("X" if len(rows[0][i]) > 12 else c for i, c in enumerate(spec))
    if "X" not in spec:
        spec = "l" * (ncol - 1) + "X"
    head = " & ".join(r"\textbf{" + inline(c) + "}" for c in rows[0]) + r" \\"
    body = "\n".join(" & ".join(inline(c) for c in (r + [""] * (ncol - len(r)))[:ncol]) + r" \\" for r in rows[1:])
    cap = ""
    if caption:
        cap = r"\caption{" + caption + "}" + (r"\label{" + label + "}" if label else "")
    if appendix:
        avg = [sum(len(r[i]) for r in rows if i < len(r)) / len(rows) for i in range(ncol)]
        # Each column is at least as wide as its longest word, then the rest is shared by content.
        words = [max(len(w) for r in rows if i < len(r) for w in (r[i].split() or [""])) for i in range(ncol)]
        minw = [max(0.035, 0.0075 * w) for w in words]
        # Leave room for the 2*\tabcolsep (12pt of the 504pt text width) around every column.
        budget = 0.99 - ncol * 12 / 504
        frac = [a / sum(avg) * budget for a in avg]
        fixed = [f < m for f, m in zip(frac, minw)]
        rest = budget - sum(m for m, x in zip(minw, fixed) if x)
        share = sum(a for a, x in zip(avg, fixed) if not x)
        frac = [m if x else rest * a / share for m, x, a in zip(minw, fixed, avg)]
        spec_long = "".join(r">{\raggedright\arraybackslash}p{%.3f\textwidth}" % f for f in frac)
        # The full caption and header on the first page; a short "(continued)" header after that.
        cont = r"\caption[]{(continued)} \\" if cap else ""
        return "\n".join([r"{\scriptsize", r"\begin{longtable}{" + spec_long + "}",
                          (cap + r" \\") if cap else "", r"\toprule", head, r"\midrule\endfirsthead",
                          cont, r"\toprule", head, r"\midrule\endhead", body,
                          r"\bottomrule", r"\end{longtable}}", ""])
    env = "table*" if wide else "table"
    w = r"\textwidth" if wide else r"\columnwidth"
    return "\n".join([r"\begin{" + env + "}[t]", r"\centering", r"\footnotesize",
                      r"\begin{tabularx}{" + w + "}{" + spec + "}", r"\toprule", head, r"\midrule", body,
                      r"\bottomrule", r"\end{tabularx}", cap, r"\end{" + env + "}", ""])


# ----------------------------------------------------------------------------- lists
def render_list(lines):
    out, stack = [], []
    item = None

    def flush():
        nonlocal item
        if item is not None:
            out.append(r"\item " + inline(" ".join(item)))
            item = None

    for ln in lines:
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", ln)
        if m:
            flush()
            ind, kind = len(m.group(1)), ("enumerate" if m.group(2)[0].isdigit() else "itemize")
            while stack and stack[-1][0] > ind:
                out.append(r"\end{" + stack.pop()[1] + "}")
            if not stack or stack[-1][0] < ind:
                stack.append((ind, kind))
                out.append(r"\begin{" + kind + "}")
            item = [m.group(3)]
        elif item is not None:
            item.append(ln.strip())
    flush()
    while stack:
        out.append(r"\end{" + stack.pop()[1] + "}")
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------- caption split
def split_caption(par: str):
    """'**Figure 3.** *caption* rest' -> ('3', 'caption', 'rest')."""
    m = re.match(r"^\*\*(?:Figure|Table) (\w+)\.\*\*\s*\*(.+?)\*(?:\s+(.*))?$", re.sub(r"\s+", " ", par).strip())
    if not m:
        return None
    return m.group(1), m.group(2), (m.group(3) or "").strip()


SUPPLEMENT_MARK = "## @SUPPLEMENT@"


def supplement_markdown(sup: str) -> str:
    """The supplement, ready to append: its "# Title" line dropped (the appendix gets its own heading)."""
    lines = sup.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return SUPPLEMENT_MARK + "\n" + "\n".join(lines)


def convert(md: str, anonymous: bool = False, supplement: str | None = None) -> str:
    global with_supplement
    with_supplement = supplement is not None
    # Look-alike punctuation (U+2024 one dot leader for ".", U+201A low-9 quote for ",") breaks
    # citation matching and typesetting; convert it to the real characters and say so.
    n = md.count("\u2024") + md.count("\u201a")
    if n:
        print(f"warning: replaced {n} look-alike periods/commas (U+2024, U+201A) in the output", file=sys.stderr)
        md = md.replace("\u2024", ".").replace("\u201a", ",")
    if supplement is not None:
        supplement = supplement.replace("\u2024", ".").replace("\u201a", ",")
        md = md.rstrip("\n") + "\n\n" + supplement_markdown(supplement) + "\n"
    lines = collect_footnotes(md.split("\n"))
    title = lines[0].lstrip("# ").strip()
    i = next(k for k, ln in enumerate(lines) if ln.startswith("## Abstract"))
    # Paragraphs between the title and the abstract (e.g. a disclosure note) go under the title.
    front = [p for p in "\n".join(lines[1:i]).split("\n\n") if p.strip() and p.strip() != "---"]
    # An "Author: Name" line under the title names the author (arXiv); --anonymous hides it (OSDI).
    authors = [p.split(":", 1)[1].strip() for p in front if p.strip().startswith("Author:")]
    front = [p for p in front if not p.strip().startswith("Author:")]
    author = "Anonymous submission" if anonymous or not authors else " \\and ".join(authors)
    lines = lines[i:]
    # Drop the draft's reference list (replaced by BibTeX) up to the next section or the end.
    md2 = "\n".join(lines)
    md2 = re.sub(r"^#{2,3} References\n.*?(?=\n## |\Z)", "", md2, flags=re.S | re.M)
    for m in re.finditer(r"^#{2,3} (\d+(?:\.\d+)?)\.? ", md2, flags=re.M):
        labels.add(m.group(1))
    lines = md2.split("\n")

    out, k = [], 0
    for p in front:
        out.append(r"\noindent " + inline(p) + "\n")
    in_appendix = False
    in_supplement = False
    pending_table_caption = None

    def block_until(pred):
        nonlocal k
        start = k
        while k < len(lines) and not pred(lines[k]):
            k += 1
        return lines[start:k]

    while k < len(lines):
        ln = lines[k]
        if not ln.strip() or ln.strip() == "---":
            k += 1
            continue
        if ln.startswith("## Abstract"):
            k += 1
            par = block_until(lambda x: x.startswith("## ") or x.strip() == "---")
            text = "\n\n".join(inline(p) for p in "\n".join(par).split("\n\n") if p.strip())
            out.append(r"\begin{abstract}" + "\n" + text + "\n" + r"\end{abstract}" + "\n")
            continue
        if ln == SUPPLEMENT_MARK:
            # Supplement: after the references, one column, sections/figures/tables numbered S1, S2, ...
            out.append("\\clearpage\n\\onecolumn\n\\appendix\n"
                       "\\renewcommand{\\thesection}{S\\arabic{section}}\n"
                       "\\setcounter{figure}{0}\\renewcommand{\\thefigure}{S\\arabic{figure}}\n"
                       "\\setcounter{table}{0}\\renewcommand{\\thetable}{S\\arabic{table}}\n"
                       "\\section*{Supplementary Material}\n")
            in_appendix = in_supplement = True
            k += 1
            continue
        m = re.match(r"^(#{2,5}) (.*)$", ln)
        if m:
            level, head = len(m.group(1)), m.group(2)
            head = re.sub(r"\s*\*\(.*?\)\*\s*$", "", head)
            head = re.sub(r"\s*\*\*\[TODO\]\*\*\s*$", "", head)
            sm = re.match(r"^(S\d+)\.\s*(.*)$", head) if in_supplement and level == 2 else None
            if sm:
                out.append(r"\section{" + inline(sm.group(2)) + r"}\label{sec:" + sm.group(1) + "}\n")
                k += 1
                continue
            if in_supplement:
                # Numbered sub-headings inside the supplement ("1. What the runtime does") keep their
                # number as text, so they don't collide with the paper's section labels.
                cmd = {2: "section", 3: "subsection", 4: "subsubsection", 5: "paragraph"}[level]
                out.append("\\" + cmd + "*{" + inline(head) + "}\n")
                k += 1
                continue
            am = re.match(r"^Appendix (\w)\.\s*(.*)$", head)
            if am:
                if not in_appendix:
                    out.append("\\clearpage\n\\onecolumn\n\\appendix\n")
                    in_appendix = True
                out.append(r"\section{" + inline(am.group(2)) + r"}\label{sec:" + am.group(1) + "}\n")
                k += 1
                continue
            nm = re.match(r"^(\d+(?:\.\d+)?)\.?\s+(.*)$", head)
            cmd = {2: "section", 3: "subsection", 4: "subsubsection", 5: "paragraph"}[level]
            if nm:
                out.append("\\" + cmd + "{" + inline(nm.group(2)) + r"}\label{sec:" + nm.group(1) + "}\n")
            else:
                out.append("\\" + cmd + "*{" + inline(head) + "}\n")
            k += 1
            continue
        if ln.startswith("```"):
            k += 1
            body = block_until(lambda x: x.startswith("```"))
            k += 1
            # The monospace font has no "§"; write it as "Sec." in code.
            body = [b.replace("§", "Sec. ") for b in body]
            out.append("\\begin{Verbatim}[breaklines,samepage=true,fontsize=\\footnotesize]\n" + "\n".join(body)
                       + "\n\\end{Verbatim}\n")
            continue
        om = re.match(r"^!\[([^\]]*)\]\((\.\./)?(docs/.+?\.png)\)", ln)
        if om:
            # An image from the project docs, with no "Figure N" caption: include it as is.
            k += 1
            out.append("\n".join([r"\begin{center}", r"\includegraphics[width=\textwidth,height=0.8\textheight,keepaspectratio]{../../" + om.group(3) + "}",
                                  r"\end{center}", ""]))
            continue
        if ln.startswith(">"):
            body = block_until(lambda x: not x.startswith(">"))
            out.append(r"\begin{quote}" + inline(" ".join(b.lstrip("> ") for b in body)) + r"\end{quote}" + "\n")
            continue
        fm = re.match(r"^!\[Figure (\w+)\]\(figures/(.+?)\.png\)", ln)
        if fm:
            num, name = fm.group(1), fm.group(2)
            k += 1
            while k < len(lines) and not lines[k].strip():
                k += 1
            par = block_until(lambda x: not x.strip())
            cap = split_caption(" ".join(par))
            caption, rest = (inline(cap[1]), cap[2]) if cap else ("", " ".join(par))
            wide = num in WIDE_FIGURES or in_appendix
            # In the one-column supplement, figures stay where they are in the text ([H]).
            env = "figure" if in_supplement else ("figure*" if wide else "figure")
            w = r"\textwidth" if wide else r"\columnwidth"
            out.append("\n".join([r"\begin{" + env + "}" + ("[H]" if in_supplement else "[t]"), r"\centering",
                                  r"\includegraphics[width=" + w + "]{../figures/" + name + ".pdf}",
                                  r"\caption{" + caption + r"}\label{fig:o" + num + "}", r"\end{" + env + "}", ""]))
            if rest:
                out.append(inline(rest) + "\n")
            continue
        if ln.startswith("|"):
            body = block_until(lambda x: not x.startswith("|"))
            # A caption may follow the table (after a blank line) or precede it.
            cap = pending_table_caption
            pending_table_caption = None
            rest = ""
            if cap is None:
                j = k
                while j < len(lines) and not lines[j].strip():
                    j += 1
                par = []
                while j < len(lines) and lines[j].strip():
                    par.append(lines[j])
                    j += 1
                sc = split_caption(" ".join(par)) if par and par[0].startswith("**Table") else None
                if sc:
                    cap, k = sc, j
                    rest = sc[2]
            caption = inline(cap[1]) if cap else None
            label = "tab:o" + cap[0] if cap else None
            out.append(render_table(body, caption, label, appendix=in_appendix))
            if rest:
                out.append(inline(rest) + "\n")
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", ln):
            body = []
            while k < len(lines):
                cur = lines[k]
                if not cur.strip():
                    nxt = next((x for x in lines[k + 1:] if x.strip()), "")
                    if re.match(r"^\s*([-*]|\d+\.)\s+", nxt) or nxt.startswith("  "):
                        k += 1
                        continue
                    break
                if cur.startswith(("|", "#", "```", "![")):
                    break
                body.append(cur)
                k += 1
            out.append(render_list(body))
            continue
        # As in Markdown, a list may start right after a paragraph line, with no blank line between.
        par = block_until(lambda x: not x.strip() or x.startswith(("|", "#", "```", "![", "---"))
                          or re.match(r"^([-*]|\d+\.)\s+", x))
        text = " ".join(par)
        if text.startswith("**Table") and split_caption(text):
            sc = split_caption(text)
            nxt = next((x for x in lines[k:] if x.strip()), "")
            if nxt.startswith("|"):
                pending_table_caption = sc
                continue
        out.append(inline(text) + "\n")

    body = "\n".join(out)
    if in_appendix:
        idx = body.index("\\clearpage\n\\onecolumn\n\\appendix")  # the first appendix
        refs = "\\bibliographystyle{plain}\n\\bibliography{references}\n\n"
        body = body[:idx] + refs + body[idx:]
    else:
        body += "\n\\bibliographystyle{plain}\n\\bibliography{references}\n"
    return PREAMBLE.replace("@TITLE@", inline(title)).replace("@AUTHOR@", author) + body + "\n\\end{document}\n"


PREAMBLE = r"""% Generated from paper/full.md by paper/latex/md2tex.py. Edit the draft and regenerate,
% or stop regenerating and edit this file directly once the draft is frozen.
\documentclass[letterpaper,twocolumn,10pt]{article}
% The USENIX style targets pdfLaTeX. Under XeTeX (e.g. Tectonic) its breakurl package refuses to
% load before hyperref, and microtype's kerning and spacing features are pdfTeX-only. So under
% XeTeX skip breakurl (hyperref breaks long URLs on its own) and load microtype with protrusion
% only, marking the style's [kerning,spacing] request as already satisfied.
\usepackage{iftex}
\ifXeTeX
  \expandafter\def\csname ver@breakurl.sty\endcsname{}
  \AtBeginDocument{\providecommand{\burl}{\url}}
  \usepackage{microtype}
  \expandafter\def\csname opt@microtype.sty\endcsname{kerning,spacing}
\fi
\usepackage{usenix2019_v3}  % USENIX paper templates page; loads hyperref, cite, microtype, xcolor

\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{longtable}
\usepackage{float}  % [H]: supplement figures stay in place
\usepackage{fvextra}
\usepackage{xurl}  % let long URLs (e.g. in the references) break anywhere

\newcommand{\todo}{\textcolor{red}{\textbf{[TODO]}}}
\renewcommand{\tabularxcolumn}[1]{>{\raggedright\arraybackslash}p{#1}}

\begin{document}

\date{}
\title{\Large \bf @TITLE@}
% The author comes from an "Author:" line in the Markdown; md2tex.py --anonymous blanks it.
\author{{\rm @AUTHOR@}}

\maketitle

"""


def swap_repo_url(md: str, url: str) -> str:
    """Point every link to the project's repository (with or without https://) at url."""
    return re.sub(r"(https?://)?(www\.)?" + re.escape(REPO_URL.split("://", 1)[1]), url, md)


def main(src: str = "paper/full.md", dst: str = "paper/latex/main.tex", anonymous: bool = False,
         supplement: str | None = None, repo_url: str | None = None) -> None:
    sup = None
    if supplement:
        with open(supplement) as f:
            sup = f.read()
    with open(src) as f:
        md = f.read()
    if repo_url:
        md = swap_repo_url(md, repo_url)
        sup = swap_repo_url(sup, repo_url) if sup is not None else None
    tex = convert(md, anonymous, sup)
    if anonymous:
        found = sorted({w for w in IDENTIFYING if w.lower() in tex.lower()})
        if found:
            hint = " Pass --repo-url=<anonymized link>." if "staciers" in found else ""
            sys.exit(f"refusing to write an anonymous build: the output contains {', '.join(found)}.{hint}")
    with open(dst, "w") as f:
        f.write(tex)
    prose = re.sub(r"\\begin\{Verbatim\}.*?\\end\{Verbatim\}", "", tex, flags=re.S)  # code isn't cited
    unresolved = sorted(set(re.findall(r"\[[^\]\n]*\d{4}[a-c]?[^\]\n]*\](?!\()", prose)))
    print(f"wrote {dst}; unresolved citations: {unresolved or 'none'}")


if __name__ == "__main__":
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sup = next((f.split("=", 1)[1] if "=" in f else "paper/supplements.md"
                for f in flags if f.startswith("--supplement")), None)
    repo = next((f.split("=", 1)[1] for f in flags if f.startswith("--repo-url=")), None)
    unknown = [f for f in flags if f != "--anonymous" and not f.startswith(("--supplement", "--repo-url="))]
    if unknown:
        sys.exit(f"unknown option(s): {' '.join(unknown)}")
    main(*args, anonymous="--anonymous" in flags, supplement=sup, repo_url=repo)
