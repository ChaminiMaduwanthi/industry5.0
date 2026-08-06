"""The text of the paper, kept apart from the document-construction code.

House rule for this file: no first-person pronouns. The article speaks about
itself and about the framework in the third person, which is the register the
target venue expects and which build_paper.py asserts before writing the file.
"""

TITLE = ("A Coupled Human–Machine Digital Twin Framework for "
         "Human-Centric and Sustainable Task Allocation in Industry 5.0")

AUTHOR_LINES = [
    "Chamini Maduwanthi",
    "[Department]",
    "[Institution]",
    "[City], Sri Lanka",
    "chaminimaduwanthi97@gmail.com",
]

ABSTRACT = (
    "This article presents a digital twin framework for production task allocation in which "
    "the state of the machine and the state of the operator are modelled together, and in which "
    "the physiological limits of the operator are enforced as hard constraints rather than as "
    "penalty terms. Industry 5.0 places human well-being alongside sustainability and "
    "productivity, yet digital twin research remains asset-centric: operators are represented by "
    "static profile attributes rather than by evolving physiological state, and the studies that "
    "do quantify operator state use it for monitoring rather than for allocation. Of 46 studies "
    "published between 2018 and 2026 reviewed for this work, none couples a quantified human "
    "twin, a machine twin and measured sustainability objectives within a single decision "
    "framework. The framework proposed here joins the two twins through five explicitly defined "
    "bidirectional coupling points. Operator fatigue evolves as an exponential function of "
    "metabolic demand, with per-operator bounds obtained from published anthropometric "
    "equations, so that protection differs between individuals without being prescribed. "
    "Evaluation uses a co-simulation of a five-machine, three-operator machining cell driven by "
    "three public benchmark datasets, over 270 runs spanning three allocation policies, three "
    "operating scenarios and thirty random seeds. Relative to an Industry 4.0 baseline under "
    "high demand, mean operator fatigue falls by 27.0% and energy per unit by 30.8%, all 79.5 "
    "constraint breaches per shift are eliminated, and the accompanying change in throughput of "
    "1.8% is not statistically significant."
)

KEYWORDS = ("Industry 5.0, human digital twin, sustainable manufacturing, "
            "multi-objective scheduling, human-centric design")

# =============================================================================
# I. INTRODUCTION
# =============================================================================
INTRO = [
    "The Industry 5.0 agenda of the European Commission sets human-centricity, sustainability "
    "and resilience alongside productivity as the goals of industrial transformation {breque2021industry50}. Where "
    "Industry 4.0 concentrated on digitalisation, connectivity and autonomy, Industry 5.0 asks "
    "what that capability is for, and answers that it must serve the operator and the "
    "environment as well as output {xu2021industry45}. Production scheduling sits directly on that question: "
    "every allocation of a task to a person and a machine distributes physical load, energy "
    "consumption and quality risk at the same moment {destouet2023survey}.",

    "Digital twin technology is the natural instrument for such decisions, because it maintains "
    "a live and computable representation of the system being scheduled. In practice that "
    "representation has remained asset-centric. Human digital twin frameworks model the operator "
    "through biographic attributes, capabilities and preferences rather than through "
    "physiological state; in one prominent framework, fatigue modelling and ergonomic assessment "
    "are identified by the authors themselves as remaining unaddressed {modoni2023hdt}. Others offer "
    "architectures without computable human parameters or experimental validation {toth2023i5arc}. Recent "
    "reviews confirm both the pattern and the terminological fragmentation that accompanies it "
    "{wang2023hdt}, {gaffinet2025hdtslr}.",

    "A complementary body of work does quantify operator state, but stops short of the decision. "
    "Biomechanical fatigue has been detected from joint-angle dynamics with considerable rigour, "
    "yet the resulting estimate serves monitoring only and never re-enters task allocation {sharotry2022fatigue}. "
    "Ergonomic indices computed inside a human digital twin inform manual decision support "
    "rather than automated optimisation {greco2020ergonomics}. Where operator fatigue does drive scheduling, no "
    "machine-side twin exists, so machine health, energy consumption and quality risk cannot "
    "participate in the allocation {tan2021fatigue}. The most closely related formulations optimise "
    "economic, ecological and social objectives together {destouet2024sustainable}, {destouet2026dynamic}, but represent the operator "
    "through static per-task multipliers: strain attaches to the operation rather than "
    "accumulating in the person, and recovery is a fixed allowance rather than a process.",

    "Of 46 studies published between 2018 and 2026 reviewed for this work — 31 assessed at "
    "abstract level or beyond, and the nine most closely related read in full — none "
    "couples a quantified human twin, a machine twin and measured sustainability objectives "
    "within a single decision framework. This article addresses that gap.",
]

