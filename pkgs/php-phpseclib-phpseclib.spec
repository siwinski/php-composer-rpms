%{?composer_find_provides_and_requires}

%global github_owner     phpseclib
%global github_name      phpseclib
%global github_version   0.3.5

%global composer_vendor  %{github_owner}
%global composer_project %{github_name}

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        1%{?dist}
Summary:        PHP Secure Communications Library - Pure-PHP implementations of RSA, AES, SSH2, SFTP, X.509 etc

License:        MIT
URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        %{url}/archive/%{github_version}.tar.gz#/%{composer_vendor}-%{composer_project}.tar.gz

BuildArch:      noarch
BuildRequires:  php-composer

# phpci
Requires:       php-pcre

%description
MIT-licensed pure-PHP implementations of an arbitrary-precision integer
arithmetic library, fully PKCS#1 (v2.1) compliant RSA, DES, 3DES, RC4,
Rijndael, AES, Blowfish, Twofish, SSH-1, SSH-2, SFTP, and X.509.

WARNING: This is just a development RPM.  Please submit issues at
         https://github.com/siwinski/php-composer-rpms/issues and prefix
         your issue title with "[%name] ".


%prep
%setup -q -n %{github_name}-%{github_version}


%build
# Empty build section, nothing to build


%install
%{composer_install}


%files
%doc *.md LICENSE AUTHORS
%dir %{composer}/%{composer_vendor}
     %{composer}/%{composer_vendor}/%{composer_project}
%exclude %{composer}/%{composer_vendor}/%{composer_project}/*.md


%changelog
