# src/ — Code

> Phase 5 (T5.1 – T5.15) එකේදී මේවා ලියනවා. **දැන් තවම හිස්.**

## සැලසුම් කරගත් ව්‍යුහය

```
src/
├── config.yaml                  # සියලු parameters (hard-code කරන්න එපා)
├── twins/
│   ├── machine_twin.py          # T5.4  MachineTwin class
│   └── human_twin.py            # T5.7  HumanTwin class      ★ novelty
├── models/
│   ├── rul_model.py             # T5.5  Remaining useful life
│   ├── energy_model.py          # T5.5  බලශක්ති පුරෝකථනය
│   ├── quality_model.py         # T5.5  Defect risk
│   ├── sustainability.py        # T5.10 kWh/unit, CO₂e, scrap
│   └── human/
│       ├── fatigue_model.py     # T5.8  ★ literature-cited
│       ├── ergonomics.py        # T5.8  RULA scoring
│       └── cognitive_load.py    # T5.8
├── simulation/
│   ├── factory.py               # T5.3  SimPy discrete-event sim
│   ├── entities.py              # Machine, Operator, Task
│   └── coupling.py              # T5.9  CP1–CP5 twin coupling
├── decision/
│   ├── weighted.py              # T5.11 Weighted-sum optimiser (v1)
│   ├── nsga2.py                 # T5.12 NSGA-II optimiser (v2)
│   ├── constraints.py           # HC1–HC4, SC1–SC3
│   └── explain.py               # T5.13 SHAP explanations
├── baselines/
│   ├── b1_random.py             # T6.1  Random / round-robin
│   └── b2_industry40.py         # T6.2  ★ Industry 4.0 baseline
├── dashboard/
│   └── app.py                   # T5.14 Streamlit + override button
├── run_experiments.py           # T6.5  270 runs
└── analyse_results.py           # T7.1–T7.6
```

## ලිවීමේ අනුපිළිවෙල

```
T5.1 environment → T5.3 factory skeleton → T5.4 MachineTwin → T5.5 M-DT models
  → T5.7 HumanTwin ★ → T5.8 human models ★ → T5.9 coupling
  → T5.10 sustainability → T5.11 weighted optimiser → T5.12 NSGA-II
  → T5.13 SHAP → T5.14 dashboard → T5.15 tests
```

> 💡 **T5.11 (සරල weighted sum) මුලින්ම.** ඒක වැඩ කරනවා තහවුරු වුණාට පස්සේ T5.12 (NSGA-II) එකට යන්න.

## සැලසුම් කරගත් dependencies

```
simpy            # discrete-event simulation
pandas, numpy    # දත්ත
scikit-learn     # ML
xgboost          # RUL / energy / quality models
pymoo            # NSGA-II multi-objective optimisation
shap             # explainable AI
scipy            # statistical tests
matplotlib       # figures
streamlit        # dashboard
pyyaml           # config
pytest           # tests
```
