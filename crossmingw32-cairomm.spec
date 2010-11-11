Summary:	C++ wrapper for cairo - cross MinGW32 version
Summary(pl.UTF-8):	Interfejs C++ do cairo - wersja skrośna dla MinGW32
%define		realname   cairomm
Name:		crossmingw32-%{realname}
Version:	1.8.6
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://cairographics.org/releases/%{realname}-%{version}.tar.gz
# Source0-md5:	39af0fd0c111bb74307f9860653046ce
URL:		http://cairographics.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.10
BuildRequires:	crossmingw32-cairo >= 1.8.0
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-libsigc++ >= 2.0
BuildRequires:	libtool >= 2:1.5
BuildRequires:	mm-common >= 0.8
BuildRequires:	pkgconfig >= 1:0.15
Requires:	crossmingw32-cairo >= 1.8.0
Requires:	crossmingw32-libsigc++ >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
C++ wrapper for cairo (cross MinGW32 version).

%description -l pl.UTF-8
Interfejs C++ do cairo (wersja skrośna MinGW32).

%package static
Summary:	Static cairomm library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka cairomm (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static cairomm library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka cairomm (wersja skrośna MinGW32).

%package dll
Summary:	DLL cairomm library for Windows
Summary(pl.UTF-8):	Biblioteka DLL cairomm dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-cairo-dll >= 1.8.0
Requires:	crossmingw32-libsigc++-dll >= 2.0

%description dll
DLL cairomm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL cairomm dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I build
%{__automake}
%{__autoconf}
%configure \
	--enable-static \
	--target=%{target} \
	--host=%{target}

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

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{doc/cairomm-1.0,devhelp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%{_libdir}/libcairomm-1.0.dll.a
%{_libdir}/libcairomm-1.0.la
%{_libdir}/cairomm-1.0
%{_includedir}/cairomm-1.0
%{_pkgconfigdir}/cairomm-1.0.pc
%{_pkgconfigdir}/cairomm-ft-1.0.pc
%{_pkgconfigdir}/cairomm-pdf-1.0.pc
%{_pkgconfigdir}/cairomm-png-1.0.pc
%{_pkgconfigdir}/cairomm-ps-1.0.pc
%{_pkgconfigdir}/cairomm-svg-1.0.pc
%{_pkgconfigdir}/cairomm-win32-1.0.pc
%{_pkgconfigdir}/cairomm-win32-font-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcairomm-1.0.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libcairomm-1.0-*.dll
