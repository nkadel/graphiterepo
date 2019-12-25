%global pypi_name twisted
%global with_python2 1

%if 0%{?rhel} && 0%{?rhel} >= 8
%global with_python2 0
%endif

%global common_description %{expand:
Twisted is a networking engine written in Python, supporting numerous protocols.
It contains a web server, numerous chat clients, chat servers, mail servers
and more.}

Name:           python-%{pypi_name}
Version:        19.2.1
Release:        1%{?dist}.1
Summary:        Twisted is a networking engine written in Python

License:        MIT
URL:            http://twistedmatrix.com/
Source0:        https://files.pythonhosted.org/packages/source/T/Twisted/Twisted-%{version}.tar.bz2
# Import gobject from gi.repository for Python 3
# https://twistedmatrix.com/trac/ticket/9642
Patch1:         0001-Import-gobject-from-gi.repository-in-Python-3.patch

%{?python_enable_dependency_generator}

%description
%{common_description}


%if 0%{?with_python2}
%package -n python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  gcc
BuildRequires:  python2-devel >= 2.6
BuildRequires:  python2-appdirs >= 1.4.0
BuildRequires:  python2-automat >= 0.3.0
BuildRequires:  python2-attrs >= 17.4.0
BuildRequires:  python2-constantly >= 15.1
BuildRequires:  python2-cryptography >= 2.3
#BuildRequires:  (python2-h2 >= 3.0 with python2-h2 < 4.0)
BuildRequires:  python2-h2 >= 3.0
BuildRequires:  python2-hyperlink >= 17.1.1
BuildRequires:  python2-idna >= 2.5
BuildRequires:  python2-incremental >= 16.10.1
#BuildRequires:  (python2-priority >= 1.1.0 with python2-priority < 2.0)
BuildRequires:  python2-priority >= 1.1.0
BuildRequires:  python2-pyasn1)
BuildRequires:  python2-pyopenssl >= 16.0.0
BuildRequires:  python2-pyserial >= 3.0
BuildRequires:  python2-service-identity >= 18.1.0
BuildRequires:  python2-setuptools)
BuildRequires:  python2-zope.interface >= 4.4.2
BuildRequires:  python2-pyhamcrest >= 1.9.0

%if 0%{?fedora}
Recommends:     python2-service-identity >= 18.1.0
%endif

%description -n python2-%{pypi_name}
%{common_description}
%endif  # with_python2


%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

BuildRequires:  gcc
BuildRequires:  python%{python3_pkgversion}-devel >= 3.3
BuildRequires:  python%{python3_pkgversion}-appdirs >= 1.4.0
BuildRequires:  python%{python3_pkgversion}-automat >= 0.3.0
BuildRequires:  python%{python3_pkgversion}-attrs >= 17.4.0
BuildRequires:  python%{python3_pkgversion}-constantly >= 15.1
BuildRequires:  python%{python3_pkgversion}-cryptography >= 2.3
#BuildRequires:  (python%{python3_pkgversion}-h2 >= 3.0 with python%{python3_pkgversion}-h2 < 4.0)
BuildRequires:  python%{python3_pkgversion}-h2 >= 3.0
BuildRequires:  python%{python3_pkgversion}-hyperlink >= 17.1.1
BuildRequires:  python%{python3_pkgversion}-idna >= 2.5
BuildRequires:  python%{python3_pkgversion}-incremental >= 16.10.1
#BuildRequires:  (python%{python3_pkgversion}-priority >= 1.1.0 with python%{python3_pkgversion}-priority < 2.0)
BuildRequires:  python%{python3_pkgversion}-priority >= 1.1.0
BuildRequires:  python%{python3_pkgversion}-pyasn1)
BuildRequires:  python%{python3_pkgversion}-pyopenssl >= 16.0.0
BuildRequires:  python%{python3_pkgversion}-pyserial >= 3.0
BuildRequires:  python%{python3_pkgversion}-service-identity >= 18.1.0
BuildRequires:  python%{python3_pkgversion}-setuptools)
BuildRequires:  python%{python3_pkgversion}-sphinx >= 1.3.1
BuildRequires:  python%{python3_pkgversion}-zope.interface >= 4.4.2
BuildRequires:  python%{python3_pkgversion}-pyhamcrest >= 1.9.0

