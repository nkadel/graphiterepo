#
# spec file for package python-graphite-web
#
# Copyright (c) 2019 Nico Kadel-Garcia.
#

# Fedora and RHEL split python2 and python3
# Older RHEL requires EPEL and python34 or python36
%global with_python3 1

# Fedora >= 38 no longer publishes python2 by default
%if 0%{?fedora} >= 30
%global with_python2 0
%else
%global with_python2 1
%endif

# Older RHEL does not use dnf, does not support "Suggests"
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_dnf 1
%else
%global with_dnf 0
%endif

%global pypi_name graphite-web

# Common SRPM package
Name:           python-%{pypi_name}
Version:        1.1.6
Release:        0%{?dist}
Url:            http://graphiteapp.org/
Summary:        Enterprise scalable realtime graphing
License:        Apache Software License 2.0 (FIXME:No SPDX)
Group:          Development/Languages/Python
# Stop using py2pack macros, use local macros published by Fedora
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
%if (0%{?rhel} > 0 && 0%{?rhel} <= 7)
# Addresses python36- versus python3- dependencies
BuildRequires: epel-rpm-macros
%endif

%description
# Graphite-Web

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5e94ef79c2ea441aaf209cfb2851849e)](https://www.codacy.com/app/graphite-project/graphite-web?utm_source=github.com&utm_medium=referral&utm_content=graphite-project/graphite-web&utm_campaign=badger)
[![Build Status](https://travis-ci.org/graphite-project/graphite-web.png?branch=master)](https://travis-ci.org/graphite-project/graphite-web)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bhttps%3A%2F%2Fgithub.com%2Fgraphite-project%2Fgraphite-web.svg?type=shield)](https://app.fossa.io/projects/git%2Bhttps%3A%2F%2Fgithub.com%2Fgraphite-project%2Fgraphite-web?ref=badge_shield)
[![codecov](https://codecov.io/gh/graphite-project/graphite-web/branch/master/graph/badge.svg)](https://codecov.io/gh/graphite-project/graphite-web)

## Overview

Graphite consists of three major components:

1. Graphite-Web, a Django-based web application that renders graphs and dashboards
2. The [Carbon](https://github.com/graphite-project/carbon) metric processing daemons
3. The [Whisper](https://github.com/graphite-project/whisper) time-series database library

![Graphite Components](https://github.com/graphite-project/graphite-web/raw/master/webapp/content/img/overview.png "Graphite Components")

## Installation, Configuration and Usage

Please refer to the instructions at [readthedocs](http://graphite.readthedocs.io/).

## License

Graphite-Web is licensed under version 2.0 of the Apache License. See the [LICENSE](https://github.com/graphite-project/graphite-web/blob/master/LICENSE) file for details.

%if %{with_python2}
%package -n python2-%{pypi_name}
Version:        1.1.6
Release:        0%{?dist}
Url:            http://graphiteapp.org/
Summary:        Enterprise scalable realtime graphing
License:        Apache Software License 2.0 (FIXME:No SPDX)

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# requires stanza of py2pack
# install_requires stanza of py2pack
%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
# Graphite-Web

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5e94ef79c2ea441aaf209cfb2851849e)](https://www.codacy.com/app/graphite-project/graphite-web?utm_source=github.com&utm_medium=referral&utm_content=graphite-project/graphite-web&utm_campaign=badger)
[![Build Status](https://travis-ci.org/graphite-project/graphite-web.png?branch=master)](https://travis-ci.org/graphite-project/graphite-web)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bhttps%3A%2F%2Fgithub.com%2Fgraphite-project%2Fgraphite-web.svg?type=shield)](https://app.fossa.io/projects/git%2Bhttps%3A%2F%2Fgithub.com%2Fgraphite-project%2Fgraphite-web?ref=badge_shield)
[![codecov](https://codecov.io/gh/graphite-project/graphite-web/branch/master/graph/badge.svg)](https://codecov.io/gh/graphite-project/graphite-web)

## Overview

Graphite consists of three major components:

1. Graphite-Web, a Django-based web application that renders graphs and dashboards
2. The [Carbon](https://github.com/graphite-project/carbon) metric processing daemons
3. The [Whisper](https://github.com/graphite-project/whisper) time-series database library

![Graphite Components](https://github.com/graphite-project/graphite-web/raw/master/webapp/content/img/overview.png "Graphite Components")

## Installation, Configuration and Usage

Please refer to the instructions at [readthedocs](http://graphite.readthedocs.io/).

## License

Graphite-Web is licensed under version 2.0 of the Apache License. See the [LICENSE](https://github.com/graphite-project/graphite-web/blob/master/LICENSE) file for details.

%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Version:        1.1.6
Release:        0%{?dist}
Url:            http://graphiteapp.org/
Summary:        Enterprise scalable realtime graphing
License:        Apache Software License 2.0 (FIXME:No SPDX)

# requires stanza of py2pack
# install_requires stanza of py2pack
%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
# Graphite-Web

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5e94ef79c2ea441aaf209cfb2851849e)](https://www.codacy.com/app/graphite-project/graphite-web?utm_source=github.com&utm_medium=referral&utm_content=graphite-project/graphite-web&utm_campaign=badger)
[![Build Status](https://travis-ci.org/graphite-project/graphite-web.png?branch=master)](https://travis-ci.org/graphite-project/graphite-web)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bhttps%3A%2F%2Fgithub.com%2Fgraphite-project%2Fgraphite-web.svg?type=shield)](https://app.fossa.io/projects/git%2Bhttps%3A%2F%2Fgithub.com%2Fgraphite-project%2Fgraphite-web?ref=badge_shield)
[![codecov](https://codecov.io/gh/graphite-project/graphite-web/branch/master/graph/badge.svg)](https://codecov.io/gh/graphite-project/graphite-web)

## Overview

Graphite consists of three major components:

1. Graphite-Web, a Django-based web application that renders graphs and dashboards
2. The [Carbon](https://github.com/graphite-project/carbon) metric processing daemons
3. The [Whisper](https://github.com/graphite-project/whisper) time-series database library

![Graphite Components](https://github.com/graphite-project/graphite-web/raw/master/webapp/content/img/overview.png "Graphite Components")

## Installation, Configuration and Usage

Please refer to the instructions at [readthedocs](http://graphite.readthedocs.io/).

## License

Graphite-Web is licensed under version 2.0 of the Apache License. See the [LICENSE](https://github.com/graphite-project/graphite-web/blob/master/LICENSE) file for details.

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
%endif # with_python2

%if %{with_python3}
%py3_install
%endif # with_python3

%clean
rm -rf %{buildroot}

%if %{with_python2}
%files -n python2-%{pypi_name}
%defattr(-,root,root,-)
%{python2_sitelib}/*
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%endif # with_python3

%changelog