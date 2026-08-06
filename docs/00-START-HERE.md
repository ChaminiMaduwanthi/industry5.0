# 🚦 START HERE — මුලින්ම මේක කියවන්න

> **අවසන් යාවත්කාලීනය: 2026-08-06**

---

## ⚡ 0. දැන් තියෙන තැන — විනාඩි 1කින්

```
Phase 1  ████████████████████  ✅  6/6     🚪 GATE 1 පසුයි
Phase 2  ██████████████░░░░░░  🟨  7/10    ([CHECK] 5 + papers කියවීම ඉතුරු)
Phase 3  ████████████████████  ✅  10/10    🚪 GATE 3 පසුයි — DESIGN FROZEN
Phase 4  ████████████████████  ✅  7/7     දත්ත සූදානම්
Phase 5  ██████████████░░░░░░  🟨  11/16    🚪 GATE 4 පසුයි · NSGA-II/SHAP/dashboard කැපුවා
Phase 6  █████████████████░░░  🟨  6/7     ★ runs 270 ✅  reproducible
Phase 7  ██████████████████░░  🟨  8/9     (T7.5 dashboard පමණයි)
Phase 8  ░░░░░░░░░░░░░░░░░░░░  ⬜  0/15    ← ★ දැන් මෙතන
                                  ──────
                                  55/80
```

### 👉 කරන්න ඕන දේ: **T8.2 — §3 Proposed Framework ලියන්න**

> 📊 **විශ්ලේෂණය ඉවරයි.** KPI table · figures 2 · sensitivity 3 · ablation ·
> §V draft (§A–§G, සංඛ්‍යා ඔක්කොම verify කරලා). **දැන් ඉතුරු paper එක ලිවීම විතරයි.**
>
> ✅ **Tests 256ම pass** · GitHub එකේ · `paper/section5-results.md` **§5 ලියලා ඉවරයි**
> ⛔ **Code එකේ කිසිම අගයක් hard-code කරන්න එපා** — හැම එකක්ම `config.yaml` එකෙන්.

> 📓 **ඊට කලින්:** [**09-worklog.md**](09-worklog.md) කියවන්න — කලින් session එකේ **මොනවද කලේ,
> මොන තීරණ ගත්තද, ඇයි** කියලා ඒකේ තියෙනවා. **ඒක නොකියවා පටන් ගත්තොත් වැඩ නැවත කරන්න වෙනවා.**

---

## 1. මේ ෆෝල්ඩරයේ තියෙන්නේ මොනවද?

සති 13ක පර්යේෂණ ව්‍යාපෘතියක්, කාර්යයන් 70කට කඩලා — **සැලසුම සහ මේ දක්වා කරපු වැඩ**.

---

## 2. කියවන අනුපිළිවෙල

```
🔁 හැම session එකකදීම:
     1️⃣  09-worklog.md   ★★★   — කලින් වතාවේ මොකද කලේ? ඊළඟට මොකද?
     2️⃣  02-task-board.md  ★★  — කරන්න තියෙන වැඩ

🆕 මුල්ම වතාවට නම් විතරක්:
     3️⃣  ../README.md            — සමස්ත චිත්‍රය
     4️⃣  07-glossary.md          — වචන තේරුම්
     5️⃣  01-project-charter.md   — පදනම
```

---

## 3. ලේඛන 10 — කවදා මොකක් පාවිච්චි කරන්නද?