CONTRIBUTIONS = [
    "A layered architecture that couples a machine digital twin to a human digital twin through "
    "five explicitly defined bidirectional coupling points, each realised as a named term in a "
    "state equation rather than as an abstract interface.",

    "A quantified human digital twin in which operator fatigue evolves as a physiological state, "
    "with per-operator resting expenditure and acceptable work level derived from published "
    "anthropometric equations, and in which fatigue, competence and ergonomic risk filter the "
    "candidate set before optimisation rather than entering the objective as penalties.",

    "Empirical evidence from a 270-run co-simulation showing that this reduces mean operator "
    "fatigue by 27.0% and energy per unit by 30.8% and removes every constraint breach, at no "
    "statistically detectable cost in throughput under high demand.",
]

INTRO_STRUCTURE = (
    "Section II reviews the relevant literature and positions the contribution. Section III "
    "presents the framework. Section IV describes the implementation and the experimental "
    "protocol. Section V reports and discusses the results. Sections VI and VII state the "
    "limitations and conclude."
)

# =============================================================================
# II. RELATED WORK
# =============================================================================
RELATED = [
    ("Industry 5.0 and Human-Centric Manufacturing", [
        "Industry 5.0 is defined by three pillars — human-centricity, sustainability and "
        "resilience — and is positioned as a values-driven complement to the "
        "technology-driven Industry 4.0 rather than as its successor {breque2021industry50}, {xu2021industry45}. Surveys of "
        "scheduling under this agenda confirm that human and environmental factors are entering "
        "formulations that were previously economic alone {destouet2023survey}. Architectural proposals for "
        "human-centric collaboration exist {toth2023i5arc}, but tend to remain conceptual, offering neither "
        "computable operator parameters nor experimental validation."]),

    ("Digital Twins in Manufacturing", [
        "The digital twin concept is well established for physical assets, spanning product "
        "design, manufacturing and service {tao2018dtdriven}, with recognised value in predictive maintenance "
        "and process optimisation {rasheed2020dt}. Twins of human–robot collaboration model the "
        "workspace and the interaction within it {malik2018hrcdt}, yet the human in that workspace is "
        "typically represented geometrically or kinematically rather than physiologically. The "
        "operator appears as a user of the twin, not as an entity the twin models."]),

    ("Human Digital Twins", [
        "Dedicated human digital twin research has grown quickly {wang2023hdt}, {gaffinet2025hdtslr}. The requirement that "
        "such applications carry a bidirectional flow of information, with data, models and "
        "simulations of machines as well as humans, has been stated explicitly {locklin2021hdt}, but that "
        "work presents an architecture without implementation, optimisation or sustainability "
        "objectives. Where operator state is quantified, the estimate is used for detection {sharotry2022fatigue} "
        "or for decision support {greco2020ergonomics} rather than for allocation. Assembly-oriented work that "
        "invokes sustainability observes the operator unidirectionally, through task duration, "
        "and reports no energy or carbon accounting {crnjac2025assembly}."]),

    ("Sustainable and Multi-Objective Scheduling", [
        "Fatigue-conscious scheduling has been formulated as a multi-objective problem and "
        "solved with evolutionary methods {tan2021fatigue}, {deb2002nsga2}, but without a machine-side twin the "
        "allocation cannot reason about equipment health, energy or defect risk. The closest "
        "formulations to the present work optimise the three sustainability pillars "
        "simultaneously, and extend to dynamic rescheduling under disruption and to carbon "
        "accounting {destouet2024sustainable}, {destouet2026dynamic}. Their treatment of the operator, however, is a static index "
        "attached to an operation–machine pair, with rest granted as a fixed proportion of "
        "working time. Strain therefore neither accumulates within a shift nor dissipates during "
        "rest, and the same worker is modelled identically at the start and at the end of the "
        "day."]),
]

