%{?composer_find_provides_and_requires}

%global github_owner     sebastianbergmann
%global github_name      diff
%global github_version   0
%global github_commit    222e1939856808fe4d02ec856a08721858d0217b
%global github_date      20130522

%global github_release   %{github_date}git%(c=%{github_commit}; echo ${c:0:7})

%global composer_vendor  sebastian
%global composer_project %{github_name}

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        0.1.%{github_release}%{?dist}
Summary:        Diff implementation for PHP

License:        BSD
URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:      noarch
BuildRequires:  php-composer

# phpci
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(pear.phpunit.de/Diff) = %{version}

%description
Diff implementation for PHP, factored out of PHPUnit into a stand-alone
component.

WARNING: This is just a development RPM.  Please submit issues at
         https://github.com/siwinski/php-composer-rpms/issues and prefix
         your issue title with "[%name] ".


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
%{composer_install}


%files
%doc *.md
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%exclude %{composer}/%{composer_vendor}/%{composer_project}/*.md


%changelog
* Tue May 28 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0-0.1.20130522git222e193
- Initial package
