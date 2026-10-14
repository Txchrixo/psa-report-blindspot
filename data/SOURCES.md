# Data sources

## CARET serial PSA measurements

`raw/caret_psa_serial.csv` contains real PSA values measured several times on the same men. They come from the CARET study, an American trial that was about preventing lung cancer, where blood was also stored and later used to study PSA over time. The values are anonymous, and each man only has a number.

I downloaded the file `psa.rda` from the GitHub copy of the R package AROC, where it is the dataset called `psa`: https://github.com/cran/AROC/raw/master/data/psa.rda. Then I converted it to CSV with `convert_caret.py`, and I renamed the columns so I could understand them.

The file contains 683 blood draws from 141 men (71 of whom were later diagnosed with prostate cancer, 70 were not). Most of the men have 1 to 9 draws, most within 1 year, some over 2 years apart. The range of the PSA ranges from 0.03 to 99.98ng/mL, with the median being 1.8. 

| Column | Original name | What it means |
| --- | --- | --- |
| `id` | `id` | The number of the man |
| `psa_total_ng_ml` | `marker1` | Total PSA in ng/mL |
| `free_to_total_ratio` | `marker2` | Free PSA divided by total PSA (0.20 means 20%) |
| `cancer_case` | `status` | 1 if the man was later diagnosed with prostate cancer, 0 if not |
| `age` | `age` | His age when the blood was taken |
| `years_from_diagnosis` | `t` | Years between the blood draw and the diagnosis (negative means before) |

I don't know what the reference date of `years_from_diagnosis` is for the men who never had cancer. I need to check the AROC documentation for that. 

The study to cite is Etzioni R, Pepe M, Longton G, Hu C, Goodman G (1999). *Incorporating the time dimension in receiver operating characteristic curves: a case study of prostate cancer.* Medical Decision Making 19(3):242–251. The AROC package is distributed under the GPL licence.

## NHANES (maybe later)

If I need single values with free PSA and the age of more men, I might use the American NHANES survey from 2009 to 2010 (files PSA_F and DEMO_F on the CDC website). I haven't downloaded it yet. It says that the data may be used only for statistical purposes, and that nobody should try to identify the people in it.