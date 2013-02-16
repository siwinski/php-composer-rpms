# See WARNING notes in %%description

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
%global jsonschema_max_ver 1.2.0

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
Requires:      php-filter
Requires:      php-hash
Requires:      php-iconv
Requires:      php-json
Requires:      php-libxml
Requires:      php-mbstring
Requires:      php-openssl
Requires:      php-pcre
Requires:      php-phar
Requires:      php-reflection
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-tokenizer
Requires:      php-xsl
Requires:      php-zip
Requires:      php-zlib

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

# Update macros' version and base path
sed -e 's:__COMPOSER_VERSION__:%version:' \
    -e 's:__COMPOSER__:%composer:' \
    -i macros.composer


%build


%install
mkdir -p -m 0755 %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}
cp -rp %{github_name}-%{github_commit}/* %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}/

# RPM "magic"
mkdir -p -m 0755 %{buildroot}%{_sysconfdir}/rpm
install -p -m 0644 macros.composer %{buildroot}%{_sysconfdir}/rpm/
mkdir -p -m 0755 %{buildroot}%{_rpmconfigdir}/fileattrs
install -p -m 0644 composer.attr %{buildroot}%{_rpmconfigdir}/fileattrs/
install -p -m 0755 composer.prov %{buildroot}%{_rpmconfigdir}/
install -p -m 0755 composer.req %{buildroot}%{_rpmconfigdir}/


%check


%files
%doc %{github_name}-%{github_commit}/LICENSE
%doc %{github_name}-%{github_commit}/*.md
%doc %{github_name}-%{github_commit}/PORTING_INFO
%dir %{composer}
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%exclude %{composer}/%{composer_vendor}/%{composer_project}/LICENSE
%exclude %{composer}/%{composer_vendor}/%{composer_project}/*.md
%exclude %{composer}/%{composer_vendor}/%{composer_project}/PORTING_INFO
# RPM "magic"
%{_sysconfdir}/rpm/macros.composer
%{_rpmconfigdir}/fileattrs/composer.attr
%{_rpmconfigdir}/composer.prov
%{_rpmconfigdir}/composer.req


%changelog
* Fri Feb 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.1.alpha6
- Initial package
