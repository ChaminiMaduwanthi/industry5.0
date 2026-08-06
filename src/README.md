# src/ — Code

> **තත්ත්වය (2026-08-06):** Phase 4–7 ලියා අවසන්. **Tests 256ම pass.**
> ඉතුරු: T5.12 NSGA-II · T5.13 SHAP · T5.14 dashboard — **තුනම කැපුවා**
> ([11-design-deviations.md](../docs/11-design-deviations.md) D3, D4).

---

## ⛔ රීතිය 1 — කිසිම අගයක් hard-code කරන්න එපා

```
හැම parameter එකක්ම  →  src/config.yaml
හැම prepared file එකක්ම →  data/processed/*.csv
කියවන එකම තැන        →  src/loader.py
```

`loader.py` හැරෙන්නට **වෙන කිසිම module එකක් `config.yaml` හෝ CSV එකක් විවෘත කරන්නේ නෑ.**
ඒකයි T7.6b (λ, μ sensitivity) සහ T7.8 (ablation) කරන්න පුළුවන් වුණේ — ඒ අධ්‍යයන වැඩ කරන්නේ
**configuration එක වෙනස් කරලා**, ඒ නිසා code එකේ ලියපු අගයක් කියන්නේ **ඒ අධ්‍යයනවලට
ළඟා විය නොහැකි අගයක්**.

---

## 📁 ව්‍යුහය

```
src/
├── config.yaml                  ★ parameters සියල්ල · [FROZEN]/[TUNABLE]/[DATA]/[CALIB]
├── loader.py                    config + data/processed/ කියවන එකම තැන
│
├── eda.py                       T4.2  D1/D3/D4 → design §3 parameters
├── build_processed.py           T4.3/4.5/4.6  → data/processed/*.csv (+ assert vs design)
│
├── twins/
│   ├── machine_twin.py          T5.4  H · E · Q · A          (design §3)
│   └── human_twin.py            T5.7  ★ F · R · C · W        (design §4)
├── models/
│   ├── sustainability.py        T5.10 kWh/unit · CO₂e · scrap
│   └── human/
│       ├── fatigue.py           T5.8  ★ F(t+dt) = E* + (F−E*)e^(−ρΔt)
│       ├── ergonomics.py        T5.8  RULA + CP5
│       └── cognitive.py         T5.8  NASA-TLX proxy + CP3   ⚠️ තීරණයට ගන්නේ නෑ (D7)
├── simulation/
│   ├── entities.py              Machine · Operator · Task
│   ├── factory.py               T5.3  SimPy clock · allocators B1/B2/B3 · CP coupling
│   └── watch.py                 live terminal view (on_epoch hook)
├── decision/
│   ├── constraints.py           HC1–HC4 filter · SC1–SC3 penalty
│   └── weighted.py              T5.11 weighted sum (B3a) — filter කලින්, optimise පස්සේ
│
├── run_experiments.py           T6.5  3 × 3 × 30 = 270 runs
├── analyse_results.py           T7.1/7.2  Table II · Mann-Whitney U · Cliff's δ
├── make_figures.py              T7.3/7.4  fig3_tradeoff · fig4_comparison
│
├── sensitivity_hc1.py           HC1 0.70/0.80/0.90 — "ඇයි 0.80?"
├── sensitivity_fatigue.py       T7.6b ★ λ, μ × 0.5/1/2   🚪 GATE 3 carry-over
├── weight_sensitivity.py        T7.6  weight configs 4
├── ablation.py                  T7.8 ★ CP1–CP5
├── crosstraining.py             workload විශ්ලේෂණය (diagnosis, ප්‍රතිකාරයක් නොවේ)
├── feasibility.py               T5.16 deferral rate (design §12)
├── deferral_diagnosis.py        T5.16 ★ set එක වහන්නේ මොකක්ද
└── decision_pressure.py         §V.E.1 objective එකට ඉඩ කීයද
```

---

## ▶️ ධාවනය කරන අනුපිළිවෙල

```bash
python -m pip install -r ../requirements.txt

python src/eda.py                  # → results/eda_summary.md · data/processed/eda_params.json
python src/build_processed.py      # → data/processed/*.csv       (design සමීකරණ assert කරයි)
python src/run_experiments.py      # → results/raw_results.csv    (270 runs, ~10 s)
python src/analyse_results.py      # → results/kpi_table.{csv,md}
python src/make_figures.py         # → figures/fig3_*, fig4_*

# විශ්ලේෂණ
python src/sensitivity_fatigue.py  python src/weight_sensitivity.py
python src/ablation.py             python src/crosstraining.py
python src/feasibility.py          python src/deferral_diagnosis.py
python src/decision_pressure.py

python -m pytest tests/ -q         # 256 pass
```

---

## 🧪 Tests — 256

| File | ආවරණය |
|---|---|
| `test_invariants.py` | fatigue ∈ [0,1] · energy > 0 · HC1–HC4 · CP1–CP5 |
| `test_human_twin.py` | design §4 සමීකරණ — code එකට එරෙහිව නොව **design එකට** එරෙහිව |
| `test_b2_baseline.py` | B2 සාධාරණද · couplings ක්‍රියාත්මකද |
| `test_experiment_runner.py` | T6.7 reproducibility *(`runtime_sec` බැහැර කරයි — ඒක wall-clock)* |
| `test_analysis.py` | Mann-Whitney · Cliff's δ · Bonferroni · % ගණනය |
| `test_ablation.py` · `test_crosstraining.py` | |
| `test_sensitivity_fatigue.py` · `test_weight_sensitivity.py` | ★ knob එක **ඇත්තටම වැඩ කරනවද** |
| `test_deferral_diagnosis.py` | ★ fixed yardstick · configuration leak නෑ |
| `test_decision_pressure.py` | ★ probe එකෙන් run එක **වෙනස් වෙන්නේ නෑ** (byte-identical) |

> ★ **මේ repo එකේ පුරුද්ද: test එක මුලින්ම.** ඒක **තමන්ගේම වැරදි 6ක්** අල්ලලා තියෙනවා —
> විස්තර `docs/09-worklog.md`.

---

## ⚠️ Design එකෙන් අයිනට ගිය තැන්

**ලියලා තියෙන්නේ [docs/11-design-deviations.md](../docs/11-design-deviations.md) එකේ.**
ලොකුම 3: NSGA-II (D3) · L5 explainability (D4) · XGBoost models (D5) — **තුනම කැපුවා**,
තුනම **§VI Limitations එකට යන්නම ඕන**.
