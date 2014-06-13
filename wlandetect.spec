Summary: 	Simple wireless roaming daemon
Name: 		wlandetect
Version: 	0.3
Release: 	14
License: 	GPL
Group: 		System/Configuration/Networking
URL: 		http://jelmer.vernstok.nl/oss/wlandetect/
Source: 	%{name}-%{version}.tar.bz2
Patch1:		wlandetect-init.d.patch
Patch2:		wlandetect-pid.patch
BuildArch:	noarch
Requires:	wireless-tools
Buildroot: 	%{_tmppath}/%{name}-%{version}-buildroot

%description
Wlandetect is a very simple Perl script that checks which access points and
other peers can be reached and executes some commands based on what it has
found. It is very useful if you often switch between various wireless
environments.

%prep

%setup -q
%patch1 -p0 -b .init
%patch2 -p0 -b .pid

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_mandir}/man8
cp wlandetect.8 %{buildroot}/%{_mandir}/man8
mkdir -p %{buildroot}/%{_sbindir}
cp wlandetect %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
perl -p -e 's,/usr/local/sbin,%{_sbindir},g' %{name}-init.d > %{buildroot}/%{_sysconfdir}/rc.d/init.d/%{name}
echo "# FORMAT: ESSID<tab><tab>commands" > %{buildroot}/%{_sysconfdir}/wlandetect.conf
echo "# use @DEV@ for device name" >>  %{buildroot}/%{_sysconfdir}/wlandetect.conf
echo "default		/sbin/iwconfig @DEV@ essid any key ""; /sbin/ifup @DEV@; dhclient @DEV@" >> %{buildroot}/%{_sysconfdir}/wlandetect.conf
echo "linksys		/sbin/iwconfig @DEV@ essid any key ""; /sbin/ifup @DEV@; dhclient @DEV@" >> %{buildroot}/%{_sysconfdir}/wlandetect.conf

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README wlandetect.conf.example
%{_sbindir}/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/wlandetect.conf
%{_mandir}/man8/*




%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3-9mdv2011.0
+ Revision: 670811
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3-8mdv2011.0
+ Revision: 608169
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3-7mdv2010.1
+ Revision: 524315
- rebuilt for 2010.1

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.3-6mdv2009.0
+ Revision: 225926
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-5mdv2008.1
+ Revision: 179682
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3-4mdv2007.1
+ Revision: 145414
- Import wlandetect

* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3-4mdv2007.1
- use the %%mrel macro
- bunzip patches

* Tue Aug 23 2005 Leonardo Chiquitto Filho <chiquitto@mandriva.com> 0.3-3mdk
- add chkconfig required fields to init.d/wlandetect (patch1), fixes #17247
- patch the script to create a var/run/wlandetect.pid, and use it when
  starting/stoping the service
- change init.d/wlandetect modes to 0755

* Wed May 18 2005 Olivier Blin <oblin@mandriva.com> 0.3-2mdk
- fix service: fix path, and enable it (#16021)

* Wed Aug 11 2004 Austin Acton <austin@mandrake.org> 0.3-1mdk
- initial package

