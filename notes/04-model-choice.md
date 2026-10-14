# Ny Model choice

The challenge asked me to write an open model between 0.6 and 6 billion parameters that behaves like current frontier models and that I can run myself. I have chosen two models, one medical, and one general, as I want to test whether a model trained for medicine reads a PSA report better than a general model of the same size.

## The main one: MedGemma 1.5 4B

[MedGemma 1.5 4B](https://huggingface.co/google/medgemma-1.5-4b-it) is a medical model by Google, based on Gemma 3, that has about 4 billion parameters. It accepts images and text, so I can send it a photo of a report directly. The model card for this model states that it can read lab reports and extract values and units from them, which is exactly what I need to do.

In my literature notes I wrote that its technical report tests this mostly on PDF reports, plus 14 report images, and that the task was to extract values and not to explain what they mean for a specific man. So I'm testing it on something close to what it claims to do, but in the conditions of a family, with a phone photo, WhatsApp compression and missing information. If a model made for medicine fails there, I think the blind spot is more convincing than with a general model.

Its card also says it was not tested on conversations with several messages and that it is more sensitive to the way the prompt is written than Gemma 3. I will keep the same prompt for every report so this doesn't change my results. To download it, I have to accept the Health AI Developer Foundations terms on Hugging Face.


## The comparison model: Qwen3-VL 4B

[Qwen3-VL-4B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) is a general model from Alibaba of about the same size, which also reads images, under the Apache 2.0 licence. I picked it because Google itself puts it next to MedGemma 1.5 in its technical report, even if they couldn't run all their tests with it. Comparing the two should tell me if the medical training helps, or if both models make the same mistakes.

## What I still need to check

I don't know yet if MedGemma runs well on the free GPU of Colab. I will check it during the pilot on a few reports, and if it doesn't fit, I'll try a smaller precision or another free GPU.