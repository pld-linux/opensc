Summary:	OpenSC library - for accessing SmartCard devices using PC/SC Lite
Summary(pl.UTF-8):	Biblioteka OpenSC - do korzystania z kart procesorowych przy użyciu PC/SC Lite
Name:		opensc
Version:	0.11.6
Release:	2
Epoch:		0
License:	LGPL v2.1+
Group:		Applications
Source0:	http://www.opensc-project.org/files/opensc/%{name}-%{version}.tar.gz
# Source0-md5:	a426759f11350c32af2f17a5cd4d5938
Source1:	%{name}-initramfs-hook
Source2:	%{name}-initramfs-local-bottom
Source3:	%{name}-initramfs-local-top
Source4:	%{name}-initramfs-README
URL:		http://www.opensc-project.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
BuildRequires:	libassuan-devel >= 1:0.6.0
BuildRequires:	libltdl-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	openct-devel
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.364
BuildRequires:	zlib-devel
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
Requires:	openct-devel
Requires:	openssl-devel
Requires:	pcsc-lite-devel

%description devel
OpenSC development files.

%description devel -l pl.UTF-8
Pliki dla programistów używających OpenSC.

%package static
Summary:	Static OpenSC libraries
Summary(pl.UTF-8):	Bibloteki statyczne OpenSC
Group:		Development/Tools
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static OpenSC libraries.

%description static -l pl.UTF-8
Statyczne biblioteki OpenSC.

%package -n browser-plugin-opensc
Summary:	OpenSC Signer plugin for Mozilla
Summary(pl.UTF-8):	Wtyczka OpenSC Signer dla Mozilli
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Requires:	pinentry >= 0.7.5-2
Provides:	mozilla-plugin-opensc
Obsoletes:	mozilla-plugin-opensc

%description -n browser-plugin-opensc
OpenSC Signer browser plugin.

Supported browsers: %{browsers}.

%description -n browser-plugin-opensc -l pl.UTF-8
Wtyczka OpenSC Signer dla przeglądarek.

Obsługiwane przeglądarki: %{browsers}.

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
	--enable-openct \
	--enable-nsplugin \
	--enable-pcsc \
	--with-pcsc-provider=%{_libdir}/libpcsclite.so.1 \
	--with-pinentry=/usr/bin/pinentry \
	--with-plugindir=%{_browserpluginsdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_browserpluginsdir} \
	$RPM_BUILD_ROOT%{_datadir}initramfs-tools/{hooks,scripts/local-{bottom,top}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# just install instead of symlinking
%{__rm} $RPM_BUILD_ROOT%{_browserpluginsdir}/opensc-signer.so
mv -f $RPM_BUILD_ROOT%{_libdir}/opensc-signer.so $RPM_BUILD_ROOT%{_browserpluginsdir}

# default config
install etc/opensc.conf $RPM_BUILD_ROOT%{_sysconfdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}initramfs-tools/hooks/opensc
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}initramfs-tools/scripts/local-bottom/opensc
install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}initramfs-tools/scripts/local-top/opensc

# useless (dlopened by *.so)
rm -f $RPM_BUILD_ROOT%{_libdir}/{onepin-opensc,opensc,pkcs11}-*.{a,la} \
	$RPM_BUILD_ROOT%{_libdir}/opensc/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n browser-plugin-opensc
%update_browser_plugins

%postun	-n browser-plugin-opensc
if [ "$1" = "0" ]; then
        %update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc NEWS README doc/nonpersistent/{ChangeLog,wiki.out} doc/html.out/tools.html
%attr(755,root,root) %{_bindir}/cardos-info
%attr(755,root,root) %{_bindir}/cryptoflex-tool
%attr(755,root,root) %{_bindir}/eidenv
%attr(755,root,root) %{_bindir}/netkey-tool
%attr(755,root,root) %{_bindir}/opensc-explorer
%attr(755,root,root) %{_bindir}/opensc-tool
%attr(755,root,root) %{_bindir}/piv-tool
%attr(755,root,root) %{_bindir}/pkcs11-tool
%attr(755,root,root) %{_bindir}/pkcs15-*
%attr(755,root,root) %{_bindir}/rutoken-tool
%attr(755,root,root) %{_libdir}/libopensc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopensc.so.2
%attr(755,root,root) %{_libdir}/libpkcs15init.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpkcs15init.so.2
%attr(755,root,root) %{_libdir}/libscconf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscconf.so.2
# PKCS11 modules
%attr(755,root,root) %{_libdir}/onepin-opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11-spy.so
%dir %{_libdir}/pkcs11
%attr(755,root,root) %{_libdir}/pkcs11/onepin-opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11/opensc-pkcs11.so
%attr(755,root,root) %{_libdir}/pkcs11/pkcs11-spy.so
%dir %{_datadir}/opensc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/opensc/*.profile
%{_mandir}/man1/cardos-info.1*
%{_mandir}/man1/cryptoflex-tool.1*
%{_mandir}/man1/netkey-tool.1*
%{_mandir}/man1/opensc-explorer.1*
%{_mandir}/man1/opensc-tool.1*
%{_mandir}/man1/pkcs11-tool.1*
%{_mandir}/man1/pkcs15-*.1*
%{_mandir}/man5/pkcs15-profile.5*

%files devel
%defattr(644,root,root,755)
%doc doc/html.out/api.html
%attr(755,root,root) %{_bindir}/opensc-config
%attr(755,root,root) %{_libdir}/libopensc.so
%attr(755,root,root) %{_libdir}/libpkcs15init.so
%attr(755,root,root) %{_libdir}/libscconf.so
%{_libdir}/libopensc.la
%{_libdir}/libpkcs15init.la
%{_libdir}/libscconf.la
%{_includedir}/opensc
%{_pkgconfigdir}/libopensc.pc
%{_pkgconfigdir}/libpkcs15init.pc
%{_pkgconfigdir}/libscconf.pc
%{_mandir}/man1/opensc-config.1*
%{_mandir}/man3/sc_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libopensc.a
%{_libdir}/libpkcs15init.a
%{_libdir}/libscconf.a

%files -n browser-plugin-opensc
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/opensc-signer.so

%files initramfs
%defattr(644,root,root,755)
%doc README.initramfs
%attr(755,root,root) %{_datadir}/initramfs-tools/hooks/opensc
%attr(755,root,root) %{_datadir}/initramfs-tools/scripts/local-top/opensc
%attr(755,root,root) %{_datadir}/initramfs-tools/scripts/local-bottom/opensc
