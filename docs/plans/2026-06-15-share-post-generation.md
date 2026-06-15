# Guard Share Post Generations

status: planned

## Context

`ShareController.post()` has no in-flight ownership. Repeated taps can start
parallel media uploads and status updates, and each successful callback can
perform the cancel segue. A callback can also arrive after the user closes or
navigates away from the composer and attempt a second stale dismissal.

## Requirements

- R1. Allow at most one active post submission per visible share controller.
- R2. Assign each accepted submission a generation captured by every nested
  media and status callback.
- R3. Resolve submission state on the main queue for both success and failure.
- R4. Dismiss only when the completion generation is still current, the
  submission remains active, and status creation succeeded.
- R5. Invalidate active callbacks before explicit close and whenever the
  controller disappears.
- R6. Preserve screenshot/JPEG creation, Twitter endpoints, text and media-ID
  flow, profile-image behavior, and success-only dismissal.
- R7. Add mutation-sensitive source, ordering, lifecycle, guidance, and
  completed-plan contracts.

## Implementation Units

### U1. Submission ownership

- **File:** `HomeScreen/ShareController.swift`
- Add in-flight and generation state plus main-queue completion and invalidation
  helpers.
- Reject duplicate taps while a submission is active.

### U2. Callback and lifecycle ordering

- Capture the accepted generation before media upload.
- Route media failure and status success/failure through one completion helper.
- Invalidate before the close segue and from `viewWillDisappear`.

### U3. Repository evidence

- **Files:** `scripts/check-baseline.py`, `AGENTS.md`, `README.md`, `SECURITY.md`,
  `VISION.md`, `CHANGES.md`
- Add function-scoped contracts and synchronized maintenance guidance.

## Scope Boundaries

- Do not modernize archival Swift syntax, UIKit, Fabric, Crashlytics, or
  TwitterKit.
- Do not add retry, alert, progress UI, draft persistence, or service changes.
- Do not edit vendored frameworks, project metadata, lockfiles, or workflows.

## Verification Plan

- Run all four Make gates and the absolute Makefile from `/tmp`.
- Reject mutations that remove duplicate suppression, generation capture,
  media-failure release, main-queue completion, stale-generation rejection,
  close invalidation, disappearance invalidation, guidance, or completed-plan
  evidence.
- Run Python checker compilation, diff, artifact, vendored/project/lockfile,
  credential-pattern, conflict-marker, and whitespace audits.
- Push a stacked pull request and take one bounded exact-head hosted and
  security-alert snapshot without polling.

