# See WARNING notes in %%description
# Disable automatic dependency processing - creates endless loop if php-composer is already installed on buildsys
AutoReqProv: no

%global github_owner       composer
%global github_name        composer
%global github_version     1.0.0
%global github_commit      0c8158f47d7dda89226d4e816fee1fb9ac6c1204
%global github_date        20121023

#%%global github_release %%{github_date}git%%(c=%%{github_commit}; echo ${c:0:7})
%global github_release     alpha6

%global php_min_ver        5.3.2

%global jsonlint_min_ver   1.0.0
%global jsonlint_max_ver   2.0.0

%global jsonschema_min_ver 1.1.0
# DEBUG
#%global jsonschema_max_ver 1.2.0
%global jsonschema_max_ver 2.0

%global symfony_min_ver    2.1.0
%global symfony_max_ver    3.0.0

%global composer           %{_datadir}/composer
%global composer_vendor    composer
%global composer_project   composer

Name:          php-composer
Version:       %{github_version}
Release:       0.1.%{github_release}%{?dist}
Summary:       Dependency Manager for PHP

Group:         Development/Libraries
License:       MIT
URL:           http://getcomposer.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz
# RPM "magic"
Source1:       macros.composer
Source2:       composer.attr
Source3:       composer.prov
Source4:       composer.req

BuildArch:     noarch

BuildRequires:  php-phpunit-PHPUnit

Requires:      php-common >= %{php_min_ver}
Requires:      php-jsonlint >= %{jsonlint_min_ver}
Requires:      php-jsonlint <  %{jsonlint_max_ver}
Requires:      php-JsonSchema >= %{jsonschema_min_ver}
Requires:      php-JsonSchema <  %{jsonschema_max_ver}
Requires:      php-pear(pear.symfony.com/Console) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/Console) <  %{symfony_max_ver}
Requires:      php-pear(pear.symfony.com/Finder) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/Finder) <  %{symfony_max_ver}
Requires:      php-pear(pear.symfony.com/Process) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/Process) <  %{symfony_max_ver}
# phpci
Requires:      php-curl
Requires:      php-date
Requires:      php-hash
Requires:      php-iconv
Requires:      php-json
Requires:      php-libxml
Requires:      php-mbstring
Requires:      php-openssl
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-tokenizer
Requires:      php-xsl
Requires:      php-zip
Requires:      php-zlib
%if 0%{?fedora}
Requires:      php-filter
Requires:      php-phar
%endif

# Common package naming (php-composervendor-composerproject)
Provides:      php-composer-composer = %{version}-%{release}
# Virtual provide
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Composer is a tool for dependency management in PHP. It allows you to declare
the dependent libraries your project needs and it will install them in your
project for you.

WARNING: This is just a development RPM.  Please submit issues at
         https://github.com/siwinski/php-composer-rpms/issues and prefix
         your issue title with "[%name] ".


%prep
%setup -q -c

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .

# FIXME need phar to create vendor dir
cd %{github_name}-%{github_commit}
curl -sS https://getcomposer.org/installer | php
# fetches dependencies - probably we want to unbundle these
php composer.phar install
# -----------

%build
# Empty build section, nothing to build

# FIXME
# this overwrites the downloaded composer.phar from the previous step - do we want that phar?
# note if vendor dir is present bin/composer works as well
%{github_name}-%{github_commit}/bin/compile
# -----------

%install
mkdir -p -m 0755 %{buildroot}%{composer}/%{composer_vendor}/%{composer_project} %{buildroot}%{_bindir}
cp -rp %{github_name}-%{github_commit}/{bin,res,src,tests} %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}/
cp -a %{github_name}-%{github_commit}/{composer.*,phpunit.xml.dist} %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}/

ln -s %{composer}/%{composer_vendor}/%{composer_project}/bin/composer %{buildroot}%{_bindir}/composer

# FIXME bundling
cp -rp %{github_name}-%{github_commit}/vendor %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}/
# -----------

# RPM "magic"
mkdir -p -m 0755 %{buildroot}%{_sysconfdir}/rpm
install -p -m 0644 macros.composer %{buildroot}%{_sysconfdir}/rpm/
mkdir -p -m 0755 %{buildroot}%{_rpmconfigdir}/fileattrs
install -p -m 0644 composer.attr %{buildroot}%{_rpmconfigdir}/fileattrs/
install -p -m 0755 composer.prov %{buildroot}%{_rpmconfigdir}/
install -p -m 0755 composer.req %{buildroot}%{_rpmconfigdir}/


%check
cd %{github_name}-%{github_commit}
phpunit -d date.timezone=UTC


%files
%doc %{github_name}-%{github_commit}/LICENSE
%doc %{github_name}-%{github_commit}/*.md
%doc %{github_name}-%{github_commit}/PORTING_INFO
%doc %{github_name}-%{github_commit}/doc
%dir %{composer}
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}

%{_bindir}/composer
# RPM "magic"
%{_sysconfdir}/rpm/macros.composer
%{_rpmconfigdir}/fileattrs/composer.attr
%{_rpmconfigdir}/composer.prov
%{_rpmconfigdir}/composer.req


%changelog
* Mon Feb 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.1.alpha6
- Initial package
