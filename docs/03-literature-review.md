# 📚 Literature Review

> **Phase 2 ප්‍රතිදානය.** Tasks T2.1 – T2.7
> ඉලක්කය: **Gap එක ඔප්පු කිරීම** — ඔබේ paper එකේ පැවැත්මට හේතුව.

---

## §1 · සෙවුම් උපාය (T2.2)

### පාවිච්චි කරන databases

| Database | Link | සටහන |
|---|---|---|
| Google Scholar | scholar.google.com | පුළුල් — මුලින්ම මේක |
| IEEE Xplore | ieeexplore.ieee.org | Engineering conferences |
| ScienceDirect | sciencedirect.com | Elsevier journals |
| MDPI | mdpi.com | *Sensors*, *Sustainability*, *Applied Sciences* — open access |
| arXiv | arxiv.org | නවතම preprints |
| SpringerLink | link.springer.com | *J. Intelligent Manufacturing* |

### Search Strings 6 (එකින් එක run කරන්න)

| # | Search string | ඉලක්කය |
|---|---|---|
| **S1** | `"Industry 5.0" AND "human-centric" AND (framework OR architecture)` | මූලික Industry 5.0 frameworks |
| **S2** | `"human digital twin" AND (manufacturing OR production)` | ★ ඔබේ core novelty |
| **S3** | `"digital twin" AND "sustainable manufacturing" AND (energy OR carbon)` | Sustainability + DT |
| **S4** | `("Operator 4.0" OR "Operator 5.0") AND (fatigue OR cognitive OR ergonomic)` | මිනිස් සාධක |
| **S5** | `"multi-objective" AND "production scheduling" AND "human factors"` | Optimization ක්‍රම |
| **S6** | `"explainable AI" AND manufacturing AND (trust OR operator)` | XAI + human trust |

### පෙරහන් (Filters)

- **වර්ෂය:** 2019 – 2026 (60%+ 2021ට පස්සේ වෙන්න ඕන)
- **භාෂාව:** English
- **වර්ගය:** Journal articles + peer-reviewed conference papers
- **බැහැර:** Blog posts, white papers, non-peer-reviewed

### සෙවුම් සටහන

| Search | දිනය | තෝරාගත් ගණන | තත්ත්වය |
|---|---|---|---|
| S1 Industry 5.0 human-centric framework | 2026-08-03 | 6 | ✅ |
| S2 Human digital twin manufacturing | 2026-08-03 | 8 | ✅ |
| S3 DT + sustainable manufacturing + energy | 2026-08-03 | 6 | ✅ |
| S4 Operator 4.0/5.0 fatigue cognitive | 2026-08-03 | 4 | ✅ |
| S5 Multi-objective scheduling + human factors | 2026-08-03 | 6 | ✅ |
| S6 XAI manufacturing + operator trust | 2026-08-03 | 4 | ✅ |
| S7 HDT + energy joint optimisation *(අමතර)* | 2026-08-03 | 3 | ✅ |
| | **එකතුව (round 1)** | **33** | |

### Round 2 — Citation chasing (T2.10) · 2026-08-03

**ක්‍රමය:** Gaffinet et al. (2025) හි references **113** Semantic Scholar API එකෙන් ලබාගෙන,
manufacturing / ergonomics / scheduling / sustainability / DT-architecture ට අදාළ ඒවා පෙරාගන්නා ලදී.

| ප්‍රභවය | ලැබුණු ගණන |
|---|---|
| Gaffinet et al. (2025) reference list | **14** අලුත් |
| අනුබද්ධ OpenAlex searches | **4** අලුත් *(Xu et al., Adel, Malik & Bilberg, Rasheed et al.)* |

### Round 3 — Metadata verification (T2.9) · 2026-08-03

**ක්‍රමය:** OpenAlex සහ Semantic Scholar APIs මගින් සෑම entry එකකම authoritative metadata ලබාගැනීම.

| | |
|---|---|
| **මුළු එකතුව** | **52 papers** |
| **කියවා තහවුරු කළ ඒවා** `[READ]` | **8** *(කණ්ඩායම A)* |
| **Metadata තහවුරු කළ ඒවා** `[OK]` | **31** |
| **තවම `[CHECK]`** | **4** |

**🔧 හම්බුණු වැරදි 3** *(අනුමානය → තහවුරු කිරීම)*

| වැරදි ලෙස තිබූ | නිවැරදි |
|---|---|
| Tan, Wei / Zhang, Xiaotao | **Tan, Weihua / Zhang, Xizheng** |
| Agarwal, Sameer *(NSGA-II)* | **Agarwal, Sakshi** |
| Gaffinet — vol 166 පමණයි | **166:104230** · DOI `10.1016/j.compind.2024.104230` |

**🎁 Round 3 එකෙන් හම්බුණු bonus papers 5**

| Ref | Cites | ඇයි වැදගත් |
|---|---|---|
| ★★ **Destouet et al. (2023)** *JMS* 67:155–173 | **232** | **අපගේ ගැටලු අවකාශයේම survey එක** — FJSP under Industry 5.0: human + environment + resilience |
| Fuller et al. (2020) *IEEE Access* 8 | 2,612 | DT enabling technologies |
| Jones et al. (2020) *CIRP JMST* 29 | 2,226 | DT characterisation SLR |
| Barredo Arrieta et al. (2020) *Information Fusion* 58 | **9,337** | **XAI පදනම** |
| Zhong et al. (2017) *Engineering* 3(5) | 2,823 | Industry 4.0 review |

