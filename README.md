# A Human-Centric Industry 5.0 Framework for Sustainable Smart Manufacturing Using Artificial Intelligence and Digital Twins

> Research project · ICARC · started 2026-08-03

---

## 1. The project in one sentence

Build a decision framework that maintains a digital twin of **both** sides of a
factory — the **machines** and the **operators** — couples them, and allocates
work by weighing **output (Profit)**, **the environment (Planet)** and
**operator well-being (People)** together; then test it against an Industry 4.0
baseline.

> The paper written from this work is titled *A Coupled Human–Machine Digital
> Twin Framework for Human-Centric and Sustainable Task Allocation in Industry
> 5.0* — see [`paper.docx`](paper.docx).

## 2. Contributions

| # | Contribution |
|---|---|
| **C1** | A **layered reference architecture** coupling a machine digital twin to a human digital twin through five explicitly defined bidirectional coupling points |
| **C2** | A **human digital twin** in which fatigue, skill and ergonomic risk are **quantified** and enforced as **hard constraints** on production decisions rather than as penalty terms |
| **C3** | **Quantitative evidence** from a 270-run co-simulation (3 policies × 3 scenarios × 30 seeds) against an Industry 4.0 baseline |

> ⚠️ The architecture specifies five layers; the fifth (explanation and operator
> override) is **specified but not implemented** in this study. See
> [docs/11-design-deviations.md](docs/11-design-deviations.md).

---

## 3. Where to start 👇

| Document | What it is | When to use it |
|---|---|---|
| 🚦 **[docs/00-START-HERE.md](docs/00-START-HERE.md)** | **Read this first** | Now |
| 📓 **[docs/09-worklog.md](docs/09-worklog.md)** | ★★★ What was done, what was decided, and what comes next | **Every session** |
| 📋 **[docs/02-task-board.md](docs/02-task-board.md)** | The master task list, in order | **Daily** |
| 📄 **[docs/12-paper-blueprint.md](docs/12-paper-blueprint.md)** | ★★★ Everything the paper needs: the framework, section-by-section plan, evidence, claims register | **Phase 8, first** |
| ⚠️ **[docs/11-design-deviations.md](docs/11-design-deviations.md)** | The 9 places the implementation departs from the frozen design | Phase 8 |
| 📝 [docs/01-project-charter.md](docs/01-project-charter.md) | Use case, objectives, research questions | Phase 1 |
| 📚 [docs/03-literature-review.md](docs/03-literature-review.md) | Search strategy, comparison table, gap statement | Phase 2 |
| 🏗️ [docs/04-framework-design.md](docs/04-framework-design.md) | 🔒 **FROZEN** — architecture, state equations, constraints | Phase 3 |
| 🧪 [docs/05-experiment-plan.md](docs/05-experiment-plan.md) | Datasets, baselines, scenarios, KPIs | Phases 4, 6, 7 |
| 📊 [docs/10-data-card.md](docs/10-data-card.md) | Dataset provenance and licences · ⚠️ one dataset is synthetic | Phases 4, 8 |
| ✍️ [docs/06-paper-outline.md](docs/06-paper-outline.md) | Paper structure and writing order | Phase 8 |
| ✅ [docs/13-reference-verification.md](docs/13-reference-verification.md) | All 33 references checked against Crossref, DataCite and source catalogues | Before submission |
| 🎬 [docs/14-demo-guide.md](docs/14-demo-guide.md) | How to demonstrate the system live, and what to say | Supervisor meetings |
| 🎯 [docs/08-competitor-destouet.md](docs/08-competitor-destouet.md) | The closest competing work, read in full | Phases 2, 8 |
| 📖 [docs/07-glossary.md](docs/07-glossary.md) | Technical terms in plain language | Any time |
| 📗 [paper/references.bib](paper/references.bib) | BibTeX library — 61 entries, 5 still marked `[CHECK]` | Phases 2, 8 |
| ✍️ [paper/section5-results.md](paper/section5-results.md) | §V draft, with the list of claims the results do **not** support | Phase 8 |

---

## 4. Repository layout

```
industry5.0/
├── README.md                  ← this file
├── paper.docx                 ← the paper, IEEE conference format
├── doc.docx                   ← the research explained in ten plain steps
├── docs/                      ← all planning and design documents
├── data/
│   ├── raw/                   ← downloaded datasets (not tracked; see the data card)
│   └── processed/             ← simulation inputs built from them
├── src/
│   ├── config.yaml            ← every parameter; nothing is hard-coded elsewhere
│   ├── loader.py              ← the only place configuration and data are read
│   ├── twins/                 ← MachineTwin, HumanTwin
│   ├── models/                ← fatigue, ergonomics, cognitive load, sustainability
│   ├── simulation/            ← SimPy factory, allocators, live shift view
│   └── decision/              ← constraint filter and weighted-sum selection
├── tests/                     ← 256 tests
├── results/                   ← experiment output (CSV)
├── figures/                   ← paper figures (SVG + PDF + PNG)
├── literature/                ← downloaded papers (not tracked; copyrighted)
└── paper/                     ← references.bib and section drafts
```

---

## 5. Running it

```bash
python -m pip install -r requirements.txt

python src/eda.py                 # estimate twin parameters from the datasets
python src/build_processed.py     # write the simulation inputs
python src/run_experiments.py     # 270 runs, about ten seconds
python src/analyse_results.py     # Table II with the statistics
python src/make_figures.py        # Figures 3 and 4

python -m pytest tests/ -q        # 256 tests
```

**Watch a single shift, epoch by epoch:**

```bash
python src/simulation/watch.py B2 S2     # Industry 4.0 under high demand
python src/simulation/watch.py B3 S2     # the proposed framework, same shift
```

---

## 6. Progress

| Phase | Name | Status |
|---|---|---|
| 1 | Foundation | ✅ **Complete · GATE 1 passed (2026-08-03)** |
| 2 | Literature review | 🟨 **46 studies (2018–2026; 51 screened), 9 read in full, gap statement ✅** |
| 3 | Framework design | ✅ **Complete · 🚪 GATE 3 passed (2026-08-04) — DESIGN FROZEN** |
| 4 | Data preparation | ✅ **Complete (2026-08-05)** — D1/D3/D4, data card, licences verified |
| 5 | Implementation | 🟨 **11/16** — twins, coupling, decision layer, 256 tests ✅ · NSGA-II, SHAP and dashboard **cut** |
| 6 | Experiments | ✅ **270 runs** (3 × 3 × 30), reproducible |
| 7 | Results analysis | ✅ **8/9** — Table II, 2 figures, 3 sensitivity studies, ablation, §V draft |
| 8 | Paper | 🟨 **Drafted** — `paper.docx` complete; author affiliation still to fill in |

**Headline result** (high demand, proposed vs Industry 4.0 baseline):
mean fatigue **−27.0%** · energy per unit **−30.8%** · constraint breaches
**79.5 → 0** · throughput **−1.8%** (p = 0.148, not statistically significant).

> ⚠️ **Nine departures from the frozen design are documented** in
> [docs/11-design-deviations.md](docs/11-design-deviations.md). The three
> largest — **NSGA-II, the explainability layer, and the machine-learning
> models** — were cut from scope, and all three belong in the paper's
> limitations section.
