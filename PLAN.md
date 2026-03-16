# Implementation Plan

This checklist captures the initial plan for turning this repository into the source of truth for a Fedora COPR packaging workflow.

## Repository foundation

- [x] Create a `specs/` directory for RPM spec files.
- [x] Add `specs/bun.spec`.
- [x] Add `specs/open-code.spec`.
- [x] Add a repository license file.
- [x] Add a GitHub Actions workflow at `.github/workflows/check.yml`.
- [ ] Add `renovate.json` for version update automation.

## Scope and policy

- [x] Keep this repository focused on packaging metadata and automation.
- [x] Do not commit upstream release artifacts into git.
- [x] Let COPR fetch upstream sources and release files via spec `Source:` URLs.
- [x] Use COPR SCM builds so Fedora infrastructure builds from this repository directly.
- [x] Replace the local `createrepo_c` workflow with COPR-hosted repository metadata.

## bun packaging

- [x] Package `bun` from upstream GitHub release binaries.
- [x] Support `x86_64` as the primary architecture.
- [ ] Support `aarch64` as the secondary architecture.
- [x] Use the optimized upstream Linux `x64` build for `x86_64`.
- [ ] Use the standard upstream Linux ARM64 build for `aarch64`.
- [ ] Add `ExclusiveArch: x86_64 aarch64` to the spec.
- [x] Document that the optimized `x86_64` build may require newer CPU features.
- [x] Validate that the package installs the Bun binary cleanly into `%{_bindir}`.
- [ ] Review Bun licensing and redistribution implications before publishing broadly.

## open-code packaging

- [x] Package the opencode desktop release under the RPM name `open-code`.
- [x] Start by repackaging the upstream desktop `.rpm` release.
- [x] Support `x86_64` as the primary architecture.
- [ ] Support `aarch64` as the secondary architecture.
- [ ] Confirm the upstream release naming pattern for both architectures.
- [x] Decide how to extract and repackage the upstream desktop RPM contents in a COPR-friendly way.
- [ ] Verify desktop integration details such as icons, desktop file, and runtime dependencies.
- [x] Defer any source-native desktop build investigation until after the repackage workflow works.

## CI and local validation

- [x] Run `rpmlint` on all spec files in CI.
- [x] Run `spectool -Rg` in CI to verify source URLs.
- [x] Run `rpmbuild -ba` in CI for all spec files.
- [x] Make the CI workflow fail on invalid specs or broken source URLs.
- [x] Document the local validation commands in `README.md`.

## COPR setup

- [x] Create a COPR project for this repository.
- [x] Enable the desired Fedora chroots.
- [x] Add an SCM package for `bun`.
- [ ] Add an SCM package for `open-code`.
- [x] Configure each SCM package to point at this git repository.
- [x] Set the correct spec path for each package in COPR.
- [ ] Enable auto-rebuilds or webhook-triggered rebuilds where appropriate.
- [x] Verify that successful builds appear in the published COPR repository.

## Rollout order

- [x] Implement `bun` for `x86_64` first.
- [ ] Add `bun` for `aarch64`.
- [ ] Implement `open-code` for `x86_64`.
- [ ] Add `open-code` for `aarch64`.
- [x] Test installation from the COPR repo on Fedora systems.

## Follow-up documentation

- [x] Add package-specific notes to `README.md` once the first specs exist.
- [ ] Document how version bumps should be performed.
- [x] Document how users enable the resulting COPR repository.
- [x] Document known limitations for CPU architecture and upstream packaging choices.
