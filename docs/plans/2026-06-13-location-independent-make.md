# Location-Independent HomeScreen Verification

status: completed

## Context

Rooted recipes support external callers, but GNU Make still split an absolute
Makefile path containing spaces before deriving the checkout root.

## Scope

1. Derive the repository root from an encoded `MAKEFILE_LIST` that preserves spaces.
2. Keep every verification script rooted at that decoded path.
3. Add a recursive-safe spaced-path full gate and synchronized contracts.
4. Preserve Swift, Xcode project, vendored framework, and workflow files.

## Work Completed

- Encoded spaces in `MAKEFILE_LIST` before Make tokenization and decoded the
  derived absolute checkout root for every verification recipe.
- Added a recursive-safe full-baseline regression that runs from an external
  directory against a copied checkout whose absolute path contains spaces.
- Tightened static contracts and guidance without changing application,
  project, vendored framework, or workflow files.

## Verification Completed

- Root and external-directory Make gates passed for all four aliases.
- GNU Make 4.2 and 4.4 space-containing absolute Makefile paths passed.
- The root-derivation mutation failed.
- The checker-invocation mutation failed.
- The plan-status mutation failed.
- The plan-evidence mutation failed.
- The documentation mutation failed.
- Checker compilation, diff hygiene, intended-path review, secret scanning, and generated-artifact inspection passed.

## Risk And Rollback

Verification path resolution only; rollback restores the relative recipe.
