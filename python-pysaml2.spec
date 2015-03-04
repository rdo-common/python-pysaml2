# Created by pyp2rpm-1.1.1
%global pypi_name pysaml2

Name:           python-pysaml2
Version:        2.3.0
Release:        1%{?dist}
Summary:        Python implementation of SAML Version 2 to be used in a WSGI environment

License:        Apache 2.0
URL:            https://github.com/rohe/pysaml2
Source0:        https://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-devel
BuildRequires:  python-pyasn1
BuildRequires:  pymongo
BuildRequires:  python-memcached
BuildRequires:  pytest
BuildRequires:  python-mako
 
Requires:       python-decorator
Requires:       python-requests >= 1.0.0
Requires:       python-paste
Requires:       python-zope-interface
Requires:       python-repoze-who
Requires:       pycrypto >= 2.2
Requires:       pytz
Requires:       pyOpenSSL
Requires:       python-dateutil
Requires:       python-argparse

%description
README for PySAML2 n implementation of SAML Version 2 to be used in a WSGI environment.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%doc
%{_bindir}/parse_xsd2.py
%{_bindir}/make_metadata.py
%{_bindir}/mdexport.py
%{_bindir}/merge_metadata.py
%{python2_sitelib}/saml2/schema
%{python2_sitelib}/saml2/authn_context
%{python2_sitelib}/xmlenc
%{python2_sitelib}/saml2/attributemaps
%{python2_sitelib}/saml2/extension
%{python2_sitelib}/saml2/entity_category
%{python2_sitelib}/saml2/userinfo
%{python2_sitelib}/saml2/profile
%{python2_sitelib}/xmldsig
%{python2_sitelib}/saml2
%{python2_sitelib}/s2repoze
%{python2_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info

%changelog
* Mon Feb 16 2015 Dan Prince - 2.3.0-1
- Initial package.
