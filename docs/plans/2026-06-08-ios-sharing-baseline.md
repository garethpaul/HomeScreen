# HomeScreen iOS Sharing Baseline Plan

status: completed

## Context

`HomeScreen` is a legacy Swift iOS app for previewing a user's latest home screen screenshot and sharing it through TwitterKit/Fabric-era APIs. This Linux host does not provide Xcode, so local verification needs a static baseline while full app builds remain a macOS/Xcode responsibility.

## Objectives

- Remove checked-in Fabric build credentials from the Xcode project.
- Keep photo-library, screenshot upload, Twitter session, and credential expectations explicit.
- Add a local `make check` baseline for plist parsing, Xcode metadata, first-party Swift source, and privacy guardrails.
- Preserve the legacy Xcode project and Twitter/Fabric framework inventory.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
