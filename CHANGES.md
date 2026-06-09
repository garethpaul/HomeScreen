# Changes

## 2026-06-09

- Made screenshot lookup nil-safe when Photos returns no image or a size
  mismatch, preserving the user-initiated sharing flow without crashing.
- Added screenshot fallback handling in the main preview controller when Photos
  returns no screenshot image.

## 2026-06-08

- Removed committed Fabric build credentials from the Xcode build phase and replaced them with local environment placeholders.
- Suppressed Fabric build-phase environment variable logging and enforced that guard in `make check`.
- Added a static `make check` baseline for project metadata, plist permissions, first-party Swift source, and documentation guardrails.
- Added the photo-library usage purpose string required for screenshot preview behavior on modern iOS.
- Guarded Twitter login, screenshot upload, latest-photo lookup, and hex color parsing edge cases without changing the legacy sharing flow.
- Removed raw Twitter media-upload response logging from first-party Swift code.
- Made Twitter JSON and profile image response handling nil-safe.
- Guarded optional Twitter write response data before JSON parsing.
