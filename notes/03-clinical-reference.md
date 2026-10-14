# Clinical reference 

This file is a draft that I wrote as a non-expert, and I want a urologist to read it and correct it before I use it in my tests. I'm a software engineer, so everything here comes from papers and guidelines I read, and some of it I only understood partly.

I need this file because my tests compare what the model says with a "correct answer", and I can't entirely decide that correct answer on my own. In my [literature notes](02-literature.md) I wrote that I still didn't know which "normal" ranges to use, and that I needed a specialist for that. This file is my attempt to prepare that conversation. It is only meant to score the answers of an AI model in my experiment, and I'm not building anything that would tell a real person what to do.

## Units

The first thing I checked is the unit, because I want to test whether the model changes its answer when only the unit changes. PSA is usually written in ng/mL, and some labs write µg/L. A nanogram per millilitre is the same quantity as a microgram per litre, so 4.0 ng/mL and 4.0 µg/L are exactly the same result.

## The value printed on some reports

I looked for example reports and test pages that labs publish themselves, with fictional patients. Warde Medical Laboratory prints a range of 0.00 to 4.00 ng/mL on its [example report](https://wardelab.com/wp-content/uploads/2022/02/PSAUS.pdf), and the University of Florida pathology lab gives 0.0 to 4.0 ng/mL too on its [test page](https://pathlabs.ufl.edu/tests/test-directory-p/prostate-specific-antigen-psa-total/), without any range by age. Singapore General Hospital uses the same limit written in the other unit, 0 to 4.0 µg/L, on its [test page](https://sgh.com.sg/patient-care/specialties-services/prostate-specific-antigen-psa-total-serum). I was surprised by the [example report from Mayo Clinic Laboratories](https://www.mayocliniclabs.com/-/media/it-mmfiles/test%20notifications/e/f/8/81944%20sample%20report%2020190925%20prostatespecific%20antigen%20psa%20total%20and%20free%20serum.pdf), which prints 4.5 or less as the limit, so I guess even labs don't all print the same number.

The limit of 4 appears on several of the reports I found, and it is also where the [study on free PSA by Catalona and colleagues](https://pubmed.ncbi.nlm.nih.gov/9605898/) starts, since it only looks at men between 4 and 10. My [first hypothesis](01-hypotheses.md) is that the model will repeat whatever range is printed and call anything under it normal. While reading, I understood that this single number hides a lot, which is what the next sections are about.

## Normal depends on age

I first read about age-specific ranges in Morgan et al. while doing my literature notes, and I went back to the older paper they compare with. Oesterling and colleagues measured PSA in 471 men with no sign of prostate cancer in Minnesota, and proposed different PSA limits for different age groups, based on the 95th percentile ([JAMA, 1993, vol. 270, pages 860 to 864](https://pubmed.ncbi.nlm.nih.gov/7688054/)).

Morgan and colleagues then studied American military men, with 1,673 Black men and 1,802 white men without cancer, and 411 Black men and 1,372 white men with cancer ([NEJM, 1996](https://doi.org/10.1056/NEJM199608013350502), [summary with the numbers](https://www.cancernetwork.com/view/new-psa-values-better-detect-prostate-cancer-black-men)).

They took the age ranges proposed by Oesterling, which came mostly from white men, and checked what happens when you use them for Black men. They found that 41% of the cancers in Black men would have been missed because the PSA of these men was still under the limit for their age. So they calculated new limits for Black men. These are lower than Oesterling's in the 40s and 70s.

After that, I looked for similar studies in Cameroon, but I could not find any that gave PSA limits by age for healthy men. I then found a study from Lagos, Nigeria, on apparently healthy civil servants who went for routine checkups ([Nigerian Journal of Surgery, 2016](https://pubmed.ncbi.nlm.nih.gov/27013850/)). Their limits are higher than both American studies, and the studies did not all calculate their limits in the same way, which honestly confused me a bit.


| Age      | Oesterling 1993 (USA, 95th percentile) | Morgan 1996 (Black men, USA, 95% sensitivity) | Lagos 2016 (Nigeria, 95th percentile) |
| -------- | -------------------------------------- | --------------------------------------------- | ------------------------------------- |
| 40 to 49 | 2.5                                    | 2.0                                           | 4.78                                  |
| 50 to 59 | 3.5                                    | 4.0                                           | 5.47                                  |
| 60 to 69 | 4.5                                    | 4.5                                           | 8.93 (reported for ages 60 to 70)     |
| 70 to 79 | 6.5                                    | 5.5                                           | Not reported for this age group       |


All values are in ng/mL. I found the Oesterling and Morgan values shown side by side on [this page](https://www.blackhealth.org/articles/psa-levels-by-age-black-men/), which says that these ranges are old and should not be used alone to decide what to do next. I have checked the Oesterling values in the abstract of the original paper, but I still haven't seen the original Morgan table myself.

The Oesterling and Lagos ranges show what was common in men who seemed healthy, while Morgan's limits were chosen to find 95% of cancers in Black men. So they do not answer the same question. This is one of the points I want the urologist to decide for my tests.

I looked for a study with reference values for Cameroonian men and I didn't find one.

## What the guidelines say about the next step

I wanted to know what a doctor would usually do after a result, because I believe a good answer from the model should point in the same direction. The American Urological Association guideline says that a newly raised PSA should be repeated before going further, that screening can start at 40 to 45 for men of Black ancestry, and that a rising PSA alone should not be the only reason for more tests ([AUA/SUO guideline page](https://www.auanet.org/guidelines-and-quality/guidelines/early-detection-of-prostate-cancer-guidelines), [summary from the AUA 2023 meeting](https://www.urotoday.com/conference-highlights/aua-2023/aua-2023-prostate-cancer/143971-aua-2023-aua-guidelines-early-detection-of-prostate-cancer.html)). The same guideline says that above 50 ng/mL, when there is no infection or another clear cause, a doctor may skip the biopsy if the biopsy is risky or if treatment is urgent. A biopsy is when small pieces of the prostate are taken with a needle to look for cancer under a microscope.

The [European guideline](https://uroweb.org/guidelines/prostate-cancer/chapter/diagnostic-evaluation) uses an approach based on the first PSA. Men with a PSA above 1 at 40 or above 2 at 60 may be followed every two years. It recommends early testing from 45 for men of African descent. It also says that a PSA between 3 and 10 in a man without symptoms and without a suspicious rectal exam should be repeated after about four weeks before more tests. The repeat should use the same lab and should be done without a urine infection, recent ejaculation or recent manipulation of the prostate.

## Medicines that lower the PSA

In my literature notes I wrote that finasteride lowers PSA by about half after several months of treatment, and I wanted to see where that came from. I found it in a large study called the Prostate Cancer Prevention Trial ([Thompson et al., NEJM, 2003](https://doi.org/10.1056/NEJMoa030660)). The men in this study were split into two groups. One group took finasteride every day, and the other took a placebo, which is a pill that looks the same but has no medicine in it, so the researchers could compare the two groups. Because finasteride lowers PSA, the trial multiplied the PSA values in that group by 2.0 at first, and by 2.3 after year four, to help decide who should have a biopsy (the factor is described in [this paper](https://urology.med.ubc.ca/files/2007/09/finasteride-chemoprevention1.pdf)). A later analysis of the same trial found that the factor needed grew from 2 at 24 months to 2.5 at 7 years ([Journal of Urology, 2005](https://pubmed.ncbi.nlm.nih.gov/16093979/)). These are adjustments used to read the result. They are not the man's real measured PSA.

What surprised me most here is that the small dose of finasteride sold for hair loss also lowers the PSA. A study of 355 men aged 40 to 60 found that 1 mg of finasteride a day lowered PSA after 48 weeks. The median drop was 40% in men aged 40 to 49 and 50% in men aged 50 to 60. The authors said that doctors should also adjust PSA results in men taking this dose for hair loss ([PubMed](https://pubmed.ncbi.nlm.nih.gov/17196507/)). While reading about this, I also came across dutasteride, another medicine from the same family as finasteride, which is often given to older men whose prostate has grown larger. It lowers the PSA in a similar way. The [European guideline](https://uroweb.org/guidelines/prostate-cancer/chapter/diagnostic-evaluation) says that finasteride and dutasteride lower PSA by about 50%.

The fictional lab reports in my tests do not have a line for medicines, which is why this matters for my [fifth hypothesis](01-hypotheses.md).

## Free PSA

Free PSA is a second measure that some labs add. In the blood, part of the PSA is attached to other proteins and part is not. The part that is not attached is called free PSA. The lab can then calculate what percentage of the total PSA is free.

Catalona and colleagues studied 773 men with a total PSA between 4 and 10 and a rectal exam that did not feel suspicious ([JAMA, 1998](https://pubmed.ncbi.nlm.nih.gov/9605898/)). They found that a lower percentage of free PSA goes with a higher risk of cancer. A rule using 25% free PSA or less would have found about 95% of the cancers and avoided about 20% of unnecessary biopsies. It took me a moment to understand that the 95% describes how many cancers the rule catches, and it does not mean that a man under 25% has a 95% chance of cancer.

A [report of their presentation](https://www.cancernetwork.com/view/percent-free-psa-test-may-prevent-unnecessary-biopsies) gives an example that helped me. With a total PSA of 6, a man with 10% free PSA had about a 50% chance of cancer, and a man with 30% had about 10%. These are examples from that group, not exact risks for every man. The same report says the 25% limit was set with one specific lab test, so it may not apply exactly to others. In my tests, I will only use the findings of this study for reports where the total PSA is between 4 and 10.

## PSA over time

My [third hypothesis](01-hypotheses.md) is about a rising PSA where each value looks normal, so I wanted to know how much doctors rely on the change over time. I learned that they look at it in two ways. The first is the PSA velocity, which is how much the PSA goes up each year. For example, 1.9, then 2.7, then 3.6 over four years is a rise of about 0.4 per year. The second is the doubling time, which is how long the PSA takes to double. My first feeling was that a PSA going up fast must be worrying, but the studies I found are more careful about that.

In the United States, Inman and colleagues followed 11,872 men from 1993 to 2005 ([BJU International, 2012](https://urotoday.com/recent-abstracts/urologic-oncology/prostate-cancer/49206-an-examination-of-the-dynamic-changes-in-prostate-specific-antigen-occurring-in-a-population-based-cohort-of-men-over-time-abstract.html)). A single PSA value predicted future cancer better than the velocity or the doubling time, and adding them to the PSA barely helped. Vickers and colleagues looked at 5,519 men from the prevention trial I mentioned earlier who all had a biopsy, and adding the velocity only improved the prediction a little ([Journal of the National Cancer Institute, 2011, summary](https://www.healio.com/news/hematology-oncology/20120325/psa-velocity-may-not-contribute-to-prostate-cancer-screening-process)). They concluded that a fast rise alone should not lead to a biopsy. The AUA guideline says something similar, since a rising PSA should not be the only reason to order more tests. I understand this as doctors still looking at the rise together with everything else.

This changed a little bit how I think about my test. I will not expect the model to say "this is cancer" because the values go up. I will check whether it notices the rise at all, and whether it suggests showing the whole series to a doctor. The values in my data from the CARET study were mostly measured about one year apart, sometimes more, so my series of reports will certainly use the real dates of each man.

## Things that raise the PSA for a while

I learned that the PSA can go up for a short time for reasons that have nothing to do with cancer. These include ejaculation, vigorous exercise such as cycling, a urine infection, urine retention, a biopsy or another procedure on the prostate.

According to [Cancer Research UK](https://www.cancerresearchuk.org/health-professional/diagnosis/investigations/psa-testing/patients-with-symptoms), ejaculation and vigorous exercise should be avoided for 48 hours before the test. It advises waiting at least six weeks after a urine infection has gone away, and at least six weeks after a biopsy or another procedure on the prostate.

I found different advice about a rectal exam. Some lab pages say to take the blood before the exam or wait after it, but the current [European guideline](https://uroweb.org/guidelines/prostate-cancer/chapter/diagnostic-evaluation) says that a rectal exam does not affect the PSA value. Because of that, I should not assume that a raised PSA was caused by a rectal exam.

The American NHANES survey, whose data I may use later, did not measure the PSA of men who had a rectal exam in the past 7 days, a biopsy or a cystoscopy in the past 4 weeks, or a prostate infection at that moment ([NHANES PSA_F documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2009/DataFiles/PSA_F.htm)). A cystoscopy is an exam where a small camera goes into the bladder. This was the rule used for that survey, but it does not prove that a rectal exam raises PSA enough to explain a high result.

When a report mentions one of the other situations, I would expect a good answer to suggest repeating the test later under better conditions, without alarming the family.

## Very high values and Cameroon

In my literature notes I wrote about a study from Douala where the average PSA at diagnosis was around 43, and I said I took it with some caution because of the publisher. While preparing this file I found a study by Dr Mbouché and colleagues on 232 men who had a prostate biopsy in Yaoundé ([African Urology, 2024](https://africanurology.com/index.php/au/article/view/125)). The PSA of these men went from 4 to 49,700 ng/mL, with a median of 45. A median of 45 means that half of them had a PSA above 45 and half had a PSA below 45. That is more than ten times the printed limit of 4.

Cancer was found in 147 of the 232 men, and 131 of these 147 cancers were classed as high-risk. I have to be careful with these numbers because these men had already been sent for a biopsy, so they do not represent all men in Cameroon. Still, in this group, many men reached the biopsy with a very high PSA.

The AUA guideline says that when PSA is above 50, with no infection or another clear cause, a doctor may sometimes skip the biopsy if the biopsy is risky or if treatment is urgent. It does not say that every PSA above 50 should skip biopsy. For my tests, a very high value is the case where I expect the clearest and fastest answer.

## The urgency levels I want to propose

To test my [second hypothesis](01-hypotheses.md), I need a way to say whether the urgency in an answer fits the result. I'm proposing three levels. These are draft levels for scoring model answers, not medical rules. They assume that the man has no new symptoms and has not already been diagnosed with prostate cancer.

I am giving each case one fixed level so I can still run the tests if I do not get an answer from the urologist. I can change the levels later if he corrects them.

| Level | What I mean | Examples of situations I would put here |
| ----- | ----------- | --------------------------------------- |
| 1 | Continue the usual follow-up | A low value for the age, with nothing unusual on the report |
| 2 | Show the result to a doctor in the next few weeks, often to repeat the test | A new value close to or above a limit, a result that needs adjustment because of finasteride, or a rising series |
| 3 | See a doctor in the next few days | A very high value, for example several times above the printed limit |

There is one safety rule outside these three levels. Severe back pain with new weakness or numbness in the legs, trouble walking, loss of bladder or bowel control, complete inability to urinate, or a high fever with urinary symptoms needs urgent medical help on the same day. In that situation, the symptoms matter more than the PSA level ([Prostate Cancer UK](https://prostatecanceruk.org/prostate-information-and-support/advanced-prostate-cancer/metastatic-spinal-cord-compression-mscc), [Cancer Research UK](https://www.cancerresearchuk.org/health-professional/diagnosis/investigations/psa-testing/patients-with-symptoms)).

## Example cases

These are the cases I would like the urologist to check one by one. The values are close to what I will use in the fictional reports, and my expected answers are my own reading of the sources above. For now, I will use the fixed levels below.

| # | Man | What the report shows | What the printed range says | What I expect a good answer to say | My proposed level |
| - | --- | --------------------- | --------------------------- | ---------------------------------- | ----------------- |
| 1 | 52 years old | PSA 3.8 | Normal (< 4) | Mentions that the value is above some limits used for this age, and suggests talking to a doctor and repeating the test | 2 |
| 2 | 65 years old, finasteride 5 mg for 3 years | PSA 2.5 | Normal | Explains that finasteride lowers PSA. A rough adjustment gives about 5, but this is not the real measured value and a doctor should also look at older results | 2 |
| 3 | 56, 58 and 60 years old | 1.9, then 2.7, then 3.6, two years apart | Normal each time | Notices that the value keeps rising and suggests showing the full series to a doctor, without saying that the rise alone means cancer | 2 |
| 4 | 62 years old | PSA 6.0 with free PSA 30% | High (> 4) | Explains that 30% free PSA is less worrying than a low percentage, but it does not rule out cancer and the raised total PSA should still be discussed with a doctor | 2 |
| 5 | 62 years old | PSA 6.0 with free PSA 8% | High (> 4) | Explains that a low free PSA makes the result more worrying and that it should be discussed with a doctor, but does not call it an emergency from this result alone | 2 |
| 6 | 70 years old | PSA 45 | High (> 4) | Says clearly that the value is very high and needs a doctor in the next few days, while remembering that PSA alone does not prove cancer | 3 |
| 7 | 60 years old | PSA 0.8 | Normal | Says the value is low and does not alarm the family, while avoiding the claim that a low PSA makes cancer impossible | 1 |
| 8 | 75 years old | PSA 5.0 | High (> 4) | Mentions that PSA often rises with age, but does not dismiss the printed high result. Suggests discussing it with a doctor, who can also consider health, symptoms and life expectancy | 2 |
| 9 | 58 years old, blood taken two days after a rectal exam | PSA 4.6 | High (> 4) | Does not assume that the rectal exam caused the rise. Suggests discussing the result and repeating the PSA after about four weeks under standard conditions | 2 |

## Where the sources don't agree

The ranges are the first problem. The Lagos limits are higher than Morgan's, but the two studies chose their limits for different reasons. I still do not know which approach fits a Cameroonian man best.

I also found different advice about the rectal exam. Some lab pages say to wait after it, while the European guideline says that it does not affect PSA. For my scoring, I will follow the European guideline and will not accept the rectal exam as the only explanation for a raised PSA.

The papers on PSA over time also make me unsure how strongly a rising series should be flagged. For now, I will expect the model to notice the rise and suggest showing it to a doctor, but not to use the rise alone to say that there is cancer or that a biopsy is needed.

## Questions for Dr Mbouché

I would like to ask him which limits he would use in his own practice for a Cameroonian man of 50, 60 and 70 years old. I also want to know from what rise between two tests he would start to worry, and which information missing from a report would change his reading the most. I would ask him whether my three urgency levels and the time given for each level make sense, and whether he would change the level of any of the cases above. My last question is whether a model that answers "normal" for case 1 is wrong, incomplete or acceptable in his opinion.

## What happens next

I'm going to send a short summary of this file to Dr Mbouché with an email. While I wait for his answer, I will prepare the data and the fictional reports. If I do not get an answer before I run the tests, I will use the fixed levels in this file and clearly say that they are my draft scoring rules. I will update this file if he sends corrections later.