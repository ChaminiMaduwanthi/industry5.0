# 📓 Work Log — කරපු දේ, දවසින් දවස

> **මේ ලේඛනයේ අරමුණ:** අලුත් session එකක් පටන් ගන්නකොට **මුලින්ම මේක කියවන්න**.
> එවිට කලින් කරපු දේ, ගත්ත තීරණ, සහ **ඊළඟට කරන්න ඕන දේ** එකපාරටම තේරෙනවා.
> ⚠️ අලුත් session එකකදී මේක නොකියවා පටන් ගත්තොත් — **කරපු වැඩ නැවත කරන්න වෙනවා**.

---

# 🗓️ 2026-08-05 (බදාදා) — Session 3

## ⏱️ සාරාංශය

| | |
|---|---|
| **කරපු ලොකු දේවල් 3** | ① පදනම (packages · `config.yaml` · git) ② **Phase 4 සම්පූර්ණයෙන්** ③ Data card + license තහවුරු කිරීම |
| **Phase තත්ත්වය** | Phase 3 ✅ FROZEN · **Phase 4 ✅ අවසන්** · Phase 2 ≈92% (ඉතුරු) |
| **ඊළඟ අදියර** | 🔵 **Phase 5 — Implementation (T5.3 SimPy factory)** |

---

## 📦 කොටස 1 — පදනම (T5.1, T5.2) ✅

**ඇයි ඉස්සරහට ගත්තේ:** task board එකේ මේවා Phase 5. ඒත් `simpy`, `xgboost`, `pymoo` **install කරලා තිබුණේ නෑ** — EDA එකවත් කරන්න බැහැ. තවද folder එක **git repo එකක්වත් නොවීය** (backup එකක් නැති තත්ත්වයක්).

```
Python 3.13.14
✅ දැනටමත් තිබුණා : pandas 2.3.2 · numpy 2.3.3 · scikit-learn 1.9.0
✅ අලුතෙන් දැම්මා  : simpy 4.1.2 · xgboost 3.4.0 · pymoo 0.6.2 · shap 0.52.0
                    streamlit 1.61.0 · PyYAML 6.0.2 · scipy 1.16.2
                    matplotlib 3.10.6 · seaborn 0.13.2 · pytest 9.1.1
```

> ✅ **සැලසුමේ අවදානම #2 විසඳුනා:** xgboost සහ pymoo **Python 3.13 එකේ වැඩ කරනවා**.
> sklearn fallback එකට යන්න ඕන වුණේ නෑ.

### ★ `src/config.yaml` — අද හදපු වැදගත්ම ලිපිගොනුව

Design එකේ **හැම parameter එකක්ම** එකතැනකට ගෙනාවා (කොටස් 13ක්: simulation, tasks, operators, fatigue, ergonomics, machines, quality, sustainability, constraints, objective, normalization, experiment, sensitivity).

හැම අගයක්ම ලකුණු කර ඇත:

| ලකුණ | අර්ථය |
|---|---|
| `[FROZEN]` | GATE 3 හි ව්‍යුහය — වෙනස් කරන්න එපා |
| `[TUNABLE]` | වෙනස් කළ හැක → experiments නැවත run |
| `[DATA]` | dataset එකකින් එන්නේ — අතින් හදන්න එපා |
| `[CALIB]` | **අපි calibrate කරපු** — T7.6b එකෙන් ආවරණය විය යුතුයි |

> ⛔ `fatigue:` කොටසේ **λ, μ දෙක වටා පැහැදිලි අනතුරු ඇඟවීමක්** දාලා තියෙනවා —
> *"NEVER write 'as reported by Calzavara et al.' for these two numbers."*
> ➜ මාස 3කට පස්සේ අමතක වුණත් config එකෙන්ම මතක් වෙනවා.

### Git

`git init` + `.gitignore` — **files 28ක් staged**. `data/raw/` සහ `literature/*.pdf` **ignore වෙනවා**
*(literature PDF = copyrighted; public repo එකකට දාන්න බෑ)*.

✅ **Initial commit දැම්මා** — files 39, insertions 5,719.
Author: `Chamini Maduwanthi <chaminimaduwanthi97@gmail.com>` *(repo එකට local config)*.

---

## 📦 කොටස 2 — T4.1 Datasets ✅

