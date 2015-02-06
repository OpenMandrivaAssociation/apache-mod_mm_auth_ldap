#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_mm_auth_ldap
%define mod_conf A31_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	LDAP Authentication module for Apache 2.x
Name:		apache-%{mod_name}
Version:	3.11
Release:	18
Group:		System/Servers
License:	GPL
URL:		http://www.muquit.com/muquit/software/mod_auth_ldap/mod_auth_ldap.html
Source0:	http://www.muquit.com/muquit/software/mod_auth_ldap/mm_mod_auth_ldap%{version}.tar.bz2
Source1:	%{mod_conf}
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	ghthash-devel
Requires:	openldap
Requires:	apache-mod_ssl
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	file

%description
LDAP Authentication module for Apache 2.x

%prep

%setup -q -n mm_mod_auth_ldap%{version}
cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# fix attribs
find . -type f|xargs chmod 644
find . -type d|xargs chmod 755

# unless renaming this it will conflict on file level with apache-mod_ldap-2.0.54
mv mm_mod_auth_ldap.c mod_mm_auth_ldap.c
perl -pi -e "s|mm_mod_auth_ldap\.c|mod_mm_auth_ldap\.c|g" mod_mm_auth_ldap.c

# possible symbol clah fix
perl -pi -e "s|mod_auth_ldap|mod_mm_auth_ldap|g" mod_mm_auth_ldap.c

%build

%{_bindir}/apxs -c \
    -DSTDC_HEADERS=1 -DHAVE_SYS_TYPES_H=1 -DHAVE_SYS_STAT_H=1 -DHAVE_STDLIB_H=1 -DHAVE_STRING_H=1 \
    -DHAVE_MEMORY_H=1 -DHAVE_STRINGS_H=1 -DHAVE_INTTYPES_H=1 -DHAVE_STDINT_H=1 -DHAVE_UNISTD_H=1 \
    -DHAVE_STRING_H=1 -DHAVE_STRINGS_H=1 -DHAVE_MEMORY_H=1 -DHAVE_MALLOC_H=1 -DHAVE_UNISTD_H=1 \
    -DHAVE_CTYPE_H=1 -DHAVE_SYS_TYPES_H=1 -DHAVE_STDLIB_H=1 -DHAVE_SOCKET=1 -DHAVE_HTONL=1 \
    -DHAVE_GETHOSTNAME=1 -DHAVE_GETHOSTBYADDR=1 -DHAVE_YP_GET_DEFAULT_DOMAIN=1 -DHAVE_LIBNSL=1 \
    -DHAVE_RES_SEARCH=1 -DHAVE_LIBRESOLV=1 -DHAVE_INET_ATON=1 -DHAVE_DN_SKIPNAME=1 -DWITH_APACHE_22=1 \
    -DWITH_APACHE_2=1 -DHAVE_LDAP=1 -DHAVE_LDAP_START_TLS_S=1 -DHAVE_LDAP_INITIALIZE=1 \
    -I%{_includedir} -L%{_libdir} -lghthash -lldap -llber -lresolv -lnsl mod_mm_auth_ldap.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc README* cache_group.* inst_cacert.pl
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 3.11-17mdv2012.0
+ Revision: 772690
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 3.11-16
+ Revision: 678349
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3.11-15mdv2011.0
+ Revision: 588034
- rebuild

* Fri Apr 23 2010 Funda Wang <fwang@mandriva.org> 3.11-14mdv2010.1
+ Revision: 538090
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 3.11-13mdv2010.1
+ Revision: 516152
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 3.11-12mdv2010.0
+ Revision: 406623
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 3.11-11mdv2009.1
+ Revision: 326163
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 3.11-10mdv2009.0
+ Revision: 235058
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.11-9mdv2009.0
+ Revision: 215610
- fix rebuild
- fix buildroot

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 3.11-8mdv2008.1
+ Revision: 182827
- rebuild

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 3.11-7mdv2008.1
+ Revision: 137502
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 25 2007 Antoine Ginies <aginies@mandriva.com> 3.11-6mdv2008.0
+ Revision: 92791
- re-submit to fix lost in space i586 package

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 3.11-5mdv2008.0
+ Revision: 82628
- rebuild

* Mon Jul 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 3.11-4mdv2008.0
+ Revision: 52593
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 3.11-3mdv2007.1
+ Revision: 140584
- rebuild

* Wed Feb 28 2007 Oden Eriksson <oeriksson@mandriva.com> 3.11-2mdv2007.1
+ Revision: 127028
- fix deps

* Wed Dec 13 2006 Oden Eriksson <oeriksson@mandriva.com> 3.11-1mdv2007.1
+ Revision: 96223
- sync sources
- 3.11
- drop redundant patches

* Thu Nov 16 2006 Oden Eriksson <oeriksson@mandriva.com> 3.07-1mdv2007.1
+ Revision: 84852
- 3.07
- rediffed P1
- rebuild
- Import apache-mod_mm_auth_ldap

* Mon Jul 03 2006 Oden Eriksson <oeriksson@mandriva.com> 3.05-6mdv2007.0
- rebuild

* Tue Jun 13 2006 Oden Eriksson <oeriksson@mandriva.com> 3.05-5mdv2007.0
- rebuilt against libghthash-0.6.0

* Mon Dec 12 2005 Oden Eriksson <oeriksson@mandriva.com> 3.05-4mdk
- rebuilt against apache-2.2.0

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 3.05-3mdk
- rebuilt to provide a -debug package too

* Mon Oct 17 2005 Oden Eriksson <oeriksson@mandriva.com> 3.05-2mdk
- rebuilt against correct apr-0.9.7

* Sat Oct 15 2005 Oden Eriksson <oeriksson@mandriva.com> 3.05-1mdk
- rebuilt for apache-2.0.55

* Tue Sep 06 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_3.05-4mdk
- rebuild

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_3.05-3mdk
- rebuilt against new openldap-2.3.6 libs
- fix correct calls to ap_log_rerror in P0 (gb)

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_3.05-2mdk
- fix deps

* Sat Jul 23 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_3.05-1mdk
- initial Mandriva package

