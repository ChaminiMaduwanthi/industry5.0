# ✍️ Paper Outline

> **Phase 8 සඳහා.** Tasks T8.1 – T8.15
> ඉලක්කය: පිටු 6ක conference paper එකක් (IEEE format).

---

## §1 · ලිවීමේ අනුපිළිවෙල ★

> ⚠️ **පිළිවෙලට ලියන්න එපා!** මේ අනුපිළිවෙලට ලියන්න:

| ලියන අනුපිළිවෙල | කොටස | ඇයි මේ පිළිවෙල |
|---|---|---|
| **1වෙනුව** | §3 Proposed Framework | ඔබ දන්නා දේ. Phase 3 එකෙන් සූදානම්. |
| **2වෙනුව** | §2 Related Work | Phase 2 එකෙන් සූදානම්. |
| **3වෙනුව** | §4 Implementation & Setup | Phase 4–6 එකෙන් සූදානම්. |
| **4වෙනුව** | §5 Results & Discussion | Phase 7 එකෙන් සූදානම්. |
| **5වෙනුව** | §6 Limitations & Future Work | ප්‍රතිඵල දැක්කම පැහැදිලියි. |
| **6වෙනුව** | §1 Introduction | ප්‍රතිඵල දන්නවා නම් ලියන්න පහසුයි. |
| **7වෙනුව** | §7 Conclusion | Introduction එකේ පිළිබිඹුව. |
| **8වෙනුව** | **Abstract** | හැම දේම දන්නාට පස්සේ. |

---

## §2 · පිටු වෙන් කිරීම (පිටු 6)

| කොටස | පිටු | වචන ≈ |
|---|---|---|
| Abstract | — | 200 |
| 1. Introduction | 0.75 | 600 |
| 2. Related Work | 1.00 | 800 |
| 3. **Proposed Framework** ★ | 1.75 | 1,200 + Fig 1, 2 |
| 4. Implementation & Setup | 0.75 | 500 + Table I |
| 5. **Results & Discussion** ★ | 1.25 | 900 + Table II, Fig 3–5 |
| 6. Limitations & Future Work | 0.25 | 200 |
| 7. Conclusion | 0.25 | 200 |
| References | (ඉතිරිය) | 30–35 refs |

---

## §3 · කොටස් අනුව ව්‍යුහය

### Abstract (T8.9) — වාක්‍ය 6ක සූත්‍රය

```
1. සන්දර්භය   : Industry 5.0 මිනිසා මධ්‍යයට ගෙන එයි, නමුත් …
2. ගැටලුව     : පවතින digital twins asset-centric ය; මිනිස් සාධක conceptual පමණි.
3. අප කරන දේ  : අපි layer 5ක framework එකක් ඉදිරිපත් කරමු, machine + human twin එකට සම්බන්ධ කරමින්.
4. ක්‍රමවේදය   : Co-simulation, benchmark datasets 3ක්, NSGA-II, replications 30ක්.
5. ප්‍රතිඵල   : Fatigue X% ↓, ergonomic risk Y% ↓, energy/unit Z% ↓, throughput W% ↓ පමණි.
6. වැදගත්කම   : මිනිස් සුබසාධනය hard constraint එකක් කිරීම කුඩා efficiency වියදමකින් හැකි බව පෙන්වයි.
```

**Keywords (5–6):** `Industry 5.0` · `Human Digital Twin` · `Sustainable Manufacturing` · `Multi-objective Optimisation` · `Explainable AI` · `Human-Centric Design`

---

### 1. Introduction (T8.7)

| ¶ | අන්තර්ගතය |
|---|---|
| ¶1 | **සන්දර්භය** — Industry 4.0 → 5.0 සංක්‍රමණය. EU නිර්වචනය. කුලුනු 3: human-centricity, sustainability, resilience. |
| ¶2 | **ගැටලුව** — Digital twin පර්යේෂණ asset-centric ය. මිනිසා "user" කෙනෙක් මිස "modelled entity" කෙනෙක් නොවේ. |
| ¶3 | **පරතරය** — Human wellbeing + sustainability එකවර optimize කරන, ක්‍රියාත්මක framework එකක් නෑ. |
| ¶4 | **අපගේ ප්‍රවේශය** — Layer 5, twin දෙක coupled, human factors hard constraints ලෙස. |
| ¶5 | **දායකත්ව** — bullet 3 (පහත බලන්න) |
| ¶6 | **ලිපියේ ව්‍යුහය** — "Section II reviews… Section III presents…" |

**දායකත්ව bullet 3 (¶5):**

