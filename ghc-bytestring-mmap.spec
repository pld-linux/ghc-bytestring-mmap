#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	bytestring-mmap
Summary:	mmap support for strict ByteStrings
Summary(pl.UTF-8):	Obsługa mmap dla ścisłych ByteStringów
Name:		ghc-%{pkgname}
Version:	0.2.2
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/bytestring-mmap
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	deabf8e1b20aed80b03e8b4dc44182ac
URL:		http://hackage.haskell.org/package/bytestring-mmap
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base < 6
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-unix
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-prof < 6
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-unix-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base < 6
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-unix
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library provides a wrapper to mmap(2), allowing files or devices
to be lazily loaded into memory as strict or lazy ByteStrings, using
the virtual memory subsystem to do on-demand loading.

%description -l pl.UTF-8
Ta biblioteka dostarcza obudowanie mmap(2), pozwalające na leniwe
wczytywanie plików lub urządzeń do pamięci jako ścisłe lub leniwe
łańcuchy bajtów (typ ByteString), przy użyciu podsystemu pamięci
wirtualnej w celu wczytywania na żądanie.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-base-prof < 6
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-unix-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbytestring-mmap-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbytestring-mmap-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbytestring-mmap-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/include
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Posix
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Posix/MMap.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Posix/MMap.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Posix/MMap
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Posix/MMap/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Posix/MMap/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbytestring-mmap-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Posix/MMap.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Posix/MMap/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
