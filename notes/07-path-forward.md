# Path forward

What I write here is only my opinion. I didn't test any of it, I'm not a doctor and I have never trained a model myself. But after reading all the answers one by one, I have some ideas of what could help close the gap. And also some things that I think more data won't fix.

## What should be fixed

The 2 models don't make the same mistake, so I don't believe one fix would work for both of them.

MedGemma gets lost on a very simple comparison. When I ask it in text only, it knows that 3.80 is under 4.00. But once it has to read the number from the image and explain it, it said the opposite in 30 of the 45 answers where the value was under the limit.

Qwen on the other hand reads the limit right, and then it stops there. A value under "< 4.00" becomes "normal, pas de cancer", even when the age of the man, his medicine or his older results tell you a doctor should look at it.

And none of them asks before answering. They asked me something in 1 or 2 answers out of 86. On the finasteride reports, just one question about medicines would have changed the whole answer.

## The data I would build

I think the most useful thing would be report explanations made together with doctors. Not explanations for a lab, but for a family that receives the result and doesn't know what to do with it.

First, reports in pairs like mine, but a lot more of them. Two reports where only one thing changes. 3.80 against 4.20, with or without finasteride, the same value alone or with three older ones, a man of 52 and a man of 72. For each one, a urologist writes the answer or at least checks it. My idea is that pairs show the model that a small detail can change everything, and that is what both models missed in my tests. I don't really know how many pairs would be needed. My guess is a few thousand to start, maybe 2,000 to 3,000, and each answer checked by at least 2 urologists so that we see when they don't agree.

Then the formats we really get here. French and English, ng/mL and µg/L, the decimal comma, age tables, biochemistry printed before the PSA... And phone photos sent on whatsapp, because that's how my aunt shared my uncle's result with us. My photos didn't make the models misread the number, but they were all readable. So the set should also have really bad photos, where the right answer is simply "I can't read this number".

The answers should also say what the report can't show. Most good answers I imagine start the same way. The value is under the printed limit, yes, but this limit doesn't know his age, his medicines or his older results. And they should never say "no cancer" from a PSA alone. Not in one direction, not in the other.

I also think real reports from labs in Douala would help, because they would show layouts and mistakes I can't imagine. My fictional reports were enough to find the gap, but not to cover everything. Real ones would have to be anonymised and shared with consent, with an ethics review. That's not something I would do alone, it should be done with a hospital.

## How I would train

For a 4B model, I think starting with a small LoRA fine-tuning on these pairs would be enough. After that, a preference step where the model sees a good answer and a bad answer for the same report. For 3.80 at 52, the good one says the value is under the printed limit but above some limits used for his age, and it suggests a doctor and a new test. The bad one says "normal, pas grave, pas de cancer", which is very close to what Qwen wrote me. I hope this would teach Qwen to not stop at the printed limit.

And I wouldn't have to invent the bad answers, I already have them. In my 172 scored answers there are a lot of real mistakes, like "Pas de cancer de la prostate" for 3.80 at 52, or finasteride called "a benefit of the medication". These would be the bad examples, and a urologist would write the good version of each one. After the training, my grid would tell if it worked or not. No more false reassurance, the value on the right side of the limit, and a question when a note is missing. So the fix would come directly from what I measured, and I could check it with the same columns.

About asking questions, I don't think it is enough to add "ask if something is missing" in the prompt. When I read the MediQ paper for my literature notes, they found that just telling the model to ask made the results worse. It worked better when the model first checks if it has enough information. So I would rather train on examples where the good answer gives what it can, then asks one or two short questions ("Does he take a medicine for the prostate?", "Do you have his older results?") and says how the answer would change with the reply.

## Changing how the answer is built

For MedGemma's mistake I'm not sure more training is the right way. Comparing two numbers is easy for a computer, but I can't trust this model to do it. So I would cut the work in two. First the model only reads the report and writes down what is on it, the value, the unit, the printed limit, the age, the notes and the older values. Then a small piece of code does the comparison and the obvious checks, like the unit or a rise between two results. Only after that, the model writes the explanation with these facts in front of it. It looks a bit like the first step MedRepBench asks the models to do, except that here the explanation still has to go further than the printed range.

There is also a simpler idea that doesn't need any training. Instead of hoping the model learned the rules, give them to it when it answers. A short text written with doctors, with the limits used by age, what finasteride does to the PSA and when a rise between 2 results should worry, added to every question. The model would still have to read and explain, but at least it wouldn't have to remember everything by itself.

## What more data won't fix

Some things are not really a model problem.

Nobody could give me a clear "normal" PSA for a Cameroonian man of 50, 60 or 70. The limits for Black men in Morgan et al. come from American men, and the Lagos study chose its limits for another reason. If doctors haven't agreed on a limit yet, a model can't learn it.

A report doesn't say if the man takes finasteride either. If it isn't printed, training won't change anything, the model has to ask.

And my urgency levels are my own drafts. Before anyone trains a model on them, urologists need to check them, and I would want more than one or two doctors to agree.

## How I would know it worked

I would run my 43 reports and my photos again, with the same grid, and add new reports that were never used for training. For me it worked if MedGemma almost stops putting the value on the wrong side of the limit, if Qwen stops saying "pas de cancer" on reports that need a doctor, and if both of them ask about medicines when it matters. I would also want a doctor to score part of the answers this time, since I was the only one checking the scores.
