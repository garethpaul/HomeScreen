---
title: HomeScreen async ownership deep review
status: completed
date: 2026-06-19
---

# HomeScreen Async Ownership Deep Review

## Scope

Review the stacked PRs #3 through #9 at `898c9019f78d1f37341af9ceae212ce86b5fc8b0`, following media upload, status creation, screenshot selection, profile image loading, and tweet feed callbacks through their UI ownership boundaries.

## Findings

1. `Post.swift` configured high-quality Photos options but passed `nil` to `requestImageForAsset`. The default opportunistic delivery mode can call the result handler more than once, so one screenshot request could produce multiple completion calls. This behavior originated in the first commit, `404f423`.
2. Screenshot callbacks in both controllers strongly owned the controller and had no generation boundary. A result from an older application-active or composer request could therefore replace newer state or retain a dismissed composer.
3. Share upload, status, and queued completion closures strongly owned the composer. The post generation check prevented stale dismissal, but did not release a dismissed controller while legacy network work remained pending. This ownership shape was carried forward by `789c0ab`.
4. Starting a profile request did not clear an already-visible avatar. A later request or reused composer could display an image that belonged to the prior generation until the replacement finished.
5. The final Twitter model callback read `tweetGeneration` before returning to the main queue. That introduced an unsynchronized cross-queue controller-state read in `3233255`; the existing main-queue completion already provides the authoritative stale check.

## Design Decision

Keep the repair at the current ownership boundaries. Pass the configured Photos options, serialize screenshot completion on the main queue with an exactly-once guard, generation-bind screenshot consumers, weakly own controllers across legacy network callbacks, clear stale profile imagery when a new generation begins, and defer the final tweet generation read to the existing main-queue completion helper.

A generic callback coordinator or Swift modernization would widen the archival project risk without improving these specific invariants, so both are deferred.

## Verification Completed

- Observed the new async contract fail on every finding before changing production code.
- `make check` passed with the baseline plus seven hostile mutations covering Photos option bypass, repeated completion, screenshot generation bypass, strong post capture, stale profile visibility, home-screen generation bypass, and off-main tweet generation access.
- `python3 -m py_compile scripts/check-baseline.py scripts/check-async-contracts.py scripts/test-async-contracts.py` passed.
- `xcodebuild -list -project HomeScreen.xcodeproj` passed.
- A current Xcode simulator build remains unsupported because the archival target has no supported `SWIFT_VERSION` and targets iOS 8.1.
- No live Twitter authentication, upload, status creation, Photos library interaction, simulator flow, or physical-device flow is claimed.

## Primary Evidence

- Apple documents that opportunistic Photos delivery may invoke the image result handler more than once, while high-quality delivery provides only the highest-quality result.
- Current source and bounded history establish the callback ownership and provenance described above.
