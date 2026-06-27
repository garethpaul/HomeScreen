# Location-Independent HomeScreen Verification

status: completed

## Context

Rooted recipes support external callers, but GNU Make still split an absolute
Makefile path containing spaces before deriving the checkout root.

## Scope

1. Derive the repository root from the single loaded Makefile path while preserving spaces.
2. Keep every verification script rooted at that decoded path.
3. Add a recursive-safe spaced-path full gate and synchronized contracts.
4. Preserve Swift, Xcode project, vendored framework, and workflow files.

## Work Completed

- Derived the absolute checkout root from the sole loaded Makefile path and
  rejected preloaded, overridden, or additional Makefiles.
- Added a recursive-safe full-baseline regression that runs from an external
  directory against a copied checkout whose absolute path contains spaces.
- Tightened static contracts and guidance without changing application,
  project, vendored framework, or workflow files.

## Verification Completed

- Root and external-directory Make gates passed for all four aliases.
- GNU Make 4.2 and 4.4 space-containing absolute Makefile paths passed.
- Preloaded, overridden, additional, and recipe-replacement Makefiles failed closed.
- The root-derivation mutation failed.
- The checker-invocation mutation failed.
- The plan-status mutation failed.
- The plan-evidence mutation failed.
- The documentation mutation failed.
- Checker compilation, diff hygiene, intended-path review, secret scanning, and generated-artifact inspection passed.

## Risk And Rollback

Verification path resolution only; rollback restores the relative recipe.
