# Joint composition-and-position control

Fixed before execution, 11 October 2026. Follow-up motivated by round27's independent review; not a new independent corpus.

Reuse the exact round27 one-edit-excluded test sets, fixed unigram/bigram models and four city/subset conditions. For source texts of equal length, randomly select two rows and two distinct columns. If their 2×2 entries are a,b / b,a with a!=b, exchange both rows' entries in those columns. This preserves each individual inscription's sign multiset and every length-specific column's counts simultaneously. No row crosses a length group or city/subset.

Use 10 fixed-seed chains per condition, starting at the observed source. Each chain has 20,000 burn-in proposals followed by 10 samples separated by 2,000 proposals, for 100 sampled controls per condition. Proposals choose a uniformly random eligible length group, two rows, and two columns. Rejected proposals count. There is no tuning after results. Log accepted moves, changed-cell and changed-row fractions and invariant checks for every sample.

These local swaps may fail to connect the full constrained state space and may mix poorly. Samples are correlated. No uniform sampling, convergence or exact randomisation p-value is claimed. If the controls change little, report that limitation explicitly. Compare internal-sign loss only for the main result; boundary prediction is invariant under these moves. A positive difference supports structure beyond these sampled local rearrangements, not language identity or meaning.
