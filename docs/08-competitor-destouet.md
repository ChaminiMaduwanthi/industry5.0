# 🎯 ළඟම තරඟකරුවා — Destouet et al. · සම්පූර්ණ විශ්ලේෂණය

> **T2.4 ★ ප්‍රතිදානය · 2026-08-04**
> **තත්ත්වය:** ✅ **Full text කියවා තහවුරු කර ඇත** (papers 3ම, accepted manuscripts)
> මේක [03-literature-review.md](03-literature-review.md) §3 Table I එකට සහ paper එකේ **§III** එකට කෙලින්ම යනවා.

---

## §0 · කියෙව්වේ මොනවද

| # | Paper | Venue | Full text ලැබුණේ |
|---|---|---|---|
| **P1** | *FJSP under Industry 5.0: A Survey on Human Reintegration, Environmental Consideration and Resilience Improvement* | *J. Manufacturing Systems* **67**:155–173 (2023) · 232 cites | HAL `hal-04084373` |
| **P2** ★ | *Multi-Objective Sustainable FJSSP: Balancing Economic, Ecological, and Social Criteria* | *Computers & Industrial Engineering* **195**:110419 (2024) · 33 cites | HAL `hal-04685337` |
| **P3** ⚠️ | *ML-Driven Solutions for Sustainable and Dynamic FJSSP under Worker Absences and Renewable Energy Variability* | *Computers & Operations Research* **186**:107323 (2026) | HAL `hal-05340152` |

> ⚠️⚠️ **P3 එක ඔබේ [references.bib](../paper/references.bib) එකේ **නෑ**.** ඒක **2026 දී** පළ වුණ ඔවුන්ගේ **අලුත්ම** එක,
> සහ ඒක ඔබේ novelty claim එකෙන් කොටසක් **කන්නවා**. §2 බලන්න. **මේක අනිවාර්යයෙන් cite කරන්න ඕන.**

---

## §1 · P2 (2024) — හරියටම මොකක්ද කරලා තියෙන්නේ

### Models 2ක් — **වෙන වෙනම**, එකට නෙවෙයි

```
MOP1 :  min { f1 = Cmax ,  f2 = ET + EM + EC ,  f3 = OCRA_max }
MOP2 :  min { f1 = Cmax ,  f2 = ET + EM + EC ,  f4 = −Sat_min }
```

| | අර්ථය |
|---|---|
| `f1` **Cmax** | Makespan — **💰 economic** |
| `f2` | මුළු බලශක්තිය = transport + operations + auxiliary — **🌱 ecological** |
| `f3` **OCRA_max** | Operator ලා අතරින් **උපරිම** OCRA ergonomic index — **👷 social** *(MOP1)* |
| `f4` **Sat_min** | Operator ලා අතරින් **අවම** තෘප්තිය (machine/variety/shift preferences) — **👷 social** *(MOP2)* |

> 💡 **වැදගත් සටහන:** Ergonomics සහ satisfaction යන දෙක **එකම model එකක නෑ**. ඔවුන් ඒවා **වෙන් කරලා**
> models දෙකකට දාලා. ඔබේ H-DT එකේ fatigue + skill + RULA + cognitive load **හතරම එකට** තියෙනවා.

### Social criterion එක ගණනය කරන්නේ කොහොමද — **OCRA**

```
OCRA  =  ATA / RTA                                    (Occhipinti 1998, ISO 11228-3)

RTA   =  CF × PM × FM × RM × ARF × (RcM × DuM)        CF = 30
```

| Multiplier | මොකෙන් එනවද |
|---|---|
| PM posture · FM force · RM repetitiveness · ARF additional risks | ★ **(operation, machine) යුගලයට ඇලවූ ස්ථිතික parameters** |
| RcM lack-of-recovery · DuM duration | Work environment |

> ★★ **මෙතන තමයි තීරණාත්මක කරුණ:** OCRA index එක ගණනය වෙන්නේ **task එකට අයිති ස්ථිතික සංඛ්‍යා** වලින්.
> Operator ගේ **තත්ත්වය කාලයත් සමඟ වෙනස් වෙන්නේ නෑ.** වෙහෙස **එකතු වෙන්නේ නෑ**, විවේකයෙන් **අඩු වෙන්නේත් නෑ**.
> ඒක **state** එකක් නෙවෙයි — ඒක **task attribute** එකක්.

