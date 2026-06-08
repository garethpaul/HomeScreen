# HomeScreen Response Nil-Safety Plan

status: completed

## Context

`HomeScreen` fetches Twitter profile data, tweet search data, upload responses,
and remote images. Several response paths force-unwrapped JSON fields or image
data, which can crash the app when Twitter responses are malformed, fields are
missing, or image downloads fail.

## Objectives

- Avoid force-unwrapping Twitter JSON response fields.
- Avoid force-unwrapping downloaded profile image data.
- Preserve existing Twitter sharing behavior when responses are valid.
- Extend the static baseline so response nil-safety stays covered.

## Work Items

1. Made `TweepPicture` parse `profile_image_url` through optional JSON dictionaries.
2. Made tweet search and upload JSON parsing avoid `json!` field access.
3. Made image downloading return an optional image and guarded profile image rendering.
4. Updated `scripts/check-baseline.py`, README, VISION, CHANGES, and this plan.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