| ලේඛනය | කවදා | මොකද |
|---|---|---|
| **[09-worklog.md](09-worklog.md)** ★★★ | **හැම session එකකම මුලින්ම** | කරපු දේ + ගත්ත තීරණ + **ඊළඟට මොකද** |
| **[02-task-board.md](02-task-board.md)** ★ | **හැමදාම** | වැඩ ලැයිස්තුව. ඉවර වුණාම ✅ දාන්න |
| [01-project-charter.md](01-project-charter.md) | ✅ අවසන් | Use case, objectives, RQs |
| [03-literature-review.md](03-literature-review.md) | සති 2–3 | Comparison table, gap statement |
| **[08-competitor-destouet.md](08-competitor-destouet.md)** ★ | Phase 2, 8 | ළඟම තරඟකරුවා + **§III එකට ready-to-paste ඡේදය** |
| **[04-framework-design.md](04-framework-design.md)** ★ | 🔒 **FROZEN** | Architecture, සමීකරණ, constraints — **structure වෙනස් කරන්න එපා** |
| [05-experiment-plan.md](05-experiment-plan.md) | ★ | Datasets, baselines, KPIs, statistics |
| **[10-data-card.md](10-data-card.md)** | Phase 4, 8 | මොන දත්තද, කොහෙන්ද, **license** එක · ⚠️ D1 synthetic බව |
| **[13-reference-verification.md](13-reference-verification.md)** 🆕 | **Submit කරන්න කලින්** | references 33 verify කළ ප්‍රතිඵල · ⚠️ [20] Sgarbossa pages ඉතුරු |
| **[12-paper-blueprint.md](12-paper-blueprint.md)** ★★★ | **Phase 8 — මුලින්ම මේක** | **පත්‍රිකාවට ඕන හැම දෙයක්ම.** Framework එකේ අන්තර්ගතය · කොටස් අනුව blueprint · සාක්ෂි · H1/H2 · ලියන්න බැරි දේ 16 |
| **[11-design-deviations.md](11-design-deviations.md)** ★ | **Phase 8** | ⚠️ **Design එකෙන් අයිනට ගිය තැන් 9** — §VI එකට අනිවාර්ය |
| **`../src/config.yaml`** ★★ | **හැම දාම** | **Parameters සියල්ල.** Code එකේ අගයක් hard-code කරන්න එපා |
| [06-paper-outline.md](06-paper-outline.md) | සති 12–13 | Paper එක ලියන හැටි |
| [07-glossary.md](07-glossary.md) | ඕනෑම වෙලාවක | තේරෙන්නේ නැති වචන |
| [`../literature/`](../literature/) | ඕනෑම වෙලාවක | බාගත් papers 5 (open access PDF) |

---

## 4. `[...]` කියන්නේ මොකද?

ලේඛනවල `[...]` දකිනවා නම් — **ඒක ඔබ පුරවන්න ඕන තැනක්**.

උදාහරණයක්:
```
| Machine ගණන | [5] |          ← ඔබේ අගය දාන්න
| Citation    | [...] |        ← paper එකේ නම දාන්න
```

---

## 5. සලකුණු තේරුම

| සලකුණ | අර්ථය |
|---|---|
| ⬜ 🟨 ✅ | නොකළ / කරමින් / අවසන් |
| 🚪 **GATE** | මේක ඉවර නොකර ඊළඟ අදියරට **යන්න එපා** |
| ★ | ඉතා වැදගත් — වැඩිපුර වෙලාව දෙන්න |
| ⚠️ | අනතුරු ඇඟවීම — මේක වැරදුනොත් ප්‍රශ්නයක් |
| 💡 | ප්‍රයෝජනවත් උපදෙසක් |

---

## 6. GATE 5ක් — මේවා පසුකරන්නම ඕන

| GATE | Task | මොකක්ද | තත්ත්වය |
|---|---|---|---|
| 🚪 1 | T1.6 | Charter එකට supervisor අනුමැතිය | ✅ **2026-08-03** |
| 🚪 2 | T2.6 | **Gap statement** — සංඛ්‍යා සමඟ | ✅ v2 ලියා ඇත |
| 🚪 3 | T3.8 | **Design freeze** | ✅ **2026-08-04** |
| 🚪 4 | T5.15 | **Tests pass** — code එක හරියට වැඩ කරනවා | ✅ **2026-08-06 · 256 pass** |
| 🚪 5 | T8.15 | **Submit** 🎉 | ⬜ |

> ⚠️ **Supervisor sign-off ගැන:** topic එක supervisor විසින්ම පවරන ලද බැවින්, වෙනම ලිඛිත අනුමැතියක්
> **blocker එකක් ලෙස නොසලකයි**. Supervisor ව හමුවනකොට design §14 checklist එක පෙන්නන්න.

---

