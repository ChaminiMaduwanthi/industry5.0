# 📝 Project Charter — පදනම

> **Phase 1 ප්‍රතිදානය.** Tasks T1.1 – T1.6
> මේක පුරවන්නේ **ඔබයි**. හිස් තැන් `[...]` වලින් සලකුණු කර ඇත.
> ⚠️ මේක අනුමත වෙන තුරු Phase 2 එකට යන්න එපා.

---

## §1 · Use Case එක (T1.1)

### නිර්දේශිත use case එක

> **CNC machining cell එකක බුද්ධිමත් කාර්ය බෙදාහැරීම**
> Machine 5ක් සහ operator 3ක් ඇති නිෂ්පාදන කොටසක, පැමිණෙන එක් එක් වැඩ order එක
> **කුමන operator ට** සහ **කුමන machine එකට** පවරන්නේද යන්න තීරණය කිරීම.

### ඇයි මේක හොඳ?

- ✅ Machine Twin එකට ඉඩ තියෙනවා (health, energy, quality)
- ✅ Human Twin එකට ඉඩ තියෙනවා (fatigue, skill, ergonomics)
- ✅ Sustainability මනින්න පුළුවන් (kWh/unit, scrap)
- ✅ Conference paper එකකට ගැලපෙන ප්‍රමාණය — ලොකු වැඩියි නෑ, පොඩි වැඩිත් නෑ

### ඔබේ තෝරාගැනීම

| ප්‍රශ්නය | පිළිතුර | තත්ත්වය |
|---|---|---|
| කර්මාන්ත වර්ගය | **CNC machining cell** (discrete manufacturing) | ✅ තහවුරු |
| Machine ගණන | **5** | ✅ තහවුරු |
| Operator ගණන | **3** | ✅ තහවුරු |
| Task වර්ග ගණන | **3** — Light / Medium / Heavy | ✅ තහවුරු |
| Shift දිග | **8 පැය (480 min)** | ✅ තහවුරු |
| Simulation කාලය | **shift 20ක්** | ✅ තහවුරු |
| Decision epoch | **15 min** | ✅ තහවුරු |

> 💡 **ශ්‍රී ලාංකික සන්දර්භය:** apparel manufacturing තෝරගත්තොත් local conference එකකට relevance එක වැඩියි. නමුත් CNC වලට public datasets වැඩියි. **CNC/general machining නිර්දේශ කරනවා**, discussion එකේ apparel context එක සඳහන් කරන්න.

---

## §2 · System Boundary (T1.2)

### ✅ ඇතුළත් (In Scope)

- [ ] Machine health & remaining useful life (RUL) පුරෝකථනය
- [ ] Machine බලශක්ති පරිභෝජනය
- [ ] නිෂ්පාදන ගුණාත්මකභාවය / defect අවදානම
- [ ] Operator fatigue (වෙහෙස)
- [ ] Operator skill–task ගැලපීම
- [ ] Operator ergonomic risk (posture)
- [ ] Task allocation තීරණය (කාට / කුමන machine එකට)
- [ ] Sustainability metrics (kWh/unit, CO₂e, scrap %)
- [ ] Explainable AI (තීරණය පැහැදිලි කිරීම)
- [ ] Operator override (මිනිසාට තීරණය වෙනස් කරන්න පුළුවන්)

### ❌ බැහැර (Out of Scope) — **මේක ලියන එකත් වැදගත්**

- [ ] Supply chain / logistics
- [ ] Physical robot control (ඇත්ත robot එකක් පාලනය කිරීම)
- [ ] Financial / cost modelling ගැඹුරින්
- [ ] Real factory deployment (මේක simulation study එකක්)
- [ ] Multi-factory / multi-site coordination
- [ ] Operator ගේ පෞද්ගලික සෞඛ්‍ය දත්ත (medical records)

---

## §3 · Objectives (T1.3)

| # | කුලුන | අරමුණ | ප්‍රාථමික KPI | ද්විතීයික KPI |
|---|---|---|---|---|
| **O1** | 👷 People | සේවක වෙහෙස සහ ශාරීරික අවදානම අවම කිරීම | Mean fatigue index (0–1) | RULA score, workload balance |
| **O2** | 🌱 Planet | බලශක්තිය සහ අපද්‍රව්‍ය අවම කිරීම | Energy per unit (kWh) | CO₂e (kg), Scrap rate (%) |
| **O3** | 💰 Profit | නිෂ්පාදනය සහ machine ලබා ගැනීම පවත්වා ගැනීම | Throughput (units/shift) | Downtime (hrs), OEE |

### KPI නිර්වචන (හරියටම ලියන්න)

