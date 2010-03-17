Summary: 	Simple wireless roaming daemon
Name: 		wlandetect
Version: 	0.3
Release: 	%mkrel 7
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