> ✅ **Round 2–3 එකෙන් ලැබුණු ලොකුම දේ:** Sharotry, Greco, Löcklin — **තුනම ඔබේ gap එකට කෙලින්ම අදාළ**
> සහ තුනම ඔබේ තර්කයට **සහාය දෙන උද්ධෘත** සපයයි (§4 බලන්න).

---

## §2 · Screening ක්‍රියාවලිය (T2.3, T2.4)

```
        සියලු ප්‍රතිඵල  (~200)
                │
                ▼  Duplicates ඉවත් කිරීම
             (~150)
                │
                ▼  Screening 1: Title + Abstract
              (~80)
                │
                ▼  Screening 2: Full text කියවීම
           ★ (30–40)  ← මේවා comparison table එකට
```

### ඇතුළත් කිරීමේ නිර්ණායක (Inclusion)

- Industry 4.0/5.0, smart manufacturing, හෝ digital twin ගැන
- Framework, architecture, හෝ implementation එකක් ඉදිරිපත් කරයි
- මිනිස් සාධක, sustainability, හෝ AI decision-making ස්පර්ශ කරයි

### බැහැර කිරීමේ නිර්ණායක (Exclusion)

- Manufacturing නොවන domain (healthcare, smart city — hard exclusion)
- Digital twin යන වචනය පාවිච්චි කරනවා විතරයි, implementation එකක් නෑ
- Full text නොලැබෙන ඒවා

---

## §3 · Comparison Table (T2.5) ★★

> මේකයි ඔබේ **gap** එක පෙන්වන සාක්ෂිය. Paper එකේ Table I ලෙස යනවා.

### 🔍 කණ්ඩායම A — ළඟම competitors **9** (**කියවා තහවුරු කර ඇත**)

> මේ **9** තමයි ඔබේ paper එකට **වඩාත්ම ළං** ඒවා. සියල්ලම full-text හෝ abstract-level කියවා තහවුරු කර ඇත.

| # | Ref | Yr | Venue | Cites | Machine DT? | **Human DT (quantified)?** | **තීරණ ගැනීමට යොදයිද?** | Sustainability? | Multi-obj? | **තහවුරු කළ අඩුපාඩුව** |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | Modoni & Sacco | 2023 | *Sensors* 23(13):6054 | 59 | ✅ | ❌ *(biographic + attitudes පමණයි)* | ⚠️ AR උපදෙස් පමණයි | ❌ | ❌ | **කර්තෘන්ම කියයි:** fatigue modelling සහ ergonomic assessment **"remain unaddressed"** |
| **2** | Tóth et al. | 2023 | *MethodsX* 11:102260 | 112 | ❌ | ❌ | ❌ | ❌ | ❌ | **සම්පූර්ණයෙන් conceptual.** Validation නෑ. XAI future work ලෙස පමණි |
| **3** | Tan et al. | 2021 | *Comp. & Ind. Eng.* 160:107557 | 108 | ❌ | ✅ **fatigue** | ✅ **NSGA-II scheduling** | ❌ | ✅ *(fatigue + makespan)* | ★ **Digital twin නෑ** — machine health/energy/quality state තීරණයට යොදාගත නොහැක |
| **4** | Sharotry et al. | 2022 | *IEEE Access* 10:12774–12791 | 40 | ❌ | ✅ **joint angles + DTW + EWMA** | ❌ **detection පමණයි** | ❌ | ❌ | ★ Fatigue හොඳට quantify කරයි — **නමුත් තීරණයකට යොදන්නේ නෑ.** Lab, subjects **2යි** |
| **5** | Greco et al. | 2020 | *Applied Sciences* 10(21):7758 | 107 | ❌ | ✅ **ergonomics** | ⚠️ decision *support* පමණයි | ❌ | ❌ | Automated optimisation නෑ. Machine DT coupling නෑ. Lab case study |
| **6** | Löcklin et al. | 2021 | *Procedia CIRP* 104:458–463 | 78 | ⚠️ සඳහන් | ❌ | ❌ | ❌ | ❌ | ★★ **Bi-directional human↔machine flow එකේ අවශ්‍යතාවය හඳුනාගනී** — නමුත් architecture proposal එකක් පමණයි |
| **7** | Crnjac Žižić et al. | 2025 | *Sensors* 25(18):5662 | 4 | ⚠️ අර්ධ | ❌ *(task duration පමණයි)* | ⚠️ line balancing | ⚠️ **වචනයෙන් පමණයි** | ❌ | Unidirectional observation. Energy/carbon දත්ත නෑ |
| **8** | ⚠️ **Destouet et al.** | 2024 | *Comp. & Ind. Eng.* 195:110419 | 33 | ❌ | ⚠️ **OCRA — ස්ථිතික** | ✅ **FJSP scheduling** | ✅ **energy** | ✅ | ★★ **ළඟම තරඟකරුවා.** ✅ **FULL TEXT කියවා ඇත.** OCRA = (operation, machine) යුගලයට ඇලවූ **static multipliers**; **fatigue එකතු වෙන්නේ නෑ**; rest = **ස්ථිර 8%**; **digital twin නෑ**; quality/machine-health නෑ; runs **10** |
| **9** | ⚠️⚠️ **Destouet et al.** | **2026** | *Comp. & Oper. Res.* 186:107323 | — | ❌ | ⚠️ OCRA + skills | ✅ **DQL rescheduling** | ✅ **carbon emissions** | ✅ | ★★★ **අලුත්ම එක — ඔවුන් dynamic + carbon එකතු කරලා.** ඒත් **digital twin තවම නෑ** (reference list එකේ පමණයි); **fatigue state නෑ**; disruption = worker absence + solar (**machine breakdown නෑ**). ★ **තමන්ම කියයි: "worker fatigue levels" ඕන** |
| **★** | **මෙම අධ්‍යයනය** | 2026 | — | — | ✅ | ✅ **fatigue (λ/μ dynamic) + skill + RULA** | ✅ **hard constraints ලෙස** | ✅ **kWh + CO₂e + scrap** | ✅ **NSGA-II** | — |