| ID | ලැබුණා | ප්‍රමාණය |
|---|---|---|
| **D1** AI4I 2020 | ✅ | 522 KB → `ai4i2020.csv` |
| **D3** Steel Energy | ✅ | 482 KB → `Steel_industry_data.csv` |
| **D4** SECOM | ✅ | 1.96 MB → `secom.data` + labels |
| **D2** C-MAPSS | ✅ | 12.4 MB → txt 13ක් *(S3 mirror — `data.nasa.gov` බිඳී ඇත)* |
| **D5** WESAD | ⛔ **අත්හැරියා** | ↓ තීරණය බලන්න |

### ⛔ තීරණය — WESAD භාවිතා නොකරයි

**හේතු 3:**
1. **අවශ්‍යතාවය නැති වුණා** — λ, μ දැන් **T7.6b sensitivity** එකෙන් ආවරණය වේ (design §4.5)
2. **ගැලපීම දුර්වලයි** — WESAD = රසායනාගාර *stress* corpus; අපට ඕන *whole-body metabolic fatigue*.
   දුර්වල fit එකකට පහර දෙන එක, අවංක calibration ප්‍රකාශයකට පහර දෙනවාට වඩා **ලේසියි**
3. **පිරිවැය** — 2.25 GB + පැය 3ක්. ඒ කාලය T7.6b එකට වඩා හොඳයි

> 💡 පස්සේ ඕන නම්: `config.yaml → fatigue.operator_specific: true`. **design/code වෙනස් වෙන්නේ නෑ.**

---

## 📦 කොටස 3 — T4.2 EDA ✅ (`src/eda.py`)

**ක්‍රමවේදය:** සාමාන්‍ය EDA එකක් නොව — **design §3 එකට ඕන parameters හරියටම එළියට ගැනීම**.

### ★ එළියට ගත්ත සංඛ්‍යා

| Parameter | අගය | කොහොමද | Design |
|---|---|---|---|
| `L0` | **216 busy-min** | D1 හි **TWF** සිදුවීම් 46 හි මධ්‍යන්‍ය tool wear | §3.1 |
| `e_idle` | **2.66 kWh/15min** | D3 හි Light_Load හි **P5** (outlier-robust) | §3.2 |
| `Δe(L/M/H)` | **5.97 / 35.79 / 56.61** | D3, `Load_Type` අනුව | §3.2 |
| Defect rate | **6.64%** | D4 SECOM class balance | §3.3 |

**ඇයි TWF විතරක්?** Failure mode 5න් TWF විතරයි **සමුච්චිත ගෙවීමේ** ශ්‍රිතයක්. අනිත් ඒවා (තාපය, බලය, අධික බර) වෙනස් යාන්ත්‍රණ — ගෙවීම මත පදනම් ආයුෂ ඇස්තමේන්තුවකට වලංගු නෑ.

### ★★ D3 එකේ හම්බුණු ගැලපීම් 2

```
① Load_Type = Light_Load / Medium_Load / Maximum_Load
   → අපේ task types L / M / H ට හරියටම map වෙනවා

② නියැදි පරතරය = විනාඩි 15
   → අපේ decision epoch එකට හරියටම සමානයි  (පේළියක් = epoch එකක්)
```
➜ **මේ දෙක Methodology එකේ ලියන්න** — energy parameters ඇත්ත කර්මාන්ත මිනුම්වලින්.

### 📊 දත්තවල තත්ත්වය

| | D1 | D3 | D4 |
|---|---|---|---|
| Rows | 10,000 | 35,040 | 1,567 |
| **Missing** | **0** ✅ | **0** ✅ | 4.5% |
| Failure / defect rate | 3.39% | — | 6.64% |

---

## 📦 කොටස 4 — T4.3 / T4.5 / T4.6 ✅ (`src/build_processed.py`)

**හැදුණු ලිපිගොනු 4:** `machine_params.csv` · `operators.csv` · `task_types.csv` · `skill_matrix.csv`

### ★★ Design එකේ සමීකරණ **verify** කළා (assert සමඟ)

Script එක design එකේ අගය **විශ්වාස කරන්නේ නෑ** — ඒවා **නැවත ගණනය කරලා assert කරනවා**:

```
✅ Mifflin–St Jeor (1990)  E'_r  →  OP1 1.1658 · OP2 0.9047 · OP3 1.1337   design ට හරියටම සමානයි
✅ Price (1990)  AWL       →  OP1 5.3520 · OP2 3.6218 · OP3 4.5533          design ට හරියටම සමානයි
✅ ISO 8996  E'_w          →  L 2.581 · M 4.259 · H 5.937                   design ට හරියටම සමානයි
```

