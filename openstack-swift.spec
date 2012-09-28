%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-swift
Version:          1.4.8
Release:          2%{?dist}
Summary:          OpenStack Object Storage (swift)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/swift
Source0:          http://launchpad.net/swift/essex/%{version}/+download/swift-%{version}.tar.gz
Source2:          %{name}-account.service
Source21:         %{name}-account@.service
Source4:          %{name}-container.service
Source41:         %{name}-container@.service
Source5:          %{name}-object.service
Source51:         %{name}-object@.service
Source6:          %{name}-proxy.service
Source20:         %{name}.tmpfs
BuildRoot:        %{_tmppath}/swift-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0001: Do-not-use-pickle-for-serialization-in-memcache.patch
Patch0002: Fix-bug-where-serialization_format-is-ignored.patch

BuildArch:        noarch
BuildRequires:    dos2unix
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-netifaces
BuildRequires:    python-paste-deploy
Requires:         python-configobj
Requires:         python-eventlet >= 0.9.8
Requires:         python-greenlet >= 0.3.1
Requires:         python-paste-deploy
Requires:         python-simplejson
Requires:         python-webob >= 0.9.8
Requires:         pyxattr
Requires:         python-setuptools
Requires:         python-netifaces
Requires:         python-netifaces

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(post):   systemd-sysv
Requires(pre):    shadow-utils
Obsoletes:        openstack-swift-auth  <= 1.4.0

%description
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.
Objects are written to multiple hardware devices in the data center, with the
OpenStack software responsible for ensuring data replication and integrity
across the cluster. Storage clusters can scale horizontally by adding new nodes,
which are automatically configured. Should a node fail, OpenStack works to
replicate its content from other active nodes. Because OpenStack uses software
logic to ensure data replication and distribution across different devices,
inexpensive commodity hard drives and servers can be used in lieu of more
expensive equipment.

%package          account
Summary:          A swift account server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      account
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} account server.

%package          container
Summary:          A swift container server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      container
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} container server.

%package          object
Summary:          A swift object server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         rsync >= 3.0

%description      object
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} object server.

%package          proxy
Summary:          A swift proxy server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      proxy
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} proxy server.

%package doc
Summary:          Documentation for %{name}
Group:            Documentation
%if 0%{?rhel} >= 6
BuildRequires:    python-sphinx10 >= 1.0
%endif
%if 0%{?fedora} >= 14
BuildRequires:    python-sphinx >= 1.0
%endif
# Required for generating docs
BuildRequires:    python-eventlet
BuildRequires:    python-simplejson
BuildRequires:    python-webob
BuildRequires:    pyxattr

%description      doc
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains documentation files for %{name}.

%prep
%setup -q -n swift-%{version}
# Fix wrong-file-end-of-line-encoding warning
dos2unix LICENSE

%patch0001 -p1 -z .pickle-memcache
%patch0002 -p1 -z .format-ignored

%build
%{__python} setup.py build
# Fails unless we create the build directory
mkdir -p doc/build
# Build docs
%if 0%{?fedora} >= 14
%{__python} setup.py build_sphinx
%endif
%if 0%{?rhel} >= 6
export PYTHONPATH="$( pwd ):$PYTHONPATH"
SPHINX_DEBUG=1 sphinx-1.0-build -b html doc/source doc/build/html
SPHINX_DEBUG=1 sphinx-1.0-build -b man doc/source doc/build/man
%endif
# Fix hidden-file-or-dir warning 
#rm doc/build/html/.buildinfo

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# systemd units
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-account.service
install -p -D -m 755 %{SOURCE21} %{buildroot}%{_unitdir}/%{name}-account@.service
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}-container.service
install -p -D -m 755 %{SOURCE41} %{buildroot}%{_unitdir}/%{name}-container@.service
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}-object.service
install -p -D -m 755 %{SOURCE51} %{buildroot}%{_unitdir}/%{name}-object@.service
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}-proxy.service
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test
# Misc other
install -d -m 755 %{buildroot}%{_sysconfdir}/swift
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/account-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/container-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/object-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/proxy-server

# Swift run directories
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -p -m 0644 %{SOURCE20} %{buildroot}%{_sysconfdir}/tmpfiles.d/openstack-swift.conf

%clean
rm -rf %{buildroot}

%pre
getent group swift >/dev/null || groupadd -r swift -g 160
getent passwd swift >/dev/null || \
useradd -r -g swift -u 160 -d %{_sharedstatedir}/swift -s /sbin/nologin \
-c "OpenStack Swift Daemons" swift
exit 0

%post account
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun account
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable openstack-swift-account.service > /dev/null 2>&1 || :
    /bin/systemctl stop openstack-swift-account.service > /dev/null 2>&1 || :
fi

%postun account
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart openstack-swift-account.service >/dev/null 2>&1 || :
fi

%triggerun -- openstack-swift-account < 1.4.5-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply openstack-swift-account
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openstack-swift-account >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del openstack-swift-account >/dev/null 2>&1 || :
/bin/systemctl try-restart openstack-swift-account.service >/dev/null 2>&1 || :

%post container
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun container
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable openstack-swift-container.service > /dev/null 2>&1 || :
    /bin/systemctl stop openstack-swift-container.service > /dev/null 2>&1 || :
fi

%postun container
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart openstack-swift-container.service >/dev/null 2>&1 || :
fi

%triggerun -- openstack-swift-container < 1.4.5-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply openstack-swift-container
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openstack-swift-container >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del openstack-swift-container >/dev/null 2>&1 || :
/bin/systemctl try-restart openstack-swift-container.service >/dev/null 2>&1 || :

