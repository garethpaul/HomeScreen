# HomeScreen Share Session Guard

status: completed

## Context

`ShareController` fetches the current Twitter user's profile image when the
share screen loads. The code chained `Twitter.sharedInstance().session().userName`
directly, which could crash if the session is missing or expires between launch
and the share view being presented.

## Objectives

- Guard the Twitter session before reading the profile user name.
- Preserve profile-image loading when a valid session exists.
- Keep screenshot preview and upload behavior unchanged.
- Extend the static baseline so share-screen session access remains guarded
  without requiring local Xcode.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
