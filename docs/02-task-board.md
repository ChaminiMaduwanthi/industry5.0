# 📋 Task Board — කරන්න තියෙන සියලුම වැඩ (පිළිවෙලට)

> මේක තමයි **ප්‍රධාන ලේඛනය**. හැමදාම මේක බලන්න.
> වැඩක් ඉවර වුණාම `⬜` එක `✅` කරන්න.

---

## තත්ත්ව සලකුණු

| සලකුණ | අර්ථය |
|---|---|
| ⬜ | නොපටන් ගත් |
| 🟨 | කරමින් පවතී |
| ✅ | අවසන් |
| ⛔ | අවහිර වී ඇත (බාධාවක් තියෙනවා) |
| 🚪 | **GATE** — මේක ඉවර නොකර ඊළඟ phase එකට යන්න එපා |
| ★ | ඉතා වැදගත් — වැඩිපුර වෙලාව දෙන්න |

---

## 🗓️ කාල සටහන (සමස්තය)

| Phase | නම | සති | දින (යෝජිත) |
|---|---|---|---|
| 1 | පදනම හදාගැනීම | 1 | Aug 03 – Aug 09 |
| 2 | Literature Review | 2 | Aug 10 – Aug 23 |
| 3 | Framework Design ★ | 1 | Aug 24 – Aug 30 |
| 4 | දත්ත සකසාගැනීම | 1 | Aug 31 – Sep 06 |
| 5 | Implementation ★ | 4 | Sep 07 – Oct 04 |
| 6 | Experiments | 1 | Oct 05 – Oct 11 |
| 7 | ප්‍රතිඵල විශ්ලේෂණය | 1 | Oct 12 – Oct 18 |
| 8 | Paper ලිවීම | 2 | Oct 19 – Nov 01 |

> ⚠️ දින ඔබේ conference deadline එකට අනුව සකසාගන්න.

---

# 🔵 PHASE 1 — පදනම හදාගැනීම

**ඉලක්කය:** මොකක්ද හරියටම කරන්නේ කියලා පිටු 1ක ලියාගැනීම.
**ප්‍රතිදානය:** `docs/01-project-charter.md` සම්පූර්ණ කිරීම.

| ID | කාර්යය | ලියන්නේ කොහේද | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T1.1** | Use case එක තෝරා නිශ්චිතව නිර්වචනය කරන්න (machine කීයද, operator කීයද, මොන වර්ගයේ වැඩද) | charter §1 | 1 දින | ✅ |
| **T1.2** | System boundary එක අඳින්න — මොනවද **ඇතුළත්**, මොනවද **බැහැර** | charter §2 | 0.5 දින | ✅ |
| **T1.3** | Objectives 3 ලියන්න (People / Planet / Profit) + එකිනෙකට KPI නම් | charter §3 | 0.5 දින | ✅ |
| **T1.4** | Research Questions 3 + Hypothesis ලියන්න | charter §4 | 1 දින | ✅ |
| **T1.5** | Scope limits සහ උපකල්පන (assumptions) ලියන්න | charter §5 | 0.5 දින | ✅ |
| **T1.6** | 🚪 **Supervisor ට පෙන්වා අනුමැතිය ගන්න** | charter §7 | 1 දින | ✅ **2026-08-03** |

> ✅ **PHASE 1 අවසන් — GATE 1 පසුයි (2026-08-03).**

> 💡 **උපදෙස:** මේ phase එක ඉක්මනට කරන්න හිතන්න එපා. මෙතන වැරදුනොත් සති 13ම නාස්ති වෙනවා.

---

# 🔵 PHASE 2 — Literature Review

**ඉලක්කය:** ඔබේ **gap** එක ඔප්පු කිරීම.
**ප්‍රතිදානය:** `docs/03-literature-review.md` + BibTeX library.

