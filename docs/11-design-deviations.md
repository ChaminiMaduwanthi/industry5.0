# 📐 Design Deviations Register

> **හදපු දිනය: 2026-08-06** · GATE 3 (2026-08-04) හි freeze කරපු design එකට **සාපේක්ෂව**.
>
> **ඇයි මේක ඕන:** design එක **freeze** කරලා තියෙන්නේ. Implementation එක ඒකෙන් අයිනට ගිය
> හැම තැනක්ම **ලේඛනගත වෙන්නම ඕන** — නැත්නම් "frozen" කියන එකට තේරුමක් නෑ.
> Supervisor සහ reviewers අහන පළමු ප්‍රශ්නය: *"ලිව්වේ එකක්, කළේ තව එකක් නේද?"*
>
> ⚠️ **මේ ලේඛනයේ ඇති හැම පේළියක්ම §VI Limitations එකට හෝ §IV Implementation එකට යා යුතුයි.**

---

## §1 · සාරාංශය

| # | Design | දේ | වර්ගය | Paper එකට බලපෑම |
|---|---|---|---|---|
| **D1** | §6 | Normalization calibration protocol **ක්‍රියාත්මක නෑ** | අවශ්‍ය නොවීය | §IV එකේ පැහැදිලි කරන්න |
| **D2** | §7.1 | Objective එක **epoch එකකට marginal** ලෙස, shift policy එකකට නොවේ | ක්‍රියාත්මක අවශ්‍යතාව | §IV |
| **D3** | §7.2 | **NSGA-II / B3b ලියලා නෑ** | ⚠️ **විෂය පථයෙන් කැපුවා** | ⛔ **§VI අනිවාර්ය** |
| **D4** | §10, §1 | **L5 Explainability (SHAP) + dashboard ලියලා නෑ** | ⚠️ **විෂය පථයෙන් කැපුවා** | ⛔ **§VI අනිවාර්ය** |
| **D5** | §3.1 | **XGBoost RUL/energy/quality models ලියලා නෑ** | ⚠️ **විෂය පථයෙන් කැපුවා** | ⛔ **§VI අනිවාර්ය** |
| **D6** | §3.3 | β₂, β₃ **calibrated**, fit කරලා නෑ | දත්ත සීමාවක් | ⛔ **§VI අනිවාර්ය** |
| **D7** | §4.8 | Cognitive load **ගණනය කරනවා, තීරණයට ගන්නේ නෑ** | design එකට අනුකූලයි | §V.E.3 හි ලියා ඇත |
| **D8** | §4.7 | `v̂` **fleet efficiency පරාසය** මත normalize | අර්ථකථනයක් | §IV |
| **D9** | — | `maintenance_minutes`, `breakdown_repair_minutes` | design එකේ **නොතිබූ** parameters | §IV |

> ✅ **වෙනස් නොවුණු දේ:** frozen parameters **32ම** (`κ_τ`, RULA base, `c_τ`, `ψ`, `γ`, HC1–HC4,
> hysteresis, weight scenarios 4, EF, λ, μ) config එකේ **හරියටම design අගයමයි** — 2026-08-06 දින
> ස්වයංක්‍රීයව පරීක්ෂා කර ඇත. §3.1, §3.2, §3.3, §3.4, §4.1, §4.4, §4.7, §4.8 **සමීකරණ code එකේ
> අකුරින් අකුරට** ක්‍රියාත්මකයි.

---

## §2 · විස්තර

### D1 · §6 Normalization calibration — **අවශ්‍ය නොවීය**

**Design කිව්වේ:** B1 runs (seeds 100–129) වලින් P5/P95 ගෙන `Ê`, `Ŵ`, `T̂` normalize කරන්න;
evaluation seeds 0–29 වෙනම තියන්න (leakage වළක්වන්න).

**කළේ:** ඒ calibration එක **කවදාවත් run කළේ නෑ**. `config.yaml → normalization.bounds` තාමත් `null`.

**ඇයි ඒක ප්‍රශ්නයක් නොවේ — හේතු 2:**
1. **Decision layer එකට ඕන නෑ.** `weighted.py` හි හැම පදයක්ම **ව්‍යුහයෙන්ම [0,1]** —
   `F̂` දැනටමත් normalized (§4.4), `(RULA−1)/6`, `Q` යනු සම්භාවිතාවක්, energy සහ time
   ඒ epoch එකේ **උපරිමයෙන්** බෙදනවා. Fitted bound එකක් ඕන නෑ.
2. **වාර්තා කිරීමට ඕන නෑ.** Table II හි තියෙන්නේ **ස්වාභාවික ඒකක** (kWh, units, RULA 1–7) —
   normalize කරන දෙයක් නෑ.

