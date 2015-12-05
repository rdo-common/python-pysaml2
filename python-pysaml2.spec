# Created by pyp2rpm-1.1.1
%global pypi_name pysaml2

Name:           python-pysaml2
Version:        3.0.2
Release:        1%{?dist}
Summary:        Python implementation of SAML Version 2
License:        ASL 2.0
URL:            https://github.com/rohe/pysaml2
Source0:        https://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
#mongodict - not in Fedora
BuildRequires:  python-pyasn1
#pymongo==3.0.1 - 2.5.2 in Fedora
BuildRequires:  python-pymongo
BuildRequires:  python-memcached >= 1.51
BuildRequires:  pytest
BuildRequires:  python-mako
BuildRequires:  python-webob

BuildRequires:  python-decorator
BuildRequires:  python-requests >= 1.0.0
BuildRequires:  python-paste
BuildRequires:  python-zope-interface
BuildRequires:  python-repoze-who
BuildRequires:  pycrypto >= 2.5
BuildRequires:  pytz
BuildRequires:  pyOpenSSL
BuildRequires:  python-dateutil
BuildRequires:  python-six

Requires:       python-decorator
Requires:       python-requests >= 1.0.0
Requires:       python-paste
Requires:       python-zope-interface
Requires:       python-repoze-who
Requires:       pycrypto >= 2.5
Requires:       pytz
Requires:       pyOpenSSL
Requires:       python-dateutil
Requires:       python-six

%description
PySAML2 implementation of SAML Version 2 to be used in a WSGI environment.

%package doc
Summary:        Documentation for Python implementation of SAML Version 2

BuildRequires:  python-sphinx

%description doc
Documentation for Python implementation of SAML Version 2.


%prep
%setup -qn %{pypi_name}-%{version}
sed -i '/argparse/d' setup.py

# Avoid non-executable-script rpmlint while maintaining timestamps
find src -name \*.py |
while read source; do
  if head -n1 "$source" | grep -F '/usr/bin/env'; then
    touch --ref="$source" "$source".ts
    sed -i '/\/usr\/bin\/env python/{d;q}' "$source"
    touch --ref="$source".ts "$source"
    rm "$source".ts
  fi
done
# special case for parse_xsd generated file which have lines like:
#!!!! 'NoneType' object has no attribute 'py_class'
source="src/saml2/schema/wsdl.py"
touch --ref="$source" "$source".ts
sed -i '1,3{d;q}' "$source"
touch --ref="$source".ts "$source"
rm "$source".ts

%build
%{__python2} setup.py build

# drop alabaster Sphinx theme, not packaged in Fedora yet
sed -i '/alabaster/d' doc/conf.py
# generate html docs
sphinx-build doc html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# some testdeps are missing in Fedora
#%check
#%{__python2} setup.py test

%files
%doc README.rst
%license LICENSE.txt
%{_bindir}/parse_xsd2.py
%{_bindir}/make_metadata.py
%{_bindir}/mdexport.py
%{_bindir}/merge_metadata.py
%{python2_sitelib}/saml2
%{python2_sitelib}/*.egg-info

%files doc
%license LICENSE.txt
%doc html

%changelog
* Sat Dec 05 2015 Alan Pevec <alan.pevec@redhat.com> 3.0.2-1
- Update to 3.0.2

* Wed Jul 15 2015 Alan Pevec <apevec@redhat.com> - 3.0.0-1
- update to upstream release 3.0.0

* Thu Jun 18 2015 Alan Pevec <apevec@redhat.com> - 3.0.0-0.3.git40603ae
- include unreleased fix for https://github.com/rohe/pysaml2/issues/202
- review feedback
- fix rpmlint errors

* Tue Mar 31 2015 Alan Pevec <apevec@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Mon Feb 16 2015 Dan Prince - 2.3.0-1
- Initial package.