### Rest (විවේකය) — **ස්ථිර නීතියක්**

$$R_{kjwt} = 0.08 \times \sum_m X_{kjwmt} \times p_{kjwm} \qquad \text{(Eq. 12)}$$

> Operator කෙනෙක් හැම operation එකකට පස්සේම **වැඩ කරපු කාලයෙන් 8%ක්** විවේක ගන්නවා. **හැමදාම. හැමෝටම.**
> ඔවුන්ගේම වචනවලින්: *"an operator rests 8 % of his working time after each operation"*
>
> ↔ **ඔබේ එකේ:** විවේකය `F_h ≥ 0.80` වුණාම **තත්ත්වය අනුව** ලැබෙනවා (HC1). ඒක **state-dependent**.

### උපකල්පන (ඔවුන්ගේම වචන)

> *"We assume that **every worker is capable of performing any task**. However, the time required to complete a task is contingent on the individual worker assigned to it. Indeed, **a more skilled worker will be faster**."*

> ★ **ඒ කියන්නේ:** ඔවුන් ළඟ **skill constraint එකක් නෑ**. Skill කියන්නේ processing time එකට ගුණ කරන
> coefficient එකක් විතරයි. ඔබේ **HC2 (`S_h,t ≥ 0.40`)** — *"දක්ෂතාව නැති කෙනෙකුට වැඩේ දෙන්න බෑ"* — ඔවුන් ළඟ **නෑ**.
> **සහ skill එකෙන් quality එකට බලපෑමක් නෑ** (ඔබේ CP1) — ඔවුන් ළඟ quality කියන දෙයක්ම නෑ.

### ⚠️ ඔවුන් ළඟ **hard constraint එකක් තියෙනවා** — මේක දැනගෙන ඉන්න

> *"In the MOP2 formulation, we **impose the OCRA index to be less than 2.2**, as recommended by ISO 11228-3, to ensure an acceptable level of risk exposure for workers."*

> ⛔ **ඒ නිසා *"අපි hard constraint පාවිච්චි කරනවා, ඔවුන් soft penalty"* කියලා **තනියම** ලියන්න එපා.** ඒක වැරදියි.
> ✅ **හරි විදිහට ලියන්න:** ඔවුන්ගේ hard constraint එක **ස්ථිතික task attribute** එකක් මත (OCRA ≤ 2.2, එකයි).
> ඔබේ HC1–HC4 **සජීවී twin state** මත — fatigue එකතු වෙනවා, machine health අඩු වෙනවා. **වර්ගය වෙනස්, ගණනත් වෙනස්.**

### Algorithm සහ පරීක්ෂණ

| | |
|---|---|
| Algorithm | **NSGA-II + NSGA-III**, Q-learning parameter tuning, RL-based variable neighbourhood search |
| Instances | Kacem et al. (2002) කුඩා · Caldeira et al. (2020) විශාල · **DFMC** engine plant: jobs 40, operations 570, machines 8, workers 8 |
| Runs | **10** (population 100, iterations 600) |
| Metrics | Hypervolume, IGD |

> 💡 **ඔබට වාසියක්:** ඔවුන් **runs 10යි**. ඔබ **30ක්** කරනවා + Mann-Whitney U + effect size.
> **තවත් වැදගත්:** ඔවුන් සංසන්දනය කරන්නේ **algorithms** (NSGA-II vs III vs SPEA2) — **paradigms නෙවෙයි**.
> ඔවුන් ළඟ **Industry 4.0 baseline එකක් නෑ**. ඔබේ **B2** එක ඒ නිසා තවමත් අලුත් දෙයක්.

### ★★ ඔවුන්ගේම සීමා ප්‍රකාශය (2024) — **verbatim**

> *"We acknowledge some limitations of this study. Firstly, **the models are static and are not designed to handle disruptions**. […] Secondly, regarding the workers, **this study is still in its early stages. Currently, the rest time for workers is set at 8% of their working time. Conducting a more detailed study on worker fatigue and optimizing break times could significantly enhance the model's effectiveness.**"*

