# §V Results — draft paragraphs

> Ready to paste. Every number here is in `results/kpi_table.csv`,
> `results/sensitivity_hc1.csv`, `results/sensitivity_fatigue.csv` and
> `results/crosstraining.csv`, and every claim is one the statistics support.
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
> aggregate: work was deferred in 14.4% of decision epochs under high demand.
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

## E. Measures where no effect was found

> Scrap rate and OEE differed by −7.9% and +2.6% respectively under high demand;
> neither reached significance after correction (p = 0.408 and p = 0.112). We
> therefore report that the framework achieved its human-centric and
> environmental gains **without degrading either product quality or overall
> equipment effectiveness**, and make no claim of improvement in them.

*(Phrasing note: this states a genuine and useful result — the gains were not
bought at the expense of quality or equipment utilisation — while claiming
exactly what the data supports and nothing beyond it.)*

---

## F. Contribution bullets for §I

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
