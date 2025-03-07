from transformers import pipeline

pipe = pipeline("image-text-to-text", model="meta-llama/Llama-3.2-11B-Vision-Instruct")
pipe("https://huggingface.co/datasets/Narsil/image_dummy/raw/main/parrots.png", text="A photo of")