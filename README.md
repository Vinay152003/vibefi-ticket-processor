# vibefi-ticket-processor

## Short Architecture & Approach

**Goal:**  
A small service that ingests a JSON ticket, decides whether to generate an **AI code patch** (LLM-assisted) or return a **Vibe-coded troubleshooting workflow**, and returns a structured response:  
`{ decision, reasoning, checklist }`

### Approach
- Lightweight **rule-first decision layer** (severity, channel, keywords) for fast, deterministic classification.
- Where rules are ambiguous or require code reasoning, call an **LLM** to classify and generate the appropriate remediation or workflow.
- Always include structured **reasoning** and a short **checklist** of next actions.
- Exposed via a simple **FastAPI HTTP API** with JSON input/output for easy integration.

### Why Rule-First + LLM?
- **Rules** provide predictable, low-latency behavior for straightforward, high-frequency cases.  
- **LLMs** handle nuanced tickets requiring reasoning or producing human-friendly remediation plans.

---

## Suggested Repo Structure

vibefi-ticket-processor/
├─ app/
│ ├─ main.py
│ ├─ decision.py
│ ├─ llm_client.py
│ ├─ prompts.py
│ ├─ schemas.py
│ └─ tests/
│ ├─ test_decision.py
│ └─ test_api.py
├─ requirements.txt
├─ README.md
└─ sample_tickets.json

yaml

---

## Core Logic
All code files in this repo are self-contained FastAPI examples implementing a rule engine, LLM call placeholder, prompts, and structured response formatting.  
Replace the LLM placeholder in `llm_client.py` with your chosen provider (e.g., OpenAI, Anthropic) and API key.

---

## Prompts & Helpers

**Classifier Prompt (prompts.py)**  
Used to decide between `ai_code_patch` and `vibe_workflow`. Prompts expect structured JSON output for easy parsing.

**Generation Prompts**
- `GEN_PATCH_PROMPT`: Produces concise code patch/pseudocode and a checklist.  
- `GEN_WORKFLOW_PROMPT`: Generates a compact troubleshooting workflow and checklist.

### Prompt Engineering Tips
- Include examples (few-shot) to improve consistency.
- Ask models to produce **only JSON** and validate with a strict parser.
- Keep outputs concise and usable — prefer pseudocode over long code patches.

---

## Validation & Testing Before Shipping

### Unit Tests
- Test `rule_decision` with varied ticket samples (errors, login issues, billing queries).  
- Test API endpoints for correct schema and response fields.

### Integration / LLM Validation
- Use recorded LLM responses (mocks) for deterministic CI tests.
- Validate JSON parsing and output integrity.

### Quality & Safety
- Lint or format generated code patches before review.
- Always require **human approval** before auto-applying code patches.
- Verify checklist items are small, actionable, and clear.

### Metrics to Track (Post-Deploy)
- **Decision accuracy** (% correct classification).  
- **Resolution time improvement** (before/after).  
- **Human override rate** (% of reclassified tickets).  
- **LLM hallucination rate** (invalid or irrelevant patches).

### Validation Steps
1. Smoke test rule-only scenarios.  
2. Mock-test LLM responses for structure validation.  
3. Stage and manually review before rollout.  
4. Monitor performance metrics after deployment.

---

## Example Test Cases

| Ticket | Input Summary | Expected Decision |
|--------|----------------|-------------------|
| A | `Unhandled exception in payments API: TypeError` | `ai_code_patch` |
| B | `Customer cannot find invoice, need steps to download` | `vibe_workflow` |
| C | Ambiguous, medium severity | LLM classification |

---

## How AI Was Used
- **Decision Augmentation:** LLM used for ambiguous or context-heavy tickets.  
- **Patch Generation:** Produces concise pseudocode or diffs to assist engineers.  
- **Workflow Generation:** Writes structured troubleshooting instructions.  
- **Prompt & Parsing:** Produces machine-usable JSON via structured prompting.

---

## Trade-offs & Notes
- **Rule-first:** Fast and predictable, but less flexible.  
- **LLM-based:** Smarter, but may hallucinate — always gated by human review.  
- **Security:** Redact sensitive or PII data before LLM calls.  
- **Latency:** Use async or background tasks for LLM calls to maintain responsiveness.

---

## How to Run Locally

```bash
git clone https://github.com/Vinay152003/vibefi-ticket-processor.git
cd vibefi-ticket-processor
pip install -r requirements.txt
uvicorn app.main:app --reload
Test an Example Request
bash
Copy code
curl -X POST "http://127.0.0.1:8000/process" \
-H "Content-Type: application/json" \
-d '{"channel":"portal","severity":"high","summary":"TypeError in payments module","details":"Unhandled exception when calling API"}'
Environment Setup
bash
Copy code
export LLM_PROVIDER=openai
Add your LLM API key in your environment or replace the placeholder inside app/llm_client.py.

Validation & Scaling Notes
Cache frequent classification results for performance.

Queue heavy LLM operations via background workers (e.g., Celery or Cloud Tasks).

Use structured logs to analyze model performance over time.

Submission Summary for VibeFI AI
Repo: https://github.com/Vinay152003/vibefi-ticket-processor

Includes:

Core logic

Prompts

Example tickets

Test cases

Key points:

Rule-first engine handles clear cases (error traces → ai_code_patch).

LLM fallback handles ambiguity and generates workflows or patches.

Includes validation, safety gating, and human-in-the-loop checks.

