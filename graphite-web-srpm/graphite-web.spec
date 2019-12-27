# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

%global commit0 53d96432b6ba1c30797405dff97ba01af009cb25
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           graphite-web
Version:        1.1.5
#Release:        2%%{?dist}
Release:        0%{?dist}

Summary:        A Django web application for enterprise scalable realtime graphing
License:        ASL 2.0
URL:            https://github.com/graphite-project/graphite-web

Source0:        https://github.com/graphite-project/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:        graphite-web-vhost.conf
Source2:        graphite-web-README.fedora
Source3:        graphite-web-graphite.wsgi
Source10:       %{name}.logrotate
Patch0:         %{name}-0.10.0-Amend-default-filesystem-locations.patch
Patch7:         %{name}-0.10.0-Disable-internal-log-rotation.patch

BuildArch:      noarch

BuildRequires:  python3-cairo
BuildRequires:  python3-devel
BuildRequires:  python3-django
BuildRequires:  python3-django-tagging
BuildRequires:  python3-mock
BuildRequires:  python3-pyparsing
BuildRequires:  python3-redis
BuildRequires:  python3-scandir
BuildRequires:  python3-six
BuildRequires:  python3-urllib3
BuildRequires:  python3-whisper

Requires:       dejavu-sans-fonts
Requires:       dejavu-serif-fonts
Requires:       python3-django
Requires:       python3-django-tagging
Requires:       python3-mod_wsgi
Requires:       python3-cairo
Requires:       python3-pyparsing
Requires:       python3-scandir
Requires:       python3-simplejson
Requires:       python3-carbon
Requires:       python3-configparser
Requires:       python3-pyparsing
Requires:       python3-scandir
Requires:       python3-simplejson
Requires:       python3-urllib3
Requires:       python3-whisper >= %{version}
Requires:       python3-whitenoise
Requires:       python3-memcached
Requires:       python3-pytz


%description
Graphite consists of a storage backend and a web-based visualization frontend.
Client applications send streams of numeric time-series data to the Graphite
backend (called carbon), where it gets stored in fixed-size database files
similar in design to RRD. The web frontend provides user interfaces
for visualizing this data in graphs as well as a simple URL-based API for
direct graph generation.

Graphite's design is focused on providing simple interfaces (both to users and
applications), real-time visualization, high-availability, and enterprise
scalability.


%prep
%autosetup -p1 -n graphite-web-%{commit0}
rm -rf webapp/graphite/thirdparty
find -type f -iname '*.swf' -delete

install -m0644 %{SOURCE2} README.fedora

sed -i '1s|^#!/usr/bin/env python|#!/usr/bin/python|' webapp/manage.py

# tests require a running redis
rm -rf webapp/tests/test_tags.py


%build
%py3_build


%install
%py3_install \
    --install-lib=%{python3_sitelib} \
    --install-data=%{_datadir}/graphite \
    --install-scripts=%{_bindir}

mkdir -p %{buildroot}%{_localstatedir}/lib/graphite-web
mkdir -p %{buildroot}%{_localstatedir}/log/graphite-web
mkdir -p %{buildroot}%{_sysconfdir}/graphite-web

install -Dp -m0644 webapp/graphite/local_settings.py.example \
    %{buildroot}%{_sysconfdir}/graphite-web/local_settings.py
ln -s %{_sysconfdir}/graphite-web/local_settings.py \
    %{buildroot}%{python3_sitelib}/graphite/local_settings.py
install -Dp -m0644 conf/dashboard.conf.example  \
    %{buildroot}%{_sysconfdir}/graphite-web/dashboard.conf
install -Dp -m0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/graphite-web.conf
install -Dp -m0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/graphite/graphite-web.wsgi

# Log rotation.
install -D -p -m0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Remove unneeded binaries.
rm -f %{buildroot}%{_bindir}/run-graphite-devel-server.py

# Rename build-index.sh.
mv %{buildroot}%{_bindir}/build-index %{buildroot}%{_bindir}/graphite-build-index
rm %{buildroot}%{_bindir}/build-index.sh


%check
pushd webapp
DJANGO_SETTINGS_MODULE=tests.settings %{__python3} manage.py test || :
popd


