"""
Global configuration for NeuroAid OSS.
Central place for model, endpoint, and metadata settings.
"""

import os


MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss:20b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
ENDPOINT = f"{OLLAMA_URL}" 


REPO_URL = "https://github.com/ayondalai7/neuroaid-oss"
DEMO_URL = "https://youtu.be/HKw9If2fOac"


TIMEOUT = 60  
TEMPERATURE = 0.2
RETRIES = 3
BACKOFF_FACTOR = 2
