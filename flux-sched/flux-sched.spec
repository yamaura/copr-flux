Name: flux-sched
Version: 0.45.0
Release: 1%{?dist}
Summary: Job Scheduling Facility for Flux Resource Manager Framework
Group: System Environment/Base
License: GPLv2+ 
URL:            https://github.com/flux-framework/%{name}
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz


BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
#let's not build the debug package for now 
%define debug_package %{nil}
#only compress -- no stripping etc 
%define __spec_install_post /usr/lib/rpm/brp-compress || :

%global __requires_exclude ^/bin/false$

ExcludeArch: ppc64le

BuildRequires: flux-core >= 0.76.0
Requires:      flux-core >= 0.76.0

BuildRequires:  gcc-toolset-12
Requires:       gcc-toolset-12-runtime
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  gettext-devel
BuildRequires:  cmake

BuildRequires: pkgconfig(libzmq) >= 4.1.4
BuildRequires: pkgconfig(libczmq) >= 3.0.2
BuildRequires: pkgconfig(jansson) >= 2.6
BuildRequires: pkgconfig(hwloc) >= 2.1
BuildRequires: pkgconfig(libxml-2.0) >= 2.9
BuildRequires: yaml-cpp-devel >= 0.5.1
BuildRequires: libuuid-devel
BuildRequires: libedit-devel

BuildRequires: boost >= 1.53.0
BuildRequires: boost-devel
BuildRequires: boost-system
BuildRequires: boost-graph
BuildRequires: boost-filesystem
BuildRequires: boost-regex

BuildRequires: python3-yaml
BuildRequires: python3-jsonschema
BuildRequires: python3-sphinx

# Should be pulled in by flux-core, but isn't
BuildRequires: python3-six
BuildRequires: python3-cffi

# Should be pulled in by flux-core
BuildRequires: python3 >= 3.6

# Required only by configure?
BuildRequires: python3-devel

# Required for 'make check'
BuildRequires: aspell aspell-en
BuildRequires: hostname
BuildRequires: man-db
BuildRequires: jq
BuildRequires: which
BuildRequires: file
BuildRequires: gdb


%description
flux-sched contains the Fluxion graph-based scheduler for the Flux
Resource Manager Framework. It consists of the sched-fluxion-resource
and sched-fluxion-qmanager modules which handle graph-based resource
matching and queue management services, respectively.

%prep
%autosetup -p1 -n %{name}-%{version}


%build
# Enable GCC Toolset 12
. /opt/rh/gcc-toolset-12/enable

cmake -B build \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DBOOST_ROOT=%{_prefix} \
    -DBoost_LIBRARY_DIRS=%{_libdir}
cmake --build build -- %{?_smp_mflags}

