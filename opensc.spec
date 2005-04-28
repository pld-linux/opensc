Summary:	OpenSC library - for accessing SmartCard devices using PC/SC Lite
Summary(pl):	Biblioteka OpenSC - do korzystania z kart procesorowych przy u�yciu PC/SC Lite
Name:		opensc
Version:	0.9.6
Release:	1
Epoch:		0
License:	LGPL
Group:		Applications
Source0:	http://www.opensc.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	38fdd64566cc6fc83338d659e816b4fb
Patch0:		%{name}-libdir.patch
Patch1:		%{name}-segv.patch
Patch2:		%{name}-explorer-debug.patch
Patch3:		%{name}-gcc4.patch
URL:		http://www.opensc.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libassuan-devel >= 1:0.6.0
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	openct-devel
BuildRequires:	pam-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# datadir is used for config files and (editable) profiles
%define		_datadir	/etc
%define		_sysconfdir	/etc/opensc
%define		mozplugindir	/usr/%{_lib}/mozilla/plugins

%description
libopensc is a library for accessing SmartCard devices using PC/SC
Lite middleware package. It is also the core library of the OpenSC
project. Basic functionality (e.g. SELECT FILE, READ BINARY) should
work on any ISO 7816-4 compatible SmartCard. Encryption and decryption
using private keys on the SmartCard is at the moment possible only
with PKCS#15 compatible cards, such as the FINEID (Finnish Electronic
IDentity) card manufactured by Setec.

%description -l pl
libopensc to biblioteka do korzystania z kart procesorowych przy
u�yciu pakietu warstwy po�redniej PC/SC Lite. Jest to tak�e podstawowa
biblioteka projektu OpenSC. Podstawowa funkcjonalno�� (np. SELECT
FILE, READ BINARY) powinna dzia�a� tak�e z dowoln� kart� procesorow�
zgodn� z ISO-7816-4. Szyfrowanie i odszyfrowywanie przy u�yciu
prywatnych kluczy na karcie na razie jest mo�liwe tylko przy u�yciu
kart kompatybilnych z PKCS#16, takich jak FINEID (Finnish Electronic
IDentity) produkowanych przez Setec.

%package devel
Summary:	OpenSC development files
Summary(pl):	Pliki dla programist�w u�ywaj�cych OpenSC
Group:		Development/Tools
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	openct-devel
Requires:	openssl-devel
Requires:	pcsc-lite-devel

%description devel
OpenSC development files.

%description devel -l pl
Pliki dla programist�w u�ywaj�cych OpenSC.

%package static
Summary:	Static OpenSC libraries
Summary(pl):	Bibloteki statyczne OpenSC
Group:		Development/Tools
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static OpenSC libraries.

%description static -l pl
Statyczne biblioteki OpenSC.

%package -n pam-pam_opensc
Summary:	OpenSC module for PAM
Summary(pl):	Modu� PAM OpenSC
License:	GPL
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	pam_opensc

%description -n pam-pam_opensc
OpenSC module for PAM.

%description -n pam-pam_opensc -l pl
Modu� PAM OpenSC.

%package -n mozilla-plugin-opensc
Summary:	OpenSC Signer plugin for Mozilla
Summary(pl):	Wtyczka OpenSC Signer dla Mozilli
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	pinentry-gtk

%description -n mozilla-plugin-opensc
OpenSC Signer plugin for Mozilla.

%description -n mozilla-plugin-opensc -l pl
Wtyczka OpenSC Signer dla Mozilli.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-pin-entry=/usr/bin/pinentry-gtk \
	--with-plugin-dir="%{mozplugindir}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{mozplugindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/security $RPM_BUILD_ROOT/%{_lib}

# just install instead of symlinking
rm -f $RPM_BUILD_ROOT%{mozplugindir}/opensc-signer.so
mv -f $RPM_BUILD_ROOT%{_libdir}/opensc/opensc-signer.so $RPM_BUILD_ROOT%{mozplugindir}

# default config
install etc/opensc.conf $RPM_BUILD_ROOT%{_sysconfdir}
install etc/scldap.conf $RPM_BUILD_ROOT%{_sysconfdir}

# useless (dlopened by *.so)
rm -f $RPM_BUILD_ROOT%{_libdir}/{libscam,opensc-*}.{a,la} \
	$RPM_BUILD_ROOT%{_libdir}/opensc/*.{a,la} \
	$RPM_BUILD_ROOT%{_libdir}/pkcs11/*.{a,la} \
	$RPM_BUILD_ROOT/%{_lib}/security/pam_opensc.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE ChangeLog NEWS docs/{pkcs-15v1_1.asn,opensc.{html,css}}
%attr(755,root,root) %{_bindir}/cardos-info
%attr(755,root,root) %{_bindir}/cryptoflex-tool
%attr(755,root,root) %{_bindir}/opensc-explorer
%attr(755,root,root) %{_bindir}/opensc-tool
%attr(755,root,root) %{_bindir}/pkcs11-tool
%attr(755,root,root) %{_bindir}/pkcs15-*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/libscam.so
%attr(755,root,root) %{_libdir}/opensc-pkcs11.so
%dir %{_libdir}/pkcs11
%attr(755,root,root) %{_libdir}/pkcs11/pkcs11-spy.so
%dir %{_libdir}/opensc
%attr(755,root,root) %{_libdir}/opensc/engine_opensc.so
%attr(755,root,root) %{_libdir}/opensc/engine_pkcs11.so
%dir %{_datadir}/opensc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/opensc/*.profile
%{_mandir}/man1/cardos-info.1*
%{_mandir}/man1/cryptoflex-tool.1*
%{_mandir}/man1/opensc-explorer.1*
%{_mandir}/man1/opensc-tool.1*
%{_mandir}/man1/pkcs11-tool.1*
%{_mandir}/man1/pkcs15-*.1*
%{_mandir}/man[57]/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/opensc-config
%attr(755,root,root) %{_libdir}/libopensc.so
%attr(755,root,root) %{_libdir}/libpkcs11.so
%attr(755,root,root) %{_libdir}/libpkcs15init.so
%attr(755,root,root) %{_libdir}/libscconf.so
%attr(755,root,root) %{_libdir}/libscldap.so
%{_libdir}/lib*.la
%{_includedir}/opensc
%{_pkgconfigdir}/*.pc
%{_mandir}/man1/opensc-config.1*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n pam-pam_opensc
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_opensc.so

%files -n mozilla-plugin-opensc
%defattr(644,root,root,755)
%attr(755,root,root) %{mozplugindir}/opensc-signer.so
