%global eclipse_base        %{_libdir}/eclipse
%global install_loc         %{_datadir}/eclipse/dropins
# Taken from update site so we match upstream
#  http://download.eclipse.org/mylyn/archive/3.5.1/v20110422-0200/
%global qualifier           v20110422-0200

Name: eclipse-mylyn-commons
Summary: Common libraries for Eclipse Mylyn
Version: 3.5.1
Release: 3
License: EPL and ASL 2.0
URL: http://www.eclipse.org/mylyn

# bash fetch-eclipse-mylyn-commons.sh
Source0: eclipse-mylyn-commons-R_3_5_1-fetched-src.tar.bz2
Source1: fetch-eclipse-mylyn-commons.sh

# Would require axis2+OSGi info. Remove once
# https://bugzilla.redhat.com/show_bug.cgi?id=497126
# is resolved.
Patch0: %{name}-nosoap.patch
# Not sure if this would be suitable for upstream?
# It changes the Bundle-Require header to
# Import-Package
Patch1: %{name}-xmlrpc-import-package-manifest-fix.patch

BuildArch: noarch

BuildRequires: java-devel >= 1.5.0
BuildRequires: jpackage-utils
BuildRequires: eclipse-pde >= 0:3.4.0
BuildRequires: apache-commons-lang >= 2.3-2.3
BuildRequires: apache-commons-logging
BuildRequires: apache-commons-io
BuildRequires: ws-commons-util >= 1.0.1-5
BuildRequires: xmlrpc3-client >= 3.0-2.8
BuildRequires: xmlrpc3-common >= 3.0-2.8
BuildRequires: ws-jaxme >= 0.5.1-2.4
BuildRequires: json
BuildRequires: jdom >= 1.0-5.5
Requires: eclipse-platform >= 0:3.4.0
Requires: apache-commons-lang >= 2.3-2.3
Requires: apache-commons-logging
Requires: apache-commons-io
Requires: ws-commons-util >= 1.0.1-5
Requires: xmlrpc3-client >= 3.0-2.8
Requires: xmlrpc3-common >= 3.0-2.8
Requires: ws-jaxme >= 0.5.1-2.4
Requires: json
Requires: jpackage-utils

Group: Development/Java

%description
Mylyn integrates task support into Eclipse.  It supports offline editing
for certain task repositories and monitors work activity to hide
information that is not relevant to the current task. This package includes
common libraries used by other Eclipse Mylyn packages.

%prep
%setup -q -n org.eclipse.mylyn.commons

rm -rf orbitDeps
mkdir orbitDeps
pushd orbitDeps
ln -s %{_javadir}/apache-commons-lang.jar
ln -s %{_javadir}/apache-commons-io.jar
ln -s %{_javadir}/apache-commons-logging-api.jar
ln -s %{_javadir}/xmlrpc3-client.jar
ln -s %{_javadir}/xmlrpc3-common.jar
ln -s %{_javadir}/ws-commons-util.jar
ln -s %{_javadir}/jdom.jar
ln -s %{_javadir}/json.jar
ln -s %{_javadir}/jaxme/jaxmeapi.jar
popd

%patch0
%patch1

%build
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.mylyn.commons \
 -a "-DjavacSource=1.5 -DjavacTarget=1.5 -DforceContextQualifier=%{qualifier} -DmylynQualifier=%{qualifier}" \
 -j -DJ2SE-1.5=%{_jvmdir}/java/jre/lib/rt.jar \
 -o `pwd`/orbitDeps

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_datadir}/eclipse
install -d -m 755 %{buildroot}%{install_loc}/mylyn-commons

unzip -q -o -d %{buildroot}%{install_loc}/mylyn-commons \
 build/rpmBuild/org.eclipse.mylyn.commons.zip

pushd %{buildroot}%{install_loc}/mylyn-commons/eclipse/plugins
rm org.apache.commons.codec_*.jar
rm org.apache.commons.httpclient_*.jar
rm org.apache.commons.lang_*.jar
rm org.apache.commons.logging_*.jar
rm org.apache.commons.io*.jar
rm org.json*.jar
rm org.jdom*.jar
rm javax.xml.bind_2.0.0*.jar
rm org.apache.ws.commons.util*.jar
rm org.apache.xmlrpc_*.jar
ln -s %{_javadir}/apache-commons-lang.jar
ln -s %{_javadir}/apache-commons-logging-api.jar
ln -s %{_javadir}/apache-commons-io.jar
ln -s %{_javadir}/xmlrpc3-client.jar
ln -s %{_javadir}/xmlrpc3-common.jar
ln -s %{_javadir}/ws-commons-util.jar
ln -s %{_javadir}/jdom.jar
ln -s %{_javadir}/json.jar
ln -s %{_javadir}/jaxme/jaxmeapi.jar
popd

%files
%defattr(-,root,root,-)
%{install_loc}/mylyn-commons
%doc org.eclipse.mylyn.commons-feature/epl-v10.html
%doc org.eclipse.mylyn.commons-feature/license.html

