# Hosted Project Validation

status: completed

## Context

The local baseline covered source, privacy metadata, documentation, and Xcode
project inventory, but it only printed a reminder when Xcode was installed.
The repository also had no hosted check to catch project-file parse failures.

## Completed Scope

- Added a pinned GitHub Actions workflow with read-only repository permissions.
- Runs the canonical `make check` gate on a bounded `macos-15` job.
- Parses `HomeScreen.xcodeproj` with `xcodebuild -list` whenever Xcode is
  available.
- Kept credential-dependent Twitter/Fabric behavior, signing, simulator tests,
  and end-to-end sharing outside the hosted baseline.
- Extended the checker and documentation to preserve the CI contract.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- workflow YAML parse
- `git diff --check`
