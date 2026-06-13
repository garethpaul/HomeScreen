#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-ios-sharing-baseline.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
SCREENSHOT_PLAN = ROOT / "docs/plans/2026-06-09-screenshot-nil-safety.md"
SCREENSHOT_FALLBACK_PLAN = ROOT / "docs/plans/2026-06-09-preview-screenshot-fallback.md"
SHARE_SESSION_PLAN = ROOT / "docs/plans/2026-06-09-share-session-guard.md"
DEPRECATED_UPLOAD_PLAN = ROOT / "docs/plans/2026-06-09-deprecated-update-with-media-removal.md"
JPEG_MEDIA_PLAN = ROOT / "docs/plans/2026-06-09-jpeg-media-data-guard.md"
TWEET_FEED_PLAN = ROOT / "docs/plans/2026-06-09-tweet-feed-failure-guard.md"
MODERNIZATION_PLAN = ROOT / "docs/plans/2026-06-10-legacy-sdk-modernization-boundary.md"
HOSTED_VALIDATION_PLAN = ROOT / "docs/plans/2026-06-10-hosted-project-validation.md"
TWEEP_PICTURE_PLAN = ROOT / "docs/plans/2026-06-10-profile-image-completion.md"
HTTPS_PROFILE_IMAGE_PLAN = ROOT / "docs/plans/2026-06-12-https-profile-image-url.md"
MEDIA_UPLOAD_PLAN = ROOT / "docs/plans/2026-06-13-media-upload-completion.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def parse_plist(relative_path, failures):
    path = ROOT / relative_path
    try:
        with path.open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def parse_xml(relative_path, failures):
    try:
        ET.parse(str(ROOT / relative_path))
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def first_party_swift():
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in sorted((ROOT / "HomeScreen").glob("*.swift"))
    )


