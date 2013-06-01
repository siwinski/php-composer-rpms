%{?composer_find_provides_and_requires}

%global github_owner     doctrine
%global github_name      annotations
%global github_version   1.1
%global github_commit    d2bb4eaf82f74fd6964503b4826d3963e134e400

%global composer_vendor  %{github_owner}
%global composer_project %{github_name}

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        1%{?dist}
Summary:        Docblock Annotations Parser

License:        MIT
URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:      noarch
BuildRequires:  php-composer
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)

# phpci
Requires:       php-ctype
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer

%description
Docblock Annotations Parser library (extracted from Doctrine Common).

WARNING: This is just a development RPM.  Please submit issues at
         https://github.com/siwinski/php-composer-rpms/issues and prefix
         your issue title with "[%name] ".


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
%{composer_install}


%check
cd %{buildroot}%{composer}/%{composer_vendor}/%{composer_project}
ln -s %{composer}/composer/composer/vendor vendor
%{_bindir}/phpunit
rm -f vendor


%files
%doc *.md
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%exclude %{composer}/%{composer_vendor}/%{composer_project}/*.md


%changelog
* Fri Apr 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1-1
- Initial package
