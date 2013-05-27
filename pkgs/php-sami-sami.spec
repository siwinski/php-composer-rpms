%{?composer_find_provides_and_requires}

%global github_owner     fabpot
%global github_name      Sami
%global github_version   1.0
%global github_commit    a3ceda872e37d001650ad0fe67c93ac669a48d52

%global composer_vendor  sami
%global composer_project sami

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        1%{?dist}
Summary:        An API documentation generator

License:        MIT
URL:            http://silex.sensiolabs.org
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:      noarch
BuildRequires:  php-composer

# phpci
Requires:       php-ctype
Requires:       php-json
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

%description
%{sumamry}.

Curious about what Sami generates? Have a look at the Symfony API
(http://api.symfony.com/).


%prep
%setup -q -n %{github_name}-%{github_commit}

# Fix bin shebang
sed 's#/usr/bin/env php#%{_bindir}/php#' -i sami.php


%build
# Empty build section, nothing to build


%install
%{composer_install}


%files
%doc *.md
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%{_bindir}/sami.php
%exclude %{composer}/%{composer_vendor}/%{composer_project}/*.md


%changelog
* Sun May 26 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
