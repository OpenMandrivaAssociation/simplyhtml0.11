%define gcj_support 1
%define section free

Name:           simplyhtml0.11
Version:        0.11
Release:        4
Epoch:          0
Summary:        Application and a java component for rich text processing
License:        GPL
Group:          Development/Java
URL:            http://www.lightdev.com/page/3.htm
Source0:        http://www.lightdev.com/dload/shtm_r.zip
Source1:        simplyhtml0.11-manifest.mf
Requires:       javahelp2
BuildRequires:  javahelp2
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild

%description
SimplyHTML is an application and a java component for rich text
processing. It stores documents as HTML files in combination with
Cascading Style Sheets (CSS). SimplyHTML is not intended to be used
as an editor for web pages.

%package javadoc
Summary:        Javadoc documentation for %{name}
Group:          Development/Java

%description javadoc
Javadoc documentation for %{name}.

%prep
%setup -q -c
%{__perl} -pi -e 's/\r$//g' gpl.txt readme.txt
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}
%{__ln_s} $(build-classpath javahelp2) jhall.jar
%{__mkdir_p} api

%build
cd src
export CLASSPATH=$(build-classpath javahelp2)
%{javac} `%{_bindir}/find . -name '*.java'`
%{jar} cvfm ../SimplyHTML0.11.jar %{SOURCE1} `%{_bindir}/find . ! -type d ! -name '*.java' -a ! -name package.html -a ! -name Thumbs.db -a ! -name '*.css'`
%{jar} i ../SimplyHTML0.11.jar
%{javadoc} -d ../api `%{_bindir}/find . -name '*.java'`
%{__rm} -r ../api/com/sun
cd ..

%install
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a SimplyHTML0.11.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/SimplyHTML0.11-%{version}.jar
%{__ln_s} SimplyHTML0.11-%{version}.jar %{buildroot}%{_javadir}/SimplyHTML0.11.jar

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc Help.pdf gpl.txt readme.txt
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Tue Sep 08 2009 Thierry Vignaud <tvignaud@mandriva.com> 0:0.11-0.0.3mdv2010.0
+ Revision: 433815
- rebuild

* Tue Feb 05 2008 David Walluck <walluck@mandriva.org> 0:0.11-0.0.2mdv2008.1
+ Revision: 162837
- remove jars before build

* Tue Feb 05 2008 David Walluck <walluck@mandriva.org> 0:0.11-0.0.1mdv2008.1
+ Revision: 162836
- import simplyhtml0.11


