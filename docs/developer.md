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
- `llm-wiki/` with `llm-wiki/llm-wiki.spec`
- `open-code/` with `open-code/open-code.spec`
- `python-hf-xet/` with `python-hf-xet/python-hf-xet.spec`
- `python-huggingface-hub/` with `python-huggingface-hub/python-huggingface-hub.spec`

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
- set the package `subdirectory` to its package folder, such as `bun/`, `llm-wiki/`, `open-code/`, `python-hf-xet/`, or `python-huggingface-hub/`
- set the spec path inside that folder, such as `bun/bun.spec`, `llm-wiki/llm-wiki.spec`, `open-code/open-code.spec`, `python-hf-xet/python-hf-xet.spec`, or `python-huggingface-hub/python-huggingface-hub.spec`
- enable `Webhook rebuild` in the COPR package configuration
- add the COPR webhook URL to the GitHub repository webhook settings with content type `application/json`

The expected result is that each new commit to `main` triggers a COPR rebuild for the affected package configuration.

## CI and local validation

The CI workflow discovers package specs from the package directories rather than a shared `specs/` directory.

- prefer running local validation in a temporary Fedora container with Podman rather than installing RPM tooling on the host
- start the container in an existing workdir such as `/root`, copy the repository into `/work`, and run validation from `/work`
- enable the published `iolaum/aitoolkit` COPR repository before resolving build dependencies
- full validation iterates over `*/*.spec`
- targeted validation can replace the loop with a single spec path when working on one package
- run `dnf builddep`, `rpmlint`, `spectool -Rg`, and `rpmbuild -ba` for each validated spec file

## Package-specific notes

### llm-wiki

- track upstream releases from `nashsu/llm_wiki`, not a fork
- repackage the upstream Tauri-generated `LLM.Wiki-<version>-1.x86_64.rpm` release artifact
- keep the package scoped to `x86_64` unless upstream release artifacts and repository architecture policy change together
- preserve the upstream desktop payload and bundled `libpdfium.so` resource as-is
- do not switch to rebuilding the Rust, Node, and Tauri application from source unless the repository intentionally adopts that heavier packaging workflow
- keep strip-related BRP post-processing disabled unless the rebuilt package is proven to preserve the Tauri binary and bundled PDFium resource correctly

### python-hf-xet

- keep the package naming Fedora-style: source package `python-hf-xet`, installable package `python3-hf-xet`
- use the upstream Linux `cp37-abi3` wheel for standard Fedora builds on `x86_64`
- do not switch to the upstream `cp313t` or `cp314t` wheels unless the packaging target explicitly changes to free-threaded Python
- avoid switching this package to a source build unless the repository intentionally adopts a Rust-native packaging workflow for it

### python-huggingface-hub

- keep the package naming Fedora-style: source package `python-huggingface-hub`, installable package `python3-huggingface-hub`
- package the upstream PyPI source release rather than vendoring the upstream git tree
- keep the package scoped to the repository's active `x86_64` target while `hf-xet` remains provided here as an `x86_64` package
- keep the upstream `hf` and `tiny-agents` entry points, and keep `python3-mcp` available so `tiny-agents` does not ship as a half-working CLI
- keep static `BuildRequires` for now instead of `%generate_buildrequires`
- reason: dynamic build requirements would pull `python3dist(hf-xet)` into `dnf builddep` resolution for CI, and GitHub Actions can only resolve that when the dependency has already been published in the COPR repo
- current CI enables the published `iolaum/aitoolkit` COPR repository before `dnf builddep`, which is enough for already-published dependencies but does not validate same-PR changes to both a dependency package and a dependent package
- revisit `%generate_buildrequires` only after CI can also resolve repo-local package outputs during the build-dependency phase
