"""
Global configuration for NeuroAid OSS.
Central place for model, endpoint, and metadata settings.
"""

import os


MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss:20b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
ENDPOINT = f"{OLLAMA_URL}"  # base URL for Ollama


REPO_URL = "https://github.com/your-org/NeuroAid-OSS"
DEMO_URL = "https://youtube.com/your-demo-link"


TIMEOUT = 60  # seconds for requests
TEMPERATURE = 0.2
RETRIES = 3
BACKOFF_FACTOR = 2
