# COPR Packaging Repository

This repository contains the packaging metadata and automation needed to publish selected upstream software through Fedora COPR.

## Current status

The active COPR project is:

- `iolaum/aitoolkit`
- `https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/`

Current published package status:

- `bun` has been built successfully for `fedora-43-x86_64`

## Scope

The repository is intentionally focused on packaging and publication, not on mirroring upstream source trees or storing a hand-managed RPM repository.

It is used to:

- keep RPM spec files under version control
- let COPR fetch upstream release artifacts during builds
- build RPMs in Fedora infrastructure via COPR
- publish installable Fedora repositories for supported packages
- document packaging constraints, architecture choices, and maintenance workflow

It is not used to:

- maintain a local `createrepo_c` repository
- commit upstream release tarballs or binaries into git
- rebuild large upstream projects from source unless that becomes necessary later

## Initial package scope

The initial package set is:

- `bun`
- `open-code`

## Packaging strategy

### bun

`bun` will be packaged from upstream GitHub release binaries.

- primary architecture: `x86_64`
- secondary architecture: `aarch64`
- `x86_64` will use the optimized upstream Linux `x64` release, not the baseline build
- `aarch64` will use the standard upstream Linux ARM64 release

This favors performance on modern `x86_64` systems over backward compatibility with older CPUs.

Current Bun deployment status:

- COPR package name: `bun`
- current working chroot: `fedora-43-x86_64`
- source package method: COPR SCM build from this repository

Install on Fedora:

```bash
sudo dnf copr enable iolaum/aitoolkit
sudo dnf install bun
```

or in Fedora Silverblue:

```
sudo curl -Lo /etc/yum.repos.d/iolaum-aitoolkit.repo \
  https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/repo/fedora-$(rpm -E %fedora)/iolaum-aitoolkit-fedora-$(rpm -E %fedora).repo
sudo rpm-ostree install bun
```

Project page:

- `https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/`

### open-code

`open-code` refers to the upstream opencode desktop application package.

- package name in this repository and in RPM metadata should be `open-code`
- initial approach: repackage the upstream desktop `.rpm` release
- primary architecture: `x86_64`
- secondary architecture: `aarch64`
- preserve the upstream desktop application payload as-is for the first version
- preserve the bundled `opencode-cli` binary

This approach is chosen because it matches the current local workflow of consuming upstream release artifacts and publishing them as installable packages, while moving repository generation and hosting into COPR.

## Intended repository layout

The repository is expected to grow into a small packaging repo with files such as:

- `specs/bun.spec`
- `specs/open-code.spec`
- `.github/workflows/check.yml`
- `renovate.json`
- `PLAN.md`

## COPR workflow

The intended workflow is:

1. update spec files in this repository
2. validate them in CI with `rpmlint`, source fetching, and RPM builds
3. configure COPR SCM packages to build directly from this repository
4. let COPR generate and host repository metadata for Fedora users

This replaces the local workflow of downloading release files, renaming them manually, and running `createrepo_c` by hand.

## Local validation

The repository uses GitHub Actions to validate spec changes.

The current validation flow is:

```bash
rpmlint specs/ --strict
spectool -Rg specs/*.spec
rpmbuild -ba specs/*.spec
```