> ★ **ඇත්තටම මේක §6 හි අරමුණට වඩා ශක්තිමත්:** §6 හි බය leakage එක.
> **කිසිම දෙයක් fit නොකිරීමෙන්** ඒ අවදානම **සම්පූර්ණයෙන්ම** නැති වෙනවා.
> ⚠️ B1 මත fit කරපු bound එකක් decision එකට දුන්නා නම් **ඒක චක්‍රීය (circular)** වෙනවා.

**➜ ක්‍රියාව:** `config.yaml` හි dead entries **ඉවත් කළා** (2026-08-06), මේ ලේඛනයට pointer එකක් සමඟ.
§IV එකේ ලියන්න: *"All objective terms are bounded on [0,1] by construction, so no calibration
run is required and no evaluation data enters the decision rule."*

---

### D2 · §7.1 Objective — **epoch marginal**

**Design කිව්වේ:** `Z(π) = w₁F̂ + w₂R̂ + w₃Ê + w₄Ŵ − w₅T̂` — **shift policy π එකකට**.

**කළේ:** decision epoch එකකට **මුළු shift එකක් ඇගයීමට බෑ**. ඒ නිසා එක් assignment
එකක **marginal දායකත්වය** ඒ පද 5න්ම ලකුණු කරලා, epoch එක හොඳම එක ගන්නවා.
Throughput එක **ප්‍රතිලෝමව** (කෙටි කාලය = අඩු පිරිවැය) — design හි ලකුණු සම්මුතිය රැකෙනවා.

**➜ §IV එකේ ලියන්න.** මේක ව්‍යුහාත්මක වෙනසක් නොවේ, **greedy epoch-wise ක්‍රියාත්මක කිරීමකි**.

---

### D3 · §7.2 NSGA-II (B3b) — ⚠️ **කැපුවා**

**Design කිව්වේ:** objectives 3ක් (People/Planet/Profit) NSGA-II එකෙන්, Pareto front එක 3-D.

**කළේ:** **B3a (weighted sum) පමණයි.** T5.12 ක්‍රියාත්මක කළේ නෑ.

**ප්‍රතිවිපාක — වැදගත්:**
```
⛔ "Pareto front" කියලා ලියන්න බෑ           ← multi-objective search එකක් run කරලා නෑ
✅ Fig 3 = "constraint sweep"                ← HC1 0.70/0.80/0.90
⛔ charter §6 හි "Pareto front figure" නිර්ණායකය  → සපුරන්නේ නෑ (නිවැරදි කර ඇත)
⛔ paper-outline §V-B හි "Fig 3 (Pareto front)"   → නිවැරදි කර ඇත
```

> 💡 **හොඳ ආරංචිය:** weight sensitivity එකෙන් පෙනුණේ **weights 4ම එකයි** කියලා (§V.E.1) —
> ඒ කියන්නේ **objective එකේ weight අවකාශය දිගේ front එකක් ඇදලා වැඩක් නෑ**. Constraint sweep
> එක **වඩාත් තොරතුරු දායකයි**. ➜ මේක §VI එකේ *"future work"* ලෙස නොව, **තර්කයක් සමඟ** ලියන්න.

---

### D4 · §10 + §1 L5 Explainability & dashboard — ⚠️ **කැපුවා**

**Design කිව්වේ:** Layer 5 = SHAP explanations + operator override interface.
**Fig 1 architecture diagram එකේ layer 5ම තියෙනවා.**

**කළේ:** T5.13 (SHAP) සහ T5.14 (Streamlit dashboard) **ලියලා නෑ**.

> ⛔⛔ **මේක වඩාත්ම පරිස්සමින් ලියන්න ඕන එක.** Fig 1 එකේ L5 පේනවා. Paper එකේ
> *"our five-layer architecture"* කියලා ලියලා ඒක **ලියලා නෑ** නම් — ඒක **reviewer කෙනෙක්
> අල්ලන ආකාරයේ අසත්‍යයක්**.
>
> ✅ **ලියන්න:** *"The explainability and operator-override layer is specified in the
> architecture (Fig. 1, L5) but is not implemented in this study; the results reported here
> come from layers L1–L4."*
>
> 💡 `factory.py` හි `on_epoch` hook එක **දැනටමත් තියෙනවා** — dashboard එකට පදනම ඇත.

---

### D5 · §3.1 XGBoost models — ⚠️ **කැපුවා**

**Design කිව්වේ:** *"XGBoost RUL model එකේ කාර්යය: sensor window එකෙන් `L_m⁰` ඇස්තමේන්තු කිරීම (T5.5)"*.

**කළේ:** `L⁰ = 216 min` එක **D1 හි TWF බෙදාහැරීමෙන් සෘජුව** ගත්තා (T4.2). ML model එකක් නෑ.
එසේම energy සහ quality models — regression/calibration, XGBoost නොවේ.

