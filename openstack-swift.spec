%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-swift
Version:          1.4.0
Release:          2%{?dist}
Summary:          OpenStack Object Storage (swift)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/swift
Source0:          http://launchpad.net/swift/diablo/1.4.0/+download/swift-%{version}.tar.gz
Source1:          %{name}-functions
Source2:          %{name}-account.init
Source3:          %{name}-auth.init
Source4:          %{name}-container.init
Source5:          %{name}-object.init
Source6:          %{name}-proxy.init
Source20:         %{name}.tmpfs
BuildRoot:        %{_tmppath}/swift-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    dos2unix
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-netifaces

Requires:         python-configobj
Requires:         python-eventlet >= 0.9.8
Requires:         python-greenlet >= 0.3.1
Requires:         python-paste-deploy
Requires:         python-simplejson
Requires:         python-webob >= 0.9.8
Requires:         pyxattr

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils

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

%package          auth
Summary:          A swift auth server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      auth
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} auth server.

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

BuildRequires:    python-sphinx >= 1.0
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

%build
%{__python} setup.py build
# Fails unless we create the build directory
mkdir -p doc/build
# Build docs
%{__python} setup.py build_sphinx
# Fix hidden-file-or-dir warning 
rm doc/build/html/.buildinfo

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Init helper functions
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_datarootdir}/%{name}/functions
# Init scripts
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-account
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-auth
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-container
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-object
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/%{name}-proxy
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test
# Misc other
install -d -m 755 %{buildroot}%{_sysconfdir}/swift
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/account-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/auth-server
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
/sbin/chkconfig --add swift-account

%preun account
if [ $1 = 0 ] ; then
    /sbin/service swift-account stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-account
fi

%postun account
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-account condrestart >/dev/null 2>&1 || :
fi

%post auth
/sbin/chkconfig --add swift-auth

%preun auth
if [ $1 = 0 ] ; then
    /sbin/service swift-auth stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-auth
fi

%postun auth
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-auth condrestart >/dev/null 2>&1 || :
fi

%post container
/sbin/chkconfig --add swift-container

%preun container
if [ $1 = 0 ] ; then
    /sbin/service swift-container stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-container
fi

%postun container
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-container condrestart >/dev/null 2>&1 || :
fi

%post object
/sbin/chkconfig --add swift-object

%preun object
if [ $1 = 0 ] ; then
    /sbin/service swift-object stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-object
fi

%postun object
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-object condrestart >/dev/null 2>&1 || :
fi

%post proxy
/sbin/chkconfig --add swift-proxy

%preun proxy
if [ $1 = 0 ] ; then
    /sbin/service swift-proxy stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-proxy
fi

%postun proxy
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-proxy condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%config(noreplace) %{_sysconfdir}/tmpfiles.d/openstack-swift.conf
%dir %{_datarootdir}/%{name}/functions
%dir %{_sysconfdir}/swift
%dir %{python_sitelib}/swift
%{_bindir}/st
%{_bindir}/swift-account-audit
%{_bindir}/swift-bench
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-log-stats-collector
%{_bindir}/swift-log-uploader
%{_bindir}/swift-ring-builder
%{_bindir}/swift-stats-populate
%{_bindir}/swift-stats-report
%{_bindir}/swift-dispersion-populate
%{_bindir}/swift-dispersion-report
%{python_sitelib}/swift/*.py*
%{python_sitelib}/swift/common
%{python_sitelib}/swift/stats
%{python_sitelib}/swift-%{version}-*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%dir %{_initrddir}/%{name}-account
%dir %{_sysconfdir}/swift/account-server
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server
%{_bindir}/swift-account-stats-logger
%{python_sitelib}/swift/account

%files auth
%defattr(-,root,root,-)
%dir %{_initrddir}/%{name}-auth
%dir %{_sysconfdir}/swift/auth-server
%{_bindir}/swauth-*
#%{python_sitelib}/swift/auth

%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%dir %{_initrddir}/%{name}-container
%dir %{_sysconfdir}/swift/container-server
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-updater
%{_bindir}/swift-container-stats-logger
%{python_sitelib}/swift/container

%files object
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample etc/rsyncd.conf-sample
%dir %{_initrddir}/%{name}-object
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
%dir %{_initrddir}/%{name}-proxy
%dir %{_sysconfdir}/swift/proxy-server
%{_bindir}/swift-proxy-server
%{python_sitelib}/swift/proxy

%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html

%changelog
* Tue Aug 23 2011 David Nalley <david@gnsa.us> - 1.4.0-2
- adding uid:gid for bz 732693

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
