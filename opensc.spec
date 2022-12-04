#
# Conditional build:
%bcond_with	openct		# use OpenCT instead of PC/SC for reader access
%bcond_without	openpace	# OpenPACE support
#
Summary:	OpenSC library - for accessing SmartCard devices using PC/SC Lite
Summary(pl.UTF-8):	Biblioteka OpenSC - do korzystania z kart procesorowych przy użyciu PC/SC Lite
Name:		opensc
Version:	0.23.0
Release:	1
License:	LGPL v2.1+
Group:		Applications
#Source0Download: https://github.com/OpenSC/OpenSC/releases
Source0:	https://github.com/OpenSC/OpenSC/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	35c599e673ae9205550974e2dcbe0825
URL:		https://github.com/OpenSC/OpenSC/wiki
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.10
BuildRequires:	cmocka-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	libltdl-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	libxslt-progs
%{?with_openct:BuildRequires:	openct-devel}
%{?with_openpace:BuildRequires:	openpace-devel >= 0.9}
BuildRequires:	openssl-devel >= 1.1.1
%{!?with_openct:BuildRequires:	pcsc-lite-devel >= 1.8.22}
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	zlib-devel
Requires:	filesystem >= 4.0-28
%{?with_openpace:Requires:	openpace >= 0.9}
%{!?with_openct:Requires:	pcsc-lite-libs >= 1.8.22}
Obsoletes:	browser-plugin-opensc < 0.12
Obsoletes:	mozilla-plugin-opensc < 0.11.0-2
Obsoletes:	opensc-initramfs < 0.12.2-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	%{name} = %{version}-%{release}
Requires:	libltdl-devel
%{?with_openct:Requires:	openct-devel}
Requires:	openssl-devel >= 1.1.1
%{!?with_openct:Requires:	pcsc-lite-devel >= 1.8.22}
Requires:	zlib-devel

%description devel
OpenSC development files.

%description devel -l pl.UTF-8
Pliki dla programistów używających OpenSC.

%package static
Summary:	Static OpenSC library
Summary(pl.UTF-8):	Bibloteka statyczna OpenSC
Group:		Development/Tools
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenSC library.

%description static -l pl.UTF-8
Biblioteka statyczna OpenSC.

%package -n bash-completion-opensc
Summary:	Bash completion for OpenSC commands
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów poleceń OpenSC
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-opensc
Bash completion for OpenSC commands.

%description -n bash-completion-opensc -l pl.UTF-8
Bashowe uzupełnianie parametrów poleceń OpenSC.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--sysconfdir=%{_sysconfdir}/opensc \
	%{?with_openct:--enable-openct --disable-pcsc} \
	%{!?with_openct:--enable-pcsc --disable-openct} \
	%{!?with_openpace:--disable-openpace} \
	--disable-silent-rules \
	--disable-strict \
	--enable-doc \
	--with-completiondir=%{bash_compdir} \
	--with-pcsc-provider=%{_libdir}/libpcsclite.so.1

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_libdir}/pkcs11}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	xdg_autostartdir=/etc/xdg/autostart

