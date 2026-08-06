# 🚦 START HERE — මුලින්ම මේක කියවන්න

> **අවසන් යාවත්කාලීනය: 2026-08-05**

---

## ⚡ 0. දැන් තියෙන තැන — විනාඩි 1කින්

```
Phase 1  ████████████████████  ✅  6/6    🚪 GATE 1 පසුයි
Phase 2  ██████████████████░░  🟨  8/10   (papers කියවීම ඉතුරුයි — හදිසි නෑ)
Phase 3  ████████████████████  ✅  10/10  🚪 GATE 3 පසුයි — DESIGN FROZEN
Phase 4  ████████████████████  ✅  7/7    දත්ත සූදානම්
Phase 5  ████████████░░░░░░░░  🟨  10/16  (T5.5/5.6/5.12 කැපිය හැක · T5.13/5.14 ඉතුරු)
Phase 6  █████████████████░░░  🟨  6/7    ★ runs 270 ✅  ප්‍රතිඵල තියෙනවා
Phase 7  ███████████░░░░░░░░░  🟨  5/9    ← ★ දැන් මෙතන
Phase 8  ░░░░░░░░░░░░░░░░░░░░  ⬜  0/15   ← ලොකුම වැඩේ ඉතුරු
                                  ──────
                                  51/80
```

### 👉 කරන්න ඕන දේ: **T7.3 + T7.4 — Figures 2**

> 📊 **ප්‍රතිඵල දැනටමත් තියෙනවා** — `results/kpi_table.md`, `ablation.csv`,
> `sensitivity*.csv`, `crosstraining.csv`. **Plot කරන එක විතරයි ඉතුරු.**
> ඊට පස්සේ T7.7 (trade-off කතාව) → **Phase 8, paper එක**.
>
> ✅ **Tests 236ම pass** · commits 42 · GitHub එකේ · `paper/section5-results.md` draft ✅
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
| **[10-data-card.md](10-data-card.md)** 🆕 | Phase 4, 8 | මොන දත්තද, කොහෙන්ද, **license** එක · ⚠️ D1 synthetic බව |
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
| 🚪 4 | T5.15 | **Tests pass** — code එක හරියට වැඩ කරනවා | ⬜ |
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
│  1️⃣  09-worklog.md · Session 10 කියවන්න   ← ★★★ මුලින්ම    │
│      Phase 7 එකේ මොකද හම්බුණේ, මොනවා ලියන්න බැරිද          │
│                                                            │
│  2️⃣  results/kpi_table.md බලන්න                            │
│      ප්‍රධාන ප්‍රතිඵලය — B3 vs B2, KPI 11 × scenario 3      │
│                                                            │
│  3️⃣  T7.3 + T7.4 — figures 2ක් හදන්න                       │
│      → figures/fig3_tradeoff.png · fig4_comparison.png     │
│                                                            │
│  4️⃣  T7.7 — trade-off කතාව                                 │
│      (paper/section5-results.md එකේ අඩක් තියෙනවා)          │
└────────────────────────────────────────────────────────────┘
```

> ⚠️ **Paper එකේ ලියන්න බැරි දේ 4ක්** Session 10 අගදී ලැයිස්තුගත කර ඇත —
> weights steer කරනවා කියන්න එපා · CP1/CP2 බලපානවා කියන්න එපා ·
> quality/OEE වැඩි වුණා කියන්න එපා · workload ප්‍රතිඵලය අත්හරින්න එපා.

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