%post object
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun object
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable openstack-swift-object.service > /dev/null 2>&1 || :
    /bin/systemctl stop openstack-swift-object.service > /dev/null 2>&1 || :
fi

%postun object
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart openstack-swift-object.service >/dev/null 2>&1 || :
fi

%triggerun -- openstack-swift-object < 1.4.5-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply openstack-swift-object
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openstack-swift-object >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del openstack-swift-object >/dev/null 2>&1 || :
/bin/systemctl try-restart openstack-swift-object.service >/dev/null 2>&1 || :


%post proxy
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun proxy
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable openstack-swift-proxy.service > /dev/null 2>&1 || :
    /bin/systemctl stop openstack-swift-proxy.service > /dev/null 2>&1 || :
fi

%postun proxy
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart openstack-swift-proxy.service >/dev/null 2>&1 || :
fi

%triggerun -- openstack-swift-proxy < 1.4.5-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply openstack-swift-proxy
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openstack-swift-proxy >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del openstack-swift-proxy >/dev/null 2>&1 || :
/bin/systemctl try-restart openstack-swift-proxy.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%doc etc/dispersion.conf-sample etc/drive-audit.conf-sample etc/object-expirer.conf-sample
%doc etc/swift.conf-sample
%config(noreplace) %{_sysconfdir}/tmpfiles.d/openstack-swift.conf
%dir %{_sysconfdir}/swift
%dir %{python_sitelib}/swift
%{_bindir}/swift
%{_bindir}/swift-account-audit
%{_bindir}/swift-bench
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-ring-builder
%{_bindir}/swift-dispersion-populate
%{_bindir}/swift-dispersion-report
%{_bindir}/swift-recon*
%{_bindir}/swift-object-expirer
%{_bindir}/swift-oldies
%{_bindir}/swift-orphans
%{_bindir}/swift-form-signature
%{_bindir}/swift-temp-url
%{python_sitelib}/swift/*.py*
%{python_sitelib}/swift/common
%{python_sitelib}/swift-%{version}-*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%dir %{_unitdir}/%{name}-account.service
%dir %{_unitdir}/%{name}-account@.service
%dir %{_sysconfdir}/swift/account-server
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server
%{python_sitelib}/swift/account


%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%dir %{_unitdir}/%{name}-container.service
%dir %{_unitdir}/%{name}-container@.service
%dir %{_sysconfdir}/swift/container-server
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-updater
%{_bindir}/swift-container-sync
%{python_sitelib}/swift/container

%files object
%defattr(-,root,root,-)
%doc etc/object-server.conf-sample etc/rsyncd.conf-sample
%dir %{_unitdir}/%{name}-object.service
%dir %{_unitdir}/%{name}-object@.service
%dir %{_sysconfdir}/swift/object-server
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-info
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-server
%{_bindir}/swift-object-updater
%{python_sitelib}/swift/obj

%files proxy
%defattr(-,root,root,-)
%doc etc/proxy-server.conf-sample
%dir %{_unitdir}/%{name}-proxy.service
%dir %{_sysconfdir}/swift/proxy-server
%{_bindir}/swift-proxy-server
%{python_sitelib}/swift/proxy

%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html

%changelog
* Thu Sep 27 2012 Derek Higgins <derekh@redhat.com> - 1.4.8-2
- Do not use pickle for serialization in memcache 

* Thu Mar 22 2012 Alan Pevec <apevec@redhat.com> 1.4.8-1
- Update to 1.4.8

* Fri Mar 09 2012 Alan Pevec <apevec@redhat.com> 1.4.7-1
- Update to 1.4.7

* Mon Feb 13 2012 Alan Pevec <apevec@redhat.com> 1.4.6-1
- Update to 1.4.6
- Switch from SysV init scripts to systemd units rhbz#734594

* Thu Jan 26 2012 Alan Pevec <apevec@redhat.com> 1.4.5-1
- Update to 1.4.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Alan Pevec <apevec@redhat.com> 1.4.4-1
- Update to 1.4.4

* Wed Nov 23 2011 David Nalley <david@gnsa.us> -1.4.3-2
* fixed some missing requires

* Sat Nov 05 2011 David Nalley <david@gnsa.us> - 1.4.3-1
- Update to 1.4.3
- fix init script add, registration, deletion BZ 685155
- fixing BR to facilitate epel6 building

* Tue Aug 23 2011 David Nalley <david@gnsa.us> - 1.4.0-2
- adding uid:gid for bz 732693

* Wed Jun 22 2011 David Nalley <david@gnsa.us> - 1.4.1-1
- Update to 1.4.0
- change the name of swift binary from st to swift

* Sat Jun 04 2011 David Nalley <david@gnsa.us> - 1.4.0-1
- Update to 1.4.0

* Fri May 20 2011 David Nalley <david@gnsa.us> - 1.3.0-1
- Update to 1.3.0 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 05 2010 Silas Sewell <silas@sewell.ch> - 1.1.0-1
- Update to 1.1.0

* Sun Aug 08 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-5
- Update for new Python macro guidelines
- Use dos2unix instead of sed
- Make gecos field more descriptive

* Wed Jul 28 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-4
- Rename to openstack-swift

* Wed Jul 28 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-3
- Fix return value in swift-functions

* Tue Jul 27 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-2
- Add swift user
- Update init scripts

* Sun Jul 18 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-1
- Initial build
