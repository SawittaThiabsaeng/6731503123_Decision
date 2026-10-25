# Support Request Classifier — A7

Student ID: 6731503123

## Project Overview
This project classifies customer support messages into:
- ACCOUNT_ISSUE
- TECHNICAL_ISSUE
- GENERAL_INQUIRY

A deterministic fallback mechanism handles unclear input,
invalid AI results, model errors, and potentially mixed issues.

## Grounding Context
The knowledge base is stored in `knowledge_base.json`.
`retrieve_context.py` retrieves relevant records using keyword matching.
A manual Jev Playground experiment compared the same message with
and without additional context. The predicted category remained
TECHNICAL_ISSUE, while the displayed probabilities changed.

## Evaluation Dataset
`eval-cases.json` contains 10 cases:
- 3 normal
- 3 edge
- 2 fallback
- 2 difficult or ambiguous

## How to Run
Run these commands from the project directory:
- `python .\test_fallback.py`
- `python .\test_a7_targeted.py`
- `python .\evaluate.py`
- `python .\benchmark.py`

## Improvement
The updated fallback logic recognizes additional descriptions of
a broken password recovery page, including:
- is broken
- does not work
- doesn't work

The targeted tests T09-T11 passed. The original 10-case evaluation
also passed with 100% local action agreement.

## Limitations
Local evaluation measures action agreement in the local pipeline,
not actual AI model accuracy. The benchmark excludes Jev inference
and network latency. The manual grounding experiment used only one
message per condition and cannot establish improved accuracy.

## Evidence
The `evidence` folder contains evaluation outputs, benchmark results,
targeted tests, and Jev Playground screenshots.
