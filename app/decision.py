from .prompts import CLASSIFY_PROMPT, GEN_PATCH_PROMPT, GEN_WORKFLOW_PROMPT
from .llm_client import call_llm
import re
from typing import Tuple

# Simple keyword sets for rule-first decisions
CODE_KEYWORDS = ["stack trace","error","exception","NullPointer", "segfault", "traceback", "failed test", "unit test", "build failed", "compilation", "TypeError", "ReferenceError"]
WORKFLOW_KEYWORDS = ["how to", "cannot access", "login", "password", "reset", "user guide", "steps", "procedure", "process", "onboarding"]

def rule_decision(ticket) -> Tuple[str, float, str]:
    text = f"{ticket.summary} {ticket.details or ''}".lower()
    severity = ticket.severity
    # if clear code error keywords, immediate ai_code_patch
    for k in CODE_KEYWORDS:
        if k.lower() in text:
            return "ai_code_patch", 0.95, f"Detected code error keyword '{k}'"
    for k in WORKFLOW_KEYWORDS:
        if k.lower() in text:
            return "vibe_workflow", 0.9, f"Detected workflow keyword '{k}'"
    # high severity but vague -> escalate to AI
    if severity in ("high","critical"):
        return "ai_code_patch", 0.6, "High severity — prefer developer remediation"
    # default to workflow
    return "vibe_workflow", 0.5, "Default workflow recommendation"

async def decide(ticket):
    decision, confidence, reason = rule_decision(ticket)
    # if confident, skip LLM
    if confidence >= 0.9:
        return {"decision": decision, "confidence": confidence, "reason": reason}
    # else call LLM for classification
    prompt = CLASSIFY_PROMPT.format(channel=ticket.channel, severity=ticket.severity, summary=ticket.summary, details=(ticket.details or ""))
    llm_resp = await call_llm(prompt)
    # parse llm_resp["text"] as JSON ideally; here we attempt to extract
    import json
    try:
        parsed = json.loads(llm_resp["text"])
        return parsed
    except Exception:
        # quick fallback: use regex
        text = llm_resp["text"].lower()
        if "ai_code_patch" in text or "code" in text:
            return {"decision":"ai_code_patch","confidence":0.8,"reason":"LLM suggested code patch"}
        return {"decision":"vibe_workflow","confidence":0.7,"reason":"LLM suggested workflow"}
