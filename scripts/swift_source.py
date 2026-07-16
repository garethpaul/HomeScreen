"""Swift source reader that blanks comments before contract assertions.

Every gate in this repo asserted substrings, occurrence counts and find()-index
orderings against raw Swift source. A commented-out guard therefore satisfied its
own assertion: inside /* ... */ the literal is byte-identical, the count is
unchanged, and the ordering is unchanged.

Verified before this module existed -- block-commenting the exactly-once delivery
guard in Post.swift getScreenshotImage:

    make check exit 0, "7 hostile mutations rejected"

while deleting the same guard IS caught:

    FAIL: Screenshot completion must be serialized on main and delivered exactly
    once

So the gate was live but blind. That guard is load-bearing:
PHImageRequestOptions.HighQualityFormat can invoke its result handler more than
once, so without the flag `completion` fires repeatedly and the screenshot uploads
more than once.

strip_swift_comments is ported verbatim from ios-app-share's check-baseline.py,
which is the working reference in this account: a real scanner handling nested
/* */ blocks, string-aware and escape-aware. A naive //[^\n]* regex would blank
the rest of the line for `let u = "https://example.com"` and fail a contract
against correct source.
"""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def strip_swift_comments(text):
    result = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False

    while index < len(text):
        character = text[index]
        next_character = text[index + 1] if index + 1 < len(text) else ""

        if block_depth:
            if character == "/" and next_character == "*":
                block_depth += 1
                index += 2
                continue
            if character == "*" and next_character == "/":
                block_depth -= 1
                index += 2
                continue
            if character == "\n":
                result.append(character)
            index += 1
            continue

        if in_string:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            index += 1
            continue

        if character == '"':
            in_string = True
            result.append(character)
            index += 1
            continue
        if character == "/" and next_character == "/":
            newline = text.find("\n", index + 2)
            if newline == -1:
                break
            result.append("\n")
            index = newline + 1
            continue
        if character == "/" and next_character == "*":
            block_depth = 1
            index += 2
            continue

        result.append(character)
        index += 1

    return "".join(result)


def read_swift(relative_path):
    """Read a Swift source file with its comments blanked out."""
    text = (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")
    return strip_swift_comments(text)