```
Mean fatigue index = (හැම operator ගේම fatigue එකතුව) / (operator ගණන × time steps)
Energy per unit     = මුළු kWh / නිෂ්පාදිත ඒකක ගණන
CO₂e                = මුළු kWh × 0.53         # ශ්‍රී ලංකා grid emission factor
Scrap rate          = දෝෂ සහිත ඒකක / මුළු ඒකක × 100
Throughput          = shift එකකට නිෂ්පාදිත ඒකක
Downtime            = machine නවතින මුළු පැය ගණන
```

> ⚠️ **CO₂ factor එකට source එකක් දෙන්න** (CEB / IEA report). Paper එකේ cite කරන්න.

---

## §4 · Research Questions & Hypothesis (T1.4)

### Research Questions

| # | ප්‍රශ්නය | පිළිතුර දෙන Phase |
|---|---|---|
| **RQ1** | Machine Digital Twin එකක් සහ Human Digital Twin එකක් තනි framework එකකට integrate කරන්නේ කෙසේද? | Phase 3 |
| **RQ2** | People, Planet, Profit අතර trade-off එක AI මගින් සමතුලිත කරන්නේ කෙසේද? | Phase 3 + 5 |
| **RQ3** | මෙම human-centric ක්‍රමය, Industry 4.0 (efficiency-only) ක්‍රමයට වඩා කෙතරම් වඩා හොඳද? | Phase 6 + 7 |

### Hypothesis (H)

> **H1:** Human Digital Twin එකක් තීරණ ගැනීමට ඇතුළත් කිරීමෙන්, throughput හි **සුළු අඩුවීමක්** (≤10%) සමඟින්,
> operator fatigue සහ ergonomic risk හි **සැලකිය යුතු අඩුවීමක්** (≥20%) ලබාගත හැක.

> **H2:** Human-centric constraints මගින් machine downtime ද අඩු වේ (වෙහෙසුණු operator → වැඩි දෝෂ → වැඩි machine stress).

> 💡 **H2 එක සිත්ගන්නා සුළුයි** — "මිනිසාට හොඳ දේ machine එකටත් හොඳයි" කියන තර්කය. සනාථ වුණොත් ලස්සන discussion point එකක්.

---

## §5 · උපකල්පන සහ සීමා (T1.5)

### උපකල්පන (Assumptions)

1. Operator ලාගේ fatigue එක පිළිගත් exponential model එකකට අනුව හැසිරේ *(citation: `[...]`)*
2. Skill levels shift එක තුළ ස්ථිරව පවතී (ඉගෙනීම සලකා නොබලයි)
3. Machine degradation benchmark dataset එකේ pattern අනුව සිදුවේ
4. සියලු operator ලා shift එකේ ආරම්භයේ fatigue = 0 සමඟ පැමිණේ
5. Task duration ස්ථිර; setup time නොසලකයි

### සීමා (Limitations) — **paper එකේ §6 එකට යනවා**

1. Simulation-based; ඇත්ත කර්මාන්තශාලාවක validate කර නැත
2. Human twin එක empirical models මත පදනම්; ඇත්ත operator sensor දත්ත නොවේ
3. කුඩා පරිමාණය (machine 5, operator 3)
4. Privacy සහ ethics ගැඹුරින් අධ්‍යයනය නොකෙරේ (future work)
5. Operator acceptance / trust user study එකක් නොකෙරේ

---

## §6 · සාර්ථකත්ව නිර්ණායක (Success Criteria)

මේ ව්‍යාපෘතිය **සාර්ථකයි** කියන්නේ මේවා තියෙනවා නම්:

- [ ] Layer 5ක architecture diagram එකක් — පැහැදිලිව අඳින ලද
- [ ] `HumanTwin` class එකක් — variable 4ක්, සංඛ්‍යාත්මකව ක්‍රියාත්මක
- [ ] Baseline 3 (B1, B2, B3) — 30 replications × 3 scenarios
- [ ] KPI table එකක් — statistical significance (p < 0.05) සමඟ
- [ ] Pareto front figure එකක්
- [ ] පිටු 6ක paper එකක් — submit කරන ලද

---

## §7 · අනුමැතිය (T1.6)

| | නම | දිනය | අනුමතද |
|---|---|---|---|
| පර්යේෂක | `[...]` | 2026-08-03 | — |
| අධීක්ෂක (Supervisor) | `[...]` | 2026-08-03 | ✅ **අනුමතයි** |

> 🚪 **GATE 1 පසුයි.** Phase 2 (Literature Review) ආරම්භ කර ඇත — 2026-08-03.

---

## 📎 සටහන්

```
[මෙතන ඔබේ සටහන් ලියන්න — supervisor කියපු දේවල්, වෙනස් කරන්න කිව්ව දේවල් ...]
```
