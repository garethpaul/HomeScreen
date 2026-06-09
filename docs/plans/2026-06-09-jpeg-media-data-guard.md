# JPEG Media Data Guard

status: completed

## Context

The share screen uploaded JPEG data from the loaded screenshot image before
posting the Twitter status. The previous call used an invalid compression
quality and assumed JPEG encoding always produced media data, so the upload path
could proceed without a valid encoded payload.

## Completed Scope

- Guarded `UIImageJPEGRepresentation` with optional binding before upload.
- Switched screenshot JPEG compression quality to the valid `1.0` range.
- Kept the existing image-presence guard before media encoding.
- Extended the static baseline to preserve the media-data guard.
- Updated README, VISION, and CHANGES with the upload guardrail.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
