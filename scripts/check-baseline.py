#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-ios-sharing-baseline.md"


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
    require(not re.search(r"Fabric\.framework/run\s+[A-Za-z0-9]{20,}\s+[A-Za-z0-9]{20,}", project),
            "Fabric build phase must not include literal API key or build secret arguments",
            failures)
    require("TwitterKit.framework" in project and "Crashlytics.framework" in project and "Fabric.framework" in project,
            "Xcode project must keep the legacy Twitter/Fabric/Crashlytics framework references visible",
            failures)

    swift = first_party_swift()
    login = read("HomeScreen/LoginController.swift")
    share = read("HomeScreen/ShareController.swift")
    post = read("HomeScreen/Post.swift")
    upload = read("HomeScreen/Upload.swift") + read("HomeScreen/UploadMedia.swift")
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
    require("println(json)" not in upload,
            "Upload code must not print raw Twitter media-upload JSON responses",
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
    require("make check" in readme and "FABRIC_API_KEY" in readme and "NSPhotoLibraryUsageDescription" in readme,
            "README must document static verification, Fabric credentials, and photo permission configuration",
            failures)
    require("scripts/check-baseline.py" in vision and "photo-library" in vision,
            "VISION must describe the static baseline and photo-library guardrails",
            failures)
    require("FABRIC_API_KEY" in security and "photo-library" in security,
            "SECURITY must document local Fabric settings and photo-library privacy expectations",
            failures)
    require("credential" in changes.lower() and "photo-library" in changes and "upload" in changes.lower(),
            "CHANGES must record credential, photo-library, and upload logging updates",
            failures)
    require("*.local.xcconfig" in gitignore and "*.secrets.xcconfig" in gitignore and ".env" in gitignore,
            ".gitignore must exclude local secret configuration files",
            failures)
    require("status: completed" in plan,
            "plan must be marked completed",
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
