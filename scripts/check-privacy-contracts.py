#!/usr/bin/env python3
from pathlib import Path
import sys


ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def main():
    sources = {
        "TweepPicture.swift": read("HomeScreen/TweepPicture.swift"),
        "TwitterRESTAPI.swift": read("HomeScreen/TwitterRESTAPI.swift"),
        "TweetsController.swift": read("HomeScreen/TweetsController.swift"),
    }
    forbidden = ("localizedDescription", "println(error)", "\\(connectionError)", "\\(clientError)")
    failures = []
    for name, source in sources.items():
        for value in forbidden:
            if value in source:
                failures.append(f"{name} contains raw Twitter error logging: {value}")

    expected = (
        "Twitter profile lookup failed",
        "Twitter profile request could not be created",
        "Twitter search request failed",
        "Twitter search request could not be created",
        "Twitter search login failed",
        "Twitter guest login failed",
        "Twitter tweet loading failed",
    )
    combined = "\n".join(sources.values())
    for message in expected:
        if combined.count(message) != 1:
            failures.append(f"privacy-safe category must appear exactly once: {message}")

    if failures:
        print("HomeScreen privacy contracts failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("HomeScreen privacy contracts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
