def next_grounding_step(state: dict):
    i = state.get("i", 0)
    steps = [
        "Take a slow breath. Name five things you can see.",
        "Name four things you can feel (e.g., clothes on skin, chair under you).",
        "Name three things you can hear, near or far.",
        "Name two things you can smell or remember smelling recently.",
        "Name one thing you can taste or imagine tasting. How is your body now?"
    ]
    done = i >= len(steps)-1
    prompt = steps[i] if i < len(steps) else "Grounding complete."
    state["i"] = i + 1
    return prompt, state, done

def next_cbt_step(state: dict):
    i = state.get("i", 0)
    steps = [
        "Briefly describe the situation that bothered you.",
        "What thought went through your mind?",
        "What evidence supports that thought?",
        "What evidence goes against it?",
        "Propose a kinder, balanced reframe."
    ]
    done = i >= len(steps)-1
    prompt = steps[i] if i < len(steps) else "CBT reframe complete."
    state["i"] = i + 1
    return prompt, state, done
