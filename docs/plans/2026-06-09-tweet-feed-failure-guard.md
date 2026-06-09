# Tweet Feed Failure Guard

status: completed

## Context

The tweet feed path already parsed Twitter response payloads defensively, but
some setup failures still never called their completion handlers. A failed
search login, request setup error, empty search result, or guest-login failure
could leave the feed spinner active. The tweet loader also force-cast returned
tweet objects before adding them to the table.

## Completed Scope

- Made Twitter search complete with an empty result when login, request setup,
  or connection setup fails.
- Guarded missing search login errors before printing diagnostic text.
- Stopped the feed loading indicator when there are no tweet IDs to load.
- Guarded guest-login failure before requesting tweet objects.
- Replaced loaded tweet force casts with optional casts.
- Extended the static baseline and documentation so tweet feed failures stay
  recoverable.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