> 💡 **ඇයි මේක වටිනවා:** කවදාහරි `config.yaml` එකේ වයසක් හෝ බරක් වෙනස් කළොත්,
> code එක **වහාම කැඩෙනවා** — design ලේඛනයට නොදැනී වෙනස් වෙන්න බෑ.

### ★ Design §4.10 එකේ table එක **ප්‍රතිනිෂ්පාදනය වුණා**

```
        Light      Medium     Heavy
OP1      ok         ok       OVER AWL
OP2      ok       OVER AWL   OVER AWL      ← OP2 ට medium වැඩ දිගටම බෑ
OP3      ok         ok       OVER AWL
```
➜ ඊයේ අතින් කරපු ගණනය කිරීම **code එකෙන් තහවුරු වුණා**.

**HC2 (skill ≥ 0.40):** යුගල 9න් **1ක් අවහිර වෙනවා — OP1 × Heavy**. (Skill 0.30.)

---

## 📦 කොටස 5 — T4.7 Data Card ✅ (`docs/10-data-card.md`)

### ✅ License **ඇත්තටම පරීක්ෂා කළා** (memory එකෙන් නොවේ)

UCI පිටු 3ම fetch කරලා බැලුවා:

```
D1 (601) · D3 (851) · D4 (179)  →  Creative Commons Attribution 4.0 International
D2 C-MAPSS                      →  Public domain (US Gov)
```
➜ **පර්යේෂණයට සහ ප්‍රකාශනයට නිදහසේ භාවිතා කළ හැක** (attribution දුන්නොත්).

### `references.bib` — dataset citations 6ක් එකතු කළා

`matzka2020ai4i` · `matzka2020xai` · `sathishkumar2021steel` · `sathishkumar2021energy` · `mccann2008secom` · `saxena2008cmapss`

---

## ⚠️ අද හම්බුණු **නිවැරදි කිරීම් 3** — මේවා වැදගත්

### 1. ★★ D1 (AI4I) යනු **SYNTHETIC** dataset එකකි

UCI විස්තරයේම: *"is a **synthetic dataset** that reflects real predictive maintenance data"*.

```
⛔ ලියන්න බෑ : "three real-world benchmark datasets"      ← 05-experiment-plan.md §2 හි ඇත
✅ ලියන්න     : "three public benchmark datasets, one synthetic (D1) and
                two derived from operational measurements (D3, D4)"
```
> ⬜ **ඉතුරු වැඩක්:** `05-experiment-plan.md` §2 හි ඡේදය නිවැරදි කරන්න.

### 2. ⚠️ Machine ආයුෂ shift එකකට වඩා **කෙටියි**

```
Task L (κ=0.7):  291–334 min   (shift 0.61–0.69)
Task M (κ=1.0):  204–234 min   (shift 0.42–0.49)   ← shift එකකින් අඩකටත් අඩුයි
Task H (κ=1.4):  145–167 min   (shift 0.30–0.35)
```

**ඇයි:** D1 හි `Tool wear` කියන්නේ **මෙවලමේ** ආයුෂ, machine එකේ නොවේ.
**තීරණය:** maintenance = **tool change** ලෙස අර්ථකථනය → `maintenance_minutes: 45 → 15`.
*(45 කියන්නේ අද මම දාපු placeholder එකක් — design එකේ තිබුණේ නෑ, ඒ නිසා freeze එකට බලපෑමක් නෑ.)*

> ⬜ **Phase 5 හි පරීක්ෂා කරන්න (T5.16 එක්කම):** machine downtime කොටස මනින්න.
> මිනිසා පිළිබඳ කතාව යටපත් වෙනවා නම් → `config.yaml → machines.l0_scale_factor` **වැඩි කරන්න**.
> ⛔ **degradation සමීකරණය වෙනස් කරන්න එපා** — ඒක frozen.

### 3. D3 හි Light_Load **skewed** (mean/median = 2.6)

