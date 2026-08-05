# 📄 Data Card (T4.7)

> **අවසන් යාවත්කාලීනය: 2026-08-05** · බාගත් දිනය: **2026-08-05**
> මේ ලේඛනයේ අරමුණ: *"මොන දත්තද, කොහෙන්ද, **පාවිච්චි කරන්න අවසර තිබුණාද**, මොකටද පාවිච්චි කලේ"*
> කියන ප්‍රශ්න 4ට උත්තර. Reviewers සහ ethics committee අහන්නේ මේවා.

---

## §1 · සාරාංශය

| ID | Dataset | ප්‍රමාණය | License | තත්ත්වය | මොකටද |
|---|---|---|---|---|---|
| **D1** | AI4I 2020 Predictive Maintenance | 10,000 × 14 | **CC BY 4.0** | ✅ භාවිතා කළා | `L0` — machine ආයුෂ |
| **D2** | NASA C-MAPSS (Turbofan) | 13 files | **Public domain** (US Gov) | 🟡 බාගත්තා, භාවිතා නෑ | RUL model (Phase 5, optional) |
| **D3** | Steel Industry Energy Consumption | 35,040 × 11 | **CC BY 4.0** | ✅ භාවිතා කළා | `e_idle`, `Δe(τ)` — බලශක්තිය |
| **D4** | SECOM | 1,567 × 591 | **CC BY 4.0** | ✅ භාවිතා කළා | defect rate — `β₀` anchor |
| **D5** | WESAD | — | Academic-use | ⛔ **භාවිතා නොකළා** | ↓ §5 බලන්න |

> ✅ **හැම license එකක්ම 2026-08-05 දින UCI dataset පිටුවෙන් සෘජුව තහවුරු කර ඇත** —
> memory එකෙන් හෝ උපකල්පනයෙන් නොවේ. තුනම `Creative Commons Attribution 4.0 International`.
> ➜ **Attribution දුන්නොත් පර්යේෂණයට සහ ප්‍රකාශනයට නිදහසේ භාවිතා කළ හැක.**

---

## §2 · ⚠️ පාඨකයාට **අනිවාර්යයෙන්** කිව යුතු කරුණක්

```
D1 (AI4I 2020) = SYNTHETIC dataset එකක්
```

UCI විස්තරයේම මෙසේ තියෙනවා:

> *"The AI4I 2020 Predictive Maintenance Dataset is a **synthetic dataset** that reflects real predictive maintenance data encountered in industry."*

**මේකෙන් අදහස් වෙන්නේ:**

| | |
|---|---|
| ✅ ඒක **පිළිගත් public benchmark** එකක් — papers සිය ගණනක් පාවිච්චි කරලා | භාවිතයට කිසි ප්‍රශ්නයක් නෑ |
| ⛔ ඒත් ඒක **මිනුම් ලොගයක් නොවේ** | *"real-world data"* කියලා ලියන්න බෑ |

> ⚠️ **`05-experiment-plan.md` §2 හි ඇති ඡේදය නිවැරදි කරන්න:**
>
> ❌ *"were driven by three **real-world** benchmark datasets"*
> ✅ *"were driven by three **public benchmark** datasets, one synthetic (D1) and two derived from operational measurements (D3, D4)"*

**D3 සහ D4 ඇත්ත මිනුම්:** D3 = දකුණු කොරියාවේ ඇත්ත වානේ කර්මාන්තශාලාවක්; D4 = ඇත්ත semiconductor නිෂ්පාදන පෙළක්.

---

## §3 · විස්තරාත්මක කාඩ්පත්

### 🔧 D1 · AI4I 2020 Predictive Maintenance Dataset

| Field | අගය |
|---|---|
| සම්පූර්ණ නම | AI4I 2020 Predictive Maintenance Dataset |
| ප්‍රභවය | UCI ML Repository, dataset **601** |
| URL | `https://archive.ics.uci.edu/dataset/601/` |
| **License** | **CC BY 4.0** *(2026-08-05 දින තහවුරු කළා)* |
| නිර්මාපක | S. Matzka (2020) |
| ස්වභාවය | ⚠️ **Synthetic** — ඇත්ත milling machine දත්තවල සංඛ්‍යානය අනුකරණය කරයි |
| Rows × Cols | 10,000 × 14 |
| **Missing values** | **0** — කිසිවක් නෑ ✅ |
| පාවිච්චි කළ features | `Tool wear [min]`, `Machine failure`, `TWF`, `HDF`, `PWF`, `OSF`, `RNF` |
| Preprocessing | කිසිවක් ඕන වුණේ නෑ (missing නෑ, cleaning අනවශ්‍යයි) |
| **එළියට ගත්ත parameter** | `L0 = 216 busy-minutes` (TWF සිදුවීම්වල මධ්‍යන්‍ය tool wear) |
| Design සම්බන්ධය | §3.1 — `H(t+dt) = H − dt·κ_τ/L0` |
| BibTeX key | `matzka2020ai4i` |