---

## §2 · ⚠️ P3 (2026) — ඔබේ library එකේ නැති අලුත් තර්ජනය

ඔවුන් 2024 එකේ සීමා දෙකෙන් **එකක්** විසඳලා තියෙනවා.

### ✅ අලුතෙන් එකතු කරලා තියෙන දේ

```
f1 : Cmax          f2 : මුළු CARBON EMISSIONS (CET + CEA + CEM)          f3 : OCRA_max
```

| අලුත් දේ | විස්තරය |
|---|---|
| 🌱 **Carbon emissions** | kWh → **emission factor** මගින් CO₂ ට හරවනවා. **ඔබ කරන්න හිටපු දේම.** |
| ⚡ **Renewable energy** | Solar PV availability — forecast + variability |
| 🔄 **Dynamic + disruptions** | **Worker absences** + solar variability යටතේ rescheduling |
| 🤖 **ML** | Q-Learning / Deep Learning / **DQL** මගින් rescheduling strategy තෝරනවා |
| 👷 **Skills constraint** | *"human-related constraints such as workers' skills and ergonomic risks"* |

### ⛔ මේකෙන් ඔබට **අහිමි වෙන** claims 3

| ලියන්න හිටපු දේ | ඇයි දැන් බෑ |
|---|---|
| ❌ *"අපි තමයි CO₂e එකතු කරන පළමු අය"* | **P3 එකේ carbon emissions තියෙනවා** — ඒකම f2 objective එක |
| ❌ *"අපි තමයි disruption/resilience කරන පළමු අය"* | **P3 එකේ dynamic rescheduling තියෙනවා** |
| ❌ *"අපි තමයි ML/RL පාවිච්චි කරන පළමු අය"* | **P3 එකේ DQL තියෙනවා** |

### ✅ නමුත් — P3 එකේත් **තවම නෑ** (තහවුරු කර ඇත)

මම P3 හි සම්පූර්ණ පිටු 40ම scan කළා:

| සොයපු දේ | P3 හි ප්‍රතිඵලය |
|---|---|
| `digital twin` | **3 වතාවක් — තුනම reference list එකේ** *(Chen 2023, Li & Chen 2023, Zhang/Tao/Nee 2021)*. **තමන් හදලා නෑ.** |
| `sensor` | **0** |
| `scrap` / `defect rate` | **0** |
| machine health / RUL / degradation | **0** *(තිබුණ 2 = "environmental degradation" සහ solution "degradation")* |
| `fatigue` | 5 — ඒත් **තමන්ගේ model එකේ නෙවෙයි**: (1) OCRA parameter table එකේ multiplier නමක්, (2) අනිත් අයගේ වැඩ ගැන, (3) **absence වෙන්න හේතුවක්** ලෙස, (4) **තමන්ගේ සීමාවක් ලෙස** ⬇️ |
| Machine breakdown disruption | **නෑ** — ඔවුන්ගේ disruptions = **worker absence + solar variability** පමණයි |

### ★★★ P3 හි ඔවුන්ගේම සීමා ප්‍රකාශය — **ඔබේ paper එකේ බලවත්ම වාක්‍යය**

> *"**Human factors:** A more refined model could account for **worker fatigue levels to prevent fatigue peaks during operations**. Additionally, the dynamic factors considered in this study are limited to operator absences, **without addressing other disruptions such as fluctuating worker efficiency or health-related constraints**."*

> 🎯 **මේක තේරුම් ගන්න:** ඔබේ **ළඟම තරඟකරුවා**, **2026 දී**, තමන්ගේම අලුත්ම paper එකේ අන්තිම පිටුවේ,
> *"අපිට worker fatigue levels ඕන"* කියලා ලියලා තියෙනවා.
>
> **ඒක තමයි ඔබේ `HumanTwin.F_h` එක.** — λ accumulation, μ recovery, `F_h < 0.80` hard constraint.
>
> ඔබේ paper එකේ §I හෝ §III එකේ මේක උපුටා දක්වන්න. Reviewer කෙනෙකුට *"මේක ඇත්තටම අවශ්‍යද?"*
> කියලා අහන්න බැරි වෙනවා — **ක්ෂේත්‍රයේ ප්‍රමුඛම කණ්ඩායමම ඉල්ලලා තියෙනවා.**

