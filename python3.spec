# TODO:
# - fix lib64 and noarch/datadir patches as the 2nd one overrides some
#   changes made by the first one; propose patches to python team as they
#   seem to be duplicated by fedora as well
#
# Conditional build:
%bcond_with	info			# info pages (requires emacs)
%bcond_without	system_mpdecimal	# system libmpdec library
%bcond_without	tkinter			# disables tkinter module building
%bcond_with	tests			# disables Python testing
%bcond_with	verbose_tests		# runs tests in verbose mode
#
# tests which will not work on 64-bit platforms
%define		no64bit_tests	test_audioop test_rgbimg test_imageop
# tests which may fail because of builder environment limitations (no /proc or /dev/pts)
%define		nobuilder_tests test_resource test_openpty test_socket test_nis test_posix test_locale test_pty

# tests which fail because of some unknown/unresolved reason (this list should be empty)
#   test_site: fails because our site.py is patched to include both /usr/share/... and /usr/lib...
#   test_gdb: fails, as the gdb uses old python version
%define		broken_tests test_httpservers test_distutils test_cmd_line test_pydoc test_telnetlib test_zlib test_gdb test_site

%define py_ver		3.5
%define py_abi		%{py_ver}m
%define py_prefix	%{_prefix}
%define py_libdir	%{py_prefix}/%{_lib}/python%{py_ver}
%define py_incdir	%{_includedir}/python%{py_abi}
%define py_sitedir	%{py_libdir}/site-packages
%define py_dyndir	%{py_libdir}/lib-dynload

Summary:	Very high level scripting language with X interface
Summary(es.UTF-8):	Lenguaje script de alto nivel con interfaz X
Summary(fr.UTF-8):	Langage de script de très haut niveau avec interface X
Summary(pl.UTF-8):	Python - język obiektowy wysokiego poziomu
Summary(pt_BR.UTF-8):	Linguagem de programação interpretada de alto nível
Summary(ru.UTF-8):	Язык программирования очень высокого уровня с X-интерфейсом
Summary(tr.UTF-8):	X arayüzlü, yüksek düzeyli, kabuk yorumlayıcı dili
Summary(uk.UTF-8):	Мова програмування дуже високого рівня з X-інтерфейсом
Name:		python3
Version:	%{py_ver}.0
Release:	4
Epoch:		1
License:	PSF
Group:		Applications
Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
# Source0-md5:	d149d2812f10cbe04c042232e7964171
Patch0:		%{name}-pythonpath.patch
Patch1:		%{name}-ac_fixes.patch
Patch2:		%{name}-lib64.patch
Patch3:		%{name}-noarch_to_datadir.patch
Patch4:		%{name}-no_cmdline_tests.patch
Patch5:		%{name}-makefile-location.patch
Patch6:		python3-atomic.patch
Patch7:		python-distro.patch
Patch8:		%{name}-db.patch
Patch9:		%{name}-install_prefix.patch
URL:		http://www.python.org/
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake
BuildRequires:	bluez-libs-devel
BuildRequires:	bzip2-devel
BuildRequires:	db-devel >= 4
%{?with_info:BuildRequires:	emacs >= 21}
BuildRequires:	expat-devel >= 1:1.95.7
BuildRequires:	file
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	gmp-devel >= 4.0
BuildRequires:	libffi-devel
BuildRequires:	libstdc++-devel
%{?with_system_mpdecimal:BuildRequires:	mpdecimal-devel >= 2.4.1}
BuildRequires:	ncurses-ext-devel >= 5.2
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 5.0
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.3.5
BuildRequires:	tar >= 1:1.22
%{?with_info:BuildRequires:	tetex-makeindex}
%{?with_tkinter:BuildRequires:	tix-devel >= 1:8.1.4-4}
%{?with_tkinter:BuildRequires:	tk-devel >= 8.4.3}
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ppc	-D__ppc__=1
%define		specflags_ppc64	-D__ppc64__=1

%if %{with verbose_tests}
%define test_flags -v -x
%else
%define test_flags -w -x
%endif

%ifarch alpha ia64 ppc64 sparc64 ppc64 %{x8664}
%define test_list %{nobuilder_tests} %{broken_tests} %{no64bit_tests}
%else
%define test_list %{nobuilder_tests} %{broken_tests}
%endif

%ifarch sparc
%define test_list %{nobuilder_tests} %{broken_tests} test_fcntl test_ioctl
%endif

%description
Python is an interpreted, interactive, object-oriented programming
language. It incorporates modules, exceptions, dynamic typing, very
high level dynamic data types, and classes. Python combines remarkable
power with very clear syntax. It has interfaces to many system calls
and libraries, as well as to various window systems, and is extensible
in C or C++. It is also usable as an extension language for
applications that need a programmable interface. Finally, Python is
portable: it runs on many brands of UNIX, on the Mac, and on PCs under
MS-DOS, Windows, Windows NT, and OS/2.

This package contains the Python binary.

%description -l de.UTF-8
Python ist eine interpretierte, interaktive, objektorientierte
Programmiersprache, vergleichbar zu Tcl, Perl, Scheme oder Java.
Python enthält Module, Klassen, Exceptions, High-Level dynamische
Datentypen und dynamisches Typisieren. Python unterstützt Interfaces
zu vielen Systemaufrufen und Libraries, sowie verschiedene
Fenstersysteme (X11, Motif, Tk, Mac und MFC)

Programmierer können neue built-in-Module für Python in C oder C++
schreiben. Python kann auch als Erweiterungssprache für Applikationen
benutzt werden, die ein programmierbares Interface brauchen. Dieses
Paket enthält die meisten Standard-Python-Module, und Module zum
Ansprechen von Tix (Tk-widget set) und RPM.

%description -l es.UTF-8
Python es un lenguaje de scripts interpretado orientado a objetos.
Contiene soporte para carga dinámica de objetos, clases, módulos y
excepciones.

Es sencillo adicionar interfaces para nuevos sistemas de biblioteca a
través de código C, tornando Python fácil de usar en ambientes
particulares/personalizados. Este paquete Python incluye la mayoría de
los módulos padrón Python, junto con módulos para crear interfaces
para el conjunto de componentes Tix para Tk y RPM.

%description -l fr.UTF-8
Python est un langage de script interprété et orienté objet. Il gère
le chargement dynamique des objets, les classes, les modules et les
exceptions. L'ajout d'interfaces aux nouvelles bibliothèques systèmes
avec du code C est simple, ce qui rend Python facile à utiliser dans
des configs personnalisées.

Ce paquetage Python contient la plupart des modules Python standards,
ainsi que ceux permettant l'interfaçage avec les widgets Tix pour Tk
et RPM.

