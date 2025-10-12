# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from translator import Translator

# --- API Setup ---
app = FastAPI(
    title="Japanese to English Translation API 🤖",
    description="An API using the liquidAI/LFM2-350M-ENJP-MT model.",
    version="1.0.0",
)


# --- Pydantic Models for Data Validation ---
class TranslationRequest(BaseModel):
    text: str


class TranslationResponse(BaseModel):
    translation: str


# --- Model Loading ---
# This instantiates the translator. The model is loaded once on server startup.
try:
    translator = Translator()
except Exception as e:
    # If model loading fails, the server shouldn't start.
    raise RuntimeError(f"Failed to initialize the translator: {e}") from e


# --- API Endpoints ---
@app.get("/", tags=["General"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Translation API is running"}


@app.post("/translate", response_model=TranslationResponse, tags=["Translation"])
def translate_text(request: TranslationRequest):
    """
    Receives Japanese text and returns the English translation.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        english_translation = translator.translate(request.text)
        return {"translation": english_translation}
    except Exception as e:
        # This catches any errors during the translation process.
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
