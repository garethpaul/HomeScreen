# Changes

## 2026-06-08

- Removed committed Fabric build credentials from the Xcode build phase and replaced them with local environment placeholders.
- Suppressed Fabric build-phase environment variable logging and enforced that guard in `make check`.
- Added a static `make check` baseline for project metadata, plist permissions, first-party Swift source, and documentation guardrails.
- Added the photo-library usage purpose string required for screenshot preview behavior on modern iOS.
- Guarded Twitter login, screenshot upload, latest-photo lookup, and hex color parsing edge cases without changing the legacy sharing flow.
- Removed raw Twitter media-upload response logging from first-party Swift code.
- Made Twitter JSON and profile image response handling nil-safe.
