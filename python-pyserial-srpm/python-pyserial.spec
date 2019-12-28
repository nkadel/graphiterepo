#
# spec file for package python-pyserial
#
# Copyright (c) 2019 Nico Kadel-Garcia.
#

# python3_pkgversion macro for EPEL in older RHEL
%{!?python3_pkgversion:%global python3_pkgversion 3}

# Fedora and RHEL split python2 and python3
# RHEL 6 requires python34 from EPEL
%global with_python3 1

# Fedora >= 30 no longer publishes python2 by default
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
%global with_python2 0
%else
%global with_python2 1
%endif

%global pypi_name pyserial

# Common SRPM package
Name:           python-%{pypi_name}
Version:        3.4
Release:        0%{?dist}
Url:            https://github.com/pyserial/pyserial
Summary:        Python Serial Port Extension
License:        BSD
Group:          Development/Languages/Python
# Stop using py2pack macros, use local macros published by Fedora
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
Python Serial Port Extension for Win32, OSX, Linux, BSD, Jython, IronPython

%if %{with_python2}
%package -n python2-%{pypi_name}
Version:        3.4
Release:        0%{?dist}
Url:            https://github.com/pyserial/pyserial
Summary:        Python Serial Port Extension
License:        BSD

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%{?python_provide:%python_provide python2-%{pypi_name}}
%if ! %{with_python3}
# Old misnamed python2 package
Obsoletes:      pyserial <= %{version}
Provides:       pyserial = %{version}
%endif # ! with_python3

%description -n python2-%{pypi_name}
Python Serial Port Extension for Win32, OSX, Linux, BSD, Jython, IronPython

%endif # with_python2

%if %{with_python3}
%package -n python3-%{pypi_name}
Version:        3.4
Release:        0%{?dist}
Url:            https://github.com/pyserial/pyserial
Summary:        Python Serial Port Extension
License:        BSD

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# Old misnamed python2 package
Obsoletes:      pyserial <= %{version}
Provides:       pyserial = %{version}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Python Serial Port Extension for Win32, OSX, Linux, BSD, Jython, IronPython

%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with_python2}
%py2_build
%endif # with_python2

%if %{with_python3}
%py3_build
%endif # with_python3

%install
%if %{with_python2}
%py2_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/miniterm.py $RPM_BUILD_ROOT%{_bindir}/miniterm.py-%{python2_version}
%if ! %{with_python3}
%{__ln_s} miniterm.py-%{python2_version} $RPM_BUILD_ROOT%{_bindir}/miniterm.py
%endif # !with_python3
%endif # with_python2

%if %{with_python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/miniterm.py $RPM_BUILD_ROOT%{_bindir}/miniterm.py-%{python3_version}
%{__ln_s} miniterm.py-%{python3_version} $RPM_BUILD_ROOT%{_bindir}/miniterm.py
%endif # with_python3

%clean
rm -rf %{buildroot}

%if %{with_python2}
%files -n python2-%{pypi_name}
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{_bindir}/miniterm.py-%{python2_version}
%if ! %{with_python3}
%{_bindir}/miniterm.py
%endif # ! with_python3
%endif # with_python2

%if %{with_python3}
%files -n python3-%{pypi_name}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/miniterm.py-%{python3_version}
%{_bindir}/miniterm.py
%endif # with_python3

%changelog
