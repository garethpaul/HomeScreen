# Reveal Successful Profile Images

status: completed

## Context

The share screen hides its profile image while loading. After a successful
HTTPS lookup, download, and circular image transform, it assigns the image but
sets `profilePic.hidden` to `true` again. The successfully loaded avatar is
therefore never visible.

## Requirements

- R1. The profile image must remain hidden before loading begins.
- R2. A successful image callback must assign the transformed image before
  revealing the image view.
- R3. Failed profile lookup, URL construction, download, or image callbacks
  must leave the image view hidden.
- R4. Profile URL selection, request behavior, credentials, and session guards
  must remain unchanged.
- R5. The deterministic checker must isolate the success callback and reject a
  missing, premature, or inverted reveal.

## Scope Boundaries

- Do not change Twitter endpoints, parameters, authentication, or completion
  behavior.
- Do not edit vendored frameworks, Pods, lockfiles, Xcode project metadata, or
  hosted workflow configuration.
- Do not modernize the archival Swift 1/iOS 8.1 syntax or SDK stack.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- Hostile mutations must reject removal of the reveal, a still-hidden success
  state, reveal before assignment, stale plan status, and missing verification
  evidence.

## Work Completed

- Kept the avatar hidden while profile lookup and download are unresolved.
- Revealed the image view only after the downloaded image was transformed and
  assigned to `profilePic`.
- Added callback-scoped ordering and visibility-count contracts without
  changing profile lookup, transport, authentication, or completion behavior.
- Updated the sharing, security, vision, and change documentation.

## Verification Completed

- All four Make gates passed locally and reported that `xcodebuild` was
  unavailable, so only the static iOS sharing baseline ran on this host.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Six isolated hostile mutations were rejected: removed reveal, inverted
  success visibility, reveal before assignment, removed initial hiding, stale
  plan status, and missing verification evidence.
- Exact-base comparison confirmed vendored frameworks, Pods, lockfiles, Xcode
  project metadata, and hosted workflow configuration remained unchanged.
- Intended-file generated-artifact and secret-pattern scans passed.
- Hosted macOS project validation and CodeQL evidence is recorded separately
  after push; this plan claims only the completed local static verification.
