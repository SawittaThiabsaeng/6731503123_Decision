
import json
import statistics
import time
from pathlib import Path

from fallback import handle_decision
from retrieve_context import retrieve_context

BASE_DIR = Path(__file__).parent
EVAL_FILE = BASE_DIR / "eval-cases.json"
OUTPUT_FILE = BASE_DIR / "evidence" / "latency_benchmark.txt"

REPEATS = 5


def run_once(case):
    message = case["input"]

    if "simulated_ai_result" in case:
        ai_result = case["simulated_ai_result"]
    elif case.get("expected_decision") is not None:
        ai_result = {"decision": case["expected_decision"]}
    else:
        ai_result = None

    start = time.perf_counter()
    retrieve_context(message)
    handle_decision(message, ai_result)
    return (time.perf_counter() - start) * 1000


def main():
    with EVAL_FILE.open("r", encoding="utf-8") as file:
        cases = json.load(file)["evaluation_cases"]

    measurements = []

    for case in cases:
        # One warm-up run, not included in measurements
        run_once(case)

        times = [run_once(case) for _ in range(REPEATS)]
        measurements.extend(times)

        print(
            f'{case["id"]}: '
            f'average={statistics.mean(times):.3f} ms, '
            f'min={min(times):.3f} ms, '
            f'max={max(times):.3f} ms'
        )

    sorted_times = sorted(measurements)
    p95_index = max(0, int(0.95 * len(sorted_times) + 0.999999) - 1)
    p95 = sorted_times[min(p95_index, len(sorted_times) - 1)]

    report = [
        "Local Pipeline Latency Benchmark",
        f"Evaluation cases: {len(cases)}",
        f"Repeats per case: {REPEATS}",
        f"Total measured runs: {len(measurements)}",
        f"Average latency: {statistics.mean(measurements):.3f} ms",
        f"Approximate p95 latency: {p95:.3f} ms",
        "Scope: local retrieval and fallback processing only.",
        "Excludes Jev model execution and network latency.",
    ]

    OUTPUT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n" + "\n".join(report))
    print(f"\nSaved report: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