**Mean** තෝරාගත්තා. **හේතුව:** බලශක්තිය **එකතු වන** රාශියක් — shift එකක මුළු kWh එක අපේක්ෂිත අගයන්ගේ එකතුවයි. Median ගත්තොත් CO₂e **පද්ධතිමය වශයෙන් අඩුවෙන්** ගණන් වෙනවා. *(දෙකම report එකේ පෙන්නලා තියෙනවා — තේරීම දෘශ්‍යමානයි.)*

---

## 🔍 දවස අගදී කරපු DOUBLE-CHECK එක — හම්බුණු දේ 2

### ✅ හරි ගිය දේවල්

```
කියපු files 14ම    →  තියෙනවා
Datasets 4         →  extract වෙලා (cmapss 15 txt ඇතුළුව)
Determinism        →  data/processed/ + results/ මකලා ආයෙත් run කලාම
                      git එකට වෙනසක් නෑ  ✅  (byte-identical)
Design සමීකරණ      →  Mifflin · Price · ISO 8996 තුනම assert pass
config.yaml        →  කොටස් 15න් 6ක් දැන් පාවිච්චි වෙනවා;
                      ඉතුරු 9 Phase 5–7 ට (dead config නෙවෙයි)
```

### ⚠️ ප්‍රශ්නය 1 — `src/README.md` පරණ වෙලා

*"දැන් තවම හිස්"* කියලා තිබුණා — ඒත් එතන files **3ක්** තියෙනවා. **හැදුවා.**

### ⚠️⚠️ ප්‍රශ්නය 2 — Quality β coefficients **වැරදියි** (මේක වැදගත්)

`config.yaml` එකේ දාලා තිබුණු β අගයන් **mean එකට විතරක්** ගැලපෙන ඒවා. පරීක්ෂා කලාම:

```
Reference තත්ත්වයේ (H=1.0, S=0.70, F̂=0.30, κ=1.0)   →   6.98%   ✅ හොඳයි
HC1–HC4 අවසර දෙන WORST තත්ත්වයේ                      →  61.1%   ⛔ බෑ!
   (H=0.30, S=0.40, F̂=0.80, κ=1.4)
```

**කිසිම කර්මාන්තශාලාවක 61% defect rate එකක් නෑ.** Reviewer කෙනෙක් මේක අල්ලනවා.

**විසඳුම — anchor 2ක් පාවිච්චි කළා** (mean + boundary):

| β | පරණ | අලුත් |
|---|---|---|
| β₀ | −4.00 | **−3.360** |
| β₁ | 2.50 | **1.270** |
| β₂ *(skill, CP1)* | 1.50 | **0.762** |
| β₃ *(fatigue, CP2)* | 1.20 | **0.610** |
| β₄ | 0.60 | **0.305** |

```
දැන්:  reference      =  6.64%   ← SECOM හි මැනපු අගයට හරියටම
       worst feasible = 25.00%   ← යථාර්ථවාදී
```

✅ **Anchor දෙකම `build_processed.py` එකේ assert කරලා** — කවුරුහරි β වෙනස් කලොත් වහාම කැඩෙනවා.

### ★ මේකෙන් ආපු වැදගත් අවබෝධයක්

> **β₂ සහ β₃ කිසිම dataset එකකින් fit කරන්න බෑ** — SECOM හි operator features නෑ.
> ➜ ඒවා **λ, μ වගේම `[CALIB]`**. **ඒ කියන්නේ calibrated parameters 4ක් තියෙනවා, 2ක් නෙවෙයි.**
> ➜ λ, μ → **T7.6b** sensitivity එකෙන් ආවරණය
> ➜ β₂, β₃ → **T7.8** ablation එකෙන් ආවරණය *(task board එකට සටහන දැම්මා)*
> ➜ දෙකම **§VI Limitations** එකේ ලියන්න.

---

## 📁 අද වෙනස් වුණු / හැදුණු ලිපිගොනු

| ලිපිගොනුව | තත්ත්වය |
|---|---|
| `src/config.yaml` | 🆕 ★ **parameters සියල්ල** (කොටස් 13) |
| `src/eda.py` | 🆕 T4.2 |
| `src/build_processed.py` | 🆕 T4.3/T4.5/T4.6 + assert-based verification |
| `requirements.txt` · `.gitignore` | 🆕 T5.1 / T5.2 |
| `data/processed/*.csv` + `eda_params.json` | 🆕 5ක් |
| `results/eda_summary.md` · `results/eda/*.png` | 🆕 |
| `docs/10-data-card.md` | 🆕 T4.7 |
| `paper/references.bib` | ✏️ dataset citations **6ක්** |
| `docs/02-task-board.md` | ✏️ Phase 4 ✅ · T5.1, T5.2 ✅ |
| `docs/09-worklog.md` · `docs/00-START-HERE.md` | ✏️ |
| `data/raw/` | 🆕 datasets 4ක් *(git එකේ නෑ)* |

