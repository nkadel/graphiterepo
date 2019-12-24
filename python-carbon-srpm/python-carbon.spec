%global srcname carbon
%global commit0 f36da0f77aaf83a61f9880dec7abbf5c14a7d2bb
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global sum Back-end data caching and persistence daemon for Graphite


Name:           python-%{srcname}
Version:        1.1.5
Release:        4%{?dist}

Summary:        %{sum}
License:        ASL 2.0
URL:            https://github.com/graphite-project/carbon

Source0:        https://github.com/graphite-project/%{srcname}/archive/%{commit0}.tar.gz#/%{srcname}-%{shortcommit0}.tar.gz
Source10:       carbon-aggregator.1
Source11:       carbon-cache.1
Source12:       carbon-client.1
Source13:       carbon-relay.1
Source14:       validate-storage-schemas.1
Source20:       %{name}.logrotate

Source30:       carbon-aggregator.service
Source31:       carbon-cache.service
Source32:       carbon-relay.service
Source33:       carbon-aggregator@.service
Source34:       carbon-cache@.service
Source35:       carbon-relay@.service

Source43:       %{name}.sysconfig

# Set sane default filesystem paths.
Patch1:         %{name}-0.10.0-Set-sane-defaults.patch
# Fix path to storage-schemas.conf.
Patch2:         %{name}-0.9.13-Fix-path-to-storage-schemas.conf.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-cachetools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-protobuf
BuildRequires:  python%{python3_pkgversion}-twisted
BuildRequires:  python%{python3_pkgversion}-whisper

BuildRequires:    systemd


%description
Carbon is one of the components of Graphite, and is responsible for
receiving metrics over the network and writing them down to disk using
a storage back-end.


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{sum}
Requires:       python%{python3_pkgversion}-cachetools
Requires:       python%{python3_pkgversion}-twisted
Requires:       python%{python3_pkgversion}-protobuf
Requires:       python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}-whisper >= %{version}
Requires(pre):  shadow-utils

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}


%description -n python%{python3_pkgversion}-%{srcname}
Carbon is one of the components of Graphite, and is responsible for
receiving metrics over the network and writing them down to disk using
a storage back-end.


%prep
%autosetup -p1 -n %{srcname}-%{commit0}

sed -i '1s|^#!/usr/bin/env python|#!%{__python3}|' lib/carbon/amqp_listener.py
sed -i '1s|^#!/usr/bin/env python|#!%{__python3}|' lib/carbon/amqp_publisher.py

# disable tests which use mmh3 hash
sed -i "s|plugin == 'rules'|plugin == 'rules' or plugin.startswith('fast-')|" lib/carbon/tests/test_routers.py

# Disable internal log rotation.
sed -i -e 's/ENABLE_LOGROTATION.*/ENABLE_LOGROTATION = False/g' \
    conf/carbon.conf.example

# Skip Ceres database test. Ceres is not packaged yet.
rm lib/carbon/tests/test_database.py


%build
%py3_build


%install
%py3_install \
    --install-data=%{_localstatedir}/lib/carbon \
    --install-lib=%{python3_sitelib} \
    --install-scripts=%{_bindir}