def extract_braced_block(source, marker):
    marker_start = source.find(marker)
    if marker_start < 0:
        return None
    brace_start = source.find("{", marker_start)
    if brace_start < 0:
        return None
    depth = 0
    for index in range(brace_start, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[marker_start:index + 1]
    return None


def main():
    failures = []
    required_files = [
        ".gitignore",
        "CHANGES.md",
        ".github/workflows/check.yml",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "HomeScreen.xcodeproj/project.pbxproj",
        "HomeScreen.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "HomeScreen/Info.plist",
        "HomeScreen/Main.storyboard",
        "HomeScreen/Base.lproj/Main.storyboard",
        "HomeScreen/Base.lproj/LaunchScreen.xib",
        "HomeScreen/Settings.bundle/Root.plist",
        "HomeScreen/AppDelegate.swift",
        "HomeScreen/LoginController.swift",
        "HomeScreen/Post.swift",
        "HomeScreen/ShareController.swift",
        "HomeScreen/Upload.swift",
        "HomeScreen/UploadMedia.swift",
        "HomeScreen/Hex.swift",
        "HomeScreen/TwitterRESTAPI.swift",
        "HomeScreen/TweepPicture.swift",
        "HomeScreen/TweetsController.swift",
        "HomeScreenTests/HomeScreenTests.swift",
        "Fabric.framework/run",
        "Crashlytics.framework/run",
        "Crashlytics.framework/submit",
        "TwitterKit.framework/Versions/A/TwitterKit",
        "docs/plans/2026-06-08-ios-sharing-baseline.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-08-response-nil-safety.md",
        "docs/plans/2026-06-08-write-response-data-guard.md",
        "docs/plans/2026-06-09-screenshot-nil-safety.md",
        "docs/plans/2026-06-09-preview-screenshot-fallback.md",
        "docs/plans/2026-06-09-share-session-guard.md",
        "docs/plans/2026-06-09-deprecated-update-with-media-removal.md",
        "docs/plans/2026-06-09-jpeg-media-data-guard.md",
        "docs/plans/2026-06-09-tweet-feed-failure-guard.md",
        "docs/plans/2026-06-10-legacy-sdk-modernization-boundary.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-10-profile-image-completion.md",
        "docs/plans/2026-06-12-https-profile-image-url.md",
        "docs/plans/2026-06-13-media-upload-completion.md",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    for xml_file in [
        "HomeScreen.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "HomeScreen/Main.storyboard",
        "HomeScreen/Base.lproj/Main.storyboard",
        "HomeScreen/Base.lproj/LaunchScreen.xib",
        "HomeScreen/Settings.bundle/Root.plist",
        "docs/readme-overview.svg",
    ]:
        parse_xml(xml_file, failures)

    app_plist = parse_plist("HomeScreen/Info.plist", failures)
    parse_plist("HomeScreenTests/Info.plist", failures)
    photo_reason = app_plist.get("NSPhotoLibraryUsageDescription", "")
    require("photo library" in photo_reason.lower() and "screenshot" in photo_reason.lower(),
            "HomeScreen/Info.plist must document why photo-library access is needed",
            failures)
    require(app_plist.get("UIMainStoryboardFile") == "Main",
            "HomeScreen/Info.plist must keep Main as the app storyboard",
            failures)
    require(app_plist.get("UILaunchStoryboardName") == "LaunchScreen",
            "HomeScreen/Info.plist must keep LaunchScreen configured",
            failures)

    project = read("HomeScreen.xcodeproj/project.pbxproj")
    require("FABRIC_API_KEY" in project and "FABRIC_BUILD_SECRET" in project,
            "Fabric build phase must use local environment placeholders",
            failures)
    require("showEnvVarsInLog = 0;" in project,
            "Fabric build phase must suppress environment variable logging",
            failures)
    require(not re.search(r"Fabric\.framework/run\s+[A-Za-z0-9]{20,}\s+[A-Za-z0-9]{20,}", project),
            "Fabric build phase must not include literal API key or build secret arguments",
            failures)
    require("TwitterKit.framework" in project and "Crashlytics.framework" in project and "Fabric.framework" in project,
            "Xcode project must keep the legacy Twitter/Fabric/Crashlytics framework references visible",
            failures)

    swift = first_party_swift()
    login = read("HomeScreen/LoginController.swift")
    share = read("HomeScreen/ShareController.swift")
    view_controller = read("HomeScreen/ViewController.swift")
    post = read("HomeScreen/Post.swift")
    active_upload = read("HomeScreen/Upload.swift")
    legacy_upload = read("HomeScreen/UploadMedia.swift")
    upload = active_upload + legacy_upload
    tweep_picture = read("HomeScreen/TweepPicture.swift")
    twitter_rest = read("HomeScreen/TwitterRESTAPI.swift")
    tweets_controller = read("HomeScreen/TweetsController.swift")
    url_helper = read("HomeScreen/URL.swift")
    hex_source = read("HomeScreen/Hex.swift")
    require("http://" not in swift,
            "First-party Swift network endpoints must use HTTPS",
            failures)
    require("session != nil && error == nil" in login and "Twitter login failed" in login,
            "LoginController must only continue after a successful Twitter session",
            failures)
    require("if let image = self.screenImage.image" in share,
            "ShareController must not upload when no screenshot image is loaded",
            failures)
    require("UIImageJPEGRepresentation(image, 100)" not in share and
            "if let media = UIImageJPEGRepresentation(image, 1.0)" in share,
            "ShareController must guard JPEG media data and use a valid compression quality",
            failures)
    require("images.lastObject as? PHAsset" in post and "images.lastObject as PHAsset" not in post,
            "Post.swift must safely handle an empty photo fetch result",
            failures)
    require("completion: (result: UIImage?) -> Void" in post and
            "if let screenshot = newImage" in post and
            "completion(result: nil)" in post and
            "(result: UIImage?)" in share,
            "Post.swift must safely handle nil screenshot images from Photos",
            failures)
    require("getScreenshotImage(screenObj) { (result: UIImage?) in" in view_controller and
            "if let screenshot = result" in view_controller and
            "self.showDefault()" in view_controller,
            "ViewController must fall back to the default image when Photos returns no screenshot",
            failures)
    require("println(json)" not in upload,
            "Upload code must not print raw Twitter media-upload JSON responses",
            failures)
    require("statuses/update_with_media.json" not in swift and
            "func UploadMedia(media: NSData" not in legacy_upload and
            "deprecated statuses/update_with_media helper was removed" in legacy_upload,
            "Deprecated update_with_media helper must stay removed",
            failures)
    require("https://upload.twitter.com/1.1/media/upload.json" in active_upload,
            "Active media upload must use Twitter media/upload.json",
            failures)
    require('json!["' not in swift and "profile_image_url!" not in swift,
            "Twitter response parsing must avoid force-unwrapped JSON fields",
            failures)
    require("if let jsonDictionary = json as? JSONDictionary" in tweep_picture and
            "if let profileImageURL = jsonDictionary[\"profile_image_url_https\"] as? String" in tweep_picture and
            'jsonDictionary["profile_image_url"]' not in tweep_picture,
            "TweepPicture must safely unwrap only the HTTPS profile image URL",
            failures)
    require("completion: (result: String?) -> Void" in tweep_picture and
            tweep_picture.count("completion(result: nil)") >= 2 and
            "(result: String?)" in share and
            "if let url_string = result" in share,
            "Profile image lookup must complete explicitly on request and response failures",
            failures)
    require("if let statuses = jsonDictionary[\"statuses\"] as? JSONArray" in twitter_rest,
            "Twitter search parsing must safely unwrap statuses arrays",
            failures)
    require("if let media_id_string = jsonDictionary[\"media_id_string\"] as?String" in upload,
            "Twitter media upload parsing must safely unwrap media IDs",
            failures)
    upload_media = extract_braced_block(upload, "func UploadMedia(")
    share_post = extract_braced_block(share, "func post()")
    require(upload_media is not None and share_post is not None,
            "Media upload and share post functions must remain inspectable",
            failures)
    if upload_media is not None and share_post is not None:
        require("completion: (result: String?) -> Void" in upload_media and
                upload_media.count("completion(result: nil)") == 2 and
                upload_media.count("completion(result: media_id_string)") == 1 and
                "return" in upload_media,
                "UploadMedia must complete once with an optional media identifier on every handled path",
                failures)
        require("println(" not in upload_media,
                "UploadMedia must not log request or connection error details",
                failures)
        require("(media_id: String?)" in share_post and
                "if let uploadedMediaID = media_id" in share_post and
                "UpdateStatus(text, uploadedMediaID)" in share_post and
                "UpdateStatus(text, media_id)" not in share_post,
                "ShareController must submit status only after a successful media upload",
                failures)
    require("UIImage(data: data)!" not in swift and "handler: ((image: UIImage?" in url_helper,
            "Image downloads must return optional images instead of force-unwrapping data",
            failures)
    require("NSURL(string: url_string)!" not in share and "if let profileURL = NSURL(string: url_string)" in share,
            "ShareController must guard profile image URLs before downloading",
            failures)
    require("Twitter.sharedInstance().session().userName" not in share and
            "if let session = Twitter.sharedInstance().session()" in share and
            "let userName = session.userName" in share,
            "ShareController must guard the Twitter session before reading the profile user name",
            failures)
    require("completion(result: [])" in twitter_rest and
            "if let loginError = error" in twitter_rest and
            "Twitter search login failed" in twitter_rest,
            "Twitter search must complete safely when login, request, or connection setup fails",
            failures)
    require("if tweetIDs.count == 0" in tweets_controller and
            "self.isLoadingTweets = true" in tweets_controller and
            "if session == nil" in tweets_controller and
            "func finishLoadingTweets()" in tweets_controller and
            "as? TWTRTweet" in tweets_controller,
            "TweetsController must guard empty IDs, guest-login failures, and loaded tweet casts",
            failures)
    require("let scanner = NSScanner(string: cString)" in hex_source and "!scanner.scanHexInt(&rgbValue)" in hex_source and "scanner.atEnd" in hex_source,
            "Hex color parser must reject invalid or partial hex strings",
            failures)

    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    makefile = read("Makefile")
    plan = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    make_gates_plan = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    nil_safety_plan = read("docs/plans/2026-06-08-response-nil-safety.md")
    write_response_plan = read("docs/plans/2026-06-08-write-response-data-guard.md")
    screenshot_plan = SCREENSHOT_PLAN.read_text(encoding="utf-8") if SCREENSHOT_PLAN.exists() else ""
    screenshot_fallback_plan = SCREENSHOT_FALLBACK_PLAN.read_text(encoding="utf-8") if SCREENSHOT_FALLBACK_PLAN.exists() else ""
    share_session_plan = SHARE_SESSION_PLAN.read_text(encoding="utf-8") if SHARE_SESSION_PLAN.exists() else ""
    deprecated_upload_plan = DEPRECATED_UPLOAD_PLAN.read_text(encoding="utf-8") if DEPRECATED_UPLOAD_PLAN.exists() else ""
    jpeg_media_plan = JPEG_MEDIA_PLAN.read_text(encoding="utf-8") if JPEG_MEDIA_PLAN.exists() else ""
    tweet_feed_plan = TWEET_FEED_PLAN.read_text(encoding="utf-8") if TWEET_FEED_PLAN.exists() else ""
    modernization_plan = MODERNIZATION_PLAN.read_text(encoding="utf-8") if MODERNIZATION_PLAN.exists() else ""
    hosted_validation_plan = HOSTED_VALIDATION_PLAN.read_text(encoding="utf-8") if HOSTED_VALIDATION_PLAN.exists() else ""
    tweep_picture_plan = TWEEP_PICTURE_PLAN.read_text(encoding="utf-8") if TWEEP_PICTURE_PLAN.exists() else ""
    https_profile_image_plan = HTTPS_PROFILE_IMAGE_PLAN.read_text(encoding="utf-8") if HTTPS_PROFILE_IMAGE_PLAN.exists() else ""
    media_upload_plan = MEDIA_UPLOAD_PLAN.read_text(encoding="utf-8") if MEDIA_UPLOAD_PLAN.exists() else ""
    workflow = read(".github/workflows/check.yml")
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
            "Makefile must expose lint, test, and build aliases for the local baseline",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "FABRIC_API_KEY" in readme and "NSPhotoLibraryUsageDescription" in readme and "nil-safe" in readme and "screenshot fallback" in readme and "write response" in readme and "Twitter session" in readme and "JPEG media data" in readme and "tweet feed failures" in readme,
            "README must document static verification, Fabric credentials, and photo permission configuration",
            failures)
    require("deprecated update_with_media" in readme,
            "README must document deprecated update_with_media removal",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "photo-library" in vision and "nil-safe" in vision and "screenshot fallback" in vision and "write response" in vision and "Twitter session" in vision and "deprecated update_with_media" in vision and "JPEG media data" in vision and "tweet feed failures" in vision,
            "VISION must describe the static baseline and photo-library guardrails",
            failures)
    require("FABRIC_API_KEY" in security and "photo-library" in security,
            "SECURITY must document local Fabric settings and photo-library privacy expectations",
            failures)
    require("credential" in changes.lower() and "photo-library" in changes and "upload" in changes.lower() and "nil-safe" in changes and "make lint" in changes and "make test" in changes and "make build" in changes,
            "CHANGES must record credential, photo-library, and upload logging updates",
            failures)
    require("screenshot" in changes.lower(),
            "CHANGES must record screenshot nil-safety updates",
            failures)
    require("screenshot fallback" in changes.lower(),
            "CHANGES must record screenshot fallback updates",
            failures)
    require("write response" in changes.lower(),
            "CHANGES must record write response data guarding",
            failures)
    require("Twitter session" in changes,
            "CHANGES must record share-screen Twitter session guarding",
            failures)
    require("deprecated update_with_media" in changes,
            "CHANGES must record deprecated update_with_media removal",
            failures)
    require("JPEG media data" in changes,
            "CHANGES must record JPEG media data guarding",
            failures)
    require("tweet feed failures" in changes,
            "CHANGES must record tweet feed failure guarding",
            failures)
    require("Swift 1-era" in readme and "iOS 8.1" in readme and "Fabric" in readme and "TwitterKit" in readme,
            "README must document the legacy SDK modernization boundary",
            failures)
    require("Swift 1-era" in vision and "iOS 8.1" in vision and "modernization" in vision.lower(),
            "VISION must document the legacy SDK modernization sequence",
            failures)
    require("retired" in security and "Crashlytics" in security and "current SDK" in security,
            "SECURITY must identify retired SDK and current-toolchain risk",
            failures)
    require("legacy SDK modernization boundary" in changes,
            "CHANGES must record the legacy SDK modernization boundary",
            failures)
    require("JSONObjectWithData(data" not in swift,
            "Twitter JSON parsing must guard optional response data before deserialization",
            failures)
    require("NSURL(string: url)!" not in url_helper and "if let requestURL = NSURL(string: url)" in url_helper and "Missing response data" in url_helper and "Invalid URL" in url_helper,
            "URL.post must guard invalid URLs and missing response data",
            failures)
    require("*.local.xcconfig" in gitignore and "*.secrets.xcconfig" in gitignore and ".env" in gitignore,
            ".gitignore must exclude local secret configuration files",
            failures)
    require("status: completed" in plan,
            "plan must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
            failures)
    require("status: completed" in nil_safety_plan,
            "response nil-safety plan must be marked completed",
            failures)
    require("status: completed" in write_response_plan,
            "write response data guard plan must be marked completed",
            failures)
    require("status: completed" in screenshot_plan,
            "screenshot nil-safety plan must be marked completed",
            failures)
    require("status: completed" in screenshot_fallback_plan,
            "screenshot fallback plan must be marked completed",
            failures)
    require("status: completed" in share_session_plan,
            "share session guard plan must be marked completed",
            failures)
    require("status: completed" in deprecated_upload_plan,
            "deprecated upload helper plan must be marked completed",
            failures)
    require("status: completed" in jpeg_media_plan,
            "JPEG media data guard plan must be marked completed",
            failures)
    require("status: completed" in tweet_feed_plan,
            "tweet feed failure guard plan must be marked completed",
            failures)
    require("status: completed" in modernization_plan and "Swift 1-era" in modernization_plan and "iOS 8.1" in modernization_plan,
            "legacy SDK modernization boundary must be completed and version-specific",
            failures)
    require("status: completed" in hosted_validation_plan and "make check" in hosted_validation_plan,
            "hosted project validation plan must be completed and document make check",
            failures)
    require("status: completed" in tweep_picture_plan and "make check" in tweep_picture_plan,
            "profile image completion plan must be completed and document verification",
            failures)
    require("status: completed" in https_profile_image_plan and "make check" in https_profile_image_plan,
            "HTTPS profile image plan must be completed and document verification",
            failures)
    require("profile_image_url_https" in readme and
            "profile_image_url_https" in vision and
            "profile_image_url_https" in security and
            "profile_image_url_https" in changes,
            "Docs must preserve the dynamic HTTPS profile-image response boundary",
            failures)
    require("optional identifier" in readme and "status submission requires a non-nil media identifier" in readme and
            "nil identifier" in security and "request or connection objects" in security and
            "media-upload completion total" in vision and "status submission only after upload success" in vision and
            "media upload completion return an optional identifier" in changes and "guarded status submission" in changes,
            "Docs must record deterministic media-upload completion",
            failures)
    media_upload_statuses = re.findall(
        r"^status: .+$", media_upload_plan, flags=re.MULTILINE
    )
    media_upload_sections = media_upload_plan.split("## Verification Completed\n", 1)
    media_upload_verification = (
        media_upload_sections[1] if len(media_upload_sections) == 2 else ""
    )
    media_upload_required_evidence = (
        "All four Make gates",
        "`xcodebuild` was",
        "python3 -m py_compile scripts/check-baseline.py",
        "git diff --check",
        "Eight isolated hostile mutations",
    )
    require(media_upload_statuses == ["status: completed"]
            and all(item in media_upload_verification for item in media_upload_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", media_upload_verification, re.IGNORECASE) is None,
            "media upload completion plan must record completed status and actual verification",
            failures)
    require("permissions:\n  contents: read" in workflow,
            "Check workflow must use read-only repository permissions",
            failures)
    require("cancel-in-progress: true" in workflow and "runs-on: macos-15" in workflow and
            "timeout-minutes: 10" in workflow,
            "Check workflow must bound duplicate and long-running macOS jobs",
            failures)
    require("actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10" in workflow and
            "persist-credentials: false" in workflow and
            "run: make check" in workflow,
            "Check workflow must pin checkout without persisted credentials and run the canonical baseline",
            failures)

    if shutil.which("xcodebuild"):
        result = subprocess.run(
            ["xcodebuild", "-list", "-project", "HomeScreen.xcodeproj"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        require(result.returncode == 0,
                "xcodebuild could not parse HomeScreen.xcodeproj: " + result.stderr.strip(),
                failures)
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("HomeScreen iOS sharing baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
