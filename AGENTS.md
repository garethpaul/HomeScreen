# AGENTS.md

## Repository purpose

`garethpaul/HomeScreen` is a Apple platform application or Objective-C/Swift sample. HomeScreen app for for sharing your #Homescreen

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `HomeScreen.xcodeproj` - Xcode project
- `Crashlytics.framework` - repository source or sample assets
- `Fabric.framework` - repository source or sample assets
- `HomeScreen` - repository source or sample assets
- `HomeScreenTests` - repository source or sample assets
- `TwitterKit.framework` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Local Apple development: `open HomeScreen.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: C/C++ headers (23), Swift (19).
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `HomeScreen/UpdateStatus.swift`, `HomeScreenTests/HomeScreenTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- The Fabric upload build phase reads `FABRIC_API_KEY` and `FABRIC_BUILD_SECRET` locally and skips the upload when either value is unset.
- Do not commit real Fabric, Twitter, signing, screenshot, or local xcconfig values to this repository.
- Home screen screenshots can reveal private apps, messages, accounts, or location hints. Keep uploads user-initiated and avoid raw response or image logging.
- Treat Twitter session state as optional on presentation paths; expired or missing sessions should not crash profile-image rendering.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
