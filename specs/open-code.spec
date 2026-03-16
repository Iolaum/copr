%global debug_package %{nil}

Name: open-code
# renovate: datasource=github-releases depName=anomalyco/opencode
Version: 1.2.27
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

%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/OpenCode
%{_bindir}/opencode-cli
%{_datadir}/applications/OpenCode.desktop
%{_datadir}/icons/hicolor/128x128/apps/OpenCode.png
%{_datadir}/icons/hicolor/256x256@2/apps/OpenCode.png
%{_datadir}/icons/hicolor/32x32/apps/OpenCode.png

%changelog
%autochangelog
