import os, time, json, requests
from typing import Iterator, Tuple, List, Dict
from appM.config import ENDPOINT, MODEL_NAME, TIMEOUT, TEMPERATURE, RETRIES, BACKOFF_FACTOR


def _get(url: str, timeout: int = 4):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r

def _post(url: str, payload: dict, timeout: int = 30, stream: bool = False):
    r = requests.post(url, json=payload, timeout=timeout, stream=stream)
    r.raise_for_status()
    return r


def server_up(endpoint: str = ENDPOINT) -> bool:
    try:
        _get(f"{endpoint}/api/tags", timeout=4)
        return True
    except Exception:
        return False

def model_present(model_name: str = MODEL_NAME, endpoint: str = ENDPOINT) -> bool:
    try:
        r = _get(f"{endpoint}/api/tags", timeout=6)
        names = [m.get("name") for m in r.json().get("models", []) if "name" in m]
        base = model_name.split(":")[0]
        return any(n == model_name or (isinstance(n, str) and n.startswith(base)) for n in names)
    except Exception:
        return False

def warmup_generate(model_name: str = MODEL_NAME, endpoint: str = ENDPOINT) -> bool:
    """
    Do a tiny non-streaming generate of 1 token.
    If it returns 200 + a 'response' key, model is truly ready.
    """
    try:
        payload = {
            "model": model_name,
            "prompt": "ping",
            "stream": False,
            "options": {"num_predict": 1}
        }
        r = _post(f"{endpoint}/api/generate", payload, timeout=20)
        _ = r.json().get("response", "")
        return True
    except Exception:
        return False

def readiness(model_name: str = MODEL_NAME, endpoint: str = ENDPOINT, do_warmup: bool = True) -> Tuple[bool, str]:
    if not server_up(endpoint):
        return False, "Ollama server is not reachable."
    if not model_present(model_name, endpoint):
        return False, f"Model '{model_name}' not found. Pull it with: ollama pull {model_name}"
    if do_warmup and not warmup_generate(model_name, endpoint):
        return False, f"Model '{model_name}' present but not responding yet (warming)."
    return True, f"Model '{model_name}' is ready."

def chat(messages: List[Dict],
         endpoint: str = ENDPOINT,
         model: str = MODEL_NAME,
         temperature: float = TEMPERATURE,
         retries: int = RETRIES,
         backoff_factor: int = BACKOFF_FACTOR) -> str:
    url = f"{endpoint}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "options": {"temperature": temperature},
        "stream": False
    }
    delay = 2
    for attempt in range(1, retries + 1):
        try:
            r = _post(url, payload, timeout=TIMEOUT)
            data = r.json()
            if "message" in data and "content" in data["message"]:
                return data["message"]["content"]
            if "content" in data:
                return data["content"]
            return "[No content returned from model]"
        except (requests.RequestException, ValueError) as e:
            if attempt < retries:
                time.sleep(delay)
                delay *= backoff_factor
            else:
                return f"[Error contacting model after {retries} attempts: {e}]"


def stream_chat(messages: List[Dict],
                endpoint: str = ENDPOINT,
                model: str = MODEL_NAME,
                temperature: float = TEMPERATURE,
                connect_timeout: int = 10) -> Iterator[str]:
    """
    Streams tokens from Ollama's /api/chat (NDJSON format).
    Yields incremental content strings so frontend can render live typing.
    """
    url = f"{endpoint}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "options": {"temperature": temperature},
        "stream": True
    }
    try:
 
        with requests.post(url, json=payload,
                           stream=True,
                           timeout=(connect_timeout, None)) as r:
            r.raise_for_status()
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    evt = json.loads(line)
                    delta = evt.get("message", {}).get("content", "")
                    if delta:
                        yield delta
                except Exception:
                    continue
    except requests.exceptions.ConnectTimeout:
        yield "[Error: Connection to Ollama timed out. Is the server running?]"
    except Exception as e:
        yield f"[Streaming error: {type(e).__name__}: {e}]"
