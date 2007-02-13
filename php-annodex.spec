Summary:	phpannodex - object oriented PHP wrappings for libannodex
Summary(pl.UTF-8):	phpannodex - obiektowo zorientowany interfejs PHP dla libannodex
Name:		php-annodex
Version:	0.4
Release:	1
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://www.annodex.net/software/phpannodex/download/phpannodex-%{version}.tar.gz
# Source0-md5:	d100a86caa47c27ec7bbf4cae339d78c
Patch0:		phpannodex-libannodex.patch
URL:		http://www.annodex.net/software/phpannodex/index.html
BuildRequires:	libannodex-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
phpannodex is an extension for PHP that provides object oriented PHP
wrappings for libannodex, a C library for manipulating Annodex media.

phpannodex consists of two main parts. The phpannodex core is a set of
C functions that wrap around the libannodex functions and make them
visible to PHP. The phpannodex classes are PHP5 classes that provide
an object oriented API for dealing with the phpannodex core.

%description -l pl.UTF-8
phpannodex to rozszerzenie PHP udostępniające obiektowo zorientowany
interfejs PHP dla libannodex - biblioteki C do obróbki mediów Annodex.

phpannodex składa się z dwóch głównych części. Rdzeń phpannodex to
zbiór funkcji C obudowujących funkcje libannodex i czyniących je
widocznymi dla PHP. Klasy phpannodex to klasy PHP5 udostępniające
obiektowo zorientowane API do współpracy z rdzeniem phpannodex.

%prep
%setup -q -n phpannodex-%{version}
%patch0 -p1

find phpannodex -name '.*.swp' | xargs rm -f

%build
cd src
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} -C src install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/phpannodex.ini
; Enable phpannodex extension module
extension=phpannodex.so
EOF

install -d $RPM_BUILD_ROOT%{_datadir}/php
cp -a phpannodex $RPM_BUILD_ROOT%{_datadir}/php

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc LICENCE README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/phpannodex.ini
%attr(755,root,root) %{php_extensiondir}/phpannodex.so
%{_datadir}/php/phpannodex
