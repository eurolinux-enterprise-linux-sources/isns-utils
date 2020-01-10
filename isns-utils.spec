Name:           isns-utils
Version:        0.93
Release:        5%{?dist}
Summary:        The iSNS daemon and utility programs

Group:          System Environment/Daemons
License:        LGPLv2+
URL:            https://github.com/mikechristie/open-isns
Source0:        https://github.com/cleech/open-isns/releases/download/v0.93/open-isns-%{version}.tar.bz2
Source1:        isnsd.service

Patch1: 0001-use-LDFLAGS.patch

BuildRequires:  openssl-devel automake pkgconfig systemd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%global _hardened_build 1

%description
The iSNS package contains the daemon and tools to setup a iSNS server,
and iSNS client tools. The Internet Storage Name Service (iSNS) protocol
allows automated discovery, management and configuration of iSCSI and
Fibre Channel devices (using iFCP gateways) on a TCP/IP network.

%prep
%setup -q -n open-isns-%{version}
%patch1 -p1


%build
autoconf
autoheader
%{configure}
%{__sed} -i -e 's|-Wall -g -O2|%{optflags}|' Makefile
%{__make} %{?_smp_mflags}


%install
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_mandir}/man8
%{__install} -d %{buildroot}%{_mandir}/man5
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/isns
%{__install} -d %{buildroot}%{_var}/lib
%{__install} -d %{buildroot}%{_var}/lib/isns

%{__install} -p -m 644 etc/isnsd.conf %{buildroot}%{_sysconfdir}/isns/isnsd.conf
%{__install} -p -m 644 etc/isnsdd.conf %{buildroot}%{_sysconfdir}/isns/isnsdd.conf
%{__install} -p -m 644 etc/isnsadm.conf %{buildroot}%{_sysconfdir}/isns/isnsadm.conf

%{__install} -p -m 755 isnsd isnsdd isnsadm isnssetup %{buildroot}%{_sbindir}
%{__install} -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/isnsd.service
%{__install} -p -m 644 doc/isns_config.5 %{buildroot}/%{_mandir}/man5/
%{__install} -p -m 644 doc/isnsd.8 doc/isnsdd.8 doc/isnsadm.8 %{buildroot}/%{_mandir}/man8/


%post
%systemd_post isnsd.service


%postun
%systemd_postun isnsd.service


%preun
%systemd_preun isnsd.service


%triggerun -- isns-utils < 0.91-7
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save isnsd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del isnsd >/dev/null 2>&1 || :
/bin/systemctl try-restart isnsd.service >/dev/null 2>&1 || :


%clean
%{__rm} -rf %{buildroot}

%files
%doc COPYING README
%{_sbindir}/isnsd
%{_sbindir}/isnsadm
%{_sbindir}/isnsdd
%{_sbindir}/isnssetup
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_unitdir}/isnsd.service
%dir %{_sysconfdir}/isns
%dir %{_var}/lib/isns
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/isns/*

%changelog
* Fri Sep 13 2013 Chris Leech <cleech@redhat.com> - 0.93-5
- remove unneeded libssl requirement

* Fri Sep 13 2013 Chris Leech <cleech@redhat.com> - 0.93-4
- set hardened build flag, required for long running processes (isnsd)
- patch makefile to actually use LDFLAGS

* Mon Aug 19 2013 Chris Leech <cleech@redhat.com> - 0.93-3
- rpmlint fixes, cleanup spec to keep building after rpm changes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 10 2012 Chris Leech <cleech@redhat.com> - 0.93-1
- Rebase to 0.93
- Make use of systemd rpm macros for scriptlets, BZ 850174

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Jon Ciesla <limburgher@gmail.com> - 0.91-7
- Migrate to systemd, BZ 789707.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.91-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.91-1
- rebuild with new openssl

* Wed Jan 16 2008 Mike Christie <mchristie@redhat.com> - 0.91-0.0
- first build
