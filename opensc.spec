
Summary:	
Summary(pl):
Name:		opensc
Version:	0.7.0
Release:	1
#License:	
#Group:		Daemons
Source0:	http://www.opensc.org/files/%{name}-%{version}.tar.gz
PreReq:		rc-scripts
Requires:	pcsc-lite
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pcscd is the daemon program for PC/SC Lite. It is a resource manager
that coorinates communications with Smart Card readers and Smart Cards
that are connected to the system. The purpose of PCSC Lite is to
provide a Windows(R) SCard interface in a very small form factor for
communicating to smartcards and readers. PCSC Lite uses the same
winscard api as used under Windows(R)

%description -l pl
pcscd jest demonem dla PC/SC Lite. Jest to zarz±dca zasobów,
koordynuj±cy komunikacjê z czytnikami Smart Card pod³±czonymi do
systemu. Celem PCSC Lite jest udostêpnienie interfejsu zgodnego z
Windows(R) SCard s³u¿±cego do komunikacji z czytnikami kart chipowych.
U¿ywa tego samego API winscard, które jest u¿ywane pod Microsoft[TM]
Windows(R).

%package libs
Summary:	Libraries
Summary(pl):	Bibloteki
Group:		Libraries

%description libs
What is a package w/o his libs?

%description libs -l pl
Bo czym¿e jest pakiet bez swoich bibliotek?

%package devel
Summary:	Development files
Summary(pl):	Pliki dla programistów
Group:		Development/Tools
Requires:	%{name}-libs = %{version}

%description devel
Development files.

%description devel -l pl
Pliki dla programistów.

%package static
Summary:	Static libraries
Summary(pl):	Bibloteki statyczne
Group:		Development/Tools
Requires:	%{name}-devel = %{version}

%description static
Static PSCS libraries.

%description static -l pl
Statyczne biblioteki PCSC.

%prep
%setup -q -a1 -a2

%build
%configure2_13
%{__make}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*
%doc AUTHORS DRIVERS NEWS HELP README SECURITY
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/reader.conf
%attr(755,root,root) %{_sbindir}/pcscd
%attr(755,root,root) %{_bindir}/bundleTool
%attr(755,root,root) %{_bindir}/formaticc
%attr(755,root,root) %{_bindir}/installifd
#%attr(754,root,root) /etc/rc.d/init.d/pcscd
%{_mandir}/man1/bundleTool.1*
%{_mandir}/man8/pcscd.8*

%files libs
%defattr(644,root,root,755)
%{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.so
%{_libdir}/libpcsc*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
