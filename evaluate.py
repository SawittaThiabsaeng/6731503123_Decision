
import json
import time
from pathlib import Path

from fallback import handle_decision
from retrieve_context import retrieve_context


BASE_DIR = Path(__file__).parent
EVAL_FILE = BASE_DIR / "eval-cases.json"



def simulate_ai_result(case):
    """Use a recorded or explicitly defined AI result for each case."""

    if "simulated_ai_result" in case:
        return case["simulated_ai_result"]

    decision = case.get("expected_decision")

    if decision is None:
        return None

    return {"decision": decision}



def evaluate_case(case):
    message = case["input"]
    ai_result = simulate_ai_result(case)

    start = time.perf_counter()

    # Retrieve relevant knowledge records
    context = retrieve_context(message)

    # Run the existing fallback validation
    result = handle_decision(message, ai_result)

    latency_ms = (time.perf_counter() - start) * 1000

    expected_action = case["expected_action"]
    actual_action = result["action"]

    return {
        "id": case["id"],
        "type": case["type"],
        "expected_action": expected_action,
        "actual_action": actual_action,
        "action_correct": actual_action == expected_action,
        "retrieved_record_ids": [record["id"] for record in context],
        "latency_ms": round(latency_ms, 3),
        "result": result,
    }


def main():
    with EVAL_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    results = [evaluate_case(case) for case in data["evaluation_cases"]]

    for item in results:
        print(
            f'{item["id"]}: '
            f'{"PASS" if item["action_correct"] else "FAIL"}'
        )
        print(f'Expected action: {item["expected_action"]}')
        print(f'Actual action: {item["actual_action"]}')
        print(f'Retrieved records: {item["retrieved_record_ids"]}')
        print(f'Latency: {item["latency_ms"]} ms')
        print("-" * 50)

    correct = sum(item["action_correct"] for item in results)
    total = len(results)
    accuracy = correct / total * 100 if total else 0
    average_latency = (
        sum(item["latency_ms"] for item in results) / total
        if total else 0
    )

    print("\n=== Evaluation Summary ===")
    print(f"Correct actions: {correct}/{total}")
    print(f"Action agreement: {accuracy:.1f}%")
    print(f"Average local processing latency: {average_latency:.3f} ms")
    print("Note: This is local pipeline testing, not actual Jev model accuracy.")


if __name__ == "__main__":
    main()
