# 🧪 Experiment Plan

> **Phase 4, 6, 7 සඳහා.** Tasks T4.x, T6.x, T7.x
> ඉලක්කය: *"මගේ framework එක Industry 4.0 ට වඩා හොඳයි"* කියා **ඔප්පු කිරීම**.

---

## §1 · Datasets (T4.1)

### බාගන්න ඕන ඒවා → `data/raw/`

| # | අවශ්‍යතාව | Dataset | ප්‍රභවය | ප්‍රමාණය | තත්ත්වය |
|---|---|---|---|---|---|
| **D1** | ⚙️ Machine failure | **AI4I 2020 Predictive Maintenance** | UCI ML Repository | 10k rows | ⬜ |
| **D2** | ⚙️ Degradation / RUL | **NASA C-MAPSS (Turbofan)** | NASA Prognostics Data Repo | ~20k | ⬜ |
| **D3** | ⚡ බලශක්තිය | **Steel Industry Energy Consumption** | UCI ML Repository | 35k rows | ⬜ |
| **D4** | 🔍 Quality / defect | **SECOM** | UCI ML Repository | 1.5k × 590 | ⬜ |
| **D5** | 😴 Stress / fatigue | **WESAD** | UniSiegen (wearables) | 15 subjects | ⬜ |
| **D6** | 🦴 Activity / posture | **UCI HAR** හෝ **PAMAP2** | UCI ML Repository | 10k | ⬜ |

> 💡 **අවම වශයෙන් D1, D3, D5** තුන ගන්න. අනිත් ඒවා optional.
> 💡 හැම dataset එකකම **license** එක බලලා data card එකේ ලියන්න.

### D1–D6 කොහෙන් මොකටද?

```
D1, D2  →  MachineTwin.health      (RUL model)
D3      →  MachineTwin.energy      (energy model)
D4      →  MachineTwin.quality     (defect model)
D5      →  HumanTwin.fatigue       (fatigue calibration)
D6      →  HumanTwin.ergo_risk     (posture/activity)
```

---

## §2 · Co-Simulation ක්‍රමවේදය (T4.4 – T4.6) ★

### ගැටලුව

> ⚠️ ලෝකයේ **machine + human දෙකම එකට ඇති කර්මාන්තශාලා dataset එකක් නෑ**.

### විසඳුම — Hybrid Co-Simulation

```
┌─────────────────────────────────────────────────────────────┐
│              SimPy Discrete-Event Simulation                │
│                    (එකම simulation clock)                    │
│                                                             │
│   ┌─────────────────────┐      ┌─────────────────────┐      │
│   │   MACHINE SIDE      │      │    HUMAN SIDE       │      │
│   │                     │      │                     │      │
│   │  ඇත්ත datasets      │      │  Empirically-       │      │
│   │  (D1–D4) වලින්      │      │  validated models   │      │
│   │  chalana ලද         │      │  (literature-cited) │      │
│   │                     │      │  + D5, D6 calibration│     │
│   └─────────────────────┘      └─────────────────────┘      │
│              ↕            coupling (CP1–CP5)      ↕         │
└─────────────────────────────────────────────────────────────┘
```

### Paper එකේ මෙසේ ලියන්න

> *"A hybrid co-simulation approach was adopted. Machine-side dynamics — degradation, energy consumption and defect generation — were driven by three public benchmark datasets: one synthetic dataset reproducing industrial predictive-maintenance statistics, and two derived from operational measurements in a steel plant and a semiconductor line. Operator-side dynamics were generated using literature-validated fatigue-recovery and RULA-based ergonomic models, with accumulation and recovery rates calibrated rather than measured and covered by a dedicated sensitivity analysis. Both sides were coupled within a single discrete-event simulation clock (SimPy), enabling bidirectional state exchange at each decision epoch."*

> ✅ මේක **පිළිගත් විද්‍යාත්මක ක්‍රමයක්**. හංගන්න දෙයක් නෑ — Methodology එකේ පැහැදිලිව කියන්න.
>
> ⚠️ **2026-08-05 දී නිවැරදි කළා (කලින් අනුවාදයේ වැරදි 2ක් තිබුණා):**
> 1. ❌ *"three **real-world** benchmark datasets"* → **D1 (AI4I) යනු synthetic** dataset එකකි.
>    ✅ දැන් *"public benchmark datasets"* සහ කුමන එකද synthetic කියලා පැහැදිලියි.
> 2. ❌ *"calibrated against the **WESAD** wearable stress corpus"* → **WESAD භාවිතා නොකරයි**
>    (තීරණය 2026-08-05, හේතු: [10-data-card.md](10-data-card.md) §5).
>    ✅ දැන් λ, μ *"calibrated rather than measured"* + T7.6b sensitivity ලෙස ලියා ඇත.

### Simulation parameters (T4.6)