> ⚠️⚠️ **වැදගත්ම අනතුරු ඇඟවීම** — ✅ **2026-08-04 දී full text 3ම කියවා තහවුරු කර ඇත.**
> 👉 **සම්පූර්ණ විශ්ලේෂණය: [08-competitor-destouet.md](08-competitor-destouet.md)**
>
> **Destouet et al.** ළඟ දැන් **objectives තුනම + carbon + dynamic disruption + ML** තියෙනවා.
> ⛔ ඒ නිසා මේ **එකක්වත්** novelty ලෙස ලියන්න **එපා**: *"objectives තුනක්"*, *"CO₂"*, *"disruption/resilience"*, *"NSGA-II"*, *"machine learning"*.
>
> ✅ **ඔබේ ඇත්ත novelty කරුණු 2:**
> 1. ★★ **Digital twin layer එක** — ඔවුන්ගේ papers **3ම** පරීක්ෂා කළා: DT එකක් **හදලා නෑ** (2026 එකේ `digital twin` වචනය තියෙන්නේ **reference list එකේ පමණයි**).
> 2. ★★ **Fatigue = සජීවී state එකක්** — ඔවුන්ගේ OCRA එක **task එකට ඇලවූ ස්ථිතික multipliers** වලින්; වෙහෙස **එකතු වෙන්නේ නෑ**, විවේකයෙන් **අඩු වෙන්නේත් නෑ** (rest = ස්ථිර 8%).
>
> 💡 මේ දෙක §III එකේ **පැහැදිලිව** ලියන්න. Ready-to-paste ඡේදය [08-competitor-destouet.md §5](08-competitor-destouet.md) එකේ තියෙනවා.

---

### 🎯 මේ table එකෙන් පේන රටාව (**ඔබේ paper එකේ හරය**)

```
   Digital Twin තියෙනවා          Fatigue quantify කරනවා
   (Modoni, Löcklin, Crnjac)     (Tan, Sharotry, Greco)
            │                              │
            │  ❌ fatigue නෑ                │  ❌ digital twin නෑ
            │  ❌ sustainability නෑ         │  ❌ sustainability නෑ
            │                              │
            └──────────┐        ┌──────────┘
                       ▼        ▼
                  ⚠️ හිස් තැන — කවුරුත් නෑ
                       │
                       ▼
                  ★ ඔබේ paper එක
```

> **පැහැදිලි ලෙස:** ක්ෂේත්‍රය **කණ්ඩායම් දෙකකට බෙදිලා**.
> එක් පිරිසක් **digital twin** හදනවා — නමුත් human model එක static profile data.
> අනෙක් පිරිස **fatigue quantify** කරනවා — නමුත් digital twin එකක් නෑ.
> **දෙකම එකට කරලා, ඒ උඩින් sustainability එකතු කරපු එකක් හම්බුණේ නෑ.**

---

### 💬 ඔබට වාසි ගෙන දෙන උද්ධෘත 4 (**paper එකේ කෙලින්ම යොදන්න**)

| # | Ref | උද්ධෘතය | මොකටද යොදන්නේ |
|---|---|---|---|
| **1** | Sharotry et al. (2022) | *"...showcases the need for a **true personalized DT** for an operator for fatigue assessment"* | ★ ඔබේ **operator-specific λ, μ** තීරණයට සාධාරණීකරණය |
| **2** | Löcklin et al. (2021) | *"Such applications require a **bi-directional flow** of information and need data, models and simulations of **machines as well as humans**"* | ★★ ඔබේ **CP1–CP5 coupling points** වලට කෙලින්ම සාධාරණීකරණය |
| **3** | Modoni & Sacco (2023) | Fatigue modelling සහ ergonomic assessment **"remain unaddressed"** *(ඔවුන්ගේම future work)* | ★ Gap එක **තරඟකරුවාම පිළිගැනීම** |
| **4** ★★★ | **Destouet et al. (2026)** | *"A more refined model could account for **worker fatigue levels to prevent fatigue peaks during operations**. Additionally, the dynamic factors considered in this study are limited to operator absences, without addressing other disruptions such as **fluctuating worker efficiency or health-related constraints**."* | ★★★ **ළඟම තරඟකරුවා, 2026 දී, තමන්ගේම අලුත්ම paper එකේ, ඔබේ contribution එකම ඉල්ලනවා.** මේක §I හෝ §III එකේ දාන්න |

