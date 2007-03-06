Summary:	C++ wrapper for cairo - cross Mingw32 version
Summary(pl.UTF-8):	Interfejs C++ do cairo - wersja skrośna dla Mingw32
%define		_realname   cairomm
Name:		crossmingw32-%{_realname}
Version:	1.2.4
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://cairographics.org/releases/%{_realname}-%{version}.tar.gz
# Source0-md5:	5d862facfbd0098c9bae618b61f7c8e6
URL:		http://cairographics.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-cairo >= 1.2.2
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	crossmingw32-cairo >= 1.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
C++ wrapper for cairo (cross mingw32 version).

%description -l pl.UTF-8
Interfejs C++ do cairo (wersja skrośna mingw32).

%package static
Summary:	Static cairomm library (cross mingw32 version)
Summary(pl.UTF-8):	Statyczna biblioteka cairomm (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static cairomm library (cross mingw32 version).

%description static -l pl.UTF-8
Statyczna biblioteka cairomm (wersja skrośna mingw32).

%package dll
Summary:	DLL cairomm library for Windows
Summary(pl.UTF-8):	Biblioteka DLL cairomm dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-cairo-dll >= 1.2.2

%description dll
DLL cairomm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL cairomm dla Windows.

%prep
%setup -q -n %{_realname}-%{version}

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-docs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

rm -rf $RPM_BUILD_ROOT%{_docdir}/libcairomm-1.0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%{_libdir}/libcairomm-1.0.dll.a
%{_libdir}/libcairomm-1.0.la
%dir %{_includedir}/cairomm-1.0
%{_includedir}/cairomm-1.0/*
%{_pkgconfigdir}/cairomm-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcairomm-1.0.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libcairomm-1.0-*.dll