---

## §3 · ✅ තහවුරු කළ සංසන්දනය (Table I එකට)

| | **Destouet 2024** | **Destouet 2026** | **★ මෙම අධ්‍යයනය** |
|---|---|---|---|
| 💰 Economic | Makespan | Makespan | **Throughput + OEE + downtime** |
| 🌱 Ecological | මුළු kWh | **Carbon emissions** | **kWh/unit + CO₂e + scrap %** |
| 👷 Social | OCRA *හෝ* satisfaction | OCRA + skills | **Fatigue + skill + RULA + cognitive — එකට** |
| **Machine Digital Twin** | ❌ | ❌ | ✅ health, energy, quality, availability |
| **Human Digital Twin** | ❌ | ❌ | ✅ **සංඛ්‍යාත්මක, පුද්ගලීකරණය කළ** |
| **Fatigue — dynamic state?** | ❌ ස්ථිතික OCRA · rest = 8% ස්ථිර | ❌ *(තමන්ම කියයි ඕන කියලා)* | ✅ **λ/μ exponential** `calzavara2019rest` |
| **Human ↔ Machine coupling** | ❌ | ❌ | ✅ **CP1–CP5 ද්විපාර්ශ්වික** |
| Quality / scrap | ❌ | ❌ | ✅ |
| Machine health / RUL | ❌ | ❌ | ✅ |
| Disruption / resilience | ❌ *(static)* | ✅ worker absence, solar | ✅ **machine breakdown (S3)** |
| **XAI** | ❌ | ❌ | ✅ SHAP |
| **Operator override** | ❌ | ❌ | ✅ human-in-command |
| **Industry 4.0 baseline?** | ❌ *(algorithms සංසන්දනය)* | ❌ | ✅ **B2** |
| Runs | 10 | — | **30** + Mann-Whitney U + effect size |

---

## §4 · ★ ඔබේ ඇත්ත Novelty — කරුණු 5 (මේවා විතරයි ලියන්න)

```
1. ★★ DIGITAL TWIN LAYER එක        ← ලොකුම එක. ඔවුන් ළඟ කිසිම DT එකක් නෑ (papers 3ම).
                                      ඔවුන්ගේ parameters ස්ථිතික. ඔබේ ඒවා සජීවී twin state.

2. ★★ FATIGUE = DYNAMIC STATE      ← λ/μ accumulation–recovery. ඔවුන් ළඟ static OCRA + 8% rest.
                                      ★ ඔවුන්ම 2026 දී මේක ඕන කියලා ලියලා තියෙනවා.

3. ★★ BIDIRECTIONAL COUPLING       ← CP1–CP5. skill→quality, fatigue→quality, health→cognitive load.
                                      ඔවුන් ළඟ skill→processing time විතරයි (එක් දිශාවක්, එක් බලපෑමක්).

4. ★  MACHINE-SIDE STATE           ← health/RUL + defect risk තීරණයට එනවා. ඔවුන් ළඟ machine = capacity විතරයි.

5. ★  HUMAN-IN-COMMAND             ← SHAP + operator override. ඔවුන් ළඟ මිනිසා optimize කරන object එකක්,
                                      තීරණය ගන්න agent එකක් නෙවෙයි.
```

> ⚠️ **1 සහ 2 උඩ paper එක ගොඩනඟන්න.** 3, 4, 5 සහායක.
> ⚠️ *"objectives තුනක්"*, *"CO₂"*, *"disruption"*, *"NSGA-II"*, *"ML"* — **මේ එකක්වත් novelty නෙවෙයි.** ඔවුන් ඔක්කොම කරලා.

---

## §5 · 📋 §III එකට ready-to-paste ඡේදය (English)

> Copy → `paper/` · T8.2 එකේදී පාවිච්චි කරන්න