%if 0%{?fedora}
Recommends:     python%{python3_pkgversion}-service-identity  >= 18.1.0
%endif

%description -n python%{python3_pkgversion}-%{pypi_name}
%{common_description}


%prep
%autosetup -p1 -n Twisted-%{version}


%build
%if 0%{?with_python2}
%py2_build
%endif  # with_python2
%py3_build

# generate html docs
PYTHONPATH=${PWD}/src/ sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%if 0%{?with_python2}
%py2_install

# Packages that install arch-independent twisted plugins install here.
# https://bugzilla.redhat.com/show_bug.cgi?id=1252140
mkdir -p %{buildroot}%{python2_sitelib}/twisted/plugins

# pem-certificate
# Needed for self-tests.

# wrong-script-interpreter
# pop3testserver.py: applies to py2.4 and that is the current default
# scripttest.py: is noop

# non-executable-script
chmod +x %{buildroot}%{python2_sitearch}/twisted/mail/test/pop3testserver.py
chmod +x %{buildroot}%{python2_sitearch}/twisted/trial/test/scripttest.py

# non-standard-executable-perm
chmod 755 %{buildroot}%{python2_sitearch}/twisted/python/_sendmsg.so
chmod 755 %{buildroot}%{python2_sitearch}/twisted/test/raiser.so

# Move and symlink python2 scripts
# no-manual-page-for-binary: man page is trial and twistd
mv %{buildroot}%{_bindir}/trial %{buildroot}%{_bindir}/trial-%{python2_version}
ln -s ./trial-%{python2_version} %{buildroot}%{_bindir}/trial-2

mv %{buildroot}%{_bindir}/twistd %{buildroot}%{_bindir}/twistd-%{python2_version}
ln -s ./twistd-%{python2_version} %{buildroot}%{_bindir}/twistd-2

# ambiguous shebangs
pathfix.py -pn -i %{__python2} %{buildroot}%{python2_sitelib} %{buildroot}%{python2_sitearch}

%endif  # with_python2

%py3_install

# Packages that install arch-independent twisted plugins install here.
# https://bugzilla.redhat.com/show_bug.cgi?id=1252140
mkdir -p %{buildroot}%{python3_sitelib}/twisted/plugins

