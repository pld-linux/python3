# NOTE: tests require processes limit >128 (256 is sufficient)
#
# Conditional build:
%bcond_with	info			# info pages (requires emacs)
%bcond_without	system_mpdecimal	# system libmpdec library
%bcond_without	tkinter			# disables tkinter module building
%bcond_without	tests			# disables Python testing
%bcond_with	verbose_tests		# runs tests in verbose mode
%bcond_without	optimizations		# expensive, stable optimizations (PGO etc.) + LTO
%bcond_with	semantic_interposition	# build without \-fno-semantic-interposition
#
# tests which will not work on 64-bit platforms
%define		no64bit_tests	-x test_audioop -x test_rgbimg -x test_imageop
# tests which may fail because of builder environment limitations (no /proc or /dev/pts)
%define		nobuilder_tests -u-network -x test_resource -x test_openpty -x test_socket -x test_nis -x test_posix -x test_locale -x test_pty -x test_asyncio -x test_os -x test_readline -x test_normalization

# tests which fail because of some unknown/unresolved reason (this list should be %{nil})
#   test_site: fails because our site.py is patched to include both /usr/share/... and /usr/lib...
#   test_gdb: fails, as the gdb uses old python version
#   test_time: test_AsTimeval (test.test_time.TestCPyTime), rounding error
%ifarch x32
%define		broken_tests_x32	-x test_time
%undefine	with_optimizations
%endif
%define		broken_tests	-x test_embed -x test_nntplib -x test_gdb -x test_site -x test_distutils -x test_bdist_rpm -x test_ssl %{?broken_tests_x32}

%ifarch armv6hl armv7hl armv7hnl
%define		_python_target_abi	%{?_gnu}hf
%else
%define		_python_target_abi	%{?_gnu}
%endif

%define py_ver		3.9
%define py_abi		%{py_ver}
%define	py_platform	%{py_abi}-%{_target_base_arch}-%{_target_os}%{?_python_target_abi}
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
Version:	%{py_ver}.10
Release:	1
Epoch:		1
License:	PSF
Group:		Development/Languages/Python
Source0:	https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
# Source0-md5:	e754c4b2276750fd5b4785a1b443683a
Source1:	pyconfig.h.in
Patch0:		%{name}-pythonpath.patch
Patch1:		%{name}-ac_fixes.patch
Patch2:		%{name}-multilib.patch
Patch3:		%{name}-no_cmdline_tests.patch
Patch4:		%{name}-makefile-location.patch
Patch5:		%{name}-config.patch
Patch6:		%{name}-BLDLIBRARY.patch
Patch7:		%{name}-db.patch
Patch8:		%{name}-install_prefix.patch
Patch9:		%{name}-tests_with_pythonpath.patch
Patch10:	%{name}-bdist_rpm.patch
Patch11:	%{name}-installcompile.patch

Patch13:	%{name}-no-randomize-tests.patch
Patch14:	python3-profile-tests.patch
Patch15:	python3-tests.patch
URL:		https://www.python.org/
BuildRequires:	autoconf >= 2.65
BuildRequires:	autoconf-archive
BuildRequires:	automake
BuildRequires:	bluez-libs-devel
BuildRequires:	bzip2-devel
BuildRequires:	db-devel >= 4
%{?with_info:BuildRequires:	emacs >= 21}
BuildRequires:	expat-devel >= 1:1.95.7
BuildRequires:	file
BuildRequires:	gdbm-devel >= 1.8.3
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	gmp-devel >= 4.0
BuildRequires:	libffi-devel
BuildRequires:	libnsl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtirpc-devel
%{?with_system_mpdecimal:BuildRequires:	mpdecimal-devel >= 2.5.0}
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
Suggests:	pip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ppc	-D__ppc__=1
%define		specflags_ppc64	-D__ppc64__=1

%if %{with verbose_tests}
%define test_flags -v
%else
%define test_flags -wW
%endif

%ifarch alpha ia64 ppc64 sparc64 ppc64 %{x8664}
%define test_list %{nobuilder_tests} %{broken_tests} %{no64bit_tests}
%else
%define test_list %{nobuilder_tests} %{broken_tests}
%endif

%ifarch sparc
%define test_list %{nobuilder_tests} %{broken_tests} -x test_fcntl -x test_ioctl
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
Provides:	python3-enum
Obsoletes:	python3-enum < 0.5
%{!?with_info:Obsoletes:	python3-doc-info < %{epoch}:%{version}-%{release}}

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
%{?with_system_mpdecimal:Requires:	mpdecimal >= 2.4.2-2}
Obsoletes:	python3-modules-sqlite < 1:3.1-2
%requires_ge_to	openssl openssl-devel

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
Obsoletes:	python3-devel-src < 1:3.2-1

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
Group:		Development/Languages/Python

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
BuildArch:	noarch

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
%patch10 -p1
%patch11 -p1

%patch13 -p1
%patch14 -p1
%patch15 -p1

%{__rm} -r Modules/expat

