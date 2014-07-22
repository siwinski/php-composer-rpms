# See WARNING notes in %%description

#
# RPM spec file for composer
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

# Disable automatic dependency processing
# (prevents endless loop if php-composer is already installed on buildsys)
AutoReqProv: no

%global github_owner       composer
%global github_name        composer
%global github_version     1.0.0
%global github_version_pre alpha8
%global github_commit      1eb1df44a97fb2daca1bb8b007f3bee012f0aa46

%global composer_vendor    composer
%global composer_project   composer

%if !0%{?github_tagged}
%global github_release git%(c=%{github_commit}; echo ${c:0:7})
%endif

# "php": ">=5.3.2"
%global php_min_ver        5.3.2
# "seld/jsonlint": "1.*"
%global jsonlint_min_ver   1.0
%global jsonlint_max_ver   2.0
# "justinrainbow/json-schema": "1.1.*"
%global jsonschema_min_ver 1.1.0
# DEBUG
#%global jsonschema_max_ver 1.2.0
%global jsonschema_max_ver 2.0
# "symfony/console": "~2.3",
# "symfony/finder": "~2.2",
# "symfony/process": "~2.1"
%global symfony_min_ver    2.3
%global symfony_max_ver    3.0

%global composer   %{_datadir}/composer

%global macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%{!?__phpunit: %global __phpunit %{_bindir}/phpunit}

# For now, disable tests by default
# Tests are only run with rpmbuild --with tests
%global with_tests %{?_with_tests:1}%{!?_with_tests:0}

Name:          composer
Version:       %{github_version}
Release:       0.5%{?github_version_pre:.%{github_version_pre}}%{?github_release:.%{github_release}}%{?dist}
Summary:       Dependency Manager for PHP

Group:         Development/Libraries
License:       MIT
URL:           http://getcomposer.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz
# Required only for bootstrapping/build
Source1:       http://getcomposer.org/download/%{version}%{?github_version_pre:-%{github_version_pre}}/composer.phar
# RPM "magic"
Source2:       macros.%{name}
Source3:       %{name}.attr
Source4:       %{name}.prov
Source5:       %{name}.req
Source6:       %{name}-fixreq
Source7:       %{name}-install

BuildArch:     noarch
%if %{with_tests}
# For tests: composer.json
BuildRequires:  php-phpunit-PHPUnit
BuildRequires:  php-jsonlint        >= %{jsonlint_min_ver}
BuildRequires:  php-jsonlint        <  %{jsonlint_max_ver}
BuildRequires:  php-JsonSchema      >= %{jsonschema_min_ver}
BuildRequires:  php-JsonSchema      <  %{jsonschema_max_ver}
BuildRequires:  php-symfony-Console >= %{symfony_min_ver}
BuildRequires:  php-symfony-Console <  %{symfony_max_ver}
BuildRequires:  php-symfony-Finder  >= %{symfony_min_ver}
BuildRequires:  php-symfony-Finder  <  %{symfony_max_ver}
BuildRequires:  php-symfony-Process >= %{symfony_min_ver}
BuildRequires:  php-symfony-Process <  %{symfony_max_ver}
# For tests: phpcompatinfo (computed from version 1.0.0-alpha8)
%endif

# composer.json
Requires:      php(language)       >= %{php_min_ver}
Requires:      php-jsonlint        >= %{jsonlint_min_ver}
Requires:      php-jsonlint        <  %{jsonlint_max_ver}
Requires:      php-JsonSchema      >= %{jsonschema_min_ver}
Requires:      php-JsonSchema      <  %{jsonschema_max_ver}
Requires:      php-symfony-Console >= %{symfony_min_ver}
Requires:      php-symfony-Console <  %{symfony_max_ver}
Requires:      php-symfony-Finder  >= %{symfony_min_ver}
Requires:      php-symfony-Finder  <  %{symfony_max_ver}
Requires:      php-symfony-Process >= %{symfony_min_ver}
Requires:      php-symfony-Process <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.0.0-alpha8)
Requires:      php-ctype
Requires:      php-curl
Requires:      php-date
Requires:      php-filter
Requires:      php-hash
Requires:      php-iconv
Requires:      php-intl
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
# RPM build
Requires:      python-argparse

# Virtual provide
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# Rename
Obsoletes:     php-composer < %{version}-%{release}
Provides:      php-composer = %{version}-%{release}

