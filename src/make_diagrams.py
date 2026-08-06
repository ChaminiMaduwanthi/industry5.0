"""
Bring Fig. 1 and Fig. 2 in line with what was actually built, and render them.

Both diagrams were drawn during Phase 3, when NSGA-II, SHAP and the operator
override were still in scope. All three were later cut, but the figures were
never revisited — so Fig. 1 announced an "NSGA-II multi-objective search" that
the paper never uses, and Fig. 2 showed a SHAP explanation and an override step
that do not exist. A reader comparing the figures with Section IV would have
found the contradiction immediately.

Three classes of fix are applied to the SVG sources, which are the originals:

    claims        NSGA-II becomes the weighted sum that was implemented; the
                  explanation and override layer is marked as specified but not
                  built, rather than being silently deleted, because it is part
                  of the architecture the paper proposes.
    captions      each SVG carried its own caption, which would print twice
                  beside the caption Word adds. Removed from the artwork.
    typography    the objective used Unicode subscripts and combining
                  circumflexes, both of which the renderer available here draws
                  as filled boxes. Subscripts become ASCII; the normalisation
                  hats are dropped from the artwork and the caption says the
                  terms are normalised, since equation (6) in the text carries
                  them properly. Ŵ is precomposed and survives, so it is
                  replaced too, for consistency within the one expression.

Run:  python src/make_diagrams.py
Writes figures/fig1_architecture.{svg,pdf,png} and fig2_dataflow.{svg,pdf,png}
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parent.parent
FIGS = ROOT / "figures"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SUBSCRIPTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")

EDITS = {
    "fig1_architecture": [
        # the decision layer runs a weighted sum, not NSGA-II
        ("Hard-constraint feasibility filter (HC1–HC4)   →   NSGA-II multi-objective search",
         "Hard-constraint feasibility filter (HC1–HC4)   →   weighted-sum selection"),
        # say plainly that the top layer was not built
        ("human-in-command, not human-in-the-loop",
         "human-in-command, not human-in-the-loop   —   specified; NOT implemented in this study"),
    ],
    "fig2_dataflow": [
        ("NSGA-II on feasible set", "weighted sum on feasible set"),
        ("8  allocation + SHAP reason", "8  allocation + explanation"),
        ("L5 Operator", "L5 Operator *"),
    ],
}

# Matched by pattern rather than by literal: these lines mix precomposed
# accents with combining ones, so an exact string is brittle.
REGEX_EDITS = {
    "fig1_architecture": [
        (r"Objective\s+Z = .*?\(People · Planet · Profit\)",
         "Objective  Z = w1F + w2R + w3E + w4W − w5T    "
         "(normalised terms · People · Planet · Profit)"),
    ],
    "fig2_dataflow": [
        (r"term\s+β3F.?_h\s+in\s+Q_m", "term  β3 F_h (normalised)  in  Q_m"),
        (r"term\s+ψ2v.?_m\s+in\s+R_h", "term  ψ2 v_m (normalised)  in  R_h"),
        (r"term\s+β2\(1 − .?_h,t\)\s+in\s+Q_m",
         "term  β2(1 − S_h,t) (normalised)  in  Q_m"),
    ],
}

# the artwork's own caption duplicates the one the document adds
CAPTION = re.compile(r"\s*<text[^>]*>\s*(?:Fig\.\s*[12]\.|human twin exchanging state)"
                     r".*?</text>", re.S)

# fig2 reuses the caption slot for the footnote its asterisk needs
FIG2_FOOTNOTE = ('<text x="480" y="786" text-anchor="middle" font-size="10.5" '
                 'fill="#666">* L5 is specified in the architecture but is not '
                 'implemented in this study (steps 8 and 9).</text>')


def fix(name: str) -> str:
    path = FIGS / f"{name}.svg"
    svg = path.read_text(encoding="utf-8")
    before = svg

    # normalise typography first, so every pattern below can be written in
    # plain ASCII digits rather than having to match Unicode subscripts
    svg = svg.translate(SUBSCRIPTS)

    for old, new in EDITS[name]:
        if old not in svg:
            raise SystemExit(f"{name}: expected text not found -> {old[:60]}")
        svg = svg.replace(old, new)

    for pattern, new in REGEX_EDITS.get(name, []):
        svg, n = re.subn(pattern, new, svg)
        if not n:
            raise SystemExit(f"{name}: pattern matched nothing -> {pattern[:60]}")

    svg = CAPTION.sub("", svg)
    if name == "fig2_dataflow":
        svg = svg.replace("</svg>", FIG2_FOOTNOTE + "\n</svg>")

    if svg != before:
        path.write_text(svg, encoding="utf-8")
    return svg


def render(name: str, dpi: int = 300) -> None:
    drawing = svg2rlg(str(FIGS / f"{name}.svg"))
    pdf = FIGS / f"{name}.pdf"
    renderPDF.drawToFile(drawing, str(pdf))
    doc = fitz.open(pdf)
    doc[0].get_pixmap(dpi=dpi).save(FIGS / f"{name}.png")
    doc.close()


def main() -> None:
    for name in EDITS:
        fix(name)
        render(name)
        svg = (FIGS / f"{name}.svg").read_text(encoding="utf-8")
        leftovers = [w for w in ("NSGA-II", "SHAP reason", "Fig. 1.", "Fig. 2.")
                     if w in svg]
        assert not leftovers, f"{name}: still contains {leftovers}"
        assert not re.search(r"[₀-₉]", svg), f"{name}: unicode subscripts remain"
        body = re.sub(r"<[^>]+>", "", svg)
        unsafe = sorted({c for c in body
                         if "Ā" <= c <= "˿" or "̀" <= c <= "ͯ"})
        assert not unsafe, (
            f"{name}: glyphs the renderer draws as boxes: {unsafe}. "
            f"Latin-1, Greek, arrows and punctuation are safe; Latin Extended-A "
            f"and combining marks are not.")
        print(f"  [ok] {name}.{{svg,pdf,png}}")

    print("\n  Fig. 1 now shows the weighted sum, and marks L5 as not implemented.")
    print("  Fig. 2 now shows the weighted sum, and footnotes steps 8 and 9.")
    print("  Both captions come from the document, not from the artwork.")


if __name__ == "__main__":
    main()
