%{?composer_find_provides_and_requires}

%global github_owner     dflydev
%global github_name      dflydev-markdown
%global github_version   1.0.2
%global github_commit    2a1b3516bd5af6e722b40ae9e1fccd03e1772060

%global composer_vendor  %{github_owner}
%global composer_project markdown

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        1%{?dist}
Summary:        PHP Markdown & Extra

License:        BSD
URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:      noarch
BuildRequires:  php-composer

# phpci
Requires:       php-pcre

%description
An updated and stripped version of the original PHP Markdown
(http://michelf.com/projects/php-markdown/) by Michel Fortin.

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
* Tue May 28 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.2-1
- Initial package
