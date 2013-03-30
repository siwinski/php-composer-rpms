
%global github_owner       evert
%global github_name        sabre-vobject
%global github_version     2.0.7

%global composer_vendor    sabre
%global composer_project   vobject

Name:       php-%{composer_vendor}-%{composer_project}
Version:    %{github_version}
Release:    1%{?dist}
Summary:    An intuitive reader for iCalendar and vCard objects

License:    BSD
URL:        https://github.com/evert/sabre-vobject
Source0:    https://github.com/%{github_owner}/%{github_name}/archive/%{github_version}.tar.gz#/%{composer_vendor}-%{composer_project}.tar.gz

BuildArch:  noarch

BuildRequires:  php-composer

%description
The VObject library for PHP allows you to easily parse and manipulate iCalendar
and vCard objects.
WARNING: This is just a development RPM.  Please submit issues at
         https://github.com/siwinski/php-composer-rpms/issues and prefix
         your issue title with "[%name] ".


%prep
%setup -q -n %{composer_vendor}-%{composer_project}-%{version}

# set version
sed -i '/"name": "%{composer_vendor}\/%{composer_project}",/ a "version": "%{version}",' composer.json
# use global autoloader
sed -i s:"include __DIR__ . '/../vendor/autoload.php';":"include 'vendor/autoload.php';": tests/bootstrap.php

composer dumpautoload


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}
mkdir -p %{buildroot}%{_datadir}/tests/%{composer_vendor}-%{composer_project}
cp -a tests/* %{buildroot}%{_datadir}/tests/%{composer_vendor}-%{composer_project}
cp -a lib/Sabre %{buildroot}%{composer}
install -pm 644 composer.json %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}/

mkdir -p %{buildroot}%{_bindir}
install -pm 755 bin/vobjectvalidate.php %{buildroot}%{_bindir}/vobjectvalidate


%check
phpunit -c tests/phpunit.xml -d date.timezone=UTC


%files
%doc LICENSE README.md ChangeLog
%dir %{composer}/Sabre
%{composer}/Sabre/*
%{_bindir}/vobjectvalidate
%{_datadir}/tests/%{composer_vendor}-%{composer_project}

%dir %{composer}/%{composer_vendor}
%{composer}/%{composer_vendor}/%{composer_project}

%changelog
 