**➜ §VI එකේ ලියන්න:** machine twin එක **සමීකරණ මත, දත්තවලින් ලබාගත් parameters සමඟ** —
learned predictor එකක් නොවේ. ⚠️ *"AI-driven digital twin"* කියලා ලියන්න එපා.

> 💡 මේක **novelty එකට බලපාන්නේ නෑ** — novelty කරුණු 2 ① twin layer ② fatigue = dynamic state.
> ML යනු Destouet ලාත් කරන දෙයක් (08-competitor §…), ඒ නිසා **වෙනසක් නොවේ**.

---

### D6 · §3.3 β₂, β₃ — **calibrated, fit කරලා නෑ**

SECOM හි operator attributes **නෑ**, ඒ නිසා skill→quality සහ fatigue→quality සංගුණක
**කිසිම dataset එකකින් fit කරන්න බෑ**. λ, μ වගේම `[CALIB]`.

**ආවරණය:** T7.8 ablation එකෙන් — ඒ දෙකෙන් **තීරණයක් වෙනස් වෙන්නේ නෑ** කියලා පෙන්නලා
(§V.E.3). ➜ ඒ නිසා ඒවායේ අගය මත **නිගමන රඳා පවතින්නේ නෑ**.

**➜ §VI අනිවාර්ය.** විස්තර: [10-data-card.md](10-data-card.md) §3.

---

### D7 · §4.8 Cognitive load — ගණනය කරනවා, **තීරණයට ගන්නේ නෑ**

§7.1 objective එකේ cognitive පදයක් නෑ; §9 filter එකේත් නෑ. ➜ **design එකට අනුකූලයි.**
ඒත් T7.8 ablation එකේදී *"CP3 ablate කරන්න බෑ"* කියලා කියන්න වුණේ මේ නිසා.
**§V.E.3 හි ලියා ඇත.**

---

### D8 · §4.7 `v̂` normalization — **අර්ථකථනයක්**

Design කිව්වේ *"`v̂_m` = normalized machine speed"* — **කොහොමද normalize කරන්නේ කියලා කියලා නෑ**.
කළේ: **fleet එකේම efficiency පරාසය** මත (`(eff − min)/(max − min)`).
➜ අත්තනෝමතික නියතයක් ඇතුළු වෙන්නේ නෑ; scale එක **fleet එකෙන්ම** එනවා.

---

### D9 · Design එකේ **නොතිබූ** parameters 2

| Parameter | අගය | ඇයි |
|---|---|---|
| `maintenance_minutes` | **15** | `L⁰` එන්නේ tool wear එකෙන් ➜ maintenance = **tool change**. 45 නම් machine පැත්ත shift එක යටපත් කරනවා |
| `breakdown_repair_minutes` | **90** | S3 හි **unplanned breakdown** එකක් tool change එකක් නොවේ. මේක නැතුව S3 හි "breakdown" එකක් machine එකක් **පූර්ණ සෞඛ්‍යයෙන්** ආපසු දෙනවා — ඒක **ත්‍යාගයක්**, බාධාවක් නොවේ |

**➜ §IV එකේ ලියන්න** (simulation parameters table එකේ).

---

## §3 · ⛔ මේ deviations නිසා පත්‍රිකාවේ **ලියන්න බැරි** දේ

```
✗ "Pareto front" / "Pareto-optimal solutions"      → D3, NSGA-II run කරලා නෑ
✗ "our five-layer architecture" (ලියපු එකක් ලෙස)    → D4, L5 ලියලා නෑ
✗ "SHAP explanations" / "operator override"        → D4
✗ "AI-driven / ML-based digital twin"              → D5, XGBoost නෑ
✗ "coefficients fitted to SECOM"                   → D6, β2/β3 calibrated
```

**මේ ලැයිස්තුව `paper/section5-results.md` අගදී ඇති එකට එකතු වේ** (එතන 11ක් තියෙනවා).

---

## §4 · ⚠️ §VI Limitations එකට යා යුතු දේ — **සම්පූර්ණ ලැයිස්තුව**

```
1. λ, μ            calibrated rather than measured  (design §4.5)
2. β2, β3          කිසිම dataset එකකින් fit කරන්න බැරි  (D6)
3. Deferral rate   15% guard එක ඉක්මවනවා (S1 24%, S3 19%) + හේතුව  (T5.16)
4. NSGA-II         ලියලා නෑ — weighted sum පමණයි  (D3)
5. L5              explainability + override ලියලා නෑ  (D4)
6. ML models       ලියලා නෑ; parameters දත්තවලින් සෘජුව  (D5)
7. D1 (AI4I)       synthetic dataset එකක්  (data card §2)
8. Operators 3     synthetic; physiological data එකතු කරලා නෑ
```
