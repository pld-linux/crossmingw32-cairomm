Summary:	C++ wrapper for cairo - cross Mingw32 version
Summary(pl.UTF-8):	Interfejs C++ do cairo - wersja skrośna dla Mingw32
%define		_realname   cairomm
Name:		crossmingw32-%{_realname}
Version:	1.2.4
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://cairographics.org/releases/%{_realname}-%{version}.tar.gz
# Source0-md5:	5d862facfbd0098c9bae618b61f7c8e6
Patch0:		%{name}-noexamples.patch
URL:		http://cairographics.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-cairo >= 1.2.2
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-pkgconfig
BuildRequires:	libtool >= 2:1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
C++ wrapper for cairo.

%description -l pl.UTF-8
Interfejs C++ do cairo.

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1
#rm -rf examples

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
#	--enable-shared \
#	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_docdir}/libcairomm-1.0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%{_libdir}/*.la
%{_libdir}/*.a
%{_bindir}/*.dll
%dir %{_includedir}/cairomm-1.0
%{_includedir}/cairomm-1.0/*
%{_pkgconfigdir}/cairomm-1.0.pc