```
The closest formulations to ours are those of Destouet et al. [P2, P3], who optimise
makespan, energy or carbon emissions, and an operator-centred criterion within a single
flexible job shop scheduling model. Our contribution is orthogonal to theirs and lies in
the state representation that feeds the optimiser rather than in the objective set itself.

In [P2, P3], the human criterion is the OCRA index, computed from posture, force,
repetitiveness and additional-risk multipliers that are attached to the (operation, machine)
pair. These multipliers are static task attributes: the operator's condition does not
accumulate over the shift and does not recover during rest, which is itself fixed at 8% of
working time after every operation. Likewise, the machine side is represented only by
processing times and per-operation energy coefficients; no machine health, degradation or
defect-risk state exists. Consequently, the two resources never influence one another beyond
the worker's skill coefficient scaling the processing time.

We replace both static representations with synchronised digital twins. The human twin
propagates fatigue through an exponential accumulation-recovery process with
operator-specific rates, so that fatigue is a state that evolves under the schedule rather
than a property of the task; rest is then triggered by that state through a hard constraint
instead of a fixed percentage. The machine twin contributes health, energy draw and defect
risk. The two twins are coupled bidirectionally at five points, allowing operator skill and
fatigue to modulate defect risk and machine condition to modulate cognitive load — couplings
that are structurally unavailable in a static parameterisation.

This distinction is not merely architectural. Destouet et al. themselves identify it as the
outstanding requirement, noting that "a more refined model could account for worker fatigue
levels to prevent fatigue peaks during operations" and that their dynamic factors remain
"limited to operator absences, without addressing [...] fluctuating worker efficiency or
health-related constraints" [P3]. The present work supplies exactly that missing layer, and
additionally evaluates it against an Industry 4.0 policy baseline, which [P2, P3] do not
consider — their comparisons are between solution algorithms rather than between
decision-making paradigms.
```

---

## §6 · 📗 references.bib එකට එකතු කරන්න

```bibtex
% [OK] ★★ 2026 --- ළඟම තරඟකරුවාගේ අලුත්ම එක. Dynamic + carbon, ඒත් DT නෑ, fatigue state නෑ.
@article{destouet2026dynamic,
  author  = {Destouet, Candice and Tlahig, Houda and Bettayeb, Belgacem and Mazari, B{\'e}lahc{\`e}ne},
  title   = {Machine Learning-Driven Solutions for Sustainable and Dynamic Flexible Job Shop
             Scheduling under Worker Absences and Renewable Energy Variability},
  journal = {Computers \& Operations Research},
  volume  = {186},
  pages   = {107323},
  year    = {2026},
  doi     = {10.1016/j.cor.2025.107323},
  note    = {★★ තමන්ගේම සීමාව ලෙස worker fatigue levels ඕන කියලා කියයි --- අපගේ H-DT එකට කෙලින්ම සාධාරණීකරණය.}
}
```

> ⚠️ **වර්ෂය:** HAL citation එකේ **2026, vol 186**. OpenAlex එකේ online year **2025**.
> Submit කරන්න කලින් publisher page එකෙන් අවසන් වර්ෂය තහවුරු කරගන්න.

---

## §7 · ✅ මේකෙන් ලැබුණු දේ (සාරාංශය)

| | |
|---|---|
| ✅ | Gap එක **තවම පවතිනවා** — digital twin layer එක ඔවුන් ළඟ **නෑ** (papers 3ම තහවුරු) |
| ✅ | ★★ **2026 dated competitor quote** එකක් ලැබුණා — fatigue state එක ඔවුන්ම ඉල්ලනවා |
| ✅ | ඔබට **Industry 4.0 baseline** එකේ වාසිය තියෙනවා — ඔවුන් ළඟ ඒක නෑ |
| ⚠️ | **CO₂, disruption, ML** — මේවා novelty ලෙස ලියන එක **නවත්වන්න** |
| ⚠️ | Paper **1ක්** bib එකට එකතු කරන්න (`destouet2026dynamic`) |
| ⚠️ | Table I එකට **පේළියක්** එකතු කරන්න (Destouet 2026) |

---

## 📎 මූලාශ්‍ර

- P1 · https://hal.science/hal-04084373 · DOI `10.1016/j.jmsy.2023.01.004`
- P2 · https://hal.science/hal-04685337 · DOI `10.1016/j.cie.2024.110419`
- P3 · https://hal.science/hal-05340152 · DOI `10.1016/j.cor.2025.107323`