> 💡 **මේ 4 ඉතාම බලවත්.** Reviewers ට *"මම හිතන්නේ gap එකක් තියෙනවා"* කියනවා වෙනුවට,
> *"**මේ ක්ෂේත්‍රයේම කර්තෘන් හතර දෙනෙක්ම මේක අවශ්‍යයි කියලා ලියලා තියෙනවා**"* කියන්න පුළුවන්.
> ★ විශේෂයෙන් **#4** — ඒක **ළඟම තරඟකරුවාගේ අලුත්ම (2026) paper එකෙන්**. ඊට වඩා ශක්තිමත් සාක්ෂියක් නෑ.

---

### 📋 කණ්ඩායම B — පුළුල් සමීක්ෂණය (round 1: papers 33)

> ⚠️ **තත්ත්ව column එක බලන්න:** `✅ full-text` = කියවා තහවුරු කර ඇත · `🔎 abstract` = abstract පමණක් · `⬜ pending` = තවම කියවා නෑ.
> **T2.4 එකේදී ඉතිරි ඒවා කියවා ✅ කරන්න.**

#### B1 · Human Digital Twin (core — වැදගත්ම කණ්ඩායම)

| # | Ref | Yr | Venue | Cites | වර්ගය | තත්ත්වය |
|---|---|---|---|---|---|---|
| 4 | ★★ **Wang, Zhou, Li, Yang, Zheng, Ci, Yuan, Wuest, Yang & Wang** | 2023 | *Robotics & CIM* 85:102626 | **393** | **ක්ෂේත්‍රයේ ප්‍රධානම reference එක.** §II-C එකේ මුලින්ම cite කරන්න | ✅ metadata |
| 5 | ★ Gaffinet, Al Haj Ali, Naudet & Panetto | 2025 | *Computers in Industry* 166:104230 | 57 | SLR + concept disambiguation. **HDM / HDS / HDT / aHDT** — refs 113 | ✅ metadata |
| 6 | Lin, Chen, Ali, Nugent, Cleland, Li, Ding & Ning | 2024 | *J. Cloud Computing* 13(1):131 | 82 | Survey | ✅ metadata |
| 7 | Bucci, Fani & Bandinelli | 2024 | *Sustainability* 17(1):129 | 50 | Review | ✅ metadata |
| 8 | Wang et al. — HDT-driven Human-Cyber-Physical Systems | 2022 | *Chinese J. Mech. Eng.* | 98 | Framework | 🔎 T2.10 |
| 9 | Montini et al. — IIoT Platform for **Human-Aware Factory DTs** | 2022 | *Procedia CIRP* | 25 | Platform | 🔎 T2.10 |
| 10 | A Systemic Human Digital Twin Model for Human-Centric Systems | 2025 | *IFAC-PapersOnLine* | — | Model | ⬜ pending |

#### B1b · ★ ERGONOMICS + DT *(T2.10 වලින් — ඔබේ gap එකට තීරණාත්මක)*

| # | Ref | Yr | Venue | Cites | ලක්ෂණය | තත්ත්වය |
|---|---|---|---|---|---|---|
| 11 | ★★ **Sharotry, Jimenez, Méndez Mediavilla, Wierschem, Koldenhoven & Valles** | 2022 | *IEEE Access* 10:12774–12791 | 40 | **Fatigue quantified** (joint angles + DTW + EWMA) — **detection පමණයි** | ✅ **READ** |
| 12 | ★★ **Greco, Caterino, Fera & Gerbino** | 2020 | *Applied Sciences* 10(21):7758 | 107 | **Ergonomics DT** — decision *support* පමණයි | ✅ **READ** |
| 13 | ★★ **Löcklin, Jung, Jazdi, Ruppert & Weyrich** | 2021 | *Procedia CIRP* 104:458–463 | 78 | **H-DT architecture.** Bi-directional flow අවශ්‍යතාවය කියයි | ✅ **READ** |
| 14 | Ramasubramanian et al. — DT for HRC in Manufacturing | 2022 | *Applied Sciences* | 73 | Review | 🔎 T2.10 |
| 15 | Liu et al. — Human-centric collaborative assembly, DT + wearable AR | 2022 | *J. Manufacturing Systems* | 66 | System | 🔎 T2.10 |
| 16 | Bousdekis et al. — HCPS framework for Operator 4.0 | 2020 | *Manufacturing Letters* | 65 | Framework | 🔎 T2.10 |
| 17 | Malik & Bilberg — DTs of human-robot collaboration | 2018 | *Procedia Manufacturing* 17:278–285 | 190 | Early DT+human | ✅ metadata |
| 18 | Ogunseiju et al. — DT framework for ergonomic risk self-management | 2021 | *J. Eng. Constr. Proj. Mgmt* | 46 | ⚠️ construction domain | 🔎 T2.10 |

#### B2 · Industry 5.0 frameworks & architectures

