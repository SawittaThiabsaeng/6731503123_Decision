
from fallback import handle_decision

tests = [
    {
        "id": "T05",
        "message": "It does not work. Please help.",
        "ai_result": {"decision": "TECHNICAL_ISSUE"},
        "expected": "ASK_FOR_MORE_INFORMATION",
    },
    {
        "id": "T06",
        "message": "My account has a problem",
        "ai_result": None,
        "expected": "SEND_TO_HUMAN",
    },
    {
        "id": "T07",
        "message": "My account has a problem",
        "ai_result": {"decision": "UNKNOWN_CATEGORY"},
        "expected": "SEND_TO_HUMAN",
    },
    {
        "id": "T08",
        "message": "I cannot log in and the website shows a 500 error",
        "ai_result": {"decision": "ACCOUNT_ISSUE"},
        "expected": "SEND_TO_HUMAN",
    },
]

for test in tests:
    result = handle_decision(
        test["message"],
        test["ai_result"],
    )

    passed = result["action"] == test["expected"]

    print(f'{test["id"]}: {"PASS" if passed else "FAIL"}')
    print(f'Expected action: {test["expected"]}')
    print(f'Actual result: {result}')
    print("-" * 50)
