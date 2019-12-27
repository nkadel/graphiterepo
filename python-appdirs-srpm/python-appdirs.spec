%global pypi_name appdirs
%bcond_without wheel
%global wheelname %{pypi_name}-%{version}-py2.py3-none-any.whl

Name:          python-%{pypi_name}
Version:       1.4.3
#Release:       8%%{?dist}
Release:       0%{?dist}
Summary:       Python module for determining platform-specific directories

License:       MIT
URL:           https://github.com/ActiveState/appdirs
Source0:       %{pypi_source}

BuildArch:     noarch
%if 0%{?rhel}
BuildRequires: epel-rpm-macros
%endif

%description
A small Python module for determining appropriate " + " platform-specific
directories, e.g. a "user data dir".

%package -n python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with wheel}
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
%endif

%description -n python2-%{pypi_name}
A small Python 2 module for determining appropriate " + " platform-specific
directories, e.g. a "user data dir".

%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with wheel}
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif

%description -n python%{python3_pkgversion}-%{pypi_name}
A small Python 3 module for determining appropriate " + " platform-specific
directories, e.g. a "user data dir".

%prep
%autosetup -n %{pypi_name}-%{version}
rm -vrf %{pypi_name}.egg-info

%build
%if %{with wheel}
  %py2_build_wheel
  %py3_build_wheel
%else
  %py2_build
  %py3_build
%endif

%install
%if %{with wheel}
  %py2_install_wheel %{wheelname}
  %py3_install_wheel %{wheelname}
%else
  %py2_install
  %py3_install
%endif

sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}{%{python2_sitelib},%{python3_sitelib}}/%{pypi_name}.py

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{pypi_name}
%license LICENSE.txt
%doc README.rst CHANGES.rst
%{python2_sitelib}/%{pypi_name}*

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE.txt
%doc README.rst CHANGES.rst
%{python3_sitelib}/%{pypi_name}*
%{python3_sitelib}/__pycache__/%{pypi_name}.*

%changelog
* Wed Dec 25 2019 Nico Kadel-Garcia <nkadel@gmail.com>
- Backport to RHEL 7

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.3-7
- Get python2 package back

* Sun Aug 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.3-6
- Drop python2 subpackage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.3-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.4.3-1
- Update to 1.4.3

* Mon Feb 13 2017 Charalampos Stratakis <cstratak@redhat.com> - 1.4.0-10
- Rebuild as wheel

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Aug 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.4.0-4
- Update to new packaging guidelines

* Sun Aug 02 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.4.0-3
- Use modern python rpm macros

* Mon Jul 27 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.4.0-2
- Include CHANGES.rst in doc
- use python2-devel in BR instead of python-devel
- run tests

* Fri May 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.4.0-1
- Initial package
