# A Human-Centric Industry 5.0 Framework for Sustainable Smart Manufacturing Using Artificial Intelligence and Digital Twins

> පර්යේෂණ ව්‍යාපෘතිය · ICARC · ආරම්භය: 2026-08-03

---

## 1. මේ ව්‍යාපෘතිය එක වාක්‍යයකින්

කර්මාන්තශාලාවක **යන්ත්‍ර** සහ **සේවකයන්** යන දෙපාර්ශ්වයටම Digital Twin නිර්මාණය කර, AI මගින් ඒවා එකට සම්බන්ධ කරමින් —
**නිෂ්පාදනය (Profit)**, **පරිසරය (Planet)**, **සේවක සුබසාධනය (People)** යන තුනම එකවර සලකා තීරණ ගන්නා ආකෘතියක් (framework) ගොඩනැගීම සහ එය Industry 4.0 ක්‍රමයට එරෙහිව සත්‍යාපනය කිරීම.

## 2. ප්‍රධාන දායකත්ව 3 (Contributions)

| # | දායකත්වය |
|---|---|
| **C1** | Machine Digital Twin සහ Human Digital Twin එකට සම්බන්ධ කරන **layer 5ක reference architecture** එකක් |
| **C2** | Fatigue, Skill, Ergonomic risk යන මිනිස් සාධක **සංඛ්‍යාත්මකව (quantified)** නිෂ්පාදන තීරණවලට hard constraint ලෙස ඇතුළත් කරන **Human Digital Twin model** එකක් |
| **C3** | Replication 30ක co-simulation අධ්‍යයනයකින්, Industry 4.0 baseline එකට එරෙහිව **ප්‍රමාණාත්මක සාක්ෂි** |

---

## 3. ලේඛන මාර්ගෝපදේශය (මුලින්ම කියවන්න 👇)

| ලේඛනය | මොකටද | කවදාද පාවිච්චි කරන්නේ |
|---|---|---|
| 🚦 **[docs/00-START-HERE.md](docs/00-START-HERE.md)** | **මුලින්ම මේක කියවන්න** | දැන් |
| 📓 **[docs/09-worklog.md](docs/09-worklog.md)** | ★★★ **කරපු දේ + ගත්ත තීරණ + ඊළඟට මොකද** | **හැම session එකකම** |
| 📋 **[docs/02-task-board.md](docs/02-task-board.md)** | **ප්‍රධාන කාර්ය ලැයිස්තුව** — කරන්න තියෙන හැම දෙයක්ම, පිළිවෙලට | **හැමදාම** |
| 📝 [docs/01-project-charter.md](docs/01-project-charter.md) | Use case, Objectives, RQs — පදනම | Phase 1 |
| 📚 [docs/03-literature-review.md](docs/03-literature-review.md) | Search strategy + comparison table + gap | Phase 2 |
| 🏗️ [docs/04-framework-design.md](docs/04-framework-design.md) | Architecture, variables, objective function | Phase 3 |
| 🧪 [docs/05-experiment-plan.md](docs/05-experiment-plan.md) | Datasets, baselines, scenarios, KPIs | Phase 4, 6, 7 |
| ✍️ [docs/06-paper-outline.md](docs/06-paper-outline.md) | Paper එකේ ව්‍යුහය + ලිවීමේ අනුපිළිවෙල | Phase 8 |
| 📖 [docs/07-glossary.md](docs/07-glossary.md) | තාක්ෂණික වචන — සිංහලෙන් සරලව | ඕනෑම වෙලාවක |
| 🎯 **[docs/08-competitor-destouet.md](docs/08-competitor-destouet.md)** | **ළඟම තරඟකරුවා** — full-text විශ්ලේෂණය + §III එකට ready-to-paste ඡේදය | Phase 2, 8 |
| 📗 [paper/references.bib](paper/references.bib) | BibTeX library — entries 43 (39 verified) | Phase 2, 8 |
| ✍️ [paper/section2-related-work.md](paper/section2-related-work.md) | **§II Related Work කෙටුම්පත** + Table I | Phase 2, 8 |

---

## 4. ෆෝල්ඩර ව්‍යුහය

```
ICARC/
├── README.md                 ← මේ ලේඛනය
├── docs/                     ← සියලුම සැලසුම් ලේඛන
├── data/
│   ├── raw/                  ← බාගත් datasets (වෙනස් නොකරන්න)
│   └── processed/            ← පිරිසිදු කරපු දත්ත
├── src/                      ← Python code
│   ├── twins/                ← MachineTwin, HumanTwin
│   ├── models/               ← AI models
│   ├── simulation/           ← SimPy factory
│   ├── decision/             ← Optimizer
│   └── dashboard/            ← Streamlit UI
├── results/                  ← Experiment output CSVs
├── figures/                  ← Paper එකට යන රූප (SVG + PDF + PNG)
├── literature/               ← බාගත් papers (open access PDF)
└── paper/                    ← LaTeX / Word කෙටුම්පත
```

---

## 5. දැන් කරන්න තියෙන දේ

👉 **[docs/00-START-HERE.md](docs/00-START-HERE.md)** විවෘත කරන්න.

---

## 6. ප්‍රගතිය

| Phase | නම | තත්ත්වය |
|---|---|---|
| 1 | පදනම හදාගැනීම | ✅ **අවසන් · GATE 1 පසුයි (2026-08-03)** |
| 2 | Literature Review | 🟨 **≈92% — papers 53, කියවා 10, gap v2 ✅, Related Work ✅, ★ Destouet full-text ✅ (2026-08-04)** |
| 3 | Framework Design ★ | ✅ **අවසන් · 🚪 GATE 3 පසුයි (2026-08-04) — DESIGN FROZEN** |
| 4 | දත්ත සකසාගැනීම | 🟨 **ඊළඟට මේක** |
| 5 | Implementation | ⬜ නොපටන් ගත් |
| 6 | Experiments | ⬜ නොපටන් ගත් |
| 7 | ප්‍රතිඵල විශ්ලේෂණය | ⬜ නොපටන් ගත් |
| 8 | Paper ලිවීම | ⬜ නොපටන් ගත් |
