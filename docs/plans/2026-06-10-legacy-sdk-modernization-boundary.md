# Legacy SDK modernization boundary

status: completed

## Current boundary

This snapshot uses Swift 1-era syntax, an iOS 8.1 deployment target, and
vendored Fabric, Crashlytics, and TwitterKit binaries. Current Xcode and iOS SDK
releases cannot be treated as drop-in build environments for this code.

## Modernization sequence

1. Preserve the current static sharing and credential baseline before changing build metadata.
2. Replace retired Fabric, Crashlytics, and TwitterKit integrations with supported services.
3. Replace legacy Twitter REST and media-upload paths behind focused tests.
4. Convert Swift syntax, UIKit lifecycle methods, and photo APIs in reviewable stages.
5. Raise the deployment target only after login, feed, screenshot, and user-confirmed sharing behavior is verified on supported devices.

Until that work is scheduled, changes should remain compatible with the
archival baseline and must not imply that the app builds with a current SDK.
