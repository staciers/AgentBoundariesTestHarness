"""Figures for Paper 1 (draft). Writes PDF (for LaTeX) and PNG (for the Markdown draft).

    .venv/bin/python paper/figures/make_figures.py [out_dir]     (default: paper/figures)

Figure 2 and figure 5 are computed from the committed runs' episodes. Figures 3, 4 and 6 plot
the pooled counts reported by each study's registered analysis; each constant names the file it
was transcribed from. Figure 7 is the sensitivity curve from ``analysis/latency_sensitivity.py``.
No model calls.
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
from statsmodels.stats.proportion import proportion_confint  # noqa: E402

sys.path.insert(0, ".")
from abh.metrics import load_episodes  # noqa: E402
from analysis import heterogeneity as het  # noqa: E402
from analysis import latency_sensitivity as lat  # noqa: E402

INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]  # categorical slots 1-6
BLUE, ORANGE, GREEN, YELLOW = SERIES[:4]
REAL_RUN = "runs/real-ledger-20261028-111807"
HW = "timeout_after_execution+delayed_visibility"
P6, NOKEY = "P6[threshold=0.7]", "P1[expose_keys=False]"

plt.rcParams.update({"font.size": 8, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": MUTED,
                     "ytick.color": INK2, "axes.titlecolor": INK, "axes.titlesize": 8.5, "axes.titleweight": "bold",
                     "legend.frameon": False, "font.family": "sans-serif"})


def wilson(k, n):
    lo, hi = proportion_confint(k, n, method="wilson")
    return k / n * 100, lo * 100, hi * 100


def style(ax, xgrid=True, ygrid=False):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if xgrid:
        ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
    if ygrid:
        ax.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    ax.set_axisbelow(True)


def save(fig, out, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, f"{name}.{ext}"), dpi=200, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- figure 1
def fig1_architecture(out):
    fig, ax = plt.subplots(figsize=(7.0, 4.3), facecolor=SURFACE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis("off")

    def box(x, y, w, h, title, sub=None, fill=SURFACE, edge=INK2, lw=1.0):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=1.2", fc=fill, ec=edge,
                                    lw=lw, zorder=2))
        lines = sub.count("\n") + 1 if sub else 0
        ax.text(x + w / 2, y + h / 2 + 1.1 * lines, title, ha="center", va="center", fontsize=8, color=INK,
                fontweight="bold", zorder=3)
        if sub:
            ax.text(x + w / 2, y + h / 2 - 1.2, sub, ha="center", va="center", fontsize=6.4, color=INK2, zorder=3,
                    linespacing=1.15)

    def path(points, color=INK2, label=None, at=None, ha="center", rotation=0):
        xs, ys = zip(*points)
        ax.plot(xs[:-1], ys[:-1], color=color, lw=1.0, zorder=1, solid_capstyle="round")
        ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>", mutation_scale=9, lw=1.0,
                                     color=color, zorder=1, shrinkA=0, shrinkB=1))
        if label:
            ax.text(*at, label, fontsize=6.2, color=color if color != INK2 else INK2, ha=ha, va="center",
                    zorder=3, rotation=rotation, linespacing=1.1, bbox=dict(fc=SURFACE, ec="none", pad=0.5))

    box(3, 51, 40, 8.5, "Agent (LLM)", "proposes tool calls; owns semantic recovery")
    box(57, 51, 23, 8.5, "Human principal", "authority; unresolved\nconsequential outcomes")

    ax.add_patch(FancyBboxPatch((2.6, 13.4), 74.8, 32.4, boxstyle="round,pad=0.3,rounding_size=1.5", fc="none",
                                ec=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=0))
    ax.text(76.8, 14.6, "control plane", fontsize=7, color=MUTED, ha="right", va="center", fontstyle="italic")

    box(4, 31, 16.5, 8.5, "Authority gate", "deterministic\ndelegation rules")
    box(22.8, 31, 14.4, 8.5, "Policy gate", "approval before\nexecution")
    box(39.6, 29.8, 21.6, 11, "Runtime", "keys · reconcile · verify\ncompensate · inspect\nclassify failures")
    box(63.5, 31, 12.5, 8.5, "Route", "unresolved\noutcomes")
    box(7, 15.5, 45, 10, "Execution contract", "per tool: key scope · partial effects · visibility\n"
        "reconcile · postcondition · compensation · inspect", fill="#eaf2fc", edge=BLUE, lw=1.4)
    box(9, 1.2, 61, 7.5, "Services (tools)", "enforce the key scope; a request commits, partly commits or times out")

    # Agent <-> control plane
    path([(9, 50.8), (9, 39.8)], label="tool call", at=(9, 45.5))
    path([(15, 39.8), (15, 50.8)], label="result or\nexecution state", at=(15.6, 45.5), ha="left")
    # Pipeline
    for a, b in ((20.7, 22.6), (37.4, 39.4), (61.4, 63.3)):
        path([(a, 35.25), (b, 35.25)])
    # To the human
    path([(29, 39.7), (29, 48), (62, 48), (62, 50.8)], color=ORANGE, label="approval", at=(45, 48))
    path([(72, 39.7), (72, 50.8)], color=ORANGE, label="consequential,\nunresolved", at=(72.6, 45), ha="left")
    # To services
    path([(57, 29.6), (57, 8.9)], label="attempts", at=(57.8, 12), ha="left")
    # Contract uses
    path([(47, 25.7), (47, 29.6)], color=BLUE, label="what is safe to retry", at=(48, 27.6), ha="left")
    path([(29, 25.7), (29, 30.8)], color=BLUE, label="consequence", at=(30, 28.2), ha="left")
    path([(29, 15.3), (29, 8.9)], color=BLUE, label="enforced by", at=(30, 12), ha="left")
    path([(6.8, 20.5), (1.0, 20.5), (1.0, 55), (2.8, 55)], color=BLUE, label="generated tool descriptions",
         at=(1.0, 30), rotation=90)
    save(fig, out, "fig1_architecture")


# --------------------------------------------------------------------------- figure 2
def fig2_harm_per_model(out):
    panels = []
    by_id = {c[0]: c for c in het.CLAIMS}
    for claim, title in ((by_id["Q1"], "Development domains (simulated)"),
                         (by_id["Q5-hidden-write"], "Accounts-payable family (simulated)")):
        rows = [(lbl.split(" (")[0], fam, ka, na, kb, nb) for lbl, fam, ka, na, kb, nb, _ in het.rows_for(claim)]
        panels.append((title, rows))
    real = defaultdict(lambda: [0, 0, 0, 0])
    for e in load_episodes(os.path.join(REAL_RUN, "episodes.jsonl")):
        if e["domain"] != "ledger_real" or e["faults"] != HW or "error" in e:
            continue
        r = real[(het.model(e), het.family(e))]
        if e["policy"] == NOKEY:
            r[0] += bool(e["harm"]); r[1] += 1
        elif e["policy"] == P6:
            r[2] += bool(e["harm"]); r[3] += 1
    panels.append(("Accounts-payable family on Postgres (real services)", [(m, f, *v) for (m, f), v in real.items()]))

    heights = [len(r) + 1.2 for _, r in panels]
    fig, axes = plt.subplots(len(panels), 1, figsize=(5.6, 0.2 * sum(heights) + 0.9), sharex=True, facecolor=SURFACE,
                             gridspec_kw={"height_ratios": heights, "hspace": 0.45})
    fam_style = {"closed": ("o", BLUE), "open": ("s", ORANGE)}
    for ax, (title, rows) in zip(axes, panels):
        style(ax)
        rows = sorted(rows, key=lambda r: r[2] / r[3])
        for y, (m, fam, ka, na, kb, nb) in enumerate(rows):
            mk, c = fam_style[fam]
            p, lo, hi = wilson(ka, na)
            ax.plot([lo, hi], [y, y], color=c, lw=1.6, zorder=2, solid_capstyle="round")
            ax.scatter([p], [y], marker=mk, s=30, color=c, edgecolor=SURFACE, lw=1, zorder=3)
            ax.scatter([kb / nb * 100], [y], marker="|", s=45, color=INK, lw=1.4, zorder=2)
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([r[0] for r in rows], fontsize=7)
        ax.set_ylim(-0.8, len(rows) - 0.2)
        ax.set_title(title, loc="left", fontsize=8)
        ax.tick_params(axis="y", length=0)
    axes[-1].set_xlim(-2, 102)
    axes[-1].set_xlabel("harm under a hidden write (% of episodes, Wilson 95% CI)")
    handles = [plt.Line2D([], [], marker="o", color=BLUE, lw=1.6, label="no runtime, closed model"),
               plt.Line2D([], [], marker="s", color=ORANGE, lw=1.6, label="no runtime, open-weight model"),
               plt.Line2D([], [], marker="|", color=INK, lw=0, markersize=7, markeredgewidth=1.4,
                          label="with the runtime (P6): 0 harm for every model")]
    axes[0].legend(handles=handles, loc="lower right", fontsize=6.6, bbox_to_anchor=(1.0, 1.08), ncol=1)
    save(fig, out, "fig2_harm_per_model")


# --------------------------------------------------------------------------- figure 3
# Transcribed from runs/stage-d-20261018-111143/stage_d.md ("Policy × runtime grid", 720 episodes per cell,
# and the component family K1-K3).
STAGE_D_GRID = {  # policy: (success none, success semantic, harm none, harm semantic), %
    "P1 autonomy": (41, 46, 15, 9), "P3 confidence": (44, 49, 39, 34), "P4 static risk": (63, 71, 18, 10),
    "P5 agent asks": (72, 79, 14, 6), "P6": (77, 77, 4, 4), "Oracle": (95, 94, 0, 0)}
STAGE_D_COMPONENTS = [  # (label, full P6 (k, n), ablated (k, n), outcome)
    ("Authority gate removed\n(harm, authority tasks)", (0, 240), (215, 240), "harm"),
    ("Routing to agent instead\nof human (harm, hidden write,\nno runtime)", (15, 360), (74, 360), "harm"),
    ("Confidence gate removed\n(success, all tasks)", (552, 720), (544, 720), "success"),
]


def fig3_stage_d(out):
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.9), facecolor=SURFACE, gridspec_kw={"width_ratios": [1.15, 1]})
    style(a, xgrid=True, ygrid=True)
    for i, (p, (sn, ss, hn, hs)) in enumerate(STAGE_D_GRID.items()):
        c = INK if p in ("P6",) else (MUTED if p == "Oracle" else SERIES[i % len(SERIES)])
        a.add_patch(FancyArrowPatch((hn, sn), (hs, ss), arrowstyle="-|>", mutation_scale=7, color=c, lw=1.0,
                                    shrinkA=3, shrinkB=3, zorder=2))
        a.scatter([hn], [sn], s=26, facecolor=SURFACE, edgecolor=c, lw=1.2, zorder=3)
        a.scatter([hs], [ss], s=30, color=c, edgecolor=SURFACE, lw=0.8, zorder=4)
        lx, ly, ha = {"P1 autonomy": (16.5, 40, "left"), "P3 confidence": (40.5, 45, "left"),
                      "P4 static risk": (19.5, 62.5, "left"), "P5 agent asks": (15.5, 73, "left"),
                      "P6": (3.6, 73.2, "center"), "Oracle": (2.2, 92.5, "left")}[p]
        a.text(lx, ly, p, fontsize=7, color=INK, ha=ha, va="center", fontweight="bold" if p == "P6" else "normal")
    a.set_xlim(-2, 50)
    a.set_ylim(35, 100)
    a.set_xlabel("harm (% of episodes)")
    a.set_ylabel("task success (% of episodes)")
    a.set_title("(a) Policy × runtime", loc="left")
    a.legend(handles=[plt.Line2D([], [], marker="o", color=INK2, markerfacecolor=SURFACE, lw=0, label="no runtime"),
                      plt.Line2D([], [], marker="o", color=INK2, lw=0, label="semantic runtime")],
             loc="upper right", fontsize=6.6)

    style(b, xgrid=True)
    for y, (lbl, full, abl, kind) in enumerate(STAGE_D_COMPONENTS):
        pf, lf, hf = wilson(*full)
        pa, la, ha_ = wilson(*abl)
        b.plot([pf, pa], [y, y], color=GRID, lw=3, zorder=1, solid_capstyle="round")
        b.errorbar([pf], [y], xerr=[[pf - lf], [hf - pf]], fmt="o", color=INK, ms=5, lw=1, capsize=0, zorder=3)
        b.errorbar([pa], [y], xerr=[[pa - la], [ha_ - pa]], fmt="D", color=ORANGE, ms=4.5, lw=1, capsize=0, zorder=3)
    b.set_yticks(range(len(STAGE_D_COMPONENTS)))
    b.set_yticklabels([c[0] for c in STAGE_D_COMPONENTS], fontsize=6.6)
    b.invert_yaxis()
    b.tick_params(axis="y", length=0)
    b.set_xlim(-3, 100)
    b.set_xlabel("% of episodes (Wilson 95% CI)")
    b.set_title("(b) P6 components, ablated one at a time", loc="left")
    b.legend(handles=[plt.Line2D([], [], marker="o", color=INK, lw=0, label="full P6"),
                      plt.Line2D([], [], marker="D", color=ORANGE, lw=0, label="component ablated")],
             loc="center right", fontsize=6.6)
    fig.tight_layout(w_pad=2.5)
    save(fig, out, "fig3_stage_d")


# --------------------------------------------------------------------------- figure 4
# Transcribed from runs/contracts-20261026-140610/contracts.md (arms A-D, N; 630 episodes each, 7 models)
# and runs/repair-20261027-101723/repair.md (D, D1, D2, N; 630 each). Hidden partial commit, no runtime.
CONTRACT_ARMS = [("no keys", 24, 630, MUTED), ("completed scope,\n'at most once' wording", 116, 630, ORANGE),
                 ("completed scope,\ncontract wording", 31, 630, BLUE), ("atomic scope,\n'at most once' wording", 45, 630, BLUE),
                 ("atomic scope,\ncontract wording", 119, 630, ORANGE)]
REPAIR_ARMS = [("no keys", 3, 630, MUTED), ("atomic scope, no repair\nguidance", 89, 630, ORANGE),
               ("+ repair described\nin prose", 15, 630, BLUE), ("+ partial report and\ncancel_partial", 7, 630, BLUE)]


def fig4_keys(out):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6), facecolor=SURFACE, sharex=True,
                             gridspec_kw={"width_ratios": [1, 1]})
    for ax, arms, title in ((axes[0], CONTRACT_ARMS, "(a) Contract study: key scope × description"),
                            (axes[1], REPAIR_ARMS, "(b) Repair study: contract-declared repair")):
        style(ax)
        for y, (lbl, k, n, c) in enumerate(arms):
            p, lo, hi = wilson(k, n)
            ax.barh(y, p, height=0.62, color=c, zorder=2)
            ax.plot([lo, hi], [y, y], color=INK, lw=0.9, zorder=3)
            ax.text(hi + 0.8, y, f"{p:.1f}%" if p < 1 else f"{p:.0f}%", fontsize=6.8, color=INK, va="center")
        ax.set_yticks(range(len(arms)))
        ax.set_yticklabels([a[0] for a in arms], fontsize=6.6)
        ax.invert_yaxis()
        ax.tick_params(axis="y", length=0)
        ax.set_title(title, loc="left")
        ax.set_xlabel("harm under a hidden partial commit (%)")
    axes[0].set_xlim(0, 27)
    fig.text(0.99, -0.04, "No runtime. With the contract-driven runtime (P6), harm was 0/210 under an atomic scope.",
             fontsize=6.6, color=INK2, ha="right")
    fig.tight_layout(w_pad=2.5)
    save(fig, out, "fig4_keys")


# --------------------------------------------------------------------------- figure 5
def fig5_autonomy(out):
    order = ["P1", "P3[threshold=0.7]", "P4", "P5", P6, "ORACLE"]
    names = {"P1": "P1 autonomy", "P3[threshold=0.7]": "P3 confidence", "P4": "P4 static risk",
             "P5": "P5 agent asks", P6: "P6", "ORACLE": "Oracle"}
    counts = {p: defaultdict(int) for p in order}
    for e in het.episodes("stage-d"):
        if e["runtime"] != "semantic" or e["policy"] not in counts:
            continue
        c = counts[e["policy"]]
        c["n"] += 1
        if e["harm"]:
            c["harmful"] += 1
        elif e["success"]:
            c["autonomous success" if e["autonomous"] else "success with a human"] += 1
        else:
            c["failed safely"] += 1
    cats = [("autonomous success", BLUE), ("success with a human", "#9cc3ef"), ("failed safely", GRID),
            ("harmful", ORANGE)]
    fig, ax = plt.subplots(figsize=(5.6, 2.3), facecolor=SURFACE)
    style(ax)
    for y, p in enumerate(order):
        left = 0
        for cat, col in cats:
            v = counts[p][cat] / counts[p]["n"] * 100
            ax.barh(y, v, left=left, height=0.64, color=col, edgecolor=SURFACE, lw=1, zorder=2)
            if v >= 3.5:
                ax.text(left + v / 2, y, f"{v:.0f}", fontsize=6.6, ha="center", va="center",
                        color=SURFACE if col in (BLUE, ORANGE) else INK)
            left += v
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([names[p] for p in order], fontsize=7)
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of episodes (Stage D, semantic runtime, 720 per policy)")
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c, label=l) for l, c in cats], ncol=4, fontsize=6.6,
              loc="lower left", bbox_to_anchor=(0, 1.0))
    save(fig, out, "fig5_autonomy")


# --------------------------------------------------------------------------- figure 6
# Transcribed from runs/stage-e-20261027-135311/stage_e.md (semantic faults by controller; E1, E4).
STAGE_E_SEMANTIC = {  # controller: ((k, n) development, (k, n) held-out)
    "LLM agents (8 models)": ((1096, 1120), (720, 720)),
    "hand-tuned / spec-derived rules": ((140, 140), (60, 90)),
    "generic rule library": ((110, 140), (60, 90)),
    "fixed workflow": ((10, 140), (0, 90)),
}
STAGE_E_SAFETY = [("hidden write\n(no keys vs P6)", (128, 240), (0, 240)),
                  ("authority\n(P1 vs P6)", (20, 160), (0, 160))]


def fig6_held_out(out):
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.5), facecolor=SURFACE, gridspec_kw={"width_ratios": [1.7, 1]})
    style(a, xgrid=False, ygrid=True)
    cols = [BLUE, GREEN, YELLOW, MUTED]
    w = 0.19
    for i, ((lbl, cells), c) in enumerate(zip(STAGE_E_SEMANTIC.items(), cols)):
        for g, (k, n) in enumerate(cells):
            p, lo, hi = wilson(k, n)
            x = g + (i - 1.5) * (w + 0.02)
            a.bar(x, p, width=w, color=c, zorder=2, label=lbl if g == 0 else None)
            a.plot([x, x], [lo, hi], color=INK, lw=0.8, zorder=3)
            a.text(x, hi + 2, f"{p:.0f}", fontsize=6.4, ha="center", color=INK)
    a.set_xticks([0, 1])
    a.set_xticklabels(["development domains", "accounts-payable family"], fontsize=7.2)
    a.set_ylim(0, 112)
    a.set_yticks([0, 25, 50, 75, 100])
    a.set_ylabel("success on semantic faults (%)")
    a.set_title("(a) Who recovers from semantic faults", loc="left")
    a.legend(fontsize=6.4, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2)

    style(b, xgrid=False, ygrid=True)
    for g, (lbl, without, with_) in enumerate(STAGE_E_SAFETY):
        for j, ((k, n), c) in enumerate(((without, ORANGE), (with_, INK))):
            p, lo, hi = wilson(k, n)
            x = g + (j - 0.5) * 0.36
            b.bar(x, max(p, 0.6), width=0.32, color=c, zorder=2)
            b.plot([x, x], [lo, hi], color=INK, lw=0.8, zorder=3)
            b.text(x, hi + 2, f"{p:.0f}", fontsize=6.4, ha="center", color=INK)
    b.set_xticks([0, 1])
    b.set_xticklabels([s[0] for s in STAGE_E_SAFETY], fontsize=7)
    b.set_ylim(0, 70)
    b.set_ylabel("harm, accounts-payable family (%)")
    b.set_title("(b) Held-out safety", loc="left")
    b.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=ORANGE, label="without the mechanism"),
                      plt.Rectangle((0, 0), 1, 1, color=INK, label="with P6")], fontsize=6.4, loc="upper right")
    fig.tight_layout(w_pad=2.5)
    save(fig, out, "fig6_held_out")


# --------------------------------------------------------------------------- figure 7
def fig7_sensitivity(out):
    eps = [e for e in load_episodes(os.path.join(REAL_RUN, "episodes.jsonl"))
           if e["faults"] == lat.HW and e["policy"] == lat.NOKEY and "error" not in e]
    real = defaultdict(list)
    observed = defaultdict(lambda: {"ledger_real": [0, 0], "ledger": [0, 0]})
    for e in eps:
        m = lat.model(e)
        observed[m][e["domain"]][0] += bool(e["harm"])
        observed[m][e["domain"]][1] += 1
        if e["domain"] == "ledger_real":
            real[m].append(lat.retry_gap(REAL_RUN, e))
    models = [m for m in lat.ORDER if m in real] + sorted(set(real) - set(lat.ORDER))
    allgaps = [g for m in models for g in real[m]]
    for ext in ("pdf", "png"):
        lat.plot(real, models, allgaps, observed, os.path.join(out, f"fig7_sensitivity.{ext}"), title=False)


# --------------------------------------------------------------------------- figure A1
# Development timeline. Studies: date each main run started. Issues: numbered as in the paper's
# appendix table, with the date each was found (pre-registration deviation logs and run notes).
STUDIES = [("2026-10-12", "Confirmation"), ("2026-10-13", "Stage A, Stage C"), ("2026-10-14", "Open replications"),
           ("2026-10-15", "Stage B"), ("2026-10-18", "Stage D"), ("2026-10-26", "Contracts"),
           ("2026-10-27", "Repair, Stage E"), ("2026-10-28", "Real services")]
ISSUES = [  # (number, date, category)
    (1, "2026-10-11", "scenario"), (2, "2026-10-12", "measurement"), (3, "2026-10-13", "scenario"),
    (4, "2026-10-13", "harness"), (5, "2026-10-13", "measurement"), (6, "2026-10-14", "harness"),
    (7, "2026-10-14", "operational"), (8, "2026-10-14", "scenario"), (9, "2026-10-14", "scenario"),
    (10, "2026-10-16", "operational"), (11, "2026-10-16", "harness"), (12, "2026-10-26", "measurement"),
    (13, "2026-10-26", "measurement"), (14, "2026-10-26", "operational"), (15, "2026-10-27", "scenario"),
    (16, "2026-10-27", "scenario"), (17, "2026-10-27", "harness"), (18, "2026-10-28", "measurement"),
    (19, "2026-10-28", "harness"), (20, "2026-10-28", "scenario"), (21, "2026-10-28", "harness"),
    (22, "2026-10-28", "scenario"), (23, "2026-10-29", "measurement"), (24, "2026-10-29", "scenario")]
ISSUE_STYLE = {"harness": (ORANGE, "o", "harness defect"), "scenario": (BLUE, "s", "scenario or design validity"),
               "measurement": (GREEN, "^", "measurement or analysis"),
               "operational": (YELLOW, "D", "provider or operational")}


def figA1_timeline(out):
    from datetime import date
    day = lambda d: (date.fromisoformat(d) - date(2026, 10, 11)).days
    fig, ax = plt.subplots(figsize=(7.0, 2.7), facecolor=SURFACE)
    style(ax, xgrid=True)
    for d, name in STUDIES:
        x = day(d)
        ax.plot([x, x], [2.55, 3.05], color=INK2, lw=1, zorder=2)
        ax.scatter([x], [3.05], s=22, color=INK, zorder=3)
        ax.text(x, 3.25, name, rotation=35, fontsize=6.6, color=INK, ha="left", va="bottom")
    per_day = defaultdict(int)
    for n, d, cat in ISSUES:
        c, m, _ = ISSUE_STYLE[cat]
        x, k = day(d), per_day[d]
        per_day[d] += 1
        y = 2.1 - 0.36 * k
        ax.scatter([x], [y], s=70, marker=m, color=c, edgecolor=SURFACE, lw=0.8, zorder=3)
        ax.text(x + 0.28, y, str(n), fontsize=6.4, color=INK, va="center", ha="left")
    ax.axvspan(day("2026-10-19") - 0.5, day("2026-10-25") + 0.5, color=GRID, alpha=0.5, lw=0, zorder=0)
    ax.text((day("2026-10-19") + day("2026-10-25")) / 2, 1.5, "no commits or runs", fontsize=6.4, color=MUTED,
            ha="center")
    ticks = range(0, 19, 2)
    ax.set_xticks(list(ticks))
    ax.set_xticklabels([f"Oct {11 + t}" for t in ticks], fontsize=7)
    ax.set_xlim(-0.8, 19.2)
    ax.set_ylim(0.45, 4.6)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(-0.7, 3.05, "studies", fontsize=7, color=INK2, ha="left", va="center", fontstyle="italic")
    ax.text(-0.7, 2.45, "issues", fontsize=7, color=INK2, ha="left", va="center", fontstyle="italic")
    ax.legend(handles=[plt.Line2D([], [], marker=m, color=c, lw=0, markersize=6, label=l)
                       for c, m, l in ISSUE_STYLE.values()], loc="upper center", ncol=4, fontsize=6.4,
              bbox_to_anchor=(0.5, -0.13))
    save(fig, out, "figA1_timeline")


# --------------------------------------------------------------------------- figure S2
# Why stratified Mantel-Haenszel tests with Holm correction (Supplement S2). Panels (a), (c) and (d)
# use committed run data; panel (b) uses made-up numbers to show how pooling can reverse an effect.
STAGE_D_REPORT = "runs/stage-d-20261018-111143/stage_d.md"


def _holm_family(path):
    rows = []
    for ln in open(path):
        m = re.match(r"^\| (D\d) \|.*\| ([0-9.e+-]+|inf) \| ([0-9.e+-]+) \| ([0-9.e+-]+) \| (.*?) \|$", ln.strip())
        if m:
            rows.append((m.group(1), float(m.group(3)), "confirmed" in m.group(5) and "not" not in m.group(5)))
    return rows


def figS2_tests(out):
    import numpy as np
    by_id = {c[0]: c for c in het.CLAIMS}
    q1 = [(lbl.split(" (")[0], fam, ka, na, kb, nb) for lbl, fam, ka, na, kb, nb, _ in het.rows_for(by_id["Q1"])]
    q1.sort(key=lambda r: r[2] / r[3])
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.6), facecolor=SURFACE)
    (a, b), (c, d) = axes

    # (a) real: base rates differ by model, and the runtime arm has no events at all
    style(a)
    for i, (m, fam, ka, na, kb, nb) in enumerate(q1):
        col = BLUE if fam == "closed" else ORANGE
        v, lo, hi = wilson(ka, na)
        a.plot([lo, hi], [i, i], color=col, lw=2, solid_capstyle="round", zorder=2)
        a.scatter([v], [i], s=34, color=col, edgecolor=SURFACE, lw=1.2, zorder=3)
        a.scatter([kb / nb * 100], [i], s=40, marker="|", color=INK, lw=2, zorder=3)
        a.text(103, i, f"{ka}/{na} vs {kb}/{nb}", va="center", fontsize=6.6, color=INK2)
    a.set_yticks(range(len(q1)), [r[0] for r in q1], fontsize=7)
    a.set_xlim(-3, 128)
    a.set_xticks([0, 25, 50, 75, 100])
    a.set_xlabel("harm under a hidden write (%)")
    a.set_title("(a) Base rates differ by model (real data, Q1)", loc="left")
    a.scatter([], [], s=34, color=INK2, label="no runtime (95% CI)")
    a.scatter([], [], s=40, marker="|", color=INK, lw=2, label="with the runtime: 0 events")
    a.legend(fontsize=6.6, loc="upper left", bbox_to_anchor=(0.03, 0.9))

    # (b) placeholder: pooling across strata reverses the within-stratum effect
    style(b, xgrid=False, ygrid=True)
    strata = [("model X\n(low base rate)", (20, 200), (1, 20)),
              ("model Y\n(high base rate)", (18, 20), (160, 200))]
    pooled_a = (sum(s[1][0] for s in strata), sum(s[1][1] for s in strata))
    pooled_b = (sum(s[2][0] for s in strata), sum(s[2][1] for s in strata))
    groups = strata + [("pooled", pooled_a, pooled_b)]
    w = 0.36
    for i, (name, (ka, na), (kb, nb)) in enumerate(groups):
        for off, (k, n), col in ((-w / 2, (ka, na), GREEN), (w / 2, (kb, nb), MUTED)):
            v = k / n * 100
            b.bar(i + off, v, width=w - 0.04, color=col, zorder=2)
            b.text(i + off, v + 2, f"{v:.0f}%\n{k}/{n}", ha="center", va="bottom", fontsize=6.4, color=INK2)
    b.axvline(1.5, color=GRID, lw=1)
    b.set_xticks(range(3), [g[0] for g in groups], fontsize=7)
    b.set_ylim(0, 112)
    b.set_ylabel("event rate (%)")
    b.set_title("(b) Pooling can reverse an effect (illustrative numbers)", loc="left")
    from matplotlib.patches import Patch
    b.legend(handles=[Patch(color=GREEN, label="arm A"), Patch(color=MUTED, label="arm B")],
             fontsize=6.8, loc="upper left")
    b.text(2, 96, "A > B in each model,\nbut A < B pooled", ha="center", fontsize=6.6, color=INK)

    # (c) real: with zero events in one arm, the logistic likelihood has no maximum
    style(c, xgrid=False, ygrid=True)
    m, fam, ka, na, kb, nb = next(r for r in q1 if r[0] == "gpt-6.1-sol")
    betas = np.linspace(0, 30, 301)

    def profile(beta):
        # logit p_B = alpha, logit p_A = alpha + beta; maximise over alpha on a grid
        al = np.linspace(-40, 5, 9001)
        pa, pb = 1 / (1 + np.exp(-(al + beta))), 1 / (1 + np.exp(-al))
        eps = 1e-300
        ll = ka * np.log(pa + eps) + (na - ka) * np.log(1 - pa + eps) + kb * np.log(pb + eps) + (nb - kb) * np.log(1 - pb + eps)
        return ll.max()
    ll = np.array([profile(x) for x in betas])
    c.plot(betas, ll, color=BLUE, lw=2, zorder=2)
    sup = ka * np.log(ka / na) + (na - ka) * np.log(1 - ka / na)
    c.axhline(sup, color=INK, lw=1, ls=(0, (3, 3)))
    c.text(30, sup - 1.2, "never reached", ha="right", va="top", fontsize=6.6, color=INK2)
    c.set_ylim(sup - 25, sup + 4)
    c.set_xlabel("log odds ratio, no runtime vs runtime")
    c.set_ylabel("log-likelihood")
    c.set_title("(c) Zero events: no finite estimate (real data)", loc="left")
    c.text(3, sup - 22, f"{m}: {ka}/{na} without the runtime vs {kb}/{nb} with it.\nThe fit keeps improving as "
           "the estimate grows, so a\nlogistic model has no answer; the stratified test\nstill gives a p-value "
           "(odds ratio = ∞).", fontsize=6.6, color=INK2)

    # (d) real: Holm on the Stage D family
    style(d, xgrid=False, ygrid=True)
    fam_rows = sorted(_holm_family(STAGE_D_REPORT), key=lambda r: r[1])
    k = len(fam_rows)
    floor = 1e-16
    xs = np.arange(1, k + 1)
    thr = [0.05 / (k - i) for i in range(k)]
    d.step(xs, thr, where="mid", color=INK, lw=1.2, label="Holm threshold 0.05/(m − i + 1)")
    for x, (cid, pv, ok) in zip(xs, fam_rows):
        y = max(pv, floor)
        d.scatter([x], [y], s=40, color=GREEN if ok else MUTED, edgecolor=SURFACE, lw=1.2, zorder=3)
        d.text(x, y * 3, cid, ha="center", va="bottom", fontsize=6.8, color=INK2)
    d.set_yscale("log")
    d.set_ylim(floor / 10, 5)
    d.set_xticks(xs, [str(i) for i in xs])
    d.set_xlabel("tests in order of p-value (smallest first)")
    d.set_ylabel("p-value (floor 1e-16)")
    d.set_title("(d) Holm, Stage D family (real data)", loc="left")
    d.scatter([], [], color=GREEN, label="confirmed")
    d.scatter([], [], color=MUTED, label="not confirmed: stop")
    d.legend(fontsize=6.6, loc="center left", bbox_to_anchor=(0.0, 0.42))

    fig.tight_layout(h_pad=2.2, w_pad=2.0)
    save(fig, out, "figS2_tests")


def main(out: str = "paper/figures") -> None:
    os.makedirs(out, exist_ok=True)
    for f in (fig1_architecture, fig2_harm_per_model, fig3_stage_d, fig4_keys, fig5_autonomy, fig6_held_out,
              fig7_sensitivity, figA1_timeline, figS2_tests):
        f(out)
        print("wrote", f.__name__)


if __name__ == "__main__":
    main(*sys.argv[1:])
