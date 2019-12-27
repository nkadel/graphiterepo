%global pkgname m2r
%global desc M2R converts a markdown file including reST markups to a valid reST format.

Name:           python-%{pkgname}
Version:        0.2.0
#Release:        2%%{?dist}
Release:        0%{?dist}
Summary:        Markdown to reStructuredText converter

License:        MIT
URL:            https://github.com/miyakogi/%{pkgname}
Source0:        https://github.com/miyakogi/%{pkgname}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?rhel}
Buildrequires:  epel-rpm-macros
%endif

%description
%{desc}


%package -n python2-%{pkgname}
BuildRequires:  python2-devel
BuildRequires:  python2-docutils
BuildRequires:  python2-mistune
BuildRequires:  python2-pygments
BuildRequires:  python2-mock
Requires:       python2-docutils
Requires:       python2-mistune
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkgname}}


%description -n python2-%{pkgname}
%{desc}


%package -n python%{python3_pkgversion}-%{pkgname}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-docutils
BuildRequires:  python%{python3_pkgversion}-mistune
BuildRequires:  python%{python3_pkgversion}-pygments
BuildRequires:  python%{python3_pkgversion}-mock
Requires:       python%{python3_pkgversion}-docutils
Requires:       python%{python3_pkgversion}-mistune
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}


%description -n python%{python3_pkgversion}-%{pkgname}
%{desc}


%prep
%setup -qn %{pkgname}-%{version}

# Remove upstream's egg-info
rm -rf %{pkgname}.egg-info

# Remove shebang
sed -i '1{\@^#!/usr/bin/env python@d}' m2r.py


%build
%py2_build
%py3_build


%install
%py3_install
%py2_install


%check
PYTHONPATH=$(pwd) %{__python2} setup.py test -s tests || :
PYTHONPATH=$(pwd) %{__python3} setup.py test -s tests || :


%files -n python2-%{pkgname}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{pkgname}.py
%{python2_sitelib}/%{pkgname}.pyc
%{python2_sitelib}/%{pkgname}.pyo
%{python2_sitelib}/%{pkgname}-%{version}*-py%{python2_version}.egg-info
#%exclude %{python2_sitelib}/tests


%files -n python%{python3_pkgversion}-%{pkgname}
%license LICENSE
%doc README.md
%{_bindir}/m2r
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pkgname}.py
%{python3_sitelib}/%{pkgname}-%{version}*-py%{python3_version}.egg-info
#%exclude %{python3_sitelib}/tests


%changelog
* Wed Dec 25 2019 Nico Kadel-Garcia <nkadel@gmail.com>
- Backport to RHEL 7

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 15 2018 Nikola Forró <nforro@redhat.com> - 0.2.0-1
- Update to 0.2.0
  resolves: #1615361

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Nikola Forró <nforro@redhat.com> - 0.1.15-1
- Update to 0.1.15
  resolves: #1597056

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.1.14-2
- Rebuilt for Python 3.7

* Thu Mar 22 2018 Nikola Forró <nforro@redhat.com> - 0.1.14-1
- Update to 0.1.14
  resolves: #1559372

* Wed Feb 14 2018 Nikola Forró <nforro@redhat.com> - 0.1.13-1
- Update to 0.1.13
  resolves: #1545220

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 06 2017 Nikola Forró <nforro@redhat.com> - 0.1.12-2
- Use more descriptive source tarball name
- Fix python2 dependency names

* Wed Sep 13 2017 Nikola Forró <nforro@redhat.com> - 0.1.12-1
- Update to 0.1.12
  resolves: #1490365

* Wed Aug 30 2017 Nikola Forró <nforro@redhat.com> - 0.1.11-1
- Update to 0.1.11
  resolves: #1486504

* Fri Aug 25 2017 Nikola Forró <nforro@redhat.com> - 0.1.10-2
- Add missing dist tag

* Tue Aug 15 2017 Nikola Forró <nforro@redhat.com> - 0.1.10-1
- Update to 0.1.10
- Switch to release versioning
  resolves: #1480575

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-2.git8e4ce37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Nikola Forró <nforro@redhat.com> - 0.1.7-1.git8e4ce37
- Update to 0.1.7
  resolves: #1473289

* Wed May 31 2017 Nikola Forró <nforro@redhat.com> - 0.1.6-1.git871d579
- Update to 0.1.6
  resolves: #1457165

* Wed May 17 2017 Nikola Forró <nforro@redhat.com> - 0.1.5-2.git539a079
- Make image_link regex non-greedy

* Tue May 16 2017 Nikola Forró <nforro@redhat.com> - 0.1.5-1.git539a079
- Initial package