> *The contributions of this paper are threefold:*
> - *(i) **A five-layer human-centric reference architecture** that couples a machine digital twin with a human digital twin through five explicitly defined bidirectional coupling points;*
> - *(ii) **A quantified Human Digital Twin model** in which operator fatigue, skill and ergonomic risk are formulated as computable state variables and enforced as hard constraints — rather than soft penalties — within production decision-making;*
> - *(iii) **Empirical evidence** from a 30-replication co-simulation study across three operating scenarios, showing that human-centric optimisation reduces operator fatigue by `[X]`% and ergonomic risk by `[Y]`% at a throughput cost of only `[Z]`% relative to an Industry 4.0 baseline.*

---

### 2. Related Work (T8.3)

උප-කොටස් 4ක්:

| § | මාතෘකාව | අවසන් වාක්‍යය |
|---|---|---|
| II-A | Industry 5.0 සහ Human-Centric Manufacturing | *"However, these remain largely conceptual…"* |
| II-B | Manufacturing හි Digital Twins | *"However, operator state is typically absent…"* |
| II-C | ★ Human Digital Twins | *"However, few couple the human twin to production decisions…"* |
| II-D | Sustainable & Multi-Objective Scheduling | *"However, human wellbeing is rarely among the objectives…"* |

**අවසානයේ:** Comparison table (Table I) + gap paragraph.

---

### 3. Proposed Framework (T8.2) ★★ — **වැදගත්ම කොටස**

| § | මාතෘකාව | අන්තර්ගතය |
|---|---|---|
| III-A | Architecture Overview | **Fig. 1** + layer 5 විස්තරය |
| III-B | Machine Digital Twin | State variables table + update rules |
| III-C | ★ Human Digital Twin | State variables + fatigue eq. + RULA. **වැඩිම ඉඩ මෙතන.** |
| III-D | ★ Twin Coupling | **Fig. 2** + coupling points CP1–CP5 |
| III-E | Multi-Objective Formulation | Objective function eq. + weights |
| III-F | ★ Human-Centric Constraints | HC1–HC4. *"hard vs soft"* තර්කය. |
| III-G | Explainability & Human Oversight | SHAP + override mechanism |

> 💡 **III-F එකේ මේ වාක්‍යය දාන්න:**
> *"The distinction between Industry 4.0 and Industry 5.0 optimisation is, in our formulation, precisely the distinction between treating operator state as a soft penalty and treating it as a hard constraint. Under the former, sufficient efficiency gain will always justify operator strain; under the latter, it never can."*

---

### 4. Implementation & Experimental Setup (T8.4)

| § | මාතෘකාව |
|---|---|
| IV-A | Co-simulation environment (SimPy, parameters) |
| IV-B | Datasets සහ preprocessing (**Table: Data sources**) |
| IV-C | AI models (XGBoost, NSGA-II, SHAP) + hyperparameters |
| IV-D | Baselines B1, B2, B3 |
| IV-E | Scenarios S1, S2, S3 + evaluation protocol (30 seeds) |

---

### 5. Results & Discussion (T8.5) ★★

| § | මාතෘකාව | Figure/Table |
|---|---|---|
| V-A | Overall KPI comparison | **Table II** |
| V-B | ★ Trade-off analysis | **Fig. 3** (Pareto front) |
| V-C | Scenario-wise behaviour (විශේෂයෙන් S2 high-demand) | **Fig. 5** |
| V-D | Sensitivity to objective weights | Table III |
| V-E | Explainability & operator oversight | **Fig. 6** |
| V-F | Discussion — මේවා අදහස් කරන්නේ මොකක්ද? | — |

> 💡 **V-F එකේ මේ 3 කතා කරන්න:**
> 1. Trade-off එක කුඩායි — human-centricity ලාභදායකයි
> 2. H2 (මිනිසාට හොඳ දේ machine එකටත් හොඳයි) සනාථ වුණාද?
> 3. W-Profit ≈ B2 — Industry 4.0 යනු අපගේ framework එකේ විශේෂ අවස්ථාවකි

---

### 6. Limitations & Future Work (T8.6)

**අවංකව ලියන්න** — reviewers ට ගරු කරන බව පෙන්නනවා.

| # | සීමාව | Future work |
|---|---|---|
| 1 | Simulation-based; real factory validation නෑ | Pilot deployment |
| 2 | Human twin empirical models මත; ඇත්ත wearable දත්ත නෑ | Real operator sensor study |
| 3 | කුඩා පරිමාණය (5 machines, 3 operators) | Scale-up study |
| 4 | Operator trust/acceptance මනා නෑ | TAM/NASA-TLX user study |
| 5 | ★ **Privacy & ethics** ගැඹුරින් නෑ | Privacy-preserving human twin (federated learning) |

