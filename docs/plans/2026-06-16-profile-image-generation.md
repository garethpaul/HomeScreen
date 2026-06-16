# Guard Profile Image Generations

Status: Planned

## Problem

`ShareController` starts an asynchronous Twitter profile lookup followed by an
image download, but the nested callbacks have no ownership tied to the visible
controller lifecycle. If the share screen disappears before either callback
finishes, the request chain can retain the controller and later assign and
reveal an avatar on a stale screen.

## Priorities

1. P0: Reject profile lookup and download callbacks after the share controller
   disappears.
2. P0: Preserve success-only avatar assignment and reveal ordering.
3. P1: Add mutation-sensitive lifecycle and guidance contracts without
   changing retired TwitterKit or network behavior.

## Requirements

1. Each accepted profile-image load must capture a generation owned by the
   current `ShareController` lifecycle.
2. Both the profile URL callback and image download callback must reject stale
   generations before starting later work or mutating UI.
3. `viewWillDisappear` must invalidate profile callbacks as well as active post
   callbacks.
4. A successful current-generation image must still be transformed, assigned,
   and revealed in that order on the existing main-queue callback.
5. Missing sessions, failed profile lookups, invalid URLs, failed downloads,
   and stale callbacks must leave the avatar hidden.
6. Portable checks, project guidance, and this plan must retain truthful local
   verification and the unavailable-Xcode boundary.

## Implementation Units

### U1. Profile callback ownership

**File:** `HomeScreen/ShareController.swift`

Add profile generation state and small ownership helpers. Capture the active
generation before starting `TweepPicture`, check it before starting the image
download, and check it again before assigning or revealing the image.

### U2. Lifecycle and ordering contracts

**File:** `scripts/check-baseline.py`

Add function-scoped contracts for generation capture, stale rejection at both
callback levels, disappearance invalidation, and success-only assignment then
reveal ordering. Bind the checks to this completed plan and maintained
guidance.

### U3. Maintained evidence

**Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, and this plan.

Document that asynchronous avatar results are lifecycle-owned and that local
Linux verification remains static rather than an iOS runtime claim.

## Test Scenarios

- A current profile URL callback may start one image download.
- A stale profile URL callback cannot start an image download.
- A current successful image callback transforms, assigns, and then reveals
  the avatar.
- A stale or failed image callback cannot assign or reveal the avatar.
- Disappearance invalidates both profile and post callback generations.
- Removing generation capture, either stale check, disappearance invalidation,
  success ordering, guidance, or completed evidence fails the portable gate.

## Scope Boundaries

- Do not modernize Swift syntax, UIKit, Fabric, Crashlytics, TwitterKit, or the
  project format.
- Do not change endpoints, retries, caching, image sizing, placeholder UI,
  session handling, or post submission behavior.
- Do not edit vendored frameworks, Xcode project metadata, workflows, or
  dependency artifacts.
- Simulator, physical-device, live Twitter, and rendered UI behavior remain
  outside Linux validation.

## Verification

- Run `make lint`, `make test`, `make build`, and `make check` from the
  repository plus the absolute Makefile from an external directory.
- Reject isolated hostile mutations for generation capture, both stale checks,
  disappearance invalidation, assignment/reveal ordering, guidance, and plan
  status.
- Compile the Python checker and audit the exact diff, generated artifacts,
  forbidden project/vendor paths, secrets, conflict markers, and whitespace.
