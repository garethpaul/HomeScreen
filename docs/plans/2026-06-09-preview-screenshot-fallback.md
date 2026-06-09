# HomeScreen Preview Screenshot Fallback

status: completed

## Context

`getScreenshotImage` now completes with `UIImage?`, but the main preview
controller still declared the callback image as non-optional and always assigned
it to the preview. When Photos returned no matching screenshot, the preview path
needed to fall back to the default image just like the empty-library path.

## Objectives

- Update the preview controller to accept the optional screenshot callback.
- Show the default image when Photos returns no screenshot.
- Preserve the existing preview behavior when a matching screenshot is found.
- Extend the static baseline so nil-safe screenshot fallback stays covered
  without Xcode locally.

## Verification

- `make check`
- `git diff --check`