TABLE1_HEADER = ["Study", "Machine twin", "Human state quantified",
                 "Drives decision", "Sustainability measured"]
TABLE1_ROWS = [
    ["Modoni and Sacco {modoni2023hdt}", "Yes", "No", "Partly", "No"],
    ["Tóth et al. {toth2023i5arc}", "No", "No", "No", "No"],
    ["Löcklin et al. {locklin2021hdt}", "Stated", "No", "No", "No"],
    ["Sharotry et al. {sharotry2022fatigue}", "No", "Yes", "No", "No"],
    ["Greco et al. {greco2020ergonomics}", "No", "Yes", "Partly", "No"],
    ["Crnjac Žižić et al. {crnjac2025assembly}", "Partly", "No", "Partly", "Rhetorical"],
    ["Tan et al. {tan2021fatigue}", "No", "Yes", "Yes", "No"],
    ["Destouet et al. {destouet2024sustainable}, {destouet2026dynamic}", "No", "Static index", "Yes", "Yes"],
    ["This article", "Yes", "Yes, dynamic", "Yes, as constraint", "Yes"],
]
TABLE1_NOTE = ("Partly denotes decision support without automated allocation. Static index "
               "denotes a per-task multiplier that neither accumulates nor recovers.")

RELATED_GAP = (
    "The pattern is a field divided in two. Studies that build twins represent the operator "
    "statically; studies that quantify the operator omit the twin; and environmental performance "
    "is co-optimised with human well-being in neither group. No reviewed study occupies the "
    "final row of Table I."
)

# =============================================================================
# III. PROPOSED FRAMEWORK
# =============================================================================
FW_SCOPE = (
    "The framework is developed for a machining cell in which arriving jobs must be assigned to "
    "an operator and a machine at each decision epoch. Five assumptions bound the model. First, "
    "operator fatigue follows a published exponential accumulation and recovery form {calzavara2019rest}, {sgarbossa2020ifac}. "
    "Second, competence is constant within a shift, so learning effects are excluded. Third, "
    "machine degradation follows the pattern of a benchmark maintenance dataset. Fourth, every "
    "operator begins the shift rested. Fifth, processing times are deterministic and "
    "sequence-dependent setup is excluded."
)

FW_ARCH = (
    "Fig. 1 shows the layered organisation. A physical layer emits machine and task events; a "
    "data layer time-aligns them into state vectors; a digital twin layer maintains the machine "
    "twin and the human twin and applies the couplings between them; and a decision layer "
    "filters candidate assignments against the human and machine constraints before optimising "
    "over whatever survives. A fifth layer, providing explanation and operator override, is "
    "specified in the architecture but is not implemented in this study; the results reported "
    "below come from the first four layers."
)

FIG1_CAPTION = ("Fig. 1. Layered organisation of the framework. The digital twin layer maintains "
                "both twins and the couplings between them; the decision layer filters before it "
                "optimises. The fifth layer is specified but not implemented in this study.")

FW_MDT = [
    "The machine twin carries health, energy rate, defect risk, availability and utilisation. "
    "Health falls in proportion to elapsed busy time and to the severity of the task being "
    "processed,",
    "where κ is the severity of task type τ and L⁰ the nominal life in busy "
    "minutes, estimated from tool-wear failures in a public maintenance dataset {matzka2020ai4i}. An idle "
    "machine does not degrade, and maintenance restores health. Energy is an idle draw plus a "
    "task-dependent increment, both estimated by load category from an industrial energy "
    "dataset {sathishkumar2021steel}; carbon is the product of energy and a national grid emission factor {ember2025electricity}. A "
    "machine is available while its health exceeds a floor and it is not under maintenance.",
]