%files
%license LICENSE
%doc README.fedora conf/* examples/*

%dir %{_sysconfdir}/graphite-web
%config(noreplace) %{_sysconfdir}/httpd/conf.d/graphite-web.conf
%config(noreplace) %{_sysconfdir}/graphite-web/dashboard.conf
%config(noreplace) %{_sysconfdir}/graphite-web/local_settings.py*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%{_bindir}/graphite-build-index
%{_datadir}/graphite
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/graphite-web
%attr(0755,apache,apache) %dir %{_localstatedir}/log/graphite-web

%{python3_sitelib}/graphite/
%{python3_sitelib}/graphite_web-*-py?.?.egg-info


%changelog
* Thu Dec 26 2019 Nico Kadel-Garcia <nkadel@gmail.com>
- Dislable check for RHEL 8

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Piotr Popieluch <piotr1212@gmail.com> - 1.1.5-1
- Update to 1.1.5

* Mon Jan 14 2019 Piotr Popieluch <piotr1212@gmail.com> - 1.1.4-2
- Add missing urllib dependency

* Sat Sep 15 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.4-1
- Update to 1.1.4
- Switch to Python 3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.3-1
- Update to 1.1.3

* Mon Apr 09 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.2-1
- Update to 1.1.2
- Add tests

* Fri Mar 16 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-4
- On Fedora 28+, require django1.11
  (See https://fedoraproject.org/wiki/Changes/Django20)

* Tue Feb 20 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 26 2017 Piotr Popieluch <piotr1212@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Thu Nov 09 2017 Piotr Popieluch <piotr1212@gmail.com> - 1.0.2-2
- Add scandir dependency

* Mon Nov 06 2017 Piotr Popieluch <piotr1212@gmail.com> - 1.0.2-1
- Update to 1.0.2

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 26 2016 Piotr Popieluch <piotr1212@gmail.com> - - 0.10.0-0.1.rc1
- Update to 0.10.0-rc1

* Sat Sep 24 2016 Piotr Popieluch <piotr1212@gmail.com> - - 0.9.15-5
- Remove whitenoise patch
- Update specfile to newer package guidelines
- Remove el5 support
- Update URL
- Remove obsoleted macros

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Mar 18 2016 Piotr Popieluch <piotr1212@gmail.com> - 0.9.15-3
- Add missing Require on python-memcached

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 28 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.9.15-1
- Update to new version

* Wed Nov 11 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.9.14-1
- Update to new version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-0.4.aa992b9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 17 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.9.13-0.3.aa992b9
- fix IE 10 javascript issues

* Thu Feb  5 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.9.13-0.2.094cf54
- update to later commit to fix XSS

* Mon Jan 19 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.9.13-0.1.pre1
- update to upstream pre-release

* Fri Nov 14 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.12-8
- obsolete hacky graphite-web-selinux subpackage
- remove EPEL 5 related packaging things

* Wed Oct 01 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.12-7
- update URL
- use commit hash for Source URL
- package should own /etc/graphite-web
- do not ghost .pyc and .pyo files
- remove thirdparty libs and .swf files in %%prep
- split fhs+thirdparty patch into two discrete patches
- be more explicit in %%files
- include python egg
- include build-index.sh script (renamed to /usr/bin/graphite-build-index)
- make manage.py available at /usr/bin/graphite-manage
- patch for Django 1.5
- disable internal log rotation and use system logrotate
- apache needs httpd_sys_rw_content_t permissions instead of httpd_sys_content_t
- improve vhost configuration (including a fix for #1141701)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 01 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-5
- Patch for fix loading dashboards by name (RHBZ#1014349)
- Patch for log name of metric that throws exception for CarbonLink (RHBZ#1014349)
- Add deque to the PICKLE_SAFE filter (RHBZ#1014356)
- Merge in EL5 conditionals for single spec

* Mon Sep 30 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-4
- Remove logrotate configuration as it conflicts with internal
  log rotation (RHBZ#1008616)

* Tue Sep 24 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-3
- Reorder Requires conditionals to fix amzn1 issues (RHBZ#1007300)
- Ensure python-whisper is also updated

* Tue Sep 17 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-2
- Don't ship js/ext/resources/*.swf (RHBZ#1000253)

* Mon Sep 02 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-1
- Update to 0.9.12
- Require Django >= 1.3
- Add EL5 conditional for SELinux policycoreutils

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-7
- Update required fonts to actually include fonts (RHBZ#917361)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 30 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-5
- Conditionally require python-sqlite2
- Conditionally require new Django namespace

* Sat Dec 29 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-4
- Update to use mod_wsgi
- Update vhost configuration file to correctly work on multiple python
  versions

* Sat Nov 24 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-3
- Address all rpmlint errors
- Add SELinux subpackage README
- Patch out thirdparty code, Require it instead

* Fri Nov 09 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-2
- Add logrotate

* Thu May 31 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-1
- Initial Package