| ID | කාර්යය | ලියන්නේ කොහේද | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T2.1** | Reference manager එකක් setup කරන්න (Zotero නිර්දේශ කරනවා — නොමිලේ) | — | 0.5 දින | ⬜ |
| **T2.2** | Search strings 6 run කරලා results export කරන්න | litreview §1 | 1 දින | ✅ **papers 33** |
| **T2.3** | **Screening 1:** Title + Abstract කියවලා ~80ක් තෝරන්න | litreview §2 | 2 දින | ✅ **52** |
| **T2.4** | **Screening 2:** Full paper කියවලා **30–40ක්** අවසන් කරන්න | litreview §2 | 3 දින | 🟨 **8/30 කියවා ඇත** |
| **T2.5** | Comparison table එක පුරවන්න (paper එකකට පේළියක්) | litreview §3 | 3 දින | ✅ **කණ්ඩායම A (8) · B (44)** |
| **T2.6** | 🚪 ★ **Gap statement එක ලියන්න** | litreview §4 | 1 දින | ✅ **v2 · citation-backed** |
| **T2.7** | Related Work කොටසේ **කෙටුම්පත** ලියන්න (පිටු 1) | `paper/section2-related-work.md` | 2 දින | ✅ **≈870 වචන + Table I** |
| **T2.8** | `references.bib` හදන්න | `paper/references.bib` | — | ✅ **entries 43** |
| **T2.9** | BibTeX entries metadata තහවුරු කරන්න | `paper/references.bib` | 1 දින | ✅ **39 තහවුරු · 4 `[CHECK]`** |
| **T2.10** | Backward citation chasing — `gaffinet2025hdtslr` reference list (113) | litreview §3 | 1 දින | ✅ **අලුත් 19** |

> ⚠️ **T2.6 එක ඉතාම වැදගත්.** Gap එක පැහැදිලි නැත්නම් paper එක reject වෙනවා.

### 📊 Phase 2 ප්‍රගතිය — 2026-08-03 (round 3 · **≈90% අවසන්**)

**✅ ලැබුණු දේ:**
- Papers **52ක්** හඳුනාගෙන කණ්ඩායම් 11කට වර්ග කර ඇත
- ළඟම competitors **8ක් කියවා** තහවුරු කර ඇත
- ★★ **Gap statement v2** — **තරඟකරුවන්ගේම වචන 3ක්** සාක්ෂි ලෙස
- ★★ **"තුනම එකවර ✅" = 0 / 52** — gap එක **ප්‍රමාණාත්මකව** තහවුරු
- ★ Fatigue model citation — `calzavara2019rest` (λ/μ අපගේ සමීකරණයට හරියටම ගැලපේ)
- ★ Ethics citation — `cardin2022ethics` (T8.12 එකට)
- ★★ **`destouet2023survey`** — අපගේ ගැටලු අවකාශයේම survey එක (232 cites)
- `references.bib` — entries **43** (**39 metadata-verified**, 4 `[CHECK]`)
- ★ **Related Work කෙටුම්පත ලියා ඇත** — ≈870 වචන + Table I

**⏳ ඉතිරි දේ (ඔබ කරන්න):**
- කණ්ඩායම B වල `🔎`/`⬜` ඒවා කියවන්න → **10/30 → 30/30** (T2.4)
- Gap statement + Related Work හි `[N]` අවසන් සංඛ්‍යාව *(දැන් papers **53**)*
- `[CHECK]` **4ක්** තහවුරු කරන්න: `ma2010muscle`, `aidt2026critical`, `dtcarbon2025`, `xai2026quality`
- ~~**Destouet et al. (2024)** full-text කියවා Table I පේළිය තහවුරු කරන්න~~ ✅ **අවසන් · 2026-08-04**

### ✅ T2.4-D · Destouet full-text විශ්ලේෂණය — **අවසන් (2026-08-04)**

> 👉 **[08-competitor-destouet.md](08-competitor-destouet.md)** — papers **3ම** full text කියවා ඇත

| | |
|---|---|
| ✅ | Gap එක **පවතී** — Destouet papers 3ම **digital twin නෑ** (2026 එකේත් `digital twin` තියෙන්නේ reference list එකේ පමණයි) |
| ✅ | ★★★ **2026 dated competitor quote** — *"worker fatigue levels to prevent fatigue peaks"* ඔවුන්ම ඉල්ලනවා |
| ✅ | ඔවුන් ළඟ **Industry 4.0 baseline නෑ** — algorithms සංසන්දනය කරනවා, paradigms නෙවෙයි. **B2 එක තවම අලුත්** |
| ⚠️ | **අලුත් paper 1ක්** හම්බුණා → `destouet2026dynamic` (*Comp. & Oper. Res.* 186:107323) — bib එකට **එකතු කර ඇත** |
| ⛔ | **Novelty ලෙස ලියන්න එපා:** *objectives තුනක්* · *CO₂* · *disruption/resilience* · *NSGA-II* · *ML* — **ඔවුන් ඔක්කොම කරලා** |
| ★ | **ලියන්න ඕන novelty කරුණු 2:** ① **Digital twin layer** ② **Fatigue = dynamic state (λ/μ)** |