%description -l pl.UTF-8
Python jest interpretowanym, interaktywnym i zorientowanym obiektowo
językiem programowania. Jest modularny, obsługuje wyjątki, dynamiczne
typy, zaawansowane dynamiczne struktury danych i klasy. Python łączy w
sobie duże możliwości i przejrzystą składnię. Posiada interfejsy do
wielu wywołań systemowych i bibliotek, w tym również do różnych
bibliotek okienkowych. Możliwości jego można jeszcze rozszerzać
poprzez odpowiednie moduły pisane w C lub C++. Python może być również
użyty jako element aplikacji, którym potrzebny jest interpreter do
skryptów. I wreszcie, Python jest wieloplatformowy, działa na wielu
odmianach UNIX-a, Macu oraz PC pod DOS-em, Windows, WindowsNT oraz
OS/2.

Ten pakiet zawiera binarkę Pythona.

%description -l pt_BR.UTF-8
Python é uma linguagem de scripts interpretada orientada a objetos.
Contém suporte para carga dinâmica de objetos, classes, módulos e
exceções. Adicionar interfaces para novos sistemas de biblioteca
através de código C é simples, tornando Python fácil de usar em
ambientes particulares/personalizados.

Este pacote Python inclui a maioria do módulos padrão Python, junto
com módulos para interfaceamento para o conjunto de componentes Tix
para Tk e RPM.

%description -l ru.UTF-8
Python - это интерпретируемый, объектно-ориентированный язык
программирования. Он поддерживает динамическую загрузку объектов,
классы, модули и обработку исключительных ситуаций (exceptions).
Простота добавления интерфейсов к новым системным библиотекам через
код на языке C делает Python хорошим выбором для использования в
специальных конфигурациях.

%description -l tr.UTF-8
Python, nesneye yönelik bir kabuk yorumlayıcıdır. Nesnelerin,
sınıfların, modüllerin ve aykırı durumların dinamik yüklenmelerine
destek verir. C koduyla birlikte kullanımı son derece kolaydır. Bu
paket, standart Python birimlerinin çoğunun yanısıra Tk ve RPM için
arayüz birimlerini de içerir.

%description -l uk.UTF-8
Python - це інтерпретована, об'єктно-орієнтована мова програмування.
Він підтримує динамічну загрузку об'єктів, класи, модулі та обробку
виключних ситуацій (exceptions). Простота додавання інтерфейсів для
нових системних бібліотек через код на мові C робить Python добрим
вибором для використання в спеціальних конфігураціях.

%package libs
Summary:	Python library
Summary(pl.UTF-8):	Biblioteka języka Python
Group:		Libraries/Python
# broken detection in rpm/pythondeps.sh
Provides:	python(abi) = %{py_ver}
# for compatibility with existing Ac packages
Provides:	python(bytecode) = %{py_ver}
%{!?with_info:Obsoletes:	python3-doc-info}

%description libs
Python shared library and very essental modules for Python binary.

%description libs -l pl.UTF-8
Biblioteka współdzielona języka Python oraz bardzo podstawowe moduły
dla Pythona.

%package modules
Summary:	Python modules
Summary(pl.UTF-8):	Moduły języka Python
Group:		Libraries/Python
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%{?with_system_mpdecimal:Requires:	mpdecimal >= 2.4.1}
Obsoletes:	python3-modules-sqlite
Obsoletes:	python3-enum
Provides:	python3-enum

%description modules
Python officially distributed modules.

%description modules -l pl.UTF-8
Oficjalnie rozprowadzane moduły języka Python.

%package -n pydoc3
Summary:	Python interactive module documentation access support
Summary(pl.UTF-8):	Interaktywne korzystanie z dokumentacji modułów języka Python
Group:		Applications
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description -n pydoc3
Python interactive module documentation access support.

%description -n pydoc3 -l pl.UTF-8
Interaktywne korzystanie z dokumentacji modułów języka Python.

%package -n idle3
Summary:	IDE for Python language
Summary(pl.UTF-8):	IDE dla języka Python
Group:		Applications
Requires:	%{name}-tkinter = %{epoch}:%{version}-%{release}

%description -n idle3
IDE for Python language.

%description -n idle3 -l pl.UTF-8
IDE dla języka Python.

%package devel
Summary:	Libraries and header files for building python code
Summary(de.UTF-8):	Libraries und Header-Dateien zum Erstellen von Python-Code
Summary(es.UTF-8):	Bibliotecas y archivos de inclusión para construir programas en python
Summary(fr.UTF-8):	Bibliothèques et en-têtes pour construire du code python
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteki Pythona
Summary(pt_BR.UTF-8):	Bibliotecas e arquivos de inclusão para o Python
Summary(ru.UTF-8):	Библиотеки и хедеры для построения кода на языке Python
Summary(tr.UTF-8):	Python ile geliştirme yapmak için gerekli dosyalar
Summary(uk.UTF-8):	Бібліотеки та хедери для програмування на мові Python
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
The Python interpreter is relatively easy to extend with dynamically
loaded extensions and to embed in other programs. This package
contains the header files and libraries which are needed to do both of
these tasks.

%description devel -l de.UTF-8
Der Python-Interpretierer ist relativ einfach anhand von dynamisch
ladbaren Erweiterungen auszubauen und läßt sich in andere Programme
integrieren. Dieses Paket enthält die Header-Dateien und Libraries,
die für beide Aufgaben erforderlich sind.

%description devel -l es.UTF-8
El interpretador Python permite incluir con facilidad extensiones
cargadas dinámicamente. Python es también fácil de ser empotrado en
otros programas. Este paquete contiene los archivos de inclusión y
bibliotecas necesarios para estas dos tareas.

%description devel -l fr.UTF-8
L'interpréteur Python est relativement facile à étendre avec des
extensions chargées dynamiquement et à insérer dans d'autres
programmes. Ce paquetage contient les en-têtes et les bibliothèques
nécessaires à ces deux tâches.

%description devel -l pl.UTF-8
Interpreter Pythona jest w miarę łatwy do rozszerzania przy pomocy
dynamicznie ładowanych rozszerzeń napisanych w C lub C++ oraz
osadzania w innych programach. Ten pakiet zawiera pliki nagłówkowe i
wszystko inne co potrzebne do tych celów.

%description devel -l pt_BR.UTF-8
O interpretador Python permite incluir com facilidade extensões
carregadas dinamicamente. Python é também fácil de ser embutido em
outros programas. Este pacote contém os arquivos de inclusão e
bibliotecas necessários para estas duas tarefas.

%description devel -l ru.UTF-8
Интерпретатор Python относительно легко расширяется при помощи
динамически загружаемых расширений и встраивается в другие программы.
Этот пакет содержит хедеры и библиотеки, необходимые для обеих этих
задач.

%description devel -l tr.UTF-8
Bu paket, Python ile geliştirme yapılabilmesi için gerekli başlık
dosyalarını ve kitaplıkları içerir.

%description devel -l uk.UTF-8
Інтерпретатор Python відносно легко розширюється за допомогою
розширень з динамічною загрузкою та вбудовується в інші програми. Цей
пакет містить хедери та бібліотеки, необхідні для обох цих задач.

%package devel-src
Summary:	Python module sources
Summary(pl.UTF-8):	Pliki źródłowe modułów Pythona
Group:		Development/Languages/Python
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description devel-src
Python module sources.

