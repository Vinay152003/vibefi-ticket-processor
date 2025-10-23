from fastapi import FastAPI
from .schemas import Ticket, DecisionResponse, ActionItem
from .decision import decide
from .llm_client import call_llm
from .prompts import GEN_PATCH_PROMPT, GEN_WORKFLOW_PROMPT
import uuid
import asyncio

app = FastAPI(title="VibeFI Ticket Processor")

def mk_action(title, desc, owner=None):
    return {"id": str(uuid.uuid4()), "title": title, "description": desc, "owner": owner}

@app.post("/process", response_model=DecisionResponse)
async def process_ticket(ticket: Ticket):
    # 1) Decide (rules then LLM)
    decision_obj = await decide(ticket)
    decision = decision_obj.get("decision")
    reasoning = decision_obj.get("reason", "")
    checklist = []
    metadata = {"confidence": decision_obj.get("confidence", 0.0)}
    # 2) If AI code patch -> call LLM to generate patch
    if decision == "ai_code_patch":
        prompt = GEN_PATCH_PROMPT.format(summary=ticket.summary, details=(ticket.details or ""))
        llm_out = await call_llm(prompt)
        text = llm_out["text"]
        # naive extraction for patch and checklist: in real impl parse JSON
        checklist.append(mk_action("Review code patch", "Dev to review and run tests"))
        checklist.append(mk_action("Run CI", "Execute test suite and integration tests"))
        return {"decision":"ai_code_patch","reason":reasoning + " | " + text,"checklist":checklist,"metadata":metadata}
    else:
        # generate vibe workflow
        prompt = GEN_WORKFLOW_PROMPT.format(summary=ticket.summary, details=(ticket.details or ""))
        llm_out = await call_llm(prompt)
        text = llm_out["text"]
        checklist.append(mk_action("Follow Vibe workflow", text))
        checklist.append(mk_action("Confirm with customer", "Contact the user to confirm resolution"))
        return {"decision":"vibe_workflow","reason":reasoning + " | " + text,"checklist":checklist,"metadata":metadata}