---

# 👉 හෙට මෙතනින් පටන් ගන්න

```
┌──────────────────────────────────────────────────────────────┐
│  🔵 PHASE 5 — Implementation  (දිගම phase එක)                │
│                                                              │
│  T5.3  ★ SimPy factory skeleton                              │
│        clock · machines 5 · operators 3 · task queue         │
│        → src/simulation/factory.py                           │
│                                                              │
│  T5.4  MachineTwin class    → src/twins/machine_twin.py      │
│  T5.7  ★★ HumanTwin class   → src/twins/human_twin.py        │
└──────────────────────────────────────────────────────────────┘
```

**⚠️ Phase 5 පටන් ගන්න කලින්:**
1. **`src/config.yaml` කියවන්න** — හැම අගයක්ම එතන. **කිසිම අගයක් code එකේ hard-code කරන්න එපා.**
2. `data/processed/` හි CSV 4 load කරන්න — machine, operator, task, skill parameters ඔක්කොම එතන
3. `src/README.md` හි ලිවීමේ අනුපිළිවෙල අනුගමනය කරන්න

**ඉතුරු කුඩා වැඩ:**
```
✅ git commit                      ← initial commit දාලා ඉවරයි (files 39)
✅ 05-experiment-plan.md §2        ← "real-world" → "public benchmark" + WESAD ඉවත් කළා
⬜ (optional) Sgarbossa ට email  →  fabio.sgarbossa@ntnu.no
```

> 💡 **Git පුරුද්ද:** session එකක් අවසන් වුණාම **commit එකක් දාන්න** — worklog එක යාවත්කාලීන
> කරන එකත් සමඟම. එවිට හැම session එකකටම save point එකක් තියෙනවා.

## 🎒 Phase 2 එකෙන් ඉතුරු (කැමති නම් සමාන්තරව)
```
- කණ්ඩායම B වල papers කියවන්න  →  10/30 → 30/30   (T2.4)
- Gap statement එකේ [N] සංඛ්‍යාව පුරවන්න
- [CHECK] 4ක් තහවුරු කරන්න
```

---
# 🗓️ 2026-08-04 (අඟහරුවාදා) — Session 2

## ⏱️ සාරාංශය

| | |
|---|---|
| **කරපු ලොකු දේවල් 3** | ① Destouet තරඟකරු විශ්ලේෂණය ② Phase 3 Framework Design ③ 🚪 GATE 3 වැසීම |
| **Phase තත්ත්වය** | Phase 2 ≈92% · **Phase 3 ✅ අවසන් (FROZEN)** |
| **ඊළඟ අදියර** | 🔵 **Phase 4 — දත්ත සකසාගැනීම (T4.1)** |

---

## 📦 කොටස 1 — Destouet ලාගේ papers 3 කියෙව්වා

**ඇයි:** ඔවුන් තමයි ළඟම තරඟකරුවා. *"ඔවුන්ට වඩා මොකද අලුත්?"* කියන ප්‍රශ්නයට උත්තර ඕන.

**කොහොමද:** ScienceDirect paywall — නමුත් **HAL** (ප්‍රංශ open archive) එකේ accepted manuscripts තිබුණා.
*(⚠️ තාක්ෂණික සටහන: HAL Anubis bot-protection එකෙන් wrap කරලා. `curl` default user-agent එකෙන් වැඩ කරනවා, browser UA එකෙන් නෑ.)*

### ★★ ලොකුම සොයාගැනීම 2

```
1. ඔවුන්ට 2026 දී අලුත් paper එකක් තියෙනවා  (Comp. & Oper. Research 186:107323)
   → ඒක අපේ library එකේ තිබුණේ නෑ
   → ඒකෙන් ඔවුන් CARBON + DYNAMIC + ML එකතු කරලා
   ⛔ ඒ නිසා ඒවා අපේ novelty ලෙස ලියන්න බෑ

2. ඒත් — papers 3ම DIGITAL TWIN එකක් හදලා නෑ
   → 2026 එකේ 'digital twin' කියන වචනය තියෙන්නේ REFERENCE LIST එකේ පමණයි
   ✅ ඒ නිසා අපේ ප්‍රධාන gap එක තවම ජීවතුන් අතර
```

