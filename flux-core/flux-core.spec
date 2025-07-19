Name:           flux-core
Version:        0.76.0
Release:        2%{?dist}
Summary: Flux Resource Manager Framework
License:        LGPL-3.0-or-later
Group: System Environment/Base
URL:            https://github.com/flux-framework/%{name}
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

#  We can't build debuginfo packages because this strips binaries which
#  causes problems with symbol resolution in tools like launchmon.
#  Revisit once we've verified that debugging tools are fixed.
%define debug_package %{nil}
%define __spec_install_post /usr/lib/rpm/brp-compress || :

%global __requires_exclude ^/bin/false$

BuildRequires:  flux-security >= 0.14.0
Requires:       flux-security >= 0.14.0

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  gettext-devel

BuildRequires: pkgconfig(libsodium) >= 1.0.14
BuildRequires: pkgconfig(libzmq) >= 4.1.4
BuildRequires: pkgconfig(libczmq) >= 3.0.2
BuildRequires: pkgconfig(jansson) >= 2.6
BuildRequires: pkgconfig(hwloc) >= 2.1
BuildRequires: pkgconfig(sqlite3) >= 3.6.0
BuildRequires: pkgconfig(bash-completion)
BuildRequires: lua-devel >= 5.1
BuildRequires: lz4-devel
BuildRequires: munge-devel
BuildRequires: lua-posix
BuildRequires: libuuid-devel
BuildRequires: ncurses-devel
BuildRequires: libarchive-devel
# for _tmpfilesdir
BuildRequires: systemd-rpm-macros
BuildRequires: systemd-devel

# for chrpath
BuildRequires: chrpath

%if 0%{?bl6}
BuildRequires: ibm_smpi-devel
BuildRequires: libevent
%endif

# requirements specifically for 'make check'
BuildRequires: aspell aspell-en
BuildRequires: hostname
BuildRequires: man-db
BuildRequires: jq
BuildRequires: which
BuildRequires: file

# libtool CCLD of libflux-core.la adds -lsodium -lpgm -lgssapi_krb5
BuildRequires: libsodium-devel >= 0.4.5
BuildRequires: openpgm-devel
BuildRequires: krb5-devel

# rely on autoreq for most dependencies
Requires: lua >= 5.1
Requires: lua-posix >= 5.1
Requires: sqlite >= 3.6.0
Requires: libuuid
Requires: ncurses

BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-cffi
BuildRequires: python3-yaml
BuildRequires: python3-jsonschema
BuildRequires: python3-sphinx
BuildRequires: python3-ply

Requires: python3
Requires: python3-cffi

Requires:       ncurses
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Flux Framework is a suite of projects, tools and libraries which may
be used to build site-custom resource managers at High Performance
Computing sites.

flux-core implements the communication layer and lowest level services
and interfaces for the Flux resource manager framework. It consists of
a distributed message broker and plug-in comms modules that implement
various distributed services.


%prep
%autosetup -n %{name}-%{version} -p1

%build

export LC_ALL=en_US.UTF-8

export CFLAGS="%{optflags} -Wno-error -Wno-error=strict-aliasing -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -Wno-error -Wno-error=strict-aliasing -fno-strict-aliasing"
%configure \
    --with-systemdsystemunitdir=%{_unitdir} \
    --with-flux-security
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# Flux test‑suite can be lengthy; allow failures on slow CI
timeout 5m make -k check || :

%post
%systemd_post flux.service
%systemd_post flux-epilog@.service
%systemd_post flux-housekeeping@.service
%systemd_post flux-prolog@.service

%preun
%systemd_preun flux.service
%systemd_preun flux-epilog@.service
%systemd_preun flux-housekeeping@.service
%systemd_preun flux-prolog@.service

%postun
%systemd_postun_with_restart flux.service
%systemd_postun_with_restart flux-epilog@.service
%systemd_postun_with_restart flux-housekeeping@.service
%systemd_postun_with_restart flux-prolog@.service