for SUBDIR in darwin libffi_osx; do
	%{__rm} -r Modules/_ctypes/$SUBDIR/*
done

%if "%{pld_release}" == "ac"
files="md5module.c sha1module.c"
files="$files sha256module.c sha512module.c"
for f in $files; do
	%{__rm} Modules/$f
done
%endif

sed -E -i -e '1s,#!\s*/usr/bin/env\s+python2(\s|$),#!%{__python}\1,' -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python}\1,' -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python}\1,' \
      Tools/gdb/libpython.py \
      Tools/pynche/pynche \
      Tools/pynche/pynche.pyw \
      Tools/scripts/2to3

sed -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      Tools/scripts/idle3 \
      Tools/scripts/pydoc3

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
	OPT="%{rpmcflags}" \
	CFLAGS_NODIST="%{!?with_semantic_interposition: -fno-semantic-interposition}" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	LDFLAGS_NODIST="%{debuginfocflags}%{!?with_semantic_interposition: -fno-semantic-interposition}" \
	ac_cv_posix_semaphores_enabled=yes \
	ac_cv_broken_sem_getvalue=no \
	--enable-ipv6 \
	--enable-shared \
	--with-computed-gotos \
	--with-dbmliborder=gdbm:ndbm:bdb \
	--with-doc-strings \
	--without-ensurepip \
        --with-platlibdir="%{_lib}" \
	%{?with_debug:--with-pydebug} \
        --with-ssl-default-suites=openssl \
	--with-system-expat \
	--with-system-ffi \
	%{?with_system_mpdecimal:--with-system-libmpdec} \
%if %{with optimizations}
	--enable-optimizations \
	--with-lto
%endif

if grep -q "#define POSIX_SEMAPHORES_NOT_ENABLED 1" pyconfig.h; then
      echo "Please ensure that /dev/shm is mounted as a tmpfs with mode 1777." >&2
      exit 1
fi

%{__make} \
	TESTOPTS="%{_smp_mflags} %{test_list}" \
	2>&1 | awk '
BEGIN { fail = 0; logmsg = ""; }
{
		if ($0 ~ /\*\*\* WARNING:/) {
				fail = 1;
				logmsg = logmsg $0;
		}
		print $0;
}
END { if (fail) { print "\nPROBLEMS FOUND:"; print logmsg; exit(1); } }'

LC_ALL=C.UTF-8
export LC_ALL
%if %{with tests}
WITHIN_PYTHON_RPM_BUILD=1 %{__make} test \
	TESTOPTS="%{test_flags} %{test_list}"
%endif