### 🏆 ලැබුණු ප්‍රබලම උද්ධෘතය (ඔවුන්ගේම 2026 paper එකේ අන්තිම පිටුවේ)

> *"**Human factors:** A more refined model could account for **worker fatigue levels to prevent fatigue peaks during operations**. Additionally, the dynamic factors considered in this study are limited to operator absences, without addressing other disruptions such as **fluctuating worker efficiency or health-related constraints**."*

➜ **ළඟම තරඟකරුවා, 2026 දී, අපේ contribution එකම ඉල්ලනවා.** මේක §I හෝ §III එකේ දාන්න.

**📄 ප්‍රතිදානය:** [08-competitor-destouet.md](08-competitor-destouet.md) — §5 එකේ **§III එකට ready-to-paste English ඡේදයක්** තියෙනවා.

---

## 📦 කොටස 2 — Phase 3 Framework Design (T3.1 – T3.7)

**📄 ප්‍රතිදානය:** [04-framework-design.md](04-framework-design.md) **v2** — සම්පූර්ණයෙන් නැවත ලියා ඇත (§14ක්, 647 පේළි)
**🖼️ Figures 2:** `figures/fig1_architecture.svg` · `figures/fig2_dataflow.svg` — **SVG + PDF + PNG (300 dpi)**

### ⚠️ හම්බුණු ඇත්ත වැරදි 3 (v1 හි තිබුණු)

| # | වැරද්ද | නිවැරදි කිරීම |
|---|---|---|
| **1** | Fatigue සමීකරණය **Calzavara ගේ එක නොවේ** | ඇත්ත සමීකරණය හොයාගෙන දැම්මා (§4.1) |
| **2** | HC1 `0.80` හැමෝටම එකයි — **පුද්ගලීකරණය නෙවෙයි** | AWL මගින් **operator-specific** කළා (§4.2, §4.4) |
| **3** | NSGA-II එකට **objectives 5ක්** | **3ක්** කරා (People/Planet/Profit) (§7.2) |

### ★★ ගත්ත ලොකුම තීරණය — HC1 එකට භෞතික අර්ථයක්

```
කලින්:  F_h < 0.80          ← 0.80 කොහෙන්ද? උත්තරයක් නෑ
දැන්:   F̂ = (F − E'_r)/(AWL − E'_r) < 0.80
        ↑ "ඔබේ පෞද්ගලික තිරසාර සීමාවෙන් 80%"
```
- `E'_r` ← Mifflin et al. (1990) · `AWL` ← Price (1990), Silva et al. (2016)
- ➜ **හැම operator කෙනෙකුටම වෙනස්.** Sharotry ලා ඉල්ලපු *"true personalized DT"* එක මේකයි.

### 🎯 Code ලියන්න **කලින්** design එක පරීක්ෂා කළා (§4.10)

සමීකරණ ක්‍රියාත්මක කරලා shift එකක් simulate කළා (medium task දිගටම):

| Operator | AWL | Rest episodes | Busy |
|---|---|---|---|
| OP1 (පිරිමි 28) | 5.35 | **0** | 100% |
| OP3 (පිරිමි 47) | 4.55 | **4** | 88% |
| OP2 (ගැහැනු 35) | 3.62 | **8** | 75% |

➜ **පුද්ගලීකරණය ක්‍රියාවෙන් ඔප්පු වුණා** — hard-code කිරීමකින් තොරව, physiology එකෙන්.
➜ **මේක §V (Results) එකට දාන්න.** Destouet ලාගේ ස්ථිර 8% rest rule එකට මේක කරන්නම බෑ.

---

## 📦 කොටස 3 — 🚪 GATE 3 වැසුවා

### ✅ T3.10 — CO₂ emission factor

**v1 හි `0.53` කල් ඉකුත් වී තිබුණා.** Ember dataset එකෙන් ඇත්ත time series ගත්තා:

```
2017: 533 gCO₂/kWh   ← 0.53 කියන්නේ මේකයි
2025: 329 gCO₂/kWh   ← දැන් තියෙන්නේ මේක

✅ EF = 0.33 kgCO₂/kWh   (Ember 2025)
```