> **ඇයි TWF විතරක්?** Failure mode 5 න් **TWF (tool wear failure) විතරයි** සෘජුවම
> සමුච්චිත ගෙවීමේ ශ්‍රිතයක්. අනිත් ඒවා (තාපය, බලය, අධික බර) වෙනස් යාන්ත්‍රණ —
> ඒවා ගෙවීම මත පදනම් ආයුෂ ඇස්තමේන්තුවකට වලංගු නෑ.

---

### ⚡ D3 · Steel Industry Energy Consumption

| Field | අගය |
|---|---|
| සම්පූර්ණ නම | Steel Industry Energy Consumption |
| ප්‍රභවය | UCI ML Repository, dataset **851** |
| URL | `https://archive.ics.uci.edu/dataset/851/` |
| **License** | **CC BY 4.0** *(2026-08-05 දින තහවුරු කළා)* |
| නිර්මාපක | Sathishkumar V E, Changsun Shin, Yongyun Cho (2021) |
| ස්වභාවය | ✅ **ඇත්ත මිනුම්** — දකුණු කොරියාවේ කුඩා පරිමාණ වානේ කර්මාන්තශාලාවක් |
| Rows × Cols | 35,040 × 11 *(= දින 365 × දිනකට 96)* |
| **නියැදි පරතරය** | ★ **විනාඩි 15** — අපේ decision epoch එකට **හරියටම සමානයි** |
| **Missing values** | **0** ✅ |
| පාවිච්චි කළ features | `Usage_kWh`, `Load_Type` |
| Preprocessing | `Load_Type` → task type: `Light_Load→L`, `Medium_Load→M`, `Maximum_Load→H` |
| **එළියට ගත්ත parameters** | `e_idle = 2.66 kWh/15min` (Light_Load හි P5) · `Δe = 5.97 / 35.79 / 56.61` (L/M/H) |
| Design සම්බන්ධය | §3.2 — `E(t) = e_idle + 1[busy]·Δe(τ)` |
| BibTeX key | `sathishkumar2021steel` |

> ★ **වාසනාවන්ත ගැලපීම් 2:** ① `Load_Type` හි කාණ්ඩ 3ම අපේ task types 3 ට map වෙනවා
> ② නියැදි පරතරය (15 min) අපේ decision epoch එකට සමානයි ➜ පේළියක් = epoch එකක්.
>
> ⚠️ **නිරපේක්ෂ අගය නොව, අනුපාතය පමණක් ගෙන ඇත.** වානේ කම්හලක් අපේ කල්පිත factory එකට වඩා
> විශාලයි. `config.yaml → machines.energy_rescale_to_kwh_per_hour` මගින් scale කරයි.
> B1/B2/B3 තුනටම එකම scale එක ➜ **සංසන්දනය බලපෑමකට ලක් නොවේ**.
>
> ⚠️ **Light_Load skewed** (mean/median = 2.6). **Mean** පාවිච්චි කළා — බලශක්තිය **එකතු වන** රාශියක්
> නිසා shift එකක මුළු kWh එක අපේක්ෂිත අගයන්ගේ එකතුවයි; median ගත්තොත් CO₂e **අඩුවෙන් ගණන් වෙනවා**.

---

### 🔍 D4 · SECOM

| Field | අගය |
|---|---|
| සම්පූර්ණ නම | SECOM (semiconductor manufacturing) |
| ප්‍රභවය | UCI ML Repository, dataset **179** |
| URL | `https://archive.ics.uci.edu/dataset/179/` |
| **License** | **CC BY 4.0** *(2026-08-05 දින තහවුරු කළා)* |
| නිර්මාපක | Michael McCann, Adrian Johnston (2008) |
| ස්වභාවය | ✅ **ඇත්ත මිනුම්** — semiconductor නිෂ්පාදන පෙළක sensor දත්ත |
| Rows × Cols | 1,567 × 591 |
| **Missing values** | **4.5%** — cells වලින් |
| Class balance | 93.4% pass / **6.6% fail** |
| **එළියට ගත්ත parameter** | Baseline defect rate **6.64%** → quality model එකේ `β₀` anchor |
| Design සම්බන්ධය | §3.3 — `Q = σ(β₀ + β₁(1−H) + β₂(1−S) + β₃F̂ + β₄κ)` |
| BibTeX key | `mccann2008secom` |

