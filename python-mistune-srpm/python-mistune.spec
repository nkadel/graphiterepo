%global upname mistune
%global with_python3 1

%global common_description %{expand:
The fastest markdown parser in pure Python, inspired by marked.}

Name:           python-mistune
Version:        0.8.3
Release:        6%{?dist}
Summary:        Markdown parser for Python 

License:        BSD
URL:            https://github.com/lepture/mistune
Source0:        https://github.com/lepture/mistune/archive/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  python2-Cython
BuildRequires:  python2-devel
BuildRequires:  python2-nose
BuildRequires:  python2-setuptools
%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-Cython
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif


%description %{common_description}

%package -n python2-%{upname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{upname}}

%description -n python2-%{upname} %{common_description}

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{upname}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{upname} %{common_description}
%endif

%prep
%setup -q -n %{upname}-%{version}
# Moved to source archive from github, doesn't contain egg-info
#rm -rf mistune.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%py3_build
popd
%endif # with_python3


%install
%if 0%{?with_python3}
pushd %{py3dir}
%py3_install
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}
%{_fixperms} %{buildroot}/*


%check
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

%{__python2} setup.py test

%files -n python2-%{upname}
%doc LICENSE README.rst
# For arch-specific packages: sitearch
%{python2_sitearch}/%{upname}.*
%{python2_sitearch}/%{upname}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{upname}
%doc LICENSE README.rst
%{python3_sitearch}/%{upname}.*
%{python3_sitearch}/%{upname}-%{version}-py?.?.egg-info
%{python3_sitearch}/__pycache__/%{upname}*
%endif # with_python3

%changelog
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.8.3-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Dec 19 2017 Christian Dersch <lupinix@fedoraproject.org> - 0.8.3-1
- new version (0.8.3)
- fixes CVE-2017-15612 and CVE-2017-16876

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.3-7
- Python 2 binary package renamed to python2-mistune
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.3-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 04 2016 Christian Dersch <lupinix@mailbox.org> - 0.7.3-1
- new version

* Sat Feb 27 2016 Christian Dersch <lupinix@mailbox.org> - 0.7.2-1
- new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Sep 23 2015 Christian Dersch <lupinix@fedoraproject.org> - 0.7.1-1
- new version

* Wed Jun 17 2015 Christian Dersch <lupinix@fedoraproject.org> - 0.6-1
- new upstream release

* Mon Apr 20 2015 Christian Dersch <lupinix@fedoraproject.org> - 0.5.1-1
- new upstream release (0.5.1)

* Fri Dec  5 2014 Christian Dersch <lupinix@fedoraproject.org> - 0.5-1
- new upstream release
- enabled tests

* Thu Dec  4 2014 Christian Dersch <lupinix@fedoraproject.org> - 0.4.1-2
- spec fixes

* Thu Dec  4 2014 Christian Dersch <lupinix@fedoraproject.org> - 0.4.1-1
- initial spec  
