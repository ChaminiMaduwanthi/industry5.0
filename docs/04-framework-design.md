# 🏗️ Framework Design ★★ — **v2 · 🚪 FROZEN**

> **Phase 3 ප්‍රතිදානය.** Tasks T3.1 – T3.10
> ★ **GATE 3 පසුයි — 2026-08-04.** Design එක **freeze** කර ඇත (§14 බලන්න).
> මේකයි ඔබේ **ප්‍රධාන දායකත්වය (C1 + C2)**.
> ⛔ **Structure එක වෙනස් කරන්න එපා.** Parameter values `config.yaml` හරහා වෙනස් කළ හැක.

---

## §0 · මේ ලේඛනයේ මොකද අලුත් (v1 → v2)

| # | වෙනස | ඇයි |
|---|---|---|
| 1 | Fatigue model එක **kcal/min** ඒකකවලට ගෙනාවා, Calzavara හි **ප්‍රකාශිත ආකෘතියටම** | v1 හි `1 − (1−F)e^(−λIΔt)` සමීකරණය Calzavara ගේ එක **නොවේ**. දැන් ඒක **හරියටම** ඔවුන්ගේ එකයි |
| 2 | HC1 threshold එක **operator-specific** කළා (AWL මත) | v1 හි හැමෝටම `0.80` — ඒක **පුද්ගලීකරණය නෙවෙයි**. දැන් 0.80 කියන්නේ *"ඔබේ පෞද්ගලික සීමාවෙන් 80%"* |
| 3 | Coupling points CP1–CP5 **සමීකරණ බවට** පත් කළා | v1 හි ඒවා **වචන** පමණයි. Novelty එකක් **implement කරන්න බැරි නම්** ඒක novelty එකක් නෙවෙයි |
| 4 | Objectives **5 → 3** කළා (People/Planet/Profit) | NSGA-II **objectives 3කට වඩා** දුර්වලයි (§7.2). ★ මේක වැදගත් නිවැරදි කිරීමක් |
| 5 | HC1 එකට **hysteresis** එකතු කළා | නැත්නම් operator එක rest ↔ work අතර **චකිත වෙනවා** (chattering) |
| 6 | Normalization එකට **leakage-free calibration protocol** එකක් | Calibration seeds ≠ evaluation seeds |

---

## §1 · Architecture — Layer 5 (T3.1) ✅

📐 **[figures/fig1_architecture.svg](../figures/fig1_architecture.svg)** · PDF + PNG (300 dpi) ද ඇත

```
╔═══════════════════════════════════════════════════════════════╗
║ L5 · HUMAN INTERFACE       Dashboard · SHAP · OVERRIDE        ║
╠═══════════════════════════════════════════════════════════════╣
║ L4 · DECISION              HC filter → NSGA-II → w₁…w₅        ║
╠═══════════════════════════════════════════════════════════════╣
║ L3 · DIGITAL TWIN   ★  M-DT ◄──CP1–CP5──► H-DT                ║
╠═══════════════════════════════════════════════════════════════╣
║ L2 · DATA                  Ingest · Clean · Sync · Window     ║
╠═══════════════════════════════════════════════════════════════╣
║ L1 · PHYSICAL              5 machines · 3 operators · sensors ║
╚═══════════════════════════════════════════════════════════════╝
```

| Layer | ආදානය | ප්‍රතිදානය | වගකීම |
|---|---|---|---|
| L1 | — | Raw readings | භෞතික තත්ත්වය (SimPy) |
| L2 | Raw | Time-aligned state vectors | දත්ත සූදානම |
| L3 | State vectors | Twin states + **coupled** updates | ★ තත්ත්ව ඇගයීම |
| L4 | Twin states | Feasible, Pareto-optimal allocation | Optimization |
| L5 | Allocation + SHAP | මානුෂීය අනුමැතිය / override | **පාලනය මිනිසා ළඟ** |

---

## §2 · සංකේත සහ ඒකක (Notation)

| සංකේතය | අර්ථය | ඒකකය |
|---|---|---|
| $h \in \mathcal{H}$ | operator, $\lvert\mathcal{H}\rvert = 3$ | — |
| $m \in \mathcal{M}$ | machine, $\lvert\mathcal{M}\rvert = 5$ | — |
| $\tau \in \{L, M, H\}$ | task type — Light / Medium / Heavy | — |
| $\Delta t$ | decision epoch | 15 min |
| $t$ | simulation clock | min |
| $\pi$ | allocation policy: task → (operator, machine) | — |

> **Shift = 480 min → epochs 32ක්. Simulated shifts 20ක් → epochs 640ක් / run.**

---

## §3 · Machine Digital Twin (T3.2) ✅

### State variables

| සංකේතය | නම | පරාසය | ප්‍රභවය |
|---|---|---|---|
| $H_m$ | Health index | [0,1] | RUL model · D1, D2 |
| $E_m$ | Energy rate | kWh/h | Energy model · D3 |
| $Q_m$ | Defect risk | [0,1] | Quality model · D4 **+ CP1, CP2** |
| $A_m$ | Availability | {0,1} | Rule |
| $U_m$ | Utilisation | [0,1] | Counter |

### 3.1 Health — degradation

$$H_m(t+\Delta t) = \max\Big(0,\; H_m(t) - \Delta t \cdot \frac{\kappa_\tau}{L_m^0}\Big)$$

| සංකේතය | අර්ථය | අගය |
|---|---|---|
| $L_m^0$ | nominal life (busy minutes) | D1/D2 RUL model එකෙන් calibrate |
| $\kappa_\tau$ | task severity | L = 0.7 · M = 1.0 · H = 1.4 |

> Idle නම් $\kappa = 0$ (degradation නෑ). Maintenance කළාම $H_m \leftarrow 1$.
> **XGBoost RUL model එකේ කාර්යය:** sensor window එකෙන් $L_m^0$ ඇස්තමේන්තු කිරීම (T5.5).

### 3.2 Energy

$$E_m(t) = e^{\text{idle}}_m + \mathbb{1}[\text{busy}] \cdot \Delta e_m(\tau)$$

