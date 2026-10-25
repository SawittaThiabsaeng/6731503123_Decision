
import json
from pathlib import Path


KNOWLEDGE_FILE = Path(__file__).parent / "knowledge_base.json"


def retrieve_context(user_message):
    """Retrieve knowledge records matching the user's message."""

    if not isinstance(user_message, str) or not user_message.strip():
        return []

    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    message = user_message.lower()
    matched_records = []

    for record in data["knowledge_records"]:
        keywords = record.get("keywords", [])

        if any(keyword.lower() in message for keyword in keywords):
            matched_records.append(record)

    return matched_records


if __name__ == "__main__":
    examples = [
        "I forgot my password and cannot log in.",
        "The website shows a 500 error.",
        "What are your opening hours?",
        "It does not work. Please help."
    ]

    for message in examples:
        records = retrieve_context(message)

        print(f"\nInput: {message}")

        if records:
            for record in records:
                print(
                    f'{record["id"]}: '
                    f'{record["category"]} - '
                    f'{record["description"]}'
                )
        else:
            print("No matching knowledge records.")