🛡️ **වැදගත්:** CO₂e = kWh × EF නිසා EF එක **ස්ථිර ගුණාකාරයක්** ➜ **B1/B2/B3 ranking එක EF තේරීමෙන් INVARIANT**. ඒ නිසා මේක ප්‍රතිඵලවලට අවදානමක් නොවේ.

### ⚠️ T3.9 — λ, μ · **අගයන් හම්බුණේ නෑ**

> ⛔⛔ **මේක හෙට අමතක කරන්න එපා:**
> **`λ = 0.020`, `μ = 0.046` කියන අගයන් කිසිම paper එකක නෑ. ඒවා අපි calibrate කරපු ඒවා.**

මාර්ග **8ක්** උත්සාහ කළා (IJPR, ResearchGate, NTNU, Visentin thesis, unipd ×2, PMC ×2, IFAC) — සමීකරණ ලැබුණා, **සංඛ්‍යා ලැබුණේ නෑ**.

**ගත්ත තීරණය:** ඒවා **calibrated parameters** ලෙස පැහැදිලිව ප්‍රකාශ කරනවා.
**හේතුව:** Calzavara ගේ λ, μ කියන්නේ **ඔවුන්ගේ subjects ගේ** heart-rate calibrated පෞද්ගලික අගයන්. අපේ operator ලා synthetic. ඒ නිසා ඒවා උපුටා ගැනීමත් සමානවම අත්තනෝමතිකයි — **calibrated කියලා ප්‍රකාශ කරන එක වඩා අවංකයි සහ වඩා ශක්තිමතුයි.**

**සාහිත්‍යගත සීමාව හම්බුණා:** Yi et al. (2022) *IJERPH* 19(2):930 — RR = **0.132 min⁻¹** (n=17, empirically fitted, එකම exponential ආකෘතිය). ඒක localized muscle — වේගවත්. අපේ එක whole-body metabolic — මන්දගාමී වීම **නිවැරදියි**.

**⚠️ නොකළොත් මේ විසඳුම වලංගු නෑ:**
- **T7.6b** — λ, μ sensitivity (0.5× · 1× · 2×)
- §6 Limitations එකේ *"calibrated rather than measured"*

**💡 ඕන නම් තවම ලබාගන්න පුළුවන්:** university library (IJPR 57(3):948–962) **හෝ** `fabio.sgarbossa@ntnu.no` ට email. ලැබුණොත් `config.yaml` එකේ අගය දෙක වෙනස් කරන්න විතරයි — **design/code වෙනස් වෙන්නේ නෑ**.

---

## 🔒 GATE 3 — Freeze එකේ නීති

> ⛔⛔ **හෙට වැඩ කරනකොට මේක උල්ලංඝනය කරන්න එපා.**

| ⛔ වෙනස් කරන්න **බැරි** (STRUCTURE) | ✅ වෙනස් කරන්න **පුළුවන්** (`config.yaml`) |
|---|---|
| Twin state variables (H,E,Q,A,U / F,S,R,C,W) | λ, μ අගයන් |
| Coupling points CP1–CP5 | EF (0.33) |
| Objective ව්‍යුහය (People/Planet/Profit) | Weights w₁…w₅ |
| Hard constraints HC1–HC4 | HC threshold අගයන් |
| Fatigue model ආකෘතිය | β, γ, ψ සංගුණක · Skill matrix |
| Normalization ක්‍රමය | |

---

## 📁 අද වෙනස් වුණු / හැදුණු ලිපිගොනු

| ලිපිගොනුව | තත්ත්වය |
|---|---|
| `docs/08-competitor-destouet.md` | 🆕 **අලුත්** — තරඟකරු විශ්ලේෂණය + ready-to-paste ඡේදය |
| `docs/09-worklog.md` | 🆕 **අලුත්** — මේ ලේඛනය |
| `docs/04-framework-design.md` | ✏️ **සම්පූර්ණයෙන් නැවත ලිව්වා** (v2, FROZEN) |
| `figures/fig1_architecture.{svg,pdf,png}` | 🆕 |
| `figures/fig2_dataflow.{svg,pdf,png}` | 🆕 |
| `literature/*.pdf` (5) | 🆕 බාගත් open-access papers |
| `paper/references.bib` | ✏️ 43 → **55** entries |
| `docs/02-task-board.md` | ✏️ Phase 3 ✅ · T5.16, T7.6b, T7.8 එකතු |
| `docs/03-literature-review.md` | ✏️ Table I + උද්ධෘත 4 |
| `README.md` · `docs/00-START-HERE.md` | ✏️ තත්ත්වය යාවත්කාලීන |