%files
%defattr(-,root,root)

# commands + other executables
%{_bindir}/flux
%{_bindir}/flux-python
%{_libexecdir}/flux

# this package owns top level libdir/flux
%dir %{_libdir}/flux

# connectors + comms modules
%{_libdir}/flux/connectors
%{_libdir}/flux/modules

# job-manager plugins
%{_libdir}/flux/job-manager

# libs
%{_libdir}/lib%{name}.so.2
%{_libdir}/lib%{name}.so.2.0.0
%{_libdir}/libflux-idset.so.1
%{_libdir}/libflux-idset.so.1.0.0
%{_libdir}/libflux-optparse.so.1
%{_libdir}/libflux-optparse.so.1.0.0
%{_libdir}/libflux-schedutil.so.1
%{_libdir}/libflux-schedutil.so.1.0.0
%{_libdir}/libflux-hostlist.so.1
%{_libdir}/libflux-hostlist.so.1.0.0
%{_libdir}/libflux-taskmap.so.1
%{_libdir}/libflux-taskmap.so.1.0.0

# pmi libs required in base pkg not devel
%{_libdir}/flux/libpmi.so
%{_libdir}/flux/libpmi.so.0
%{_libdir}/flux/libpmi.so.0.0.0
%{_libdir}/flux/libpmi2.so
%{_libdir}/flux/libpmi2.so.0
%{_libdir}/flux/libpmi2.so.0.0.0

# devel
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/flux-pmi.pc
%{_libdir}/pkgconfig/flux-optparse.pc
%{_libdir}/pkgconfig/flux-idset.pc
%{_libdir}/pkgconfig/flux-schedutil.pc
%{_libdir}/pkgconfig/flux-hostlist.pc
%{_libdir}/pkgconfig/flux-taskmap.pc
%{_libdir}/*.so
%{_includedir}/flux

# doc + "flux help" config file (json)
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_datadir}/flux

# tmpfiles config
%{_tmpfilesdir}/*

# bash completions
%{_sysconfdir}/bash_completion.d/flux
%{_sysconfdir}/flux/system/cron.d/kvs-backup.cron

# lua binding/modules
%{_libdir}/lua/%{lua_version}/flux.so
%{_datadir}/lua/%{lua_version}/flux
%{_datadir}/lua/%{lua_version}/fluxometer
%{_datadir}/lua/%{lua_version}/fluxometer.lua

# rc scripts
%dir %{_sysconfdir}/flux
%dir %{_sysconfdir}/flux/rc1.d
# dir {_sysconfdir}/flux/rc3.d # Generated by rc3 ? TODO: install
%{_sysconfdir}/flux/rc1
%{_sysconfdir}/flux/rc1.d/*
%{_sysconfdir}/flux/rc3

# systemd unit file
%{_unitdir}/flux.service
%{_unitdir}/flux-epilog@.service
%{_unitdir}/flux-housekeeping@.service
%{_unitdir}/flux-prolog@.service

# shell
%dir %{_sysconfdir}/flux/shell
%dir %{_sysconfdir}/flux/shell/lua.d
%dir %{_sysconfdir}/flux/shell/lua.d/mpi
%{_sysconfdir}/flux/shell/initrc.lua
%{_sysconfdir}/flux/shell/lua.d/*.lua
%{_sysconfdir}/flux/shell/lua.d/mpi/*.lua

# python binding
%{python3_sitearch}/*
#usr/lib/python3.9/site-packages/flux/*
# python bindings links
%{_libdir}/flux/python3.9/*
#
#{python3_sitelib}/_flux/*
#{python3_sitelib}/flux/*

%changelog
* Sat Jul 19 2025 Yuki Yamaura <ymruki@gmail.com> – 0.73.0-2
- Add systemd

* Mon Jul 14 2025 Yuki Yamaura <ymruki@gmail.com> – 0.73.0-1
- Initial RPM package for Flux-core
