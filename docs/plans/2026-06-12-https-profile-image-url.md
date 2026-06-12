# HTTPS Profile Image URL

status: completed

## Context

`TweepPicture` requests user metadata over HTTPS but extracts the legacy
`profile_image_url` response field. Twitter historically returned plain-HTTP
values in that field, and the app then passes the dynamic string to
`NSURLConnection`. Because the insecure scheme is response data rather than a
source literal, the existing static endpoint scan cannot detect it.

Twitter also provides `profile_image_url_https` specifically for encrypted
profile-image transport.

## Priority

Profile images are fetched on the sharing screen. Requiring the HTTPS response
field avoids cleartext image requests, App Transport Security failures, and
network tampering without changing the login or sharing workflow.

## Requirements

- R1. `TweepPicture` must read only `profile_image_url_https` from Twitter user
  metadata.
- R2. Missing, malformed, or non-string HTTPS profile fields must continue to
  complete with `nil` exactly once.
- R3. Existing request, JSON, session, and downloader guards must remain intact.
- R4. The static baseline must reject restoration of the non-HTTPS response
  key.
- R5. No SDK, project, or deployment-target modernization is included.

## Implementation Units

### U1. Select the encrypted response field

- **Files:** `HomeScreen/TweepPicture.swift`
- Replace the legacy profile-image response key with
  `profile_image_url_https` while preserving optional casts and completion
  behavior.

### U2. Extend the sharing baseline

- **Files:** `scripts/check-baseline.py`
- Require the HTTPS field and reject the legacy key as an exact JSON lookup.

### U3. Update maintenance documentation

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record the dynamic-response HTTPS boundary.

## Scope Boundaries

- Do not add fallback to plain HTTP.
- Do not change image decoding, Twitter authentication, or sharing UI.
- Do not replace retired SDK dependencies in this change.

## Verification

- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- A mutation restoring `profile_image_url` must fail the baseline.

Completed on 2026-06-12 with the static sharing baseline, Python checker
compilation, diff hygiene, and a legacy response-key mutation rejected.
