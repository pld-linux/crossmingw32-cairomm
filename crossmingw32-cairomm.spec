Summary:	C++ wrapper for cairo - cross MinGW32 version
Summary(pl.UTF-8):	Interfejs C++ do cairo - wersja skrośna dla MinGW32
%define		realname   cairomm
Name:		crossmingw32-%{realname}
Version:	1.14.2
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	https://www.cairographics.org/releases/%{realname}-%{version}.tar.xz
# Source0-md5:	fbcaad2d3756b42592fe8c92b39945f5
URL:		https://www.cairographics.org/
BuildRequires:	crossmingw32-cairo >= 1.12.0
BuildRequires:	crossmingw32-gcc-c++ >= 1:4.6
BuildRequires:	crossmingw32-libsigc++ >= 2.6.0
BuildRequires:	meson >= 0.50.0
BuildRequires:	mm-common >= 0.8
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	python3 >= 1:3.5
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-cairo >= 1.12.0
Requires:	crossmingw32-gcc-c++ >= 1:4.6
Requires:	crossmingw32-libsigc++ >= 2.6.0
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
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*
%define		filterout_cxx	-f[-a-z0-9=]*

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
Requires:	crossmingw32-cairo-dll >= 1.12.0
Requires:	crossmingw32-libsigc++-dll >= 2.6.0

%description dll
DLL cairomm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL cairomm dla Windows.

%prep
%setup -q -n %{realname}-%{version}

cat > meson-cross.txt <<'EOF'
[host_machine]
system = 'windows'
cpu_family = 'x86'
cpu = 'i386'
endian='little'
[binaries]
c = '%{target}-gcc'
cpp = '%{target}-g++'
ar = '%{target}-ar'
windres = '%{target}-windres'
pkgconfig = 'pkg-config'
[properties]
%ifarch %{ix86}
c_args = ['%(echo %{rpmcflags} | sed -e "s/ \+/ /g;s/ /', '/g")']
%else
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc.
# now at least i486 is required for atomic operations
c_args = ['-O2']
%endif
EOF

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%meson build \
	--cross-file meson-cross.txt

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%{_libdir}/libcairomm-1.0.dll.a
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
%{_dlldir}/libcairomm-1.0-1.dll