FW_HDT = [
    "The human twin is the element that distinguishes this framework, and it is stated in "
    "physiological units rather than as an abstract index. Fatigue F is an energy expenditure "
    "rate in kcal per minute that relaxes exponentially towards whatever the current activity "
    "demands,",
    "where E* is the metabolic demand of the task while working and the resting expenditure "
    "while at rest, and ρ is the accumulation rate λ when demand exceeds the current "
    "state and the recovery rate μ otherwise {calzavara2019rest}, {sgarbossa2020ifac}. Task demand follows the metabolic "
    "classes of ISO 8996 {iso8996}. A light task therefore never exhausts an operator, because the "
    "asymptote towards which it drives fatigue is its own modest demand.",
    "Two per-operator constants make the model personal rather than generic. Resting expenditure "
    "follows the Mifflin–St Jeor equation {mifflin1990ree}, and the acceptable work level — the "
    "expenditure sustainable across a full shift — follows established relaxation-allowance "
    "and aerobic-capacity relations {price1990relaxation}, {silva2016age}. Normalised fatigue is the position between the "
    "two,",
    "so that a value of 0.80 means eighty per cent of that individual's own sustainable band "
    "rather than eighty per cent of an arbitrary scale. Because acceptable work level depends on "
    "age, sex and body mass, the three synthetic operators of the case study receive different "
    "protection without any rule prescribing it: for one of them the demand of a medium task "
    "already exceeds the sustainable level, so rest must be interleaved to keep that operator "
    "inside the band, while for another it does not.",
    "Ergonomic risk extends a posture score with the fatigue state and the pace of the assigned "
    "machine,",
    "with R₀ the baseline posture score for the task type {mcatamney1993rula}. Cognitive load is tracked on "
    "a task-load proxy {hart1988tlx} and reported, although it does not enter the allocation rule.",
]

FW_COUPLING = [
    "Five coupling points carry state between the twins, shown in Fig. 2. Competence and fatigue "
    "raise defect risk on the machine side; machine health raises cognitive load; task intensity "
    "sets the asymptote of the fatigue equation; and machine pace raises ergonomic risk. The "
    "first two enter the quality model, which is where the two twins meet most directly,",
    "with σ the logistic function, S the competence of the operator at the task, and "
    "β₂ and β₃ constrained positive. The intercept is anchored on the defect "
    "rate of a semiconductor process dataset {mccann2008secom}; because that dataset carries no operator "
    "attributes, β₂ and β₃ are calibrated rather than fitted, and their "
    "influence is quantified by ablation in Section V.",
]

FIG2_CAPTION = ("Fig. 2. The five coupling points. Each is a named term in a state equation, so "
                "a coupling can be disabled individually and its contribution measured.")

FW_OBJ = [
    "The allocation objective aggregates the three pillars over normalised terms,",
    "covering fatigue and ergonomic risk, energy and waste, and throughput. Four weightings are "
    "examined in Section V.",
    "Four constraints are enforced as filters applied before the objective is evaluated: "
    "normalised fatigue below 0.80, competence at or above a floor, ergonomic risk at or below "
    "an action level, and machine health above a floor. A hysteresis band holds an operator at "
    "rest until fatigue falls to 0.60, which prevents alternation across the threshold at "
    "successive epochs. When no admissible pairing exists, the work is left in the queue and the "
    "deferral is recorded rather than absorbed.",
    "The ordering is the substantive claim of the framework. The distinction between Industry "
    "4.0 and Industry 5.0 optimisation is, in this formulation, precisely the distinction "
    "between treating operator state as a soft penalty and treating it as a hard constraint. "
    "Under the former, a sufficient efficiency gain will always justify operator strain; under "
    "the latter, it never can.",
]

EQUATIONS = {
    "health": "H(t+Δt) = max(0, H(t) − Δt · κᵩ / L⁰)",
    "fatigue": "F(t+Δt) = E* + (F(t) − E*) exp(−ρ Δt)",
    "fhat": "F̂ = clip[ (F − Eᵣ) / (AWL − Eᵣ), 0, 1 ]",
    "rula": "R = clip[ R₀(τ) + ψ₁F̂ + ψ₂v̂, 1, 7 ]",
    "quality": ("Q = σ( β₀ + β₁(1−H) + β₂(1−S) "
                "+ β₃F̂ + β₄κᵩ )"),
    "objective": ("Z = w₁F̂ + w₂R̂ + w₃Ê + w₄Ŵ "
                  "− w₅Ť"),
}

