#
# Conditional build:
%bcond_without	openct	# use PCSC directly, without OpenCT support
#
Summary:	OpenSC library - for accessing SmartCard devices using PC/SC Lite
Summary(pl.UTF-8):	Biblioteka OpenSC - do korzystania z kart procesorowych przy użyciu PC/SC Lite
Name:		opensc
Version:	0.12.0
Release:	1
Epoch:		0
License:	LGPL v2.1+
Group:		Applications
Source0:	http://www.opensc-project.org/files/opensc/%{name}-%{version}.tar.gz
# Source0-md5:	630fa3b8717d22a1d069d120153a0c52
Source1:	%{name}-initramfs-hook
Source2:	%{name}-initramfs-local-bottom
Source3:	%{name}-initramfs-local-top
Source4:	%{name}-initramfs-README
URL:		http://www.opensc-project.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
BuildRequires:	docbook-style-xsl
BuildRequires:	libltdl-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	libxslt-progs
%{?with_openct:BuildRequires:	openct-devel}
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	openssl-devel >= 0.9.7d
%{!?with_openct:BuildRequires:	pcsc-lite-devel >= 1.6.0}
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.364
BuildRequires:	zlib-devel
%{!?with_openct:Requires:	pcsc-lite-libs >= 1.6.0}
Obsoletes:	browser-plugin-opensc
Obsoletes:	mozilla-plugin-opensc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# datadir is used for config files and (editable) profiles
%define		_datadir	/etc
%define		_sysconfdir	/etc/opensc

%description
libopensc is a library for accessing SmartCard devices using PC/SC
Lite middleware package. It is also the core library of the OpenSC
project. Basic functionality (e.g. SELECT FILE, READ BINARY) should
work on any ISO 7816-4 compatible SmartCard. Encryption and decryption
using private keys on the SmartCard is at the moment possible only
with PKCS#15 compatible cards, such as the FINEID (Finnish Electronic
IDentity) card manufactured by Setec.

%description -l pl.UTF-8
libopensc to biblioteka do korzystania z kart procesorowych przy
użyciu pakietu warstwy pośredniej PC/SC Lite. Jest to także podstawowa
biblioteka projektu OpenSC. Podstawowa funkcjonalność (np. SELECT
FILE, READ BINARY) powinna działać także z dowolną kartą procesorową
zgodną z ISO-7816-4. Szyfrowanie i odszyfrowywanie przy użyciu
prywatnych kluczy na karcie na razie jest możliwe tylko przy użyciu
kart kompatybilnych z PKCS#16, takich jak FINEID (Finnish Electronic
IDentity) produkowanych przez Setec.

%package devel
Summary:	OpenSC development files
Summary(pl.UTF-8):	Pliki dla programistów używających OpenSC
Group:		Development/Tools
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libltdl-devel
%{?with_openct:Requires:	openct-devel}
Requires:	openssl-devel
%{!?with_openct:Requires:	pcsc-lite-devel >= 1.6.0}

%description devel
OpenSC development files.

%description devel -l pl.UTF-8
Pliki dla programistów używających OpenSC.

%package static
Summary:	Static OpenSC library
Summary(pl.UTF-8):	Bibloteka statyczna OpenSC
Group:		Development/Tools
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static OpenSC library.

%description static -l pl.UTF-8
Biblioteka statyczna OpenSC.

%package initramfs
Summary:	OpenSC support scripts for initramfs-tools
Summary(pl.UTF-8):	Skrypty dla initramfs-tools ze wsparciem dla OpenSC
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	initramfs-tools

%description initramfs
OpenSC support scripts for initramfs-tools.

%description initramfs -l pl.UTF-8
Skrypty dla initramfs-tools ze wsparciem dla OpenSC.

%prep
%setup -q

install %{SOURCE4} README.initramfs

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_openct:--enable-openct --disable-pcsc} \
	%{!?with_openct:--enable-pcsc --disable-openct} \
	--enable-doc \
	--with-pcsc-provider=%{_libdir}/libpcsclite.so.1

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/{hooks,scripts/local-{bottom,top}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/hooks/opensc
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/scripts/local-bottom/opensc
install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/scripts/local-top/opensc

# not needed (dlopened by soname)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{onepin-opensc-pkcs11,opensc-pkcs11,pkcs11-spy}.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README doc/html.out/tools.html
%attr(755,root,root) %{_bindir}/cardos-tool
%attr(755,root,root) %{_bindir}/cryptoflex-tool
%attr(755,root,root) %{_bindir}/eidenv
%attr(755,root,root) %{_bindir}/netkey-tool
%attr(755,root,root) %{_bindir}/opensc-explorer
%attr(755,root,root) %{_bindir}/opensc-tool
%attr(755,root,root) %{_bindir}/piv-tool
%attr(755,root,root) %{_bindir}/pkcs11-tool
%attr(755,root,root) %{_bindir}/pkcs15-crypt
%attr(755,root,root) %{_bindir}/pkcs15-init
%attr(755,root,root) %{_bindir}/pkcs15-tool
%attr(755,root,root) %{_bindir}/rutoken-tool
%attr(755,root,root) %{_bindir}/westcos-tool
%attr(755,root,root) %{_libdir}/libopensc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopensc.so.3
# PKCS11 modules
%attr(755,root,root) %{_libdir}/onepin-opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11-spy.so
%dir %{_libdir}/pkcs11
%attr(755,root,root) %{_libdir}/pkcs11/onepin-opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11/opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11/pkcs11-spy.so
%dir %{_datadir}/opensc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/opensc.conf
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/opensc/*.profile
%{_mandir}/man1/cardos-tool.1*
%{_mandir}/man1/cryptoflex-tool.1*
%{_mandir}/man1/netkey-tool.1*
%{_mandir}/man1/opensc-explorer.1*
%{_mandir}/man1/opensc-tool.1*
%{_mandir}/man1/pkcs11-tool.1*
%{_mandir}/man1/pkcs15-crypt.1*
%{_mandir}/man1/pkcs15-init.1*
%{_mandir}/man1/pkcs15-tool.1*
%{_mandir}/man1/westcos-tool.1*
%{_mandir}/man5/pkcs15-profile.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopensc.so
%{_libdir}/libopensc.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libopensc.a

%files initramfs
%defattr(644,root,root,755)
%doc README.initramfs
%attr(755,root,root) %{_datadir}/initramfs-tools/hooks/opensc
%attr(755,root,root) %{_datadir}/initramfs-tools/scripts/local-top/opensc
%attr(755,root,root) %{_datadir}/initramfs-tools/scripts/local-bottom/opensc
