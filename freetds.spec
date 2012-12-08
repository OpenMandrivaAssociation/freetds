%define TDSVER	7.0

%define	major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	An OpenSource implementation of the tabular data stream protocol
Name:		freetds
Version:	0.91
Release:	5
License:	LGPL
Group:		System/Libraries
URL:		http://www.freetds.org/
Source0:	http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/%{name}-%{version}.tar.gz
Patch0:		freetds-do_not_build_the_docs.diff
Patch1:		freetds-0.82-libtool.patch
Patch2:		freetds-0.91-fmtstr.diff
BuildRequires:	autoconf automake libtool
BuildRequires:	docbook-style-dsssl
BuildRequires:	doxygen
#BuildRequires:	gnutls-devel
#BuildRequires:	krb5-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	unixODBC-devel >= 2.0.0

%description
FreeTDS is a free (open source) implementation of Sybase's db-lib, ct-lib, and
ODBC libraries. Currently, dblib and ctlib are most mature. Both of these
libraries have several programs know to compile and run against them. ODBC is
just a roughed in skeleton, and not useful for real work.

This package is built with support for TDS version %{TDSVER}.

%package -n	%{libname}
Summary:	An Open Source implementation of the tabular data stream protocol
Group:		System/Libraries
Obsoletes:	%{name} < 0.91
Provides:	%{name}
# library package contained binaries as well, so obsoleting:
Obsoletes:	%{_lib}freetds_mssql0 < 0.91

%description -n	%{libname}
FreeTDS is a free (open source) implementation of Sybase's db-lib, ct-lib, and
ODBC libraries. Currently, dblib and ctlib are most mature. Both of these
libraries have several programs know to compile and run against them. ODBC is
just a roughed in skeleton, and not useful for real work.

This package is built with support for TDS version %{TDSVER}.

%package -n	%{libname}-unixodbc
Summary:	Driver ODBC for unixODBC
Group:		System/Libraries
Obsoletes:	%{name}-unixodbc < 0.91
Provides:	%{name}-unixodbc
Requires:	%{libname} >= %{version}-%{release}
Obsoletes:	%{_lib}freetds_mssql0-unixodbc < 0.91

%description -n	%{libname}-unixodbc
The freetds-unixodbc package contains ODBC driver build for unixODBC.

This package is built with support for TDS version %{TDSVER}.

%package -n	%{develname}
Summary:	Development libraries and header files for the FreeTDS library
Group:		Development/C
Requires:	libtool
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libname}-unixodbc = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}
Provides:	%{name}-devel = %{version}
Provides:	freetds_mssql-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < 0.91
Obsoletes:	%{mklibname %{name} 0 -d} < 0.91
Obsoletes:	%{_lib}freetds_mssql-devel < 0.91

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
Obsoletes:	%{name}-doc < 0.91
Provides:	%{name}-doc
Obsoletes:	%{_lib}freetds_mssql0-doc < 0.91

%description -n	%{libname}-doc
The freetds-doc package contains the useguide and reference of FreeTDS and can
be installed even if FreeTDS main package is not installed

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0

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
    --with-unixodbc=%{_prefix} \
    --disable-static
#    --enable-krb5=%{_prefix} \
#    --with-gnutls

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

%files -n %{libname}
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
%{_libdir}/libtdsodbc.so.*

%files  -n %{develname}
%doc TODO
%{_includedir}/*.h
%{_libdir}/*.so
%{_datadir}/%{name}-%{version}/samples

%files -n %{libname}-doc
%doc doc/images doc/doc/freetds-*/userguide doc/doc/freetds-*/reference


%changelog
* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.91-4
+ Revision: 739191
- rebuilt for new unixODBC (second try)

* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.91-3
+ Revision: 739126
- rebuilt for new unixODBC

* Mon Dec 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.91-2
+ Revision: 737853
- drop the static lib and the libtool *.la file
- various fixes

* Sat Aug 20 2011 Oden Eriksson <oeriksson@mandriva.com> 0.91-1
+ Revision: 695909
- 0.91

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.82-12
+ Revision: 664354
- mass rebuild

* Sun Jan 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.82-11mdv2011.0
+ Revision: 627571
- don't force the usage of automake1.7

* Sat Sep 18 2010 Funda Wang <fwang@mandriva.org> 0.82-10mdv2011.0
+ Revision: 579335
- add missing requires

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.82-9mdv2010.1
+ Revision: 519002
- rebuild

* Thu Sep 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.82-8mdv2010.0
+ Revision: 427840
- added P1 from fedora to fix build (libtool)
- fix build

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

* Wed Feb 25 2009 Thierry Vignaud <tv@mandriva.org> 0.82-7mdv2009.1
+ Revision: 344804
- rebuild for new libreadline

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 0.82-6mdv2009.1
+ Revision: 316559
- rebuild

* Fri Sep 12 2008 Oden Eriksson <oeriksson@mandriva.com> 0.82-5mdv2009.0
+ Revision: 284184
- fix #31665 (Typo in summary and bad source url)

* Tue Jun 17 2008 Anssi Hannula <anssi@mandriva.org> 0.82-4mdv2009.0
+ Revision: 222182
- replace freetds_mssql subpackages

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.82-3mdv2009.0
+ Revision: 207642
- whoops!
- add compat headers

* Thu May 08 2008 Oden Eriksson <oeriksson@mandriva.com> 0.82-2mdv2009.0
+ Revision: 204503
- rebuild
- 0.82
- added P0 to disable building the allready built docs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 04 2007 Oden Eriksson <oeriksson@mandriva.com> 0.64-5mdv2008.0
+ Revision: 79215
- sync with freetds-0.64-7.fc8.src.rpm to make it build the docs
- new devel naming


* Wed Oct 11 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-10 10:38:53 (63317)
- rebuild

* Wed Oct 11 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-10 10:37:57 (63316)
- Import freetds

* Tue Jul 18 2006 Oden Eriksson <oeriksson@mandriva.com> 0.64-2mdv2007.1
- rebuild

* Mon Jul 03 2006 Oden Eriksson <oeriksson@mandriva.com> 0.64-2mdv2007.0
- 0.64 (Major feature enhancements)

* Tue May 16 2006 Oden Eriksson <oeriksson@mandriva.com> 0.64-1.RC2.1mdk
- 0.64RC2

* Fri Oct 21 2005 Oden Eriksson <oeriksson@mandriva.com> 0.64-0.20051020.1mdk
- new snap (20051020)

* Fri Sep 02 2005 Oden Eriksson <oeriksson@mandriva.com> 0.64-0.20050831.1mdk
- used a snap in an attempt to close #17272

* Fri May 06 2005 Oden Eriksson <oeriksson@mandriva.com> 0.63-3mdk
- rebuilt with gcc4

* Sun Apr 10 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.63-2mdk
- added one lib64 fix

* Thu Mar 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.63-1mdk
- 0.63
- use the %%mkrel macro

* Fri Feb 04 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.62.4-5mdk
- rebuilt against new readline

* Mon Jan 03 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.62.4-4mdk
- fix deps

* Mon Jan 03 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.62.4-3mdk
- libifiction (why hasn't this been done before?)

* Wed Jul 14 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.62.4-2mdk
- make it compile on 10.0 too

* Sat Jul 03 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.62.4-1mdk
- 0.62.4

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.62.3-2mdk
- rebuild

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.62.3-1mdk
- 0.62.3
- merge spec file stuff from the provided spec file
- fix deps
- misc spec file fixes

