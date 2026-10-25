
VALID_CATEGORIES = {
    "ACCOUNT_ISSUE",
    "TECHNICAL_ISSUE",
    "GENERAL_INQUIRY"
}


def handle_decision(user_message, ai_result, model_error=None):
    """Validate an AI decision and safely handle failures."""

    # Handle model failure or timeout
    if model_error is not None:
        return {
            "status": "REVIEW",
            "reason": "AI service unavailable or timed out",
            "action": "SEND_TO_HUMAN"
        }

    # Validate user input
    if not isinstance(user_message, str) or not user_message.strip():
        return {
            "status": "REVIEW",
            "reason": "Missing or invalid user message",
            "action": "ASK_FOR_MORE_INFORMATION"
        }

    # Validate AI response format
    if not isinstance(ai_result, dict):
        return {
            "status": "REVIEW",
            "reason": "Invalid AI response format",
            "action": "SEND_TO_HUMAN"
        }

    category = ai_result.get("decision")

    if not isinstance(category, str) or category not in VALID_CATEGORIES:
        return {
            "status": "REVIEW",
            "reason": "Unknown or invalid decision category",
            "action": "SEND_TO_HUMAN"
        }

    message = user_message.lower()

    # Detect vague requests
    vague_phrases = [
        "it does not work",
        "it doesn't work",
        "please help"
    ]

    if any(phrase in message for phrase in vague_phrases):
        return {
            "status": "REVIEW",
            "reason": "Insufficient information",
            "action": "ASK_FOR_MORE_INFORMATION"
        }

    
    # Detect requests involving multiple issue types
    has_account_issue = any(word in message for word in [
        "account", "login", "log in", "password"
    ])

    has_technical_issue = any(word in message for word in [
        "website", "server error", "500 error",
        "not loading", "crash", "bug"
    ])

    # Detect password recovery pages that fail to load
    account_recovery_page_failing = (
        any(phrase in message for phrase in [
            "password reset page",
            "password recovery page"
        ])
        and any(phrase in message for phrase in [
            "not loading",
            "does not load",
            "doesn't load",
            "is broken",
            "does not work",
            "doesn't work"
])
    )

    if (
        (has_account_issue and has_technical_issue)
        or account_recovery_page_failing
    ):
        return {
            "status": "REVIEW",
            "reason": "Multiple possible issue categories",
            "action": "SEND_TO_HUMAN"
        }


    return {
        "status": "ACCEPTED",
        "category": category,
        "action": "ROUTE_TO_SUPPORT"
    }


# Run the demonstration only when this file is executed directly
if __name__ == "__main__":
    test_message = "It does not work. Please help."
    observed_ai_result = {"decision": "TECHNICAL_ISSUE"}

    result = handle_decision(test_message, observed_ai_result)
    print(result)

    # Demonstrate an AI timeout
    timeout_result = handle_decision(
        "I cannot log in",
        None,
        model_error="TimeoutError"
    )
    print(timeout_result)
