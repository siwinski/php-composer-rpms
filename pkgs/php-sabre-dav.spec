
%global composer_vendor    sabre
%global composer_project   dav

Name:           php-%{composer_vendor}-%{composer_project}
Version:        1.8.3
Release:        1%{?dist}
Summary:        Sabre

License:        BSD
URL:            https://code.google.com/p/sabredav/
Source0:        https://sabredav.googlecode.com/files/SabreDAV-%{version}.zip

BuildArch:      noarch

BuildRequires:  php-composer
BuildRequires:  php-composer(sabre/vobject)

%description
%{summary}

%prep
%setup -q -n SabreDAV

# set version
sed -i '/"name": "%{composer_vendor}\/%{composer_project}",/ a "version": "%{version}",' composer.json
# use global autoloader
sed -i s:"include __DIR__ . '/../vendor/autoload.php';":"include 'vendor/autoload.php';": tests/bootstrap.php
# unbundle
rm -rf vendor


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}
mkdir -p %{buildroot}%{_datadir}/tests/%{composer_vendor}-%{composer_project}
cp -a tests/* %{buildroot}%{_datadir}/tests/%{composer_vendor}-%{composer_project}
cp -a lib/Sabre %{buildroot}%{composer}
install -pm 644 composer.json %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}/


%check
phpunit -c tests/phpunit.xml -d date.timezone=UTC


%files
%doc LICENSE README.md ChangeLog docs examples
%dir %{composer}/Sabre
%{composer}/Sabre/*
%{_datadir}/tests/%{composer_vendor}-%{composer_project}

%dir %{composer}/%{composer_vendor}
%{composer}/%{composer_vendor}/%{composer_project}


%changelog