from . import processor, model

# image = "https://huggingface.co/datasets/hf-internal-testing/fixtures_got_ocr/resolve/main/image_ocr.jpg"
def get_text(image_dir):
    image = image_dir
    inputs = processor(image, return_tensors="pt").to("cpu")

    generate_ids = model.generate(
        **inputs,
        do_sample=False,
        tokenizer=processor.tokenizer,
        stop_strings="<|im_end|>",
        max_new_tokens=4096,
    )

    text = processor.decode(generate_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    return text