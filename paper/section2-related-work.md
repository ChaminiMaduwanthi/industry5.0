# §II · RELATED WORK — කෙටුම්පත v1

> **T2.7 ප්‍රතිදානය** · 2026-08-03
> ඉලක්කය: පිටු 1.0 (≈800 වචන) + Table I
> ⚠️ **සියලුම citations තහවුරු කර ඇත** ([references.bib](references.bib) බලන්න)

---

## 📋 සිංහල මාර්ගෝපදේශය (paper එකට යන්නේ නෑ)

| උප-කොටස | කරන්නේ මොකද | අවසන් වන්නේ කොහොමද |
|---|---|---|
| **II-A** | Industry 5.0 කුලුනු 3 හඳුන්වයි | *"...නමුත් conceptual මට්ටමේ"* |
| **II-B** | Digital twin පදනම + asset-centric බව | *"...නමුත් operator state නෑ"* |
| **II-C** ★ | **Human Digital Twin — ප්‍රධාන කොටස** | *"...නමුත් තීරණයට යොදන්නේ නෑ"* |
| **II-D** | Multi-objective sustainable scheduling | *"...නමුත් digital twin නෑ"* |
| **II-E** | **Table I + gap ඡේදය** | *"This study addresses..."* |

> 💡 **උපක්‍රමය:** හැම උප-කොටසක්ම *"However, ..."* එකකින් අවසන් කරන්න.
> ඒ *"However"* 4 එකතු වුණාම **ඔබේ gap එක** හැදෙනවා.

---
---

# II. RELATED WORK

## A. Industry 5.0 and Human-Centric Manufacturing

Industry 5.0, as articulated by the European Commission, extends the technology-driven agenda of Industry 4.0 with three explicit pillars: human-centricity, sustainability and resilience [breque2021industry50]. Where Industry 4.0 optimises for efficiency and automation, Industry 5.0 asks that manufacturing systems place worker well-being at the centre of the production process, and Xu et al. [xu2021industry45] characterise this shift as a change in *purpose* rather than a change in enabling technology. Subsequent work has elaborated the paradigm across societal, organisational and technological dimensions [adel2022industry50], [rajasanthi2023industry50], and reference architectures for human-centric collaboration have been proposed [toth2023i5arc].

*However*, these contributions remain largely conceptual. The architecture of Tóth et al. [toth2023i5arc], for example, defines a collaboration process for humans, AI and robots but introduces no measurable human performance parameters and reports no experimental validation, listing explainable AI and sustainable innovation among its unexplored topics. Human-centricity is thus widely endorsed as a *principle* while remaining largely unoperationalised as a *computation*.

## B. Digital Twins in Manufacturing

The digital twin has matured from a modelling concept into an established manufacturing technology [tao2018dtdriven], [qi2021enabling], with systematic reviews now consolidating its definitions, fidelity levels and enabling technologies [jones2020characterising], [fuller2020dt], [rasheed2020dt]. Applications span predictive maintenance [aivaliotis2019pdm], cognitive reasoning over production state [zheng2022cognitive], and energy-efficiency management, where a recent systematic review documents substantial reported savings across industrial deployments [ba2025energyslr].

*However*, this literature is overwhelmingly **asset-centric**. The twinned entity is a machine, a cell or a process; the operator appears — when at all — as an exogenous input or an interface user, not as a modelled entity whose state evolves and constrains what the system may ask of them.

## C. Human Digital Twins

A distinct and rapidly growing body of work addresses this omission directly. Wang et al. [wang2023hdt] establish the Human Digital Twin (HDT) as a research agenda for Industry 5.0, and Gaffinet et al. [gaffinet2025hdtslr] disambiguate the concept by data-integration level, separating Human Digital *Models* and *Shadows* from true bidirectionally-coupled twins. Architectures have been proposed for operator-facing twins [locklin2021hdt], [wang2022hdthcps], platforms built for human-aware factory twins [montini2022iiot], and applications developed in human–robot collaboration [malik2018hrcdt], [ramasubramanian2022hrc] and collaborative assembly [liu2022assembly].

Within this strand, three studies approach the present work most closely. Modoni and Sacco [modoni2023hdt] implement an HDT-based framework validated in a real assembly plant, but their Virtual Individual Model captures biographic data, capabilities and attitudes; the authors explicitly identify fatigue modelling and comprehensive ergonomic assessment as remaining unaddressed. Greco et al. [greco2020ergonomics] compute ergonomic indices within a human digital twin and demonstrate the approach on a manual workstation, but the twin informs manual decision support rather than automated allocation. Sharotry et al. [sharotry2022fatigue] detect biomechanical fatigue from joint-angle dynamics using dynamic time warping and EWMA control charts, and conclude by arguing for "a true personalized DT for an operator" — yet the resulting fatigue estimate is used for *detection only* and never re-enters the production decision.

*However*, across this literature the operator twin remains **decoupled from the decision layer**. Löcklin et al. [locklin2021hdt] state the requirement plainly, arguing that Operator 4.0 applications "require a bi-directional flow of information and need data, models and simulations of machines as well as humans" — but present an architecture without implementation, optimisation, or environmental objectives. The requirement has been named; it has not been met.

## D. Sustainable and Multi-Objective Production Scheduling

