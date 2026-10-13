# Clinical reference ![draft](https://img.shields.io/badge/draft-lightgrey)

This file is a draft that I wrote as a non-expert, and I want a urologist to read it and correct it before I use it in my tests. I'm a software engineer, so everything here comes from papers and guidelines I read, and some of it I only understood partly.

I need this file because my tests compare what the model says with a "correct answer", and I can't entirely decide that correct answer on my own. In my [literature notes](02-literature.md) I wrote that I still didn't know which "normal" ranges to use, and that I needed a specialist for that. This file is my attempt to prepare that conversation. It is only meant to score the answers of an AI model in my experiment, and I'm not building anything that would tell a real person what to do.

## Units

The first thing I checked is the unit, because I want to test whether the model changes its answer when only the unit changes. PSA is usually written in ng/mL, and some labs write µg/L. A nanogram per millilitre is the same quantity as a microgram per litre, since both sides are multiplied by a thousand, so 4.0 ng/mL and 4.0 µg/L are exactly the same result.

## The value printed on some reports

I looked for example reports and test pages that labs publish themselves, with fictional patients. Warde Medical Laboratory prints a range of 0.00 to 4.00 ng/mL on its [example report](https://wardelab.com/wp-content/uploads/2022/02/PSAUS.pdf), and the University of Florida pathology lab gives 0.0 to 4.0 ng/mL too on its [test page](https://pathlabs.ufl.edu/tests/test-directory-p/prostate-specific-antigen-psa-total/), without any range by age. Singapore General Hospital uses the same limit written in the other unit, 0 to 4.0 µg/L, on its [test page](https://sgh.com.sg/patient-care/specialties-services/prostate-specific-antigen-psa-total-serum). I was surprised by the [example report from Mayo Clinic Laboratories](https://www.mayocliniclabs.com/-/media/it-mmfiles/test%20notifications/e/f/8/81944%20sample%20report%2020190925%20prostatespecific%20antigen%20psa%20total%20and%20free%20serum.pdf), which prints 4.5 or less as the limit, so I guess even labs don't all print the same number.

So 4 is the most common limit, and it is also where the [study on free PSA by Catalona and colleagues](https://www.qxmd.com/r/9605898) starts, since it only looks at men between 4 and 10. My [first hypothesis](01-hypotheses.md) is that the model will repeat whatever range is printed and call anything under it normal. While reading, I understood that this single number hides a lot, which is what the next sections are about.

## Normal depends on age

I first read about age-specific ranges in Morgan et al. while doing my literature notes, and I went back to the older paper they compare with. Oesterling and colleagues measured PSA in 471 men without prostate cancer in Minnesota, and proposed different PSA limits for different age groups, using the median plus two standard deviations ([JAMA, 1993, vol. 270, pages 860 to 864, described here](https://cancernetwork.com/view/age-specific-reference-ranges-psa-detection-prostate-cancer)).

They then studied American military men, with 1,673 Black men and 1,802 white men without cancer, and 411 Black men and 1,372 white men with cancer ([NEJM, 1996](https://doi.org/10.1056/NEJM199608013350502), [summary with the numbers](https://www.cancernetwork.com/view/new-psa-values-better-detect-prostate-cancer-black-men)).

They took the age ranges proposed by Oesterling, which were calculated on mostly white men, and checked what happens when you use them for Black men. They found that, 41% of the cancers in Black men would have been missed, because the PSA of these men was still under the limit for their age. So they calculated new ranges for Black men, which are lower than Oesterling's in the 40s and 70s.

After that, I looked for similar studies in Cameroon, but I could not find any that gave PSA limits by age for healthy men. I then found a study from Lagos, Nigeria, on healthy civil servants who went for routine checkups ([Nigerian Journal of Surgery, 2016](https://doaj.org/article/5eb6be81605243a19a40b72492dc2b27)). Their limits are higher than both American studies, and the studies did not all calculate their limits in the same way, which honestly confused me a bit.


| Age      | Oesterling 1993 (USA, 95th percentile) | Morgan 1996 (Black men, USA, 95% sensitivity) | Lagos 2016 (Nigeria, 95th percentile) |
| -------- | -------------------------------------- | --------------------------------------------- | ------------------------------------- |
| 40 to 49 | 2.5                                    | 2.0                                           | 4.78                                  |
| 50 to 59 | 3.5                                    | 4.0                                           | 5.47                                  |
| 60 to 69 | 4.5                                    | 4.5                                           | 8.93 (reported for ages 60 to 70)     |
| 70 to 79 | 6.5                                    | 5.5                                           | Not reported for this age group       |


All values are in ng/mL. I found the Oesterling and Morgan values shown side by side on [this page](https://www.blackhealth.org/articles/psa-levels-by-age-black-men/), which also says these ranges are old and are no longer used on their own when deciding what to do next. I still haven't seen the original tables myself.

The Oesterling and Lagos ranges describe what is common in healthy men, while Morgan's are designed to catch cancers, so they don't answer the same question. This is one of the points I want the urologist to decide for my tests.

I looked for a study with reference values for Cameroonian men and I didn't find one.

## What the guidelines say about the next step

I wanted to know what a doctor would usually do after a result, because I believe a good answer from the model should point in the same direction. The American Urological Association guideline of 2023 says that a newly raised PSA should be repeated before going further, that screening can start at 40 to 45 for men of Black ancestry, and that a rising PSA alone should not be the only reason for more tests ([AUA/SUO guideline page](https://www.auanet.org/guidelines-and-quality/guidelines/early-detection-of-prostate-cancer-guidelines), [summary from the AUA 2023 meeting](https://www.urotoday.com/conference-highlights/aua-2023/aua-2023-prostate-cancer/143971-aua-2023-aua-guidelines-early-detection-of-prostate-cancer.html)). The same summary says that above 50 ng/mL, when there is no infection or other cause, a doctor may even skip the biopsy if treatment is urgent.

The European guideline uses an approach based on the first PSA. According to a [side-by-side comparison of both guidelines](https://www.guidelinecentral.com/insights/jun-2026-earlydetectionprostatecancer-guideline-sidebyside/), men with a PSA above 1 at 40 or above 2 at 60 should be followed every two years, it recommends early testing from 45 for men of African descent, and a PSA between 3 and 10 in a man without symptoms should be repeated before more tests. I read this through the comparison page and I haven't opened the European guideline itself yet.