### 🎁 Phase 2 එකෙන් ලැබුණු **තීරණාත්මක** සොයාගැනීම් 4

| # | සොයාගැනීම | මොකට වැදගත්ද |
|---|---|---|
| **1** | **ක්ෂේත්‍රය කණ්ඩායම් 2කට බෙදිලා** — DT තියෙන අයට fatigue නෑ; fatigue තියෙන අයට DT නෑ | ඔබේ gap එක **ව්‍යුහාත්මකයි**, අහම්බයක් නෙවෙයි |
| **2** | **Löcklin et al. (2021):** *"require a bi-directional flow… machines as well as humans"* | ඔබේ **CP1–CP5 coupling points** වලට කෙලින්ම සාධාරණීකරණය |
| **3** | **Sharotry et al. (2022):** *"the need for a true personalized DT for an operator"* | ඔබේ **operator-specific λ, μ** තීරණයට සාධාරණීකරණය |
| **4** | ⚠️ **Destouet et al. (2024)** ළඟ People+Planet+Profit **තුනම** තියෙනවා | **ළඟම තරඟකරුවා.** ඔබේ වෙනස = **digital twin layer එක** — ඒක §III එකේ පැහැදිලිව කියන්න |

---

# 🔵 PHASE 3 — Framework Design ★★

**ඉලක්කය:** Code කරන්න කලින් **කඩදාසියේ** සම්පූර්ණ design එක.
**ප්‍රතිදානය:** `docs/04-framework-design.md` + architecture diagram.

| ID | කාර්යය | ලියන්නේ කොහේද | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T3.1** | Layer 5ක architecture diagram | `figures/fig1_architecture.svg` +PDF +PNG | 1 දින | ✅ **2026-08-04** |
| **T3.2** | **Machine Twin** variables + update rules | design §3 | 0.5 දින | ✅ |
| **T3.3** | ★ **Human Twin** variables + update rules | design §4 | 1 දින | ✅ |
| **T3.4** | Normalization + leakage-free calibration protocol | design §6 | 0.5 දින | ✅ |
| **T3.5** | ★ **Objective function** (weights w₁…w₅) | design §7 | 1 දින | ✅ |
| **T3.6** | **Constraints** — hard + soft + hysteresis + violation handling | design §8 | 0.5 දින | ✅ |
| **T3.7** | Data flow / coupling diagram (CP1–CP5) | `figures/fig2_dataflow.svg` +PDF +PNG | 1 දින | ✅ |
| **T3.9** | ★ λ, μ — calibrated parameters ලෙස නිර්වචනය + bounds + sensitivity | design §4.5 | 0.5 දින | ✅ **2026-08-04** |
| **T3.10** | CO₂ emission factor — **0.33 kgCO₂/kWh** (Ember 2025) | design §3.2 | 0.5 දින | ✅ **2026-08-04** |
| **T3.8** | 🚪🚪 **DESIGN FREEZE** | design §14 | 0.5 දින | ✅ **GATE 3 පසුයි · 2026-08-04** |

> ✅ **PHASE 3 අවසන් — GATE 3 පසුයි (2026-08-04).**
> Topic එක supervisor විසින්ම පවරන ලද බැවින් වෙනම sign-off එකක් blocker එකක් ලෙස නොසැලකේ.
> ⛔ **මෙතනින් පස්සේ design STRUCTURE එක වෙනස් කරන්න එපා.** Parameter values `config.yaml` හරහා වෙනස් කළ හැක.

### 🎁 Phase 3 එකෙන් ලැබුණු **තීරණාත්මක** සොයාගැනීම් 4

