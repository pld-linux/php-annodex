%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	phpannodex - object oriented PHP wrappings for libannodex
Summary(pl):	phpannodex - obiektowo zorientowany interfejs PHP dla libannodex
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
BuildRequires:	rpmbuild(macros) >= 1.322
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
phpannodex is an extension for PHP that provides object oriented PHP
wrappings for libannodex, a C library for manipulating Annodex media.

phpannodex consists of two main parts. The phpannodex core is a set of
C functions that wrap around the libannodex functions and make them
visible to PHP. The phpannodex classes are PHP5 classes that provide
an object oriented API for dealing with the phpannodex core.

%description -l pl
phpannodex to rozszerzenie PHP udostêpniaj±ce obiektowo zorientowany
interfejs PHP dla libannodex - biblioteki C do obróbki mediów Annodex.

phpannodex sk³ada siê z dwóch g³ównych czê¶ci. Rdzeñ phpannodex to
zbiór funkcji C obudowuj±cych funkcje libannodex i czyni±cych je
widocznymi dla PHP. Klasy phpannodex to klasy PHP5 udostêpniaj±ce
obiektowo zorientowane API do wspó³pracy z rdzeniem phpannodex.

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
install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d

%{__make} -C src install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{extensionsdir}

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/phpannodex.ini
; Enable phpannodex extension module
extension=phpannodex.so
EOF

install -d $RPM_BUILD_ROOT%{_datadir}/php
cp -r phpannodex $RPM_BUILD_ROOT%{_datadir}/php

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc LICENCE README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/phpannodex.ini
%attr(755,root,root) %{extensionsdir}/phpannodex.so
%{_datadir}/php/phpannodex
