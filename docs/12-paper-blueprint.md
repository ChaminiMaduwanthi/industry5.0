# 📄 Paper Blueprint — පත්‍රිකාවට ඕන **හැම දෙයක්ම**

> **හදපු දිනය: 2026-08-06.** මුල ඉඳන් (2026-08-03) කරපු **හැම දෙයක්ම** නැවත අධ්‍යයනය කරලා,
> තරඟකරුවන්ගේ papers **2ක ව්‍යුහය** කියවලා හදපු ලේඛනය.
>
> **මේක Phase 8 එකේ එකම reference එක.** ලියන්න වාඩි වුණාම මේක සහ
> [11-design-deviations.md](11-design-deviations.md) දෙක ළඟ තියාගන්න.

---

# 📑 අන්තර්ගතය

| කොටස | මොකද |
|---|---|
| **A** | ★★ **Framework එක ඇතුළේ තියෙන්නේ මොකක්ද** — අපි යෝජනා කරන දේ, සම්පූර්ණයෙන් |
| **B** | Framework paper එකක් ලියන්නේ කොහොමද — **තරඟකරුවන්ගෙන් ඉගෙනගත්තු දේ** |
| **C** | කොටස් අනුව blueprint — මොනවා ලියනවද, සාක්ෂිය කොහෙද, තත්ත්වය |
| **D** | සාක්ෂි ගබඩාව — තියෙන හැම සංඛ්‍යාවක්ම, table එකක්ම, figure එකක්ම |
| **E** | ★ Claims register — H1/H2 තීන්දු + **ලියන්න බැරි දේ 16** |
| **F** | ⛔ **පරතර පරීක්ෂාව** — ලියන්න පටන් ගන්න කලින් ඉතුරු දේ |

---

# 🏗️ A · FRAMEWORK එක ඇතුළේ තියෙන්නේ මොකක්ද

> **§III එකේ ලියන්නේ මේකයි.** පිටු 1.75, වචන 1,200 + Fig 1, 2 — **පත්‍රිකාවේ ලොකුම කොටස**.

## A.0 · එක වාක්‍යයකින්

> **Machine එකක තත්ත්වයත්, මිනිසෙකුගේ තත්ත්වයත් එකවර සජීවීව ආකෘතිගත කරලා, ඒ දෙක
> එකිනෙකට බලපාන ආකාරය පැහැදිලිව ලියලා, මිනිසාගේ සීමා `optimizer` එකට කලින්
> filter එකක් ලෙස බලාත්මක කරන කාර්ය බෙදාහැරීමේ framework එකක්.**

**Industry 4.0 එකට වඩා වෙනස වචන 3යි:** *filter, not penalty.*

---

## A.1 · ස්ථර 5 (Fig. 1)

```
╔═══════════════════════════════════════════════════════════════╗
║ L5 · HUMAN INTERFACE     Dashboard · SHAP · OVERRIDE          ║  ⚠️ නිර්වචනය
║                                                                ║     කරලා, ලියලා නෑ
╠═══════════════════════════════════════════════════════════════╣
║ L4 · DECISION            HC filter  →  weighted sum  →  w₁…w₅ ║  ✅
╠═══════════════════════════════════════════════════════════════╣
║ L3 · DIGITAL TWIN  ★★    M-DT ◄── CP1–CP5 ──► H-DT            ║  ✅ ★ හදවත
╠═══════════════════════════════════════════════════════════════╣
║ L2 · DATA                Ingest · Clean · Sync · Window       ║  ✅
╠═══════════════════════════════════════════════════════════════╣
║ L1 · PHYSICAL            machines 5 · operators 3 · sensors   ║  ✅ (SimPy)
╚═══════════════════════════════════════════════════════════════╝
```

| Layer | ආදානය | ප්‍රතිදානය | වගකීම |
|---|---|---|---|
| L1 | — | Raw readings | භෞතික තත්ත්වය |
| L2 | Raw | Time-aligned state vectors | දත්ත සූදානම |
| L3 | State vectors | Twin states + **coupled** updates | ★ තත්ත්ව ඇගයීම |
| L4 | Twin states | **Feasible** allocation | Optimisation |
| L5 | Allocation + explanation | මානුෂීය අනුමැතිය / override | පාලනය මිනිසා ළඟ |

> ⛔⛔ **L5 ලියලා නෑ** (deviations D4). *"our five-layer architecture"* කියලා **ලියන්න එපා**.
> ✅ ලියන්න: *"…is specified in the architecture (Fig. 1, L5) but is not implemented in this
> study; the results reported here come from layers L1–L4."*

---

## A.2 · Machine Digital Twin (M-DT) — §III-B

**State variables 5:**

