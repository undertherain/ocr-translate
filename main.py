# main.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    """
    Manually loads the model and tokenizer to translate a sample Japanese sentence,
    running on GPU if available, otherwise defaulting to CPU.
    """
    # 1. Configure Model and Device
    # This uses the specific English-Japanese translation model.
    model_id = "liquidAI/LFM2-350M-ENJP-MT"

    # Set device and data type based on hardware availability.
    if torch.cuda.is_available():
        print("✅ GPU detected. Using CUDA with bfloat16.")
        device_config = {"device_map": "auto", "torch_dtype": torch.bfloat16}
    else:
        print("⚠️ No GPU detected. Using CPU with float32.")
        device_config = {"device_map": "cpu", "torch_dtype": torch.float32}

    # 2. Load Model and Tokenizer
    # This architecture directly uses the core transformer classes.
    try:
        model = AutoModelForCausalLM.from_pretrained(model_id, **device_config)
        tokenizer = AutoTokenizer.from_pretrained(model_id)
    except Exception as e:
        print(f"❌ Error loading the model or tokenizer: {e}")
        return

    # 3. Prepare the Prompt
    # We create a structured prompt with a system instruction and the user's text.
    japanese_sentence = "こんにちは、世界！"
    messages = [
        {"role": "system", "content": "Translate to English."},
        {"role": "user", "content": japanese_sentence},
    ]

    # `apply_chat_template` formats the input correctly for the model.
    input_ids = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to(
        model.device
    )  # Move tokenized input to the same device as the model

    # 4. Generate the Translation
    # `model.generate` performs the inference. Using greedy decoding (default)
    # is best for translation.
    outputs = model.generate(input_ids, max_new_tokens=256)

    # The output tensor includes input_ids, so we slice them off to decode only the new tokens.
    new_tokens = outputs[0][len(input_ids[0]) :]
    translation = tokenizer.decode(new_tokens, skip_special_tokens=True)

    # 5. Print the Result
    print("-" * 30)
    print(f"Japanese Original:   {japanese_sentence}")
    print(f"English Translation: {translation}")
    print("-" * 30)


if __name__ == "__main__":
    main()
