# Developer Notes

This document collects maintainer-facing notes for the COPR packaging repository.

## Renovate

The Renovate app from Mend is installed for this repository.

- Renovate app: `https://github.com/apps/renovate`
- Mend settings: `https://developer.mend.io/github/Iolaum`

This repository uses Renovate to propose version bumps for annotated RPM spec files.
The current spec annotations live next to the `Version:` field and identify the upstream release source for each package.

Each package owns its own directory so COPR subdirectory configuration, CI, and any future package-specific files stay isolated.

- `bun/` with `bun/bun.spec`
- `open-code/` with `open-code/open-code.spec`
- `python-hf-xet/` with `python-hf-xet/python-hf-xet.spec`

Renovate configuration lives in `renovate.json`.

## Maintainer expectations

- review Renovate pull requests before merge, especially for major upstream releases
- keep CI green on Renovate pull requests before merging
- verify that updated spec files still fetch sources and build cleanly
- treat `Release:` as a maintainer-managed field when packaging changes require more than a plain upstream version bump

## COPR rebuild automation

COPR packages in this repository should be configured as SCM packages that build from the `main` branch of the GitHub repository.

- set `Source Type` to `SCM`
- set `Clone URL` to the repository URL
- set `Committish` to `main`
- set the package `subdirectory` to its package folder, such as `bun/`, `open-code/`, or `python-hf-xet/`
- set the spec path inside that folder, such as `bun/bun.spec`, `open-code/open-code.spec`, or `python-hf-xet/python-hf-xet.spec`
- enable `Webhook rebuild` in the COPR package configuration
- add the COPR webhook URL to the GitHub repository webhook settings with content type `application/json`

The expected result is that each new commit to `main` triggers a COPR rebuild for the affected package configuration.

## CI and local validation

The CI workflow discovers package specs from the package directories rather than a shared `specs/` directory.

- iterate over `*/*.spec`
- install package build dependencies with `dnf builddep`
- run `rpmlint`, `spectool -Rg`, and `rpmbuild -ba` for each spec file

## Package-specific notes

### python-hf-xet

- keep the package naming Fedora-style: source package `python-hf-xet`, installable package `python3-hf-xet`
- use the upstream Linux `cp37-abi3` wheel for standard Fedora builds on `x86_64`
- do not switch to the upstream `cp313t` or `cp314t` wheels unless the packaging target explicitly changes to free-threaded Python
- avoid switching this package to a source build unless the repository intentionally adopts a Rust-native packaging workflow for it
