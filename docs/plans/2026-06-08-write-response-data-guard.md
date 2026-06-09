# HomeScreen Write Response Data Guard

status: completed

## Context

`HomeScreen` has legacy Twitter write paths for media and status updates plus a
generic URL POST helper. Their response `data` values are optional in the
callbacks, so they need the same guard used by the profile image path before
passing bytes to `NSJSONSerialization` or `NSString`.

## Objectives

- Guard optional response data before JSON deserialization in write-response
  paths.
- Guard invalid generic POST URLs before building `NSMutableURLRequest`.
- Preserve the existing success/error request flow.
- Extend `scripts/check-baseline.py` so first-party Swift cannot pass optional
  `data` directly to `JSONObjectWithData`.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
