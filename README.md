# COPR Packaging Repository

This repository contains the packaging metadata and automation needed to publish selected upstream software through Fedora COPR.

## Current status

The active COPR project is:

- `iolaum/aitoolkit`
- `https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/`

Current published package status:

- `bun`: [![Copr build status](https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/package/bun/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/package/bun/)
- `open-code`: [![Copr build status](https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/package/open-code/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/package/open-code/)

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

`bun` is packaged from upstream GitHub release binaries.

- primary architecture: `x86_64`
- secondary architecture: `aarch64` is planned but not yet enabled
- `x86_64` will use the optimized upstream Linux `x64` release, not the baseline build
- `aarch64` will use the standard upstream Linux ARM64 release once support is added

This favors performance on modern `x86_64` systems over backward compatibility with older CPUs.

Current Bun deployment status:

- COPR package name: `bun`
- current working chroot: `fedora-43-x86_64`
- source package method: COPR SCM build from this repository

Install on Fedora:

```bash
sudo dnf copr enable iolaum/aitoolkit
sudo dnf install bun
bun --version
```

or in Fedora Silverblue:

```
sudo curl -Lo /etc/yum.repos.d/iolaum-aitoolkit.repo \
  https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/repo/fedora-$(rpm -E %fedora)/iolaum-aitoolkit-fedora-$(rpm -E %fedora).repo
sudo rpm-ostree install bun
```

For Silverblue and related rpm-ostree systems, reboot into the new deployment or start a new shell session before verifying the install with `bun --version`.

Project page:

- `https://copr.fedorainfracloud.org/coprs/iolaum/aitoolkit/`

### open-code

`open-code` refers to the upstream opencode desktop application package.

- package name in this repository and in RPM metadata should be `open-code`
- initial approach: repackage the upstream desktop `.rpm` release
- primary architecture: `x86_64`
- secondary architecture: `aarch64` is planned but not yet enabled
- preserve the upstream desktop application payload as-is for the first version
- preserve the bundled `opencode-cli` binary

This approach is chosen because it matches the current local workflow of consuming upstream release artifacts and publishing them as installable packages, while moving repository generation and hosting into COPR.

Packaging note:

- `open-code` disables Fedora RPM strip-related BRP post-processing during rebuilds
- this is required because the upstream `opencode-cli` binary carries bundled payload data that gets truncated by default strip steps
- the spec includes smoke checks to verify the packaged CLI still reports the expected OpenCode version and help output

Install on Fedora:

```bash
sudo dnf copr enable iolaum/aitoolkit
sudo dnf install open-code
opencode-cli --version
```

Desktop verification after install:

- confirm `OpenCode` appears in the desktop launcher
- launch `OpenCode` once to verify the desktop entry, icons, and bundled runtime work as expected

## Intended repository layout

Each package now lives in its own directory so COPR package subdirectories, build separation, and any future package-specific metadata stay isolated.

The repository is expected to grow into a small packaging repo with files such as:

- `bun/bun.spec`
- `open-code/open-code.spec`
- `docs/developer.md`
- `.github/workflows/check.yml`
- `renovate.json`

## COPR workflow

The intended workflow is:

1. update spec files in this repository
2. let Renovate propose `Version:` bumps for annotated spec files when supported upstream releases change
3. validate changes in CI with `rpmlint`, source fetching, and RPM builds
4. review and merge the resulting pull request
5. configure COPR packages to build from this repository with source type `SCM`, clone URL set to this GitHub repository, and `Committish` set to `main`
6. set each package `subdirectory` to its package folder, such as `bun/` or `open-code/`, and set the matching spec path inside that folder
7. enable `Webhook rebuild` for each COPR SCM package
8. add the COPR webhook URL to the GitHub repository webhook settings with content type `application/json`
9. let COPR rebuild from new commits on `main`, generate and host repository metadata for Fedora users, and publish the updated package
10. verify the published package in COPR and test installation from a Fedora system

This repository uses the Renovate GitHub App from Mend (`https://github.com/apps/renovate`) to automate supported package version updates.
Maintainer-facing notes for Renovate and related workflow details are documented in `docs/developer.md`.

This replaces the local workflow of downloading release files, renaming them manually, and running `createrepo_c` by hand.

For routine package updates:

1. wait for Renovate to open a pull request for supported upstream releases, or update the spec manually when needed
2. run local validation or open a pull request and let CI validate the change
3. review whether the change is a straightforward `Version:` bump or also needs packaging adjustments
4. merge the change to `main` so GitHub sends the webhook event to COPR
5. confirm that COPR starts a new SCM build from `main` for the updated package
6. confirm the new build appears in the expected Fedora chroot
7. install or upgrade from the COPR repository and verify the packaged application behavior

For automatic COPR rebuilds from GitHub:

1. open the package configuration in the COPR project
2. set `Source Type` to `SCM`
3. set `Clone URL` to the GitHub repository URL
4. set `Committish` to `main`
5. set the package subdirectory to the package folder, such as `bun/` or `open-code/`, and set the matching spec path inside that folder
6. enable `Webhook rebuild`
7. copy the webhook URL shown by COPR
8. add that URL in GitHub under repository `Settings` -> `Webhooks`
9. set the GitHub webhook content type to `application/json`
10. save the webhook and verify that a new commit to `main` triggers a COPR rebuild

## Local validation

The repository uses GitHub Actions to validate spec changes.

The current validation flow is:

```bash
for file in */*.spec; do
  rpmlint "$file" --strict
  spectool -Rg "$file"
  rpmbuild -ba "$file"
done
```
