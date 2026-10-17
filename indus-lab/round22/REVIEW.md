# Independent code review

A separate review agent inspected the protocol, code and results. No direct held-out answer leakage into fitted mappings was found. Training excludes the held-out concept; scoring and fixed tie-breaking match the protocol.

The main comparison is 632/782 initial predictions correct versus 576/782 for copying, not the much weaker shuffled control. Improvement occurs in 11 directions, ties in three and declines in five.

The reviewer flagged the original wording "equal-concept micro accuracy": observations are equally weighted concept-language records, not equally weighted unique concepts. The protocol now explicitly documents this wording correction.

Eligibility uses both source and target initials and supplied cognacy labels to select an unambiguous sample. Although target initials are not fed into training for held-out concepts, this is a favorable sample selected with knowledge of the answers' ambiguity. Performance cannot be extrapolated to unknown cognates or all vocabulary.

Related languages, shared concepts and overlapping cross-validation training folds make the observations dependent. No ancestral pronunciations, chronology or Indus reading follows from these accuracy scores.
