# Hypotheses

This is before any paper-reading or experimentation. I'm not a doctor, and I'm not too familiar with PSA yet... so I'm probably going to guess wrong on a lot of these. That's OK! I want to see where I was wrong too.

**My first guess is simple.** I think the model will basically just echo what the report says. If a value is within the range printed on the report, it will call it "normal" and be done with it. Or at least, I don't know if "normal" is normal for everyone. Maybe it depends on age or other things, but I don't think the model will ask.

**My second guess** is that it will always end with "please see a doctor" or something like that. This is good, but if you get the same sentence for a low value and a very high value, it doesn't really help a family know whether to do something this week or a year later. I want to see whether it changes its advice or always gives the same sentence.

**Third,** my uncle had results from several years, not just one report. I think that if you give the model a few reports where all the numbers look OK but keep going up, it will look at each report individually and say everything is OK. Maybe a person looking through them would notice the trend.

**Fourth,** the picture I got from my aunt was not a clear PDF. It was a photo of a paper report. I think a blurry photo or one compressed by WhatsApp could lead the model to read a number incorrectly. I think it will answer with the same confidence, without saying, "I'm not sure I can read this."

**Last one.** A lab report doesn't contain the patient's full history: their medications, sometimes their age, or other results. I think the model will answer anyway, without asking about what's missing. As I said: **"A comforting answer, but without all the data."**

If the tests show that I'm wrong on some points, that's a result too. I'll come back to this file at the end.

## What I found

After scoring everything, here is where I was right and wrong. The numbers are in [notes/results](06-results.md).

**First guess.** Right for Qwen. When the value was under the printed limit but a doctor was still needed, it called the result normal in 19 of 26 answers. It used the age a lot, but mostly to reassure. MedGemma did something I didn't expect. It put a value under the limit on the wrong side in 30 of 45 answers.

**Second guess.** Half right. Almost every answer says to see a doctor, as I thought. Qwen changes the urgency with the value, but it said there was nothing to do in 12 of 54 answers that needed a doctor. MedGemma gave nearly the same advice for 0.80 and for 45.

**Third guess.** Wrong for Qwen, which saw the rise every time, even if it sometimes put it on age. Closer to right for MedGemma, which saw it in 3 of 8 answers.

**Fourth guess.** Mostly wrong. The photos didn't make the models misread the PSA. It's true that no model said a photo was hard to read, but the photos were readable, so I can't conclude much there. The mistakes on the photos are the same as on the files.

**Last one.** Right for both. They asked me something in 1 or 2 answers out of 86, and no model used the finasteride or the rectal exam note well. Qwen gave the same "nothing to do" with or without the finasteride note.
