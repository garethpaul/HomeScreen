# HomeScreen

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/HomeScreen` is a Apple platform application or Objective-C/Swift sample. HomeScreen app for for sharing your #Homescreen

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: C/C++ headers (23), Swift (19).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `Crashlytics.framework` - source or example code
- `Fabric.framework` - source or example code
- `HomeScreen` - source or example code
- `HomeScreen.xcodeproj` - Xcode project file
- `HomeScreenTests` - source or example code
- `Makefile` - local verification entry point
- `SECURITY.md` - security reporting and disclosure guidance
- `scripts/check-baseline.py` - static iOS sharing and privacy verifier
- `TwitterKit.framework` - source or example code
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: Crashlytics.framework, Fabric.framework, HomeScreen, HomeScreenTests, TwitterKit.framework
- Dependency and build manifests: none detected
- Entry points or build surfaces: `make check`, HomeScreen.xcodeproj
- Test-looking files: HomeScreen/UpdateStatus.swift, HomeScreenTests/HomeScreenTests.swift, HomeScreenTests/Info.plist

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects
- Python 3 for local static verification on non-macOS hosts

### Setup

```bash
git clone https://github.com/garethpaul/HomeScreen.git
cd HomeScreen
make lint
make test
make build
make check
```

The setup commands above are derived from repository files. The checked-in frameworks are legacy Fabric/TwitterKit-era artifacts, so a full build may require matching Xcode and iOS SDK versions.

## Running or Using the Project

- Open `HomeScreen.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- Provide Fabric values through local Xcode build settings or environment-backed xcconfig values:
  - `FABRIC_API_KEY`
  - `FABRIC_BUILD_SECRET`
- Keep the `NSPhotoLibraryUsageDescription` plist entry aligned with the screenshot preview/share flow whenever photo access changes.

## Testing and Verification

Run the local static baseline:

```bash
make lint
make test
make build
make check
```

The `lint`, `test`, and `build` targets intentionally alias the static baseline
on hosts without the legacy Xcode toolchain, so the standard local gate commands
stay available while preserving the single source of truth.

The baseline runs `scripts/check-baseline.py`, parses plist/storyboard/workspace XML, checks the Xcode project metadata, verifies the legacy Swift and framework inventory, and guards against checked-in Fabric credential literals, missing photo-library permission text, unsafe empty-screenshot uploads, nil screenshot callbacks, screenshot fallback behavior, nil-safe Twitter/profile image and write response handling, missing Twitter session guards on the share screen, raw Twitter upload-response logging, deprecated update_with_media helper code, and invalid hex color parsing.

For full legacy verification on macOS, use Xcode's test action or `xcodebuild test` with the appropriate scheme and destination.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- The Fabric upload build phase reads `FABRIC_API_KEY` and `FABRIC_BUILD_SECRET` locally and skips the upload when either value is unset.
- Do not commit real Fabric, Twitter, signing, screenshot, or local xcconfig values to this repository.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include Crashlytics.framework/Versions/A/Headers/Crashlytics.h, HomeScreen/AppDelegate.swift, HomeScreen/LoginController.swift, HomeScreen/ShareController.swift, and 6 more.
- Review changes touching external API calls or credential-adjacent configuration; examples from the scan include Crashlytics.framework/Versions/A/Headers/Crashlytics.h, Crashlytics.framework/Versions/A/Resources/Info.plist, Fabric.framework/Versions/A/Headers/Fabric.h, Fabric.framework/Versions/A/Resources/Info.plist, and 6 more.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include Crashlytics.framework/Versions/A/Resources/Info.plist, Fabric.framework/Versions/A/Resources/Info.plist, HomeScreen/Info.plist, HomeScreen/Settings.bundle/Root.plist, and 6 more.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include HomeScreen/Post.swift, TwitterKit.framework/Versions/A/Headers/TWTRConstants.h.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include Crashlytics.framework/Versions/A/Resources/Info.plist, Fabric.framework/Versions/A/Resources/Info.plist, HomeScreen/Images.swift, HomeScreen/Info.plist, and 6 more.
- Review changes touching database, model, or persistence code; examples from the scan include HomeScreen/TweetsController.swift, TwitterKit.framework/Versions/A/Headers/TWTRTweetTableViewCell.h, TwitterKit.framework/Versions/A/Headers/TWTRTweetViewDelegate.h.
- Home screen screenshots can reveal private apps, messages, accounts, or location hints. Keep uploads user-initiated and avoid raw response or image logging.
- Treat Twitter session state as optional on presentation paths; expired or
  missing sessions should not crash profile-image rendering.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-response-nil-safety.md` for the Twitter/image response nil-safety guardrail.
- See `docs/plans/2026-06-08-write-response-data-guard.md` for the Twitter write response data guardrail.
- See `docs/plans/2026-06-09-screenshot-nil-safety.md` for the Photos screenshot nil-safety guardrail.
- See `docs/plans/2026-06-09-share-session-guard.md` for the share-screen Twitter session guardrail.
- See `docs/plans/2026-06-09-deprecated-update-with-media-removal.md` for the
  deprecated update_with_media removal guardrail.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local gate alias guardrail.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing changes to plist files, Swift sources, Xcode project metadata, credential handling, or screenshot-sharing behavior.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