# =============================================================================
# IV. IMPLEMENTATION
# =============================================================================
IMPL = [
    ("Co-Simulation Environment", [
        "No public dataset carries machine and operator state together, so a hybrid "
        "co-simulation is adopted. Machine-side dynamics are driven by public benchmark "
        "datasets, operator-side dynamics by the literature-derived models of Section III, and "
        "both advance on a single discrete-event clock implemented in SimPy. State is exchanged "
        "across the coupling points at every decision epoch. The modelled cell has five "
        "machines, three operators and three task types over an eight-hour shift divided into "
        "fifteen-minute epochs, with a scheduled break after four hours. Table II lists the "
        "parameters and their sources."]),

    ("Data and Parameter Estimation", [
        "Twin parameters are estimated directly from the benchmark data rather than learned. "
        "Nominal machine life comes from the tool-wear failures of the AI4I 2020 dataset {matzka2020ai4i}; "
        "idle and per-task energy draw from the load categories of an industrial steel energy "
        "dataset {sathishkumar2021steel}, whose fifteen-minute sampling interval coincides with the decision epoch; "
        "and the baseline defect rate from a semiconductor process dataset {mccann2008secom}. Only the ratios "
        "between load categories are carried into the simulation, with the absolute level "
        "rescaled to the modelled cell, so that the comparison between policies is unaffected by "
        "the scale of the source plant. The AI4I dataset is synthetic by construction, "
        "reproducing the statistics of industrial maintenance data rather than recording them; "
        "the other two are operational measurements."]),

    ("Allocation Policies", [
        "Three policies are compared. A random policy assigns admissible pairs without "
        "preference and serves as a sanity floor. An Industry 4.0 baseline retains the machine "
        "twin at full strength, including the machine-health constraint, and selects the fastest "
        "available pairing; the human twin continues to run and is reported, but does not enter "
        "the decision. The proposed policy adds the human constraints and the multi-objective "
        "score. The baseline is the same simulator under restriction rather than separate code, "
        "and the physical couplings remain active for it: a tired operator still produces more "
        "defects under the baseline, because that occurs in the cell whether or not the "
        "scheduler models it."]),

    ("Scenarios and Evaluation Protocol", [
        "Three scenarios are used: normal demand, high demand at 150% of nominal, and a "
        "disruption scenario in which two machines fail mid-shift. Each policy is run under each "
        "scenario with thirty random seeds, giving 270 runs in total; a seed fixes the order "
        "book and the disruption pattern, so the three policies face identical conditions. "
        "Comparisons use the Mann–Whitney U test with Cliff's delta as the effect size, "
        "Bonferroni-corrected across the eleven indicators reported per scenario. Rank tests are "
        "used throughout because thirty runs is not a large sample, several indicators are "
        "bounded, and one is identically zero under the proposed policy; normality is tested and "
        "reported but never relied upon. Re-running the full matrix reproduces every reported "
        "value."]),
]

TABLE2_HEADER = ["Parameter", "Value", "Source"]
TABLE2_ROWS = [
    ["Machines / operators / task types", "5 / 3 / 3", "Case definition"],
    ["Shift length, decision epoch", "480 min, 15 min", "Case definition"],
    ["Nominal machine life L⁰", "216 busy-min", "AI4I 2020 {matzka2020ai4i}"],
    ["Idle draw, task increment", "estimated by load class", "Steel energy {sathishkumar2021steel}"],
    ["Baseline defect rate", "6.6%", "SECOM {mccann2008secom}"],
    ["Grid emission factor", "0.33 kg CO₂/kWh", "Ember {ember2025electricity}"],
    ["Task metabolic demand", "2.58 / 4.26 / 5.94 kcal min⁻¹", "ISO 8996 {iso8996}"],
    ["Resting expenditure Eᵣ", "per operator", "Mifflin–St Jeor {mifflin1990ree}"],
    ["Acceptable work level", "per operator", "{price1990relaxation}, {silva2016age}"],
    ["Fatigue rates λ, μ", "0.020, 0.046 min⁻¹", "Calibrated; see §VI"],
    ["Fatigue limit, hysteresis", "0.80, release at 0.60", "Design choice"],
    ["Runs", "3 × 3 × 30 = 270", "Protocol"],
]