%description
Composer is a tool for dependency management in PHP. It allows you to declare
the dependent libraries your project needs and it will install them in your
project for you.

WARNING: This is just a development RPM.  Please submit issues at
         https://github.com/siwinski/php-composer-rpms/issues and prefix
         your issue title with "[%name] ".


%prep
%setup -qn %{github_name}-%{github_commit}

# RPM "magic"
mkdir rpm
cp %{SOURCE2} \
   %{SOURCE3} \
   %{SOURCE4} \
   %{SOURCE5} \
   %{SOURCE6} \
   %{SOURCE7} \
   rpm

# Use system libraries
sed -e "s#__DIR__.'/../../vendor/symfony/'#'%pear_phpdir/Symfony/Component/'#" \
    -e "s#__DIR__.'/../../vendor/seld/jsonlint/src/'#'%{_datadir}/php/Seld/JsonLint/'#" \
    -e "s#__DIR__.'/../../vendor/justinrainbow/json-schema/src/'#'%{_datadir}/php/JsonSchema/'#" \
    -i src/Composer/Compiler.php

# No self update
rm -f src/Composer/Command/SelfUpdateCommand.php
sed '/SelfUpdateCommand/d' -i src/Composer/Console/Application.php

# Update bin shebang
sed 's#/usr/bin/env php#%{_bindir}/php#' -i bin/composer

# Set configs (these settings are written to the source's composer.json file)
## Allows loading of classes from the global PHP include path
php %{SOURCE1} config use-include-path true
## Bin dir
php %{SOURCE1} config bin-dir %{_bindir}
## Cache dir
php %{SOURCE1} config cache-dir %{_prefix}/cache/composer

# Create autoload files
php %{SOURCE1} dump-autoload


%build
# Empty build section, nothing to build


%install
pushd %{github_name}-%{github_commit}

mkdir -pm 0755 %{buildroot}%{composer}/%{composer_vendor}/%{composer_project} %{buildroot}%{_bindir}
cp -rp {bin,res,src,tests,vendor} %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}/
cp -a {composer.*,phpunit.xml.dist} %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}/

# Bin
mkdir -pm 0755 %{buildroot}/%{_bindir}
ln -s %{composer}/%{composer_vendor}/%{composer_project}/bin/composer %{buildroot}%{_bindir}/composer

# Cache
mkdir -pm 0777 %{buildroot}/%{_prefix}/cache/composer

# symlink generic autoloader to include path
ln -s %{composer}/%{composer_vendor}/%{composer_project}/vendor %{buildroot}%{composer}/vendor

popd

# RPM "magic"
## Macros
mkdir -pm 0755 %{buildroot}%{macrosdir}
install -pm 0644 rpm/macros.%{name} %{buildroot}%{macrosdir}/
## Fileattrs
mkdir -pm 0755 %{buildroot}%{_rpmconfigdir}/fileattrs
install -pm 0644 rpm/%{name}.attr    %{buildroot}%{_rpmconfigdir}/fileattrs/
install -pm 0755 rpm/%{name}.prov    %{buildroot}%{_rpmconfigdir}/
install -pm 0755 rpm/%{name}.req     %{buildroot}%{_rpmconfigdir}/


%check
%if %{with_tests}
    %{__phpunit} -c tests/complete.phpunit.xml -d date.timezone=UTC
%else
: Tests skipped, missing '--with tests' option
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md doc
%{composer}/vendor
%dir %{composer}
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%{_bindir}/composer
%dir %{_prefix}/cache/composer
# RPM "magic"
%{macrosdir}/%{name}.composer
%{_rpmconfigdir}/fileattrs/%{name}.attr
%{_rpmconfigdir}/%{name}.prov
%{_rpmconfigdir}/%{name}.req


%changelog
* Wed May 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.4.alpha7
- Updated to version 1.0.0-alpha7
- Use ustream PHAR as source instead of downloading
- Path substitution instead of patch
- Updated some macro logic
- Allow for setting of PHAR version
- No COMPOSER_DEV_WARNING_TIME
- No self update

* Fri Apr 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.3.alpha6.20130328git78c250d
- Added composer-install
- Disabled tests by default

* Sat Mar 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.2.20130328git
- Added composer-fixreq

* Thu Mar 28 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.0.0-0.1.20130328git
- git snapshot 78c250da19b823617a14513450576977da36eb3f
- enable tests

* Mon Feb 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.1.alpha6
- Initial package