| සංකේතය | නම | පරාසය | ප්‍රභවය |
|---|---|---|---|
| $H_m$ | Health index | [0,1] | D1 (AI4I) |
| $E_m$ | Energy rate | kWh/h | D3 (Steel) |
| $Q_m$ | Defect risk | [0,1] | D4 (SECOM) **+ CP1, CP2** |
| $A_m$ | Availability | {0,1} | Rule |
| $U_m$ | Utilisation | [0,1] | Counter |

**සමීකරණ 4:**

```
§3.1  H(t+Δt) = max(0, H(t) − Δt·κ_τ / L⁰)          idle නම් κ = 0 · maintenance → H ← 1
§3.2  E(t)    = e_idle + 1[busy]·Δe(τ)              CO₂e = kWh × EF
§3.3  Q       = σ(β₀ + β₁(1−H) + β₂(1−S) + β₃F̂ + β₄κ)          ★★ මෙතන twin දෙක හමුවෙනවා
§3.4  A(t)    = 1[H > 0.30] · 1[not under maintenance]
```

**දත්තවලින් ලබාගත් parameters:** `L⁰ = 216` busy-min · `e_idle = 2.66` kWh/15min ·
`Δe = 5.97 / 35.79 / 56.61` (L/M/H) · defect anchor `6.64%` · `EF = 0.33` kgCO₂/kWh.

---

## A.3 · ★★ Human Digital Twin (H-DT) — §III-C · **වැඩිම ඉඩ මෙතන**

> **මේකයි novelty එක.** Destouet ලා ළඟ තියෙන්නේ **task එකට ඇලවූ ස්ථිතික OCRA multipliers** —
> වෙහෙස **එකතු වෙන්නේ නෑ, විවේකයෙන් අඩු වෙන්නෙත් නෑ**. අපේ එක **සජීවී state එකක්**.

**State variables 6:**

| සංකේතය | නම | පරාසය | ඒකකය |
|---|---|---|---|
| $F_h$ | **Fatigue** (energy expenditure rate) | $[E'_r, \infty)$ | **kcal/min** |
| $\hat F_h$ | Normalized fatigue | [0,1] | — |
| $S_{h,\tau}$ | Skill | [0,1] | — |
| $R_h$ | Ergonomic risk (RULA) | [1,7] | — |
| $C_h$ | Cognitive load | [0,1] | — |
| $W_h$ | Workload share | [0,1] | — |

### ★ සමීකරණ 5 — **හැම එකකටම citation එකක් තියෙනවා**

```
§4.1  F(t+Δt) = E* + (F(t) − E*)·e^(−ρΔt)                     Calzavara et al. (2019) ආකෘතිය
         E* = E'_w(τ) වැඩ කරනවා නම් · E'_r විවේකයේ
         ρ  = λ වෙහෙසෙනකොට · μ යථා තත්ත්වයට එනකොට

§4.2  E'_r = (S + 10W + 6.25H_cm − 5·age)/1440                Mifflin et al. (1990)
      AWL  = (60 − 0.55·age)·0.005·W/3   පිරිමි                Price (1990), Silva (2016)
             (48 − 0.37·age)·0.005·W/3   ගැහැනු

§4.3  E'_w(τ) = (W/m²)_τ × A_Du × 0.01434                      ISO 8996 metabolic classes

§4.4  F̂ = clip((F − E'_r)/(AWL − E'_r), 0, 1)                 ★ භෞතික අර්ථය තියෙනවා

§4.7  R = clip(RULA_base(τ) + ψ₁F̂ + ψ₂v̂, 1, 7)               McAtamney & Corlett (1993)
§4.8  C = clip(c_τ + γ₁(1−H) + γ₂Q + γ₃(n−1)/(|M|−1), 0, 1)   Hart & Staveland (1988)
```

### ★★ **පුද්ගලීකරණය — මේක තමයි ලොකුම තර්කය**

Operator 3 දෙනාට **වෙනස් anthropometrics** ➜ **වෙනස් AWL** ➜ framework එක **තනිවම**
වෙනස් ආරක්ෂාවක් දෙනවා. **Hard-code කරලා නෑ — physiology එකෙන් එනවා:**

| Operator | ස්ත්‍රී/පු. | වයස | බර | උස | $E'_r$ | **AWL** | Medium වැඩ දරාගන්නවද |
|---|---|---|---|---|---|---|---|
| OP1 | පිරිමි | 28 | 72 | 175 | 1.166 | **5.352** | ✅ |
| OP2 | ගැහැනු | 35 | 62 | 163 | 0.905 | **3.622** | ⚠️ **බෑ** (E'_w = 4.26 > AWL) |
| OP3 | පිරිමි | 47 | 80 | 170 | 1.134 | **4.553** | ✅ |

> ★ **§III-C එකේ මේ table එක දාන්න.** OP2 ට medium වැඩ දිගටම බැරි වීම **bug එකක් නොවේ —
> ඒක framework එකේ අරමුණ.** ඒක **Sharotry et al. (2022) ඉල්ලපු *"true personalized DT"***.

**Skill matrix (§4.6):** OP1 {L .90, M .60, H **.30**} · OP2 {L .50, M .90, H .70} ·
OP3 {L .70, M .40, H .90} · processing time `p = p⁰/(0.5 + 0.5·S)`

---

## A.4 · ★★ Twin Coupling — CP1–CP5 (Fig. 2) — §III-D

> **මේකයි "coupled" කියන වචනයට තේරුමක් දෙන්නේ.** Löcklin et al. (2021) ඉල්ලපු
> *"bi-directional flow… machines as well as humans"* එකේ ක්‍රියාත්මක ස්වරූපය.

| # | සම්බන්ධතාවය | දිශාව | සමීකරණයේ පදය | **ඇත්තටම බලපානවද?** |
|---|---|---|---|---|
| **CP1** | Skill → Quality | H→M | $\beta_2(1-S)$ in $Q_m$ | ⚠️ redundant *(පහත)* |
| **CP2** | Fatigue → Quality | H→M | $\beta_3\hat F$ in $Q_m$ | ⚠️ redundant |
| **CP3** | Health → Cognitive | M→H | $\gamma_1(1-H)$ in $C_h$ | ගණනය කරයි, තීරණයට නෑ |
| **CP4** | Task intensity → Fatigue | M→H | $E'_w(\tau)$ = asymptote | ✅ ව්‍යුහාත්මක |
| **CP5** | Machine pace → Ergonomics | M→H | $\psi_2\hat v_m$ in $R_h$ | ★★ **මේක විතරයි තීරණ වෙනස් කරන්නේ** |

> ★★★ **T7.8 ablation එකේ අවංක ප්‍රතිඵලය — මේක ලියන්නම ඕන:**
> CP5 හැංගුවම shift එකකට **ඇත්ත ergonomic breaches 5.3ක්** (සම්පූර්ණ framework එකේ **0**).
> CP1, CP2 හැංගුවම **තීරණයක් වෙනස් වෙන්නේ නෑ** — ඒත් **අදාළ නොවීම නිසා නොවේ, redundancy නිසා**:
> ```
> Skill   →  processing time · skill-matching preference · competence floor   ← මං 3ක්
> Fatigue →  fatigue limit · objective එකේ fatigue පදය                        ← මං 2ක්
> Pace    →  ergonomic score එක විතරයි                                        ← මං 1යි ★
> ```

---

## A.5 · Decision layer — §III-E, §III-F

### පිළිවෙල — **මේක තමයි framework එකේ හරය**

```
epoch එකකට වරක් (15 min):

  1 · twin states update  (coupling ඇතුළුව)
  2 · HARD CONSTRAINT FILTER      ← ★★ optimizer එකට කලින්
  3 · optimise  (feasible set එක උඩ පමණයි)
  4 · [L5: explain + override]    ← නිර්වචනය කරලා, ලියලා නෑ
```

### Objective (§7.1)

$$\min_\pi Z = \underbrace{w_1\hat F + w_2\hat R}_{\text{👷 People}} + \underbrace{w_3\hat E + w_4\hat W}_{\text{🌱 Planet}} - \underbrace{w_5\hat T}_{\text{💰 Profit}}$$

Weight scenarios 4: W-Balanced (default) · W-Human · W-Green · W-Profit.

### ★★ Hard constraints — **Industry 5.0 හි හරය**

| # | සීමාව | තේරුම | Destouet ලා ළඟ තියෙනවද |
|---|---|---|---|
| **HC1** | $\hat F_h < 0.80$ | පෞද්ගලික තිරසාර සීමාවෙන් 80% | ❌ **නෑ** (fatigue state එකක්ම නෑ) |
| **HC2** | $S_{h,\tau} \ge 0.40$ | දක්ෂතාවය නැති කෙනෙකුට වැඩේ නෑ | ❌ **නෑ** |
| **HC3** | $R_h \le 5$ | RULA action level | ⚠️ සමානයි — ඒත් **ස්ථිතික** |
| **HC4** | $H_m > 0.30$ | කැඩෙන්න ළං machine එකට වැඩ නෑ | ❌ **නෑ** |

**Hysteresis:** F̂ ≥ 0.80 → mandatory rest, F̂ ≤ 0.60 වෙනකම් *(chattering වළක්වයි)*
**Soft constraints:** SC1 workload Gini · SC2 skill mismatch · SC3 machine switching

> ★★★ **§III-F එකේ දාන්නම ඕන වාක්‍යය** *(outline එකේ තියෙනවා — ඒක තමයි පත්‍රිකාවේ තර්කය)*:
> > *"The distinction between Industry 4.0 and Industry 5.0 optimisation is, in our
> > formulation, precisely the distinction between treating operator state as a soft penalty
> > and treating it as a hard constraint. Under the former, sufficient efficiency gain will
> > always justify operator strain; under the latter, it never can."*

---

# 📚 B · FRAMEWORK PAPER එකක් ලියන්නේ කොහොමද

> ළඟම තරඟකරුවන්ගේ papers **2ක්** (Destouet 2024 · CIE 195 සහ Destouet 2026 · COR 186)
> **ව්‍යුහය මට්ටමින් කියවා** ලබාගත් රටාව.

## B.1 · ඔවුන්ගේ ව්‍යුහය

```
1. Introduction
2. Related works            ← තේමා අනුව උප-කොටස් (energy · human factors · multi-objective)
3. PROBLEM DESCRIPTION      ← ★ 3.1 Assumptions → 3.2 Mathematical model
                                 3.2.1 Notations  3.2.2 Objective functions  3.2.3 Constraints
4. Algorithms description   ← ★ MODEL එකයි SOLVER එකයි වෙන් කරලා
5. Metrics and instances
6. Algorithms performance
7. Results and sensitivity analysis     ← sensitivity නමින්ම උප-කොටසක්
8. Conclusion
```

### ★ ඉගෙනගත්තු පාඩම් 4

| # | පාඩම | අපි කරන්නේ |
|---|---|---|
| **1** | **Assumptions මුලින්ම, ලැයිස්තුවක් ලෙස** — model එකට කලින් | §III මුලට assumption 5 (charter §5) |
| **2** | **Notation → Objectives → Constraints** කියන අනුපිළිවෙල | §III-B/C notation, §III-E objective, §III-F constraints |
| **3** | ★ **Model එකයි solver එකයි වෙන් කරන්න** | §III = model · §IV = SimPy + weighted sum + protocol |
| **4** | **Sensitivity යනු වෙනම නම් කරපු කොටසක්**, footnote එකක් නොවේ | §V-D — අපිට **3ක්** තියෙනවා (λμ · HC1 · weights) |

## B.2 · ★★ ඔවුන්ගේ Introduction එකේ **චලන 10** — අපිත් මේ අනුපිළිවෙලට

| # | චලනය | ඔවුන් | ➜ අපි |
|---|---|---|---|
| 1 | **සන්දර්භය** | *"Today's Industry 5.0 context is human-centered…"* | EU නිර්වචනය · කුලුනු 3 |
| 2 | **I4.0 → I5.0 සංක්‍රමණය** | I4.0 digitised; I5.0 adds resilience + social | එයම |
| 3 | **ක්ෂේත්‍රය වෙනස් වෙන්න ඕන** | scheduling must adapt: නව constraints, නව objectives | Digital twins **asset-centric** ය |
| 4 | **ක්ෂේත්‍රයේ තත්ත්වය** | NP-hard · methods ලැයිස්තුව | DT + human factors දෙපැත්තට බෙදිලා |
| 5 | ***"In this paper, we consider…"*** | SFJSSP එක නම් කරයි | Task allocation in a machining cell |
| 6 | ★ **පරතරය** | *"To the best of our knowledge, only a few…"* | **"Of the 46 studies… none couples"** |
| 7 | **දායකත්ව** | transport + setup + working hours | ★ bullet 3 *(§C.1 බලන්න)* |
| 8 | **ක්‍රමවේදය** | NSGA-II/III + Q-learning + VNS | Co-simulation · hard-constraint filter · weighted sum |
| 9 | **ඇගයීම** | instances · profiles · sensitivity | 270 runs · baselines 3 · scenarios 3 · sensitivity 3 |
| 10 | **ලිපියේ ව්‍යුහය** | *"The rest of this article…"* | එයම |

> 💡 **චලනය 6 ඔවුන් *"only a few works"* කියනවා. අපිට ඊට වඩා ශක්තිමත් එකක් තියෙනවා —
> ගණන් කරපු *"none of 46"*.** ඒක **ප්‍රමාණාත්මකයි**, ඔවුන්ගේ එක **ගුණාත්මකයි**.

## B.3 · ඔවුන්ගෙන් **ගන්න එපා** කියන දේ

```
✗ පිටු 40ක journal ව්‍යුහය   →  අපේ එක පිටු 6ක conference එකක්
✗ §6 "Algorithms performance"  →  අපි algorithm එකක් නොව FRAMEWORK එකක් යෝජනා කරනවා
✗ Chromosome coding විස්තර     →  අපේ solver එක weighted sum — විස්තර අවශ්‍ය නෑ
```

---

# 📝 C · කොටස් අනුව BLUEPRINT

> `✅` = ලියලා/සාක්ෂිය තියෙනවා · `🟨` = කොටසක් · `⬜` = ලියන්න ඕන

## C.0 · ලිවීමේ අනුපිළිවෙල (outline §1)

```
§III  →  §II  →  §IV  →  §V  →  §VI  →  §I  →  §VII  →  Abstract
```

## C.1 · §I Introduction (T8.7) — ¶6 · වචන 600

| ¶ | අන්තර්ගතය | සාක්ෂිය | තත්ත්වය |
|---|---|---|---|
| 1 | සන්දර්භය — I4.0 → I5.0, කුලුනු 3 | `breque2021industry50` · `xu2021industry45` | ✅ |
| 2 | ගැටලුව — DT asset-centric; මිනිසා "user", "modelled entity" නොවේ | `modoni2023hdt` · `toth2023i5arc` | ✅ |
| 3 | ★ පරතරය — **"Of the 46 studies… none couples"** | litreview §4 | ✅ |
| 4 | අපගේ ප්‍රවේශය — layers, coupled twins, **hard constraints** | design §1, §8 | ✅ |
| 5 | ★ දායකත්ව bullet 3 | ↓ | 🟨 |
| 6 | ලිපියේ ව්‍යුහය | — | ⬜ |

### ★ දායකත්ව bullet 3 — **නිවැරදි කරපු අනුවාදය**

> *The contributions of this paper are threefold:*
> - *(i) **A layered human-centric architecture** that couples a machine digital twin with a
>   human digital twin through **five explicitly defined bidirectional coupling points**;*
> - *(ii) **A quantified human digital twin** in which operator fatigue evolves as a
>   physiological state with **per-operator parameters derived from published anthropometric
>   equations**, and is enforced as a **hard constraint** rather than a soft penalty;*
> - *(iii) **Empirical evidence** from a 270-run co-simulation across three scenarios showing
>   that this reduces mean operator fatigue by **27%** and energy per unit by **31%**, and
>   eliminates all **79.5** constraint breaches per shift, at **no statistically detectable
>   throughput cost** under high demand (p = 0.148).*

> ⚠️ **outline එකේ පරණ අනුවාදයේ *"five-layer"* සහ *"ergonomic risk by [Y]%"* තිබුණා.**
> L5 ලියලා නෑ; ergonomic risk **13–15%** විතරයි (20% නොවේ). **ඉහත එක පාවිච්චි කරන්න.**

## C.2 · §II Related Work (T8.3) — වචන 800 · **draft ✅ 1,539 වචන**

උප-කොටස් 4 + Table I + gap ඡේදය. **`paper/section2-related-work.md` එකේ ලියලා ඉවරයි**
(`[N]` = 46 පුරවලා). ➜ **වචන 800 ට කපන්න ඕන.**

## C.3 · ★★ §III Proposed Framework (T8.2) — වචන 1,200 + Fig 1, 2

| § | අන්තර්ගතය | ප්‍රභවය | තත්ත්වය |
|---|---|---|---|
| III-0 | **Assumptions 5** *(පාඩම B.1-1)* | charter §5 | ⬜ |
| III-A | Architecture + **Fig. 1** | design §1 | ✅ fig |
| III-B | M-DT — state table + eq. §3.1–3.4 | design §3 | ✅ |
| III-C | ★ **H-DT** — state table + eq. §4.1–4.8 + **operator table** | design §4 | ✅ |
| III-D | ★ **CP1–CP5** + **Fig. 2** | design §5 | ✅ fig |
| III-E | Objective + weights | design §7.1, §7.3 | ✅ |
| III-F | ★ **HC1–HC4** + *"hard vs soft"* වාක්‍යය | design §8 | ✅ |
| ~~III-G~~ | ~~Explainability~~ | ⛔ **කැපුවා (D4)** | — |

> ⛔ **outline එකේ §III-G තියෙනවා — ඒක අයින් කරන්න.** ඒ වෙනුවට III-A එකේ
> **එක වාක්‍යයකින්** L5 නිර්වචනය කරලා **ලියලා නෑ** කියලා කියන්න.

## C.4 · §IV Implementation & Setup (T8.4) — වචන 500 + Table I

| § | අන්තර්ගතය | තත්ත්වය |
|---|---|---|
| IV-A | Co-simulation (SimPy) + parameters | ✅ config |
| IV-B | Datasets + preprocessing **(Table I)** ⚠️ D1 **synthetic** බව | ✅ data card |
| IV-C | ⚠️ **නැවත ලියන්න** — outline එකේ *"XGBoost, NSGA-II, SHAP"* — **තුනම කැපුවා** | ⬜ |
| IV-D | Baselines B1, B2, B3 — ★ **B2 සාධාරණව හදපු හැටි** | ✅ |
| IV-E | Scenarios S1–S3 + protocol (seeds 30, Bonferroni) | ✅ |

**IV-C එකට ලියන්න ඕන දේ** *(නිවැරදි අනුවාදය)*:
> Twin parameters are estimated directly from the benchmark datasets rather than learned:
> nominal machine life from tool-wear failures in D1, idle and per-task energy draw by load
> category in D3, and the baseline defect rate from D4. The decision layer is a weighted sum
> over the feasible set. No learned predictor is used **(§VI)**.

## C.5 · ★★ §V Results & Discussion (T8.5) — වචන 900 + Table II + Fig 3, 4

**`paper/section5-results.md` — 2,242 වචන, §A–§G, සංඛ්‍යා ඔක්කොම verify කරලා ✅**

| § | අන්තර්ගතය | සාක්ෂිය |
|---|---|---|
| V-A | Headline + **Table II** | `kpi_table.md` |
| V-B | ★ Trade-off + **Fig. 3** ⛔ *"Pareto front"* නොවේ | `sensitivity_hc1.csv` |
| V-C | Baseline comparison + **Fig. 4** | `raw_results.csv` |
| V-D | ★ Robustness — sensitivity **3ක්** (λμ · HC1 · weights) | 3 CSV |
| V-E | ★★ **"Constraints steer, not the objective"** | `decision_pressure.csv` |
| V-F | Ablation — CP5 විතරයි | `ablation.csv` |
| V-G | Workload + cross-training diagnosis | `crosstraining.csv` |
| V-H | **H1/H2 තීන්දු** *(§E.1 බලන්න)* | ⬜ **අලුතෙන් ලියන්න** |

> ⚠️ **§V 2,242 → 900 වචනවලට කපන්න ඕන.** ★★ තියෙන ඒවා තියාගෙන, V-G කපන්න/කෙටි කරන්න.

## C.6 · §VI Limitations (T8.6) — වචන 200 · **8ම ලියන්නම ඕන**

```
1. λ, μ           calibrated rather than measured
2. β₂, β₃         කිසිම dataset එකකින් fit කරන්න බැරි
3. Deferral rate  15% guard ඉක්මවනවා (S1 24%, S3 19%) + හේතුව
4. NSGA-II        ලියලා නෑ — weighted sum පමණයි
5. L5             explainability + override ලියලා නෑ
6. ML models      ලියලා නෑ; parameters දත්තවලින් සෘජුව
7. D1 (AI4I)      synthetic dataset
8. Operators 3    synthetic; physiological data එකතු කරලා නෑ
```

## C.7 · §VII Conclusion + Abstract

**Abstract වාක්‍ය 6 — නිවැරදි කරපු අනුවාදය:**
```
1. සන්දර්භය  : Industry 5.0 මිනිසා මධ්‍යයට ගෙන එයි…
2. ගැටලුව    : පවතින digital twins asset-centric; මිනිස් සාධක conceptual පමණි
3. අප කරන දේ : coupled machine + human twin, human limits as HARD CONSTRAINTS
4. ක්‍රමවේදය  : co-simulation · benchmark datasets 3 · 270 runs · scenarios 3
5. ප්‍රතිඵල  : fatigue −27% · energy/unit −31% · breaches 79.5 → 0 ·
               throughput −1.8% (සැලකිය යුතු නොවේ)          ⛔ NSGA-II කියන්න එපා
6. වැදගත්කම  : මිනිසා රැක ගැනීම මනින්න පුළුවන් efficiency වියදමකින් තොරව හැකි බව
```
**Keywords 5:** `Industry 5.0` · `Human Digital Twin` · `Sustainable Manufacturing` ·
`Multi-objective Scheduling` · `Human-Centric Design`  ⛔ *(`Explainable AI` **අයින් කරන්න**)*

---

# 📊 D · සාක්ෂි ගබඩාව

| ලිපිගොනුව | තියෙන්නේ | යන්නේ |
|---|---|---|
| `kpi_table.{csv,md}` | **KPI 11 × scenario 3** · Mann-Whitney U · Cliff's δ · Bonferroni α=0.0045 · **25/33 significant** | **Table II** |
| `raw_results.csv` | **270 runs × 39 columns** · reproducible | §V-A, Fig 4 |
| `sensitivity_hc1.csv` | HC1 0.70/0.80/0.90 × scenario 3 | **Fig. 3**, §V-D |
| `sensitivity_fatigue.csv` | λ,μ × 0.5/1/2 | §V-D 🚪 GATE 3 |
| `sensitivity.csv` | weight configs 4 + B2 | §V-D, §V-E |
| `decision_pressure.csv` | **95.7% තීරණවලට candidate 0–1** | ★★ §V-E |
| `ablation.csv` | CP1, CP2, CP5, all-off × scenario 3 | §V-F |
| `crosstraining.csv` | B2 / B3 / B3+retrained | §V-G |
| `feasibility.csv` + `deferral_diagnosis.csv` + `deferral_queue_depth.csv` | T5.16 | §VI-3 |
| `figures/fig1–fig4` (png+pdf+svg) | architecture · dataflow · trade-off · comparison | §III, §V |
| `paper/section2-related-work.md` | **1,539 වචන + Table I** | §II |
| `paper/section5-results.md` | **2,242 වචන §A–§G** | §V |
| `references.bib` | **entries 61** ⚠️ `[CHECK]` **5** | References |

**★ ප්‍රධාන සංඛ්‍යා (S2 high-demand · B3 vs B2):**
```
mean fatigue      0.741 → 0.541   −27.0%   p<0.001  δ=−1.00
energy per unit   1.321 → 0.915   −30.8%   p<0.001  δ=−1.00
CO₂e              39.88 → 27.18   −31.8%   p<0.001  δ=−1.00
mean RULA          4.72 → 4.03    −14.6%   p<0.001  δ=−1.00
breaches           79.5 → 0.0     −100%    p<0.001  δ=−1.00
throughput         91.9 → 90.2     −1.8%   p=0.148  ← සැලකිය යුතු නොවේ ★
OEE               0.667 → 0.684    +2.6%   p=0.112  ← සැලකිය යුතු නොවේ
```

---

# ⚖️ E · CLAIMS REGISTER

## E.1 · ★★ H1 සහ H2 — **තීන්දු** *(2026-08-06 දී පරීක්ෂා කළා)*

### H1 — **අර්ධ වශයෙන් පමණයි සනාථ වේ**

> *"throughput හි සුළු අඩුවීමක් (≤10%) සමඟින්, fatigue සහ ergonomic risk හි සැලකිය යුතු
> අඩුවීමක් (≥20%)"*

| scenario | fatigue | RULA | throughput | තීන්දුව |
|---|---|---|---|---|
| S1 | −26.2% ✅ | **−13.2% ❌** | −10.0% ✅ | **PARTIAL** |
| S2 | −27.0% ✅ | **−14.6% ❌** | −1.8% ✅ | **PARTIAL** |
| S3 | −31.9% ✅ | **−14.3% ❌** | **−12.7% ❌** | **PARTIAL** |

> ⛔ **"H1 confirmed" කියලා ලියන්න එපා.** Fatigue කොටස ✅, **ergonomic කොටස තුනේම ✗**,
> throughput කොටස S3 එකේ ✗.
>
> ✅ **ඇයි RULA 20% ට යන්නේ නෑ — ගණන් කරපු පැහැදිලි කිරීමක් තියෙනවා:**
> ```
> Task mix (L .35 / M .40 / H .25) × RULA_base (2/3/4)  →  floor = 2.90
> B2 = 4.72  ⇒  ලබාගත හැකි උපරිම අඩුවීම = 38%
> B3 = 4.03  ⇒  floor එකට උඩින් ඉතුරු 1.13, ඉන් 1.08 = ψ₁·F̂ (fatigue පදය)
> ```
> ➜ **H1 එක bounded index එකක floor එක නොසලකා 20% ඉල්ලලා තිබුණා.** Floor එකට උඩින්
> තියෙන කොටසින් **බොහෝමයක්ම framework එක ගෙනියනවා**. ➜ **§V-H සහ §VI එකේ මෙසේ ලියන්න.**

### H2 — **S1, S2 සනාථයි · S3 නෑ**

> *"Human-centric constraints මගින් machine downtime ද අඩු වේ"*

| scenario | B2 | B3 | Δ | p | තීන්දුව |
|---|---|---|---|---|---|
| S1 | 1.533 | 1.100 | **−28.3%** | <0.001 | ✅ **SUPPORTED** |
| S2 | 1.858 | 1.358 | **−26.9%** | <0.001 | ✅ **SUPPORTED** |
| S3 | 2.775 | 2.825 | +1.8% | 0.906 | ❌ **not supported** |

> ★★ **මේක ලස්සන ප්‍රතිඵලයක් — "මිනිසාට හොඳ දේ machine එකටත් හොඳයි"** සාමාන්‍ය සහ
> අධි-ඉල්ලුම් තත්ත්වවලදී **සනාථ වෙනවා**.
> ⚠️ **S3 එකේ නෑ** — ඒක **හේතුවත් සමඟ** ලියන්න: S3 හි downtime එකට **unplanned breakdowns
> (90 min repair)** ආධිපත්‍යය දරනවා, policy එකට ඒක වළක්වන්න බෑ.

## E.2 · ⛔ ලියන්න **බැරි** දේ 16

```
ප්‍රතිඵලවලින් (11) — paper/section5-results.md අග:
 1  "quality improved"                          p = 0.408
 2  "OEE improved"                              p = 0.112
 3  "HC1 = 0.80 following Price (1990)"         Price = AWL; 0.80 අපේ
 4  "λ = 0.020 as reported by Calzavara"        ආකෘතිය ඔවුන්ගේ, අගය අපේ
 5  workload ප්‍රතිඵලය අත්හැරීම                   ඒක සැලකිය යුතුයි, ලොකුයි, අපට විරුද්ධයි
 6  retrained matrix එකේ ප්‍රතිඵල වාර්තා කිරීම     setup එක උත්තරයට ගැලපීමක්
 7  "the weights let a practitioner tune…"      මනින්න බැරි තරම් වෙනසයි
 8  "all five coupling points contribute"       ablatable 3න් 1යි
 9  "the fatigue limit causes the deferrals"    ඉවත් කළත් ≤0.8 points
10  "a Pareto front"                            multi-objective search නෑ
11  "deferral rate meets the 15% guard"         S1, S3 එකේ නෑ

Deviations වලින් (5) — docs/11-design-deviations.md §3:
12  "our five-layer architecture" (ලියපු එකක් ලෙස)   L5 ලියලා නෑ
13  "SHAP explanations" / "operator override"       කැපුවා
14  "AI-driven / ML-based digital twin"             XGBoost නෑ
15  "coefficients fitted to SECOM"                  β2, β3 calibrated
16  ⚠️ "H1 confirmed"                                ergonomic කොටස තුනේම ✗
```

## E.3 · ✅ **ලියන්න පුළුවන්** ප්‍රබලම claims 6

```
1  fatigue −27%, energy/unit −31%, breaches 79.5 → 0   p<0.001, δ=−1.00  ★★★
2  "at no statistically detectable throughput cost"    p = 0.148         ★★★
3  "without degrading quality or OEE"                  no effect found   ★★
4  H2 — මිනිසාට හොඳ දේ machine එකටත් හොඳයි (S1, S2)     p<0.001          ★★
5  "the framework is steered by its constraints"       95.7% measured    ★★★
6  "Industry 4.0 is the limit of the objective,
    not of the framework"                              W-Profit          ★★
```

---

# ⛔ F · පරතර පරීක්ෂාව — ලියන්න පටන් ගන්න කලින්

## F.1 · අනිවාර්ය 3

| # | දේ | ඇයි | කාලය |
|---|---|---|---|
| **1** | ⛔ **T8.1 — IEEE template** | මේක නැතුව පිටු ගණන් කරන්න බෑ | 30 min |
| **2** | ⛔ **`[CHECK]` 5 තහවුරු කරන්න** | `ma2010muscle` · `aidt2026critical` · `dtcarbon2025` · `xai2026quality` · `iso8996` — **submit කරන්න කලින්** | 1 h |
| **3** | ⚠️ **charter §2, §3 නිවැරදි කරන්න** | XAI + override **in scope** ලෙස තියෙනවා (කැපුවා); CO₂ factor **0.53** (දැන් 0.33) | 15 min |

## F.2 · ලියනකොට ඕන වෙන අලුත් දේ 3

| # | දේ | කොහෙද |
|---|---|---|
| 1 | **§III-0 Assumptions 5** — charter §5 එකෙන් | §III මුල |
| 2 | **§V-H — H1/H2 තීන්දු ඡේදය** | §V අග |
| 3 | **§IV-C නැවත ලිවීම** — XGBoost/NSGA-II/SHAP අයින් | §IV |

## F.3 · optional (කලාහම හොඳයි, නැතත් කමක් නෑ)

```
⚪ Fig 5 — fatigue over time (S2, B2 vs B3)   ← ලස්සන, ඒත් පිටු 6 ට ඉඩ නෑ
⚪ T2.4 — papers 15ක් තවම pending             ← §II ලියනකොට ඕන ඒවා විතරක්
⚪ Othman et al. වර්ෂය                        ← 2018+ නම් N = 47
```

## F.4 · ✅ **සූදානම්** — කරන්න දෙයක් නෑ

```
✅ Fig 1, 2, 3, 4  (png + pdf + svg, කළු-සුදු පරීක්ෂාව pass)
✅ Table I  (related-work draft එකේ)      ✅ Table II  (kpi_table.md)
✅ §II draft 1,539 වචන                    ✅ §V draft 2,242 වචන
✅ Design සම්පූර්ණයි — §III එකට ඕන හැම සමීකරණයක්ම
✅ සංඛ්‍යා ඔක්කොම result files එකට verify කරලා
✅ Deviations 9 + Limitations 8 ලේඛනගතයි
✅ references.bib entries 61
```

---

> ## 🎯 එක වාක්‍යයකින්
>
> **§III (framework) සහ §V (results) දෙකටම ඕන හැම දෙයක්ම තියෙනවා.**
> ඉතුරු තියෙන්නේ **template එක, `[CHECK]` 5, සහ charter එකේ පරණ තැන් 2** විතරයි —
> **පැය 2ක වැඩක්**. ඊට පස්සේ **ලිවීම විතරයි**.