# not needed (dlopened by soname)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{onepin-opensc-pkcs11,opensc-pkcs11,pkcs11-spy}.la
# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{opensc,smm-local}.la

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README doc/tools/tools.html
%attr(755,root,root) %{_bindir}/cardos-tool
%attr(755,root,root) %{_bindir}/cryptoflex-tool
%attr(755,root,root) %{_bindir}/dnie-tool
%attr(755,root,root) %{_bindir}/egk-tool
%attr(755,root,root) %{_bindir}/eidenv
%attr(755,root,root) %{_bindir}/gids-tool
%attr(755,root,root) %{_bindir}/goid-tool
%attr(755,root,root) %{_bindir}/iasecc-tool
%attr(755,root,root) %{_bindir}/netkey-tool
%attr(755,root,root) %{_bindir}/npa-tool
%attr(755,root,root) %{_bindir}/openpgp-tool
%attr(755,root,root) %{_bindir}/opensc-asn1
%attr(755,root,root) %{_bindir}/opensc-explorer
%attr(755,root,root) %{_bindir}/opensc-notify
%attr(755,root,root) %{_bindir}/opensc-tool
%attr(755,root,root) %{_bindir}/piv-tool
%attr(755,root,root) %{_bindir}/pkcs11-register
%attr(755,root,root) %{_bindir}/pkcs11-tool
%attr(755,root,root) %{_bindir}/pkcs15-crypt
%attr(755,root,root) %{_bindir}/pkcs15-init
%attr(755,root,root) %{_bindir}/pkcs15-tool
%attr(755,root,root) %{_bindir}/sc-hsm-tool
%attr(755,root,root) %{_bindir}/westcos-tool
%attr(755,root,root) %{_libdir}/libopensc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopensc.so.8
%attr(755,root,root) %{_libdir}/libsmm-local.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsmm-local.so.8
# PKCS11 modules
%attr(755,root,root) %{_libdir}/onepin-opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11-spy.so
%attr(755,root,root) %{_libdir}/pkcs11/onepin-opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11/opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11/pkcs11-spy.so
%dir %{_sysconfdir}/opensc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/opensc/opensc.conf
%dir %{_datadir}/opensc
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/opensc/*.profile
%{_desktopdir}/org.opensc.notify.desktop
/etc/xdg/autostart/pkcs11-register.desktop
%if %{with openpace}
/etc/eac/cvc/DESCHSMCVCA00001
/etc/eac/cvc/DESRCACC100001
%endif
%{_mandir}/man1/cardos-tool.1*
%{_mandir}/man1/cryptoflex-tool.1*
%{_mandir}/man1/dnie-tool.1*
%{_mandir}/man1/egk-tool.1*
%{_mandir}/man1/eidenv.1*
%{_mandir}/man1/gids-tool.1*
%{_mandir}/man1/goid-tool.1*
%{_mandir}/man1/iasecc-tool.1*
%{_mandir}/man1/netkey-tool.1*
%{_mandir}/man1/npa-tool.1*
%{_mandir}/man1/openpgp-tool.1*
%{_mandir}/man1/opensc-asn1.1*
%{_mandir}/man1/opensc-explorer.1*
%{_mandir}/man1/opensc-notify.1*
%{_mandir}/man1/opensc-tool.1*
%{_mandir}/man1/piv-tool.1*
%{_mandir}/man1/pkcs11-register.1*
%{_mandir}/man1/pkcs11-tool.1*
%{_mandir}/man1/pkcs15-crypt.1*
%{_mandir}/man1/pkcs15-init.1*
%{_mandir}/man1/pkcs15-tool.1*
%{_mandir}/man1/sc-hsm-tool.1*
%{_mandir}/man1/westcos-tool.1*
%{_mandir}/man5/opensc.conf.5*
%{_mandir}/man5/pkcs15-profile.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopensc.so
%attr(755,root,root) %{_libdir}/libsmm-local.so
%{_pkgconfigdir}/opensc-pkcs11.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopensc.a

%files -n bash-completion-opensc
%defattr(644,root,root,755)
%{bash_compdir}/cardos-tool
%{bash_compdir}/cryptoflex-tool
%{bash_compdir}/dnie-tool
%{bash_compdir}/egk-tool
%{bash_compdir}/eidenv
%{bash_compdir}/gids-tool
%{bash_compdir}/goid-tool
%{bash_compdir}/iasecc-tool
%{bash_compdir}/netkey-tool
%{bash_compdir}/npa-tool
%{bash_compdir}/openpgp-tool
%{bash_compdir}/opensc-asn1
%{bash_compdir}/opensc-explorer
%{bash_compdir}/opensc-notify
%{bash_compdir}/opensc-tool
%{bash_compdir}/piv-tool
%{bash_compdir}/pkcs11-register
%{bash_compdir}/pkcs11-tool
%{bash_compdir}/pkcs15-crypt
%{bash_compdir}/pkcs15-init
%{bash_compdir}/pkcs15-tool
%{bash_compdir}/sc-hsm-tool
%{bash_compdir}/westcos-tool
