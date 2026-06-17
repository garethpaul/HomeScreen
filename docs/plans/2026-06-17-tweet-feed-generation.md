---
title: "fix: Bind tweet feed callbacks to the latest request"
type: fix
date: 2026-06-17
status: completed
---

# fix: Bind tweet feed callbacks to the latest request

## Context

`TweetsController` starts an initial search and permits later refresh searches,
but request ownership begins only when search IDs reach `loadTweets`. Searches,
guest login, and tweet loading can therefore overlap. An older callback may
append stale tweets, finish the spinner for a newer refresh, or cause the newer
IDs to be discarded by the existing `isLoadingTweets` check.

## Prioritized Engineering Tasks

1. **Selected: make the latest accepted feed request authoritative.** Bind the
   search, guest-login, and tweet-load callback chain to one generation and
   reject stale completions before they start later work or mutate UI.
2. **Follow-up: modernize retired TwitterKit feed rendering.** Keep SDK and API
   replacement in the broader Swift/current-Xcode migration because model,
   authentication, and table-cell APIs are coupled.
3. **Follow-up: add Apple-runtime refresh interaction tests.** Keep simulator
   UI behavior separate from the dependency-free Linux baseline.

## Requirements

- R1. Initial load and refresh must enter one `startTweetLoad` ownership path
  that increments and captures a request generation before calling `Search`.
- R2. Search, guest-login, and tweet-load callbacks must use weak controller
  ownership and reject stale generations before starting later work.
- R3. All accepted UI/state completion must run on the main queue and reject a
  stale generation before replacing tweets or changing spinner/loading state.
- R4. A successful current request must replace the feed as one array instead
  of appending into prior results; failed or empty current requests must finish
  deterministically with an empty feed.
- R5. The latest refresh must not be discarded merely because an older request
  remains in flight.
- R6. Maintained checks must reject bypassed ownership, strong callback
  captures, stale checks removed from each boundary, append-based mutation,
  off-main completion, and stale spinner completion.
- R7. Existing search endpoints, guest authentication, tweet cells, navigation,
  sharing flows, dependencies, workflow, and legacy toolchain boundaries must
  remain unchanged.

## Implementation Units

### Feed request ownership

File: `HomeScreen/TweetsController.swift`

Add request generation state and small start/complete helpers. Route initial
and refresh loads through the start helper, capture the generation through the
full callback chain, collect loaded tweets locally, and replace the table only
from one main-queue completion helper when the generation is still current.

### Structural verification and guidance

Files:

- `scripts/check-baseline.py`
- `AGENTS.md`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-17-tweet-feed-generation.md`

Add function-scoped source and ordering contracts plus synchronized lifecycle
guidance. Record only verification that actually runs.

## Validation

- Run all four Make gates and external-directory `make check`.
- Run Python checker execution, workflow/project/plist/XML parsing, and exact
  diff audits.
- Reject isolated mutations for start-path bypass, generation capture removal,
  stale search/login/load acceptance, strong captures, append-based feed
  mutation, off-main completion, stale spinner completion, stale plan status,
  and weakened plan evidence.
- Require canonical push and pull-request checks on the exact delivery head
  before terminal tracker reconciliation.

## Boundaries

- This change does not alter Twitter search parameters, add pagination or
  retry UI, modernize Swift/UIKit/TwitterKit, edit project/vendor/lock files, or
  change share-composer behavior.
- Linux static verification cannot prove guest authentication, live search,
  table rendering, pull-to-refresh interaction, simulator behavior, or device
  networking.
- The new PR remains stacked on PR #8; no existing PR is merged or closed.

## Primary Reference

- Apple main-thread UI guidance remains authoritative for UIKit state changes;
  this archival project expresses that boundary with
  `NSOperationQueue.mainQueue().addOperationWithBlock`.

## Work Completed

- Routed initial and refresh requests through one generation-capturing start
  helper.
- Used weak ownership and stale-generation rejection across search, guest
  login, tweet loading, and main-queue UI completion.
- Replaced append-based table mutation with one current-generation array
  replacement and deterministic empty completion for current failures.
- Added function-scoped source, ordering, guidance, and plan contracts without
  changing Twitter endpoints, dependencies, project metadata, or share flows.

## Verification Completed

- All four Make gates passed and external-directory `make check` passed through
  the absolute Makefile path.
- Python checker execution, workflow/project/plist/XML validation, and
  `git diff --check` passed.
- Twelve isolated implementation mutations were rejected across both entry
  points, generation capture, weak search/login/load ownership, stale checks at
  every callback boundary, replacement-vs-append behavior, main-queue
  completion, and spinner ordering.
- Plan-aware review identified the missing early stale check in the final tweet
  model callback; the check was added before model collection, its focused
  mutation was rejected, and no actionable findings remain.
- `xcodebuild` and live Twitter services were unavailable on Linux, so no guest
  authentication, search result, table-rendering, refresh-interaction,
  simulator, or device-networking behavior is claimed.
