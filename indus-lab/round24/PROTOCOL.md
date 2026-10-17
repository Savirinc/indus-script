# Copper tablet text–motif association test

Written before execution. The source catalogue and hare group have been inspected before: this is retrospective internal testing, not independent discovery.

Use only id, cisi, material, type, symbol, dir., text and excavation-idno from the supplied CSV. Do not use its speculative Sanskrit/translations. Select Copper TAB records; group by catalogue object ID. Require a single distinct informative symbol label across an object's rows, excluding blank, None, -, Unknown, Othr. These excluded labels are unspecified, not proof of absent imagery. Preserve raw motif category codes without expanding them into meanings.

Choose the longest clean, direction-labelled R/L or L/R text per object. Clean means +DDD-DDD+ format with no 000. A tie of distinct longest strings is ambiguous and excluded. Stored sign order is used unchanged. This selection excludes nonreading reverse marks from the predictor; the full whitelisted copper ledger is retained separately. Catalogue IDs are not independently verified physical-object identities.

Test A: leave one catalogue object out; predict its motif only if the remaining exact-text matches have a unanimous label. Abstain if no match or conflict. This measures repeated-text association only.

Test B: hold out the entire exact-text family. Find training text families at minimum unit-cost sign edit distance divided by maximum sequence length. Predict only if the union of labels from all tied nearest families is one category. Otherwise abstain. Do not tune distance, choose favourable neighbours or discard failures. Report object-weighted accuracy, coverage and equal-text-family mean success. Compare with a training-only majority-label baseline that also abstains on tied modes. Report when a held-out label does not exist in training.

Families are exact strings only; near-duplicates remain possible. Classifications may derive from the same scholarly reconstruction. Both tests are internal catalogue checks, not independent photographic validation. Neither a text–motif association nor a prediction establishes the spoken animal name, a sign sound value, or Dravidian language identity.
