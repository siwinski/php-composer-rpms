Name:           php-composer-sabredav
Version:        1.8.3
Release:        1%{?dist}
Summary:        Sabre

License:        GPLv3
URL:            https://code.google.com/p/sabredav/
Source0:        https://sabredav.googlecode.com/files/SabreDAV-%{version}.zip
BuildArch:      noarch
BuildRequires:  php-composer

%description
%{summary}

%prep
%setup -q -n SabreDAV


%build
# nothing

%install
# read reqs and provs from here
install -Dpm 644 composer.json %{buildroot}%{composer}/SabreDAV/composer.json


%files
%doc
%{composer}/SabreDAV


%changelog