| # | සොයාගැනීම | බලපෑම |
|---|---|---|
| **1** | ★★ v1 හි fatigue සමීකරණය **Calzavara ගේ එක නොවේ** | නිවැරදි කළා. දැන් cite කරන ආකෘතියම පාවිච්චි කරනවා |
| **2** | ★★ **HC1 threshold එක පුද්ගලීකරණය කළ හැකියි** — AWL (Price 1990) මගින් | `0.80` දැන් **operator කෙනෙකුට වෙනස් නිරපේක්ෂ මට්ටමකට** පරිවර්තනය වෙනවා. ⚠️ **නමුත් `0.80` කියන ආන්තිකය අපගේ තේරීමකි — Price දෙන්නේ AWL එක පමණි** *(2026-08-05 නිවැරදි කිරීම; T7.6b sweep එකෙන් ආවරණයි)* |
| **3** | ⚠️ **NSGA-II එකට objectives 5ක් වැඩියි** | objectives **3** (People/Planet/Profit) කරා. Pareto front එකත් 3-D — plot කරන්න පුළුවන් |
| **4** | ★★★ **Design validation** — code ලියන්න කලින් සංඛ්‍යාත්මකව පරීක්ෂා කළා | OP1: rest 0ක් · OP3: 4ක් · OP2: 8ක් — **පුද්ගලීකරණය ක්‍රියාවෙන් ඔප්පු වුණා** (design §4.10) |

> 💡 මේකයි ඔබේ **contribution C1 සහ C2**.

---

# 🔵 PHASE 4 — දත්ත සකසාගැනීම

**ඉලක්කය:** Simulation එකට අවශ්‍ය සියලු දත්ත සූදානම් කිරීම.
**ප්‍රතිදානය:** `data/processed/` + data card.

| ID | කාර්යය | ලියන්නේ කොහේද | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T4.1** | Datasets 4–6 බාගන්න → `data/raw/` | expplan §1 | 0.5 දින | ✅ **08-05** |
| **T4.2** | EDA කරන්න — missing values, outliers, distributions | `src/eda.py` | 1 දින | ✅ **08-05** |
| **T4.3** | Cleaning + feature engineering | `data/processed/` | 1.5 දින | ✅ **08-05** |
| **T4.4** | ★ **Fatigue model එක literature එකෙන් තෝරන්න** + citation එක සටහන් කරන්න | design §4.1 | 1 දින | ✅ **08-04** |
| **T4.5** | Ergonomic scoring rules (RULA/REBA) නිර්වචනය කරන්න | `task_types.csv` | 0.5 දින | ✅ **08-05** |
| **T4.6** | Task types + Skill matrix හදන්න (operator × task) | `data/processed/` | 0.5 දින | ✅ **08-05** |
| **T4.7** | **Data card** ලියන්න — මොන දත්ත, කොහෙන්, license එක මොකක්ද | `docs/10-data-card.md` | 0.5 දින | ✅ **08-05** |

> ⚠️ **T4.4 එකේදී ඔබම fatigue සමීකරණයක් හදන්න එපා.** Literature එකෙන් පිළිගත් එකක් ගෙන cite කරන්න. නැත්නම් reviewers ප්‍රශ්න කරනවා.

## 🎁 Phase 4 එකෙන් ලැබුණු දේ (2026-08-05)

| එළියට ගත්ත parameter | අගය | ප්‍රභවය | Design |
|---|---|---|---|
| `L0` machine ආයුෂ | **216 busy-min** | D1, TWF සිදුවීම් | §3.1 |
| `e_idle` | **2.66 kWh/15min** | D3, Light_Load P5 | §3.2 |
| `Δe(L/M/H)` | **5.97 / 35.79 / 56.61** | D3, Load_Type | §3.2 |
| Baseline defect rate | **6.64%** | D4 | §3.3 |

> ⚠️ **Phase 4 හි හම්බුණු නිවැරදි කිරීම් 2 — පත්‍රිකාවට වැදගත්:**
> 1. **D1 (AI4I) යනු SYNTHETIC dataset එකකි.** expplan §2 හි *"real-world benchmark datasets"* →
>    *"public benchmark datasets"* ලෙස **වෙනස් කරන්න**. (D3, D4 ඇත්ත මිනුම්.)
> 2. **Machine ආයුෂ shift එකකට වඩා කෙටියි** (medium වැඩේ 204–234 min). Maintenance = **tool change**
>    ලෙස අර්ථකථනය කර `maintenance_minutes: 15` කළා. Phase 5 හි downtime කොටස මනින්න —
>    වැඩි නම් `config.yaml → machines.l0_scale_factor` වෙනස් කරන්න (**සමීකරණය නොවේ**).

