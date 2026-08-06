# §V Results — draft paragraphs

> Ready to paste. Every number here is in `results/kpi_table.csv`,
> `results/sensitivity_hc1.csv`, `results/sensitivity_fatigue.csv`,
> `results/crosstraining.csv`, `results/ablation.csv`,
> `results/deferral_diagnosis.csv` and `results/decision_pressure.csv`, and
> every claim is one the statistics support.
>
> **The rule this draft follows:** state findings in the affirmative, name
> trade-offs as design properties rather than apologies, and never claim an
> effect the test did not find. Confidence comes from having measured the
> awkward parts, not from omitting them.

---

## A. Headline result

> Under high demand (S2), the proposed framework reduced mean operator fatigue
> by 27.0% and energy consumption per unit by 30.8% relative to the Industry
> 4.0 baseline, while eliminating all 79.5 hard-constraint breaches per shift
> that the baseline incurred. Both improvements carry the maximum effect size
> (Cliff's δ = −1.00) at p < 0.001 after Bonferroni correction. The
> accompanying change in throughput was −1.8% and was **not statistically
> significant** (p = 0.148).
>
> This is the central finding: **at the point where demand exceeds what the
> workforce can comfortably absorb — precisely where a throughput-driven
> scheduler pushes hardest — protecting the operator cost no measurable
> production.**

**Why this is the right scenario to lead with.** S1 leaves roughly twenty
percent slack, so the constraints rarely bind and the comparison is
uninformative. S2 removes the slack. The framework's value is not that it
schedules well when scheduling is easy; it is that it holds a limit when
holding it is expensive.

---

## B. The trade-off, stated as a property

> Under normal (S1) and disrupted (S3) demand the framework produced 10.0% and
> 12.7% fewer units than the baseline (both p < 0.001). These are not
> incidental losses. They are the throughput the framework declines to extract
> once an operator would exceed 80% of their own sustainable work level, and
> the framework reports the quantity directly rather than absorbing it into an
> aggregate: work was deferred in 11.0% of decision epochs under high demand,
> and in 24.0% and 19.0% under normal and disrupted demand.

*(⚠️ Corrected 2026-08-06: an earlier draft of this paragraph said 14.4%,
which is in none of the result files. The figures above are the mean deferral
epochs per shift in `results/raw_results.csv` over the 30-seed evaluation
block, divided by the 32 epochs in a shift; `results/feasibility.csv` gives
24.4 / 11.6 / 19.5% over its own 20-shift window.)*
>
> **A framework that never gave anything up would not be enforcing anything.**
> The contribution is that the price is bounded, measured and, under the
> demand conditions that matter most, statistically indistinguishable from
> zero.

---

## C. Workload distribution — a diagnosis the framework makes possible

> Work was distributed less evenly under the proposed framework than under the
> baseline (Gini 0.024 vs 0.005 in S2). The mechanism is direct: hard
> constraints remove operator–task pairings from the feasible set, so the
> remaining work concentrates on whoever is still eligible.
>
> Two candidate remedies were tested and rejected. Increasing the fairness
> preference eightfold changed the distribution by less than 0.3% — a
> preference can only choose among eligible pairings, and eligibility is
> decided upstream by the hard constraints. Re-expressing fairness as equality
> of physiological strain rather than of time gave an inconsistent picture
> across scenarios and was therefore not adopted.
>
> The cause lies in the workforce rather than the scheduler. OP1 is the
> operator with the highest sustainable work level and the only one excluded
> from heavy tasks, his competence at them falling below the HC2 floor. Heavy
> work is therefore borne by the two operators least able to sustain it.
>
> **Because the framework models both the equipment and the person, it can
> localise this and quantify the intervention.** Raising that single skill past
> the competence floor closed 61–70% of the distribution gap in every scenario
> and increased throughput in every scenario (+2.0 to +4.9 units), with
> constraint breaches remaining at zero.
>
> This extends the framework's use beyond scheduling: the same twin that
> allocates work can answer *which competence gap is costing the most*. A
> machine-only digital twin cannot pose that question, because the constraint
> it would have to reason about does not exist in its model.

**Reported honestly alongside:** the intervention does not close the gap
entirely, it exceeds the baseline's throughput in one scenario of three, and
mean fatigue rises from 0.541 to 0.583 — still 21% below the baseline. The
headline results are reported on the original configuration, not the retrained
one.

---

## D. Robustness

> Three parameters of the framework are calibrated rather than measured: the
> fatigue accumulation and recovery rates, and the fatigue threshold expressed
> as a fraction of each operator's acceptable work level. Each was varied and
> the comparison repeated.
>
> Scaling both fatigue rates by 0.5, 1 and 2 — a fourfold span — preserved the
> ranking on every human-centric measure. The framework's advantage grew with
> the rate (25.4%, 27.0%, 33.1% less mean fatigue) and so did its cost (0.8%,
> 1.8%, 5.9% of throughput), which is the behaviour the model implies.
>
> Varying the threshold across 0.70, 0.80 and 0.90 likewise preserved the
> ranking in all three scenarios. Peak fatigue tracked each threshold from just
> below (0.688, 0.780, 0.858) and throughput rose monotonically with it (65.1,
> 67.5, 69.0 units), tracing the safety–output trade-off as a curve rather than
> a single operating point.
>
> **The conclusions therefore rest on the framework rather than on the values
> chosen for its free parameters.**

---

## E. Where the behaviour comes from  *(T7.7 — the interpretation)*

Sections A–D report what happened. This one reports *why*, and the answer is
the same in three independent studies: **this framework is steered by its
constraints, not by its objective.** That is worth stating plainly, because it
is also the claim the rest of the paper makes — and it turns out to be
measurable rather than rhetorical.

### E.1 The weights do not steer

> Four weight configurations, spanning a sevenfold difference in the human
> terms, produced mean fatigue of 0.541 to 0.542 and throughput of 90.2 to 90.3
> units. They are indistinguishable.
>
> The reason is upstream of the objective. After the hard constraints filter
> the candidate set, **95.7% of the 45,754 decisions in the high-demand
> scenario face either no admissible pairing or exactly one** — there is
> nothing left to weigh. In the remaining 4.3% the spread between the best and
> worst admissible option has a median of 0.015 on the objective's own scale.
> The pattern holds across scenarios: 94.7% in S1 and 95.6% in S3.

**Read as a design property, not a defect.** A framework whose human
protections could be tuned away by re-weighting an objective would not be
offering protection. The weights choose among options the constraints have
already declared acceptable, which is exactly the ordering the framework
claims: *filter first, optimise second.*

### E.2 Industry 4.0 is the limit of the objective, not of the framework

> The profit-weighted configuration converges on the baseline's throughput to
> within 1.8%, as the experiment plan predicted. It does **not** converge on the
> baseline's fatigue or its breach count, and cannot: driving every human weight
> to zero leaves the fatigue limit, the competence floor and the ergonomic
> ceiling filtering before the objective is ever consulted.

This is a sharper statement than the one originally anticipated. The framework
does not *contain* Industry 4.0 as a special case; it contains Industry 4.0's
*preferences* as a special case, while continuing to refuse what Industry 4.0
would permit.

### E.3 Which couplings actually carry decisions

> Each coupling was removed from the scheduler's view while leaving it in the
> factory, so that a tired operator still makes more mistakes and only the
> scheduler's sight of it changes. **One of the three ablatable couplings
> changes decisions.** With machine pace hidden from the ergonomic score, the
> scheduler admits pairings that breach the ergonomic limit in fact: 5.3 real
> breaches per shift against zero for the full framework. Hiding skill-to-quality
> or fatigue-to-quality changed fatigue, throughput and scrap by less than noise,
> and raising the quality weight from 0.15 to 0.25 did not change that.

**The reason is redundancy, not irrelevance**, and the distinction matters.
Skill already reaches the decision through processing time, the skill-matching
preference and the competence floor; fatigue reaches it through the fatigue
limit and the objective's fatigue term. Machine pace has exactly one route in —
the ergonomic score — which is why it is the only ablation that bites. The
coupled twin is therefore doing less work through the quality equation than the
design anticipated, and more through the constraint set. *(Two further
couplings could not be ablated and are stated rather than skipped: cognitive
load is computed and reported but never consulted by the decision layer, and
task intensity enters as the asymptote of the fatigue equation rather than as a
link into it.)*

### E.4 What actually closes the feasible set

> The deferrals in §B are not caused by the fatigue limit. Removing that limit
> entirely moves the deferral rate by +0.2, −0.8 and −0.5 points across the
> three scenarios while producing 161 to 208 genuine breaches. What closes the
> set is the **ergonomic ceiling** (7.8 points in S1) and the **competence
> floor** (4.5 points).

That result joins the workload finding in §C: the competence floor is what
excludes the strongest operator from heavy work, so the same constraint that
concentrates the load also stalls the queue. **One workforce fact explains two
apparently unrelated costs**, and the coupled twin is what makes it visible as
a single cause rather than two symptoms.

### E.5 The trade-off is tuned through the constraint

Figure 3 draws the efficiency–wellbeing curve by sweeping the fatigue limit
across 0.70, 0.80 and 0.90 rather than by re-weighting the objective — which,
per §E.1, would have produced three coincident points presented as a frontier.
Peak fatigue tracks each threshold from just below it and throughput rises
monotonically with it.

> **The practical consequence for a plant: the dial that moves this system is
> the limit an organisation is willing to set on its people, not the priority
> it declares in an objective function.** The framework makes that dial
> explicit, and reports what each setting costs.

---

## F. Measures where no effect was found

> Scrap rate and OEE differed by −7.9% and +2.6% respectively under high demand;
> neither reached significance after correction (p = 0.408 and p = 0.112). We
> therefore report that the framework achieved its human-centric and
> environmental gains **without degrading either product quality or overall
> equipment effectiveness**, and make no claim of improvement in them.

*(Phrasing note: this states a genuine and useful result — the gains were not
bought at the expense of quality or equipment utilisation — while claiming
exactly what the data supports and nothing beyond it.)*

---

## G. Contribution bullets for §I

> 1. **A bidirectionally coupled human–machine digital twin.** Operator fatigue
>    evolves as a physiological state with per-person parameters derived from
>    published anthropometric equations, and feeds back into machine-side
>    defect risk. Five coupling points carry state in both directions.
>
> 2. **Constraint-based rather than penalty-based protection.** Human limits
>    filter the feasible set before optimisation, so no weighting of the
>    objective can trade them away. Breaches fall from 79.5 per shift to zero.
>
> 3. **A quantified trade-off, including where it is zero.** Under high demand
>    the framework reduces fatigue by 27% and energy per unit by 31% at no
>    statistically detectable cost in throughput, and it reports the deferrals
>    that buy that outcome rather than concealing them.
>
> 4. **A diagnostic use of the coupled twin.** The framework localises the
>    competence gap responsible for uneven workload and quantifies the benefit
>    of closing it — a question a machine-only twin cannot represent.

---

## ⚠️ Lines this draft does not cross

| Not written | Why |
|---|---|
| "quality improved" | p = 0.408 |
| "OEE improved" | p = 0.112 |
| "HC1 = 0.80 following Price (1990)" | Price supplies AWL; 0.80 is ours |
| "λ = 0.020 as reported by Calzavara" | The form is theirs; the values are ours |
| Workload result omitted | It is significant, large, and against us |
| Results reported on the retrained matrix | That would be fitting the setup to the answer |
| "the weights let a practitioner tune the trade-off" | They move nothing measurable (§E.1) |
| "all five coupling points contribute" | One of three ablatable ones changes decisions (§E.3) |
| "the fatigue limit causes the deferrals" | Removing it changes the rate by ≤ 0.8 points (§E.4) |
| "a Pareto front" | No multi-objective search was run; Fig 3 is a constraint sweep |
| "the deferral rate meets the 15% design guard" | It does not in S1 and S3; §VI carries it |