%check
ulimit -c unlimited
ctest -B build --output-on-failure || {
  cat build/*/*.log && exit 1
  }


%install
# RPM_BUILD_ROOT comes from BuildRoot tag.
rm -rf %{buildroot}
mkdir -p %{buildroot}
#cmake --install build --prefix {_prefix} --destdir {buildroot}
( cd build && \
  make install \
    DESTDIR=%{buildroot} \
)

# remove libtool archives
find %{buildroot} -name '*.la' -delete

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

# rc1,3 files for fluxion
%{_sysconfdir}/flux/rc1.d/01-sched-fluxion
%{_sysconfdir}/flux/rc3.d/01-sched-fluxion
%{_libdir}/flux/modules/sched-fluxion-qmanager.so
%{_libdir}/flux/modules/sched-fluxion-resource.so
%{_libdir}/flux/libreapi_cli.so
%{_libdir}/libfluxion-data.so.0.45
%{_libdir}/libfluxion-data.so.0.45.0
%{_libexecdir}/flux

# flux-ion-R
%{_libexecdir}/flux/cmd/flux-ion-R.py
%{python3_sitelib}/fluxion/*
%{_libdir}/flux/python3.9/*

# docs
%{_mandir}/man5/*

%post

%changelog
* Thu Jul 17 2025 Yuki Yamaura <ymruki@gmail.com> 0.45.0-1
- Bump release to flux-sched v0.45.0

* Tue Feb 14 2023 Mark A. Grondona <mgrondona@llnl.gov> 0.26.0-2
- Apply performance fixes from PR #1007

* Wed Feb  8 2023 Mark A. Grondona <mgrondona@llnl.gov> 0.26.0-1
- Bump release to flux-sched v0.26.0
- Update flux-core requires to v0.47.0

* Wed Oct  5 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.25.0-1
- Bump release to flux-sched v0.25.0
- update flux-core requires to v0.44.0
- remove flux-tree and flux-tree-helper from package

* Wed Aug  3 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.24.0-1
- Bump release to flux-sched v0.23.0
- update flux-core requires to v0.42.0

* Thu May 19 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.23.0-1
- Bump release to flux-sched v0.22.0
- update flux-core requires to v0.39.0

* Thu May 19 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.23.0-1
- Bump release to flux-sched v0.22.0
- update flux-core requires to v0.39.0

* Mon Apr 11 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.22.0-1
- Bump release to flux-sched v0.22.0
- update flux-core requires to v0.38.0

* Sat Mar  5 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.21.1-1
- Bump release to flux-sched v0.21.1
- update flux-core requires to v0.36.0 so older packages can be retired
- remove patch for missing doc file

* Wed Mar  2 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.21.0-1
- Bump release to flux-sched v0.21.0
- package new section 5 man pages
- add patch for missing doc file (issue #914)

* Wed Nov 10 2021 Mark A. Grondona <mgrondona@llnl.gov> 0.20.0-1
- Bump release to flux-sched v0.20.0

* Fri Oct 15 2021 Mark A. Grondona <mgrondona@llnl.gov> 0.19.0-1
- Bump release to flux-sched v0.19.0
- Bump flux-core requires to v0.30.0

* Tue Sep  7 2021 Mark A. Grondona <mgrondona@llnl.gov> 0.18.0-1
- Bump release to flux-sched v0.18.0
- Bump flux-core requires to v0.29.0
- Do not package rc.X dirs since they are owned by flux-core now

* Tue Jul  6 2021 Mark A. Grondona <mgrondona@llnl.gov> 0.17.0-1
- Bump release to flux-sched v0.17.0
- Bump flux-core requires to v0.28.0
- Replace readline-devel buildrequires with libedit-devel
- Remove workaround for Issude #796 (datastaging plugin install)

* Mon May 10 2021 Mark A. Grondona <mgrondona@llnl.gov> 0.16.0-2
- Fix installation of datastaging.so shell plugin

* Thu May  6 2021 Mark A. Grondona <mgrondona@llnl.gov> 0.16.0-1
- Bump release to flux-sched v0.16.0
- Bump flux-core requires to v0.26.0

* Fri Jan 29 2021 Mark A. Grondona <mgrondona@llnl.gov> 0.15.0-1
- Bump release to flux-sched v0.15.0
- Bump flux-core requires to v0.23.1
- Add flux-ion-R and python modules
- Disable ppc64le build due to Issue #808

* Tue Dec 22 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.14.0-1
- Bump release to flux-sched v0.14.0
- Bump flux-core requires to v0.22.0
- Add datastaging shell plugin to package

* Wed Oct 07 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.12.0-1
- Bump release to flux-sched v0.12.0
- Update requires to flux-core v0.20.0

* Wed Sep 02 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.11.0-1
- Bump release to flux-sched v0.11.0
- Update requires to flux-core v0.19.0

* Thu Jul 30 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.10.0-1
- Bump release to flux-sched v0.10.0
- Update requires to flux-core v0.18.0 or greater
- Update builrequires for t4

* Fri Jun 19 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.9.0-1
- Bump release to flux-sched v0.9.0
- Bump flux-core requires to v0.17.0
- Add python3-devel to BuildRequires
- Edit description to change name to Fluxion
- Change names of all components to fluxion variants
- Package flux-tree and its helper script

* Tue Feb 25 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.8.0-3
- Bump release to rebuild against flux-core v0.16.0

* Wed Feb  5 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.8.0-2
- Bump release to rebuild against flux-core v0.15.0

* Tue Jan 14 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.8.0-1
- Update to flux-sched v0.8.0
- Update package contents
- Disable tests due to #567
- Add PyYAML and python-jsonschema as BuildRequires
- export PYTON_VERSION=3.6

* Fri Jun 14 2019 Mark A. Grondona <mgrondona@llnl.gov> 0.7.1-1
- Bump package to 0.7.1

* Wed Jan 30 2019 Mark A. Grondona <mgrondona@llnl.gov> 0.7.0-2
- Remove priority_mod_fair_tree.so to avoid #433
- Bump release to 2

* Fri Jan 25 2019 Mark A. Grondona <mgrondona@llnl.gov> 0.7.0-1
- Bump package to 0.7.0
- Bump BuildRequires: flux-core to 0.11.0 or later
- Add yaml-cpp-devel to BuildRequires
- libflux-rdl.so no longer installed
- Add resource.so and rc* startup scrpits

* Fri Aug 03 2018 Mark A. Grondona 0.6.0-1
- Bump package to 0.6.0
- Bump BuildRequires: flux-core to 0.10.0 or later
- Remove deprecated flux/cpuset.so Lua module

* Mon May 14 2018 Mark A. Grondona 0.5.0-1
- Bump package to 0.5.0
- Bump BuildRequires: flux-core to 0.9.0 or later
- Bump BuildRequires: hwloc to 1.11.1 or later
- Add BuildRequires: readline-devel
- Add BuildRequires for boost
- Add workaround for priority_mod_fair_tree.so plugin installed in _libdir
- Add files in libdir/flux/modules/sched/* to manifest
- Add --with-boost-libdir to configure to workaround boost autoconf breakage

* Thu Aug 24 2017 Mark A. Grondona 0.4.0-1
- Bump package to 0.4.0
- Bump BuildRequires: flux-core to 0.8.0 or later
- Add jansson and libxml-2.0 BuildRequires

* Mon Aug 15 2016 Jim Garlick <garlick@llnl.gov> 0.2.0-1
- Bump package to 0.2.0
- Bump BuildRequires: flux-core to 0.4.0 or greater
- Drop Requires: flux-core, libuuid; should be covered by AutoReqProv

* Fri Aug 12 2016 Jim Garlick <garlick@llnl.gov> 0.1.0-4
- Rebuild for new flux-core, bump to rel 4

* Mon May 23 2016 Dong H. Ahn <ahn1@llnl.gov> 0.1.0-3
- Adjustment for TOSS3 deployment 
      Remove the use of environmental modules
      Adjust for installing into default system directories.
* Thu May 19 2016 Dong H. Ahn <ahn1@llnl.gov> 0.1.0-2
- Minor adjustment to flux-sched.module
* Sun May 15 2016 Dong H. Ahn <ahn1@llnl.gov> 0.1.0-1
- Build from initial flux-sched-0.1.0 tag