---

# 🔵 PHASE 5 — Implementation ★★ (දිගම phase එක)

**ඉලක්කය:** ක්‍රියාත්මක වන prototype එකක්.
**ප්‍රතිදානය:** `src/` යටතේ ක්‍රියාකාරී code.

### 5A · පදනම (සති 1)

| ID | කාර්යය | File | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T5.1** | Python environment + `requirements.txt` setup | `requirements.txt` · `src/config.yaml` | 0.5 දින | ✅ **08-05** |
| **T5.2** | Git repo එකක් හදන්න (`git init`) + `.gitignore` | `.gitignore` | 0.5 දින | ✅ **08-05** |
| **T5.3** | SimPy factory skeleton — clock, machines, operators, task queue | `src/loader.py` · `src/simulation/` | 3 දින | ✅ **08-05** |

> ✅ **T5.3 හි ලැබුණු දේ:** `loader.py` (config + CSV එක තැනකින්, validation සමඟ) ·
> `entities.py` (Task/Machine/Operator + Gini) · `factory.py` (SimPy clock, epoch 32,
> break policy, B1 random allocator, deterministic).
>
> ⚠️ **T5.4 එකේදී මුලින්ම කරන්න ඕන දේ 2:**
> 1. `factory.py` හි `_FAILURES_SUPPORTED = False` → **`True`** කරන්න.
>    ⛔ දැන් **S3 = S1** (machine failures නෑ). ඒක නොදැනුවත්ව results හදන්න එපා — warning එකක් print වෙනවා.
> 2. Machine **downtime කොටස** මනින්න (Phase 4 හි carry-over) → වැඩි නම් `l0_scale_factor`.

### 5B · Digital Twins (සති 1.5)

| ID | කාර්යය | File | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T5.4** | `MachineTwin` class ලියන්න | `src/twins/machine_twin.py` | 1 දින | ✅ **08-05** |

> ✅ **T5.4 හි ලැබුණු දේ:** H (§3.1) · E (§3.2) · Q (§3.3, **CP1 සජීවී**) · A (§3.4) ·
> maintenance · S3 breakdowns · scrap sampling · `watch.py` එකේ health bars.
>
> ✅ **Phase 4 carry-over විසඳුනා — machine downtime 3.4% විතරයි.** `l0_scale_factor`
> වෙනස් කරන්න ඕන නෑ. (බය වුණේ machine එක shift එකෙන් අඩකට ඉවර වීම ගැන — ඒත් machine 5ක්
> operator 3කට ඇති නිසා ප්‍රශ්නයක් නෑ.)
>
> ⚠️ **T5.7 එකේදී නැවත බලන්න:** S3 හි throughput එකට බලපෑමක් **නෑ** (S1 හි 20%ක ඉඩක්
> තියෙන නිසා breakdowns අවශෝෂණය වෙනවා). S3 හි ඇත්ත සංඥාව = *"machine කැඩුණම B2 මිනිසාව
> තල්ලු කරනවද?"* — ඒක **fatigue එකෙන් විතරයි පේන්නේ**. T5.7 ට පස්සෙත් S3 නිශ්චලනම්
> → `S3.demand_multiplier` වැඩි කරන්න.
| **T5.5** | M-DT AI models train කරන්න — RUL, Energy, Quality (XGBoost) | `src/models/` | 2 දින | ⬜ |
| **T5.6** | Model evaluation — RMSE/F1 report කරන්න | `results/model_eval.csv` | 0.5 දින | ⬜ |
| **T5.7** | ★★ `HumanTwin` class ලියන්න | `src/twins/human_twin.py` | 1.5 දින | ✅ **08-05** |
| **T5.8** | ★ Fatigue + Ergonomic + Cognitive load models | `src/models/human/` | 2 දින | ✅ **08-05** |
| **T5.9** | Twin දෙක simulation clock එකට සම්බන්ධ කරන්න (co-simulation) | `src/simulation/` | 1 දින | ✅ **08-05** |

### 5C · තීරණ ස්ථරය (සති 1)

