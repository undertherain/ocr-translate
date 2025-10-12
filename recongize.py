# inference.py (Updated with Robust Method)

from pathlib import Path

import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor


def perform_ocr(model_id: str, image_path: Path) -> str:
    """
    Loads the model and performs OCR on the given image using an explicit
    multi-modal processing approach.
    """
    if not image_path.is_file():
        raise FileNotFoundError(f"Image file not found at: {image_path}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    print(f"📦 Using device: {device} with dtype: {dtype}")

    print(f"📚 Loading processor from {model_id}...")
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    print(f"🧠 Loading model from {model_id}...")
    model = AutoModelForImageTextToText.from_pretrained(
        model_id,
        torch_dtype=dtype,
        trust_remote_code=True,
    ).to(device)

    image = Image.open(image_path).convert("RGB")

    # Define the conversation WITHOUT the final empty assistant message.
    # We will let add_generation_prompt=True handle it.
    system_message = (
        "You are an expert OCR model specializing in recognizing Japanese text, "
        "including handling furigana annotations correctly."
    )
    user_prompt = (
        "Recognize all the Japanese text in this image. For any kanji that has furigana "
        "above it, please format it in Markdown as `[漢字]{かんじ}`. Present the entire "
        "recognized text in this Markdown format. Return only the recognized text."
    )
    messages = [
        {"role": "system", "content": [{"type": "text", "text": system_message}]},
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": user_prompt},
            ],
        },
    ]

    # 1. First, format the prompt text using the template.
    prompt_text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    # 2. Then, call the processor with the text AND the image.
    # This guarantees that both modalities are processed correctly.
    inputs = processor(text=prompt_text, images=image, return_tensors="pt").to(device)

    # `inputs` is now guaranteed to be a dictionary with 'input_ids' and 'pixel_values'
    print(f"✅ Input successfully processed. Keys: {inputs.keys()}")

    # 3. Generate the response. This will now work correctly.
    print("\n🚀 Performing OCR...")
    generation_output = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False,
    )

    generated_text = processor.batch_decode(
        generation_output, skip_special_tokens=True
    )[0]

    # The output cleanup is simpler now
    final_output = generated_text.split(prompt_text)[-1].strip()

    return final_output


if __name__ == "__main__":
    MODEL_ID = "blackbird/lfm2-vl-furigana-ocr"
    IMAGE_FILE = Path("example.png")

    if not IMAGE_FILE.exists():
        print(f"⚠️  '{IMAGE_FILE}' not found. Please provide your image.")
    else:
        try:
            recognized_text = perform_ocr(MODEL_ID, IMAGE_FILE)
            print("\n" + "=" * 50)
            print("✅ OCR Result:")
            print(recognized_text)
            print("=" * 50)
        except Exception as e:
            print(f"\nAn error occurred: {e}")