D3 (Steel Industry Energy) එකෙන් regression මගින් $e^{\text{idle}}_m$, $\Delta e_m(\tau)$ ලබාගන්න.

$$\text{Energy per unit} = \frac{\sum_m \int E_m \, dt}{\text{units produced}} \qquad
\text{CO}_2\text{e} = \text{total kWh} \times \text{EF}$$

#### ✅ T3.10 විසඳා ඇත — CO₂ emission factor

> ⚠️ **v1 හි තිබූ `0.53` කල් ඉකුත් වී ඇත.** ශ්‍රී ලංකා grid එක සැලකිය යුතු ලෙස decarbonise වී තිබේ.

| වර්ෂය | gCO₂/kWh | | වර්ෂය | gCO₂/kWh |
|---|---|---|---|---|
| 2016 | 522 | | 2022 | 410 |
| 2017 | 533 | | 2023 | 417 |
| 2019 | 518 | | 2024 | 378 |
| 2021 | 418 | | **2025** | **329** |

$$\boxed{\;\text{EF} = 0.33\ \text{kg CO}_2/\text{kWh} \quad (\text{Ember, 2025})\;}$$

> 📚 **Citation:** Ember, *Yearly Electricity Data* — Our World in Data හරහා → `ember2025electricity`
> 💡 පරාසය 2013–2025: **0.30 – 0.53** kgCO₂/kWh (ජල විදුලිය මත රඳා පවතී — වර්ෂයෙන් වර්ෂයට වෙනස් වේ).

> ★★ **වැදගත් methodological කරුණක් (paper එකේ ලියන්න):**
> CO₂e = kWh × EF නිසා, **EF එක ස්ථිර ගුණාකාරයක්** පමණි.
> ඒ නිසා **B1 / B2 / B3 අතර සංසන්දනය EF තේරීමෙන් ස්වායත්තයි (invariant)** — EF එක වෙනස් කළත් **ranking එක වෙනස් වෙන්නේ නෑ**.
> ➜ ඒ නිසා මේක ප්‍රතිඵලවලට **අවදානමක් නොවේ**. kWh **සහ** CO₂e දෙකම වාර්තා කරන්න.

### 3.3 Quality — ★ මෙතන twin දෙක හමු වෙනවා

$$Q_{m,h,\tau}(t) = \sigma\Big(\beta_0 + \beta_1\big(1 - H_m(t)\big) + \underbrace{\beta_2\big(1 - S_{h,\tau}\big)}_{\textbf{CP1}} + \underbrace{\beta_3 \hat{F}_h(t)}_{\textbf{CP2}} + \beta_4 \kappa_\tau\Big)$$

$\sigma(\cdot)$ = logistic. $\beta_0 \ldots \beta_4$ — D4 (SECOM) / D1 මත fit කර, $\beta_2, \beta_3 > 0$ ලෙස සීමා කරන්න.

> ★★ **මේ එක සමීකරණය තමයි ඔබේ paper එකේ හදවත.** Destouet ලාගේ model එකේ quality කියන දෙයක්ම නෑ; skill එක processing **time** එකට විතරයි බලපාන්නේ. මෙතන skill **සහ** fatigue දෙකම **defect risk** එකට බලපානවා.

### 3.4 Availability

$$A_m(t) = \mathbb{1}\big[H_m(t) > H_{\min}\big] \cdot \mathbb{1}\big[\text{not under maintenance}\big], \qquad H_{\min} = 0.30$$

---

## §4 · Human Digital Twin (T3.3) ★★ — **ඔබේ novelty එක**

### State variables