%description devel-src -l pl.UTF-8
Pliki źródłowe modułów Pythona.

%package devel-tools
Summary:	Python development tools
Summary(pl.UTF-8):	Narzędzia programistyczne języka Python
Group:		Development/Languages/Python
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description devel-tools
Python development tools such as profilers and debugger.

%description devel-tools -l pl.UTF-8
Narzędzia programistyczne języka Python takie jak profiler oraz
debugger.

%package 2to3
Summary:	Automated Python 2 to 3 code translation
Summary(pl.UTF-8):	Automatyczne tłumaczenie kodu Pythona 2 do 3
Group:		Development/Languages/Pythona

%description 2to3
2to3 is a Python program that reads Python 2.x source code and applies
a series of fixers to transform it into valid Python 3.x code. The
standard library contains a rich set of fixers that will handle almost
all code. 2to3 supporting library lib2to3 is, however, a flexible and
generic library, so it is possible to write your own fixers for 2to3.
lib2to3 could also be adapted to custom applications in which Python
code needs to be edited automatically.

%description 2to3 -l pl.UTF-8
2to3 to program w Pythonie czytający od źródłowy w Pythonie 2.x i
aplikujący serię poprawek przekształcających go w poprawny kod w
Pythonie 3.x. Biblioteka standardowa zawiera duży zbiór poprawek
obsługujących większość kodu. Biblioteka wspierająca 2to3 (lib2to3)
jest jednak elastyczną i ogólną biblioteką, więc można pisać własne
poprawki dla 2to3. lib2to3 można także zaadaptować na potrzeby
własnych zastosowań, w których kod w Pythonie musi być modyfikowany
automatycznie.

%package static
Summary:	Static python library
Summary(pl.UTF-8):	Statyczna biblioteka Pythona
Group:		Development/Languages/Python
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static python library.

%description static -l pl.UTF-8
Statyczna biblioteka Pythona.

%package doc-info
Summary:	Documentation on Python in texinfo format
Summary(pl.UTF-8):	Dokumentacja do Pythona w formacie texinfo
Group:		Documentation

%description doc-info
Documentation on Python in texinfo format.

%description doc-info -l pl.UTF-8
Dokumentacja do Pythona w formacie texinfo.

%package tkinter
Summary:	Standard Python interface to the Tk GUI toolkit
Summary(de.UTF-8):	Grafische Tk-Schnittstelle für Python
Summary(es.UTF-8):	Interfaz de GUI Tk para Python
Summary(fr.UTF-8):	Interface graphique Tk pour Python
Summary(pl.UTF-8):	Standardowy interfejs Pythona do biblioteki Tk
Summary(pt_BR.UTF-8):	Interface GUI Tk para Phyton
Summary(tr.UTF-8):	Python için grafik kullanıcı arayüzü
Group:		Libraries/Python
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}
Requires:	tcl >= 8.4.3
Requires:	tix >= 1:8.1.4-4
Requires:	tk >= 8.4.3

%description tkinter
Standard Python interface to the Tk GUI toolkit.

%description tkinter -l de.UTF-8
Eine grafische Schnittstelle für Python, basierend auf Tcl/Tk, und von
vielen Konfigurations-Tools genutzt.

%description tkinter -l es.UTF-8
Una interfaz gráfica para Python, basada en Tcl/Tk, y usada por muchas
herramientas de configuración.

%description tkinter -l fr.UTF-8
Interface graphique pour Python, basée sur Tcl/Tk et utilisée par
beaucoup des outils de configuration.

%description tkinter -l pl.UTF-8
Standardowy interfejs Pythona do biblioteki Tk.

%description tkinter -l pt_BR.UTF-8
Uma interface gráfica para Python, baseada em Tcl/Tk, e usada por
muitas ferramentas de configuração.

%description tkinter -l ru.UTF-8
Графический интерфейс (GUI) для Python, построенный на Tcl/Tk.

%description tkinter -l tr.UTF-8
Python için Tcl/Tk'ye dayalı ve pek çok ayarlama aracı tarafından
kullanılan grafik bir arayüzdür.

%description tkinter -l uk.UTF-8
Графічний інтерфейс (GUI) для Python, побудований на Tcl/Tk.

%package examples
Summary:	Example programs in Python
Summary(pl.UTF-8):	Przykładowe programy w Pythonie
Group:		Development/Languages/Python

%description examples
Example programs in Python.

These are for Python 2.3.4, not %{version}.

%description examples -l pl.UTF-8
Przykładowe programy w Pythonie.

Przykłady te są dla Pythona 2.3.4, nie %{version}.

%package test
Summary:	Test modules for Python
Summary(pl.UTF-8):	Moduły testowe dla Pythona
Group:		Development/Languages/Python

%description test
Test modules for Python.

%description test -l pl.UTF-8
Moduły testowe dla Pythona.

%prep
%setup -q -n Python-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%{__rm} -r Modules/zlib
%{__rm} -r Modules/expat

for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx; do
	%{__rm} -r Modules/_ctypes/$SUBDIR/*
done

%if "%{pld_release}" == "ac"
files="md5module.c sha1module.c"
files="$files sha256module.c sha512module.c"
for f in $files; do
	%{__rm} Modules/$f
done
%endif

find . -name '*.py' | xargs -r grep -El '^#! */usr/bin/env python3?' | xargs %{__sed} -i -e '1s,^#! */usr/bin/env python3\?,#!/usr/bin/python3,'

%build
if ! grep -q "tmpfs" /proc/self/mounts; then
	echo "You need to have /dev/shm mounted in order to build this package!" >&2
	echo "(Or any other tmpfs mounted and accessible to the rpmbuild process)" >&2
	exit 1
fi

%{__aclocal}
%{__autoconf}
%configure \
	CC="%{__cc}" \
	OPT="%{rpmcflags} -fno-caller-saves" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	ac_cv_posix_semaphores_enabled=yes \
	ac_cv_broken_sem_getvalue=no \
	--enable-ipv6 \
	--enable-shared \
	--with-computed-gotos \
	--with-dbmliborder=gdbm:bdb \
	--with-doc-strings \
	--without-ensurepip \
	--with-fpectl \
	%{?with_debug:--with-pydebug} \
	--with-signal-module \
	--with-system-expat \
	--with-system-ffi \
	%{?with_system_mpdecimal:--with-system-libmpdec} \
	--with-threads \
%ifarch %{ix86} %{x8664} ppc ppc64
	--with-tsc
%endif

%{__make} 2>&1 | awk '
BEGIN { fail = 0; logmsg = ""; }
{
        if ($0 ~ /\*\*\* WARNING:/) {
                fail = 1;
                logmsg = logmsg $0;
        }
        print $0;
}
END { if (fail) { print "\nPROBLEMS FOUND:"; print logmsg; exit(1); } }'