# no-manual-page-for-binary
mkdir -p %{buildroot}%{_mandir}/man1/
for s in conch core mail; do
cp -a docs/$s/man/*.1 %{buildroot}%{_mandir}/man1/
done

# Move and symlink python3 scripts
# no-manual-page-for-binary: man page is trial and twistd
mv %{buildroot}%{_bindir}/trial %{buildroot}%{_bindir}/trial-%{python3_version}
ln -s ./trial-%{python3_version} %{buildroot}%{_bindir}/trial-3
ln -s ./trial-%{python3_version} %{buildroot}%{_bindir}/trial

mv %{buildroot}%{_bindir}/twistd %{buildroot}%{_bindir}/twistd-%{python3_version}
ln -s ./twistd-%{python3_version} %{buildroot}%{_bindir}/twistd-3
ln -s ./twistd-%{python3_version} %{buildroot}%{_bindir}/twistd

# non-executable-script
chmod +x %{buildroot}%{python3_sitearch}/twisted/mail/test/pop3testserver.py
chmod +x %{buildroot}%{python3_sitearch}/twisted/trial/test/scripttest.py

# ambiguous shebangs
pathfix.py -pn -i %{__python3} %{buildroot}%{python3_sitelib} %{buildroot}%{python3_sitearch}


%check
# can't get this to work within the buildroot yet due to multicast
# https://twistedmatrix.com/trac/ticket/7494
%if 0%{?with_python2}
PATH=%{buildroot}%{_bindir}:$PATH PYTHONPATH=%{buildroot}%{python2_sitearch} %{buildroot}%{_bindir}/trial-2 twisted ||:
%endif
PATH=%{buildroot}%{_bindir}:$PATH PYTHONPATH=%{buildroot}%{python3_sitearch} %{buildroot}%{_bindir}/trial twisted ||:


%if 0%{?with_python2}
%files -n python2-twisted
%doc CONTRIBUTING NEWS.rst README.rst
%license LICENSE
%{_bindir}/trial-2*
%{_bindir}/twistd-2*
%{python2_sitearch}/twisted
%{python2_sitearch}/Twisted-%{version}-py?.?.egg-info
%endif  # with_python2

%files -n python%{python3_pkgversion}-twisted
%doc CONTRIBUTING NEWS.rst README.rst html
%license LICENSE
%{_bindir}/trial-3*
%{_bindir}/twistd-3*
%{python3_sitearch}/twisted
%{python3_sitearch}/Twisted-%{version}-py?.?.egg-info
%{_bindir}/cftp
%{_bindir}/ckeygen
%{_bindir}/conch
%{_bindir}/mailmail
%{_bindir}/pyhtmlizer
%{_bindir}/tkconch
%{_bindir}/trial
%{_bindir}/twist
%{_bindir}/twistd
%{_mandir}/man1/cftp.1*
%{_mandir}/man1/ckeygen.1*
%{_mandir}/man1/conch.1*
%{_mandir}/man1/mailmail.1*
%{_mandir}/man1/pyhtmlizer.1*
%{_mandir}/man1/tkconch.1*
%{_mandir}/man1/trial.1*
%{_mandir}/man1/twistd.1*


%changelog
* Wed Jul 24 2019 Stephen Smoogen <smooge@fedoraproject.org> - 19.2.1-1.1
- Cut down python-cryptography to the version shipped in RHEL and see if that works.

* Mon Jun 24 2019 Troy Dawson <tdawson@redhat.com> - 1.0.2-9.1
- Make python2 optional
- Do not build python2 for RHEL8

* Sun Jun 09 2019 Robert-André Mauchin <zebob.m@gmail.com> - 19.2.1-1
- Release 19.2.1

* Wed May 22 2019 Robert-André Mauchin <zebob.m@gmail.com> - 19.2.0-3
- Add patch to import gobject from gi.repository for Python 3
- Fix #1712748

* Tue May 14 2019 Robert-André Mauchin <zebob.m@gmail.com> - 19.2.0-2
- Add patch regenerating raiser.c to use with Python 3.8a4
- Fix #11709817

* Wed Apr 10 2019 Robert-André Mauchin <zebob.m@gmail.com> - 19.2.0-1
- Release 19.2.0 (#1698490)

* Thu Mar 07 2019 Robert-André Mauchin <zebob.m@gmail.com> - 18.9.0-1
- Release 18.9.0
- Run tests

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 18.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 22 2018 Miro Hrončok <mhroncok@redhat.com> - 18.7.0-3
- Recommend pythonX-service-identity

* Sat Jul 21 2018 Robert-André Mauchin <zebob.m@gmail.com> - 18.7.0-2
- Remove erroneous symlink to binaries

* Sun Jul 15 2018 Robert-André Mauchin <zebob.m@gmail.com> - 18.7.0-1
- Update to 18.7.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 18.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Robert-André Mauchin <zebob.m@gmail.com> - 18.4.0-1
- Update to 18.4.0
- Default binaries to Python 3
- Drop old Obsoletes/Provides
- Refresh BR
- Remove useless macros
- Use python_enable_dependency_generator

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 16.4.1-11
- Rebuilt for Python 3.7

* Wed May 23 2018 Miro Hrončok <mhroncok@redhat.com> - 16.4.1-10
- Fix ambiguous shebangs

* Fri Apr 27 2018 Petr Viktorin <pviktori@redhat.com> - 16.4.1-9
- No longer require python-crypto

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 16.4.1-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 16.4.1-6
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 16.4.1-2
- rebuilt

* Wed Oct 26 2016 Jonathan Steffan <jsteffan@fedoraproject.org> - 16.4.1-1
- Update to 16.4.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 16.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 8 2016 Jonathan Steffan <jsteffan@fedoraproject.org> - 16.3.0-1
- Update to 16.3.0
- mahole, tap2deb, tap2rpm are removed upstream

* Sun Jun 26 2016 Jonathan Steffan <jsteffan@fedoraproject.org> - 16.2.0-2
- Add rpmlint notes
- Fix unneeded py3 conditional for py2 script chmod

* Sun Jun 26 2016 Jonathan Steffan <jsteffan@fedoraproject.org> - 16.2.0-1
- Update to 16.2.0
- Update upstream source location

* Thu Jun  2 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 16.1.1-3
- Drop tkinter dependency (only required for tkconch)
- Use python3 conditionals
- Move BR under the proper subpackage

* Tue May 10 2016 Petr Viktorin <pviktori@redhat.com> - 16.1.1-2
- Update to better conform to Python packaging guidelines

* Thu May 05 2016 Julien Enselme <jujens@jujens.eu> - 16.1.1-1
- Update to 16.1.1 (#1287381)

* Thu Mar 10 2016 Julien Enselme <jujens@jujens.eu> - 15.5.0-2
- Add python3 support

* Thu Mar 10 2016 Julien Enselme <jujens@jujens.eu> - 15.5.0-1
- Update to 15.5.0 (#1287381)
- Use new python macros
- Remove deprecated %%clean section

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Tom Prince <tom.prince@twistedmatrix.com> - 15.4.0-2
- Add arch-independent plugin directory to package. (RHBZ#1252140)

* Thu Oct 29 2015 Tom Prince <tom.prince@twistedmatrix.com> - 15.4.0-1
- Update to 15.4.0
- Include test certificates.

* Mon Jul 20 2015 Jonathan Steffan <jsteffan@fedoraproject.org> - 15.2.1-1
- Update to 15.2.1

* Sat May 09 2015 Jonathan Steffan <jsteffan@fedoraproject.org> - 15.1.0-1
- Update to 15.1.0 (RHBZ#1187921,RHBZ#1192707)
- Require python-service-identity (RHBZ#1119067)
- Obsolete python-twisted-core-doc (RHBZ#1187025)

* Sat Nov 22 2014 Jonathan Steffan <jsteffan@fedoraproject.org> - 14.0.2-1
- Update to 14.0.2 (RHBZ#1143002)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Jonathan Steffan <jsteffan@fedoraproject.org> - 14.0.0-1
- Update to 14.0.0
- Ship Twisted as a fully featured package without subpackages on the advice
  of upstream and to mirror what pypi provides
- Explictly build for python2 with new macros

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 03 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.2.0-1
- Updated to 12.2.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.1.0-1
- Updated to 12.1.0

* Sun Feb 12 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.0.0-1
- Updated to 12.0.0

* Sat Jan 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 11.1.0-2
- Rebuilt for gcc-4.7

* Fri Nov 18 2011 Julian Sikorski <belegdol@fedoraproject.org> - 11.1.0-1
- Updated to 11.1.0
- Dropped obsolete Group, Buildroot, %%clean and %%defattr

* Sat Apr 30 2011 Julian Sikorski <belegdol@fedoraproject.org> - 11.0.0-1
- Updated to 11.0.0
- Added comment on how to obtain the PKG-INFO file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 10.2.0-1
- Updated to 10.2.0

* Mon Nov 08 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-3
- Use python_sitelib instead of python-sitearch
- The aforementioned macros are defined in Fedora 13 and above

* Sun Nov 07 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-2
- Added egg-info file

* Tue Sep 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-1
- Updated to 10.1.0
- Switched to macros for versioned dependencies

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matthias Saou <http://freshrpms.net/> 8.2.0-1
- Update to 8.2.0.
- Change back spec cosmetic details from Paul's to Thomas' preference.

* Wed Jul 16 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-2
- Update to 8.1.0.
- Minor spec file cleanups.
- Merge back changes from Paul Howarth.

* Wed May 21 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.5.0-1
- update to 2.5.0 release (only the umbrella package was missing)

* Tue Jan 16 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-3
- list packages in README.fedora

* Wed Jan 03 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-2
- add a README.fedora
- made noarch, since it doesn't actually install any python twisted/ module
  code
- fixed provides/obsoletes

* Wed Jun 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-1
- this is now a pure umbrella package

* Mon Oct 10 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.1.0-1
- upstream release

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.1-1
- upstream release

* Mon Apr 04 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-2
- add zsh support

* Fri Mar 25 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-1
- final release

* Thu Mar 17 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.2.a3
- dropped web2

* Wed Mar 16 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.1.a3
- upstream release

* Sat Mar 12 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.1.a2
- new prerelease; FE versioning

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0a1-1
- prep for split

* Fri Aug 20 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.3.0-1
- new version

* Mon Apr 19 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.2.0-3
- vaultize

* Mon Apr 12 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.2.0-2
- require pyOpenSSL, SOAPpy, openssh-clients, crypto, dia so trial can run

