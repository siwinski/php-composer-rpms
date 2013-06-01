%{?composer_find_provides_and_requires}

%global github_owner     fabpot
%global github_name      Silex
%global github_version   1.0.0
%global github_commit    46115368bb187d76aa43252e593378bfeb403b82

%global composer_vendor  silex
%global composer_project silex

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        1%{?dist}
Summary:        PHP micro-framework based on the Symfony2 Components

License:        MIT
URL:            http://silex.sensiolabs.org
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:      noarch
BuildRequires:  php-composer

# phpci
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-phar
Requires:       php-reflection
Requires:       php-session
Requires:       php-spl
Requires:       php-tokenizer

%description
Silex is a PHP microframework for PHP 5.3+. It is built on the shoulders of
Symfony2 and Pimple and also inspired by sinatra.

A microframework provides the guts for building simple single-file apps. Silex
aims to be:
* Concise: Silex exposes an intuitive and concise API that is fun to use.
* Extensible: Silex has an extension system based around the Pimple micro
  service-container that makes it even easier to tie in third party libraries.
* Testable: Silex uses Symfony2's HttpKernel which abstracts request and
  response. This makes it very easy to test apps and the framework itself. It
  also respects the HTTP specification and encourages its proper use.

WARNING: This is just a development RPM.  Please submit issues at
         https://github.com/siwinski/php-composer-rpms/issues and prefix
         your issue title with "[%name] ".


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
%{composer_install} --verbose


%files
%doc *.md
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%exclude %{composer}/%{composer_vendor}/%{composer_project}/*.md


%changelog
* Sun May 26 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
