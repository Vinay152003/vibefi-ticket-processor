# vibefi-ticket-processor
1) Short architecture & approach

Goal: Small service that ingests a JSON ticket, decides whether to generate an AI code patch (LLM-assisted) or return a Vibe-coded troubleshooting workflow, and returns a structured response: { decision, reasoning, checklist }.

Approach:

Lightweight rule-first decision layer (severity, channel, keywords) to be fast and deterministic for common cases.

Where rules are ambiguous or require code reasoning, call an LLM to classify + generate remediation (AI code patch) or to generate a step-by-step Vibe-coded workflow.

Always include structured reasoning and a short checklist of next actions.

Expose via a simple HTTP API (FastAPI) with JSON in/out for easy integration.

Why rule-first + LLM?

Rules give predictable, low-latency behavior for straightforward, high-frequency patterns.

LLM used when nuance or code reasoning is required — or to produce human-friendly remediation steps.

2) Suggested repo structure
vibefi-ticket-processor/
├─ app/
│  ├─ main.py              # FastAPI app (entry)
│  ├─ decision.py          # rule + LLM decision logic
│  ├─ llm_client.py        # thin wrapper for LLM calls
│  ├─ prompts.py           # stored prompts
│  ├─ schemas.py           # pydantic request/response models
│  └─ tests/
│     ├─ test_decision.py
│     └─ test_api.py
├─ requirements.txt
├─ README.md
└─ sample_tickets.json

3) Core logic (FastAPI + decision code)

Code files in this repo are self-contained example you can drop into app/. It includes a rule engine, LLM call placeholder, prompts, and response shaping.

Note: Replace the LLM-call placeholder in llm_client.py with your chosen provider (OpenAI, Anthropic, etc.) and your API key.

4) Prompts & helpers (explicit)

Classifier prompt (see prompts.py): used to instruct the model to choose between ai_code_patch and vibe_workflow. The prompt contains deterministic rules and expects JSON output — you should prefer models that support structured JSON output (or parse JSON from model text).

Generation prompts:

GEN_PATCH_PROMPT asks the model to produce a concise code patch/pseudocode and a checklist as JSON. Limit tokens and ask the model to return only JSON.

GEN_WORKFLOW_PROMPT asks for a compact Vibe-coded workflow and checklist.

Prompt engineering tips:

Always include examples in the prompt for the model to follow (few-shot).

Ask the model to produce only JSON; validate with a strict JSON parser and fallback to simpler parsing if it fails.

Constrain length and ask for minimal viable patches (pseudocode ok).

5) Validation & testing before shipping

Unit tests:

Test rule_decision with typical tickets (stack traces, login issues, billing tickets).

Test API endpoints with sample tickets and assert schema and response fields.

Integration / LLM validation:

Use recorded sample responses (mock LLM) in CI to ensure deterministic tests.

For each LLM prompt, create expected outputs (gold standard) and check parsing logic.

Quality & safety:

Lint/format generated code patches and run them in a sandbox or static analyzer. Prefer pseudocode or suggested diffs rather than full auto-deploy.

Limit the LLM’s capacity to auto-apply patches. Always require human approval before production change.

Verify checklist items are actionable and small (1-3 steps).

Metrics to track (post-deploy):

Decision accuracy (human-agreed): % of tickets correctly routed.

Time to resolution (before/after).

Human override rate: % times operators change the decision.

LLM hallucination rate for code (detected as invalid patches).

Validation steps:

Smoke tests — rules-only cases.

LLM mock tests — ensure parsing robust.

Staging with manual review: integrate model outputs but gate deployment behind human approval.

Canary and monitor metrics (errors, overrides).

6) Example test cases (quick)

Ticket A: { channel:"portal", severity:"high", summary:"Unhandled exception in payments api: TypeError at process_payment" }

Expected: ai_code_patch (rule triggers on "TypeError", "exception")

Ticket B: { channel:"email", severity:"low", summary:"Customer cannot find invoice, need steps to download invoice" }

Expected: vibe_workflow

Ticket C: ambiguous medium severity: ask LLM — check its output JSON for decision, confidence, reason.

7) How AI was used (document where it helped)

Decision augmentation: LLM used when rule certainty low to classify ambiguous tickets.

Patch generation: LLM produces code snippet or diff (pseudocode) to accelerate developer remediation drafts.

Workflow generation: LLM writes human-friendly troubleshooting flows.

Prompt / parsing: careful prompts produce structured JSON for machine consumption.

8) Trade-offs & notes

Rule-first: faster, cheaper, predictable, but less flexible.

LLM use: flexible and human-like, but can hallucinate — always gate auto-code application.

Security: never send full customer PII to third-party LLMs without redaction and contractual clearance.

Latency: synchronous LLM calls increase response time; consider async / background tasks for heavy generation and return a provisional answer quickly.

9) How to present to VibeFI AI (what to submit)

Push the code above to a small repo vibefi-ticket-processor with README.md explaining:

How to run locally: uvicorn app.main:app --reload

How to set LLM_PROVIDER and where to wire the actual provider.

Include sample_tickets.json and tests/ with pytest tests.

In your submission note, include:

Where the LLM was used (classifier + generator), and sample prompts (as provided).

Validation plan and safety controls (human-in-the-loop for code patches).

A short note on scaling (cache decisions, queue heavy LLM jobs via background worker like Celery).

10) Quick “reply” text you can paste to VibeFI AI

Hi VibeFI AI team — thanks for the brief. I implemented a small FastAPI service that accepts a ticket JSON, applies a rule-first decision engine (with LLM fallback), and returns {decision, reasoning, checklist}.
Repo: https://github.com/Vinay152003/vibefi-ticket-processor
— includes core logic, prompts, example tickets, and tests.
Key notes: rules handle high-confidence cases (error traces → ai_code_patch); LLM is used for ambiguous classification and for generating minimal code patches or Vibe-coded workflows. I included validation steps, human-in-the-loop gating for code patches, and test cases. Happy to demo or iterate on the prompt & thresholds.
