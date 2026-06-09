# Deprecated Update With Media Removal

status: completed

## Context

The app already has an active `Upload.swift` media upload path that uses
Twitter's `media/upload.json`, parses `media_id_string` safely, and feeds that
identifier into status posting. A second legacy helper in `UploadMedia.swift`
still targeted the deprecated `statuses/update_with_media.json` endpoint, never
called its completion, and expanded the app's network surface.

## Completed Scope

- Removed the obsolete `UploadMedia(media:completion:)` implementation while
  keeping the Xcode-referenced source file present.
- Preserved the active `Upload.swift` path that uploads media first and returns
  a guarded `media_id_string`.
- Extended the static baseline to reject `statuses/update_with_media.json` and
  the obsolete helper signature.
- Updated README, VISION, and CHANGES so the upload surface is documented.

## Verification

- `make check`
- `git diff --check`
