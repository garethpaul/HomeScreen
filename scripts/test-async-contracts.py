#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check-async-contracts.py"
FILES = (
    "HomeScreen/Post.swift",
    "HomeScreen/ShareController.swift",
    "HomeScreen/TweetsController.swift",
    "HomeScreen/ViewController.swift",
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
        if old not in source:
            raise AssertionError(f"Mutation target missing in {relative_path}: {old}")
        path.write_text(source.replace(old, new, 1), encoding="utf-8")
        result = run_checker(mutation_root)
        if result.returncode == 0:
            raise AssertionError(f"Mutation survived in {relative_path}: {old}")


def main():
    result = run_checker(ROOT)
    if result.returncode != 0:
        raise SystemExit(result.stderr)

    mutations = (
        ("HomeScreen/Post.swift", "options: options", "options: nil"),
        ("HomeScreen/Post.swift", "if completionDelivered", "if false"),
        ("HomeScreen/ShareController.swift", "controller.screenshotGeneration != generation", "false"),
        ("HomeScreen/ShareController.swift", "UploadMedia(media) { [weak self]", "UploadMedia(media) {"),
        (
            "HomeScreen/ShareController.swift",
            "profilePic.image = nil\n        profilePic.hidden = true",
            "profilePic.image = nil\n        profilePic.hidden = false",
        ),
        ("HomeScreen/ViewController.swift", "controller.screenshotGeneration != generation", "false"),
        # Neuter mutations: the guard is wrapped in `if false { ... }` so it is
        # dead, while every fragment the gate asserts stays byte-identical, live
        # and uncommented. Fragment-presence assertions -- with or without
        # comment stripping -- pass these; only a whole-construct pin rejects them.
        (
            "HomeScreen/Post.swift",
            "if completionDelivered {\n                return\n            }\n            completionDelivered = true",
            "if false {\n                if completionDelivered {\n                    return\n                }\n            }\n            completionDelivered = true",
        ),
        (
            "HomeScreen/ShareController.swift",
            "if controller.screenshotGeneration != generation {\n                        return\n                    }",
            "if false {\n                        if controller.screenshotGeneration != generation {\n                            return\n                        }\n                    }",
        ),
        (
            "HomeScreen/ViewController.swift",
            "if controller.screenshotGeneration != generation {\n                        return\n                    }",
            "if false {\n                        if controller.screenshotGeneration != generation {\n                            return\n                        }\n                    }",
        ),
        (
            "HomeScreen/TweetsController.swift",
            "var loadedTweetModels: [TWTRTweet] = []",
            "if controller.tweetGeneration != generation { return }\n                            var loadedTweetModels: [TWTRTweet] = []",
        ),
    )
    for mutation in mutations:
        mutate(*mutation)

    print(f"HomeScreen async ownership tests passed ({len(mutations)} hostile mutations rejected).")


if __name__ == "__main__":
    main()
