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
PROFILE_VISIBILITY_PLAN = ROOT / "docs/plans/2026-06-13-profile-image-success-visibility.md"
LOCATION_INDEPENDENT_MAKE_PLAN = ROOT / "docs/plans/2026-06-13-location-independent-make.md"
STATUS_DISMISSAL_PLAN = ROOT / "docs/plans/2026-06-14-successful-status-dismissal.md"
POST_GENERATION_PLAN = ROOT / "docs/plans/2026-06-15-share-post-generation.md"
PROFILE_GENERATION_PLAN = ROOT / "docs/plans/2026-06-16-profile-image-generation.md"
TWEET_GENERATION_PLAN = ROOT / "docs/plans/2026-06-17-tweet-feed-generation.md"


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
        "HomeScreen/UpdateStatus.swift",
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
        "docs/plans/2026-06-13-profile-image-success-visibility.md",
        "docs/plans/2026-06-13-location-independent-make.md",
        "docs/plans/2026-06-14-successful-status-dismissal.md",
        "docs/plans/2026-06-15-share-post-generation.md",
        "docs/plans/2026-06-16-profile-image-generation.md",
        "docs/plans/2026-06-17-tweet-feed-generation.md",
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
    update_status = read("HomeScreen/UpdateStatus.swift")
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
            "complete(nil)" in post and
            "(result: UIImage?)" in share,
            "Post.swift must safely handle nil screenshot images from Photos",
            failures)
    require("getScreenshotImage(screenObj) { [weak self] (result: UIImage?) in" in view_controller and
            "if let screenshot = result" in view_controller and
            "controller.showDefault()" in view_controller,
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
    profile_success = extract_braced_block(share, "if let newImg = image")
    require(profile_success is not None,
            "Share screen must retain a successful profile image callback",
            failures)
    if profile_success is not None:
        image_assignment = "controller.profilePic!.image = circle"
        reveal = "controller.profilePic.hidden = false"
        require(image_assignment in profile_success and reveal in profile_success and
                profile_success.find(image_assignment) < profile_success.find(reveal),
                "Successful profile image callbacks must assign the image before revealing it",
                failures)
    require(share.count("profilePic.hidden = true") >= 2 and
            share.count("controller.profilePic.hidden = false") == 1,
            "Profile image visibility must stay hidden initially and reveal only on success",
            failures)
    profile_load = extract_braced_block(share, "func startProfileImageLoad(")
    invalidate_profile = extract_braced_block(share, "func invalidateProfileImageLoad()")
    require(profile_load is not None and invalidate_profile is not None,
            "Profile image generation helpers must remain inspectable",
            failures)
    if profile_load is not None:
        profile_url_callback = extract_braced_block(profile_load, "TweepPicture(userName)")
        profile_download_callback = extract_braced_block(profile_load, "url.downloadImage(profileURL")
        require("profileGeneration += 1" in profile_load and
                "let generation = profileGeneration" in profile_load and
                "TweepPicture(userName){ [weak self]" in profile_load and
                "addOperationWithBlock { [weak self] in" in profile_load and
                "url.downloadImage(profileURL, { [weak self]" in profile_load,
                "Profile image loading must use weak ownership at every asynchronous boundary",
                failures)
        require(profile_url_callback is not None and
                "if controller.profileGeneration != generation" in profile_url_callback and
                profile_url_callback.find("if controller.profileGeneration != generation") <
                profile_url_callback.find("url.downloadImage(profileURL"),
                "Stale profile URL callbacks must stop before image download",
                failures)
        require(profile_download_callback is not None and
                "if controller.profileGeneration != generation" in profile_download_callback and
                profile_download_callback.find("if controller.profileGeneration != generation") <
                profile_download_callback.find("controller.profilePic!.image = circle"),
                "Stale profile downloads must stop before avatar mutation",
                failures)
    require("if let statuses = jsonDictionary[\"statuses\"] as? JSONArray" in twitter_rest,
            "Twitter search parsing must safely unwrap statuses arrays",
            failures)
    require("if let media_id_string = jsonDictionary[\"media_id_string\"] as?String" in upload,
            "Twitter media upload parsing must safely unwrap media IDs",
            failures)
    upload_media = extract_braced_block(upload, "func UploadMedia(")
    status_update = extract_braced_block(update_status, "func UpdateStatus(")
    share_post = extract_braced_block(share, "func post()")
    require(upload_media is not None and status_update is not None and share_post is not None,
            "Media upload, status update, and share post functions must remain inspectable",
            failures)
    if upload_media is not None and status_update is not None and share_post is not None:
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
        require("completion: (succeeded: Bool) -> Void" in status_update and
                status_update.count("completion(succeeded: false)") == 2 and
                status_update.count("completion(succeeded: true)") == 1 and
                'jsonDictionary["id_str"] as? String' in status_update and
                "whitespaceAndNewlineCharacterSet" in status_update and
                "!trimmedStatusID.isEmpty" in status_update and
                "println(" not in status_update,
                "UpdateStatus must complete once and accept only a nonblank status identifier",
                failures)
        status_call = extract_braced_block(share_post, "UpdateStatus(text, uploadedMediaID)")
        require(status_call is not None and
                "controller.completePost(generation, succeeded: succeeded)" in status_call,
                "ShareController must route status completion through generation ownership",
                failures)
        require(share_post.count('performSegueWithIdentifier("cancelSegue", sender: self)') == 0,
                "ShareController post must not dismiss before status success",
                failures)
        require("if self.postInFlight" in share_post and
                "self.postInFlight = true" in share_post and
                "let generation = self.postGeneration" in share_post,
                "ShareController must suppress duplicate posts and capture submission ownership",
                failures)
        require("controller.completePost(generation, succeeded: succeeded)" in share_post and
                "controller.completePost(generation, succeeded: false)" in share_post,
                "ShareController must resolve status and media failure through one generation-bound completion",
                failures)
    complete_post = extract_braced_block(share, "func completePost(")
    invalidate_post = extract_braced_block(share, "func invalidatePost()")
    view_disappear = extract_braced_block(share, "override func viewWillDisappear(")
    close_action = extract_braced_block(share, "func close()")
    require(complete_post is not None and invalidate_post is not None and
            view_disappear is not None and close_action is not None,
            "Share post completion and invalidation functions must remain inspectable",
            failures)
    if complete_post is not None:
        require("NSOperationQueue.mainQueue().addOperationWithBlock { [weak self]" in complete_post and
                "!controller.postInFlight || controller.postGeneration != generation" in complete_post and
                "controller.postInFlight = false" in complete_post and
                "if succeeded" in complete_post and
                'controller.performSegueWithIdentifier("cancelSegue", sender: controller)' in complete_post,
                "Share completion must reject stale generations and dismiss successful current posts on the main queue",
                failures)
    if invalidate_post is not None and view_disappear is not None and close_action is not None:
        require("postGeneration += 1" in invalidate_post and
                "postInFlight = false" in invalidate_post and
                "invalidatePost()" in view_disappear and
                "invalidatePost()" in close_action and
                close_action.find("invalidatePost()") < close_action.find('performSegueWithIdentifier("cancelSegue"'),
                "Share controller close and disappearance must invalidate active post callbacks before dismissal",
                failures)
    if invalidate_profile is not None and view_disappear is not None:
        require("profileGeneration += 1" in invalidate_profile and
                "invalidateProfileImageLoad()" in view_disappear and
                view_disappear.find("invalidateProfileImageLoad()") <
                view_disappear.find("invalidatePost()"),
                "Share disappearance must invalidate profile callbacks before post callbacks",
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
    setup_tweet_view = extract_braced_block(tweets_controller, "func setupView()")
    start_tweet_load = extract_braced_block(tweets_controller, "func startTweetLoad()")
    load_tweets = extract_braced_block(tweets_controller, "func loadTweets(")
    complete_tweet_load = extract_braced_block(tweets_controller, "func completeTweetLoad(")
    refresh_tweets = extract_braced_block(tweets_controller, "func refreshInvoked()")
    require(setup_tweet_view is not None and start_tweet_load is not None and load_tweets is not None and
            complete_tweet_load is not None and refresh_tweets is not None,
            "TweetsController request ownership helpers must remain inspectable",
            failures)
    if setup_tweet_view is not None and start_tweet_load is not None and refresh_tweets is not None:
        require("startTweetLoad()" in setup_tweet_view and
                "Search()" not in setup_tweet_view and
                "tweetGeneration += 1" in start_tweet_load and
                "let generation = tweetGeneration" in start_tweet_load and
                "Search() { [weak self]" in start_tweet_load and
                "NSOperationQueue.mainQueue().addOperationWithBlock { [weak self]" in start_tweet_load and
                "controller.tweetGeneration != generation" in start_tweet_load and
                "controller.loadTweets(result, generation: generation)" in start_tweet_load and
                "startTweetLoad()" in refresh_tweets and
                "Search()" not in refresh_tweets,
                "Initial and refresh searches must use one weak, generation-bound start path",
                failures)
    if load_tweets is not None:
        tweet_models_callback = extract_braced_block(
            load_tweets, "loadTweetsWithIDs(tweetIDs)"
        )
        require("tweetGeneration != generation" in load_tweets and
                "if tweetIDs.count == 0" in load_tweets and
                "completeTweetLoad(generation, loadedTweets: [])" in load_tweets and
                "logInGuestWithCompletion { [weak self]" in load_tweets and
                "controller.tweetGeneration != generation" in load_tweets and
                "loadTweetsWithIDs(tweetIDs) { [weak self]" in load_tweets and
                "loadedTweetModels.append(tweet)" in load_tweets and
                "self.tweets.append" not in load_tweets and
                "controller.completeTweetLoad(generation, loadedTweets: loadedTweetModels)" in load_tweets,
                "Tweet login and load callbacks must reject stale generations and collect replacement results weakly",
                failures)
        require(tweet_models_callback is not None and
                "if let controller = self" in tweet_models_callback and
                "controller.tweetGeneration != generation" not in tweet_models_callback and
                "controller.completeTweetLoad(generation, loadedTweets: loadedTweetModels)" in tweet_models_callback,
                "Tweet model callbacks must defer generation state reads to main-queue completion",
                failures)
    if complete_tweet_load is not None:
        require("NSOperationQueue.mainQueue().addOperationWithBlock { [weak self]" in complete_tweet_load and
                "controller.tweetGeneration != generation" in complete_tweet_load and
                "controller.tweets = loadedTweets" in complete_tweet_load and
                complete_tweet_load.find("controller.tweets = loadedTweets") <
                complete_tweet_load.find("controller.isLoadingTweets = false") <
                complete_tweet_load.find("controller.activityIndicator.stopAnimating()") <
                complete_tweet_load.find("controller.activityIndicator.hidden = true"),
                "Tweet completion must replace the current feed and finish its spinner on the main queue only for the current generation",
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
    profile_visibility_plan = PROFILE_VISIBILITY_PLAN.read_text(encoding="utf-8") if PROFILE_VISIBILITY_PLAN.exists() else ""
    location_independent_make_plan = LOCATION_INDEPENDENT_MAKE_PLAN.read_text(encoding="utf-8") if LOCATION_INDEPENDENT_MAKE_PLAN.exists() else ""
    status_dismissal_plan = STATUS_DISMISSAL_PLAN.read_text(encoding="utf-8") if STATUS_DISMISSAL_PLAN.exists() else ""
    post_generation_plan = POST_GENERATION_PLAN.read_text(encoding="utf-8") if POST_GENERATION_PLAN.exists() else ""
    profile_generation_plan = PROFILE_GENERATION_PLAN.read_text(encoding="utf-8") if PROFILE_GENERATION_PLAN.exists() else ""
    tweet_generation_plan = TWEET_GENERATION_PLAN.read_text(encoding="utf-8") if TWEET_GENERATION_PLAN.exists() else ""
    workflow = read(".github/workflows/check.yml")
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
            "Makefile must expose lint, test, and build aliases for the local baseline",
            failures)
    require("override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile and '@python3 "$(ROOT)/scripts/check-baseline.py"' in makefile,
            "Makefile must invoke the checker through the loaded checkout root", failures)
    require("absolute Makefile path" in readme and "any working directory" in readme,
            "README must document location-independent verification", failures)
    require("Make verification target derive the checkout root" in changes and "external directories" in changes,
            "CHANGES must record location-independent verification", failures)
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
    profile_generation_guidance = "Profile image callbacks are generation-bound to the visible share screen."
    for document_name, document in (
            ("README.md", readme),
            ("SECURITY.md", security),
            ("VISION.md", vision),
            ("CHANGES.md", changes)):
        require(profile_generation_guidance in document,
                f"{document_name} must document profile callback lifecycle ownership",
                failures)
    require("Tweet feed callbacks are generation-bound so only the latest initial or refresh" in readme and
            "Tweet feed callbacks are generation-bound and weakly own the controller" in security and
            "Tweet feed callback generations make the latest initial or refresh request" in vision and
            "Tweet feed callbacks are generation-bound so older overlapping searches" in changes and
            "Keep tweet search, guest-login, model-load, and UI completion callbacks weakly owned and bound to the latest request generation." in read("AGENTS.md"),
            "Docs must record latest-request tweet feed generation ownership",
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
    require("revealed only after a successful profile image download" in readme.lower() and
            "success-only profile image reveal" in security.lower() and
            "successful profile images become visible" in vision.lower() and
            "Reveal the profile image only after" in changes,
            "Docs must record success-only profile image visibility",
            failures)
    require("optional identifier" in readme and "status submission requires a non-nil media identifier" in readme and
            "nil identifier" in security and "request or connection objects" in security and
            "media-upload completion total" in vision and "status submission only after upload success" in vision and
            "media upload completion return an optional identifier" in changes and "guarded status submission" in changes,
            "Docs must record deterministic media-upload completion",
            failures)
    require("dismisses only after Twitter confirms status creation" in readme and
            "success-only share dismissal" in security and
            "Keep share dismissal behind confirmed status creation" in vision and
            "Moved share-composer dismissal behind" in changes and
            "Keep share-composer dismissal behind" in read("AGENTS.md"),
            "Docs must record success-only status dismissal",
            failures)
    post_generation_guidance = "Share post callbacks are generation-bound so duplicate taps and stale completions cannot dismiss the composer."
    require(all(post_generation_guidance in read(path) for path in
                ["AGENTS.md", "README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]),
            "Docs must record share post generation ownership",
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
    profile_visibility_statuses = re.findall(
        r"^status: .+$", profile_visibility_plan, flags=re.MULTILINE
    )
    profile_visibility_sections = profile_visibility_plan.split(
        "## Verification Completed\n", 1
    )
    profile_visibility_verification = (
        profile_visibility_sections[1]
        if len(profile_visibility_sections) == 2 else ""
    )
    profile_visibility_required_evidence = (
        "All four Make gates",
        "`xcodebuild` was",
        "python3 -m py_compile scripts/check-baseline.py",
        "git diff --check",
        "Six isolated hostile mutations",
        "Hosted macOS project validation and CodeQL evidence",
    )
    require(profile_visibility_statuses == ["status: completed"]
            and all(item in profile_visibility_verification
                    for item in profile_visibility_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b",
                          profile_visibility_verification,
                          re.IGNORECASE) is None,
            "profile image visibility plan must record completed status and actual local verification",
            failures)
    location_statuses = re.findall(r"^status: .+$", location_independent_make_plan, flags=re.MULTILINE)
    location_sections = location_independent_make_plan.split("## Verification Completed\n", 1)
    location_verification = location_sections[1] if len(location_sections) == 2 else ""
    location_required = ("Root and external-directory Make gates passed", "root-derivation mutation failed", "checker-invocation mutation failed", "plan-status mutation failed", "plan-evidence mutation failed", "documentation mutation failed")
    require(location_statuses == ["status: completed"] and all(item in location_verification for item in location_required) and re.search(r"\b(?:pending|todo|tbd|not run)\b", location_verification, re.IGNORECASE) is None,
            "location-independent Make plan must record completed verification", failures)
    status_dismissal_statuses = re.findall(r"^status: .+$", status_dismissal_plan, flags=re.MULTILINE)
    status_dismissal_sections = status_dismissal_plan.split("## Verification Completed\n", 1)
    status_dismissal_verification = status_dismissal_sections[1] if len(status_dismissal_sections) == 2 else ""
    status_dismissal_required = (
        "All four Make gates passed",
        "absolute Makefile path passed from `/tmp`",
        "python3 -m py_compile scripts/check-baseline.py",
        "isolated hostile mutations were rejected",
        "changed-line credential scan passed",
    )
    require(status_dismissal_statuses == ["status: completed"] and
            all(item in status_dismissal_verification for item in status_dismissal_required) and
            re.search(r"\b(?:pending|todo|tbd|not run)\b", status_dismissal_verification, re.IGNORECASE) is None,
            "successful status dismissal plan must record completed verification", failures)
    post_generation_statuses = re.findall(r"^status: .+$", post_generation_plan, flags=re.MULTILINE)
    post_generation_sections = post_generation_plan.split("## Verification Completed\n", 1)
    post_generation_verification = post_generation_sections[1] if len(post_generation_sections) == 2 else ""
    post_generation_required = (
        "All four Make gates passed",
        "absolute Makefile passed from `/tmp`",
        "python3 -m py_compile scripts/check-baseline.py",
        "hostile mutations were rejected",
        "changed-line credential scan passed",
        "hosted pull-request and security-alert snapshot",
    )
    require(post_generation_statuses == ["status: completed"] and
            all(item in post_generation_verification for item in post_generation_required) and
            re.search(r"\b(?:pending|todo|tbd|not run)\b", post_generation_verification, re.IGNORECASE) is None,
            "share post generation plan must record completed verification", failures)
    profile_generation_statuses = re.findall(r"^Status: .+$", profile_generation_plan, flags=re.MULTILINE)
    profile_generation_sections = profile_generation_plan.split("## Verification Completed\n", 1)
    profile_generation_verification = profile_generation_sections[1] if len(profile_generation_sections) == 2 else ""
    profile_generation_required = (
        "All four Make gates passed",
        "absolute Makefile passed from `/tmp`",
        "python3 -m py_compile scripts/check-baseline.py",
        "hostile mutations were rejected",
        "changed-line credential scan passed",
        "No Xcode, simulator, or physical-device scenario was executed",
    )
    require(profile_generation_statuses == ["Status: Completed"] and
            all(item in profile_generation_verification for item in profile_generation_required) and
            re.search(r"\b(?:pending|todo|tbd)\b", profile_generation_verification, re.IGNORECASE) is None,
            "profile image generation plan must record completed verification", failures)
    tweet_generation_statuses = re.findall(
        r"^status: .+$", tweet_generation_plan, flags=re.MULTILINE
    )
    tweet_generation_sections = tweet_generation_plan.split(
        "## Verification Completed\n", 1
    )
    tweet_generation_verification = (
        tweet_generation_sections[1]
        if len(tweet_generation_sections) == 2 else ""
    )
    normalized_tweet_generation_verification = " ".join(
        tweet_generation_verification.split()
    )
    tweet_generation_required = (
        "All four Make gates passed",
        "external-directory `make check` passed",
        "Twelve isolated implementation mutations were rejected",
        "removed the final callback's off-main controller-generation read",
        "`xcodebuild` and live Twitter services were unavailable on Linux",
        "no guest authentication, search result, table-rendering, refresh-interaction, simulator, or device-networking behavior is claimed",
        "`32332556006a444d70b76bb07cb09d8472f7b5ac`",
        "push run `27719581668`",
        "pull-request run `27719591737`",
        "PR #9 remained open and mergeable",
    )
    require(tweet_generation_statuses == ["status: completed"] and
            all(item in normalized_tweet_generation_verification
                    for item in tweet_generation_required) and
            re.search(r"\b(?:pending|todo|tbd|not run|not yet)\b",
                      tweet_generation_verification,
                      re.IGNORECASE) is None,
            "tweet feed generation plan must record completed status, review resolution, actual verification, and the runtime boundary",
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