| # | Ref | Yr | Venue | Cites | වර්ගය | තත්ත්වය |
|---|---|---|---|---|---|---|
| 19 | ★ **Breque, De Nul & Petridis** — *Industry 5.0: Towards a Sustainable, Human-Centric and Resilient European Industry* | 2021 | European Commission | — | **මූලික නිර්වචනය — අනිවාර්ය** | ⚠️ **කර්තෘ නාම op.europa.eu එකෙන් තහවුරු කරන්න** |
| 20 | ★ **Xu, Lu, Vogel-Heuser & Wang** | 2021 | *J. Manufacturing Systems* 61:530–535 | **2,358** | **Industry 4.0 vs 5.0 වෙනස — අනිවාර්ය** | ✅ metadata |
| 21 | **Adel** — Future of Industry 5.0 in society | 2022 | *J. Cloud Computing* 11(1):40 | 829 | Human-centric solutions + research areas | ✅ metadata |
| 22 | Human-centric AI architecture for Industry 5.0 applications | 2022 | *Int. J. Production Research* · `10.1080/00207543.2022.2138611` | — | Architecture | ⬜ pending |
| 23 | Human-centric Industry 5.0 manufacturing: multi-level framework within Society 5.0 | 2025 | T&F · `10.1080/19397038.2025.2551000` | — | Framework (process/system/management) | 🔎 abstract |
| 24 | Towards AI-based Sustainable and XR-based human-centric manufacturing (ISO 23247) | 2025 | arXiv:2508.14580 | — | Implementation | ⬜ pending |

#### B2b · ★ ETHICS & PRIVACY *(T8.12 ට අත්‍යවශ්‍ය)*

| # | Ref | Yr | Venue | Cites | ලක්ෂණය | තත්ත්වය |
|---|---|---|---|---|---|---|
| 25 | ★★ **Cardin & Trentesaux** — Design and Use of Human Operator Digital Twins in Industrial CPS: **Ethical Implications** | 2022 | *IFAC-PapersOnLine* 55(2):360–365 | 19 | **Privacy/ethics ඡේදයට ප්‍රාථමික citation** | ✅ metadata |

#### B2c · Digital Twin පදනම *(M-DT එකට)*

| # | Ref | Yr | Venue | Cites | තත්ත්වය |
|---|---|---|---|---|---|
| 26 | Tao, Cheng, Qi, Zhang, Zhang & Sui — DT-driven product design, manufacturing and service | 2018 | *Int. J. Adv. Manuf. Technol.* | **2,439** | 🔎 T2.10 |
| 27 | Rasheed, San & Kvamsdal — DT: Values, Challenges and Enablers | 2020 | *IEEE Access* 8:21980–22012 | 1,770 | ✅ metadata |
| 28 | Qi, Tao, Hu, Anwer, Liu, Wei, Wang & Nee — Enabling technologies and tools for DT | 2019 | *J. Manufacturing Systems* | 1,289 | 🔎 T2.10 |
| 29 | Aivaliotis, Georgoulias & Chryssolouris — DT for **predictive maintenance** | 2019 | *Int. J. Comput. Integr. Manuf.* | 334 | 🔎 T2.10 |
| 30 | Zheng, Lu & Kiritsis — The emergence of **cognitive digital twin** | 2021 | *Int. J. Production Research* | 298 | 🔎 T2.10 |

#### B3 · Operator 4.0/5.0 · Fatigue · Ergonomics ★ *(ඔබේ H-DT එකට පදනම)*

| # | Ref | Yr | Venue | වර්ගය | තත්ත්වය |
|---|---|---|---|---|---|
| 36 | ★★ **Calzavara, Persona, Sgarbossa & Visentin** | 2019 | *IJPR* 57(3):948–962 · 78 cites | **Exponential fatigue accumulation (λ) + recovery (μ).** දෙකම **operator-specific**. Heart-rate calibrated. **Task assignment optimisation එකට යොදා ඇත** | ✅ **READ · T4.4 ප්‍රාථමික citation** |
| 37 | ★ **McAtamney & Corlett** — **RULA** | 1993 | *Applied Ergonomics* 24(2):91–99 · **3,285 cites** | **Ergonomic scoring — අනිවාර්ය** | ✅ metadata |
| 38 | Ma, Chablat, Bennis & Zhang — muscle fatigue & recovery model | 2010 | arXiv:1010.5891 | විකල්ප / cross-check fatigue model | 🔎 abstract |
| 39 | Operator 4.0 and Cognitive Ergonomics | 2020 | Springer chapter | Conceptual | ⬜ pending |
| 40 | A review on cognitive workload for Industry 5.0 | 2025 | *Computers & Industrial Eng.* | Review | ⬜ pending |
| 41 | Othman et al. — Workforce scheduling incorporating human factors | — | *JIEM* | Model | ⬜ pending |

> ✅ **T4.4 හි ලොකුම අවදානම විසඳී ඇත.** Calzavara et al. හි **λ (accumulation)** සහ **μ (alleviation)**
> parameters [04-framework-design.md §3](04-framework-design.md) හි අපගේ සමීකරණවලට **හරියටම ගැලපේ**.
> දෙකම **operator-specific** වීම නිසා, අපගේ human twin එක *generic worker model* එකක් නොව
> **පුද්ගලීකරණය කළ** එකක් බව තර්ක කළ හැක — Sharotry et al. (2022) කැඳවන දෙයම.

#### B4 · Multi-objective scheduling ★ *(ඔබේ optimiser එකට පදනම)*

