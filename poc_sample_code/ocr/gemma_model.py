from transformers import pipeline
import torch

pipe = pipeline(
    "image-text-to-text",
    model="google/gemma-3-27b-it",
    device="cpu",
    torch_dtype=torch.bfloat16,
    # add access details here 
)

messages = [
    {
        "role": "system",
        "content": [{"type": "text", "text": "You are a helpful assistant who can read cursive as well printed handwritten text."}]
    },
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "file://sample_images/Sample Form.png"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    }
]

output = pipe(text=messages, max_new_tokens=200)
print(output[0]["generated_text"][-1]["content"])