| Parameter | අගය | සටහන |
|---|---|---|
| Machine ගණන | 5 | |
| Operator ගණන | 3 | |
| Task වර්ග | 3 | Light / Medium / Heavy |
| Shift දිග | 8 පැය (480 min) | |
| Decision epoch | 15 min | තීරණයක් ගන්නා පරතරය |
| Simulated shifts | 20 | එක run එකකට |
| Break policy | පැය 4කට පසු විනාඩි 30 | |
| Random seeds | 30 | 0–29 |

---

## §3 · Data Card (T4.7)

සෑම dataset එකකටම මේක පුරවන්න:

| Field | D1 | D3 | D5 |
|---|---|---|---|
| සම්පූර්ණ නම | `[...]` | `[...]` | `[...]` |
| ප්‍රභවය / URL | `[...]` | `[...]` | `[...]` |
| License | `[...]` | `[...]` | `[...]` |
| Rows / Subjects | `[...]` | `[...]` | `[...]` |
| Features පාවිච්චි කලේ | `[...]` | `[...]` | `[...]` |
| Missing values ගැන කලේ | `[...]` | `[...]` | `[...]` |
| Citation | `[...]` | `[...]` | `[...]` |

---

## §4 · Baselines (T6.1 – T6.3) ★★

| ID | නම | Twin පාවිච්චි කරයි | Optimize කරන්නේ | Constraints | අරමුණ |
|---|---|---|---|---|---|
| **B1** | Random / Round-robin | නෑ | කිසිවක් නෑ | නෑ | පහළම මට්ටම (sanity check) |
| **B2** | ★ **Industry 4.0** | Machine twin **විතරයි** | Throughput විතරයි | HC4 විතරයි (machine health) | **ප්‍රධාන සංසන්දනය** |
| **B3** | ★ **Proposed (Industry 5.0)** | Machine + Human twin | People/Planet/Profit | HC1–HC4 සියල්ල | **ඔබේ framework එක** |

### වැදගත් සටහන

> ⚠️ **B2 එක සාධාරණව හදන්න.** ඒක "දුර්වල" කරලා ඔබේ එක ජය ගන්නවා නම් ඒක **වංචාවක්** — reviewers ඒක අල්ලනවා.
>
> B2 එකට machine twin එකේ **සම්පූර්ණ බලය** දෙන්න. එකම වෙනස: **මිනිසා ගැන හිතන්නේ නෑ**.

### B3 හි variants (optional, තියෙනවා නම් හොඳයි)

| ID | නම | වෙනස |
|---|---|---|
| B3a | Proposed (Weighted sum) | සරල optimizer |
| B3b | Proposed (NSGA-II) | Pareto-optimal |
| B3c | Proposed + XAI + override | සම්පූර්ණ framework එක |

---

## §5 · Scenarios (T6.4)

| ID | නම | විස්තරය | පරීක්ෂා කරන දේ |
|---|---|---|---|
| **S1** | **Normal** | සාමාන්‍ය demand, machine සියල්ල හොඳින් | මූලික ක්‍රියාකාරීත්වය |
| **S2** | **High-demand** | Demand 150%, කාලය අඩුයි | 👷 **වෙහෙස පීඩනය** — මිනිසා රැක ගන්නවාද? |
| **S3** | **Disruption** | Shift මැදදී machine 2ක් කැඩෙනවා | 🛡️ **Resilience** — Industry 5.0 හි 3වන කුලුන |

> 💡 **S2 එකයි වැදගත්ම එක.** Demand වැඩි වුණාම Industry 4.0 ක්‍රමය මිනිසාව හිර කරනවා;
> ඔබේ framework එක HC1 නිසා ඒක වළක්වනවා. **ඒක ලස්සන ප්‍රතිඵලයක්.**

---

## §6 · Experiment Matrix (T6.5)

```
Baselines (3) × Scenarios (3) × Seeds (30)  =  270 runs
```

| | S1 Normal | S2 High-demand | S3 Disruption |
|---|---|---|---|
| **B1** Random | 30 runs | 30 runs | 30 runs |
| **B2** Industry 4.0 | 30 runs | 30 runs | 30 runs |
| **B3** Proposed | 30 runs | 30 runs | 30 runs |

### Runner එකේ ව්‍යුහය

```python
# src/run_experiments.py
for scenario in ["S1", "S2", "S3"]:
    for baseline in ["B1", "B2", "B3"]:
        for seed in range(30):
            result = run_simulation(scenario, baseline, seed)
            append_to_csv(result, "results/raw_results.csv")
```

### `raw_results.csv` හි columns

```
run_id, scenario, baseline, seed,
mean_fatigue, max_fatigue, mean_rula, workload_gini,
energy_kwh, energy_per_unit, co2e_kg, scrap_rate,
throughput, downtime_hrs, oee,
constraint_violations, runtime_sec
```

---

## §7 · KPI Table (T7.1)

> Paper එකේ **Table II** ලෙස යනවා. මේක තමයි ප්‍රධාන ප්‍රතිඵලය.

### S1 (Normal) සඳහා

