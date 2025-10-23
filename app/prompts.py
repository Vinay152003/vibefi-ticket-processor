# Prompts used for classification and generation

CLASSIFY_PROMPT = """
You are a technical classifier. Given a ticket with channel: {channel}, severity: {severity}, summary: {summary}, details: {details}
Decide whether this ticket requires an 'ai_code_patch' or 'vibe_workflow'.
Return only valid JSON with keys:
{{
  "decision": "ai_code_patch" or "vibe_workflow",
  "confidence": 0.0-1.0,
  "reason": "one-line reason"
}}
Rules:
- If ticket mentions stack traces, code errors, failing tests, environment issues -> prefer ai_code_patch.
- If ticket is about user procedures, account flow, permissions, or requires step-by-step operational steps -> prefer vibe_workflow.
- High severity + code keywords -> prefer ai_code_patch.
"""

GEN_PATCH_PROMPT = """
You are an assistant that writes minimal code patches and a checklist for remediation.
Ticket: {summary}
Details: {details}
Provide:
1) Short reasoning
2) A minimal code patch snippet or pseudocode (bounded to 50 lines)
3) A checklist of next steps (3-6 items)
Return JSON: {{ "reason":..., "patch": "...", "checklist": [{{"id":"", "title":"", "description":""}}] }}
"""

GEN_WORKFLOW_PROMPT = """
You are an assistant that writes a Vibe-coded troubleshooting workflow (concise).
Ticket: {summary}
Details: {details}
Return JSON: {{ "reason":..., "workflow_steps": [ "Step 1...", "Step 2..." ], "checklist": [...] }}
"""
