# Dismiss Share Composer After Status Success

status: planned

## Context

`ShareController.post()` starts media upload and immediately performs the
cancel segue. The composer therefore disappears before media upload or status
creation succeeds, and every upload, request-construction, transport, or
malformed-response failure looks like a successful share.

## Requirements

- R1. `UpdateStatus` must complete exactly once with a Boolean result.
- R2. Status creation succeeds only when the Twitter response contains a valid
  nonblank status identifier.
- R3. Request-construction, transport, missing-data, malformed-JSON, and
  missing-identifier failures must complete with `false` without logging raw
  transport objects.
- R4. The share composer must dismiss only after successful media upload and
  successful status creation.
- R5. The success dismissal must run on the main queue; failure paths must keep
  the composer visible.
- R6. Existing Twitter endpoints, authentication, text, JPEG generation, media
  identifier flow, profile image behavior, and close-button behavior remain
  unchanged.
- R7. The deterministic baseline must enforce completion totality, response
  validation, callback ordering, main-queue dismissal, and completed plan
  evidence.

## Implementation Units

### U1. Make status submission total

- **Files:** `HomeScreen/UpdateStatus.swift`
- Add a Boolean completion and explicit success/failure response paths.
- Treat only a nonblank `id_str` as successful status creation.

### U2. Make dismissal success-only

- **Files:** `HomeScreen/ShareController.swift`
- Nest dismissal after successful status completion and dispatch it to the main
  queue.
- Remove the unconditional post-start segue while preserving the explicit close
  action.

### U3. Enforce and document the lifecycle

- **Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
  `CHANGES.md`, `AGENTS.md`
- Add function-scoped contracts and synchronized operational guidance.

## Scope Boundaries

- Do not modernize archival Swift syntax, UIKit, Fabric, Crashlytics, or
  TwitterKit.
- Do not add retry, alert, progress, draft persistence, or duplicate-submit UI.
- Do not edit vendored frameworks, project metadata, lockfiles, or workflow
  configuration.

## Verification Plan

- Run focused static contracts, Python checker compilation, all four Make gates,
  and the absolute Makefile gate from `/tmp`.
- Reject mutations that remove status failure completion, response-ID
  validation, success nesting, main-queue dispatch, or plan evidence.
- Run diff, artifact, vendored-path, and changed-line credential audits before
  committing.