LC_ALL=C
export LC_ALL
%if %{with tests}
binlibdir=`echo build/lib.*`
# -l and -j don't go together! and -j is brought up by Tools/scripts/run_tests.py
%{__make} test \
	TESTOPTS="%{test_flags} %{test_list}" \
	TESTPYTHON="LD_LIBRARY_PATH=`pwd` PYTHONHOME=`pwd` PYTHONPATH=`pwd`/Lib:`pwd`/$binlibdir ./python -tt"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pkgconfigdir}} \
	$RPM_BUILD_ROOT{%{py_sitedir},%{py_sitescriptdir}}/__pycache__ \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT{%{_infodir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT/etc/shrc.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with info}
%{__make} -C Doc/info
cp -p Doc/info/python*info* $RPM_BUILD_ROOT%{_infodir}
%endif

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a Tools $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# make libpython3.so simply symlink to real lib
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpython3.so
ln -s libpython%{py_abi}.so $RPM_BUILD_ROOT%{_libdir}/libpython3.so

#
# create several useful aliases, such as timeit.py, profile.py, pdb.py, smtpd.py
#

# for python devel tools
for script in timeit profile pdb pstats; do
	echo "alias ${script}%{py_ver}.py='python%{py_ver} -m ${script}'"
done > $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh

echo "alias pygettext%{py_ver}.py='pygettext%{py_ver}'" \
	>> $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh

sed 's/=/ /' \
	< $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh \
	> $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.csh

# for python modules
for script in smtpd webbrowser; do
	echo "alias ${script}%{py_ver}.py='python%{py_ver} -m ${script}'"
done > $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-modules.sh

sed 's/=/ /' \
	< $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-modules.sh \
	> $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-modules.csh

# xgettext specific for Python code
#
# we will have two commands: pygettext.py (an alias) and pygettext;
# this way there are no import (which is impossible now) conflicts and
# pygettext.py is provided for compatibility
install -p Tools/i18n/pygettext.py $RPM_BUILD_ROOT%{_bindir}/pygettext%{py_ver}

# reindent python code
install -p Tools/scripts/reindent.py $RPM_BUILD_ROOT%{_bindir}/pyreindent%{py_ver}

# just to cut the noise, as they are not packaged (now)
%{__rm} $RPM_BUILD_ROOT%{py_scriptdir}/plat-*/regen
%{__rm} $RPM_BUILD_ROOT%{py_scriptdir}/ctypes/macholib/fetch_macholib*
%{__rm} $RPM_BUILD_ROOT%{py_scriptdir}/site-packages/README
%{__rm} $RPM_BUILD_ROOT%{py_scriptdir}/distutils/command/wininst*.exe
%{__rm} $RPM_BUILD_ROOT%{py_scriptdir}/idlelib/*.bat
%{__rm} $RPM_BUILD_ROOT%{py_scriptdir}/idlelib/*.pyw

# currently provided by python-2to3, consider switching to this one
%{__rm} $RPM_BUILD_ROOT%{_bindir}/2to3

# that seems to be only an empty extension template,
# which seems to be built only {with tests}
%{__rm} -f $RPM_BUILD_ROOT%{py_dyndir}/xxlimited.*.so

# already in %%doc
%{__rm} $RPM_BUILD_ROOT%{py_scriptdir}/LICENSE.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	doc-info -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	doc-info -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/python%{py_ver}
%attr(755,root,root) %{_bindir}/python%{py_abi}
%attr(755,root,root) %{_bindir}/python3
%{_mandir}/man1/python%{py_ver}.1*
%{_mandir}/man1/python3.1*

%files libs
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_libdir}/libpython%{py_abi}.so.*.*

%dir %{py_incdir}
%{py_incdir}/pyconfig.h

%dir %{py_libdir}
%dir %{py_dyndir}
%dir %{py_sitedir}
%dir %{py_sitedir}/__pycache__
%dir %{py_scriptdir}
%dir %{py_scriptdir}/__pycache__
%dir %{py_sitescriptdir}
%dir %{py_sitescriptdir}/__pycache__

# shared modules required by python library
%attr(755,root,root) %{py_dyndir}/_struct.cpython-*.so

# modules required by python library
%{py_scriptdir}/_collections_abc.py
%{py_scriptdir}/_sitebuiltins.py
%{py_scriptdir}/_sysconfigdata.py
%{py_scriptdir}/_weakrefset.py
%{py_scriptdir}/abc.py
%{py_scriptdir}/bisect.py
%{py_scriptdir}/codecs.py
%{py_scriptdir}/copyreg.py
%{py_scriptdir}/functools.py
%{py_scriptdir}/genericpath.py
%{py_scriptdir}/heapq.py
%{py_scriptdir}/keyword.py
%{py_scriptdir}/linecache.py
%{py_scriptdir}/locale.py
%{py_scriptdir}/io.py
%{py_scriptdir}/posixpath.py
%{py_scriptdir}/re.py
%{py_scriptdir}/reprlib.py
%{py_scriptdir}/site.py
%{py_scriptdir}/sre_*.py
%{py_scriptdir}/stat.py
%{py_scriptdir}/sysconfig.py
%{py_scriptdir}/token.py
%{py_scriptdir}/tokenize.py
%{py_scriptdir}/traceback.py
%{py_scriptdir}/weakref.py
%{py_scriptdir}/os.py
# needed by the dynamic sys.lib patch
%{py_scriptdir}/types.py
%{py_scriptdir}/__pycache__/_sitebuiltins.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_sysconfigdata.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_weakrefset.cpython-*.py[co]
%{py_scriptdir}/__pycache__/abc.cpython-*.py[co]
%{py_scriptdir}/__pycache__/bisect.cpython-*.py[co]
%{py_scriptdir}/__pycache__/codecs.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_collections_abc.cpython-*.py[co]
%{py_scriptdir}/__pycache__/copyreg.cpython-*.py[co]
%{py_scriptdir}/__pycache__/functools.cpython-*.py[co]
%{py_scriptdir}/__pycache__/genericpath.cpython-*.py[co]
%{py_scriptdir}/__pycache__/heapq.cpython-*.py[co]
%{py_scriptdir}/__pycache__/keyword.cpython-*.py[co]
%{py_scriptdir}/__pycache__/linecache.cpython-*.py[co]
%{py_scriptdir}/__pycache__/locale.cpython-*.py[co]
%{py_scriptdir}/__pycache__/io.cpython-*.py[co]
%{py_scriptdir}/__pycache__/posixpath.cpython-*.py[co]
%{py_scriptdir}/__pycache__/re.cpython-*.py[co]
%{py_scriptdir}/__pycache__/reprlib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/site.cpython-*.py[co]
%{py_scriptdir}/__pycache__/sre_*.cpython-*.py[co]
%{py_scriptdir}/__pycache__/stat.cpython-*.py[co]
%{py_scriptdir}/__pycache__/sysconfig.cpython-*.py[co]
%{py_scriptdir}/__pycache__/token.cpython-*.py[co]
%{py_scriptdir}/__pycache__/tokenize.cpython-*.py[co]
%{py_scriptdir}/__pycache__/traceback.cpython-*.py[co]
%{py_scriptdir}/__pycache__/weakref.cpython-*.py[co]
%{py_scriptdir}/__pycache__/os.cpython-*.py[co]
%{py_scriptdir}/__pycache__/types.cpython-*.py[co]

%{py_scriptdir}/collections

# encodings required by python library
%dir %{py_scriptdir}/encodings
%{py_scriptdir}/encodings/__pycache__
%{py_scriptdir}/encodings/*.py

%dir %{py_libdir}/config-%{py_abi}
%{py_libdir}/config-%{py_abi}/Makefile
%{py_libdir}/config-%{py_abi}/Setup
%{py_libdir}/config-%{py_abi}/Setup.config
%{py_libdir}/config-%{py_abi}/Setup.local

%files modules
%defattr(644,root,root,755)
/etc/shrc.d/python*-modules*
%attr(755,root,root) %{_bindir}/pyvenv
%attr(755,root,root) %{_bindir}/pyvenv-%{py_ver}
%{py_scriptdir}/__future__.py
%{py_scriptdir}/__phello__.foo.py
%{py_scriptdir}/_bootlocale.py
%{py_scriptdir}/_compat_pickle.py
%{py_scriptdir}/_compression.py
%{py_scriptdir}/_dummy_thread.py
%{py_scriptdir}/_markupbase.py
%{py_scriptdir}/_osx_support.py
%{py_scriptdir}/_pydecimal.py
%{py_scriptdir}/_pyio.py
%{py_scriptdir}/_strptime.py
%{py_scriptdir}/_threading_local.py
%{py_scriptdir}/aifc.py
%{py_scriptdir}/antigravity.py
%{py_scriptdir}/argparse.py
%{py_scriptdir}/ast.py
%{py_scriptdir}/asynchat.py
%{py_scriptdir}/asyncore.py
%{py_scriptdir}/base64.py
%{py_scriptdir}/bdb.py
%{py_scriptdir}/binhex.py
%{py_scriptdir}/bz2.py
%{py_scriptdir}/cProfile.py
%{py_scriptdir}/calendar.py
%{py_scriptdir}/cgi.py
%{py_scriptdir}/cgitb.py
%{py_scriptdir}/chunk.py
%{py_scriptdir}/cmd.py
%{py_scriptdir}/code.py
%{py_scriptdir}/codeop.py
%{py_scriptdir}/colorsys.py
%{py_scriptdir}/compileall.py
%{py_scriptdir}/configparser.py
%{py_scriptdir}/contextlib.py
%{py_scriptdir}/copy.py
%{py_scriptdir}/crypt.py
%{py_scriptdir}/csv.py
%{py_scriptdir}/datetime.py
%{py_scriptdir}/decimal.py
%{py_scriptdir}/difflib.py
%{py_scriptdir}/dis.py
%{py_scriptdir}/doctest.py
%{py_scriptdir}/dummy_threading.py
%{py_scriptdir}/enum.py
%{py_scriptdir}/filecmp.py
%{py_scriptdir}/fileinput.py
%{py_scriptdir}/fnmatch.py
%{py_scriptdir}/formatter.py
%{py_scriptdir}/fractions.py
%{py_scriptdir}/ftplib.py
%{py_scriptdir}/getopt.py
%{py_scriptdir}/getpass.py
%{py_scriptdir}/gettext.py
%{py_scriptdir}/glob.py
%{py_scriptdir}/gzip.py
%{py_scriptdir}/hashlib.py
%{py_scriptdir}/hmac.py
%{py_scriptdir}/imaplib.py
%{py_scriptdir}/imghdr.py
%{py_scriptdir}/imp.py
%{py_scriptdir}/inspect.py
%{py_scriptdir}/ipaddress.py
%{py_scriptdir}/lzma.py
%{py_scriptdir}/macpath.py
%{py_scriptdir}/macurl2path.py
%{py_scriptdir}/mailbox.py
%{py_scriptdir}/mailcap.py
%{py_scriptdir}/mimetypes.py
%{py_scriptdir}/modulefinder.py
%{py_scriptdir}/netrc.py
%{py_scriptdir}/nntplib.py
%{py_scriptdir}/ntpath.py
%{py_scriptdir}/nturl2path.py
%{py_scriptdir}/numbers.py
%{py_scriptdir}/opcode.py
%{py_scriptdir}/operator.py
%{py_scriptdir}/optparse.py
%{py_scriptdir}/pathlib.py
%{py_scriptdir}/pickle.py
%{py_scriptdir}/pickletools.py
%{py_scriptdir}/pipes.py
%{py_scriptdir}/pkgutil.py
%{py_scriptdir}/platform.py
%{py_scriptdir}/plistlib.py
%{py_scriptdir}/poplib.py
%{py_scriptdir}/pprint.py
%{py_scriptdir}/pty.py
%{py_scriptdir}/py_compile.py
%{py_scriptdir}/pyclbr.py
%{py_scriptdir}/queue.py
%{py_scriptdir}/quopri.py
%{py_scriptdir}/random.py
%{py_scriptdir}/rlcompleter.py
%{py_scriptdir}/runpy.py
%{py_scriptdir}/signal.py
%{py_scriptdir}/sched.py
%{py_scriptdir}/selectors.py
%{py_scriptdir}/shelve.py
%{py_scriptdir}/shlex.py
%{py_scriptdir}/shutil.py
%{py_scriptdir}/smtpd.py
%{py_scriptdir}/smtplib.py
%{py_scriptdir}/sndhdr.py
%{py_scriptdir}/socket.py
%{py_scriptdir}/socketserver.py
%{py_scriptdir}/ssl.py
%{py_scriptdir}/statistics.py
%{py_scriptdir}/string.py
%{py_scriptdir}/stringprep.py
%{py_scriptdir}/struct.py
%{py_scriptdir}/subprocess.py
%{py_scriptdir}/sunau.py
%{py_scriptdir}/symbol.py
%{py_scriptdir}/symtable.py
%{py_scriptdir}/tabnanny.py
%{py_scriptdir}/tarfile.py
%{py_scriptdir}/telnetlib.py
%{py_scriptdir}/tempfile.py
%{py_scriptdir}/textwrap.py
%{py_scriptdir}/this.py
%{py_scriptdir}/threading.py
%{py_scriptdir}/trace.py
%{py_scriptdir}/tracemalloc.py
%{py_scriptdir}/tty.py
%{py_scriptdir}/turtle.py
%{py_scriptdir}/typing.py
%{py_scriptdir}/uu.py
%{py_scriptdir}/uuid.py
%{py_scriptdir}/warnings.py
%{py_scriptdir}/wave.py
%{py_scriptdir}/webbrowser.py
%{py_scriptdir}/xdrlib.py
%{py_scriptdir}/zipapp.py
%{py_scriptdir}/zipfile.py
%{py_scriptdir}/__pycache__/__future__.cpython-*.py[co]
%{py_scriptdir}/__pycache__/__phello__.foo.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_bootlocale.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_compat_pickle.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_compression.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_dummy_thread.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_markupbase.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_osx_support.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_pydecimal.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_pyio.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_strptime.cpython-*.py[co]
%{py_scriptdir}/__pycache__/_threading_local.cpython-*.py[co]
%{py_scriptdir}/__pycache__/aifc.cpython-*.py[co]
%{py_scriptdir}/__pycache__/antigravity.cpython-*.py[co]
%{py_scriptdir}/__pycache__/argparse.cpython-*.py[co]
%{py_scriptdir}/__pycache__/ast.cpython-*.py[co]
%{py_scriptdir}/__pycache__/asynchat.cpython-*.py[co]
%{py_scriptdir}/__pycache__/asyncore.cpython-*.py[co]
%{py_scriptdir}/__pycache__/base64.cpython-*.py[co]
%{py_scriptdir}/__pycache__/bdb.cpython-*.py[co]
%{py_scriptdir}/__pycache__/binhex.cpython-*.py[co]
%{py_scriptdir}/__pycache__/bz2.cpython-*.py[co]
%{py_scriptdir}/__pycache__/cProfile.cpython-*.py[co]
%{py_scriptdir}/__pycache__/calendar.cpython-*.py[co]
%{py_scriptdir}/__pycache__/cgi.cpython-*.py[co]
%{py_scriptdir}/__pycache__/cgitb.cpython-*.py[co]
%{py_scriptdir}/__pycache__/chunk.cpython-*.py[co]
%{py_scriptdir}/__pycache__/cmd.cpython-*.py[co]
%{py_scriptdir}/__pycache__/code.cpython-*.py[co]
%{py_scriptdir}/__pycache__/codeop.cpython-*.py[co]
%{py_scriptdir}/__pycache__/colorsys.cpython-*.py[co]
%{py_scriptdir}/__pycache__/compileall.cpython-*.py[co]
%{py_scriptdir}/__pycache__/configparser.cpython-*.py[co]
%{py_scriptdir}/__pycache__/contextlib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/copy.cpython-*.py[co]
%{py_scriptdir}/__pycache__/crypt.cpython-*.py[co]
%{py_scriptdir}/__pycache__/csv.cpython-*.py[co]
%{py_scriptdir}/__pycache__/datetime.cpython-*.py[co]
%{py_scriptdir}/__pycache__/decimal.cpython-*.py[co]
%{py_scriptdir}/__pycache__/difflib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/dis.cpython-*.py[co]
%{py_scriptdir}/__pycache__/doctest.cpython-*.py[co]
%{py_scriptdir}/__pycache__/dummy_threading.cpython-*.py[co]
%{py_scriptdir}/__pycache__/enum.cpython-*.py[co]
%{py_scriptdir}/__pycache__/filecmp.cpython-*.py[co]
%{py_scriptdir}/__pycache__/fileinput.cpython-*.py[co]
%{py_scriptdir}/__pycache__/fnmatch.cpython-*.py[co]
%{py_scriptdir}/__pycache__/formatter.cpython-*.py[co]
%{py_scriptdir}/__pycache__/fractions.cpython-*.py[co]
%{py_scriptdir}/__pycache__/ftplib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/getopt.cpython-*.py[co]
%{py_scriptdir}/__pycache__/getpass.cpython-*.py[co]
%{py_scriptdir}/__pycache__/gettext.cpython-*.py[co]
%{py_scriptdir}/__pycache__/glob.cpython-*.py[co]
%{py_scriptdir}/__pycache__/gzip.cpython-*.py[co]
%{py_scriptdir}/__pycache__/hashlib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/hmac.cpython-*.py[co]
%{py_scriptdir}/__pycache__/imaplib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/imghdr.cpython-*.py[co]
%{py_scriptdir}/__pycache__/imp.cpython-*.py[co]
%{py_scriptdir}/__pycache__/inspect.cpython-*.py[co]
%{py_scriptdir}/__pycache__/ipaddress.cpython-*.py[co]
%{py_scriptdir}/__pycache__/lzma.cpython-*.py[co]
%{py_scriptdir}/__pycache__/macpath.cpython-*.py[co]
%{py_scriptdir}/__pycache__/macurl2path.cpython-*.py[co]
%{py_scriptdir}/__pycache__/mailbox.cpython-*.py[co]
%{py_scriptdir}/__pycache__/mailcap.cpython-*.py[co]
%{py_scriptdir}/__pycache__/mimetypes.cpython-*.py[co]
%{py_scriptdir}/__pycache__/modulefinder.cpython-*.py[co]
%{py_scriptdir}/__pycache__/netrc.cpython-*.py[co]
%{py_scriptdir}/__pycache__/nntplib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/ntpath.cpython-*.py[co]
%{py_scriptdir}/__pycache__/nturl2path.cpython-*.py[co]
%{py_scriptdir}/__pycache__/numbers.cpython-*.py[co]
%{py_scriptdir}/__pycache__/opcode.cpython-*.py[co]
%{py_scriptdir}/__pycache__/operator.cpython-*.py[co]
%{py_scriptdir}/__pycache__/optparse.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pathlib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pickle.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pickletools.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pipes.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pkgutil.cpython-*.py[co]
%{py_scriptdir}/__pycache__/platform.cpython-*.py[co]
%{py_scriptdir}/__pycache__/plistlib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/poplib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pprint.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pty.cpython-*.py[co]
%{py_scriptdir}/__pycache__/py_compile.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pyclbr.cpython-*.py[co]
%{py_scriptdir}/__pycache__/queue.cpython-*.py[co]
%{py_scriptdir}/__pycache__/quopri.cpython-*.py[co]
%{py_scriptdir}/__pycache__/random.cpython-*.py[co]
%{py_scriptdir}/__pycache__/rlcompleter.cpython-*.py[co]
%{py_scriptdir}/__pycache__/runpy.cpython-*.py[co]
%{py_scriptdir}/__pycache__/sched.cpython-*.py[co]
%{py_scriptdir}/__pycache__/selectors.cpython-*.py[co]
%{py_scriptdir}/__pycache__/shelve.cpython-*.py[co]
%{py_scriptdir}/__pycache__/shlex.cpython-*.py[co]
%{py_scriptdir}/__pycache__/shutil.cpython-*.py[co]
%{py_scriptdir}/__pycache__/signal.cpython-*.py[co]
%{py_scriptdir}/__pycache__/smtpd.cpython-*.py[co]
%{py_scriptdir}/__pycache__/smtplib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/sndhdr.cpython-*.py[co]
%{py_scriptdir}/__pycache__/socket.cpython-*.py[co]
%{py_scriptdir}/__pycache__/socketserver.cpython-*.py[co]
%{py_scriptdir}/__pycache__/ssl.cpython-*.py[co]
%{py_scriptdir}/__pycache__/statistics.cpython-*.py[co]
%{py_scriptdir}/__pycache__/string.cpython-*.py[co]
%{py_scriptdir}/__pycache__/stringprep.cpython-*.py[co]
%{py_scriptdir}/__pycache__/struct.cpython-*.py[co]
%{py_scriptdir}/__pycache__/subprocess.cpython-*.py[co]
%{py_scriptdir}/__pycache__/sunau.cpython-*.py[co]
%{py_scriptdir}/__pycache__/symbol.cpython-*.py[co]
%{py_scriptdir}/__pycache__/symtable.cpython-*.py[co]
%{py_scriptdir}/__pycache__/tabnanny.cpython-*.py[co]
%{py_scriptdir}/__pycache__/tarfile.cpython-*.py[co]
%{py_scriptdir}/__pycache__/telnetlib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/tempfile.cpython-*.py[co]
%{py_scriptdir}/__pycache__/textwrap.cpython-*.py[co]
%{py_scriptdir}/__pycache__/this.cpython-*.py[co]
%{py_scriptdir}/__pycache__/threading.cpython-*.py[co]
%{py_scriptdir}/__pycache__/trace.cpython-*.py[co]
%{py_scriptdir}/__pycache__/tracemalloc.cpython-*.py[co]
%{py_scriptdir}/__pycache__/tty.cpython-*.py[co]
%{py_scriptdir}/__pycache__/turtle.cpython-*.py[co]
%{py_scriptdir}/__pycache__/typing.cpython-*.py[co]
%{py_scriptdir}/__pycache__/uu.cpython-*.py[co]
%{py_scriptdir}/__pycache__/uuid.cpython-*.py[co]
%{py_scriptdir}/__pycache__/warnings.cpython-*.py[co]
%{py_scriptdir}/__pycache__/wave.cpython-*.py[co]
%{py_scriptdir}/__pycache__/webbrowser.cpython-*.py[co]
%{py_scriptdir}/__pycache__/xdrlib.cpython-*.py[co]
%{py_scriptdir}/__pycache__/zipapp.cpython-*.py[co]
%{py_scriptdir}/__pycache__/zipfile.cpython-*.py[co]

#
# list .so modules to be sure that all of them are built
#

%attr(755,root,root) %{py_dyndir}/_bisect.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_bz2.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_cn.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_hk.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_iso2022.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_jp.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_kr.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_tw.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_crypt.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_csv.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_ctypes*.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_curses_panel.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_curses.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_datetime.cpython-*.so
%ifnarch sparc64
%attr(755,root,root) %{py_dyndir}/_dbm.cpython-*.so
%endif
%attr(755,root,root) %{py_dyndir}/_decimal.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_elementtree.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_gdbm.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_hashlib.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_heapq.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_json.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_lsprof.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_lzma.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_md5.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_multibytecodec.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_multiprocessing.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_opcode.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_pickle.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_posixsubprocess.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_random.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_sha1.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_socket.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_ssl.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testbuffer.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testcapi.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testimportmultiple.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testmultiphase.cpython-*.so

# for openssl < 0.9.8 package sha256 and sha512 modules
%if "%{pld_release}" != "ac"
%attr(755,root,root) %{py_dyndir}/_sha256.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_sha512.cpython-*.so
%endif

%attr(755,root,root) %{py_dyndir}/array.cpython-*.so
%attr(755,root,root) %{py_dyndir}/audioop.cpython-*.so
%attr(755,root,root) %{py_dyndir}/binascii.cpython-*.so
%attr(755,root,root) %{py_dyndir}/cmath.cpython-*.so
%attr(755,root,root) %{py_dyndir}/fcntl.cpython-*.so
%attr(755,root,root) %{py_dyndir}/grp.cpython-*.so
%attr(755,root,root) %{py_dyndir}/math.cpython-*.so
%attr(755,root,root) %{py_dyndir}/mmap.cpython-*.so
%attr(755,root,root) %{py_dyndir}/nis.cpython-*.so
%attr(755,root,root) %{py_dyndir}/ossaudiodev.cpython-*.so
%attr(755,root,root) %{py_dyndir}/parser.cpython-*.so
%attr(755,root,root) %{py_dyndir}/pyexpat.cpython-*.so
%attr(755,root,root) %{py_dyndir}/readline.cpython-*.so
%attr(755,root,root) %{py_dyndir}/resource.cpython-*.so
%attr(755,root,root) %{py_dyndir}/select.cpython-*.so
%attr(755,root,root) %{py_dyndir}/syslog.cpython-*.so
%attr(755,root,root) %{py_dyndir}/termios.cpython-*.so
%attr(755,root,root) %{py_dyndir}/spwd.cpython-*.so
%attr(755,root,root) %{py_dyndir}/unicodedata.cpython-*.so
%attr(755,root,root) %{py_dyndir}/zlib.cpython-*.so

%dir %{py_scriptdir}/plat-*
%{py_scriptdir}/plat-*/__pycache__
%{py_scriptdir}/plat-*/*.py

%dir %{py_scriptdir}/asyncio
%{py_scriptdir}/asyncio/__pycache__
%{py_scriptdir}/asyncio/*.py

%{py_scriptdir}/concurrent

%dir %{py_scriptdir}/ctypes
%dir %{py_scriptdir}/ctypes/macholib
%{py_scriptdir}/ctypes/__pycache__
%{py_scriptdir}/ctypes/macholib/__pycache__

%{py_scriptdir}/ctypes/*.py
%{py_scriptdir}/ctypes/macholib/*.py
%doc %{py_scriptdir}/ctypes/macholib/README.ctypes

%dir %{py_scriptdir}/curses
%{py_scriptdir}/curses/__pycache__
%{py_scriptdir}/curses/*.py

%dir %{py_scriptdir}/dbm
%{py_scriptdir}/dbm/__pycache__
%{py_scriptdir}/dbm/*.py

%dir %{py_scriptdir}/distutils
%dir %{py_scriptdir}/distutils/command
%doc %{py_scriptdir}/distutils/README
%{py_scriptdir}/distutils/__pycache__
%{py_scriptdir}/distutils/command/__pycache__
%{py_scriptdir}/distutils/*.py
%{py_scriptdir}/distutils/command/*.py
%{py_scriptdir}/distutils/command/command_template

%dir %{py_scriptdir}/email
%dir %{py_scriptdir}/email/mime
%{py_scriptdir}/email/__pycache__
%{py_scriptdir}/email/mime/__pycache__
%{py_scriptdir}/email/architecture.rst
%{py_scriptdir}/email/*.py
%{py_scriptdir}/email/mime/*.py

%dir %{py_scriptdir}/ensurepip
%{py_scriptdir}/ensurepip/__pycache__
%{py_scriptdir}/ensurepip/*.py
%{py_scriptdir}/ensurepip/_bundled

%dir %{py_scriptdir}/html
%{py_scriptdir}/html/*.py
%{py_scriptdir}/html/__pycache__

%dir %{py_scriptdir}/http
%{py_scriptdir}/http/__pycache__
%{py_scriptdir}/http/*.py

%dir %{py_scriptdir}/idlelib

%dir %{py_scriptdir}/importlib
%{py_scriptdir}/importlib/__pycache__
%{py_scriptdir}/importlib/*.py

%dir %{py_scriptdir}/json
%{py_scriptdir}/json/__pycache__
%{py_scriptdir}/json/*.py

%dir %{py_scriptdir}/logging
%{py_scriptdir}/logging/__pycache__
%{py_scriptdir}/logging/*.py

%dir %{py_scriptdir}/multiprocessing
%{py_scriptdir}/multiprocessing/__pycache__
%{py_scriptdir}/multiprocessing/*.py
%dir %{py_scriptdir}/multiprocessing/dummy
%{py_scriptdir}/multiprocessing/dummy/__pycache__
%{py_scriptdir}/multiprocessing/dummy/*.py

%{py_scriptdir}/turtledemo

%dir %{py_scriptdir}/unittest
%{py_scriptdir}/unittest/__pycache__
%{py_scriptdir}/unittest/*.py

%dir %{py_scriptdir}/urllib
%{py_scriptdir}/urllib/__pycache__
%{py_scriptdir}/urllib/*.py

%dir %{py_scriptdir}/venv
%{py_scriptdir}/venv/__pycache__
%{py_scriptdir}/venv/*.py
%dir %{py_scriptdir}/venv/scripts
%dir %{py_scriptdir}/venv/scripts/posix
%{py_scriptdir}/venv/scripts/posix/activate
%{py_scriptdir}/venv/scripts/posix/activate.csh
%{py_scriptdir}/venv/scripts/posix/activate.fish

%dir %{py_scriptdir}/wsgiref
%{py_scriptdir}/wsgiref/__pycache__
%{py_scriptdir}/wsgiref/*.py

%dir %{py_scriptdir}/xml
%dir %{py_scriptdir}/xml/dom
%dir %{py_scriptdir}/xml/etree
%dir %{py_scriptdir}/xml/parsers
%dir %{py_scriptdir}/xml/sax
%{py_scriptdir}/xml/__pycache__
%{py_scriptdir}/xml/dom/__pycache__
%{py_scriptdir}/xml/etree/__pycache__
%{py_scriptdir}/xml/parsers/__pycache__
%{py_scriptdir}/xml/sax/__pycache__
%{py_scriptdir}/xml/*.py
%{py_scriptdir}/xml/dom/*.py
%{py_scriptdir}/xml/etree/*.py
%{py_scriptdir}/xml/parsers/*.py
%{py_scriptdir}/xml/sax/*.py

%dir %{py_scriptdir}/xmlrpc
%{py_scriptdir}/xmlrpc/__pycache__
%{py_scriptdir}/xmlrpc/*.py

%attr(755,root,root) %{py_dyndir}/_sqlite3.cpython-*.so
%dir %{py_scriptdir}/sqlite3
%{py_scriptdir}/sqlite3/__pycache__
%{py_scriptdir}/sqlite3/*.py

%files -n pydoc3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pydoc3
%attr(755,root,root) %{_bindir}/pydoc3.5
%{py_scriptdir}/pydoc.py
%{py_scriptdir}/__pycache__/pydoc.cpython-*.py[co]
%dir %{py_scriptdir}/pydoc_data
%{py_scriptdir}/pydoc_data/__pycache__
%{py_scriptdir}/pydoc_data/*.py
%{py_scriptdir}/pydoc_data/*.css

%files -n idle3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/idle3
%attr(755,root,root) %{_bindir}/idle3.5
%dir %{py_scriptdir}/idlelib/Icons
%{py_scriptdir}/idlelib/__pycache__
%{py_scriptdir}/idlelib/*.py
%doc %{py_scriptdir}/idlelib/*.txt
%doc %{py_scriptdir}/idlelib/ChangeLog
%{py_scriptdir}/idlelib/Icons/*
%{py_scriptdir}/idlelib/*.def

%files devel
%defattr(644,root,root,755)
%doc Misc/{ACKS,NEWS,README,README.valgrind,valgrind-python.supp}
%attr(755,root,root) %{_bindir}/python%{py_ver}-config
%attr(755,root,root) %{_bindir}/python%{py_abi}-config
%attr(755,root,root) %{_bindir}/python3-config
%attr(755,root,root) %{_libdir}/libpython%{py_abi}.so
%attr(755,root,root) %{_libdir}/libpython3.so
%{py_incdir}/*.h
%exclude %{py_incdir}/pyconfig.h
%attr(755,root,root) %{py_libdir}/config-%{py_abi}/makesetup
%attr(755,root,root) %{py_libdir}/config-%{py_abi}/install-sh
%{py_libdir}/config-%{py_abi}/config.c
%{py_libdir}/config-%{py_abi}/config.c.in
%{py_libdir}/config-%{py_abi}/python.o
%{py_libdir}/config-%{py_abi}/python-config.py
%{_pkgconfigdir}/python-%{py_ver}.pc
%{_pkgconfigdir}/python-%{py_abi}.pc
%{_pkgconfigdir}/python3.pc

%files devel-tools
%defattr(644,root,root,755)
/etc/shrc.d/python*-devel*
%attr(755,root,root) %{_bindir}/pygettext%{py_ver}
%attr(755,root,root) %{_bindir}/pyreindent%{py_ver}
%{py_scriptdir}/pdb.py
%{py_scriptdir}/profile.py
%{py_scriptdir}/pstats.py
%{py_scriptdir}/timeit.py
%{py_scriptdir}/__pycache__/pdb.cpython-*.py[co]
%{py_scriptdir}/__pycache__/profile.cpython-*.py[co]
%{py_scriptdir}/__pycache__/pstats.cpython-*.py[co]
%{py_scriptdir}/__pycache__/timeit.cpython-*.py[co]

%files 2to3
%attr(755,root,root) %{_bindir}/2to3-%{py_ver}
%dir %{py_scriptdir}/lib2to3
%{py_scriptdir}/lib2to3/__pycache__
%{py_scriptdir}/lib2to3/*.txt
%{py_scriptdir}/lib2to3/*.pickle
%{py_scriptdir}/lib2to3/*.py
%dir %{py_scriptdir}/lib2to3/fixes
%{py_scriptdir}/lib2to3/fixes/__pycache__
%{py_scriptdir}/lib2to3/fixes/*.py
%dir %{py_scriptdir}/lib2to3/pgen2
%{py_scriptdir}/lib2to3/pgen2/__pycache__
%{py_scriptdir}/lib2to3/pgen2/*.py

%files static
%defattr(644,root,root,755)
%{_libdir}/libpython%{py_abi}.a

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files test
%{py_scriptdir}/idlelib/idle_test
%{py_scriptdir}/test
%{py_scriptdir}/ctypes/test
%{py_scriptdir}/distutils/tests
%{py_scriptdir}/lib2to3/tests
%{py_scriptdir}/sqlite3/test
%{py_scriptdir}/tkinter/test
%{py_scriptdir}/unittest/test

%if %{with info}
%files doc-info
%defattr(644,root,root,755)
%{_infodir}/*.info*
%endif

%if %{with tkinter}
%files tkinter
%defattr(644,root,root,755)
%dir %{py_scriptdir}/tkinter
%{py_scriptdir}/tkinter/__pycache__
%{py_scriptdir}/tkinter/*.py
%attr(755,root,root) %{py_dyndir}/_tkinter.cpython-*.so
%endif
