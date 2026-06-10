# Changes

## 2026-06-10

- Made profile-image lookup complete with `nil` on request, transport, JSON,
  and missing-field failures instead of silently abandoning the callback.
- Added pinned, read-only macOS CI for the canonical `make check` baseline.
- Made Xcode-enabled checks parse `HomeScreen.xcodeproj` instead of only
  printing a manual verification reminder.

## 2026-06-09

- Guarded tweet feed failures so Twitter search/login errors complete safely,
  clear loading state, and avoid force-casting returned tweet objects.
- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static iOS sharing baseline.
- Made screenshot lookup nil-safe when Photos returns no image or a size
  mismatch, preserving the user-initiated sharing flow without crashing.
- Added screenshot fallback handling in the main preview controller when Photos
  returns no screenshot image.
- Guarded share-screen Twitter session access before reading the profile user
  name for profile-image rendering.
- Removed deprecated update_with_media helper code so the active upload flow
  stays on the guarded media/upload path.
- Guarded JPEG media data creation before upload and used a valid screenshot
  compression quality.

## 2026-06-08

- Removed committed Fabric build credentials from the Xcode build phase and replaced them with local environment placeholders.
- Suppressed Fabric build-phase environment variable logging and enforced that guard in `make check`.
- Added a static `make check` baseline for project metadata, plist permissions, first-party Swift source, and documentation guardrails.
- Added the photo-library usage purpose string required for screenshot preview behavior on modern iOS.
- Guarded Twitter login, screenshot upload, latest-photo lookup, and hex color parsing edge cases without changing the legacy sharing flow.
- Removed raw Twitter media-upload response logging from first-party Swift code.
- Made Twitter JSON and profile image response handling nil-safe.
- Guarded optional Twitter write response data before JSON parsing.
