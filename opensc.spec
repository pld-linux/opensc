Summary:	OpenSC library - for accessing SmartCard devices using PC/SC Lite
Summary(pl):	Biblioteka OpenSC - do korzystania z kart procesorowych przy u¿yciu PC/SC Lite
Name:		opensc
Version:	0.7.0
Release:	1
License:	LGPL
Group:		Applications
Source0:	http://www.opensc.org/files/%{name}-%{version}.tar.gz
Patch0:		%{name}-nolibs.patch
URL:		http://www.opensc.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libtool >= 1:1.4.2-9
BUildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
u¿yciu pakietu warstwy po¶redniej PC/SC Lite. Jest to tak¿e podstawowa
biblioteka projektu OpenSC. Podstawowa funkcjonalno¶æ (np. SELECT
FILE, READ BINARY) powinna dzia³aæ tak¿e z dowoln± kart± procesorow±
zgodn± z ISO-7816-4. Szyfrowanie i odszyfrowywanie przy u¿yciu
prywatnych kluczy na karcie na razie jest mo¿liwe tylko przy u¿yciu
kart kompatybilnych z PKCS#16, takich jak FINEID (Finnish Electronic
IDentity) produkowanych przez Setec.

%package devel
Summary:	OpenSC development files
Summary(pl):	Pliki dla programistów u¿ywaj±cych OpenSC
Group:		Development/Tools
Requires:	%{name}-libs = %{version}

%description devel
OpenSC development files.

%description devel -l pl
Pliki dla programistów u¿ywaj±cych OpenSC.

%package static
Summary:	Static OpenSC libraries
Summary(pl):	Bibloteki statyczne OpenSC
Group:		Development/Tools
Requires:	%{name}-devel = %{version}

%description static
Static OpenSC libraries.

%description static -l pl
Statyczne biblioteki OpenSC.

%package -n pam_opensc
Summary:	OpenSC module for PAM
Summary(pl):	Modu³ PAM OpenSC
License:	GPL
Group:		Base
Requires:	%{name} = %{version}

%description -n pam_opensc
OpenSC module for PAM.

%description -n pam_opensc -l pl
Modu³ PAM OpenSC.

%prep
%setup -q
%patch -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib
mv -f $RPM_BUILD_ROOT%{_libdir}/security $RPM_BUILD_ROOT/lib

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.signer THANKS TODO docs/pkcs-15v1_1.asn
%attr(755,root,root) %{_bindir}/cryptoflex-tool
%attr(755,root,root) %{_bindir}/opensc-explorer
%attr(755,root,root) %{_bindir}/opensc-tool
%attr(755,root,root) %{_bindir}/pkcs15-*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/libscam.so
%dir %{_libdir}/pkcs11
%attr(755,root,root) %{_libdir}/pkcs11/opensc-pkcs11.so
%dir %{_datadir}/opensc
%{_datadir}/opensc/*.profile
%{_mandir}/man[157]/pkcs15*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/opensc-config
%attr(755,root,root) %{_libdir}/libopensc.so
%attr(755,root,root) %{_libdir}/libpkcs15init.so
%attr(755,root,root) %{_libdir}/libscconf.so
%attr(755,root,root) %{_libdir}/libscldap.so
%{_libdir}/libopensc.la
%{_libdir}/libpkcs15init.la
%{_libdir}/libscconf.la
%{_libdir}/libscldap.la
%{_libdir}/libscrandom.a
%{_includedir}/opensc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopensc.a
%{_libdir}/libpkcs15init.a
%{_libdir}/libscconf.a
%{_libdir}/libscldap.a

%files -n pam_opensc
%defattr(644,root,root,755)
%attr(755,root,root) /lib/security/pam_opensc.so