## 7. ව්‍යාපෘතියේ අවදානම් 3 (දැනගෙන ඉන්න)

| අවදානම | වළක්වා ගන්නේ කොහොමද |
|---|---|
| **Scope creep** — වැඩේ ලොකු වෙලා ඉවර වෙන්නේ නෑ | Charter §2 හි "බැහැර" ලැයිස්තුව අනුගමනය කරන්න. අලුත් අදහසක් ආවොත් → future work. |
| **Human Twin එක conceptual විතරක් වීම** | T3.3 සහ T5.7 වලට වැඩිපුර වෙලාව දෙන්න. **සංඛ්‍යා** තියෙන්නම ඕන. |
| **B2 (Industry 4.0) baseline එක නොකිරීම** | T6.2 අත්හරින්න එපා. ඒක නැත්නම් paper එකේ අගයක් නෑ. |

---

## 8. දැන් කරන්න ඕන දේ 👇

```
┌────────────────────────────────────────────────────────────┐
│  1️⃣  09-worklog.md · Session 11 කියවන්න   ← ★★★ මුලින්ම    │
│      Phase 7 එකේ මොකද හම්බුණේ, මොනවා ලියන්න බැරිද          │
│                                                            │
│  2️⃣  paper/section5-results.md කියවන්න                     │
│      §V ලියලා ඉවරයි — §A headline · §E trade-off කතාව      │
│      ⚠️ අගදී "ලියන්න බැරි දේ" ලැයිස්තුව බලන්න               │
│                                                            │
│  3️⃣  ★★★ 12-paper-blueprint.md කියවන්න                     │
│      පත්‍රිකාවට ඕන හැම දෙයක්ම එකතැනක                        │
│                                                            │
│  4️⃣  T8.1 template → T8.2 §3 Proposed Framework            │
│      ⛔ ඊට කලින්: [CHECK] 5 + charter §2/§3 (blueprint §F.1)│
└────────────────────────────────────────────────────────────┘
```

> ⚠️ **Paper එකේ ලියන්න බැරි දේ 11ක්** — සම්පූර්ණ ලැයිස්තුව
> [`paper/section5-results.md`](../paper/section5-results.md) අගදී. ප්‍රධාන ඒවා:
> weights steer කරනවා කියන්න එපා · coupling 5ම බලපානවා කියන්න එපා ·
> quality/OEE වැඩි වුණා කියන්න එපා · **"Pareto front" කියන්න එපා** ·
> workload ප්‍රතිඵලය අත්හරින්න එපා.

> ⚠️ **§VI Limitations එකට අනිවාර්ය 8ක්** → [11-design-deviations.md](11-design-deviations.md) §4.
> ප්‍රධාන ඒවා: λ, μ calibrated · β₂, β₃ fit කරන්න බැරි · deferral 15% guard ඉක්මවනවා ·
> **NSGA-II, L5 explainability, ML models තුනම කැපුවා**.

> ✅ **`[N]` විසඳා ඇත (2026-08-06):** **46** studies (2018–2026) · screened **51** ·
> ඇගයූ **31** · full-text **9** · තුනම ✅ = **0**. Gap statement සහ Related Work
> දෙකේම පුරවා ඇත. ⚠️ Othman et al. (*JIEM*) හි වර්ෂය 2018+ නම් → **47**.

---

## 9. ⛔ Design FROZEN — වෙනස් කරන්න බැරි දේ

> GATE 3 පසු වී ඇත (2026-08-04). **STRUCTURE එක freeze — PARAMETER VALUES නෙවෙයි.**

| ⛔ බැරි | ✅ පුළුවන් (`config.yaml`) |
|---|---|
| Twin state variables · CP1–CP5 | λ, μ · EF · weights w₁…w₅ |
| Objective ව්‍යුහය · HC1–HC4 | HC threshold අගය · β, γ, ψ · skill matrix |
| Fatigue model ආකෘතිය · Normalization | |

**Parameter** වෙනස් → experiments නැවත run. **Structure** වෙනස් → **code + experiments දෙකම** නැවත.

---

**සුබ පැතුම්! 🚀**