| # | Ref | Yr | Venue | වර්ගය | තත්ත්වය |
|---|---|---|---|---|---|
| 31 | ★★ **Tan, Yuan, Wang & Zhang** — fatigue-conscious DRC-FJSP by enhanced NSGA-II | 2021 | *Comp. & Ind. Eng.* 160:107557 · **108 cites** | **ළඟම methodological competitor.** Fatigue + makespan — **නමුත් digital twin නෑ, sustainability නෑ** | ✅ metadata + abstract |
| 32 | ★ **Deb, Pratap, Agarwal & Meyarivan** — **NSGA-II** | 2002 | *IEEE Trans. Evol. Comput.* 6(2):182–197 · **48,367 cites** | **Algorithm citation — අනිවාර්ය** | ✅ metadata |
| 33 | ★★ **Destouet, Tlahig, Bettayeb & Mazari** — Multi-objective **sustainable** FJSP: economic, ecological, **social** | 2024 | *Comp. & Ind. Eng.* 195:110419 · 33 cites | ★ **People/Planet/Profit තුනම** — නමුත් digital twin නෑ. **අපගේ objective function එකට හොඳම සංසන්දනය** | ✅ metadata |
| 34 | Memetic NSGA-II for FJSP with real-time energy tariffs | 2023 | *Flexible Services & Mfg J.* | Energy-aware | ⬜ pending |
| 35 | Metaheuristics for multi-objective scheduling in Industry 4.0/5.0 | 2025 | *Frontiers in Industrial Eng.* | Survey | ⬜ pending |

#### B5 · Digital Twin + Sustainability

| # | Ref | Yr | Venue | වර්ගය | තත්ත්වය |
|---|---|---|---|---|---|
| 27 | Analysis of DT Applications in Energy Efficiency: Systematic Review | 2025 | *Sustainability* 17(8):3560 | SLR | ⬜ pending |
| 28 | AI-Driven Digital Twins in Sustainable Manufacturing: Critical Review | 2026 | *Sustainability* 18(11):5785 | Review | ⬜ pending |
| 29 | DT-driven carbon emissions management in manufacturing | 2025 | Elsevier | Framework | ⬜ pending |
| 30 | DT Integration in Circular Manufacturing | 2025 | *Sustainability* 17(16):7316 | Review | ⬜ pending |
| 31 | Energy Footprint Model for DT Workshop (low-carbon operation) | 2024 | MDPI (PMC11175332) | Model | ⬜ pending |

#### B6 · Explainable AI in manufacturing

| # | Ref | Yr | Venue | වර්ගය | තත්ත්වය |
|---|---|---|---|---|---|
| 32 | Lundberg & Lee — **SHAP** | 2017 | NeurIPS | **Method citation — අනිවාර්ය** | ⬜ pending |
| 33 | XAI in Manufacturing and Industrial CPS: A Survey | 2024 | *Electronics* 13(17):3497 | Survey | ⬜ pending |
| 34 | A review of XAI methods in manufacturing systems | 2025 | *Discover Applied Sciences* | Review | ⬜ pending |
| 35 | XAI-Driven Quality and Condition Monitoring in Smart Manufacturing | 2026 | *Sensors* 26(3):911 | Application | ⬜ pending |

---

### ★ ඔබේ අධ්‍යයනය — සංසන්දනාත්මක පිහිටීම

| # | Ref | Yr | Human factors? | Machine DT? | **Human DT (quantified)?** | Sustainability? | Multi-obj? | XAI? | Validation |
|---|---|---|---|---|---|---|---|---|---|
| **★** | **මෙම අධ්‍යයනය** | 2026 | ✅ | ✅ | ✅ **fatigue + skill + RULA, hard constraints ලෙස** | ✅ kWh/unit + CO₂e + scrap | ✅ NSGA-II | ✅ SHAP + override | Co-simulation, 30 replications, 3 scenarios |

### Column අර්ථ

| Column | ✅ දෙන්නේ කවදාද |
|---|---|
| **Human factors?** | මිනිසා ගැන යම් සැලකිල්ලක් තියෙනවා නම් (conceptual වුණත්) |
| **Machine DT?** | යන්ත්‍රයට digital twin එකක් implement කරලා තියෙනවා නම් |
| **Human DT?** | ★ මිනිසාට **සංඛ්‍යාත්මක** twin එකක් තියෙනවා නම් (මේ column එක බොහෝ විට හිස්) |
| **Sustainability?** | Energy/carbon/waste මනිනවා නම් |
| **XAI?** | AI තීරණය පැහැදිලි කරනවා නම් |

---

## §4 · Gap Statement (T2.6) 🚪★

### තත්ත්වය: **තහවුරු කර ඇත (අර්ධ වශයෙන්)** — 2026-08-03

Round 1 (papers 33) සහ full-text කියවූ 3 මත පදනම්ව, **gap එක ඇත්තටම පවතී**.

### 🔬 සාක්ෂි — කියවූ competitors **9** (**තහවුරු කර ඇත**)

| Paper | Cites | Machine DT | Human state **quantified** | **තීරණයට යොදයිද** | Sustainability **measured** | Multi-obj |
|---|---|---|---|---|---|---|
| Modoni & Sacco (2023) | 59 | ✅ | ❌ | ❌ | ❌ | ❌ |
| Tóth et al. (2023) | 112 | ❌ | ❌ | ❌ | ❌ | ❌ |
| Löcklin et al. (2021) | 78 | ⚠️ | ❌ | ❌ | ❌ | ❌ |
| Crnjac Žižić et al. (2025) | 4 | ⚠️ | ❌ | ⚠️ | ⚠️ වචනයෙන් | ❌ |
| Greco et al. (2020) | 107 | ❌ | ✅ ergonomics | ⚠️ support | ❌ | ❌ |
| Sharotry et al. (2022) | 40 | ❌ | ✅ fatigue | ❌ detection | ❌ | ❌ |
| Tan et al. (2021) | 108 | ❌ | ✅ fatigue | ✅ scheduling | ❌ | ✅ |
| **★ මෙම අධ්‍යයනය** | — | ✅ | ✅ | ✅ | ✅ | ✅ |

