from fallback_after import handle_decision

tests = [
    ("T09", "The password reset page is broken."),
    ("T10", "The password reset page does not work."),
    ("T11", "The password recovery page is broken."),
]

for test_id, message in tests:
    result = handle_decision(
        message,
        {"decision": "ACCOUNT_ISSUE"}
    )
    expected = "SEND_TO_HUMAN"
    actual = result["action"]
    status = "PASS" if actual == expected else "FAIL"

    print(f"{test_id}: {status}")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")
    print("-" * 40)
