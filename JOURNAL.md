# Journal

## 2026-10-12 (morning)

I made the repo, explained why I wanted to do it in `notes/00-why.md`, then wrote down my hypotheses before I read anything so I could compare what I found with what I wrote later. It was weird to be doing this so soon after my uncle died, but that's probably part of why I want to do it.

I started to look for what existed on this topic. I wrote down the keywords I used and the informations I found.

**I'm not done yet,** so tonight I'll continue to read, complete my notes on the literature, and try to figure out what is missing.

## 2026-10-12 (evening, finished after midnight)

I came back to the literature as planned tonight. In the morning I had only read Hugging Face and a few first papers, so tonight I searched with more precise words and read about photos of documents, about models that don't ask questions, and about PSA itself. It took me longer than I thought, and I finished after midnight.

First, the range of a "normal" PSA does not apply to everyone, it depends on age. I read this morning that there was a study with different ranges for black men. I didn't know that before reading this, and it makes the " 4" on a report look less reassuring. Second, a study said AI models gave fewer and fewer medical warnings, which is contrary to what I wrote in my second hypothesis. I'm leaving the hypothesis as is, because I wrote it before reading, but I will test both scenarios.

I also realized that I can't figure out on my own what the "right answer" is for my tests. I ould perhaps need a doctor to look at it, so tomorrow (today) I want to write down the medical references I found and send a message to a doctor. 

## 2026-10-13

Today, with the help of Perplexity to check facts and find information in papers, I wrote most of my clinical reference file. I started from what I had noted in the literature and went back to the sources to try to understand where the numbers come from. I was a bit confused when I found that the ranges from Lagos are higher than the American ones for Black men.

## 2026-10-13 (night, finished after 2 am)

Tonight I finished the clinical reference file. I went back to the sources I wasn't sure about. This time I opened the European guideline itself, and it says two things I didn't expect. A PSA between 3 and 10 should be repeated after about four weeks, and a rectal exam doesn't change the PSA, even though some lab pages say the opposite. I chose to follow the guideline.

I was also surprised that the small finasteride pill for hair loss lowers the PSA too, and that labs don't all print the same limit (Mayo Clinic prints 4.5 instead of 4).

I gave each of my nine cases a fixed level, so I can still run my tests if no doctor answers. I also added a safety rule for serious symptoms, because then the symptoms matter more than the PSA.

Then I made a two-page document in French and emailed it separately to five urologists who published on prostate cancer in Cameroon:
- Dr Frantz Guy Epoupa Ngalle (Hôpital Général de Douala)
- Dr Marcella Biyouma (Hôpital Laquintinie, Douala)
- Dr Cyril Kamadjou (Douala)
- Dr Jean Cédrick Fouda (Hôpital Central de Yaoundé)
- Dr Landry Oriole Mbouché (Yaoundé)

I also sent a short LinkedIn message to the ones I found there.

I only have about a day, so I'm not expecting much, but one answer would already help. If nobody replies, I'll keep my own levels and say it clearly in the README. Today I start on the data and the fictional reports.


## 2026-10-14 (morning)

I got the CARET data and downloaded it and converted it to CSV with a small Python script (thanks claude) which contains 683 blood draws from 141 men. As I was looking at it, I realized most of the draws are about one year apart and not two years apart as I thought, so I changed that in my notes. 

Man 49 caught my attention. His PSA went from 0.93 to 1.67, then 2.08, then 3.51 over about five years, and every single one was under 4, and he was diagnosed with prostate cancer soon after his last one. I think this is the type of case that I would use in my third hypothesis.