> ⚠️ **වැදගත් සීමාවක්:** SECOM හි features **නිර්නාමික sensor කියවීම්** — operator තොරතුරු **නෑ**.
> ඒ නිසා **`β₂` (skill) සහ `β₃` (fatigue) මේකෙන් fit කරන්න බෑ.** ඒවා design §3.3 හි පරිදිම,
> ධන ලකුණු සීමාව සමඟ තබා ඇත; ඒවායේ බලපෑම **T7.8 ablation** එකෙන් මනිනවා.
> ➜ මේක §VI Limitations එකේ ලියන්න.

---

### ✈️ D2 · NASA C-MAPSS *(බාගත්තා — තවම භාවිතා නෑ)*

| Field | අගය |
|---|---|
| සම්පූර්ණ නම | Turbofan Engine Degradation Simulation Data Set |
| ප්‍රභවය | NASA Prognostics Data Repository *(S3 mirror — `data.nasa.gov` බිඳී ඇත)* |
| URL | `https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip` |
| **License** | **Public domain** — එක්සත් ජනපද රජයේ කෘතියක් |
| නිර්මාපක | Saxena, Goebel, Simon & Eklund (2008) |
| තත්ත්වය | 🟡 Phase 5 හි RUL model එකට **optional** |

---

## §4 · ප්‍රතිනිෂ්පාදනය — දත්ත ආපහු ගන්නේ කොහොමද

```bash
# data/raw/ එකේ ඇති ලිපිගොනු git එකේ නෑ (ප්‍රමාණය + license). මෙසේ ආපහු ගන්න:
curl -L -o data/raw/ai4i2020.zip     "https://archive.ics.uci.edu/static/public/601/ai4i+2020+predictive+maintenance+dataset.zip"
curl -L -o data/raw/steel_energy.zip "https://archive.ics.uci.edu/static/public/851/steel+industry+energy+consumption.zip"
curl -L -o data/raw/secom.zip        "https://archive.ics.uci.edu/static/public/179/secom.zip"
curl -L -o data/raw/cmapss.zip       "https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip"

python src/eda.py               # → results/eda_summary.md + data/processed/eda_params.json
python src/build_processed.py   # → data/processed/*.csv
```

---

## §5 · ⛔ D5 (WESAD) භාවිතා **නොකළේ** ඇයි

**තීරණය: 2026-08-05 — භාවිතා නොකරයි.**

| හේතුව | විස්තරය |
|---|---|
| **1. අවශ්‍යතාවය නැති වුණා** | WESAD ඕන වුණේ `λ, μ` calibrate කරන්නයි. ඒවා දැන් **calibrated parameters** ලෙස ප්‍රකාශ කර, **T7.6b sensitivity analysis** (0.5× · 1× · 2×) මගින් ආවරණය කරයි. *(design §4.5)* |
| **2. ගැලපීම දුර්වලයි** | WESAD කියන්නේ රසායනාගාර **stress** corpus එකක් (EDA/ECG, විෂයන් 15). අපට ඕන **whole-body metabolic fatigue** — ඒක වෙනස් දෙයක්. දුර්වල fit එකක් **අවංක calibration ප්‍රකාශයකට වඩා පහසුවෙන් විවේචනය කළ හැක**. |
| **3. පිරිවැය** | 2.25 GB බාගැනීම + පැය 3ක වැඩක් — ඒ කාලය T7.6b එකට යෙදීම වඩා වටිනවා. |

> 💡 **පස්සේ ඕන නම්:** design §4.5 හි ක්‍රමය තියෙනවා. `config.yaml → fatigue.operator_specific: true`
> කරලා අගය දාන්න පුළුවන් — **design හෝ code වෙනස් වෙන්නේ නෑ.**

---

## §6 · Ethics සහ privacy (T8.12 එකට)

| ප්‍රශ්නය | උත්තරය |
|---|---|
| මිනිස් දත්ත එකතු කළාද? | **නෑ.** Operator 3 දෙනා **synthetic** — anthropometrics යනු design තේරීමක් *(design §4.2)* |
| පුද්ගලික දත්ත භාවිතා කළාද? | **නෑ.** භාවිතා කළ dataset 3ම **machine/process** දත්ත, පුද්ගලික දත්ත නොවේ |
| Ethics approval ඕනද? | **නෑ** — මිනිස් විෂයන් නෑ. *(පත්‍රිකාවේ පැහැදිලිව ලියන්න)* |
| License අනුකූලද? | ✅ **ඔව්** — CC BY 4.0 තුනක් + public domain එකක්; attribution `references.bib` හි |

> ⚠️ **පත්‍රිකාවේ ලියන්න:** *"No human subjects were involved. Operator profiles are
> synthetic and physiologically parameterised from published anthropometric equations."*
