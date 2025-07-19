Name:    flux-security
Version: 0.14.0
Release: 2%{?dist}

Summary: Flux Resource Manager Framework
License: LGPLv3
Group: System Environment/Base
URL:            https://github.com/flux-framework/%{name}
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
%define debug_package %{nil}
%define __spec_install_post /usr/lib/rpm/brp-compress || :

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  gettext-devel
BuildRequires:  pam-devel

BuildRequires: pkgconfig(libsodium) >= 1.0.14
BuildRequires: pkgconfig(jansson) >= 2.6
BuildRequires: munge-devel
BuildRequires: libuuid-devel

# for man pages
BuildRequires: python3-sphinx

# rely on autoreq for most dependencies

%description
Flux Framework is a suite of projects, tools and libraries which may
be used to build site-custom resource managers at High Performance
Computing sites.

flux-security implements Flux security code and APIs, including the
privileged IMP executable.

%prep
%autosetup -n %{name}-%{version}

%build

CFLAGS="${KOJI_CFLAGS}"
export CFLAGS

%configure \
       --enable-pam \
       --disable-static || (cat config.log && exit 1)

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
find ${RPM_BUILD_ROOT} -name *.la | while read f; do rm -f $f; done

# Create packaged directories
mkdir -p 755 ${RPM_BUILD_ROOT}/etc/flux/imp/conf.d

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)

# IMP executable
%attr(04755, root, root) %{_libexecdir}/flux/flux-imp

# libs
%{_libdir}/lib%{name}.so.1
%{_libdir}/lib%{name}.so.1.0.0

# devel
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so
%{_includedir}/flux

# docs
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

# conf
%dir %{_sysconfdir}/flux
%dir %{_sysconfdir}/flux/security
%dir %{_sysconfdir}/flux/imp
%dir %{_sysconfdir}/flux/imp/conf.d
%config %{_sysconfdir}/flux/security/conf.d/sign.toml

%changelog
* Sat Jul 19 2025 Yuki Yamaura <ymruki@gmail.com> 0.14.0-2
- --enable-pam is now default

* Thu Jul 17 2025 Yuki Yamaura <ymruki@gmail.com> 0.14.0-1
- Update to flux-security v0.14.0

* Mon Jun  6 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.7.0-1
- Update to flux-security v0.7.0
- Package section 3 manpages

* Mon Jan 31 2022 Mark A. Grondona <mgrondona@llnl.gov> 0.6.0-1
- Update to flux-security v0.6.0
- Add sphinx buildrequires and package man pages

* Sat Sep  4 2021 Mark A. Grondona <mgrondona@llnl.gov> 0.5.0-1
- Update to flux-security v0.5.0
- Package missing /etc/flux/{security,imp,imp/conf.d} directories

* Thu Dec 17 2020 Mark A. Grondona <mgrondona@llnl.gov> 0.4.0-2
- Add sign.toml config file to package
- Remove custom CFLAGS (does not compile on TOSS4)

* Thu Oct 22 2020 Jim Garlick <garlick@llnl.gov> 0.4.0-1
- Initial package for TOSS
