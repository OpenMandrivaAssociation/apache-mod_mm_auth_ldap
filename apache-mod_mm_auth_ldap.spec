#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_mm_auth_ldap
%define mod_conf A31_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	LDAP Authentication module for Apache 2.x
Name:		apache-%{mod_name}
Version:	3.11
Release:	%mkrel 8
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%{_sbindir}/apxs -c \
    -DSTDC_HEADERS=1 -DHAVE_SYS_TYPES_H=1 -DHAVE_SYS_STAT_H=1 -DHAVE_STDLIB_H=1 -DHAVE_STRING_H=1 \
    -DHAVE_MEMORY_H=1 -DHAVE_STRINGS_H=1 -DHAVE_INTTYPES_H=1 -DHAVE_STDINT_H=1 -DHAVE_UNISTD_H=1 \
    -DHAVE_STRING_H=1 -DHAVE_STRINGS_H=1 -DHAVE_MEMORY_H=1 -DHAVE_MALLOC_H=1 -DHAVE_UNISTD_H=1 \
    -DHAVE_CTYPE_H=1 -DHAVE_SYS_TYPES_H=1 -DHAVE_STDLIB_H=1 -DHAVE_SOCKET=1 -DHAVE_HTONL=1 \
    -DHAVE_GETHOSTNAME=1 -DHAVE_GETHOSTBYADDR=1 -DHAVE_YP_GET_DEFAULT_DOMAIN=1 -DHAVE_LIBNSL=1 \
    -DHAVE_RES_SEARCH=1 -DHAVE_LIBRESOLV=1 -DHAVE_INET_ATON=1 -DHAVE_DN_SKIPNAME=1 -DWITH_APACHE_22=1 \
    -DWITH_APACHE_2=1 -DHAVE_LDAP=1 -DHAVE_LDAP_START_TLS_S=1 -DHAVE_LDAP_INITIALIZE=1 \
    -I%{_includedir} -L%{_libdir} -lghthash -lldap -llber -lresolv -lnsl mod_mm_auth_ldap.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README* cache_group.* inst_cacert.pl
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