| සංකේතය | නම | පරාසය | ඒකකය |
|---|---|---|---|
| $F_h$ | **Fatigue** (energy expenditure rate) | $[E'_{r,h},\, \infty)$ | **kcal/min** |
| $\hat F_h$ | Normalized fatigue | [0,1] | — |
| $S_{h,\tau}$ | Skill | [0,1] | — |
| $R_h$ | Ergonomic risk (RULA) | [1,7] | — |
| $C_h$ | Cognitive load | [0,1] | — |
| $W_h$ | Workload share | [0,1] | — |

---

### 4.1 ★★ Fatigue — Calzavara et al. (2019) ආකෘතිය

> 📚 **ප්‍රාථමික citation:** Calzavara, Persona, Sgarbossa & Visentin (2019), *IJPR* **57**(3):948–962, DOI `10.1080/00207543.2018.1497816` → `calzavara2019rest`
>
> ✅ **සමීකරණ තහවුරු කර ඇත (2026-08-04)** — Sgarbossa & Vijayakumar, *IFAC World Congress 2020*, pp. 10758–10761 හි Eq. (3), (4), (9) මගින්, එම model එකම උපුටමින්.

**ප්‍රකාශිත ආකෘතිය:**

$$F(t_o) = E'_w + \big(E'_r - E'_w\big)\, e^{-\lambda t_o} \qquad\qquad R(t_r) = F(t_o)\, e^{-\mu t_r}$$

**අපගේ epoch-wise ඒකාබද්ධ ස්වරූපය** *(ප්‍රභවයේ Eq. 9 හි λ/μ මාරු වීමේ තර්කයම)*:

$$\boxed{\;F_h(t+\Delta t) \;=\; E^{*} \;+\; \big(F_h(t) - E^{*}\big)\, e^{-\rho \Delta t}\;}$$

$$E^{*} = \begin{cases} E'_w(\tau) & \text{වැඩ කරනවා නම්} \\[2pt] E'_{r,h} & \text{විවේක / idle} \end{cases}
\qquad
\rho = \begin{cases} \lambda_h & E^{*} \ge F_h(t) \quad \text{(වෙහෙස වැඩිවීම)} \\[2pt] \mu_h & E^{*} < F_h(t) \quad \text{(යථා තත්ත්වයට)} \end{cases}$$

> 💡 **ඇයි මේක v1 එකට වඩා හොඳ:** v1 හි fatigue හැම task එකකදීම **1 දක්වා** නැඟුණා.
> දැන් ඒක නැඟෙන්නේ **ඒ task එකේ ඇත්ත ශක්ති ඉල්ලුම දක්වා** පමණයි — සැහැල්ලු වැඩක් කවදාවත් operator ව
> සම්පූර්ණයෙන් වෙහෙසන්නේ නෑ. **භෞතික විද්‍යාවට ගැලපෙනවා, සහ ප්‍රභවයටත් ගැලපෙනවා.**

---

### 4.2 ★ පුද්ගලීකරණය — operator ට අනන්‍ය නියතයන්

**විවේකයේ ශක්ති පරිභෝජනය** — Mifflin–St Jeor *(Mifflin et al., 1990)*:

$$E'_{r,h} = \frac{S + 10W + 6.25H_{\text{cm}} - 5\,\text{age}}{1440} \quad \text{[kcal/min]}, \qquad S = \begin{cases} +5 & \text{පිරිමි} \\ -161 & \text{ගැහැනු}\end{cases}$$

**Acceptable Work Level** — පැය 8ක් තිරසාරව දරාගත හැකි උපරිමය *(Price, 1990; Silva et al., 2016)*:

$$\text{AWL}_h = \begin{cases} (60 - 0.55\,\text{age}) \times 0.005 \times W / 3 & \text{පිරිමි} \\[3pt] (48 - 0.37\,\text{age}) \times 0.005 \times W / 3 & \text{ගැහැනු}\end{cases} \quad \text{[kcal/min]}$$

**යෝජිත operator profiles 3** *(simulation එකේ synthetic operators — anthropometrics design choice එකක්, data එකක් නෙවෙයි)*:

| Operator | ස්ත්‍රී/පු. | වයස | බර (kg) | උස (cm) | $E'_{r,h}$ | $\text{AWL}_h$ |
|---|---|---|---|---|---|---|
| OP1 | පිරිමි | 28 | 72 | 175 | **1.166** | **5.352** |
| OP2 | ගැහැනු | 35 | 62 | 163 | **0.905** | **3.622** |
| OP3 | පිරිමි | 47 | 80 | 170 | **1.134** | **4.553** |

> ★★ **මේකයි Sharotry et al. (2022) ඉල්ලපු *"true personalized DT"* එක.** OP2 සහ OP3 ට OP1 ට වඩා
> **අඩු තිරසාර සීමාවක්** තියෙනවා — ඒ නිසා framework එක ස්වයංක්‍රීයව ඔවුන්ට බර වැඩ අඩුවෙන් දෙනවා.
> **මේක hard-code කරලා නෑ — physiology එකෙන් එනවා.**

### 4.3 Task ශක්ති ඉල්ලුම — ISO 8996 metabolic classes

$$E'_w(\tau) = \text{(W/m²)}_\tau \times A_{Du} \times 0.01434 \quad \text{[kcal/min]}, \qquad A_{Du} \approx 1.8\ \text{m²}$$

| Task | ISO 8996 class | W/m² | $E'_w$ (kcal/min) | $\kappa_\tau$ | RULA$_{\text{base}}$ | $c_\tau$ |
|---|---|---|---|---|---|---|
| **L** Light | Class 1 — low | 100 | **2.58** | 0.7 | 2 | 0.20 |
| **M** Medium | Class 2 — moderate | 165 | **4.26** | 1.0 | 3 | 0.40 |
| **H** Heavy | Class 3 — high | 230 | **5.94** | 1.4 | 4 | 0.60 |

> 💡 **සටහන:** OP2 ගේ AWL = 3.62 < Medium task එකේ 4.26. ඒ කියන්නේ OP2 ට medium වැඩ **දිගටම** කරන්න බෑ —
> විවේක අවශ්‍යයි. **ඒක bug එකක් නෙවෙයි, ඒක තමයි framework එකේ අරමුණ.** (§4.10 බලන්න.)

### 4.4 Normalized fatigue — ★ physiologically meaningful

$$\boxed{\;\hat F_h(t) = \text{clip}\!\left(\frac{F_h(t) - E'_{r,h}}{\text{AWL}_h - E'_{r,h}},\; 0,\; 1\right)\;}$$

| $\hat F_h$ | අර්ථය |
|---|---|
| 0 | පෞද්ගලික විවේක මට්ටමේ |
| 0.80 | ★ **පෞද්ගලික තිරසාර සීමාවෙන් 80%** ← **HC1** |
| 1.0 | හරියටම AWL එකේ — දිගු කාලීනව දරාගත නොහැක |

> ★★ **මේකයි v1 එකට වඩා ලොකුම දියුණුව.** `0.80` කියන අංකයට දැන් **භෞතික අර්ථයක්** තියෙනවා,
> සහ ඒක **හැම operator කෙනෙකුටම වෙනස්** — arbitrary නෑ. Reviewer කෙනෙක් *"0.80 කොහෙන්ද?"* කියලා
> ඇහුවොත් උත්තරය: *"පිළිගත් acceptable work level එකෙන් 80%, එය Price (1990) අනුව ගණනය කර ඇත."*

### 4.5 λ, μ — ✅ **විසඳා ඇත (T3.9): calibrated parameters ලෙස**

| | |
|---|---|
| අර්ථය | $\lambda_h$ = වෙහෙස වීමේ අනුපාතය · $\mu_h$ = යථා තත්ත්වයට පත්වීමේ අනුපාතය |
| ඒකකය | min⁻¹, දෙකම **operator-specific** |
| වර්ගය | ★ **Calibrated parameter** — measured constant එකක් නොවේ |

#### ඇයි calibrated, measured නොවේ?

Calzavara et al. (2019) හි $\lambda$, $\mu$ අගයන් **operator ගේ පෞද්ගලික ලක්ෂණ අනුව heart-rate calibration එකකින්** ලබාගනී — ඒවා විශ්වීය නියතයන් නොවේ. අපගේ operator ලා **synthetic** බැවින්, ඕනෑම ප්‍රකාශිත අගයක් උපුටා ගැනීමත් සමානවම අත්තනෝමතික වේ. ඒ නිසා ඒවා **පැහැදිලිව calibrated parameters ලෙස ප්‍රකාශ කර**, sensitivity analysis මගින් ආවරණය කිරීම **වඩාත් අවංක සහ වඩාත් ශක්තිමත්ය**.

#### ✅ Default අගයන් (freeze කර ඇත)

$$\lambda = 0.020\ \text{min}^{-1}\ (t_{1/2} = 35\ \text{min}), \qquad \mu = 0.046\ \text{min}^{-1}\ (t_{1/2} = 15\ \text{min})$$

**තෝරාගැනීමේ නිර්ණායක 2:**
1. Shift එකක් (480 min) තුළ $\hat F$ එක **අර්ථවත් පරාසයක්** ආවරණය කළ යුතුය — §4.10 හි තහවුරු වේ (0.66 – 0.76)
2. $\mu > \lambda$ — යථා තත්ත්වයට පත්වීම වෙහෙසීමට වඩා **වේගවත්** විය යුතුය *(ergonomics සාහිත්‍යයේ පොදු නිරීක්ෂණයකි)*

#### 📚 සාහිත්‍යගත සීමා (literature-grounded bounds)

Exponential work–recovery models හි ප්‍රකාශිත recovery rate constants:

| ප්‍රභවය | අගය | ආකෘතිය | සටහන |
|---|---|---|---|
| Yi et al. (2022) *IJERPH* 19(2):930 | **0.132** min⁻¹ | $MS = MS_0 + (MVC - MS_0)(1 - e^{-0.132t})$ | Manual demolition, **n = 17**, empirically fitted |
| Ma et al. (2010) | 2.4 (normalised) | muscle-level | ⚠️ වෙනස් normalization |
| **අපගේ default** | **0.046** min⁻¹ | whole-body metabolic | localized muscle එකට වඩා මන්දගාමී — **නිවැරදියි** |

> 💡 **ඇයි 0.132 ට වඩා අඩු?** Yi et al. මනින්නේ **එක් මාංශ පේශියක** යථා තත්ත්වයට පත්වීම — ඒක වේගවත්.
> අපි මනින්නේ **මුළු ශරීරයේ පරිවෘත්තීය** තත්ත්වය — ඒක මන්දගාමී. ඒ නිසා අපගේ අගය **භෞතික විද්‍යාවට ගැලපෙනවා**.

#### ⚠️ අනිවාර්ය කොන්දේසි 2 (මේවා නොකළොත් gate එක වලංගු නෑ)

```
1. T7.6 sensitivity analysis එකට  λ, μ  එකතු කරන්න   →  0.5× · 1× · 2×
      ලකුණු කරන්න:  scaling එකෙන් B2 vs B3 හි RANKING එක වෙනස් වෙනවද?
      වෙනස් නොවේ නම්  →  නිගමන robust  ✅

2. §6 Limitations එකේ මෙසේ ලියන්න:
      "Fatigue accumulation and recovery rates were calibrated rather than
       measured; operator-specific values would require physiological data
       collection, which this simulation study does not include."
```

> ⚠️ **කිසිසේත්ම ලියන්න එපා:** *"λ = 0.020 as reported by Calzavara et al."* — **ඒක අසත්‍යයකි.**
> ✅ **ලියන්න:** *"the accumulation and recovery rates were calibrated such that fatigue traverses a meaningful fraction of the operator's acceptable work band over one shift, following the exponential form of Calzavara et al. [x]"*

#### 🔬 විකල්ප වැඩිදියුණු කිරීමක් (optional · Phase 4)

**D5 · WESAD:** subject එකකගේ physiological arousal series එක ගෙන, work bout වලට exponential rise එකක් සහ rest bout වලට exponential decay එකක් fit කර subject-wise $\lambda, \mu$ ලබාගන්න → operator 3 දෙනාට map කරන්න.
කළොත් *"calibrated against the WESAD corpus"* කියලා ලියන්න පුළුවන් — **ඊට වඩා ශක්තිමත්**. නමුත් **අනිවාර්ය නෑ**.

---

### 4.6 Skill matrix

| | Task L | Task M | Task H |
|---|---|---|---|
| **OP1** | 0.90 | 0.60 | 0.30 |
| **OP2** | 0.50 | 0.90 | 0.70 |
| **OP3** | 0.70 | 0.40 | 0.90 |

> Shift තුළ ස්ථිර (learning effect නොසලකයි — charter §5 assumption 2).
> Processing time: $p_{h,\tau} = p^0_\tau \big/ (0.5 + 0.5\,S_{h,\tau})$ — දක්ෂ අය වේගවත්.

### 4.7 Ergonomic risk — RULA + CP5

$$R_h(t) = \text{clip}\Big(\underbrace{\text{RULA}_{\text{base}}(\tau)}_{\text{McAtamney \& Corlett 1993}} + \underbrace{\psi_1 \hat F_h(t)}_{\text{වෙහෙස → නරක posture}} + \underbrace{\psi_2 \hat v_m}_{\textbf{CP5}},\; 1,\; 7\Big)$$

$\psi_1 = 2.0$, $\psi_2 = 1.0$, $\hat v_m$ = normalized machine speed. වාර්තා කිරීමේදී පූර්ණ සංඛ්‍යාවකට round කරන්න.

### 4.8 Cognitive load — NASA-TLX proxy + CP3

$$C_h(t) = \text{clip}\Big(c_\tau + \underbrace{\gamma_1\big(1 - H_m(t)\big)}_{\textbf{CP3}} + \gamma_2 Q_m(t) + \gamma_3\frac{n_h - 1}{|\mathcal{M}| - 1},\; 0,\; 1\Big)$$

$\gamma_1 = 0.30$, $\gamma_2 = 0.20$, $\gamma_3 = 0.15$; $n_h$ = එකවර බලාගන්නා machine ගණන. *(Hart & Staveland, 1988)*

### 4.9 Workload share

$$W_h = \frac{\text{busy minutes of } h}{\sum_{h'} \text{busy minutes of } h'}, \qquad
\text{Gini} = \frac{\sum_h \sum_{h'} |W_h - W_{h'}|}{2 |\mathcal{H}|^2 \bar{W}}$$

### 4.10 ★★ Design validation — code ලියන්න **කලින්** කරපු සංඛ්‍යාත්මක පරීක්ෂාව

> ✅ **2026-08-04 දී ක්‍රියාත්මක කර පරීක්ෂා කරන ලදී.** §4.1–§4.4 සමීකරණ, provisional λ/μ සමඟ,
> shift එකක් (epochs 32) පුරා **medium task එකක් දිගටම** දුන්නොත් මොකද වෙන්නේ:

| Operator | AWL | අවසන් $\hat F$ | **Rest episodes** | Busy time |
|---|---|---|---|---|
| **OP1** (පිරිමි, 28) | 5.35 | 0.74 | **0** | 480/480 min — **100%** |
| **OP3** (පිරිමි, 47) | 4.55 | 0.76 | **4** | 420/480 min — **88%** |
| **OP2** (ගැහැනු, 35) | 3.62 | 0.66 | **8** | 360/480 min — **75%** |

**Task තිරසාරභාවය** ($E'_w$ vs AWL):

| | Light | Medium | Heavy |
|---|---|---|---|
| OP1 | ✅ | ✅ | ⚠️ over AWL |
| OP3 | ✅ | ✅ | ⚠️ over AWL |
| OP2 | ✅ | ⚠️ over AWL | ⚠️ over AWL |

> ★★ **මේ ප්‍රතිඵලය ඉතාම වැදගත් — paper එකේ §III හෝ §V එකේ දාන්න.**
>
> Framework එක **තනිවම**, hard-code කිරීමකින් තොරව, operator තුන් දෙනාට **වෙනස් ආරක්ෂාවක්** දෙනවා:
> OP1 ට විවේක අවශ්‍ය නෑ; OP3 ට 4ක්; OP2 ට 8ක්. **ඒ වෙනස එන්නේ physiology එකෙන් මිසක් නීතියකින් නෙවෙයි.**
>
> ➜ මේකයි Sharotry et al. (2022) ඉල්ලපු *"true personalized DT"* එක **ක්‍රියාවෙන්**.
> ➜ Destouet ලාගේ ස්ථිර 8% rest rule එකට මේක **කරන්න බැහැ** — හැමෝටම එකයි.

**T3.11 (feasibility) පිළිබඳ ප්‍රතිඵලය:** worst case එකේදීත් OP2 **75%** ක් නිදහස්ව වැඩ කරනවා.
Operator 3 දෙනා එකවර විවේකයට යන අවස්ථා දුර්ලභ ➜ **feasible set එක හිස් වීමේ අවදානම අඩුයි.**
එහෙත් Phase 5 මුලදී `constraint_deferrals` අනුපාතය තහවුරු කරන්න (§12).

---

---

## §5 · Coupling Points (T3.7) ★★ — **implement කළ හැකි ස්වරූපයෙන්**

📐 **[figures/fig2_dataflow.svg](../figures/fig2_dataflow.svg)**

| # | සම්බන්ධතාවය | දිශාව | **සමීකරණයේ පදය** |
|---|---|---|---|
| **CP1** | Skill → Quality | H→M | $\beta_2(1 - S_{h,\tau})$ in $Q_m$ |
| **CP2** | Fatigue → Quality | H→M | $\beta_3 \hat F_h$ in $Q_m$ |
| **CP3** | Health → Cognitive load | M→H | $\gamma_1(1 - H_m)$ in $C_h$ |
| **CP4** | Task intensity → Fatigue | M→H | $E'_w(\tau)$ as asymptote in $F_h$ |
| **CP5** | Machine speed → Ergonomics | M→H | $\psi_2 \hat v_m$ in $R_h$ |

> ★★ **Ablation study එකක් කරන්න (T7.6 එකට එකතු කරන්න):** CP1–CP5 **ක්‍රියා විරහිත** කර B3 run කරන්න.
> එවිට framework එක **ස්වාධීන twin දෙකක්** බවට පත් වෙනවා — හරියටම Destouet ලාගේ static ආකෘතිය වගේ.
> **ප්‍රතිඵලයේ වෙනස = coupling එකේ ඇත්ත වටිනාකම.** මේක reviewer කෙනෙකුට දිය හැකි **ප්‍රබලම සාක්ෂිය**.

---

## §6 · Normalization (T3.4) ✅

$$\hat{x} = \text{clip}\left(\frac{x - x_{\min}}{x_{\max} - x_{\min}},\, 0,\, 1\right)$$

| Metric | $x_{\min}$ | $x_{\max}$ | ප්‍රභවය |
|---|---|---|---|
| Fatigue $\hat F$ | — | — | §4.4 හි දැනටමත් normalized |
| Ergonomic $\hat R$ | 1 | 7 | RULA පරාසය (ස්ථිර) |
| Energy $\hat E$ | P5 | P95 | ★ B1 calibration runs |
| Waste $\hat W$ | 0 | P95 | ★ B1 calibration runs |
| Throughput $\hat T$ | P5 | P95 | ★ B1 calibration runs |

**★ Calibration protocol (leakage-free):**

```
1. B1 (random) run කරන්න  seeds 100–129  ← calibration block
2. එම runs වලින්  P5, P95  ගන්න  (outlier-robust; min/max නෙවෙයි)
3. ඒ අගයන්  config.yaml  එකේ FREEZE කරන්න
4. ඇගයීම් runs සියල්ල  seeds 0–29  ← evaluation block, වෙනස් seeds
```

> ⚠️ **ඇයි P5/P95, min/max නෙවෙයි?** එක outlier run එකකින් scale එක විනාශ වෙන එක වළක්වන්න.
> ⚠️ **ඇයි වෙනස් seeds?** Evaluation data එකෙන් normalize කළොත් ඒක **leakage** එකක් — reviewer කෙනෙක් අල්ලනවා.

---

## §7 · Objective Function (T3.5) ★★

### 7.1 Scalarized form (B3a — weighted sum)

$$\min_{\pi} \; Z(\pi) = \underbrace{w_1 \hat F(\pi) + w_2 \hat R(\pi)}_{\text{👷 People}} + \underbrace{w_3 \hat E(\pi) + w_4 \hat W(\pi)}_{\text{🌱 Planet}} - \underbrace{w_5 \hat T(\pi)}_{\text{💰 Profit}}$$

$\sum w_i = 1$, $w_i \ge 0$. සියලු පද shift එක පුරා **සාමාන්‍යගත** කර ඇත.

### 7.2 ⚠️ Multi-objective form (B3b — NSGA-II) — **වැදගත් නිවැරදි කිරීමක්**

> ❌ **v1 හි ගැටලුව:** objectives **5ක්** NSGA-II එකට දුන්නොත් ඒක **හොඳට වැඩ කරන්නේ නෑ**.
> Objectives 4කට වඩා ගියාම හැම solution එකක්ම අනෙකට non-dominated වෙනවා → selection pressure නැති වෙනවා.
> *(මේ නිසා තමයි Destouet ලා **NSGA-III** පාවිච්චි කළේ.)*

✅ **විසඳුම — objectives 3ක් ලෙස කාණ්ඩගත කරන්න.** ඒක ඔබේ People/Planet/Profit කතාවටත් **හරියටම ගැලපෙනවා**:

$$\min_{\pi} \Big[\; \underbrace{f_1 = \tfrac{w_1\hat F + w_2\hat R}{w_1 + w_2}}_{\text{👷 People}},\quad \underbrace{f_2 = \tfrac{w_3\hat E + w_4\hat W}{w_3 + w_4}}_{\text{🌱 Planet}},\quad \underbrace{f_3 = -\hat T}_{\text{💰 Profit}} \;\Big]$$

> ✅ **වාසි 3:** ① NSGA-II නිවැරදිව වැඩ කරනවා ② Pareto front එක **3-D** — plot කරන්න පුළුවන් (Fig 3) ③ axis 3 = pillar 3.

### 7.3 Weight scenarios

| Config | $w_1$ | $w_2$ | $w_3$ | $w_4$ | $w_5$ | අර්ථය |
|---|---|---|---|---|---|---|
| **W-Balanced** | 0.20 | 0.15 | 0.20 | 0.15 | 0.30 | default |
| **W-Human** | 0.35 | 0.25 | 0.10 | 0.10 | 0.20 | මිනිසාට ප්‍රමුඛතාවය |
| **W-Green** | 0.15 | 0.10 | 0.30 | 0.25 | 0.20 | පරිසරයට ප්‍රමුඛතාවය |
| **W-Profit** | 0.05 | 0.05 | 0.05 | 0.05 | 0.80 | ≈ Industry 4.0 |

> 💡 **T7.6 හි ඔප්පු කරන්න ඕන දේ:** `W-Profit ≈ B2`.
> එවිට ලියන්න පුළුවන්: *"Industry 4.0 is a **special case** of our framework in which the human and environmental weights approach zero."*

---

## §8 · Constraints (T3.6) ★ — **Industry 5.0 හි හරය**

### 🔴 Hard constraints

| # | Constraint | තේරුම | ★ Destouet ලා ළඟ තියෙනවද |
|---|---|---|---|
| **HC1** | $\hat F_h < 0.80$ | පෞද්ගලික තිරසාර සීමාවෙන් 80% | ❌ **නෑ** (fatigue state එකක්ම නෑ) |
| **HC2** | $S_{h,\tau} \ge 0.40$ | දක්ෂතාවය නැති කෙනෙකුට වැඩේ නෑ | ❌ **නෑ** (*"every worker is capable of performing any task"*) |
| **HC3** | $R_h \le 5$ | RULA action level | ⚠️ සමාන එකක් ඇත (OCRA ≤ 2.2) — ඒත් **ස්ථිතික** |
| **HC4** | $H_m > 0.30$ | කැඩෙන්න ළං machine එකට වැඩ නෑ | ❌ **නෑ** (machine health state එකක්ම නෑ) |

> ⚠️ **පරිස්සමින් ලියන්න:** *"අපි hard constraints පාවිච්චි කරනවා, ඔවුන් නෑ"* කියන්න **එපා** — ඒක වැරදියි.
> ✅ **ලියන්න:** ඔවුන්ගේ එක **ස්ථිතික task attribute** එකක් මත; අපගේ HC1 සහ HC4 **කාලයත් සමඟ පරිණාමය වන twin state** මත.
> **වර්ගය වෙනස්, ප්‍රභවය වෙනස්.** විස්තර: [08-competitor-destouet.md](08-competitor-destouet.md)

### ★ HC1 hysteresis — chattering වළක්වා ගැනීම

```
if  F̂_h ≥ 0.80  →  operator h  ට  MANDATORY REST  ලෑස්ති කරන්න
    rest එක  දිගටම  F̂_h ≤ 0.60  වෙනකම්                    ← hysteresis band
    (single threshold එකක් නම් 0.799 ↔ 0.801 අතර හැම epoch එකකම මාරු වෙනවා)
```

### Violation handling — **හැම එකක්ම log කරන්න**

| තත්ත්වය | ක්‍රියාව | Log column |
|---|---|---|
| HC1 කැඩෙනවා | Mandatory rest (hysteresis සමඟ) | `hc1_rest_events` |
| HC2/HC3 නිසා (h,m) යුගලයක් බෑ | ඒ යුගලය feasible set එකෙන් ඉවත් | `hc_filtered_pairs` |
| HC4 කැඩෙනවා | Machine → maintenance, $T_{\text{maint}}$ කාලයක් | `hc4_maint_events` |
| **feasible යුගලයක් නෑ** | Task queue එකේ රැඳෙනවා | ★ `constraint_deferrals` |

> ★ **`constraint_deferrals` එක ඉතාම වැදගත්.** ඒක තමයි *"මිනිසා රැක ගන්න throughput කීයක් අත්හැරියාද"* කියන
> ප්‍රශ්නයට **සෘජු සංඛ්‍යාත්මක උත්තරය**. §5 Results එකේ මේක වාර්තා කරන්න.

### 🟡 Soft constraints — objective එකට penalty

| # | Constraint | Penalty |
|---|---|---|
| **SC1** | Workload සාධාරණව බෙදීම | $+\,\text{Gini}(W)$ |
| **SC2** | Task–skill ගැලපීම | $+\,(1 - S_{h,\tau})$ |
| **SC3** | Machine switching අඩු කිරීම | $+\,\text{setup penalty}$ |

---

## §9 · Decision Loop (L4) — pseudocode

```python
# epoch එකකට වරක් — 15 min
def decide(epoch, twins, pending_tasks):
    # 1 · twin states යාවත්කාලීන (coupling ඇතුළුව)
    for m in machines: m.update(dt)          # H, E, A
    for h in operators: h.update(dt)         # F (λ/μ), C, R, W
    apply_coupling(CP3, CP4, CP5)            # M-DT → H-DT
    apply_coupling(CP1, CP2)                 # H-DT → M-DT  → Q_m

    # 2 · feasible set
    feasible = [(t, h, m) for t in pending_tasks
                          for h in operators
                          for m in machines
                if F_hat[h] < 0.80           # HC1
                and skill[h][t.type] >= 0.40 # HC2
                and rula(h, t, m) <= 5       # HC3
                and health[m] > 0.30         # HC4
                and available[m] and idle[h]]

    if not feasible:
        log("constraint_deferral", epoch, len(pending_tasks))
        return None                          # ★ වහන්න එපා — මේකට වටිනාකමක් තියෙනවා

    # 3 · optimise  (feasible set එක උඩ පමණයි)
    front = nsga2(feasible, objectives=[people, planet, profit])
    choice = select_by_weights(front, w)     # හෝ knee point

    # 4 · explain + override
    reason = shap_explain(choice, feasible)
    choice = operator_interface(choice, reason)   # L5 — override හැකියි

    return choice
```

> 💡 **පිළිවෙල වැදගත්:** constraint filter එක **optimizer එකට කලින්**. එවිට hard constraint එකක්
> **කිසිසේත්ම** කැඩෙන්නේ නෑ — penalty එකකින් "මිලදී ගන්න" බැහැ. **ඒකයි 4.0 සහ 5.0 අතර ඇත්ත වෙනස.**

---

## §10 · Explainability (L5)

```
තීරණය: Task #47 (Medium) → OP2, Machine M3

ඇයි?
  ✓ OP2 ගේ skill මේ task එකට 0.90 (ඉහළම)
  ✓ OP2 ගේ F̂ = 0.31  (සීමාව 0.80 — පෞද්ගලික AWL 3.62 kcal/min)
  ✓ M3 හි health 0.87, energy 2.1 kWh (අඩුම)
  ✓ අපේක්ෂිත defect risk 0.04  (CP1+CP2 සැලකිල්ලට ගෙන)

ඇයි OP1 නොවේ?
  ✗ OP1 ගේ F̂ = 0.82 → HC1 කඩනවා → mandatory rest (0.60 වෙනකම්)

විකල්පය: OP3 (skill 0.40) — HC2 සීමාවට ළඟයි, defect risk 3.2× වැඩියි
```

SHAP values මගින් ස්වයංක්‍රීයව ජනනය කරන්න (T5.13).

---

## §11 · ★ B2 (Industry 4.0 baseline) — සාධාරණ ලෙස ව්‍යුත්පන්න කිරීම

> ⚠️ B2 එක **වෙනම code එකක්** ලෙස ලියන්න එපා. **එකම framework එක**, පහත සීමා සමඟ.
> එවිට සංසන්දනය **සාධාරණයි** කියලා ඔප්පු කරන්න පුළුවන්.

| | B2 (Industry 4.0) | B3 (Proposed 5.0) |
|---|---|---|
| M-DT | ✅ **සම්පූර්ණ බලය** (H, E, Q, A) | ✅ සම්පූර්ණ |
| H-DT | ⚠️ **පවතී, නමුත් optimizer ට නොපෙනේ** | ✅ පෙනේ |
| Coupling | CP4 පමණයි *(fatigue තවම track වෙනවා — මනින්න ඕන නිසා)* | CP1–CP5 සියල්ල |
| Objectives | $-\hat T$ පමණයි | People + Planet + Profit |
| Constraints | **HC4 පමණයි** | HC1–HC4 |
| Weights | W-Profit | W-Balanced |

> ★ **තීරණාත්මක කරුණ:** B2 යටතේත් H-DT එක **ක්‍රියාත්මකයි** — නැත්නම් B2 හි fatigue **මනින්න බෑ**.
> එය තීරණයට **බලපාන්නේ නෑ** පමණයි. මේ වෙනස methodology එකේ පැහැදිලිව ලියන්න.

---

## §12 · ✅ විවෘත කරුණු — **සියල්ල විසඳා ඇත (2026-08-04)**

| # | කරුණ | විසඳුම | තත්ත්වය |
|---|---|---|---|
| **T3.9** | $\lambda_h, \mu_h$ | **Calibrated parameters** ලෙස ප්‍රකාශ කර, literature bounds + අනිවාර්ය sensitivity analysis සමඟ (§4.5) | ✅ |
| **T3.10** | CO₂ emission factor | **0.33 kgCO₂/kWh** — Ember (2025). `0.53` කල් ඉකුත් වී ඇති බව හම්බුණා (§3.2) | ✅ |
| **T3.11** | Feasibility smoke test | §4.10 හි සංඛ්‍යාත්මකව පරීක්ෂා කර ඇත — worst case OP2 **75% busy** ➜ අවදානම අඩුයි | ✅ **අර්ධ** |

### ⏭️ Phase 5 එකට රැගෙන යන කොන්දේසි 3

> මේවා **design එකේ අඩුපාඩු නොවේ** — implementation එකේදී **තහවුරු කළ යුතු** දේවල්.

```
1. constraint_deferrals අනුපාතය මනින්න  (epochs 640)
     >15% නම් → HC1 එක 0.85 දක්වා ලිහිල් කරන්න හෝ operator profiles සකසන්න
     ★ තීරණය config.yaml එකේ ලේඛනගත කරන්න

2. T7.6 sensitivity analysis එකට λ, μ එකතු කරන්න  (0.5× · 1× · 2×)
     ★ B2 vs B3 ranking එක වෙනස් නොවේ නම් → නිගමන robust

3. §6 Limitations එකේ "calibrated rather than measured" කියලා ලියන්න
```

---

## §13 · Traceability — RQ සහ contribution → design

| | ආවරණය කරන design කොටස |
|---|---|
| **RQ1** M-DT සහ H-DT integrate කරන්නේ කෙසේද | §1 (layers), §5 (CP1–CP5), §9 (loop) |
| **RQ2** People/Planet/Profit trade-off සමතුලනය | §7 (objectives), §8 (constraints) |
| **RQ3** 4.0 ට වඩා හොඳද | §11 (B2 derivation) → Phase 6 |
| **C1** Layer 5 architecture | §1 + Fig 1 |
| **C2** Quantified H-DT, hard constraints ලෙස | §4 + §8 |
| **C3** ප්‍රමාණාත්මක සාක්ෂි | §6 calibration + Phase 6–7 |
| **H1** fatigue ↓20%, throughput ↓≤10% | §8 HC1 + `constraint_deferrals` |
| **H2** මිනිසාට හොඳ = machine එකටත් හොඳ | §3.3 CP1+CP2 → $Q_m$ → scrap ↓ |

---

## §14 · Design Freeze (T3.8) 🚪

- [x] Architecture diagram — `figures/fig1_architecture.svg` (+ PDF, PNG 300 dpi)
- [x] Data flow / coupling diagram — `figures/fig2_dataflow.svg` (+ PDF, PNG)
- [x] M-DT variables සහ update rules — §3
- [x] H-DT variables සහ update rules — §4
- [x] Fatigue model **ප්‍රභවයට ගැලපෙන ලෙස** — §4.1
- [x] Personalisation (E'_r, AWL) සමීකරණ සහිතව — §4.2
- [x] Coupling points **සමීකරණ ලෙස** — §5
- [x] Normalization + leakage-free calibration — §6
- [x] Objective function (3-objective ලෙස නිවැරදි කර) — §7
- [x] Constraints + hysteresis + violation handling — §8
- [x] Decision loop pseudocode — §9
- [x] B2 සාධාරණ ව්‍යුත්පත්තිය — §11
- [x] **T3.9** — λ, μ: calibrated parameters ලෙස නිර්වචනය + bounds + sensitivity mandate (§4.5)
- [x] **T3.10** — CO₂ emission factor: **0.33 kgCO₂/kWh**, Ember (2025) (§3.2)
- [x] **Design validation** — සමීකරණ සංඛ්‍යාත්මකව පරීක්ෂා කර ඇත (§4.10)

---

# 🚪🚪 **GATE 3 — පසුයි · 2026-08-04** ✅

| | |
|---|---|
| **තත්ත්වය** | ★ **DESIGN FROZEN** |
| **Freeze දිනය** | **2026-08-04** |
| **අනුමැතිය** | Topic එක **supervisor විසින්ම පවරන ලද** බැවින්, වෙනම sign-off එකක් **blocker එකක් ලෙස නොසැලකේ**. Supervisor ව හමුවන ඊළඟ අවස්ථාවේදී §14 checklist එක ඉදිරිපත් කරන්න. |
| **ඊළඟ අදියර** | 🔵 **Phase 4 — දත්ත සකසාගැනීම (T4.1 – T4.7)** |

### ⛔ Freeze කළාට පස්සේ වෙනස් කරන්න **බැරි** දේ

```
✗ Twin state variables (H,E,Q,A,U / F,S,R,C,W)      ✗ Coupling points CP1–CP5
✗ Objective function ව්‍යුහය (People/Planet/Profit)  ✗ Hard constraints HC1–HC4
✗ Fatigue model ආකෘතිය (exponential λ/μ)            ✗ Normalization ක්‍රමය
```

### ✅ Freeze කළාට පස්සේත් වෙනස් කරන්න **පුළුවන්** දේ (`config.yaml` හරහා)

```
✓ λ, μ අගයන්        ✓ EF (0.33)         ✓ Weights w₁…w₅
✓ HC threshold අගය  ✓ β, γ, ψ සංගුණක    ✓ Skill matrix අගයන්
```

> ⚠️ **වෙනස කරුණාකර තේරුම් ගන්න:** **STRUCTURE එක** freeze — **PARAMETER VALUES** නෙවෙයි.
> Parameter එකක් වෙනස් කලොත් experiments නැවත run කරන්න ඕන, ඒත් **code එක නැවත ලියන්න ඕන නෑ**.
> Structure එකක් වෙනස් කලොත් **දෙකම** නැවත කරන්න ඕන. **ඒකයි freeze එකේ අර්ථය.**

---

## 📎 මේ ලේඛනයේ නව citations

| Key | භාවිතය | තත්ත්වය |
|---|---|---|
| `calzavara2019rest` | Fatigue λ/μ ආකෘතිය | ✅ bib එකේ ඇත |
| `mcatamney1993rula` | RULA | ✅ bib එකේ ඇත |
| **`mifflin1990ree`** | $E'_{r,h}$ resting energy expenditure | ⬜ **bib එකට එකතු කරන්න** |
| **`price1990relaxation`** | AWL (පිරිමි) | ⬜ **bib එකට එකතු කරන්න** |
| **`silva2016age`** | AWL (වයස් සාධකය) | ⬜ **bib එකට එකතු කරන්න** |
| **`iso8996`** | Task metabolic classes | ⬜ **bib එකට එකතු කරන්න** |
| **`hart1988tlx`** | NASA-TLX (cognitive load proxy) | ⬜ **bib එකට එකතු කරන්න** |
| **`sgarbossa2020ifac`** | Calzavara සමීකරණ තහවුරු කිරීම | ⬜ optional |