| ID | කාර්යය | File | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T5.10** | Sustainability tracker — kWh/unit, CO₂e, scrap % | `src/models/sustainability.py` | 1 දින | ✅ **08-05** |
| **T5.11** | Decision layer **v1: Weighted sum** (සරල එක — මුලින්ම මේක) | `src/decision/weighted.py` | 2 දින | ✅ **08-05** |
| **T5.12** | Decision layer **v2: NSGA-II** (pymoo) → Pareto front | `src/decision/nsga2.py` | 2 දින | ⬜ |

### 5D · මානුෂීය අතුරුමුහුණත (සති 0.5)

| ID | කාර්යය | File | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T5.13** | SHAP integration — AI තීරණය පැහැදිලි කිරීම (XAI) | `src/decision/explain.py` | 1 දින | ⬜ |
| **T5.14** | ★ Streamlit dashboard + **operator override button** | `src/dashboard/app.py` | 2 දින | ⬜ |
| **T5.15** | 🚪 Unit tests + sanity checks (fatigue 0–1 අතරද? energy ධනද?) | `tests/` | 1 දින | 🟨 **පටන් ගත්තා 08-05** |

> 🟨 **T5.15 කලින්ම පටන් ගත්තා** — `tests/test_invariants.py` (checks 124, ඔක්කොම pass).
> **හේතුව:** T5.4 එකේ **HC4 ක්‍රියාත්මක වෙලාම නැති bug එකක්** තිබුණා, සහ ඒක **ප්‍රතිඵල දිහා
> බැලුවම පේන්නේ නෑ** — invariant test එකකින් විතරයි අල්ලුනේ. *(worklog බලන්න.)*
>
> ⬜ **තව එකතු කරන්න ඕන (twins ආවම):** fatigue `[0,1]` ද · HC1 කැඩෙනවද ·
> AWL ට යටින්ද · energy ධනද · CP1–CP5 ක්‍රියාත්මකද.
| **T5.16** | ★ **GATE 3 carry-over:** `constraint_deferrals` අනුපාතය මනින්න (epochs 640) | `results/feasibility.csv` | 0.5 දින | 🟨 **මැනුවා 08-05 — තීරණය ඉතුරුයි** |

> ⚠️ **T5.16 (design §12 එකෙන් එනවා):** deferrals **>15%** නම් → HC1 එක 0.85 දක්වා ලිහිල් කරන්න
> **හෝ** operator profiles සකසන්න. **තීරණය `config.yaml` එකේ ලේඛනගත කරන්න.**

> 💡 **T5.11 මුලින්ම කරන්න, T5.12 ඊට පස්සේ.** සරල එක වැඩ කරනවා තහවුරු වුණාට පස්සේ complex එකට යන්න.
> 💡 **T5.14 override button එක** = human-centricity ඔප්පු කරන ප්‍රායෝගික සාක්ෂිය. අමතක කරන්න එපා.

---

# 🔵 PHASE 6 — Experiments

**ඉලක්කය:** Baseline 3 × Scenario 3 × Seed 30 = **run 270ක්**.
**ප්‍රතිදානය:** `results/raw_results.csv`

| ID | කාර්යය | File | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T6.1** | **B1** — Random / Round-robin baseline | `src/baselines/b1_random.py` | 0.5 දින | ⬜ |
| **T6.2** | ★★ **B2** — Industry 4.0 baseline (machine twin විතරයි, throughput විතරක් optimize) | `src/baselines/b2_industry40.py` | 1 දින | ⬜ |
| **T6.3** | **B3** — ඔබේ framework එක (Phase 5 එකෙන් එනවා) | `src/decision/` | — | ⬜ |
| **T6.4** | Scenario 3 නිර්වචනය — Normal / High-demand / Breakdown | expplan §5 | 0.5 දින | ✅ **08-05** |
| **T6.5** | Experiment runner ලියන්න — 30 seeds × 3 baselines × 3 scenarios | `src/run_experiments.py` | 1 දින | ⬜ |
| **T6.6** | සියලු runs ධාවනය + logging | `results/raw_results.csv` | 1 දින | ⬜ |
| **T6.7** | Reproducibility check — seed එකම දුන්නම එකම උත්තරයද? | — | 0.5 දින | ⬜ |

