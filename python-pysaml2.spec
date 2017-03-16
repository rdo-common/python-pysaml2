# Created by pyp2rpm-1.1.1
%global sname pysaml2

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-pysaml2
Version:        3.0.2
Release:        7%{?dist}
Summary:        Python implementation of SAML Version 2
License:        ASL 2.0
URL:            https://github.com/rohe/pysaml2
Source0:        https://pypi.python.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:      noarch

Patch0:         python-pysaml2-3.0.2-CVE-2016-10149.patch

%description
PySAML2 implementation of SAML Version 2 to be used in a WSGI environment.


%package -n python2-%{sname}
Summary:        Python implementation of SAML Version 2

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
BuildRequires:  python-defusedxml

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
Requires:       python-defusedxml


%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
PySAML2 implementation of SAML Version 2 to be used in a WSGI environment.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        Python implementation of SAML Version 2

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
#mongodict - not in Fedora
BuildRequires:  python3-pyasn1
#pymongo==3.0.1 - 2.5.2 in Fedora
BuildRequires:  python3-pymongo
BuildRequires:  python3-memcached >= 1.51
BuildRequires:  python3-pytest
BuildRequires:  python3-mako
BuildRequires:  python3-webob

BuildRequires:  python3-decorator
BuildRequires:  python3-requests >= 1.0.0
BuildRequires:  python3-paste
BuildRequires:  python3-zope-interface
BuildRequires:  python3-repoze-who
BuildRequires:  python3-crypto >= 2.5
BuildRequires:  python3-pytz
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-dateutil
BuildRequires:  python3-six
BuildRequires:  python3-defusedxml

Requires:       python3-decorator
Requires:       python3-requests >= 1.0.0
Requires:       python3-paste
Requires:       python3-zope-interface
Requires:       python3-repoze-who
Requires:       python3-crypto >= 2.5
Requires:       python3-pytz
Requires:       python3-pyOpenSSL
Requires:       python3-dateutil
Requires:       python3-six
Requires:       python3-defusedxml


%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
PySAML2 implementation of SAML Version 2 to be used in a WSGI environment.
%endif

%package doc
Summary:        Documentation for Python implementation of SAML Version 2

BuildRequires:  python-sphinx

%description doc
Documentation for Python implementation of SAML Version 2.


%prep
%setup -qn %{sname}-%{version}
sed -i '/argparse/d' setup.py
%patch0 -p1

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
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

# drop alabaster Sphinx theme, not packaged in Fedora yet
sed -i '/alabaster/d' doc/conf.py
# generate html docs
sphinx-build doc html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
for bin in parse_xsd2 make_metadata mdexport merge_metadata; do
    mv %{buildroot}%{_bindir}/$bin.py %{buildroot}%{_bindir}/$bin-%{python3_version}.py
    ln -s ./$bin-%{python3_version}.py %{buildroot}%{_bindir}/$bin-3.py
done
%endif

%py2_install
for bin in parse_xsd2 make_metadata mdexport merge_metadata; do
    mv %{buildroot}%{_bindir}/$bin.py %{buildroot}%{_bindir}/$bin-%{python2_version}.py
    ln -s ./$bin-%{python2_version}.py %{buildroot}%{_bindir}/$bin-2.py
    ln -s ./$bin-%{python2_version}.py %{buildroot}%{_bindir}/$bin.py             
done


# some testdeps are missing in Fedora
#%check
#%{__python2} setup.py test

%files -n python2-%{sname}
%doc README.rst
%license LICENSE.txt
%{_bindir}/parse_xsd2.py
%{_bindir}/make_metadata.py
%{_bindir}/mdexport.py
%{_bindir}/merge_metadata.py
%{_bindir}/parse_xsd2-2*.py
%{_bindir}/make_metadata-2*.py
%{_bindir}/mdexport-2*.py
%{_bindir}/merge_metadata-2*.py
%{python2_sitelib}/saml2
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc README.rst
%license LICENSE.txt
%{_bindir}/parse_xsd2-3*.py
%{_bindir}/make_metadata-3*.py
%{_bindir}/mdexport-3*.py
%{_bindir}/merge_metadata-3*.py
%{python3_sitelib}/saml2
%{python3_sitelib}/*.egg-info
%endif


%files doc
%license LICENSE.txt
%doc html

%changelog
* Thu Mar 16 2017 Jason Joyce <jjoyce@redhat.com> - 3.0.2-7
- security fix for entity expansion issue - CVE-2016-10149

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-5
- Rebuild for Python 3.6

* Sun Nov 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.2-4
- fix pycrypto dependency

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

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
