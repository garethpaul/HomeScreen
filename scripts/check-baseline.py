#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-ios-sharing-baseline.md"
SCREENSHOT_PLAN = ROOT / "docs/plans/2026-06-09-screenshot-nil-safety.md"
SCREENSHOT_FALLBACK_PLAN = ROOT / "docs/plans/2026-06-09-preview-screenshot-fallback.md"


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


def main():
    failures = []
    required_files = [
        ".gitignore",
        "CHANGES.md",
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
        "docs/plans/2026-06-08-response-nil-safety.md",
        "docs/plans/2026-06-08-write-response-data-guard.md",
        "docs/plans/2026-06-09-screenshot-nil-safety.md",
        "docs/plans/2026-06-09-preview-screenshot-fallback.md",
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
    upload = read("HomeScreen/Upload.swift") + read("HomeScreen/UploadMedia.swift")
    tweep_picture = read("HomeScreen/TweepPicture.swift")
    twitter_rest = read("HomeScreen/TwitterRESTAPI.swift")
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
    require('json!["' not in swift and "profile_image_url!" not in swift,
            "Twitter response parsing must avoid force-unwrapped JSON fields",
            failures)
    require("if let jsonDictionary = json as? JSONDictionary" in tweep_picture and
            "if let profileImageURL = jsonDictionary[\"profile_image_url\"] as? String" in tweep_picture,
            "TweepPicture must safely unwrap profile image URLs",
            failures)
    require("if let statuses = jsonDictionary[\"statuses\"] as? JSONArray" in twitter_rest,
            "Twitter search parsing must safely unwrap statuses arrays",
            failures)
    require("if let media_id_string = jsonDictionary[\"media_id_string\"] as?String" in upload,
            "Twitter media upload parsing must safely unwrap media IDs",
            failures)
    require("UIImage(data: data)!" not in swift and "handler: ((image: UIImage?" in url_helper,
            "Image downloads must return optional images instead of force-unwrapping data",
            failures)
    require("NSURL(string: url_string)!" not in share and "if let profileURL = NSURL(string: url_string)" in share,
            "ShareController must guard profile image URLs before downloading",
            failures)
    require("let scanner = NSScanner(string: cString)" in hex_source and "!scanner.scanHexInt(&rgbValue)" in hex_source and "scanner.atEnd" in hex_source,
            "Hex color parser must reject invalid or partial hex strings",
            failures)

    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    plan = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    nil_safety_plan = read("docs/plans/2026-06-08-response-nil-safety.md")
    write_response_plan = read("docs/plans/2026-06-08-write-response-data-guard.md")
    screenshot_plan = SCREENSHOT_PLAN.read_text(encoding="utf-8") if SCREENSHOT_PLAN.exists() else ""
    screenshot_fallback_plan = SCREENSHOT_FALLBACK_PLAN.read_text(encoding="utf-8") if SCREENSHOT_FALLBACK_PLAN.exists() else ""
    require("make check" in readme and "FABRIC_API_KEY" in readme and "NSPhotoLibraryUsageDescription" in readme and "nil-safe" in readme and "screenshot fallback" in readme and "write response" in readme,
            "README must document static verification, Fabric credentials, and photo permission configuration",
            failures)
    require("scripts/check-baseline.py" in vision and "photo-library" in vision and "nil-safe" in vision and "screenshot fallback" in vision and "write response" in vision,
            "VISION must describe the static baseline and photo-library guardrails",
            failures)
    require("FABRIC_API_KEY" in security and "photo-library" in security,
            "SECURITY must document local Fabric settings and photo-library privacy expectations",
            failures)
    require("credential" in changes.lower() and "photo-library" in changes and "upload" in changes.lower() and "nil-safe" in changes,
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

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run a scheme-specific Xcode test on macOS before release.")
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
