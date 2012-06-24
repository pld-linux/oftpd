Summary:	Yet another anonymous FTP server
Summary(pl):	Kolejny anonimowy serwer FTP
Name:		oftpd
Version:	0.2.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.time-travellers.org/oftpd/%{name}-%{version}.tar.gz
# Source0-md5:	2958164251fd70b9d52de8c184822dec
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-sbindir.patch
URL:		http://www.time-travellers.org/oftpd/
BuildRequires:	autoconf
BuildRequires:	automake
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:	ftpserver
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
Obsoletes:	vsftpd
Obsoletes:	wu-ftpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
oftpd is designed to be as secure as an anonymous FTP server can
possibly be. It runs as non-root for most of the time, and uses the
Unix chroot() command to hide most of the systems directories from
external users -- they cannot change into them even if the server is
totally compromised. It also contains its own directory-change and
directory-listing code (most FTP servers execute the system "ls"
command to list files).

%description -l pl
oftpd jest zaprojektowany �eby by� tak bezpiecznym jak tylko anonimowy
serwer FTP mo�e najprawdopodobniej by�. Dzia�a jako nie-root przez
wi�kszo�� czasu i wykorzystuje Unixowe polecenie chroot() �eby ukry�
wi�kszo�� systemowych katalog�w przed zewn�trznymi u�ytkownikami - nie
mog� si� do nich dosta� nawet je�li serwer zostanie z�amany. Zawiera
te� sw�j w�asny kod do zmiany i listowania katalog�w (wi�kszo��
serwer�w FTP wykorzystuje do tego polecenie systemowe "ls")

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/sysconfig,/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT/home/services/ftp/pub

%{__make} install DESTDIR=$RPM_BUILD_ROOT
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add oftpd
if [ -f /var/lock/subsys/oftpd ]; then
	/etc/rc.d/init.d/oftpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/oftpd start\" to start oftpd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/oftpd ]; then
		/etc/rc.d/init.d/oftpd stop 1>&2
	fi
	/sbin/chkconfig --del oftpd
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README AUTHORS TODO BUGS
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /home/services/ftp
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) /etc/sysconfig/*
