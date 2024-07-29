%define TDSVER 7.4
%define major 0
%define ctmaj 4
%define symaj 5
%define libtdsodbc %mklibname tdsodbc %{major}
%define libct %mklibname ct %{ctmaj}
%define libsybdb %mklibname sybdb %{symaj}
%define devname %mklibname %{name} -d

Summary:	An OpenSource implementation of the tabular data stream protocol
Name:		freetds
Version:	1.4.22
Release:	1
License:	LGPLv2
Group:		System/Libraries
Url:		http://www.freetds.org/
Source0:	ftp://ftp.freetds.org/pub/freetds/stable/%{name}-%{version}.tar.gz

BuildRequires:	docbook-style-dsssl
BuildRequires:	doxygen
BuildRequires:	gettext-devel
#BuildRequires:	gnutls-devel
#BuildRequires:	krb5-devel
BuildRequires:	readline-devel
BuildRequires:	git
BuildRequires:	unixODBC-devel >= 2.0.0
BuildRequires:	pkgconfig(ncurses)
Conflicts:	%{_lib}freetds0 < 0.91-6
BuildSystem:	autotools
BuildOption:	--with-tdsver=%{TDSVER}
BuildOption:	--with-unixodbc=%{_prefix}

%description
FreeTDS is a free (open source) implementation of Sybase's db-lib, ct-lib, and
ODBC libraries. Currently, dblib and ctlib are most mature. Both of these
libraries have several programs know to compile and run against them. ODBC is
just a roughed in skeleton, and not useful for real work.

This package is built with support for TDS version %{TDSVER}.

%package -n	%{libct}
Summary:	An Open Source implementation of the tabular data stream protocol
Group:		System/Libraries
Conflicts:	%{_lib}freetds0 < 0.91-6

%description -n	%{libct}
This package contains a shared library for %{name} and is built with support 
for TDS version %{TDSVER}.

%package -n	%{libsybdb}
Summary:	An Open Source implementation of the tabular data stream protocol
Group:		System/Libraries
Obsoletes:	%{_lib}freetds0 < 0.91-6

%description -n	%{libsybdb}
This package contains a shared library for %{name} and is built with support 
for TDS version %{TDSVER}.

%package -n	%{libtdsodbc}
Summary:	Driver ODBC for unixODBC
Group:		System/Libraries
Obsoletes:	%{_lib}freetds0-unixodbc < 0.91-6

%description -n	%{libtdsodbc}
This package contains the ODBC driver build for unixODBC and is built with 
support for TDS version %{TDSVER}.

%package -n	%{devname}
Summary:	Development libraries and header files for the FreeTDS library
Group:		Development/C
Requires:	%{libtdsodbc} = %{version}-%{release}
Requires:	%{libct} = %{version}-%{release}
Requires:	%{libsybdb} = %{version}-%{release}
Provides:	%{name}-devel = %{version}
Provides:	freetds_mssql-devel = %{version}-%{release}

%description -n	%{devname}
This package allows you to compile applications with freetds libraries and is
built with support for TDS version %{TDSVER}.

%package -n	%{name}-doc
Summary:	User documentation for FreeTDS
Group:		Books/Other
Obsoletes:	%{_lib}freetds0-doc < 0.91-6

%description -n	%{name}-doc
The freetds-doc package contains the useguide and reference of FreeTDS and can
be installed even if FreeTDS main package is not installed

%prep -a
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

# lib64 fix
sed -i -e "s|/lib\b|/%{_lib}|g" configure*

# perl path fix
find -type f | xargs sed -i -e "s|/usr/local/bin/perl|%{_bindir}/perl|g"

# cleanup the initial source
sed -i 's/\r//' doc/tds_ssl.html
sed -i '1 s,#!.*/perl,#!%{__perl},' samples/*.pl doc/api_status.txt

find doc/ samples/ COPYING* -type f -print0 | xargs -0 chmod -x
find . -name "*.[ch]" -print0 | xargs -0 chmod -x

# disable docs
sed -i -e 's#src doc#src#' Makefile.*

%install -p
install -d %{buildroot}/interfaces
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}-%{version}/samples
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5

%install -a
install -m0644 include/freetds/tds.h %{buildroot}%{_includedir}/

install -m0644 doc/*.1 %{buildroot}%{_mandir}/man1/
install -m0644 doc/*.5 %{buildroot}%{_mandir}/man5/

chmod +x %{buildroot}%{_libdir}/*.so
cp -a -f samples/* %{buildroot}%{_datadir}/%{name}-%{version}/samples/

mv %{buildroot}/interfaces %{buildroot}%{_datadir}/%{name}-%{version}/

cd %{buildroot}%{_sysconfdir}/%{name}
ln -sf ../..%{_datadir}/%{name}-%{version}/interfaces/
cd -

#remove unwanted files
rm -rf %{buildroot}%{_sysconfdir}/locales.conf
rm -rf %{buildroot}%{_docdir}/%{name}-*

%files
%doc AUTHORS.md COPYING.txt ChangeLog INSTALL.md NEWS.md README.md
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
%{_datadir}/%{name}-%{version}/interfaces
%{_sysconfdir}/%{name}/interfaces
%{_mandir}/man1/*
%{_mandir}/man5/*

%files  -n %{libtdsodbc}
%{_libdir}/libtdsodbc.so.%{major}*

%files  -n %{libct}
%{_libdir}/libct.so.%{ctmaj}*

%files  -n %{libsybdb}
%{_libdir}/libsybdb.so.%{symaj}*

%files  -n %{devname}
%doc TODO.md
%{_includedir}/*.h
%{_libdir}/*.so
%{_datadir}/%{name}-%{version}/samples

%files -n %{name}-doc
%doc %{_docdir}/%{name}
