from transformers import AutoProcessor, AutoModelForImageTextToText

# device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForImageTextToText.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf", device_map="cpu")
processor = AutoProcessor.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf")