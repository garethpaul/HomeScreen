# Twitter Read Error Logging

status: completed

## Scope

Keep profile lookup, search, guest-login, and tweet-model failures total without
printing raw Twitter transport, request, or localized error details.

## Work Completed

- Replaced profile lookup, search request, search login, guest login, and tweet
  model error interpolation with stable privacy-safe categories.
- Preserved every existing empty/nil completion path.
- Added a focused checker and four hostile mutations covering connection,
  request-construction, localized, and model-load error detail leaks.
- Bound the new checker to `make check` and synchronized repository guidance.

## Verification

- `make check`
- four hostile mutations
- external-directory Make execution
- `git diff --check`
- Codex review was attempted once for PR #12 and skipped after HTTP 401.