| KPI | කුලුන | B1 Random | B2 Industry 4.0 | **B3 Proposed** | Δ vs B2 | p-value |
|---|---|---|---|---|---|---|
| Mean fatigue | 👷 | `[...]` | `[...]` | `[...]` | `[...]%` | `[...]` |
| Max fatigue | 👷 | | | | | |
| Mean RULA | 👷 | | | | | |
| Workload Gini | 👷 | | | | | |
| Energy/unit (kWh) | 🌱 | | | | | |
| CO₂e (kg) | 🌱 | | | | | |
| Scrap rate (%) | 🌱 | | | | | |
| Throughput (units) | 💰 | | | | | |
| Downtime (hrs) | 💰 | | | | | |
| OEE (%) | 💰 | | | | | |

> සියලු අගයන් **mean ± std** ලෙස ලියන්න (30 runs වලින්).
> S2, S3 සඳහාත් මේ table එකම හදන්න.

---

## §8 · සංඛ්‍යානමය පරීක්ෂාව (T7.2) ★

### කුමන test එකද?

```python
from scipy.stats import mannwhitneyu, shapiro

# 1. Normality බලන්න
stat, p = shapiro(b3_results)

# 2a. Normal නම් → t-test
# 2b. Normal නොවේ නම් → Mann-Whitney U  (බොහෝ විට මේක)
stat, p = mannwhitneyu(b2_results, b3_results, alternative='two-sided')
```

### Effect size එකත් දෙන්න (p-value විතරක් මදි)

```python
# Cliff's delta හෝ Cohen's d
d = (mean(b3) - mean(b2)) / pooled_std
```

| Effect size | අර්ථය |
|---|---|
| \|d\| < 0.2 | නොසැලකිය යුතු |
| 0.2 – 0.5 | කුඩා |
| 0.5 – 0.8 | මධ්‍යම |
| > 0.8 | විශාල ✅ |

> ⚠️ **Multiple comparisons:** KPI 10ක් test කරනවා නම් **Bonferroni correction** එකක් දාන්න (α = 0.05/10 = 0.005).

---

## §9 · Figures (T7.3 – T7.5)

| Fig | නම | වර්ගය | File |
|---|---|---|---|
| 1 | Framework Architecture | Diagram (draw.io) | `figures/fig1_architecture.png` |
| 2 | Twin Coupling / Data Flow | Sequence diagram | `figures/fig2_dataflow.png` |
| 3 | ★ **Pareto Front** — Throughput vs Fatigue | Scatter + front line | `figures/fig3_pareto.png` |
| 4 | Baseline Comparison | Grouped bar chart (KPI × B1/B2/B3) | `figures/fig4_comparison.png` |
| 5 | Fatigue over time (S2 scenario) | Line chart, B2 vs B3 | `figures/fig5_fatigue_time.png` |
| 6 | Dashboard + SHAP explanation | Screenshot | `figures/fig6_dashboard.png` |

### Fig 3 (Pareto) ඇයි වැදගත්?

```
  Fatigue
    ▲
0.8 │  ● B2 (Industry 4.0)
    │   ╲
0.6 │    ╲
    │     ╲___
0.4 │         ●───●  ← ඔබේ Pareto front
    │              ╲
0.2 │               ●
    └────────────────────► Throughput
       400   450   500  550
```
> මේ රූපයෙන් පෙන්නනවා: *"Throughput ටිකක් අත්හැරියොත් fatigue ගොඩක් අඩු කරන්න පුළුවන්."*
> **මේකයි ඔබේ paper එකේ ප්‍රධාන පණිවිඩය.**

---

## §10 · Sensitivity Analysis (T7.6)

Weight configs 4 (§5 of framework-design) යටතේ B3 run කරලා පෙන්වන්න:

| Config | Fatigue | Energy | Throughput | සටහන |
|---|---|---|---|---|
| W-Balanced | `[...]` | `[...]` | `[...]` | default |
| W-Human | `[...]` | `[...]` | `[...]` | fatigue අඩුම |
| W-Green | `[...]` | `[...]` | `[...]` | energy අඩුම |
| W-Profit | `[...]` | `[...]` | `[...]` | ≈ B2 වෙනවා ✅ |

> 💡 **W-Profit ≈ B2 වුණොත් ඒක ලොකු තහවුරු කිරීමක්** — ඔබේ framework එක Industry 4.0 එක **සාමාන්‍යකරණය** කරන එකක් බව පෙන්නනවා.

---

## §11 · Reproducibility Checklist (T6.7)

- [ ] සියලු random seeds fix කර ඇත (`numpy`, `random`, `torch`)
- [ ] `requirements.txt` version numbers සමඟ
- [ ] එකම seed → එකම ප්‍රතිඵලය (2 වතාවක් run කර පරීක්ෂා කරන්න)
- [ ] Dataset versions/dates සටහන් කර ඇත
- [ ] Config file එකක් (`config.yaml`) — hard-coded values නෑ
- [ ] `results/raw_results.csv` save කර ඇත
- [ ] Code එක GitHub එකේ (paper එකේ link එක දෙන්න — reviewers කැමතියි)
