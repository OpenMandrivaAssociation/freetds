%define TDSVER	7.0

%define	major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary: 	An OpenSource implementation of the tabular data stream protocol
Name: 		freetds
Version: 	0.82
Release: 	%mkrel 10
License: 	LGPL
Group: 		System/Libraries
URL: 		http://www.freetds.org/
Source0:	http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/%{name}-%{version}.tar.gz
Patch0:		freetds-do_not_build_the_docs.diff
Patch1:		freetds-0.82-libtool.patch
BuildRequires:	doxygen
BuildRequires:	docbook-style-dsssl
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	unixODBC-devel >= 2.0.0
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
FreeTDS is a free (open source) implementation of Sybase's db-lib, ct-lib, and
ODBC libraries. Currently, dblib and ctlib are most mature. Both of these
libraries have several programs know to compile and run against them. ODBC is
just a roughed in skeleton, and not useful for real work.

This package is built with support for TDS version %{TDSVER}.

%package -n	%{libname}
Summary:	An Open Source implementation of the tabular data stream protocol
Group:          System/Libraries
Obsoletes:	%{name}
Provides:	%{name}
# library package contained binaries as well, so obsoleting:
Obsoletes:	%{_lib}freetds_mssql0

%description -n	%{libname}
FreeTDS is a free (open source) implementation of Sybase's db-lib, ct-lib, and
ODBC libraries. Currently, dblib and ctlib are most mature. Both of these
libraries have several programs know to compile and run against them. ODBC is
just a roughed in skeleton, and not useful for real work.

This package is built with support for TDS version %{TDSVER}.

%package -n	%{libname}-unixodbc
Summary:	Driver ODBC for unixODBC
Group:		System/Libraries
Obsoletes:	%{name}-unixodbc
Provides:	%{name}-unixodbc
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{_lib}freetds_mssql0-unixodbc

%description -n	%{libname}-unixodbc
The freetds-unixodbc package contains ODBC driver build for unixODBC.

This package is built with support for TDS version %{TDSVER}.

%package -n	%{develname}
Summary:	Development libraries and header files for the FreeTDS library
Group:		Development/C
Requires:	libtool
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libname}-unixodbc = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}
Provides:	%{name}-devel = %{version}
Provides:	freetds_mssql-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Obsoletes:	%{mklibname %{name} 0 -d}
Obsoletes:	%{_lib}freetds_mssql-devel

%description -n	%{develname}
FreeTDS is a free (open source) implementation of Sybase's db-lib, ct-lib, and
ODBC libraries. Currently, dblib and ctlib are most mature. Both of these
libraries have several programs know to compile and run against them. ODBC is
just a roughed in skeleton, and not useful for real work.

This package is built with support for TDS version %{TDSVER}.

This package allows you to compile applications with freetds libraries.

%package -n	%{libname}-doc
Summary:	User documentation for FreeTDS
Group:		Books/Other
Obsoletes:	%{name}-doc
Provides:	%{name}-doc
Obsoletes:	%{_lib}freetds_mssql0-doc

%description -n	%{libname}-doc
The freetds-doc package contains the useguide and reference of FreeTDS and can
be installed even if FreeTDS main package is not installed

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

# perl path fix
find -type f | xargs perl -pi -e "s|/usr/local/bin/perl|%{_bindir}/perl|g"

# cleanup the initial source
sed -i 's/\r//' doc/tds_ssl.html
sed -i '1 s,#!.*/perl,#!%{__perl},' samples/*.pl doc/api_status.txt

find doc/ samples/ COPYING* -type f -print0 | xargs -0 chmod -x
find . -name "*.[ch]" -print0 | xargs -0 chmod -x

# cause to rebuild docs
rm doc/doc/freetds-%{version}/reference/index.html
rm doc/doc/freetds-%{version}/userguide/index.htm

%build
autoreconf -fis

%configure2_5x \
    --with-tdsver=%{TDSVER} \
    --with-unixodbc=%{_prefix}

%make
# DOCBOOK_DSL="`rpm -ql docbook-style-dsssl | grep html/docbook.dsl`"

# (oe) the test suite assumes you have access to a sybase/mssql database 
# server (tds_connect) and have a correct freedts config...
#make check

%install
rm -rf %{buildroot}

install -d %{buildroot}/interfaces
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}-%{version}/samples
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5

%makeinstall

install -m0644 include/tdsconvert.h %{buildroot}%{_includedir}/
install -m0644 include/tds.h %{buildroot}%{_includedir}/
install -m0644 include/tdsver.h %{buildroot}%{_includedir}/

install -m0644 doc/*.1 %{buildroot}%{_mandir}/man1/
install -m0644 doc/*.5 %{buildroot}%{_mandir}/man5/
 
chmod +x %{buildroot}%{_libdir}/*.so
cp -a -f samples/* %{buildroot}%{_datadir}/%{name}-%{version}/samples/

mv %{buildroot}/interfaces %{buildroot}%{_datadir}/%{name}-%{version}/

pushd %{buildroot}%{_sysconfdir}/%{name}
    ln -sf ../..%{_datadir}/%{name}-%{version}/interfaces/
popd

#remove unwanted files
rm -rf %{buildroot}%{_sysconfdir}/locales.conf
rm -rf %{buildroot}%{_docdir}/%{name}-*

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname}-unixodbc -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname}-unixodbc -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING ChangeLog INSTALL NEWS README PWD
%config(noreplace) %{_sysconfdir}/freetds.conf
%config(noreplace) %{_sysconfdir}/pool.conf
%dir %{_datadir}/%{name}-%{version}
%{_bindir}/bsqldb
%{_bindir}/bsqlodbc
%{_bindir}/datacopy
%{_bindir}/defncopy
%{_bindir}/fisql
%{_bindir}/freebcp
%{_bindir}/osql
%{_bindir}/tdspool
%{_bindir}/tsql
%{_libdir}/libct.so.*
%{_libdir}/libsybdb.so.*
%{_datadir}/%{name}-%{version}/interfaces
%dir %{_sysconfdir}/%{name}/interfaces
%{_mandir}/man1/*
%{_mandir}/man5/*

%files  -n %{libname}-unixodbc
%defattr(-,root,root)
%{_libdir}/libtdsodbc.so.*

%files  -n %{develname}
%defattr(-,root,root)
%doc TODO
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_datadir}/%{name}-%{version}/samples

%files -n %{libname}-doc
%defattr (-,root,root)
%doc doc/images doc/doc/freetds-*/userguide doc/doc/freetds-*/reference