> ⚠️ **T6.2 (Industry 4.0 baseline) එක නැත්නම් paper එකට අගයක් නෑ.** "5.0 හොඳයි" කියන්න "4.0" එකට එරෙහිව පෙන්නන්නම ඕන.
> ⚠️ **එක run එකක ප්‍රතිඵල දාන්න එපා.** Runs 30ක් + mean ± std අවශ්‍යයි.

---

# 🔵 PHASE 7 — ප්‍රතිඵල විශ්ලේෂණය

**ඉලක්කය:** Tables + Figures සූදානම් කිරීම.
**ප්‍රතිදානය:** `figures/` + `results/kpi_table.csv`

| ID | කාර්යය | ප්‍රතිදානය | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T7.1** | KPI table හදන්න — B1 vs B2 vs B3, KPI 6ක් | `results/kpi_table.csv` | 1 දින | ⬜ |
| **T7.2** | ★ සංඛ්‍යානමය පරීක්ෂාව — Mann-Whitney U + effect size | `results/stats.csv` | 1 දින | ⬜ |
| **T7.3** | ★ **Fig 3: Pareto front** — efficiency vs wellbeing trade-off | `figures/fig3_pareto.png` | 1 දින | ⬜ |
| **T7.4** | **Fig 4:** Baseline comparison bar chart | `figures/fig4_comparison.png` | 0.5 දින | ⬜ |
| **T7.5** | **Fig 5:** Dashboard screenshot + SHAP explanation | `figures/fig5_dashboard.png` | 0.5 දින | ⬜ |
| **T7.6** | Sensitivity analysis — weights (w₁…w₅) වෙනස් කලාම මොකද වෙන්නේ? | `results/sensitivity.csv` | 1.5 දින | ⬜ |
| **T7.6b** | ★★ **GATE 3 carry-over:** **λ, μ** sensitivity — 0.5× · 1× · 2× | `results/sensitivity_fatigue.csv` | 0.5 දින | ⬜ |
| **T7.8** | ★★ **Ablation:** CP1–CP5 ක්‍රියා විරහිත කර B3 run කරන්න | `results/ablation.csv` | 1 දින | ⬜ |
| **T7.7** | ප්‍රතිඵල අර්ථ නිරූපණය — **trade-off කතාව** ලියන්න | notes | 0.5 දින | ⬜ |

> ⚠️ **T7.6b අනිවාර්යයි.** λ, μ **calibrated** parameters (measured නෙවෙයි) නිසා, scaling එකෙන්
> **B2 vs B3 ranking එක වෙනස් නොවන බව** පෙන්නන්නම ඕන. එහෙම නම් නිගමන **robust**. (design §4.5)
>
> ✅ **T7.6b හි HC1 කොටස ඉවරයි (2026-08-05):** `src/sensitivity_hc1.py` · `results/sensitivity_hc1.csv`
> HC1 = **0.70 / 0.80 / 0.90** තුනේම, scenario 3ේම — සීමා සහිත ක්‍රමය මානුෂීය මිනුම් 5ම මත ජය ගනී.
> ⬜ **ඉතුරු:** λ, μ scaling (B2 හැදුවම — T6.2).
>
> ⚠️ **ඇයි HC1 එකතු කළේ:** `0.80` කියන්නේ **අපගේ ආරක්ෂක ආන්තිකයකි** — Price (1990) දෙන්නේ
> **AWL එක පමණි**. λ/μ ගේම තත්ත්වය. ⛔ *"HC1 = 0.80 following Price (1990)"* ලෙස **ලියන්න එපා**.
> ⚠️ **T7.8 (ablation) — ඔබේ ප්‍රබලම සාක්ෂිය.** CP1–CP5 නැති කලාම framework එක Destouet ලාගේ
> static ආකෘතිය බවට පත් වෙනවා. **වෙනස = coupling එකේ ඇත්ත වටිනාකම.** (design §5)
>
> ⚠️ **T7.8 එකට තවත් හේතුවක් (2026-08-05 හි හම්බුණා):** `β₂` (skill→quality) සහ `β₃` (fatigue→quality)
> **කිසිම dataset එකකින් fit කරන්න බෑ** — SECOM හි operator features නෑ. ඒ නිසා ඒවා **λ, μ වගේම
> calibrated**. T7.8 එකෙන් ඒවා ඉවත් කලාම මොකද වෙන්නේ කියලා පෙන්නන එක **අනිවාර්යයි**.
> Calibration විස්තර: [10-data-card.md](10-data-card.md) §3 (D4).

