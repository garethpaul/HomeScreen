#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check-privacy-contracts.py"
FILES = (
    "HomeScreen/TweepPicture.swift",
    "HomeScreen/TwitterRESTAPI.swift",
    "HomeScreen/TweetsController.swift",
)


def run_checker(root):
    return subprocess.run(
        ["python3", str(CHECKER), str(root)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def mutate(relative_path, old, new):
    with tempfile.TemporaryDirectory() as temporary_directory:
        mutation_root = Path(temporary_directory)
        for source_relative_path in FILES:
            destination = mutation_root / source_relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source_relative_path, destination)
        path = mutation_root / relative_path
        source = path.read_text(encoding="utf-8")
        if source.count(old) != 1:
            raise AssertionError(f"Mutation target must be unique in {relative_path}: {old}")
        path.write_text(source.replace(old, new, 1), encoding="utf-8")
        result = run_checker(mutation_root)
        if result.returncode == 0:
            raise AssertionError(f"Mutation survived in {relative_path}: {old}")


def main():
    result = run_checker(ROOT)
    if result.returncode != 0:
        raise SystemExit(result.stderr)

    mutations = (
        ("HomeScreen/TweepPicture.swift", 'println("Twitter profile lookup failed")', 'println("Error: \\(connectionError)")'),
        ("HomeScreen/TweepPicture.swift", 'println("Twitter profile request could not be created")', 'println("Error: \\(clientError)")'),
        ("HomeScreen/TwitterRESTAPI.swift", 'println("Twitter search login failed")', 'println("error: \\(error.localizedDescription)")'),
        ("HomeScreen/TweetsController.swift", 'println("Twitter tweet loading failed")', 'println(error)'),
    )
    for mutation in mutations:
        mutate(*mutation)

    print(f"HomeScreen privacy tests passed ({len(mutations)} hostile mutations rejected).")


if __name__ == "__main__":
    main()