---

### 7. Conclusion (T8.8)

වාක්‍ය 4ක්:
1. අපි මොකක්ද කලේ (framework එක)
2. කොහොමද validate කලේ (co-simulation, 30 replications)
3. ප්‍රධාන සොයාගැනීම (සංඛ්‍යා සමඟ)
4. පුළුල් වැදගත්කම (Industry 5.0 ට මොකද කියන්නේ)

> ❌ **Conclusion එකේ අලුත් තොරතුරු දාන්න එපා.**

---

## §4 · Privacy & Ethics ඡේදය (T8.12) ★

> ⚠️ මිනිස් දත්ත එකතු කරන නිසා **මේක අනිවාර්යයි**. §6 එකේ හෝ §3-G එකේ දාන්න.

**කෙටුම්පත:**

> *A human digital twin necessarily processes data about identifiable workers, raising legitimate concerns about surveillance. Three design decisions in our framework are intended to mitigate this. First, the human twin models only task-relevant state — fatigue, skill and posture — and never health records, location outside the work cell, or affective state beyond workload. Second, all human-derived variables enter the optimiser as **protective** constraints: they can only restrict what is asked of an operator, never justify asking more. Third, the operator override mechanism (Section III-G) ensures that the system's authority is advisory. We note, however, that consent, data retention and the boundary between assistance and monitoring require empirical study with actual workers, which we leave to future work.*

---

## §5 · අවසන් Checklist (T8.10, T8.11, T8.13)

### ආකෘතිය
- [ ] Conference template එක නිවැරදිද? (IEEE conference, 2-column)
- [ ] පිටු ගණන සීමාව තුළද?
- [ ] Author info + affiliation නිවැරදිද?
- [ ] Section numbering නිවැරදිද?

### අන්තර්ගතය
- [ ] Contributions bullet 3 Introduction එකේ තියෙනවාද?
- [ ] Gap statement එකේ **ඇත්ත සංඛ්‍යා** තියෙනවාද?
- [ ] හැම claim එකකටම සාක්ෂියක් තියෙනවාද?
- [ ] Throughput trade-off එක **පැහැදිලිව** කියලා තියෙනවාද? (වහලා නෑනේ?)
- [ ] p-values + effect sizes report කරලාද?
- [ ] Privacy/ethics ඡේදය තියෙනවාද?
- [ ] Limitations අවංකද?

### References
- [ ] 30+ ද?
- [ ] 2021ට පස්සේ ඒවා 60%+ ද?
- [ ] සියලු citations text එකේ පාවිච්චි වෙලාද?
- [ ] BibTeX format එක consistent ද?
- [ ] Self-citation අධික නැද්ද?

### Figures & Tables
- [ ] හැම figure එකකටම text එකේ reference එකක් තියෙනවාද? ("as shown in Fig. 3")
- [ ] Captions විස්තරාත්මකද? (figure එක තනියම තේරෙන්න ඕන)
- [ ] කළු-සුදු print කලාම කියවන්න පුළුවන්ද? ★
- [ ] Font size 8pt ට වඩා ලොකුද?
- [ ] Axis labels + units තියෙනවාද?

### අවසන්
- [ ] Grammar check (Grammarly)
- [ ] Plagiarism check (Turnitin) — 15% ට අඩුද?
- [ ] Supervisor කියෙව්වාද?
- [ ] සමාන පර්යේෂකයෙක් කියෙව්වාද?
- [ ] Code GitHub එකේද? Link එක paper එකේද?
- [ ] Submission portal එකේ deadline එක බැලුවාද?

---

## §6 · පොදු වැරදි — වළක්වා ගන්න

| ❌ වැරදි | ✅ නිවැරදි |
|---|---|
| "Our framework is better" | "Our framework reduces fatigue by 35% (p < 0.01, d = 1.2)" |
| Throughput අඩුවීම වහනවා | ඒක ප්‍රධාන findings එකක් ලෙස ඉදිරිපත් කරනවා |
| Baseline එකක් නැතුව ප්‍රතිඵල | B1, B2, B3 සංසන්දනය |
| එක run එකක ප්‍රතිඵල | 30 runs, mean ± std, statistical test |
| "Human-centric" කියලා විතරක් කීම | Fatigue, RULA සංඛ්‍යාත්මකව පෙන්වීම |
| Related work = paper ලැයිස්තුවක් | Related work = gap එකට යන තර්කයක් |
| Limitations නොලිවීම | අවංකව ලිවීම |
| Figures කුඩා/අපැහැදිලි | Vector format, ලොකු font |
