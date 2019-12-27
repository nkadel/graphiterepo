# what it's called on pypi
%global pypi_name Automat
# what it's imported as
%global libname automat

%global common_description %{expand:
Automat is a library for concise, idiomatic Python expression of finite-state
automata (particularly deterministic finite-state transducers).}

%bcond_with  tests
%bcond_without  python2

Name:           python-%{pypi_name}
Version:        0.7.0
Release:        3.1%{?dist}
Summary:        Self-service finite-state machines for the programmer on the go

License:        MIT
URL:            https://github.com/glyph/automat
Source0:        %pypi_source
# PEP 570 adds "positional only" arguments to Python, which changes the
# code object constructor. This adds support for Python 3.8.
# https://github.com/glyph/automat/pull/111
Patch0:         0001-Add-support-for-positional-only-arguments.patch

BuildArch:      noarch
%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

%{?python_enable_dependency_generator}

%description %{common_description}


%if %{with python2}
%package -n     python2-%{pypi_name}
Summary:        %{summary}
Provides:       python2-%{libname}
%{?python_provide:%python_provide python2-%{pypi_name}}
# Added for misnamed packages
%{?python_provide:%python_provide python2-%{libname}}

BuildRequires:  python2-devel
BuildRequires:  python2-m2r
BuildRequires:  python2-setuptools
#BuildRequires:  python2-setuptools-scm
BuildRequires:  python2-setuptools_scm
%if %{with tests}
BuildRequires:  python2-pytest
BuildRequires:  python2-attrs >= 16.1
BuildRequires:  python2-graphviz > 0.5.1
BuildRequires:  python2-six
BuildRequires:  python2-twisted >= 16.1.1
%endif

%description -n python2-%{pypi_name} %{common_description}
%endif


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
Provides:       python%{python3_pkgversion}-%{libname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
# Added for misnamed packages
%{?python_provide:%python_provide python%{python3_pkgversion}-%{libname}}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-m2r
BuildRequires:  python%{python3_pkgversion}-setuptools
#BuildRequires:  python%{python3_pkgversion}-setuptools-scm
BuildRequires:  python%{python3_pkgversion}-setuptools_scm
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-attrs >= 16.1
BuildRequires:  python%{python3_pkgversion}-graphviz > 0.5.1
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-twisted >= 16.1.1
%endif

%description -n python%{python3_pkgversion}-%{pypi_name} %{common_description}


%prep
%autosetup  -p1 -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%if %{with python2}
%py2_build
%endif
%py3_build


%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%if %{with python2}
%py2_install
rm -rf %{buildroot}%{_bindir}/*
%endif
%py3_install


%check
%if %{with tests}
%if %{with python2}
PYTHONPATH=%{buildroot}%{python2_sitelib} pytest-%{python2_version} --verbose automat/_test
%endif
PYTHONPATH=%{buildroot}%{python3_sitelib} pytest-%{python3_version} --verbose automat/_test
%endif


%if %{with python2}
%files -n python2-%{pypi_name}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{libname}
%{python2_sitelib}/%{pypi_name}-%{version}-py%{python2_version}.egg-info
%endif


%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/automat-visualize
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info


%changelog
* Wed Dec 25 2019 Nico Kadel-Garcia <nkadel@gmail.com>
- Reset python-setuptools-scm to python-setuptools_scm dependency

* Mon Jul 22 2019 Stephen Smoogen <smooge@fedora00.int.smoogespace.com> - 0.7.0-3.1
- Bootstrap version

* Mon May 27 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0-3
- Add patch supporting for positional only arguments for Python 3.8

* Sat Apr 06 2019 Carl George <carl@george.computer> - 0.7.0-2
- Add provides for lowercase name
- Run tests with pytest like upstream does

* Mon Mar 11 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0-1
- Release 0.7.0 (#1687495)

* Fri Mar 08 2019 Jeroen van Meeuwen <vanmeeuwen+fedora@kolabsys.com> - 0.6.0-5
 - Add bcond_without tests

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-2
- Rebuilt for Python 3.7

* Fri Apr 13 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.0-1
- Initial package.
