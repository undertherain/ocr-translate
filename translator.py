# translator.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class Translator:
    """
    A class to handle loading the translation model and performing translations.
    The model is loaded during initialization to be reused across requests.
    """

    def __init__(self):
        print("Initializing translator...")
        model_id = "liquidAI/LFM2-350M-ENJP-MT"

        # This architectural decision places the model on the best available hardware.
        if torch.cuda.is_available():
            print("✅ GPU detected. Loading model on GPU.")
            device_config = {"device_map": "auto", "torch_dtype": torch.bfloat16}
        else:
            print("⚠️ No GPU detected. Loading model on CPU (this might be slow).")
            device_config = {"device_map": "cpu", "torch_dtype": torch.float32}

        try:
            self.model = AutoModelForCausalLM.from_pretrained(model_id, **device_config)
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            print("✅ Translator initialized successfully.")
        except Exception as e:
            print(f"❌ Error during translator initialization: {e}")
            raise

    def translate(self, japanese_text: str) -> str:
        """
        Translates a single Japanese sentence into English.
        """
        messages = [
            {"role": "system", "content": "Translate to English."},
            {"role": "user", "content": japanese_text},
        ]

        input_ids = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(input_ids, max_new_tokens=256)

        # Slicing the output tensor removes the input tokens for a clean decoding.
        new_tokens = outputs[0][len(input_ids[0]) :]
        translation = self.tokenizer.decode(new_tokens, skip_special_tokens=True)

        return translation.strip()
