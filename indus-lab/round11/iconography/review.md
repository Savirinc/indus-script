# Round11: imagery labels do not yet isolate a sign400–animal relationship

The requested exploratory follow-up uses only the fixed round10 TAB:B representative rows. Sign400 was already selected; Gavi was selected as the requested comparison, and category counts were viewed before the protocol was frozen. All inference is post hoc and exploratory.

## Descriptive counts

Cells below give **sign400 present / category total**; categories refer to raw catalogue labels, not independently verified motif presence.

| Raw category | Harappa | Mohenjo-daro |
|---|---:|---:|
| Gavi | 6/9 | 0/0 |
| Other specific labels | 12/43 | 0/9 |
| Mult | 3/8 | 4/9 |
| Othr | 1/1 | 0/0 |
| Literal None | 41/100 | 3/8 |
| Missing | 1/2 | 0/3 |

Literal `None` is preserved as a label; it does not establish the absence of an image. `Mult` and `Othr` do not establish the absence of Gavi or any other specific motif. "Other specific" means other named raw labels, not verified motif-negative controls. It includes labels such as Scene whose full motif contents are unspecified.

## Frozen comparison

Within Harappa, Gavi-labelled representatives have sign400 in 6/9 cases, compared with 12/43 for other specific labels. Conditioning on exact sign length gives a common odds-ratio estimate of 5.77 with an exact equal-tail 95% interval of **0.91–63.89**. This is imprecise and includes no association. The equal-tail exact two-sided p is .0667. The previously used absolute-distance two-sided convention produces .0467; discrete exact two-sided definitions differ. A claim of a confirmed association based on selecting the smaller p would be unwarranted, especially given post hoc selection.

The declared coding sensitivity including Mult/Othr among non-Gavi labels is similar: 6/9 versus 16/52, odds ratio 5.84, interval 0.92–65.30, equal-tail p=.0653. It does not repair motif measurement.

Mohenjo-daro has no Gavi-labelled representative in this sample, so the within-city comparison is not estimable. Combining sites cannot supply a genuine within-Mohenjo-daro comparison. No other motif significance scan was performed.

## M-482 audit and what can be concluded

Raw record2966.1/M-482 has `symbol=Mult`, `type=TAB:B`, `text=+400-740-803+`, and `sides=1`. The coordinator reports a Gavi identification from its photograph; this agent has not independently inspected that photograph. These statements need not conflict. A label "multiple" does not say that Gavi is absent. It would therefore be incorrect to treat this case automatically as a mistranscription and replace Mult with Gavi.

The existing field is a single category. Our research question requires multiple motif-presence fields for every physical object/face: Gavi present, another animal present, human figure present, plant motif present, and so on, each with absent/not visible/uncertain/uninspected states and photographic references. A confirmed Gavi-positive photograph under raw Mult would falsify the shortcut "raw label other than Gavi means Gavi absent," not identify the meaning of sign400.

This check does not establish whether sign400 tracks animal imagery or tablet manufacture. Holding the raw TAB:B subtype fixed is useful, but material, manufacturing details, dates, workshops, and associated motifs remain unvalidated or uncontrolled. Literal None dominates Harappa's sample (100/163), and all seven Mohenjo-daro sign400 positives fall under Mult or literal None. Therefore the most relevant cases cannot be properly classified from the existing exclusive field.

A falsifiable next comparison requires photo-verified multi-label annotation of all selected cases and matched sign400-negative controls, with annotators blinded to the sign400 hypothesis where feasible. Freeze the visual classification before comparing signs. Keep already inspected examples exploratory and reserve new verified examples for confirmation. No reading, animal name, commodity, or phonetic value is justified by this analysis.

Files: protocol.md (written before inferential calculation); analyze.py; analysis_rows.json; results.json. Reproduce with `python3 indus-lab/round11/iconography/analyze.py`. Uses NumPy/SciPy and the reviewed round10 exact-conditional implementation. Other rounds are unmodified.
