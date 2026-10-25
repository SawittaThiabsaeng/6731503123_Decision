# Support Request Classifier

**Student Name:** Sawitta Thiabsaeng  
**Student ID:** 6731503123  
**Course:** Platform Development

## Project Overview

The Support Request Classifier is an AI decision capability that categorizes customer support messages into three categories:

- `ACCOUNT_ISSUE` — Account and login problems
- `TECHNICAL_ISSUE` — Website and application problems
- `GENERAL_INQUIRY` — General questions and service information

The project combines an AI decision capability with deterministic Python fallback rules to handle unclear messages, invalid model outputs, model errors, and potentially ambiguous requests.

## Assignment A6: Build and Integrate an AI Decision Capability

A6 focuses on implementing the initial AI decision capability and designing a validation and fallback mechanism.

Key components:

- Jev Playground experiments for support request classification
- Python fallback validation
- Handling of vague, invalid, and ambiguous requests
- Proposed integration architecture and downstream actions
- Test cases and evidence of fallback behavior

**Report:** `A6_6731503123.pdf`

**Main files:**
- `fallback.py`
- `test_fallback.py`

Note: Jev Playground and the local Python fallback were tested separately. A live API integration between them has not been implemented.

## Assignment A7: Evaluate and Improve AI Capability

A7 evaluates the existing capability and improves one part of the fallback logic.

Key components:

- Grounding context and keyword-based knowledge retrieval
- A 10-case evaluation dataset
- Baseline and post-improvement benchmarks
- Additional targeted tests for password-recovery page failures
- Engineering reflection and limitations

**Report:** `A7_6731503123.pdf`

**Main files:**
- `knowledge_base.json`
- `retrieve_context.py`
- `eval-cases.json`
- `evaluate.py`
- `benchmark.py`
- `fallback_before.py`
- `fallback_after.py`
- `test_a7_targeted.py`

The updated fallback recognizes additional phrases, including `is broken`, `does not work`, and `doesn't work`, when identifying password-recovery page failures.

The three targeted tests T09–T11 passed. The original 10-case evaluation achieved 100% local action agreement. This result measures agreement with the expected local actions, not actual AI model accuracy.

## How to Run

Run these commands from the project directory:

```powershell
python .\test_fallback.py
python .\test_a7_targeted.py
python .\evaluate.py
python .\benchmark.py
```

## Evidence

The `evidence/` directory contains test outputs, benchmark results, retrieval evidence, and screenshots from the Jev Playground grounding experiment.

## Limitations

- The knowledge retrieval method uses keyword matching.
- The Jev Playground model is not automatically integrated with the local Python fallback.
- The benchmark excludes model inference and network latency.
- The grounding experiment used one message per condition and does not establish improved classification accuracy.
- Further testing with a larger dataset is needed before production deployment.

## Submission Files

- `A6_6731503123.pdf`
- `A7_6731503123.pdf`
- Python source code, evaluation dataset, knowledge base, and supporting evidence
>>>>>>> Stashed changes
