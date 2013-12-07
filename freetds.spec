%define TDSVER	7.0
%define	major	0
%define	ctmaj	4
%define	symaj	5
%define	libtdsodbc	%mklibname tdsodbc %{major}
%define	libct		%mklibname ct %{ctmaj}
%define	libsybdb	%mklibname sybdb %{symaj}
%define devname 	%mklibname %{name} -d

Summary:	An OpenSource implementation of the tabular data stream protocol
Name:		freetds
Version:	0.92.63
Release:	2
License:	LGPLv2
Group:		System/Libraries
Url:		http://www.freetds.org/
Source0:	http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/git/%{name}-%{version}.tar.bz2
Patch0:		freetds-do_not_build_the_docs.diff
Patch1:		freetds-0.82-libtool.patch
Patch2:		freetds-0.91-fmtstr.diff

BuildRequires:	libtool
BuildRequires:	docbook-style-dsssl
BuildRequires:	doxygen
#BuildRequires:	gnutls-devel
#BuildRequires:	krb5-devel
BuildRequires:	readline-devel
BuildRequires:	unixODBC-devel >= 2.0.0
BuildRequires:	pkgconfig(ncurses)
Conflicts:	%{_lib}freetds0 < 0.91-6

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

%prep
%setup -q
%apply_patches

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
	if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# lib64 fix
sed -i -e "s|/lib\b|/%{_lib}|g" configure*

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

autoreconf -fis

%build
%configure2_5x \
	--with-tdsver=%{TDSVER} \
	--with-unixodbc=%{_prefix} \
	--disable-static
#	--enable-krb5=%{_prefix} \
#	--with-gnutls

%make
# DOCBOOK_DSL="`rpm -ql docbook-style-dsssl | grep html/docbook.dsl`"

# (oe) the test suite assumes you have access to a sybase/mssql database 
# server (tds_connect) and have a correct freedts config...
#make check

%install
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

%files
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
%{_datadir}/%{name}-%{version}/interfaces
%dir %{_sysconfdir}/%{name}/interfaces
%{_mandir}/man1/*
%{_mandir}/man5/*

%files  -n %{libtdsodbc}
%{_libdir}/libtdsodbc.so.%{major}*

%files  -n %{libct}
%{_libdir}/libct.so.%{ctmaj}*

%files  -n %{libsybdb}
%{_libdir}/libsybdb.so.%{symaj}*

%files  -n %{devname}
%doc TODO
%{_includedir}/*.h
%{_libdir}/*.so
%{_datadir}/%{name}-%{version}/samples

%files -n %{name}-doc
%doc doc/images doc/doc/freetds-*/userguide doc/doc/freetds-*/reference