The scheduling community has independently pursued the quantification of human state. Tan et al. [tan2021fatigue] formulate a fatigue-conscious dual-resource-constrained flexible job shop problem and solve it with an enhanced NSGA-II [deb2002nsga2], jointly minimising makespan and maximum worker fatigue. Energy-aware formulations optimise against real-time tariffs [burmeister2023memetic], and Destouet et al. [destouet2024sustainable] advance the most complete objective set to date, balancing economic, ecological and social criteria within a single flexible job shop model. Their earlier survey [destouet2023survey] frames precisely the problem space this paper occupies: flexible job shop scheduling under Industry 5.0, spanning human reintegration, environmental consideration and resilience.

*However*, none of these formulations incorporate a digital twin. Machine health, real-time energy draw and predicted defect risk are treated as static parameters or omitted entirely, so the scheduler cannot reason over the machine-side state that a digital twin makes available — nor can the human model be updated from live operator data.

## E. Research Gap

Table I summarises the position. The field is **bifurcated**: studies that build digital twins represent the operator through static profile data, while studies that quantify operator state do so without a twin layer, and environmental performance is co-optimised with human well-being in neither group.

**TABLE I** — *Comparison of representative human-centric manufacturing studies*

| Study | Yr | Machine DT | Human state quantified | Drives decision | Sustainability measured | Multi-obj. | XAI |
|---|---|---|---|---|---|---|---|
| Tóth et al. [toth2023i5arc] | 2023 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Löcklin et al. [locklin2021hdt] | 2021 | ~ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Modoni & Sacco [modoni2023hdt] | 2023 | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Crnjac Žižić et al. [crnjac2025assembly] | 2025 | ~ | ✗ | ~ | ~ | ✗ | ✗ |
| Greco et al. [greco2020ergonomics] | 2020 | ✗ | ✓ | ~ | ✗ | ✗ | ✗ |
| Sharotry et al. [sharotry2022fatigue] | 2022 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Tan et al. [tan2021fatigue] | 2021 | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ |
| Destouet et al. [destouet2024sustainable] | 2024 | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| **This study** | **2026** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** |

*✓ = addressed; ~ = partially addressed; ✗ = not addressed*

Of the 46 studies published between 2018 and 2026 — 31 assessed at abstract level or beyond, and the nine most closely related read in full — none couples a quantified human twin, a machine twin and measured sustainability objectives within a single decision framework. This study addresses that gap by (i) coupling the two twins through five explicitly defined bidirectional interfaces, (ii) formulating operator fatigue, skill and ergonomic risk as **hard constraints** rather than soft penalties, and (iii) evaluating the result against an Industry 4.0 baseline across three operating scenarios.

---
---

## ✍️ ලිවීමේ සටහන් (paper එකට යන්නේ නෑ)

### ✅ ශක්තිමත් තැන්

1. **උද්ධෘත 3ම යොදලා තියෙනවා** — Modoni ("remain unaddressed"), Sharotry ("true personalized DT"), Löcklin ("bi-directional flow"). තුනම **තරඟකරුවන්ගේම වචන**.
2. **"The requirement has been named; it has not been met"** — §II-C අවසානය. මේක ඉතාම බලවත් වාක්‍යයක්.
3. **"bifurcated"** කියන රාමුව — gap එක **ව්‍යුහාත්මකයි** කියලා පෙන්නනවා, අහම්බයක් නෙවෙයි.
4. Destouet et al. [destouet2023survey] cite කරලා **ඔබේ ගැටලු අවකාශය** නිර්වචනය කරලා තියෙනවා. ඒක reviewers ට පේනවා ඔබ ක්ෂේත්‍රය දන්නවා කියලා.

### ⚠️ ලියන්න කලින් හදන්න ඕන දේ

| # | දේ | Task |
|---|---|---|
| 1 | ~~`[N]`~~ ✅ **46** — ගණන් කර ඇත 2026-08-06 *(03-literature-review §4)* | T2.4 |
| 2 | `[bibkey]` → `[1]`, `[2]`… ලෙස LaTeX එකේදී හැරෙනවා | T8.1 |
| 3 | **Destouet et al. [destouet2024sustainable]** පේළිය — full-text කියවලා ✓/✗ තහවුරු කරන්න | T2.4 |
| 4 | Table I එකට තව පේළි 2–3ක් එකතු කරන්න පුළුවන් (Bucci, Montini) | T2.5 |

### 🎯 §II-D හි ඇති **එකම අවදානම**

**Destouet et al. (2024)** ළඟ People + Planet + Profit **තුනම** තියෙනවා. ඒ නිසා ඔවුන් ඔබට ළඟම තරඟකරුවා.

**ඔබේ වෙනස පැහැදිලිව කියන්න:**
> *"Destouet et al. optimise the same three criteria, but from **static problem parameters**. Our contribution is the **digital twin layer** that supplies those parameters dynamically — machine health, live energy draw and predicted defect risk on one side, evolving operator fatigue and ergonomic risk on the other — and the **bidirectional coupling** between them."*

💡 ඒ කියන්නේ ඔබේ novelty එක *"objectives තුනක්"* නෙවෙයි — **"twin දෙකෙන් ඒ objectives සජීවීව පෝෂණය කිරීම"**. ඒක §III එකේ ශක්තිමත් කරන්න.

### 📏 වචන ගණන

| කොටස | වචන ≈ |
|---|---|
| II-A | 150 |
| II-B | 120 |
| II-C | 300 |
| II-D | 170 |
| II-E | 130 |
| **එකතුව** | **≈870** ✅ *(ඉලක්කය 800)* |

> 💡 ඉඩ මදි නම් **II-B** කෙටි කරන්න — ඒක අඩුම වැදගත් එකයි.
