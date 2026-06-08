## HomeScreen Vision

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

Next priorities:

- Add README setup, permissions, and verification instructions
- Move Twitter configuration into documented local settings
- Modernize Swift, photo APIs, and Twitter/Fabric dependencies in a dedicated pass
- Add tests or manual checks for image selection and share behavior

Contribution rules:

- One PR = one focused photo, Twitter, upload, UI, or documentation change.
- Verify photo-library and sharing behavior on a device or simulator.
- Keep credentials, screenshots, and signing files out of git.
- Document any new network behavior involving images or posts.

## Security And Privacy

Home screen screenshots and photo-library contents can reveal personal
information. The app should keep sharing user-initiated and avoid uploading or
logging images without explicit action.

Twitter credentials and session data must remain out of source control.

## What We Will Not Merge (For Now)

- Hardcoded Twitter/Fabric credentials
- Silent screenshot upload or background photo access
- Analytics around private images or account data
- Broad dependency migration bundled with sharing behavior changes