> 🎯 **පැහැදිලි රටාව:** **එකම column එකක්වත් සම්පූර්ණ නෑ.**
> Digital twin තියෙන අයට fatigue නෑ. Fatigue තියෙන අයට digital twin නෑ. **කාටවත් sustainability නෑ.**

### ✅ **`[N]` ගණන් කර ඇත — 2026-08-06**

> කලින් ලේඛන 4ක **52 / 47 / 53** කියලා තිබුණා. ඒවා **එකම දේ ගැන නොවේ**:
> 52 = round 3 screening · 47 = කණ්ඩායම B rows · 53 = Destouet 2026 එකතු කළාට පස්සේ.
> ➜ **ගණන් කරලා විසඳුවා** — පේළි එකින් එක, අනන්‍යතාවෙන් dedupe කරලා.

#### ගණන් කිරීම

```
කණ්ඩායම A  (ළඟම competitors)                                       =  9
කණ්ඩායම B  (පුළුල් සමීක්ෂණය · පේළි ගණන් කළා)                         = 47
A ∩ B  (Tan · Sharotry · Greco · Löcklin · Destouet 2024)          =  5
                                                                    ─────
UNION  =  9 + 47 − 5                                                = 51  records
```

> ⚠️ **කණ්ඩායම B එකේ `#` අංක නැවත භාවිතා වෙලා** — B5 = 27–31, B6 = 32–35, ඒවා
> B2c සහ B4 සමඟ ගැටෙනවා. **අංකවලින් ගණන් කරන්න බෑ; පේළි ගණන් කරන්නම ඕන.**
> *(කලින් 47/52/53 පටලැවුණේ මේකෙන්.)*

#### ➜ `[N]` = **46** — *"published between 2018 and 2026"*

Union 51 න් **5ක්** window එකෙන් පිට හෝ නොදන්නා, සහ ඒවා **reviewed studies නොව method citations**:

| ඉවත් කළේ | වර්ෂය | ඇයි |
|---|---|---|
| McAtamney & Corlett — **RULA** | 1993 | method citation |
| Deb et al. — **NSGA-II** | 2002 | method citation |
| Ma et al. — muscle fatigue | 2010 | window එකෙන් පිට |
| Lundberg & Lee — **SHAP** | 2017 | method citation |
| ⚠️ **Othman et al.** — *JIEM* | **වර්ෂය නෑ** | තහවුරු කරන්න බෑ ➜ ගණනට ගත්තේ නෑ |

```
51 − 5  =  46  studies published 2018–2026          ← ★ මේක තමයි [N]
```

