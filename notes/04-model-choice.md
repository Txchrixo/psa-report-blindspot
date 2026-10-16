# Model choice

The challenge asked me to pick an open model between 0.6 and 6 billion parameters that behaves like the current frontier models, and that I can run myself. I chose two models. The main one is a general model, because that is the kind of assistant a family would use. The second one is a medical model, to see if a model made for medicine does better on the same reports.

## The main one: Qwen3-VL 4B

[Qwen3-VL-4B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) is a general model from Alibaba with about 4 billion parameters, under the Apache 2.0 licence. It reads images and answers like a chat assistant. When my aunt shared the photo of my uncle's results, the AI someone in the family could have asked is ChatGPT, Gemini or Meta AI inside WhatsApp. These are general assistants, and Qwen3-VL is the closest to them that I can load myself. Google also puts it next to MedGemma 1.5 in its technical report, even if they couldn't run all their tests with it.

## The comparison model: MedGemma 1.5 4B

[MedGemma 1.5 4B](https://huggingface.co/google/medgemma-1.5-4b-it) is a medical model by Google, built on Gemma 3, with about 4 billion parameters. It also accepts images. Its model card says it can read lab reports and extract the values and units, which is close to my task.

In my literature notes I wrote that its technical report tests this mostly on PDF reports, plus 14 report images, and that the task was to extract values and not to explain them for a specific man. So I test it in the conditions of a family, with a phone photo, WhatsApp compression and missing information. Its card also says it is more sensitive to the way the prompt is written than Gemma 3, and that it was not tested on conversations with several messages. I keep the same prompt for every report. To download it I accepted the Health AI Developer Foundations terms on Hugging Face.

The two models differ in many ways. They come from different companies, and Qwen looks at the image in much more detail (about 3,500 input tokens against about 290 for MedGemma). So if they answer differently, I can't say that the medical training is the reason. I can only describe how each one behaves.

## Why the main model changed

In my first plan MedGemma was the main model and Qwen was the comparison. After the pilot I swapped them. MedGemma made big mistakes, like saying that 3.80 is above 4.00, but a family is unlikely to use a medical model like this one. Qwen made quieter mistakes. It said "normal, pas grave" for 3.80 at 52, and it read the finasteride note without changing its conclusion. This is the comforting answer without all the data that I wrote about at the very beginning, so I want it at the center of the study.

## Where they run

Both models load in bfloat16 and use about 9 GB of GPU memory (8.6 GB for MedGemma, 8.9 GB for Qwen). I don't use float16 because Gemma 3 models give broken answers in it, and I don't use a smaller precision because then I wouldn't be testing the models as they are published. In the pilot MedGemma ran on a T4 and Qwen on an L4. For the full run both run on an L4 with transformers 5.20, so they are in the same conditions.