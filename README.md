# Screenshot to OCR to translate for linux desktop

## Set up screenshot tool

Create keyboard shortcut like ctrl+PrtSc associated with `ocr-translate.sh` script provided with this repo.
It is tested to work with Gnome Shell and Wayland, other compositors might require some massaging.

## Translation API and client

This project provides a high-quality Japanese-to-English translation service powered by the liquidAI/LFM2-350M-ENJP-MT language model. The service is exposed via a RESTful API built with FastAPI and is containerized with Docker for easy deployment. A simple command-line interface (CLI) is also included for direct terminal interaction.

## ✨ Features

    High-Quality Translation: Leverages a 350M parameter Hugging Face transformer model fine-tuned for Japanese-English translation.

    FastAPI Backend: A robust and fast API server with automatic interactive documentation.

    Dockerized Deployment: Includes Dockerfile and docker-compose.yml for a simple, one-command setup.

    Command-Line Interface: A convenient CLI client (cli.py) for using the translation service directly from your terminal.

    CPU/GPU Support: Optimized to run on a standard CPU but can be configured to leverage an NVIDIA GPU for enhanced performance.

## 📂 Project Structure

The repository is organized with a clear separation of concerns for the API, model logic, and deployment configuration.

.
├── docker-compose.yml  # Manages the containerized application
├── Dockerfile          # Blueprint for building the application image
├── main.py             # FastAPI server logic and API endpoints
├── cli.py              # Command-line client to interact with the API
├── translator.py       # Core logic for loading the model and translating
└── requirements.txt    # Python project dependencies

## 🚀 Getting Started

You can get the server running in just a few steps. The recommended method is using Docker, as it handles all dependencies and configuration automatically.

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for manual setup or running the CLI client)
- requests library for the CLI (pip install requests)

### Method 1: Using Docker (Recommended)

This is the simplest way to start the server.

- Clone the repository (if you haven't already).
- Build and run the container from the project's root directory:
 
```bash
    docker-compose up --build
```

The server will start after the model finishes downloading and loading. It is now accessible at http://localhost:8000.

### Method 2: Manual Local Setup

If you prefer to run the server without Docker:

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install dependencies:

```Bash
pip install -r requirements.txt
```

Start the server:
```Bash
    uvicorn main:app --reload
```

## 💻 Usage

Once the server is running, you can interact with it in two ways.

Interacting with the API

The API exposes a /translate endpoint that accepts POST requests.

Interactive Docs: Visit http://localhost:8000/docs in your browser for a user-friendly Swagger UI where you can test the endpoint directly.

cURL Example:

```Bash
curl -X 'POST' \
  'http://127.0.0.1:8000/translate' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "今日の天気は素晴らしいですね。"
}'
```

Response:
```JSON
{"translation":"The weather is wonderful today, isn't it?"}
```

Using the Command-Line Client (CLI)

The cli.py script lets you use the API from your terminal.

    Pipe input with echo:
    Bash

echo "神戸は美しい都市です。" | python cli.py

## Output: Kobe is a beautiful city.

Pipe a text file:
Bash

    cat your_file.jp | python cli.py

## 🛠️ Technology Stack

    Backend: FastAPI

    Machine Learning: PyTorch, Hugging Face Transformers

    Containerization: Docker & Docker Compose

    Model: liquidAI/LFM2-350M-ENJP-MT

## 💡 Hardware Note

This application is configured to run on a CPU by default, which makes it highly portable. However, translation performance will be significantly faster on a system with a CUDA-enabled NVIDIA GPU. To enable GPU support in Docker, you'll need the NVIDIA Container Toolkit and must uncomment the deploy section in the docker-compose.yml file.
