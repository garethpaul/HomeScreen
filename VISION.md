## HomeScreen Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

HomeScreen is an iOS app for sharing a user's home screen image and browsing
posts tagged with `#Homescreen`.

The repository is useful as a legacy Swift sample combining photo library access,
TwitterKit/Fabric integration, media upload, and status search.

The goal is to keep the screenshot-sharing flow understandable while making
photo-library, Twitter, and credential boundaries explicit.

The current focus is:

Priority:

- Preserve latest-image selection, preview, and sharing flow
- Keep Twitter REST search and upload behavior easy to inspect
- Avoid committing Fabric/Twitter credentials, signing material, or private images
- Maintain security policy and legacy project context
- Keep `scripts/check-baseline.py` passing for credential placeholders, plist
  permissions, nil-safe response parsing, Swift source guardrails, and static
  project inventory
- Keep `make lint`, `make test`, `make build`, and `make check` available as
  local verification gates
- Keep JPEG media data generation guarded before screenshot uploads
- Keep tweet feed failures recoverable so search/login errors clear loading
  state instead of crashing or hanging
- Keep profile-image lookup completion total across request and response
  failures so presentation setup does not hang
- Keep pinned macOS CI parsing `HomeScreen.xcodeproj` through the canonical
  `make check` gate

Next priorities:

- Move Twitter configuration into documented local settings
- Modernize Swift, photo APIs, and Twitter/Fabric dependencies in a dedicated pass
- Add tests or manual checks for image selection and share behavior

Contribution rules:

- One PR = one focused photo, Twitter, upload, UI, or documentation change.
- Verify photo-library and sharing behavior on a device or simulator.
- Keep credentials, screenshots, and signing files out of git.
- Document any new network behavior involving images or posts.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Home screen screenshots and photo-library contents can reveal personal
information. The app should keep sharing user-initiated and avoid uploading or
logging images without explicit action.

Twitter credentials and session data must remain out of source control.

Current baseline: `make lint`, `make test`, `make build`, and `make check`
run `scripts/check-baseline.py` without Xcode.
It verifies that the Fabric build phase uses local placeholders, the
photo-library permission describes screenshot sharing, uploads require a loaded
image, Photos screenshot callbacks and screenshot fallback behavior are
nil-safe, Twitter JSON, profile image, and write response data handling are
nil-safe, share-screen Twitter session access is guarded, raw upload responses
are not logged, deprecated update_with_media helper code stays removed, and the
legacy project/framework inventory remains visible. JPEG media data creation
must use a valid compression quality and be guarded before upload.
Tweet feed failures must complete safely and clear loading state when Twitter
search or guest-login setup fails.
On macOS, the same baseline must use `xcodebuild -list` to confirm that Xcode
can parse the project. Functional sharing remains a separate manual check
because it depends on credentials, signing, device state, and retired services.

## Modernization Boundary

The current repository preserves a Swift 1-era, iOS 8.1 application with
retired Fabric, Crashlytics, and TwitterKit binaries. Modernization must replace
those integrations, isolate Twitter REST and media-upload behavior, then convert
Swift and UIKit APIs in independently verifiable stages.

## What We Will Not Merge (For Now)

- Hardcoded Twitter/Fabric credentials
- Silent screenshot upload or background photo access
- Analytics around private images or account data
- Broad dependency migration bundled with sharing behavior changes

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