> 💡 **Throughput ටිකක් අඩු වුණොත් ඒක වහන්න එපා.** ඒක තමයි ඔබේ ප්‍රධාන කතාව:
> *"Throughput 5%ක් අඩු කිරීමෙන් fatigue 35%ක් අඩු කළ හැක."* — මේක **දුර්වලකමක් නෙවෙයි, contribution එකක්.**

---

# 🔵 PHASE 8 — Paper ලිවීම

**ඉලක්කය:** පිටු 6ක conference paper එකක්.
**ප්‍රතිදානය:** `paper/main.pdf`

| ID | කාර්යය | පිටු | කාලය | තත්ත්වය |
|---|---|---|---|---|
| **T8.1** | Conference template එක බාගෙන setup කරන්න (IEEE format) | — | 0.5 දින | ⬜ |
| **T8.2** | ★ **§3 Proposed Framework** ලියන්න (මුලින්ම මේක!) | 1.75 | 2 දින | ⬜ |
| **T8.3** | **§2 Related Work** අවසන් කරන්න (T2.7 කෙටුම්පතෙන්) | 1.0 | 1 දින | ⬜ |
| **T8.4** | **§4 Implementation & Experimental Setup** | 0.75 | 1 දින | ⬜ |
| **T8.5** | ★ **§5 Results & Discussion** | 1.25 | 2 දින | ⬜ |
| **T8.6** | **§6 Limitations & Future Work** (අවංකව ලියන්න) | 0.25 | 0.5 දින | ⬜ |
| **T8.7** | **§1 Introduction** + contributions bullet 3 | 0.75 | 1 දින | ⬜ |
| **T8.8** | **§7 Conclusion** | 0.25 | 0.5 දින | ⬜ |
| **T8.9** | **Abstract + Keywords** (අන්තිමට) | — | 0.5 දින | ⬜ |
| **T8.10** | References පරීක්ෂාව — 30+ ද? 2020ට පස්සේ 60%+ ද? | — | 0.5 දින | ⬜ |
| **T8.11** | Figures පරීක්ෂාව — කළු-සුදු print කරලා කියවන්න පුළුවන්ද? | — | 0.5 දින | ⬜ |
| **T8.12** | ★ **Privacy / Ethics ඡේදය** ලියන්න (මිනිස් දත්ත නිසා අවශ්‍යයි) | — | 0.5 දින | ⬜ |
| **T8.13** | Plagiarism check (Turnitin) | — | 0.5 දින | ⬜ |
| **T8.14** | Supervisor review + සංශෝධන | — | 3 දින | ⬜ |
| **T8.15** | 🚪 **Submit** 🎉 | — | 0.5 දින | ⬜ |

> 💡 **§3 මුලින්ම, Introduction සහ Abstract අන්තිමට.** ප්‍රතිඵල දැනගත්තට පස්සේ ඒවා ලියන එක ගොඩක් පහසුයි.

---

# ⭐ කිසිසේත් අමතක නොකළ යුතු දේ 5

| # | දේ | Task ID | ඇයි |
|---|---|---|---|
| 1 | **Industry 4.0 baseline (B2)** | T6.2 | මේක නැත්නම් paper එකේ අගයක් නෑ |
| 2 | **Human Twin එක සංඛ්‍යාත්මක වීම** | T3.3, T5.7 | conceptual විතරක් නම් contribution එකක් නෙවෙයි |
| 3 | **Runs 30ක්** | T6.6 | එක run එකක් = reject |
| 4 | **Trade-off කතාව වහන්නේ නැතිව කීම** | T7.7 | ඒක තමයි Industry 5.0 හි හරය |
| 5 | **Privacy / Ethics ඡේදය** | T8.12 | මිනිස් දත්ත එකතු කරන නිසා reviewers අහනවා |

---

# 📌 දැන් කරන්න ඕන දේ

```
👉 T1.1 — Use case එක තෝරන්න
   docs/01-project-charter.md විවෘත කරලා §1 පුරවන්න
```
