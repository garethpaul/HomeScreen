#!/usr/bin/env python3
from pathlib import Path
import sys


ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


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


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    failures = []
    post = read("HomeScreen/Post.swift")
    share = read("HomeScreen/ShareController.swift")
    tweets = read("HomeScreen/TweetsController.swift")
    view = read("HomeScreen/ViewController.swift")

    screenshot_request = extract_braced_block(post, "func getScreenshotImage(")
    require(screenshot_request is not None, "Screenshot request helper must remain inspectable", failures)
    if screenshot_request is not None:
        require("options.deliveryMode = .HighQualityFormat" in screenshot_request and
                "options.resizeMode = .Exact" in screenshot_request and
                "options: options" in screenshot_request,
                "Screenshot requests must pass the high-quality Photos options they configure",
                failures)
        require("var completionDelivered = false" in screenshot_request and
                "NSOperationQueue.mainQueue().addOperationWithBlock" in screenshot_request and
                "if completionDelivered" in screenshot_request and
                "completionDelivered = true" in screenshot_request,
                "Screenshot completion must be serialized on main and delivered exactly once",
                failures)

    share_profile_load = extract_braced_block(share, "func startProfileImageLoad(")
    require(share_profile_load is not None and
            "profilePic.image = nil" in share_profile_load and
            "profilePic.hidden = true" in share_profile_load,
            "Starting a profile load must clear and hide stale profile imagery",
            failures)

    share_screenshot_load = extract_braced_block(share, "func startScreenshotLoad()")
    require("var screenshotGeneration = 0" in share and
            share_screenshot_load is not None and
            "screenshotGeneration += 1" in share_screenshot_load and
            "let generation = screenshotGeneration" in share_screenshot_load and
            "getScreenshotImage(screenObj) { [weak self]" in share_screenshot_load and
            "controller.screenshotGeneration != generation" in share_screenshot_load and
            "func invalidateScreenshotLoad()" in share and
            "invalidateScreenshotLoad()" in extract_braced_block(share, "override func viewWillDisappear(") ,
            "Share screenshots must be weakly owned and generation-bound to the visible composer",
            failures)

    complete_post = extract_braced_block(share, "func completePost(")
    share_post = extract_braced_block(share, "func post()")
    require(complete_post is not None and
            "addOperationWithBlock { [weak self]" in complete_post and
            "if let controller = self" in complete_post,
            "Queued post completion must not retain a dismissed composer",
            failures)
    require(share_post is not None and
            "UploadMedia(media) { [weak self]" in share_post and
            "UpdateStatus(text, uploadedMediaID) { [weak self]" in share_post,
            "Upload and status callbacks must weakly own the composer",
            failures)

    view_screenshot_load = extract_braced_block(view, "func getLatestImage()")
    require("var screenshotGeneration = 0" in view and
            view_screenshot_load is not None and
            "screenshotGeneration += 1" in view_screenshot_load and
            "let generation = screenshotGeneration" in view_screenshot_load and
            "getScreenshotImage(screenObj) { [weak self]" in view_screenshot_load and
            "controller.screenshotGeneration != generation" in view_screenshot_load,
            "Home screen image callbacks must be weakly owned and latest-generation only",
            failures)

    load_tweets = extract_braced_block(tweets, "func loadTweets(")
    tweet_models_callback = extract_braced_block(load_tweets or "", "loadTweetsWithIDs(tweetIDs)")
    require(tweet_models_callback is not None and
            "controller.completeTweetLoad(generation, loadedTweets: loadedTweetModels)" in tweet_models_callback and
            "controller.tweetGeneration != generation" not in tweet_models_callback,
            "Final tweet callbacks must defer generation state reads to main-queue completion",
            failures)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("HomeScreen async ownership contracts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