rm -rf %{buildroot}%{_localstatedir}/lib/carbon/*
mkdir -p %{buildroot}%{_localstatedir}/lib/carbon/lists
mkdir -p %{buildroot}%{_localstatedir}/lib/carbon/rrd
mkdir -p %{buildroot}%{_localstatedir}/lib/carbon/whisper

# default config
mkdir -p %{buildroot}%{_sysconfdir}/carbon
install -D -p -m0644 conf/carbon.conf.example \
    %{buildroot}%{_sysconfdir}/carbon/carbon.conf
install -D -p -m0644 conf/storage-aggregation.conf.example \
    %{buildroot}%{_sysconfdir}/carbon/storage-aggregation.conf
install -D -p -m0644 conf/storage-schemas.conf.example \
    %{buildroot}%{_sysconfdir}/carbon/storage-schemas.conf

# man pages
mkdir -p %{buildroot}%{_mandir}/man1
install -D -p -m0644 %{SOURCE10} %{buildroot}%{_mandir}/man1
install -D -p -m0644 %{SOURCE11} %{buildroot}%{_mandir}/man1
install -D -p -m0644 %{SOURCE12} %{buildroot}%{_mandir}/man1
install -D -p -m0644 %{SOURCE13} %{buildroot}%{_mandir}/man1
install -D -p -m0644 %{SOURCE14} %{buildroot}%{_mandir}/man1

# log files
mkdir -p %{buildroot}%{_localstatedir}/log/carbon
install -D -p -m0644 %{SOURCE20} \
    %{buildroot}%{_sysconfdir}/logrotate.d/python%{python3_pkgversion}-%{srcname}

# init scripts
install -D -p -m0644 %{SOURCE30} \
    %{buildroot}%{_unitdir}/carbon-aggregator.service
install -D -p -m0644 %{SOURCE31} \
    %{buildroot}%{_unitdir}/carbon-cache.service
install -D -p -m0644 %{SOURCE32} \
    %{buildroot}%{_unitdir}/carbon-relay.service
install -D -p -m0644 %{SOURCE33} \
    %{buildroot}%{_unitdir}/carbon-aggregator@.service
install -D -p -m0644 %{SOURCE34} \
    %{buildroot}%{_unitdir}/carbon-cache@.service
install -D -p -m0644 %{SOURCE35} \
    %{buildroot}%{_unitdir}/carbon-relay@.service

# remove .py suffix
for i in %{buildroot}%{_bindir}/*.py; do
    mv ${i} ${i%%.py}
done

# fix permissions
chmod 755 %{buildroot}%{python3_sitelib}/carbon/amqp_listener.py
chmod 755 %{buildroot}%{python3_sitelib}/carbon/amqp_publisher.py


%pre -n python%{python3_pkgversion}-%{srcname}
getent group carbon >/dev/null || groupadd -r carbon
getent passwd carbon >/dev/null || \
    useradd -r -g carbon -d %{_localstatedir}/lib/carbon \
    -s /sbin/nologin -c "Carbon cache daemon" carbon


%post -n python%{python3_pkgversion}-%{srcname}
%systemd_post carbon-aggregator.service
%systemd_post carbon-cache.service
%systemd_post carbon-relay.service


%preun -n python%{python3_pkgversion}-%{srcname}
%systemd_preun carbon-aggregator.service
%systemd_preun carbon-cache.service
%systemd_preun carbon-relay.service


%postun -n python%{python3_pkgversion}-%{srcname}
%systemd_postun_with_restart carbon-aggregator.service
%systemd_postun_with_restart carbon-cache.service
%systemd_postun_with_restart carbon-relay.service


%check
PYTHONPATH=lib trial-3 carbon


%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%doc conf/ examples/ distro/redhat/init.d/

%{python3_sitelib}/carbon
%{python3_sitelib}/carbon-*-py?.?.egg-info
%{python3_sitelib}/twisted/plugins/*

%dir %{_sysconfdir}/carbon
%config(noreplace) %{_sysconfdir}/carbon/carbon.conf
%config(noreplace) %{_sysconfdir}/carbon/storage-aggregation.conf
%config(noreplace) %{_sysconfdir}/carbon/storage-schemas.conf

%config(noreplace) %{_sysconfdir}/logrotate.d/python%{python3_pkgversion}-%{srcname}

%attr(0755,carbon,carbon) %dir %{_localstatedir}/lib/carbon
%attr(0755,carbon,carbon) %dir %{_localstatedir}/lib/carbon/lists
%attr(0755,carbon,carbon) %dir %{_localstatedir}/lib/carbon/rrd
%attr(0755,carbon,carbon) %dir %{_localstatedir}/lib/carbon/whisper
%attr(0755,carbon,carbon) %dir %{_localstatedir}/log/carbon

%{_bindir}/carbon-aggregator
%{_bindir}/carbon-aggregator-cache
%{_bindir}/carbon-cache
%{_bindir}/carbon-client
%{_bindir}/carbon-relay
%{_bindir}/validate-storage-schemas

%{_mandir}/man1/carbon-aggregator.1*
%{_mandir}/man1/carbon-cache.1*
%{_mandir}/man1/carbon-client.1*
%{_mandir}/man1/carbon-relay.1*
%{_mandir}/man1/validate-storage-schemas.1*


%{_unitdir}/carbon-aggregator.service
%{_unitdir}/carbon-cache.service
%{_unitdir}/carbon-relay.service
%{_unitdir}/carbon-aggregator@.service
%{_unitdir}/carbon-cache@.service
%{_unitdir}/carbon-relay@.service


%changelog
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 11 2019 Piotr Popieluch <piotr1212@gmail.com> - 1.1.5-3
- Remove requires on configparser

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Piotr Popieluch <piotr1212@gmail.com> - 1.1.5-1
- Update to 1.1.5

* Thu Sep 27 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.4-2
- Remove Python 2 Subpackage

* Sat Sep 15 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.4-1
- Update to 1.1.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.3-2
- Switch to Python 3 by default
- Remove sys-v init

* Mon Apr 09 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.3-1
- Update to 1.1.3

* Wed Feb 28 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.2-1
- Update to 1.1.2
- Build python3-carbon

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.1-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 27 2017 Piotr Popieluch <piotr1212@gmail.com> - 1.1.1-2
- Add tests
- Add missing Requires

* Tue Dec 26 2017 Piotr Popieluch <piotr1212@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-0.4.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 piotr1212@gmail.com - 0.10.0-0.2.rc1
- Fix requires
- Fix logrotate name

* Thu Sep 22 2016 Piotr Popieluch <piotr1212@gmail.com> - 0.10.0-0.1.rc1
- Update to 0.10.0-rc1

* Sun Sep 18 2016 Piotr Popieluch <piotr1212@gmail.com> - - 0.9.15-6
- Set correct interpreter for amqp listener and publiser

* Sun Sep 18 2016 Piotr Popieluch <piotr1212@gmail.com> - 0.9.15-5
- Add example init script to upstream, rhbz#1360469
- Enable logrotate by default, fixes rhbz#1285727
- Add storage-aggregation.conf, fixes rhbz#1285725
- Update to newer package guidelines
- Remove el5 support
- Remove obsoleted macros
- Update URL

* Wed Aug 03 2016 Piotr Popieluch <piotr1212@gmail.com> - 0.9.15-4
- Add systemd unit files with instances

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 28 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.9.15-1
- Update to new version

* Sun Nov 08 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.9.14-1
- Update to new version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-0.2.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.9.13-0.1.pre1
- update to 0.9.13-pre1

* Mon Nov 24 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.12-7
- patch setup.py to prevent installation of upstream init scripts

* Fri Nov 14 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.12-6
- conditionally define macros for EPEL 6 and below

* Wed Oct 01 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.12-5
- update URL
- improve description
- use commit hash for Source URL
- use loop to rename files
- include README.md and examples/
- amend patch for filesystem default paths
- fix path to storage-schemas.conf
- add man pages from Debian
- disable internal log rotation and include logrotate configuration
  for Fedora >= 21 and EPEL >= 7
- be more explicit in %%files
- include python egg
- migrate to systemd on Fedora >= 21 and EPEL >= 7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 30 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-3
- Update default runtime user to carbon for carbon-aggregator and
  carbon-relay (RHBZ#1013813)

* Tue Sep 24 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-2
- Add strict python-whisper Requires (RHBZ#1010432)
- Don't cleanup user and user data on package remove (RHBZ#1010430)

* Mon Sep 02 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-1
- Update to 0.9.12

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 24 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-2
- Update spec to build on el5
- Fix python_sitelib definition

* Wed May 30 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-1
- Initial Package
