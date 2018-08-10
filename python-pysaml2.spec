%global srcname pysaml2

Name:           python-%{srcname}
Version:        4.5.0
Release:        4%{?dist}
Summary:        Python implementation of SAML Version 2
License:        Apache 2.0
URL:            https://github.com/IdentityPython/%{srcname}

%global gittag v%{version}

%if 0%{?fedora} < 32 || 0%{?rhel}
%global with_python2 1
%endif

%if 0%{?fedora} && ! 0%{?rhel}
%global with_python3 1
%endif

Source0: https://github.com/IdentityPython/%{srcname}/archive/%{gittag}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?with_python3}
BuildRequires:  python3-sphinx
%else
BuildRequires:  python2-sphinx
%endif

%description
PySAML2 is a pure python implementation of SAML2. It contains all
necessary pieces for building a SAML2 service provider or an identity
provider.  The distribution contains examples of both.  Originally
written to work in a WSGI environment there are extensions that allow
you to use it with other frameworks.


%if 0%{?with_python2}
%package -n python2-%{srcname}
Summary: Python implementation of SAML Version 2

%{?python_provide:%python_provide python2-%{srcname}}

Requires: python2-requests >= 1.0.0
Requires: python2-future
Requires: python2-cryptography
Requires: python2-pytz
Requires: python2-pyOpenSSL
Requires: python2-dateutil
Requires: python2-defusedxml
Requires: python2-six

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%description -n python2-%{srcname}
PySAML2 is a pure python implementation of SAML2. It contains all
necessary pieces for building a SAML2 service provider or an identity
provider.  The distribution contains examples of both.  Originally
written to work in a WSGI environment there are extensions that allow
you to use it with other frameworks.

%endif

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary: Python implementation of SAML Version 2

%{?python_provide:%python_provide python3-%{srcname}}

Requires: python3-requests >= 1.0.0
Requires: python3-future
Requires: python3-cryptography
Requires: python3-pytz
Requires: python3-pyOpenSSL
Requires: python3-dateutil
Requires: python3-defusedxml
Requires: python3-six

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{srcname}
PySAML2 is a pure python implementation of SAML2. It contains all
necessary pieces for building a SAML2 service provider or an identity
provider.  The distribution contains examples of both.  Originally
written to work in a WSGI environment there are extensions that allow
you to use it with other frameworks.

%endif

%package doc
Summary: Documentation for Python implementation of SAML Version 2

%description doc
Documentation for Python implementation of SAML Version 2.

%prep
%setup -qn %{srcname}-%{version}
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
%if 0%{?with_python2}
 %py2_build
%endif

%if 0%{?with_python3}
 %py3_build
%endif

# drop alabaster Sphinx theme, not packaged in Fedora yet
#sed -i '/alabaster/d' doc/conf.py
# generate html docs
%if 0%{?with_python3}
sphinx-build-3 doc html
%else
sphinx-build-2 doc html
%endif
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

%if 0%{?with_python2}
%py2_install
for bin in parse_xsd2 make_metadata mdexport merge_metadata; do
    mv %{buildroot}%{_bindir}/$bin.py %{buildroot}%{_bindir}/$bin-%{python2_version}.py
    ln -s ./$bin-%{python2_version}.py %{buildroot}%{_bindir}/$bin-2.py
    ln -s ./$bin-%{python2_version}.py %{buildroot}%{_bindir}/$bin.py             
done
%endif

%if 0%{?with_python2}
%files -n python2-%{srcname}
%doc README.rst
%license LICENSE.txt
%{_bindir}/parse_xsd2.py
%{_bindir}/parse_xsd2-2*.py
%{_bindir}/make_metadata.py
%{_bindir}/make_metadata-2*.py
%{_bindir}/mdexport.py
%{_bindir}/mdexport-2*.py
%{_bindir}/merge_metadata.py
%{_bindir}/merge_metadata-2*.py
%{python2_sitelib}/saml2
%{python2_sitelib}/*.egg-info
%endif

%if 0%{?with_python3}
%files -n python3-%{srcname}
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
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.5.0-3
- Rebuilt for Python 3.7

* Wed Jun  6 2018  <jdennis@redhat.com> - 4.5.0-2
- Resolves: rhbz#1582254 - re-enable python2 support

* Fri May 18 2018  <jdennis@redhat.com> - 4.5.0-1
- upgrade to current upstream
- enforce Python packaging standards

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.0.2-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

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
