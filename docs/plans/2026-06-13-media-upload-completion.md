# Media Upload Completion

status: completed

## Context

`UploadMedia` calls its completion only when Twitter returns a JSON
`media_id_string`. Request-construction, transport, missing-data, malformed-JSON,
and missing-field failures either log raw error objects or return without a
completion result.

The share caller therefore has no deterministic failure signal, and transport
details may be written to device logs during a screenshot-sharing operation.

## Priority

Home-screen screenshots can contain private information. The upload boundary
should complete exactly once with an explicit optional result and avoid logging
request or connection details.

## Requirements

- R1. Change `UploadMedia` completion to return `String?`.
- R2. Return the media identifier only after valid response data, JSON object,
  and `media_id_string` extraction.
- R3. Return `nil` for request-construction, transport, missing-data,
  deserialization, or missing-ID failures.
- R4. Remove raw upload request and connection error logging.
- R5. Update `ShareController` to call `UpdateStatus` only for a non-nil media
  identifier.
- R6. Keep upload/status endpoints, JPEG generation, and user-initiated share
  behavior unchanged.
- R7. Extend the deterministic baseline with function-scoped completion and
  logging contracts plus completed plan evidence.

## Implementation Units

### U1. Make upload completion total

- **Files:** `HomeScreen/Upload.swift`
- Add explicit success and failure completion paths without logging transport
  objects.

### U2. Guard status submission

- **Files:** `HomeScreen/ShareController.swift`, `scripts/check-baseline.py`
- Accept the optional media ID and submit only after successful extraction.

### U3. Document the privacy boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record deterministic upload failure signaling and log suppression.

## Scope Boundaries

- Do not re-enable the deprecated `update_with_media` helper.
- Do not change Twitter endpoints, credentials, image encoding, or status text.
- Do not modernize Swift, UIKit, Fabric, Crashlytics, or TwitterKit in this
  focused change.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- Hostile mutations removing optional completion, success return, each failure
  class, caller guarding, completed status, or verification evidence must be
  rejected.

## Work Completed

- Changed `UploadMedia` to complete with an optional media identifier.
- Added explicit nil completion for handled callback failures and request
  construction failure while preserving the successful media ID path.
- Removed upload request and connection error logging.
- Guarded status submission on a non-nil uploaded media identifier.
- Updated static contracts and privacy, vision, README, and change docs.

## Verification Completed

- All four Make gates passed locally and reported that `xcodebuild` was
  unavailable, so only the static iOS sharing baseline ran on this host.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Eight isolated hostile mutations were rejected: optional-signature removal,
  success-return removal, callback and request failure removal, raw error
  logging, caller-guard removal, stale plan status, and missing evidence.
