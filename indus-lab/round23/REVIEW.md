# Independent methods review

A separate agent reviewed code, protocol and results without modifying them. No direct held-out target leakage or alignment implementation bug was found. The predictor receives only source forms and tables trained on other concepts. Insertions and deletions follow the protocol; concatenating training emissions preserves the target sequence.

The 105/825 exact predictions versus 100/825 copying result is a small gain, not strong whole-word recovery. Context adds no exact-word gain and seven more edits than the segment model.

Material limitations: known cognacy, arbitrary synonym selection, dependent related-language observations and reused concepts. Holding out concepts does not necessarily exclude identical word forms appearing under different concepts. Context/segment support thresholds count token occurrences, not independent words. Unit-cost alignment choices are not independently established historical sound correspondences. No ancestral reconstruction, chronology or Indus reading follows.
