%{?composer_find_provides_and_requires}

%global github_owner     fabpot
%global github_name      PHP-CS-Fixer
%global github_version   0.2.0
%global github_commit    6ed572044d43a540f758534a1bd10ca424f496fc

%global composer_vendor  %{github_owner}
%global composer_project php-cs-fixer

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        1%{?dist}
Summary:        PHP Coding Standards Fixer

License:        MIT
URL:            http://cs.sensiolabs.org
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:      noarch
BuildRequires:  php-composer

# phpci
Requires:       php-pcre
Requires:       php-phar
Requires:       php-spl

%description
The PHP Coding Standards Fixer tool fixes most issues in your code when you want
to follow the PHP coding standards as defined in the PSR-1 and PSR-2 documents.

If you are already using PHP_CodeSniffer to identify coding standards problems
in your code, you know that fixing them by hand is tedious, especially on large
projects. This tool does the job for you.

WARNING: This is just a development RPM.  Please submit issues at
         https://github.com/siwinski/php-composer-rpms/issues and prefix
         your issue title with "[%name] ".


%prep
%setup -q -n %{github_name}-%{github_commit}

# TODO: No self-update

# Fix bin shebang
sed 's#/usr/bin/env php#%{_bindir}/php#' -i php-cs-fixer


%build
# Empty build section, nothing to build


%install
%{composer_install}


%files
%doc *.md
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%{_bindir}/php-cs-fixer
%exclude %{composer}/%{composer_vendor}/%{composer_project}/*.md


%changelog
* Sun May 26 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-1
- Initial package