> ⚠️ **ඉතුරු එකම දෙය:** Othman et al. (*JIEM*, "Workforce scheduling incorporating human
> factors") හි **වර්ෂය table එකේ නෑ**. ඒක **2018 හෝ ඊට පසුව** නම් → **N = 47**.
> ➜ ගණනට නොගැනීම **conservative** — වැරදි දිශාවට වැරදෙන එකක් නොවේ.

#### ඇගයීමේ ගැඹුර — *"none"* කියන්න පුළුවන් කීයකටද?

| | ගණන |
|---|---|
| Records screened (A ∪ B) | **51** |
| ★ **Published 2018–2026** → `[N]` | **46** |
| Abstract මට්ටමින් හෝ ඊට වඩා **ඇගයූ** | **31** |
| **Full text කියවූ** (කණ්ඩායම A) | **9** |
| ★★ **තුනම එකවර ✅** | **0** |

> ⚠️ කණ්ඩායම B හි **15ක් තවම `⬜ pending`**. ඒ නිසා *"none of 46"* කියන එක
> **ඇගයීමේ ගැඹුර නොකියා ලියන්න එපා** — reviewer කෙනෙක් *"46ම කියෙව්වද?"* කියලා අහනවා.
>
> ✅ **මෙසේ ලියන්න** *(සම්පූර්ණයෙන් සත්‍ය, තවමත් ශක්තිමත්)*:
>
> > *"Of the 46 studies published between 2018 and 2026 — 31 assessed at abstract level or
> > beyond, and the nine most closely related read in full — none couples a quantified human
> > twin, a machine twin and measured sustainability objectives within a single decision
> > framework."*

### 📊 අවසන් සංඛ්‍යා

| ප්‍රශ්නය | Paper ගණන |
|---|---|
| මුළු papers (N) | ✅ **46** *(2018–2026 · screened 51)* |
| Machine DT ✅ | `[X]` |
| Human-side model කිසියම් ආකාරයක ✅ | `[Y]` |
| ★ Human state **quantified & decision-coupled** ✅ | `[Z]` *(දැනට හඳුනාගත්තේ: **1** — Tan et al.)* |
| Sustainability **measured** ✅ | `[W]` |
| ★★ **තුනම එකවර ✅** | **0** ← 47 අතරින් **එකක්වත් නෑ** |

### ✍️ Gap Statement — කෙටුම්පත **v2** *(citation-backed)*

> *Our review of **46** studies published between 2018 and 2026 reveals that the field is **bifurcated**, and that the two halves have not been joined.*
>
> ***First**, digital-twin research that adopts a human-centric framing represents the operator through **static profile data** rather than dynamic physiological state. The Human Digital Twin framework of Modoni and Sacco [1] models worker capabilities, aspirations and attitudes, but computes neither fatigue nor ergonomic risk — a limitation the authors themselves identify as unaddressed. Others remain entirely conceptual, offering no computable human parameters and no experimental validation [2].*
>
> ***Second**, the complementary body of work **does quantify operator state, but stops short of decision-making**. Sharotry et al. [3] detect biomechanical fatigue from joint-angle dynamics with considerable rigour, yet the resulting fatigue estimate is used for monitoring only and is never fed back into task allocation; the authors conclude by calling for "a true personalized DT for an operator". Greco et al. [4] compute ergonomic indices within a human digital twin, but the twin informs manual decision support rather than automated optimisation. Where fatigue does drive scheduling — as in the enhanced NSGA-II formulation of Tan et al. [5] — no machine-side digital twin exists, so machine health, energy consumption and quality risk cannot participate in the allocation decision.*
>
> ***Third**, the requirement to join these halves has been **explicitly stated but not met**. Löcklin et al. [6] argue that Operator 4.0 applications "require a bi-directional flow of information and need data, models and simulations of machines as well as humans", yet present an architecture without implementation, optimisation or sustainability objectives. Meanwhile, environmental performance is almost never co-optimised with human wellbeing: recent human-centric digital twin work invokes sustainability rhetorically while reporting no energy or carbon accounting [7]. Of the **46** studies published between 2018 and 2026 — **31** assessed at abstract level or beyond, and the **nine** most closely related read in full — **none** couples a quantified human twin, a machine twin and measured sustainability objectives within a single decision framework.*
>
> *This study addresses all three gaps.*

> ✅ **Citations [1]–[7] සියල්ලම තහවුරු කර ඇත** — වෙනස් කරන්න එපා.
> ✅ **`[N]` = 46 පුරවා ඇත (2026-08-06)** — ගණන් කිරීම §4 මුල බලන්න.
> ⚠️ **එකම ඉතුරු දෙය:** Othman et al. (*JIEM*) හි වර්ෂය — 2018+ නම් N = 47.

### 🚪 GATE 2 තත්ත්වය

- [x] Gap එකේ **දිශාව** තහවුරු — competitors **9ක්** කියවා
- [x] **Citation-backed** තර්කයක් ලියා ඇත (v2)
- [x] ★ **තරඟකරුවන්ගේම වචන 3ක්** gap එකට සහාය දෙයි (Sharotry, Löcklin, Modoni)
- [x] "තුනම එකවර ✅" = **0 / 46** — තහවුරු කර ඇත
- [x] ✅ **`[N]` = 46** — ගණන් කර ඇත (2026-08-06) · screened 51 · ඇගයූ 31 · full-text 9
- [ ] Supervisor අනුමැතිය

---

## §5 · මූලික තේමා (Related Work කොටසට)

Related Work එක **උප-කොටස් 4කට** කඩන්න:

| # | තේමාව | ආවරණය කරන දේ |
|---|---|---|
| **A** | Industry 5.0 සහ human-centric manufacturing | නිර්වචන, EU Industry 5.0 pillars, Operator 4.0/5.0 |
| **B** | Manufacturing හි Digital Twins | Architectures, fidelity levels, applications |
| **C** | Human Digital Twins | ★ මේකට වැඩිම අවධානය — මෙතනයි gap එක |
| **D** | Sustainable & multi-objective production optimisation | NSGA-II, energy-aware scheduling |

**සෑම උප-කොටසක්ම මෙසේ අවසන් කරන්න:**
> *"However, `[මේ ක්ෂේත්‍රයේ අඩුපාඩුව]`."*

---

## §6 · මූලික References (පටන් ගන්න මේවායින්)

> මේවා **යෝජනා** පමණයි. ඔබම හොයලා තහවුරු කරගන්න.

| Topic | හොයන්න |
|---|---|
| Industry 5.0 නිර්වචනය | European Commission — *Industry 5.0: Towards a Sustainable, Human-Centric and Resilient European Industry* (2021) |
| Operator 4.0 | Romero et al. — *Towards an Operator 4.0 Typology* |
| Digital Twin අර්ථ දැක්වීම | Tao et al. — *Digital Twin in Industry: State-of-the-Art* |
| Human Digital Twin | "human digital twin manufacturing survey" කියලා search කරන්න (2022+) |
| Multi-objective scheduling | Deb et al. — *NSGA-II* (algorithm එකට cite කරන්න ඕන) |
| Fatigue modelling | "operator fatigue model manufacturing exponential" |
| RULA ergonomics | McAtamney & Corlett (1993) — RULA |
| XAI in manufacturing | Lundberg & Lee — *SHAP* (2017) |

---

## §7 · Reference Manager (T2.1)

- [ ] **Zotero** install කරන්න (නොමිලේ) → zotero.org
- [ ] Browser connector එක install කරන්න
- [ ] `ICARC-Industry5.0` කියලා collection එකක් හදන්න
- [ ] Sub-collections: `A-Industry5`, `B-DigitalTwin`, `C-HumanDT`, `D-Optimization`
- [ ] BibTeX export → `paper/references.bib`

---

## 📎 සටහන්

```
[කියවපු papers ගැන වැදගත් සටහන් මෙතන ලියන්න]
```
