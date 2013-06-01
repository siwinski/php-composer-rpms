%{?composer_find_provides_and_requires}

%global github_owner     doctrine
%global github_name      lexer
%global github_version   1.0
%global github_commit    2f708a85bb3aab5d99dab8be435abd73e0b18acb

%global composer_vendor  %{github_owner}
%global composer_project %{github_name}

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        1%{?dist}
Summary:        Base library for a lexer that can be used in parsers

License:        MIT
URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:      noarch
BuildRequires:  php-composer
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)

# phpci
Requires:       php-reflection
Requires:       php-pcre

%description
Base library for a lexer that can be used in top-down, recursive descent
parsers.

This lexer is used in Doctrine Annotations and in Doctrine ORM (DQL).

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
%{_bindir}/phpunit


%files
%doc *.md
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%exclude %{composer}/%{composer_vendor}/%{composer_project}/*.md


%changelog
* Fri Apr 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1
- Initial package
