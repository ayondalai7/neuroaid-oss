import os, io, csv, json, time, datetime as dt, requests, streamlit as st
from pathlib import Path
from appM.config import ENDPOINT, MODEL_NAME, REPO_URL, DEMO_URL
from appM.neuroaid import backends
from appM.neuroaid.prompts import SYSTEM_BASE
from appM.neuroaid.utils import append_journal, load_journal
from urllib.parse import quote  

st.set_page_config(page_title="NeuroAid OSS", page_icon="🧠", layout="wide")

@st.cache_resource
def load_css_text() -> str:
    css_path = Path(__file__).resolve().parent / "theme.css"
    return css_path.read_text(encoding="utf-8")

@st.cache_resource
def cached_readiness() -> tuple[bool, str]:
    return backends.readiness(model_name=MODEL_NAME, endpoint=ENDPOINT, do_warmup=False)

@st.cache_data
def load_journal_cached():
    try:
        data = load_journal()
        return data or []
    except Exception:
        return []


st.markdown(f"<style>{load_css_text()}</style>", unsafe_allow_html=True)
ready, _msg = cached_readiness()
status_text = "✅ Model is ready" if ready else "⏳ Model loading…"


GITHUB_SVG = """<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
  <path d="M8 0C3.58 0 0 3.58 0 8a8 8 0 0 0 5.47 7.59c.4.07.55-.17.55-.38
  0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
  -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07
  -.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08
  -.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.68 7.68 0 0 1 2-.27c.68 0 1.36.09
  2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82
  2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01
  2.2 0 .21.15.46.55.38A8 8 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
</svg>"""
YOUTUBE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
  <path d="M23.5 6.2s-.2-1.6-.8-2.3c-.7-.8-1.5-.9-1.9-1C17.7 2.5 12 
  2.5 12 2.5s-5.7 0-8.8.4c-.4.1-1.2.1-1.9 1-.6.7-.8 2.3-.8 
  2.3S0 8.1 0 10v4c0 1.9.2 3.8.2 
  3.8s.2 1.6.8 2.3c.7.8 1.5.9 1.9 
  1 3.1.4 8.8.4 8.8.4s5.7 0 8.8-.4c.4-.1 
  1.2-.1 1.9-1 .6-.7.8-2.3.8-2.3S24 
  15.9 24 14v-4c0-1.9-.2-3.8-.2-3.8zM9.5 
  15.6V8.4L15.5 12l-6 3.6z"/>
</svg>"""
GITHUB_IMG  = f'<img alt="GitHub"  width="20" height="20" src="data:image/svg+xml;utf8,{quote(GITHUB_SVG)}" />'
YOUTUBE_IMG = f'<img alt="Demo"    width="22" height="22" src="data:image/svg+xml;utf8,{quote(YOUTUBE_SVG)}" />'

# Navbar
status_info = f"Running on {MODEL_NAME} · {status_text}"
navbar_html = f"""
<header class="navbar">
  <div class="nav-center">🧠 NeuroAid OSS</div>
  <div class="nav-right">
    <span class="nav-icon">{GITHUB_SVG}</span>
    <span class="nav-icon">{YOUTUBE_SVG}</span>
    <span class="status-pill">{status_info}</span>
  </div>
</header>
"""

st.markdown(navbar_html, unsafe_allow_html=True)
# JS: shrink on scroll + dedupe duplicate navbars
st.markdown("""
<script>
(function() {
  function shrinkOnScroll() {
    const nav = document.querySelector('.navbar');
    if (!nav) return;
    if (window.scrollY > 10) nav.classList.add('shrink');
    else nav.classList.remove('shrink');
  }
  window.addEventListener('scroll', shrinkOnScroll);

  function dedupe() {
    const navs = document.querySelectorAll('header.navbar');
    navs.forEach((n, i) => { if (i > 0 && n.parentNode) n.parentNode.removeChild(n); });
  }
  dedupe();
  new MutationObserver(dedupe).observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="crisis small">
  ⚠️ Crisis Support
  <div class="emergency-menu">
    <ul>
      <li><a href="tel:911">🚑 911 (US)</a></li>
      <li><a href="tel:100">🚓 100 (Police - India)</a></li>
      <li><a href="tel:108">🚨 108 (Ambulance - India)</a></li>
    </ul>
  </div>
</div>
""", unsafe_allow_html=True)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_BASE}]
if "typing" not in st.session_state:
    st.session_state.typing = False


st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.markdown("<h2 class='chat-title'>Conversation</h2>", unsafe_allow_html=True)


for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    cls = "assistant" if m["role"] == "assistant" else "user"
    st.markdown(
        f"<div class='msg {cls}'><div class='bubble'>{m['content']}</div></div>",
        unsafe_allow_html=True
    )


text = st.chat_input("Type a message…", disabled=not ready)
if text:
    
    st.session_state.messages.append({"role": "user", "content": text})
    st.markdown("<div class='msg assistant'><div class='bubble streaming'>", unsafe_allow_html=True)
    stream_slot = st.empty()
    st.markdown("</div></div>", unsafe_allow_html=True)

    reply_parts = []

    for delta in backends.stream_chat(
        st.session_state.messages,
        endpoint=ENDPOINT,
        model=MODEL_NAME
    ):
        reply_parts.append(delta)
        stream_slot.markdown("".join(reply_parts) + "▌")
        
    final_reply = "".join(reply_parts)
    stream_slot.markdown(final_reply)
    st.session_state.messages.append({"role": "assistant", "content": final_reply})
    st.rerun()


data = load_journal_cached()
st.sidebar.header("Session")


if st.sidebar.button("Start New Session"):
    st.session_state.clear()
    st.rerun()  


try:
    j = io.BytesIO()
    j.write(json.dumps(data, indent=2).encode("utf-8"))
    j.seek(0)
    st.sidebar.download_button("Export Journal (.json)", j, "journal.json", "application/json")
except Exception as e:
    st.sidebar.warning(f"JSON export failed: {e}")


try:
    c = io.StringIO()
    w = csv.DictWriter(c, fieldnames=["timestamp", "assistant", "user"])
    w.writeheader()
    for r in data:
        w.writerow({k: r.get(k, '') for k in w.fieldnames})
    st.sidebar.download_button("Export Journal (.csv)", c.getvalue(), "journal.csv", "text/csv")
except Exception as e:
    st.sidebar.warning(f"CSV export failed: {e}")


if st.sidebar.button("Save Current to Journal"):
    try:
        last_assistant = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "assistant"), "")
        last_user = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), "")
        entry = {
            "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
            "assistant": last_assistant,
            "user": last_user,
        }
        p = append_journal(entry)
        st.sidebar.success(f"Saved to {p.name} (in /data).")
        st.balloons()              
        st.cache_data.clear()        
        st.rerun()                    
    except Exception as e:
        st.sidebar.warning(f"Could not save journal entry: {e}")