---

## ⛔ Paper එකේ ලියන්න **බැරි** දේ (අද තහවුරු වුණු)

```
✗ "අපි තමයි objectives තුනක් සලකන පළමු අය"     → Destouet 2024 කරලා
✗ "අපි තමයි CO₂ එකතු කරන පළමු අය"              → Destouet 2026 කරලා
✗ "අපි තමයි disruption/resilience කරන අය"      → Destouet 2026 කරලා
✗ "අපි තමයි ML/NSGA පාවිච්චි කරන අය"           → Destouet කරලා
✗ "λ = 0.020 as reported by Calzavara"        → ★ අසත්‍යයක්
✗ "අපි hard constraints, ඔවුන් soft penalty"   → ඔවුන්ටත් OCRA ≤ 2.2 තියෙනවා
```

## ✅ ලියන්න **පුළුවන්** novelty කරුණු 2

```
① ★★ DIGITAL TWIN LAYER      — ඔවුන්ගේ papers 3ම DT එකක් හදලා නෑ
② ★★ FATIGUE = DYNAMIC STATE — ඔවුන්ගේ එක static OCRA + ස්ථිර 8% rest
                                ★ ඔවුන්ම 2026 දී මේක ඕන කියලා ලියලා
```

---

# 👉 හෙට මෙතනින් පටන් ගන්න

```
┌──────────────────────────────────────────────────────────────┐
│  🔵 PHASE 4 — දත්ත සකසාගැනීම                                 │
│                                                              │
│  T4.1  Datasets බාගන්න → data/raw/                           │
│        ★ අවම වශයෙන්: D1 (AI4I 2020) · D3 (Steel Energy)      │
│                       D5 (WESAD)                             │
│        විස්තර: 05-experiment-plan.md §1                      │
│                                                              │
│  T4.2  EDA — missing values, outliers, distributions         │
│  T4.3  Cleaning + feature engineering                        │
│  T4.7  Data card (license එක අනිවාර්යයි)                     │
└──────────────────────────────────────────────────────────────┘
```

**⚠️ Phase 4 පටන් ගන්න කලින් කියවන්න ඕන:**
1. [04-framework-design.md](04-framework-design.md) §3 — machine twin එකට **මොන දත්තද** ඕන
2. [04-framework-design.md](04-framework-design.md) §4.5 — WESAD එකෙන් λ/μ calibrate කරන optional ක්‍රමය
3. [05-experiment-plan.md](05-experiment-plan.md) §1–§3 — dataset ලැයිස්තුව + data card

**💡 T4.4 (fatigue model තේරීම) දැනටමත් අවසන්** — design §4.1 එකේ. නැවත කරන්න එපා.

---

## 🎒 Phase 2 එකෙන් ඉතුරු වුණු දේ (කැමති නම් සමාන්තරව)

```
- කණ්ඩායම B වල papers කියවන්න  →  10/30 → 30/30   (T2.4)
- Gap statement එකේ [N] අවසන් සංඛ්‍යාව පුරවන්න     (දැන් papers 53)
- [CHECK] 4ක් තහවුරු කරන්න
```

> 💡 මේවා **Phase 4 එකට බාධාවක් නෙවෙයි**. Paper එක ලියන්න කලින් (Phase 8) කරලා තිබ්බාම ඇති.

---

# 🗓️ 2026-08-03 (සඳුදා) — Session 1

| | |
|---|---|
| **කරපු දේ** | Phase 1 සම්පූර්ණයෙන් (charter, use case, RQs, hypothesis) · Phase 2 ≈90% |
| **Gates** | 🚪 GATE 1 පසුයි · 🚪 GATE 2 (gap statement v2 ලියා ඇත) |
| **ප්‍රතිදාන** | `01-project-charter.md` · `03-literature-review.md` · `paper/section2-related-work.md` · `references.bib` (43) |
| **හම්බුණු දේ** | Papers 52 · competitors 8ක් කියවා · gap **ව්‍යුහාත්මක** බව තහවුරු (DT තියෙන අයට fatigue නෑ, fatigue තියෙන අයට DT නෑ) |
