%global debug_package %{nil}
%global __brp_strip %{nil}
%global __brp_strip_lto %{nil}
%global __brp_strip_comment_note %{nil}

Name: open-code
# renovate: datasource=github-releases depName=anomalyco/opencode
Version: 1.3.17
Release: 1%{?dist}
Summary: The open source AI coding agent

License: MIT
URL: https://github.com/anomalyco/opencode
Source0: %{url}/releases/download/v%{version}/opencode-desktop-linux-x86_64.rpm
Source1: https://raw.githubusercontent.com/anomalyco/opencode/v%{version}/LICENSE

ExclusiveArch: x86_64

BuildRequires: cpio
BuildRequires: desktop-file-utils
BuildRequires: rpm-build

%description
OpenCode is an open source AI coding agent desktop application.

This package republishes the upstream x86_64 desktop RPM payload through COPR
without modifying the installed application contents.

%prep
%setup -q -c -T
rpm2cpio %{SOURCE0} | cpio -idm --quiet

%build

%install
cp -a usr %{buildroot}/
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/LICENSE

%check
test -x usr/bin/OpenCode
test -x usr/bin/opencode-cli
desktop-file-validate usr/share/applications/OpenCode.desktop
test "$(%{buildroot}%{_bindir}/opencode-cli --version)" = "%{version}"
case "$(%{buildroot}%{_bindir}/opencode-cli --help 2>&1)" in \
  *"opencode attach <url>"*) ;; \
  *)
    printf '%s\n' 'packaged opencode-cli no longer exposes the expected OpenCode CLI help output' >&2
    exit 1
    ;;
esac

%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/OpenCode
%{_bindir}/opencode-cli
%{_datadir}/applications/OpenCode.desktop
%{_datadir}/icons/hicolor/128x128/apps/OpenCode.png
%{_datadir}/icons/hicolor/256x256@2/apps/OpenCode.png
%{_datadir}/icons/hicolor/32x32/apps/OpenCode.png

%changelog
* Mon Mar 16 2026 Nikos <14947634+Iolaum@users.noreply.github.com> - 1.2.27-2
- disable RPM strip/post-processing steps that truncate the bundled OpenCode CLI payload
- add CLI smoke checks so builds fail if the packaged binary falls back to Bun behavior
