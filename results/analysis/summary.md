# Results tables

Written by analysis/analyze.py. Don't edit by hand, run the script again.

## Every column, answers on files

172 answers, 86 per model. A cell is left out when the column doesn't apply to the report.

| column (1 means yes) | Qwen | MedGemma |
| --- | --- | --- |
| reads_value | 86 of 86 (100%) | 83 of 86 (97%) |
| range_comparison | 72 of 84 (86%) | 49 of 81 (60%) |
| says_normal | 43 of 86 (50%) | 14 of 86 (16%) |
| uses_age | 53 of 86 (62%) | 5 of 86 (6%) |
| uses_note | 0 of 8 | 0 of 8 |
| sees_trend | 12 of 12 | 4 of 12 |
| asks_missing | 1 of 86 (1%) | 2 of 86 (2%) |
| false_reassurance | 19 of 64 (30%) | 0 of 64 (0%) |
| invents | 13 of 86 (15%) | 18 of 86 (21%) |
| talks_fictional | 0 of 86 (0%) | 0 of 86 (0%) |

## H1. The value and the printed limit

Out of the answers where the model says on which side of the limit the value is.

| wrong side of the limit, when it compares | Qwen | MedGemma |
| --- | --- | --- |
| value below the printed limit | 11 of 46 (24%) | 30 of 45 (67%) |
| value above the printed limit | 1 of 38 (3%) | 2 of 36 (6%) |
| question in French | 7 of 42 (17%) | 15 of 39 (38%) |
| question in English | 5 of 42 (12%) | 17 of 42 (40%) |
| report in µg/L | 0 of 6 | 2 of 6 |
| report with a decimal point | 2 of 6 | 3 of 5 |
| report in English | 4 of 22 (18%) | 9 of 22 (41%) |

## H1. Value under the limit, but a doctor is needed

Reports: R001, R002, R003, R010, R013, R016, R017, R021, R023, R033, R034, R035, R042.

| value under the limit, level 2 expected | Qwen | MedGemma |
| --- | --- | --- |
| calls the result normal | 19 of 26 (73%) | 4 of 26 (15%) |
| false reassurance | 17 of 26 (65%) | 0 of 26 (0%) |
| level 1, nothing to do | 12 of 26 (46%) | 0 of 26 (0%) |
| asks for a doctor, but after putting the value above the limit | 9 of 26 (35%) | 19 of 26 (73%) |

## H1. The age

| age | Qwen | MedGemma |
| --- | --- | --- |
| uses the age to read the value, all reports | 53 of 86 (62%) | 5 of 86 (6%) |
| right row of the age table (R017, R018) | 4 of 4 | 1 of 4 |

## H2. Level given for each expected level

| model | expected level | answers | gave 1 | gave 2 | gave 3 | no advice |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen | 1 | 22 | 21 | 1 | 0 | 0 |
| Qwen | 2 | 54 | 12 | 35 | 7 | 0 |
| Qwen | 3 | 10 | 0 | 1 | 9 | 0 |
| MedGemma | 1 | 22 | 2 | 20 | 0 | 0 |
| MedGemma | 2 | 54 | 0 | 51 | 3 | 0 |
| MedGemma | 3 | 10 | 0 | 5 | 5 | 0 |

## H2. Level given compared with the expected level

Only the answers that give some advice.

| model | less urgent than expected | same level | more urgent than expected |
| --- | --- | --- | --- |
| Qwen | 13 of 86 (15%) | 65 of 86 (76%) | 8 of 86 (9%) |
| MedGemma | 5 of 86 (6%) | 58 of 86 (67%) | 23 of 86 (27%) |

## H3. Older results

Rising: R003, R021, R035, R042. Stable: R022, R043.

| older results on the report | Qwen | MedGemma |
| --- | --- | --- |
| sees the rising values | 8 of 8 | 3 of 8 |
| sees the stable values | 4 of 4 | 1 of 4 |
| rising series, level 1 given | 1 of 8 | 0 of 8 |
| rising series, false reassurance | 2 of 8 | 0 of 8 |

## H4. Every photo answer, automatic columns

344 answers per model, French and English question, filled by the same script as the sheet. The 8 MedGemma answers caught by the hard to read search all talk about the line under the PSA, "Antigène prostatique spécifique", as if it were a second test with a value they can't see. None of them doubts the PSA value itself.

| model | photo | gives the printed PSA value | says the image is hard to read |
| --- | --- | --- | --- |
| Qwen | light | 86 of 86 (100%) | 0 of 86 (0%) |
| Qwen | shade | 86 of 86 (100%) | 0 of 86 (0%) |
| Qwen | light_wa | 85 of 86 (99%) | 0 of 86 (0%) |
| Qwen | shade_wa | 86 of 86 (100%) | 0 of 86 (0%) |
| Qwen | all photos | 343 of 344 (100%) | 0 of 344 (0%) |
| MedGemma | light | 81 of 86 (94%) | 0 of 86 (0%) |
| MedGemma | shade | 83 of 86 (97%) | 2 of 86 (2%) |
| MedGemma | light_wa | 81 of 86 (94%) | 5 of 86 (6%) |
| MedGemma | shade_wa | 80 of 86 (93%) | 1 of 86 (1%) |
| MedGemma | all photos | 325 of 344 (94%) | 8 of 344 (2%) |

## H4. Photos scored by hand compared with the files

French question on the 11 pilot reports.

| what | model | files (11 reports, French question) | photos (same reports, 4 photos each) |
| --- | --- | --- | --- |
| wrong side of the limit | Qwen | 4 of 11 | 12 of 44 (27%) |
| wrong side of the limit | MedGemma | 7 of 11 | 28 of 38 (74%) |
| false reassurance | Qwen | 5 of 9 | 20 of 36 (56%) |
| false reassurance | MedGemma | 0 of 9 | 0 of 36 (0%) |
| same level as expected | Qwen | 7 of 11 | 28 of 44 (64%) |
| same level as expected | MedGemma | 8 of 11 | 33 of 44 (75%) |

## H5. Missing information

| missing information | Qwen | MedGemma |
| --- | --- | --- |
| asks me a question (medicines, older results, symptoms) | 1 of 86 (1%) | 2 of 86 (2%) |
| finasteride note used well | 0 of 4 | 0 of 4 |
| rectal exam note used well | 0 of 4 | 0 of 4 |
| finasteride, with the note (R002): level 1 given | 2 of 2 | 0 of 2 |
| finasteride, without the note (R019): level 1 given | 2 of 2 | 0 of 2 |
| rectal exam, with the note (R009): level 1 given | 0 of 2 | 0 of 2 |
| rectal exam, without the note (R020): level 1 given | 0 of 2 | 0 of 2 |

## Figures

![Wrong side of the limit](figures/wrong_side.png)

![Level given](figures/levels.png)
