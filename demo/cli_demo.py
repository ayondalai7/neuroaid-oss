
import argparse
from appM.neuroaid.prompts import SYSTEM_BASE, CRISIS_MESSAGE
from appM.neuroaid.backends import chat
from appM.neuroaid.flows import next_grounding_step, next_cbt_step

def run(mode: str):
    messages = [{"role":"system","content": SYSTEM_BASE}]
    flow_state = {}
    print(f"NeuroAid OSS ({mode}) — type 'quit' to exit.\n")

    while True:
        if mode == "grounding":
            prompt, flow_state, done = next_grounding_step(flow_state)
            print(f"[Guide] {prompt}")
        elif mode == "cbt":
            prompt, flow_state, done = next_cbt_step(flow_state)
            print(f"[Guide] {prompt}")
        else:
            user = input("You: ").strip()
            if user.lower() in ("quit","exit"): break
            if user:
                if any(k in user.lower() for k in ["suicide","kill myself","end my life","hurt myself","harm others"]):
                    print(f"[NeuroAid] {CRISIS_MESSAGE}")
                    continue
                messages.append({"role":"user","content": user})
                ans = chat(messages)
                messages.append({"role":"assistant","content": ans})
                print(f"[NeuroAid] {ans}")
            continue

        user = input("You: ").strip()
        if user.lower() in ("quit","exit"): break
        if user:
            messages.append({"role":"user","content": user})
            ans = chat(messages)
            messages.append({"role":"assistant","content": ans})
            print(f"[NeuroAid] {ans}")
        if mode in ("grounding","cbt") and done:
            print("[NeuroAid] Exercise complete. Try another step or type 'quit'.")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["grounding","cbt","free"], default="grounding")
    args = p.parse_args()
    run(args.mode)
