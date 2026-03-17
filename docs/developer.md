# Developer Notes

This document collects maintainer-facing notes for the COPR packaging repository.

## Renovate

The Renovate app from Mend is installed for this repository.

- Renovate app: `https://github.com/apps/renovate`
- Mend settings: `https://developer.mend.io/github/Iolaum`

This repository uses Renovate to propose version bumps for annotated RPM spec files.
The current spec annotations live next to the `Version:` field and identify the upstream release source for each package.

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
- set spec path and subdirectory fields for each package as needed
- enable `Webhook rebuild` in the COPR package configuration
- add the COPR webhook URL to the GitHub repository webhook settings with content type `application/json`

The expected result is that each new commit to `main` triggers a COPR rebuild for the affected package configuration.
