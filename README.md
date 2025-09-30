[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](#)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Ready-brightgreen)](#)

# 🧠 NeuroAid OSS — local-first grounding, CBT & journaling. Optional Ollama chat.

Most AI “mental health tools” send your thoughts to the cloud. **NeuroAid runs locally by default**: guided routines, journaling saved in JSON, and optional Ollama chat — all open-sourced under MIT.

---

## ✨ Features
- 📝 **Guided routines**: 5-4-3-2-1 Grounding, CBT reframing  
- 🔒 **Local-first journaling** (`/data/journal.json`)  
- ⚡ **Works offline** (no model required)  
- 🤖 **Optional Ollama integration** for chat (`MODEL_NAME` + `OLLAMA_URL`)  
- 🛠️ **Extensible packs system** (`/packs/*.json`)  



## 🚀 Quickstart
git clone https://github.com/ayondalai7/neuroaid-oss && cd NeuroAid-OSS
python -m venv .venv && source .venv/bin/activate  
.venv\Scripts\activate  
pip install -r requirements.txt
export OLLAMA_URL=http://localhost:11434
export MODEL_NAME=llama3.1:8b   # or mistral, gemma, etc.
streamlit run appM/app.py




 



