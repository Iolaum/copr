%global debug_package %{nil}
%global __brp_strip %{nil}
%global __brp_strip_lto %{nil}
%global __brp_strip_comment_note %{nil}
%global __provides_exclude_from ^(/usr/lib/LLM Wiki/.*|%{_datadir}/applications/LLM Wiki\.desktop)$

Name: llm-wiki
# renovate: datasource=github-releases depName=nashsu/llm_wiki
Version: 0.4.0
Release: 1%{?dist}
Summary: Personal knowledge base for LLM concepts

License: GPL-3.0-only
URL: https://github.com/nashsu/llm_wiki
Source0: %{url}/releases/download/v%{version}/LLM.Wiki-%{version}-1.x86_64.rpm
Source1: %{url}/raw/v%{version}/LICENSE

ExclusiveArch: x86_64

BuildRequires: cpio
BuildRequires: desktop-file-utils
BuildRequires: rpm-build

%description
LLM Wiki is a desktop personal knowledge base for LLM concepts.

This package republishes the upstream x86_64 Tauri-generated RPM payload
through COPR without modifying the installed application contents.

%prep
%setup -q -c -T
rpm2cpio %{SOURCE0} | cpio -idm --quiet

%build

%install
cp -a usr %{buildroot}/
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/LICENSE

%check
test -x "%{buildroot}%{_bindir}/llm-wiki"
test -f "%{buildroot}/usr/lib/LLM Wiki/pdfium/libpdfium.so"
desktop-file-validate "%{buildroot}%{_datadir}/applications/LLM Wiki.desktop"

%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/llm-wiki
%dir "/usr/lib/LLM Wiki"
%dir "/usr/lib/LLM Wiki/pdfium"
"/usr/lib/LLM Wiki/pdfium/libpdfium.so"
"%{_datadir}/applications/LLM Wiki.desktop"
%{_datadir}/icons/hicolor/128x128/apps/llm-wiki.png
%{_datadir}/icons/hicolor/256x256@2/apps/llm-wiki.png
%{_datadir}/icons/hicolor/32x32/apps/llm-wiki.png

%changelog
%autochangelog
