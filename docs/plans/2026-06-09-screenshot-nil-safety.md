# HomeScreen Screenshot Nil-Safety

status: completed

## Context

`getScreenshotImage` asks Photos for the latest screenshot-sized image before
the share flow uploads it. The Photos callback passes an implicitly unwrapped
`UIImage!`, so missing image data could crash the app even after the empty
photo-fetch guard.

## Objectives

- Return an optional screenshot from `getScreenshotImage`.
- Complete with `nil` when no matching image is available or Photos returns no
  image.
- Keep `ShareController` from setting or uploading a missing screenshot.
- Extend `scripts/check-baseline.py` so the nil-safe screenshot contract stays
  covered without Xcode locally.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