# =============================================================================
# V. RESULTS
# =============================================================================
RESULTS = [
    ("Overall Comparison", [
        "Table III reports the eleven indicators under high demand, the scenario in which "
        "demand exceeds what three operators can absorb comfortably and in which protecting "
        "them therefore has to cost something. Relative to the Industry 4.0 baseline, the "
        "proposed policy reduces mean operator fatigue by 27.0% and energy per unit by 30.8%, "
        "reduces mean ergonomic risk by 14.6%, and eliminates all 79.5 constraint breaches per "
        "shift that the baseline incurs. Each of these carries the maximum effect size at "
        "p < 0.001 after correction. The accompanying change in throughput is 1.8% and is not "
        "statistically significant (p = 0.148).",

        "That is the central finding. At the point where a throughput-driven scheduler pushes "
        "hardest, holding every operator inside their own sustainable band cost no measurable "
        "production. Fig. 4 shows the same comparison across the three pillars. Under normal and "
        "disrupted demand the picture is different and is reported as such: throughput falls by "
        "10.0% and 12.7% respectively, both significant. Those are not incidental losses but the "
        "throughput the framework declines to extract once an operator would pass their own "
        "limit, and the quantity is reported directly — work was deferred in 11.0% of "
        "decision epochs under high demand, and in 24.0% and 19.0% under the other two "
        "scenarios. A framework that never gave anything up would not be enforcing anything."]),

    ("The Efficiency–Well-Being Trade-Off", [
        "Fig. 3 traces the trade-off by sweeping the fatigue limit across 0.70, 0.80 and 0.90 "
        "rather than by re-weighting the objective. Peak fatigue tracks each limit from just "
        "below it and throughput rises monotonically with it, so the curve is a genuine frontier "
        "and the operating point is a choice along it rather than a fixed property of the "
        "method. The practical implication is that the dial which moves this system is the limit "
        "an organisation is willing to set on its people, not the priority it declares in an "
        "objective function."]),

    ("Robustness", [
        "Three parameters are calibrated rather than measured: the fatigue accumulation and "
        "recovery rates, and the fatigue limit expressed as a fraction of the acceptable work "
        "level. Each was varied and the comparison repeated. Scaling both rates by 0.5, 1 and 2 "
        "— a fourfold span — preserved the ordering of the two policies on every "
        "human-centric indicator. The advantage grew with the rate, from 25.4% to 27.0% to 33.1% "
        "less mean fatigue, and so did the cost, from 0.8% to 1.8% to 5.9% of throughput, which "
        "is the behaviour the model implies. Varying the limit across 0.70, 0.80 and 0.90 "
        "likewise preserved the ordering in all three scenarios. The conclusions therefore rest "
        "on the framework rather than on the values chosen for its free parameters."]),

    ("What Steers the Framework", [
        "The four weightings of the objective proved indistinguishable: mean fatigue spans 0.541 "
        "to 0.542 and throughput 90.2 to 90.3 units, across weightings that differ sevenfold on "
        "the human terms. The cause lies upstream of the objective. After the constraints filter "
        "the candidate set, 95.7% of the 45,754 decisions taken under high demand face either no "
        "admissible pairing or exactly one, so there is nothing left to weigh; among the "
        "remaining 4.3%, the best and worst admissible options differ by a median of 0.015 on "
        "the objective's own scale.",

        "This is a design property rather than a defect. A framework whose human protections "
        "could be tuned away by re-weighting an objective would not be offering protection. It "
        "also sharpens the relationship to Industry 4.0: the profit-weighted configuration does "
        "converge on the baseline's throughput, to within 1.8%, but it cannot converge on the "
        "baseline's fatigue or breach count, because driving every human weight to zero still "
        "leaves the fatigue limit, the competence floor and the ergonomic ceiling filtering "
        "before the objective is consulted. Industry 4.0 is the limit of the objective, not of "
        "the framework."]),

    ("Contribution of the Couplings", [
        "Each coupling was removed from the scheduler's view while remaining active in the "
        "simulated cell, so that only the scheduler's sight of it changed. One of the three "
        "couplings that can be ablated in this way changes decisions. With machine pace hidden "
        "from the ergonomic score, the scheduler admits pairings that breach the ergonomic limit "
        "in fact, producing 5.3 genuine breaches per shift against zero for the full framework. "
        "Hiding competence-to-quality or fatigue-to-quality changed fatigue, throughput and "
        "scrap by less than run-to-run variation.",

        "The reason is redundancy rather than irrelevance, and the distinction matters. "
        "Competence already reaches the decision through processing time, through the "
        "skill-matching preference and through the competence floor; fatigue reaches it through "
        "the fatigue limit and through the objective's fatigue term. Machine pace has exactly "
        "one route into the decision, the ergonomic score, which is why it is the only ablation "
        "that bites. The coupled twin therefore does less work through the quality equation than "
        "the design anticipated, and more through the constraint set."]),

    ("Hypotheses and Discussion", [
        "Two hypotheses were stated before the experiments. The first held that including a "
        "human digital twin in the decision would reduce operator fatigue and ergonomic risk by "
        "at least 20% for a throughput cost of at most 10%. It is only partly supported. The "
        "fatigue target is met in all three scenarios, at 26.2%, 27.0% and 31.9%. The ergonomic "
        "target is not met in any: the reductions are 13.2%, 14.6% and 14.3%. The arithmetic "
        "explains why. Mean ergonomic risk cannot fall below 2.90 for the task mix used, because "
        "the baseline posture scores of the task types floor it, so at most a 38% reduction was "
        "ever available; of the 1.13 points that remain above that floor under the proposed "
        "policy, 1.08 are the fatigue term. The hypothesis set a target on a bounded index "
        "without accounting for its floor, and the part of the index that is actually "
        "controllable is the part the framework moves. The throughput condition is met under "
        "normal and high demand but not under disruption, where the cost reaches 12.7%.",

        "The second hypothesis held that protecting the operator would also reduce machine "
        "downtime, on the argument that a fatigued operator generates defects and stress that "
        "the equipment ultimately absorbs. It is supported under normal and high demand, where "
        "downtime falls by 28.3% and 26.9% respectively at p < 0.001, and is not supported under "
        "disruption, where unplanned repairs dominate downtime and no policy can avoid them "
        "(p = 0.906). The supported half is the more useful one: it says that human-centric "
        "allocation is not purchased at the expense of the equipment, and speaks to an Industry "
        "4.0 audience in its own terms.",

        "Two indicators showed no significant effect. Scrap rate and overall equipment "
        "effectiveness differed by −7.9% and +2.6% under high demand, neither reaching "
        "significance after correction. The appropriate reading is that the human-centric and "
        "environmental gains were achieved without degrading product quality or equipment "
        "effectiveness, and no claim of improvement in either is made.",

        "One result runs against the framework and is reported rather than omitted. Work was "
        "distributed less evenly under the proposed policy than under the baseline. The "
        "mechanism is direct: hard constraints remove operator–task pairings from the "
        "feasible set, so the remaining work concentrates on whoever is still eligible. "
        "Increasing the fairness preference eightfold changed the distribution by less than "
        "0.3%, since a preference can only choose among eligible pairings. The cause lies in the "
        "workforce rather than in the scheduler: the operator with the highest sustainable work "
        "level is the only one excluded from heavy tasks, his competence at them falling below "
        "the floor, so heavy work falls to the two operators least able to sustain it. Because "
        "the framework models both the equipment and the person, it can localise that and price "
        "it: raising that single competence past the floor closes roughly two thirds of the gap "
        "in every scenario and raises throughput in every scenario, with breaches still at zero. "
        "This is reported as a diagnosis and not applied as a fix; the results above stand on "
        "the configuration that was actually run. A machine-only twin could not pose the "
        "question, because the constraint it would have to reason about does not exist in its "
        "model."]),
]

