# NeuroAid OSS (Clean Demo)

Local-first cognitive companion powered by **gpt-oss:20b** (via Ollama).

## Quickstart
```bash
# 1) Pull model (separate terminal)
ollama pull gpt-oss:20b
ollama serve      # if not already running
ollama run gpt-oss:20b

# 2) Create venv & install
python -m venv .venv
./.venv/Scripts/python -m pip install -r requirements.txt

# 3) Run Streamlit
./.venv/Scripts/python -m streamlit run app/app.py
```
