import sys, re, subprocess
from pathlib import Path
from docx import Document
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"c:\Users\Admin\Desktop\research\industry 5.0")
d = Document(ROOT / "paper.docx")
paras = [(p.style.name, p.text) for p in d.paragraphs]

EQ = re.compile(r"^\t.*\t\(\d\)$")
prose, refs, in_refs = [], [], False
for st, tx in paras:
    if st == "Heading 1" and tx.strip().lower() == "references":
        in_refs = True
        continue
    if in_refs:
        refs.append(tx)
    elif not EQ.match(tx):
        prose.append(tx)
prose_txt = "\n".join(prose)

print("=" * 78)
print("  A · FORBIDDEN CLAIMS, read in context")
print("=" * 78)
NEG = r"(not|no|never|rather than|instead of|without|neither)"
CASES = [
    (r"Pareto", "Pareto front"),
    (r"operator override|override layer", "operator override"),
    (r"five-layer", "five-layer architecture"),
]
for pat, name in CASES:
    hits = []
    for tx in prose:
        for m in re.finditer(pat, tx, re.I):
            window = tx[max(0, m.start() - 120): m.end() + 120]
            negated = re.search(NEG, window, re.I) is not None
            hits.append((negated, window.strip()[:120]))
    if not hits:
        print(f"  clear    {name}: absent")
    elif all(h[0] for h in hits):
        print(f"  ok       {name}: {len(hits)} mention(s), every one a disclaimer")
    else:
        print(f"  BLOCKING {name}: an unqualified claim")
        for n, w in hits:
            if not n:
                print(f"           …{w}…")

print("\n" + "=" * 78)
print("  B · EQUATIONS — referred to in the running text?")
print("=" * 78)
for n in range(1, 7):
    cited = bool(re.search(rf"\({n}\)", prose_txt))
    print(f"  eq ({n}) referenced in prose: {cited}")
print("  note: IEEE permits an equation introduced by the sentence before it;")
print("        a number is only required where the text points back to it.")

print("\n" + "=" * 78)
print("  C · SPELLING CONSISTENCY (British vs American)")
print("=" * 78)
PAIRS = [("optimis", "optimiz"), ("normalis", "normaliz"), ("modell", "modeli"),
         ("behaviour", "behavior"), ("recognis", "recogniz"), ("analys", "analyz")]
for br, am in PAIRS:
    b = len(re.findall(br, prose_txt, re.I))
    a = len(re.findall(am, prose_txt, re.I))
    flag = "MIXED" if b and a else "ok"
    if b or a:
        print(f"  {flag:6s} {br}* = {b:2d}   {am}* = {a:2d}")
hy = [("well-being", "wellbeing"), ("trade-off", "tradeoff"), ("re-entered", "reentered")]
for a, b in hy:
    ca, cb = len(re.findall(a, prose_txt, re.I)), len(re.findall(b, prose_txt, re.I))
    if ca and cb:
        print(f"  MIXED  {a}={ca}  {b}={cb}")
    elif ca or cb:
        print(f"  ok     {a if ca else b} used consistently ({ca or cb})")

print("\n" + "=" * 78)
print("  D · NUMBER CONSISTENCY inside the paper")
print("=" * 78)
pairs = [(r"27\.0%", "fatigue reduction"), (r"30\.8%", "energy per unit"),
         (r"79\.5", "breaches"), (r"1\.8%", "throughput change"),
         (r"0\.148", "throughput p-value"), (r"46 studies", "review size"),
         (r"270", "run count"), (r"95\.7%", "constrained decisions")]
for pat, what in pairs:
    n = len(re.findall(pat, prose_txt))
    print(f"  {what:26s} appears {n}x")

print("\n" + "=" * 78)
print("  E · FIGURES — greyscale legibility (T8.11)")
print("=" * 78)
out = Path(r"C:\Users\Admin\AppData\Local\Temp\claude\c--Users-Admin-Desktop-research-industry-5-0\4d82e16a-cff5-499e-b01b-74011f7805dd\scratchpad")
for n in ("fig1_architecture", "fig2_dataflow", "fig3_tradeoff", "fig4_comparison"):
    im = Image.open(ROOT / "figures" / f"{n}.png").convert("L")
    im.save(out / f"pre_{n}_gray.png")
    w, h = im.size
    print(f"  {n:20s} {w}x{h}  greyscale proof written")

print("\n" + "=" * 78)
print("  F · PAGE BUDGET")
print("=" * 78)
words = sum(len(t.split()) for s, t in paras
            if s in ("Body Text", "Abstract", "Keywords"))
nref = len([t for t in refs if t.strip()])
text_pages = words / 1150
extras = (2.72 + 2.82 + 2.26 + 2 * 3.74 + 1.5 + 1.9 + 1.8 + nref * 2 * 0.11) / (2 * 9.7)
print(f"  running text {words} words -> {text_pages:.1f} pages")
print(f"  figures, tables, references  -> +{extras:.1f} pages")
print(f"  ESTIMATE  ~{text_pages + extras:.1f} pages")
print("  (an estimate only — Word or LibreOffice is needed for the true count)")