%if %{with info}
%{__make} -C Doc texinfo
%{__make} -C Doc/build/texinfo info
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pkgconfigdir}} \
	$RPM_BUILD_ROOT{%{py_sitedir},%{py_sitescriptdir}}/__pycache__ \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT{%{_infodir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT/etc/shrc.d \
	$RPM_BUILD_ROOT%{_prefix}/lib/debug/%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with info}
cp -p Doc/build/texinfo/python*info* $RPM_BUILD_ROOT%{_infodir}
%endif

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a Tools $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# make libpython3.so simply symlink to real lib
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpython3.so
ln -s libpython%{py_abi}.so $RPM_BUILD_ROOT%{_libdir}/libpython3.so

# gdb helper that will end up in -debuginfo package
soname=$(ls -1d $RPM_BUILD_ROOT%{_libdir}/libpython%{py_abi}.so.*.* | sed -e "s#^$RPM_BUILD_ROOT##g")
cp -a Tools/gdb/libpython.py "$RPM_BUILD_ROOT%{_prefix}/lib/debug/$soname-gdb.py"

#
# create several useful aliases, such as timeit.py, profile.py, pdb.py, smtpd.py
#

# for python devel tools
for script in timeit profile pdb pstats; do
	echo "#alias ${script}%{py_ver}.py='python%{py_ver} -m ${script}'"
done > $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh

echo "#alias pygettext%{py_ver}.py='pygettext%{py_ver}'" \
	>> $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh

sed 's/=/ /' \
	< $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh \
	> $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.csh

# for python modules
for script in smtpd webbrowser; do
	echo "#alias ${script}%{py_ver}.py='python%{py_ver} -m ${script}'"
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
%{__rm} $RPM_BUILD_ROOT%{py_libdir}/ctypes/macholib/fetch_macholib*
%{__rm} $RPM_BUILD_ROOT%{py_libdir}/idlelib/*.bat
%{__rm} $RPM_BUILD_ROOT%{py_libdir}/idlelib/*.pyw
%{__rm} $RPM_BUILD_ROOT%{py_libdir}/idlelib/help.html
%{__rm} $RPM_BUILD_ROOT%{py_libdir}/site-packages/README.txt

# currently provided by python-2to3, consider switching to this one
%{__rm} $RPM_BUILD_ROOT%{_bindir}/2to3

# that seems to be only an empty extension template,
# which seems to be built only {with tests}
%{__rm} -f $RPM_BUILD_ROOT%{py_dyndir}/xxlimited.*.so

# already in %%doc
%{__rm} $RPM_BUILD_ROOT%{py_libdir}/LICENSE.txt

%{__mv} $RPM_BUILD_ROOT%{py_incdir}/pyconfig.h $RPM_BUILD_ROOT%{py_libdir}/config-%{py_platform}/pyconfig.h
%{__sed} -e's#@PREFIX@#%{_prefix}#g;s#@PY_VER@#%{py_ver}#g;s#@PY_ABI@#%{py_platform}#g' %{SOURCE1} > $RPM_BUILD_ROOT%{py_incdir}/pyconfig.h

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
%if "%{py_ver}" != "%{py_abi}"
%attr(755,root,root) %{_bindir}/python%{py_abi}
%endif
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
%dir %{py_libdir}/__pycache__
%dir %{py_scriptdir}
%dir %{py_sitescriptdir}
%dir %{py_sitescriptdir}/__pycache__

# shared modules required by python library
%attr(755,root,root) %{py_dyndir}/_struct.cpython-*.so

# modules required by python library
%{py_libdir}/_collections_abc.py
%{py_libdir}/_sitebuiltins.py
%{py_libdir}/_sysconfigdata_*.py
%{py_libdir}/_weakrefset.py
%{py_libdir}/abc.py
%{py_libdir}/bisect.py
%{py_libdir}/codecs.py
%{py_libdir}/copyreg.py
%{py_libdir}/enum.py
%{py_libdir}/functools.py
%{py_libdir}/genericpath.py
%{py_libdir}/heapq.py
%{py_libdir}/keyword.py
%{py_libdir}/linecache.py
%{py_libdir}/locale.py
%{py_libdir}/io.py
%{py_libdir}/operator.py
%{py_libdir}/posixpath.py
%{py_libdir}/re.py
%{py_libdir}/reprlib.py
%{py_libdir}/site.py
%{py_libdir}/sre_*.py
%{py_libdir}/stat.py
%{py_libdir}/sysconfig.py
%{py_libdir}/token.py
%{py_libdir}/tokenize.py
%{py_libdir}/traceback.py
%{py_libdir}/weakref.py
%{py_libdir}/os.py
# needed by the dynamic sys.lib patch
%{py_libdir}/types.py
%{py_libdir}/__pycache__/_sitebuiltins.cpython-*.py[co]
%{py_libdir}/__pycache__/_sysconfigdata_*.cpython-*.py[co]
%{py_libdir}/__pycache__/_weakrefset.cpython-*.py[co]
%{py_libdir}/__pycache__/abc.cpython-*.py[co]
%{py_libdir}/__pycache__/bisect.cpython-*.py[co]
%{py_libdir}/__pycache__/codecs.cpython-*.py[co]
%{py_libdir}/__pycache__/_collections_abc.cpython-*.py[co]
%{py_libdir}/__pycache__/copyreg.cpython-*.py[co]
%{py_libdir}/__pycache__/enum.cpython-*.py[co]
%{py_libdir}/__pycache__/functools.cpython-*.py[co]
%{py_libdir}/__pycache__/genericpath.cpython-*.py[co]
%{py_libdir}/__pycache__/heapq.cpython-*.py[co]
%{py_libdir}/__pycache__/keyword.cpython-*.py[co]
%{py_libdir}/__pycache__/linecache.cpython-*.py[co]
%{py_libdir}/__pycache__/locale.cpython-*.py[co]
%{py_libdir}/__pycache__/io.cpython-*.py[co]
%{py_libdir}/__pycache__/operator.cpython-*.py[co]
%{py_libdir}/__pycache__/posixpath.cpython-*.py[co]
%{py_libdir}/__pycache__/re.cpython-*.py[co]
%{py_libdir}/__pycache__/reprlib.cpython-*.py[co]
%{py_libdir}/__pycache__/site.cpython-*.py[co]
%{py_libdir}/__pycache__/sre_*.cpython-*.py[co]
%{py_libdir}/__pycache__/stat.cpython-*.py[co]
%{py_libdir}/__pycache__/sysconfig.cpython-*.py[co]
%{py_libdir}/__pycache__/token.cpython-*.py[co]
%{py_libdir}/__pycache__/tokenize.cpython-*.py[co]
%{py_libdir}/__pycache__/traceback.cpython-*.py[co]
%{py_libdir}/__pycache__/weakref.cpython-*.py[co]
%{py_libdir}/__pycache__/os.cpython-*.py[co]
%{py_libdir}/__pycache__/types.cpython-*.py[co]

%{py_libdir}/collections

# encodings required by python library
%dir %{py_libdir}/encodings
%{py_libdir}/encodings/__pycache__
%{py_libdir}/encodings/*.py

%dir %{py_libdir}/config-%{py_platform}
%{py_libdir}/config-%{py_platform}/Makefile
%{py_libdir}/config-%{py_platform}/Setup
%{py_libdir}/config-%{py_platform}/Setup.local
%{py_libdir}/config-%{py_platform}/pyconfig.h

%files modules
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/shrc.d/python*-modules*
%{py_libdir}/__future__.py
%{py_libdir}/__phello__.foo.py
%{py_libdir}/_aix_support.py
%{py_libdir}/_bootlocale.py
%{py_libdir}/_bootsubprocess.py
%{py_libdir}/_compat_pickle.py
%{py_libdir}/_compression.py
%{py_libdir}/_markupbase.py
%{py_libdir}/_osx_support.py
%{py_libdir}/_pydecimal.py
%{py_libdir}/_py_abc.py
%{py_libdir}/_pyio.py
%{py_libdir}/_strptime.py
%{py_libdir}/_threading_local.py
%{py_libdir}/aifc.py
%{py_libdir}/antigravity.py
%{py_libdir}/argparse.py
%{py_libdir}/ast.py
%{py_libdir}/asynchat.py
%{py_libdir}/asyncore.py
%{py_libdir}/base64.py
%{py_libdir}/bdb.py
%{py_libdir}/binhex.py
%{py_libdir}/bz2.py
%{py_libdir}/cProfile.py
%{py_libdir}/calendar.py
%{py_libdir}/cgi.py
%{py_libdir}/cgitb.py
%{py_libdir}/chunk.py
%{py_libdir}/cmd.py
%{py_libdir}/code.py
%{py_libdir}/codeop.py
%{py_libdir}/colorsys.py
%{py_libdir}/compileall.py
%{py_libdir}/configparser.py
%{py_libdir}/contextlib.py
%{py_libdir}/contextvars.py
%{py_libdir}/copy.py
%{py_libdir}/crypt.py
%{py_libdir}/csv.py
%{py_libdir}/dataclasses.py
%{py_libdir}/datetime.py
%{py_libdir}/decimal.py
%{py_libdir}/difflib.py
%{py_libdir}/dis.py
%{py_libdir}/doctest.py
%{py_libdir}/filecmp.py
%{py_libdir}/fileinput.py
%{py_libdir}/fnmatch.py
%{py_libdir}/formatter.py
%{py_libdir}/fractions.py
%{py_libdir}/ftplib.py
%{py_libdir}/getopt.py
%{py_libdir}/getpass.py
%{py_libdir}/gettext.py
%{py_libdir}/glob.py
%{py_libdir}/graphlib.py
%{py_libdir}/gzip.py
%{py_libdir}/hashlib.py
%{py_libdir}/hmac.py
%{py_libdir}/imaplib.py
%{py_libdir}/imghdr.py
%{py_libdir}/imp.py
%{py_libdir}/inspect.py
%{py_libdir}/ipaddress.py
%{py_libdir}/lzma.py
%{py_libdir}/mailbox.py
%{py_libdir}/mailcap.py
%{py_libdir}/mimetypes.py
%{py_libdir}/modulefinder.py
%{py_libdir}/netrc.py
%{py_libdir}/nntplib.py
%{py_libdir}/ntpath.py
%{py_libdir}/nturl2path.py
%{py_libdir}/numbers.py
%{py_libdir}/opcode.py
%{py_libdir}/optparse.py
%{py_libdir}/pathlib.py
%{py_libdir}/pickle.py
%{py_libdir}/pickletools.py
%{py_libdir}/pipes.py
%{py_libdir}/pkgutil.py
%{py_libdir}/platform.py
%{py_libdir}/plistlib.py
%{py_libdir}/poplib.py
%{py_libdir}/pprint.py
%{py_libdir}/pty.py
%{py_libdir}/py_compile.py
%{py_libdir}/pyclbr.py
%{py_libdir}/queue.py
%{py_libdir}/quopri.py
%{py_libdir}/random.py
%{py_libdir}/rlcompleter.py
%{py_libdir}/runpy.py
%{py_libdir}/secrets.py
%{py_libdir}/signal.py
%{py_libdir}/sched.py
%{py_libdir}/selectors.py
%{py_libdir}/shelve.py
%{py_libdir}/shlex.py
%{py_libdir}/shutil.py
%{py_libdir}/smtpd.py
%{py_libdir}/smtplib.py
%{py_libdir}/sndhdr.py
%{py_libdir}/socket.py
%{py_libdir}/socketserver.py
%{py_libdir}/ssl.py
%{py_libdir}/statistics.py
%{py_libdir}/string.py
%{py_libdir}/stringprep.py
%{py_libdir}/struct.py
%{py_libdir}/subprocess.py
%{py_libdir}/sunau.py
%{py_libdir}/symbol.py
%{py_libdir}/symtable.py
%{py_libdir}/tabnanny.py
%{py_libdir}/tarfile.py
%{py_libdir}/telnetlib.py
%{py_libdir}/tempfile.py
%{py_libdir}/textwrap.py
%{py_libdir}/this.py
%{py_libdir}/threading.py
%{py_libdir}/trace.py
%{py_libdir}/tracemalloc.py
%{py_libdir}/tty.py
%{py_libdir}/turtle.py
%{py_libdir}/typing.py
%{py_libdir}/uu.py
%{py_libdir}/uuid.py
%{py_libdir}/warnings.py
%{py_libdir}/wave.py
%{py_libdir}/webbrowser.py
%{py_libdir}/xdrlib.py
%{py_libdir}/zipapp.py
%{py_libdir}/zipfile.py
%{py_libdir}/zipimport.py
%{py_libdir}/__pycache__/__future__.cpython-*.py[co]
%{py_libdir}/__pycache__/__phello__.foo.cpython-*.py[co]
%{py_libdir}/__pycache__/_aix_support.cpython-*.py[co]
%{py_libdir}/__pycache__/_bootlocale.cpython-*.py[co]
%{py_libdir}/__pycache__/_bootsubprocess.cpython-*.py[co]
%{py_libdir}/__pycache__/_compat_pickle.cpython-*.py[co]
%{py_libdir}/__pycache__/_compression.cpython-*.py[co]
%{py_libdir}/__pycache__/_markupbase.cpython-*.py[co]
%{py_libdir}/__pycache__/_osx_support.cpython-*.py[co]
%{py_libdir}/__pycache__/_pydecimal.cpython-*.py[co]
%{py_libdir}/__pycache__/_py_abc.cpython-*.py[co]
%{py_libdir}/__pycache__/_pyio.cpython-*.py[co]
%{py_libdir}/__pycache__/_strptime.cpython-*.py[co]
%{py_libdir}/__pycache__/_threading_local.cpython-*.py[co]
%{py_libdir}/__pycache__/aifc.cpython-*.py[co]
%{py_libdir}/__pycache__/antigravity.cpython-*.py[co]
%{py_libdir}/__pycache__/argparse.cpython-*.py[co]
%{py_libdir}/__pycache__/ast.cpython-*.py[co]
%{py_libdir}/__pycache__/asynchat.cpython-*.py[co]
%{py_libdir}/__pycache__/asyncore.cpython-*.py[co]
%{py_libdir}/__pycache__/base64.cpython-*.py[co]
%{py_libdir}/__pycache__/bdb.cpython-*.py[co]
%{py_libdir}/__pycache__/binhex.cpython-*.py[co]
%{py_libdir}/__pycache__/bz2.cpython-*.py[co]
%{py_libdir}/__pycache__/cProfile.cpython-*.py[co]
%{py_libdir}/__pycache__/calendar.cpython-*.py[co]
%{py_libdir}/__pycache__/cgi.cpython-*.py[co]
%{py_libdir}/__pycache__/cgitb.cpython-*.py[co]
%{py_libdir}/__pycache__/chunk.cpython-*.py[co]
%{py_libdir}/__pycache__/cmd.cpython-*.py[co]
%{py_libdir}/__pycache__/contextvars.cpython-*.py[co]
%{py_libdir}/__pycache__/code.cpython-*.py[co]
%{py_libdir}/__pycache__/codeop.cpython-*.py[co]
%{py_libdir}/__pycache__/colorsys.cpython-*.py[co]
%{py_libdir}/__pycache__/compileall.cpython-*.py[co]
%{py_libdir}/__pycache__/configparser.cpython-*.py[co]
%{py_libdir}/__pycache__/contextlib.cpython-*.py[co]
%{py_libdir}/__pycache__/copy.cpython-*.py[co]
%{py_libdir}/__pycache__/crypt.cpython-*.py[co]
%{py_libdir}/__pycache__/csv.cpython-*.py[co]
%{py_libdir}/__pycache__/dataclasses.cpython-*.py[co]
%{py_libdir}/__pycache__/datetime.cpython-*.py[co]
%{py_libdir}/__pycache__/decimal.cpython-*.py[co]
%{py_libdir}/__pycache__/difflib.cpython-*.py[co]
%{py_libdir}/__pycache__/dis.cpython-*.py[co]
%{py_libdir}/__pycache__/doctest.cpython-*.py[co]
%{py_libdir}/__pycache__/filecmp.cpython-*.py[co]
%{py_libdir}/__pycache__/fileinput.cpython-*.py[co]
%{py_libdir}/__pycache__/fnmatch.cpython-*.py[co]
%{py_libdir}/__pycache__/formatter.cpython-*.py[co]
%{py_libdir}/__pycache__/fractions.cpython-*.py[co]
%{py_libdir}/__pycache__/ftplib.cpython-*.py[co]
%{py_libdir}/__pycache__/getopt.cpython-*.py[co]
%{py_libdir}/__pycache__/getpass.cpython-*.py[co]
%{py_libdir}/__pycache__/gettext.cpython-*.py[co]
%{py_libdir}/__pycache__/glob.cpython-*.py[co]
%{py_libdir}/__pycache__/graphlib.cpython-*.py[co]
%{py_libdir}/__pycache__/gzip.cpython-*.py[co]
%{py_libdir}/__pycache__/hashlib.cpython-*.py[co]
%{py_libdir}/__pycache__/hmac.cpython-*.py[co]
%{py_libdir}/__pycache__/imaplib.cpython-*.py[co]
%{py_libdir}/__pycache__/imghdr.cpython-*.py[co]
%{py_libdir}/__pycache__/imp.cpython-*.py[co]
%{py_libdir}/__pycache__/inspect.cpython-*.py[co]
%{py_libdir}/__pycache__/ipaddress.cpython-*.py[co]
%{py_libdir}/__pycache__/lzma.cpython-*.py[co]
%{py_libdir}/__pycache__/mailbox.cpython-*.py[co]
%{py_libdir}/__pycache__/mailcap.cpython-*.py[co]
%{py_libdir}/__pycache__/mimetypes.cpython-*.py[co]
%{py_libdir}/__pycache__/modulefinder.cpython-*.py[co]
%{py_libdir}/__pycache__/netrc.cpython-*.py[co]
%{py_libdir}/__pycache__/nntplib.cpython-*.py[co]
%{py_libdir}/__pycache__/ntpath.cpython-*.py[co]
%{py_libdir}/__pycache__/nturl2path.cpython-*.py[co]
%{py_libdir}/__pycache__/numbers.cpython-*.py[co]
%{py_libdir}/__pycache__/opcode.cpython-*.py[co]
%{py_libdir}/__pycache__/optparse.cpython-*.py[co]
%{py_libdir}/__pycache__/pathlib.cpython-*.py[co]
%{py_libdir}/__pycache__/pickle.cpython-*.py[co]
%{py_libdir}/__pycache__/pickletools.cpython-*.py[co]
%{py_libdir}/__pycache__/pipes.cpython-*.py[co]
%{py_libdir}/__pycache__/pkgutil.cpython-*.py[co]
%{py_libdir}/__pycache__/platform.cpython-*.py[co]
%{py_libdir}/__pycache__/plistlib.cpython-*.py[co]
%{py_libdir}/__pycache__/poplib.cpython-*.py[co]
%{py_libdir}/__pycache__/pprint.cpython-*.py[co]
%{py_libdir}/__pycache__/pty.cpython-*.py[co]
%{py_libdir}/__pycache__/py_compile.cpython-*.py[co]
%{py_libdir}/__pycache__/pyclbr.cpython-*.py[co]
%{py_libdir}/__pycache__/queue.cpython-*.py[co]
%{py_libdir}/__pycache__/quopri.cpython-*.py[co]
%{py_libdir}/__pycache__/random.cpython-*.py[co]
%{py_libdir}/__pycache__/rlcompleter.cpython-*.py[co]
%{py_libdir}/__pycache__/runpy.cpython-*.py[co]
%{py_libdir}/__pycache__/sched.cpython-*.py[co]
%{py_libdir}/__pycache__/secrets.cpython-*.py[co]
%{py_libdir}/__pycache__/selectors.cpython-*.py[co]
%{py_libdir}/__pycache__/shelve.cpython-*.py[co]
%{py_libdir}/__pycache__/shlex.cpython-*.py[co]
%{py_libdir}/__pycache__/shutil.cpython-*.py[co]
%{py_libdir}/__pycache__/signal.cpython-*.py[co]
%{py_libdir}/__pycache__/smtpd.cpython-*.py[co]
%{py_libdir}/__pycache__/smtplib.cpython-*.py[co]
%{py_libdir}/__pycache__/sndhdr.cpython-*.py[co]
%{py_libdir}/__pycache__/socket.cpython-*.py[co]
%{py_libdir}/__pycache__/socketserver.cpython-*.py[co]
%{py_libdir}/__pycache__/ssl.cpython-*.py[co]
%{py_libdir}/__pycache__/statistics.cpython-*.py[co]
%{py_libdir}/__pycache__/string.cpython-*.py[co]
%{py_libdir}/__pycache__/stringprep.cpython-*.py[co]
%{py_libdir}/__pycache__/struct.cpython-*.py[co]
%{py_libdir}/__pycache__/subprocess.cpython-*.py[co]
%{py_libdir}/__pycache__/sunau.cpython-*.py[co]
%{py_libdir}/__pycache__/symbol.cpython-*.py[co]
%{py_libdir}/__pycache__/symtable.cpython-*.py[co]
%{py_libdir}/__pycache__/tabnanny.cpython-*.py[co]
%{py_libdir}/__pycache__/tarfile.cpython-*.py[co]
%{py_libdir}/__pycache__/telnetlib.cpython-*.py[co]
%{py_libdir}/__pycache__/tempfile.cpython-*.py[co]
%{py_libdir}/__pycache__/textwrap.cpython-*.py[co]
%{py_libdir}/__pycache__/this.cpython-*.py[co]
%{py_libdir}/__pycache__/threading.cpython-*.py[co]
%{py_libdir}/__pycache__/trace.cpython-*.py[co]
%{py_libdir}/__pycache__/tracemalloc.cpython-*.py[co]
%{py_libdir}/__pycache__/tty.cpython-*.py[co]
%{py_libdir}/__pycache__/turtle.cpython-*.py[co]
%{py_libdir}/__pycache__/typing.cpython-*.py[co]
%{py_libdir}/__pycache__/uu.cpython-*.py[co]
%{py_libdir}/__pycache__/uuid.cpython-*.py[co]
%{py_libdir}/__pycache__/warnings.cpython-*.py[co]
%{py_libdir}/__pycache__/wave.cpython-*.py[co]
%{py_libdir}/__pycache__/webbrowser.cpython-*.py[co]
%{py_libdir}/__pycache__/xdrlib.cpython-*.py[co]
%{py_libdir}/__pycache__/zipapp.cpython-*.py[co]
%{py_libdir}/__pycache__/zipfile.cpython-*.py[co]
%{py_libdir}/__pycache__/zipimport.cpython-*.py[co]

#
# list .so modules to be sure that all of them are built
#

%attr(755,root,root) %{py_dyndir}/_asyncio.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_bisect.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_blake2.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_bz2.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_cn.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_hk.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_iso2022.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_jp.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_kr.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_codecs_tw.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_contextvars.cpython-*.so
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
%attr(755,root,root) %{py_dyndir}/_posixshmem.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_posixsubprocess.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_queue.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_random.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_sha1.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_sha3.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_socket.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_ssl.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_statistics.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testbuffer.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testcapi.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testinternalcapi.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testimportmultiple.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_testmultiphase.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_uuid.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_xxsubinterpreters.cpython-*.so
%attr(755,root,root) %{py_dyndir}/_xxtestfuzz.cpython-*.so

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

%dir %{py_libdir}/asyncio
%{py_libdir}/asyncio/__pycache__
%{py_libdir}/asyncio/*.py

%{py_libdir}/concurrent

%dir %{py_libdir}/ctypes
%dir %{py_libdir}/ctypes/macholib
%{py_libdir}/ctypes/__pycache__
%{py_libdir}/ctypes/macholib/__pycache__

%{py_libdir}/ctypes/*.py
%{py_libdir}/ctypes/macholib/*.py
%doc %{py_libdir}/ctypes/macholib/README.ctypes

%dir %{py_libdir}/curses
%{py_libdir}/curses/__pycache__
%{py_libdir}/curses/*.py

%dir %{py_libdir}/dbm
%{py_libdir}/dbm/__pycache__
%{py_libdir}/dbm/*.py

%dir %{py_libdir}/distutils
%dir %{py_libdir}/distutils/command
%doc %{py_libdir}/distutils/README
%{py_libdir}/distutils/__pycache__
%{py_libdir}/distutils/command/__pycache__
%{py_libdir}/distutils/*.py
%{py_libdir}/distutils/command/*.py
%{py_libdir}/distutils/command/command_template

%dir %{py_libdir}/email
%dir %{py_libdir}/email/mime
%{py_libdir}/email/__pycache__
%{py_libdir}/email/mime/__pycache__
%{py_libdir}/email/architecture.rst
%{py_libdir}/email/*.py
%{py_libdir}/email/mime/*.py

%dir %{py_libdir}/ensurepip
%{py_libdir}/ensurepip/__pycache__
%{py_libdir}/ensurepip/*.py
%{py_libdir}/ensurepip/_bundled

%dir %{py_libdir}/html
%{py_libdir}/html/*.py
%{py_libdir}/html/__pycache__

%dir %{py_libdir}/http
%{py_libdir}/http/__pycache__
%{py_libdir}/http/*.py

%dir %{py_libdir}/idlelib

%dir %{py_libdir}/importlib
%{py_libdir}/importlib/__pycache__
%{py_libdir}/importlib/*.py

%dir %{py_libdir}/json
%{py_libdir}/json/__pycache__
%{py_libdir}/json/*.py

%dir %{py_libdir}/logging
%{py_libdir}/logging/__pycache__
%{py_libdir}/logging/*.py

%dir %{py_libdir}/multiprocessing
%{py_libdir}/multiprocessing/__pycache__
%{py_libdir}/multiprocessing/*.py
%dir %{py_libdir}/multiprocessing/dummy
%{py_libdir}/multiprocessing/dummy/__pycache__
%{py_libdir}/multiprocessing/dummy/*.py

%{py_libdir}/turtledemo

%dir %{py_libdir}/unittest
%{py_libdir}/unittest/__pycache__
%{py_libdir}/unittest/*.py

%dir %{py_libdir}/urllib
%{py_libdir}/urllib/__pycache__
%{py_libdir}/urllib/*.py

%dir %{py_libdir}/venv
%{py_libdir}/venv/__pycache__
%{py_libdir}/venv/*.py
%dir %{py_libdir}/venv/scripts
%dir %{py_libdir}/venv/scripts/common
%{py_libdir}/venv/scripts/common/Activate.ps1
%{py_libdir}/venv/scripts/common/activate
%dir %{py_libdir}/venv/scripts/posix
%{py_libdir}/venv/scripts/posix/activate.csh
%{py_libdir}/venv/scripts/posix/activate.fish

%dir %{py_libdir}/wsgiref
%{py_libdir}/wsgiref/__pycache__
%{py_libdir}/wsgiref/*.py

%dir %{py_libdir}/xml
%dir %{py_libdir}/xml/dom
%dir %{py_libdir}/xml/etree
%dir %{py_libdir}/xml/parsers
%dir %{py_libdir}/xml/sax
%{py_libdir}/xml/__pycache__
%{py_libdir}/xml/dom/__pycache__
%{py_libdir}/xml/etree/__pycache__
%{py_libdir}/xml/parsers/__pycache__
%{py_libdir}/xml/sax/__pycache__
%{py_libdir}/xml/*.py
%{py_libdir}/xml/dom/*.py
%{py_libdir}/xml/etree/*.py
%{py_libdir}/xml/parsers/*.py
%{py_libdir}/xml/sax/*.py

%dir %{py_libdir}/xmlrpc
%{py_libdir}/xmlrpc/__pycache__
%{py_libdir}/xmlrpc/*.py

%attr(755,root,root) %{py_dyndir}/_sqlite3.cpython-*.so
%dir %{py_libdir}/sqlite3
%{py_libdir}/sqlite3/__pycache__
%{py_libdir}/sqlite3/*.py

%attr(755,root,root) %{py_dyndir}/_zoneinfo.cpython-*.so
%dir %{py_libdir}/zoneinfo
%{py_libdir}/zoneinfo/__pycache__
%{py_libdir}/zoneinfo/*.py

%files -n pydoc3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pydoc3
%attr(755,root,root) %{_bindir}/pydoc%{py_ver}
%{py_libdir}/pydoc.py
%{py_libdir}/__pycache__/pydoc.cpython-*.py[co]
%dir %{py_libdir}/pydoc_data
%{py_libdir}/pydoc_data/__pycache__
%{py_libdir}/pydoc_data/*.py
%{py_libdir}/pydoc_data/*.css

%files -n idle3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/idle3
%attr(755,root,root) %{_bindir}/idle%{py_ver}
%dir %{py_libdir}/idlelib/Icons
%{py_libdir}/idlelib/__pycache__
%{py_libdir}/idlelib/*.py
%doc %{py_libdir}/idlelib/*.txt
%doc %{py_libdir}/idlelib/ChangeLog
%{py_libdir}/idlelib/Icons/*
%{py_libdir}/idlelib/*.def

%files devel
%defattr(644,root,root,755)
%doc Misc/{ACKS,NEWS,README,README.valgrind,valgrind-python.supp}
%attr(755,root,root) %{_bindir}/python%{py_ver}-config
%if "%{py_ver}" != "%{py_abi}"
%attr(755,root,root) %{_bindir}/python%{py_abi}-config
%endif
%attr(755,root,root) %{_bindir}/python3-config
%attr(755,root,root) %{_libdir}/libpython%{py_abi}.so
%attr(755,root,root) %{_libdir}/libpython3.so
%{py_incdir}/*.h
%exclude %{py_incdir}/pyconfig.h
%{py_incdir}/cpython
%{py_incdir}/internal
%attr(755,root,root) %{py_libdir}/config-%{py_platform}/makesetup
%attr(755,root,root) %{py_libdir}/config-%{py_platform}/install-sh
%{py_libdir}/config-%{py_platform}/config.c
%{py_libdir}/config-%{py_platform}/config.c.in
%{py_libdir}/config-%{py_platform}/python.o
%{py_libdir}/config-%{py_platform}/python-config.py
%dir %{py_libdir}/config-%{py_platform}/__pycache__
%{py_libdir}/config-%{py_platform}/__pycache__/python-config.*
%{_pkgconfigdir}/python-%{py_ver}.pc
%{_pkgconfigdir}/python-%{py_ver}-embed.pc
%{_pkgconfigdir}/python3-embed.pc
%if "%{py_ver}" != "%{py_abi}"
%{_pkgconfigdir}/python-%{py_abi}.pc
%endif
%{_pkgconfigdir}/python3.pc

%files devel-tools
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/shrc.d/python*-devel*
%attr(755,root,root) %{_bindir}/pygettext%{py_ver}
%attr(755,root,root) %{_bindir}/pyreindent%{py_ver}
%{py_libdir}/pdb.py
%{py_libdir}/profile.py
%{py_libdir}/pstats.py
%{py_libdir}/timeit.py
%{py_libdir}/__pycache__/pdb.cpython-*.py[co]
%{py_libdir}/__pycache__/profile.cpython-*.py[co]
%{py_libdir}/__pycache__/pstats.cpython-*.py[co]
%{py_libdir}/__pycache__/timeit.cpython-*.py[co]

%files 2to3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/2to3-%{py_ver}
%dir %{py_libdir}/lib2to3
%{py_libdir}/lib2to3/__pycache__
%{py_libdir}/lib2to3/*.txt
%{py_libdir}/lib2to3/*.pickle
%{py_libdir}/lib2to3/*.py
%dir %{py_libdir}/lib2to3/fixes
%{py_libdir}/lib2to3/fixes/__pycache__
%{py_libdir}/lib2to3/fixes/*.py
%dir %{py_libdir}/lib2to3/pgen2
%{py_libdir}/lib2to3/pgen2/__pycache__
%{py_libdir}/lib2to3/pgen2/*.py

%files static
%defattr(644,root,root,755)
%{_libdir}/libpython%{py_abi}.a

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files test
%defattr(644,root,root,755)
%{py_libdir}/idlelib/idle_test
%{py_libdir}/test
%{py_libdir}/ctypes/test
%{py_libdir}/distutils/tests
%{py_libdir}/lib2to3/tests
%{py_libdir}/sqlite3/test
%{py_libdir}/tkinter/test
%{py_libdir}/unittest/test

%if %{with info}
%files doc-info
%defattr(644,root,root,755)
%{_infodir}/python.info*
%endif

%if %{with tkinter}
%files tkinter
%defattr(644,root,root,755)
%dir %{py_libdir}/tkinter
%{py_libdir}/tkinter/__pycache__
%{py_libdir}/tkinter/*.py
%attr(755,root,root) %{py_dyndir}/_tkinter.cpython-*.so
%endif