TABLE3_NOTE = ("Mean ± standard deviation over 30 runs. Δ is the change of the "
               "proposed policy relative to the Industry 4.0 baseline; for workload balance, "
               "which sits near zero, the absolute difference is given. Mann–Whitney U, "
               "Bonferroni-corrected at α = 0.0045; δ is Cliff's delta.")

FIG3_CAPTION = ("Fig. 3. Throughput against mean operator fatigue as the fatigue limit is swept "
                "across 0.70, 0.80 and 0.90. Filled markers are the operating point; crosses are "
                "the Industry 4.0 baseline for the same scenario.")

FIG4_CAPTION = ("Fig. 4. The three policies on six indicators under high demand, two per "
                "sustainability pillar. Error bars are one standard deviation over 30 runs. The "
                "proposed policy records zero constraint breaches, marked by the stub on the "
                "baseline.")

# =============================================================================
# VI. LIMITATIONS  ·  VII. CONCLUSION
# =============================================================================
LIMITATIONS = [
    "The fatigue accumulation and recovery rates are calibrated rather than measured; "
    "operator-specific values would require physiological data collection that a simulation "
    "study does not include. Both are held inside the range implied by published exponential "
    "work–recovery models, with the recovery rate kept below the localized-muscle bound "
    "reported for manual work {yi2022demolition}. "
    "Their influence is further bounded by the sensitivity analysis of Section "
    "V. The two coupling coefficients linking competence and fatigue to defect risk are "
    "likewise calibrated, because no available dataset carries operator attributes alongside "
    "process outcomes; their influence is bounded by the ablation. The deferral rate exceeds "
    "the 15% guard adopted during design in two scenarios, at 24% and 19%; removing the fatigue "
    "limit entirely moves that rate by less than one point, which locates the cause in the "
    "ergonomic ceiling and the competence floor rather than in fatigue, and neither can be "
    "relaxed without permitting the outcomes the framework exists to prevent.",

    "Three elements of the specification are not implemented. The decision layer uses a weighted "
    "sum rather than the multi-objective search the architecture allows, so no Pareto front is "
    "claimed; the trade-off in Fig. 3 is a constraint sweep. The explanation and override layer "
    "is specified but not built, so no claim is made about operator acceptance or oversight in "
    "practice. Twin parameters are estimated from data rather than learned by predictive models. "
    "Finally, one of the three datasets is synthetic, the operator profiles are synthetic, and "
    "the cell is small at five machines and three operators; validation in an operating facility "
    "remains future work, as do the multi-objective search {deb2002nsga2} and the explanation layer {lundberg2017shap}, "
    "and the privacy and ethical questions that arise once a twin models a named person {cardin2022ethics}."
]

CONCLUSION = [
    "This article has presented a task allocation framework in which a machine digital twin and "
    "a human digital twin are coupled through five explicitly defined bidirectional interfaces, "
    "and in which operator fatigue, competence and ergonomic risk filter the candidate set "
    "before optimisation rather than entering the objective as penalties. Fatigue is modelled as "
    "a physiological state with per-operator bounds derived from published anthropometric "
    "equations, so that protection differs between individuals as their physiology differs, "
    "without any rule prescribing the difference.",

    "Across 270 runs of a co-simulated machining cell, the framework reduced mean operator "
    "fatigue by 27.0% and energy per unit by 30.8% relative to an Industry 4.0 baseline under "
    "high demand, and eliminated every constraint breach, at a throughput difference that was "
    "not statistically significant. Machine downtime fell as well under normal and high demand, "
    "which suggests that protecting the operator is not paid for by the equipment. The weighting "
    "of the objective proved almost irrelevant to the outcome: after the constraints filter, "
    "most decisions have nothing left to weigh. That is the central lesson. In a human-centric "
    "formulation the protection has to live in the feasible set rather than in the objective, "
    "because only there can it not be traded away.",
]
