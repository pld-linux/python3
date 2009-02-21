
# Conditional build:
%bcond_with	info			# info pages (requires emacs)
%bcond_without	tkinter			# disables tkinter module building
%bcond_without	tests			# disables Python testing
%bcond_with	verbose_tests		# runs tests in verbose mode
%bcond_with	openssl097
#
# tests which will not work on 64-bit platforms
%define		no64bit_tests	test_audioop test_rgbimg test_imageop
# tests which may fail because of builder environment limitations (no /proc or /dev/pts)
%define		nobuilder_tests test_resource test_openpty test_socket test_nis test_posix test_locale test_pty
# tests which fail because of some unknown/unresolved reason (this list should be empty)
%define		broken_tests test_anydbm test_bsddb test_re test_shelve test_whichdb test_zipimport test_distutils

%define	beta		%{nil}

%define py_ver		3.0
%define py_prefix	%{_prefix}
%define py_libdir	%{py_prefix}/%{_lib}/python%{py_ver}
%define py_incdir	%{_includedir}/python%{py_ver}
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
Name:		python30
Version:	%{py_ver}.1
Release:	0.1
Epoch:		1
License:	PSF
Group:		Applications
Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}%{beta}.tar.bz2
# Source0-md5:	7291eac6a9a7a3642e309c78b8d744e5
Patch1:		%{name}-pythonpath.patch
Patch2:		%{name}-no_ndbm.patch
Patch3:		%{name}-ac_fixes.patch
Patch4:		%{name}-noarch_to_datadir.patch
Patch5:		%{name}-lib64.patch
Patch6:		%{name}-doc_path.patch
Patch7:		%{name}-db4.6.patch
URL:		http://www.python.org/
BuildRequires:	autoconf
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
BuildRequires:	ncurses-ext-devel >= 5.2
%if %{with openssl097}
BuildRequires:	openssl-devel < 0.9.8
%else
BuildRequires:	openssl-devel >= 0.9.8
%endif
BuildRequires:	readline-devel >= 5.0
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.3.5
%{?with_info:BuildRequires:	tetex-makeindex}
%{?with_tkinter:BuildRequires:	tix-devel >= 1:8.1.4-4}
%{?with_tkinter:BuildRequires:	tk-devel >= 8.4.3}
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with verbose_tests}
%define test_flags -v -l -x
%else
%define test_flags -l -x
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
%{!?with_info:Obsoletes:	python30-doc-info}

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

%description modules
Python officially distributed modules.

%description modules -l pl.UTF-8
Oficjalnie rozprowadzane moduły języka Python.

%package modules-sqlite
Summary:	Python SQLite modules
Summary(pl.UTF-8):	Moduły SQLite języka Python
Group:		Libraries/Python
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description modules-sqlite
Python officially distributed sqlite module.

%description modules-sqlite -l pl.UTF-8
Oficjalnie rozprowadzany moduł sqlite języka Python.

%package -n pydoc30
Summary:	Python interactive module documentation access support
Summary(pl.UTF-8):	Interaktywne korzystanie z dokumentacji modułów języka Python
Group:		Applications
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description -n pydoc30
Python interactive module documentation access support.

%description -n pydoc30 -l pl.UTF-8
Interaktywne korzystanie z dokumentacji modułów języka Python.

%package -n idle30
Summary:	IDE for Python language
Summary(pl.UTF-8):	IDE dla języka Python
Group:		Applications
Requires:	%{name}-tkinter = %{epoch}:%{version}-%{release}

%description -n idle30
IDE for Python language.

%description -n idle30 -l pl.UTF-8
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
Obsoletes:	python-devel

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

%package static
Summary:	Static python library
Summary(pl.UTF-8):	Statyczna biblioteka Pythona
Group:		Development/Languages/Python
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static python library.

%description static -l pl.UTF-8
Statyczna biblioteka Pythona.

%package doc
Summary:	Documentation on Python
Summary(de.UTF-8):	Dokumentation zu Python
Summary(es.UTF-8):	Documentación para Python
Summary(fr.UTF-8):	Documentation sur Python
Summary(pl.UTF-8):	Dokumentacja do Pythona
Summary(pt_BR.UTF-8):	Documentação para a linguagem de programação Python
Summary(ru.UTF-8):	Документация по языку Python
Summary(tr.UTF-8):	Python belgeleri
Summary(uk.UTF-8):	Документація по мові Python
Group:		Documentation

%description doc
This package contains documentation on the Python language and
interpretor as a mix of plain ASCII files and LaTeX sources.

%description doc -l de.UTF-8
Dieses Paket enthält Dokumentationen zu Python (Sprache und
Interpreter) in Form von einfachen ASCII-Dateien und LaTeX-Quellen.

%description doc -l es.UTF-8
Documentación para Python. Contiene archivos en texto y PostScript.

%description doc -l fr.UTF-8
Ce paquetage contient la documentation sur le langage python et sur
son interpréteur sous forme de fichiers ASCII et LaTeX.

%description doc -l pl.UTF-8
Oficjalna dokumentacja do Pythona. Zawiera przykładowe programy,
narzędzia i dokumentację. Strony podręcznika man znajdują się w
głównym pakiecie. Ten pakiet nie zawiera źródeł dokumentacji
napisanych w LaTeXu, tylko gotowe do wykorzystania pliki postscriptowe
i HTML.

%description doc -l pt_BR.UTF-8
O pacote python-doc contém documentação para a linguagem de
programação e para o interpretador Python. Fornecida em arquivos texto
e Postcript.

%description doc -l ru.UTF-8
Этот пакет содержит документацию по собственно языку Python и по
исполняющему его интерпретатору в виде набора текстовых файлов и
исходных текстов в формате LaTeX.

%description doc -l tr.UTF-8
Bu paket, Python dili ile ilgili belgeleri ve düz ASCII dosyaları ve
LaTeX kaynaklarının bir karışımı olan yorumlayıcıyı içerir.

%description doc -l uk.UTF-8
Цей пакет містить документацію по власне мові Python та по виконуючому
її інтерпретатору у вигляді набора текстових файлів та вихідних
текстів у форматі LaTeX.

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

%prep
%setup -q -n Python-%{version}%{beta}
#patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
#patch4 -p1
#patch6 -p1
#patch7 -p1

%build
sed -i -e 's#-ltermcap#-ltinfo#g' configure*
%{__autoconf}
CPPFLAGS="-I/usr/include/ncursesw"; export CPPFLAGS
%configure \
	--with-cxx-main="%{__cxx}" \
	--enable-shared \
	--enable-ipv6 \
	--with-wide-unicode \
	--with-signal-module \
	--with-tsc \
	--with-threads \
	--with-doc-strings \
	--with-wctype-functions \
	--with-fpectl \
	--with-system-ffi \
	LINKCC='$(PURIFY) $(CXX)' \
	LDSHARED='$(CC) $(CFLAGS) -shared' \
	BLDSHARED='$(CC) $(CFLAGS) -shared' \
	LDFLAGS="%{rpmcflags} %{rpmldflags}"

%{__make} \
	OPT="%{rpmcflags}" 2>&1 | awk '
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
%{__make} test \
	TESTOPTS="%{test_flags} %{test_list}" \
	TESTPYTHON="LD_LIBRARY_PATH=`pwd` PYTHONHOME=`pwd` PYTHONPATH=`pwd`/Lib:$binlibdir ./python -tt"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{py_sitedir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT%{_infodir} \
	$RPM_BUILD_ROOT/etc/shrc.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with info}
%{__make} -C Doc/info
install Doc/info/python*info* $RPM_BUILD_ROOT%{_infodir}
%endif

install Makefile.pre.in $RPM_BUILD_ROOT%{py_libdir}/config

mv $RPM_BUILD_ROOT{%{py_libdir}/config,%{_libdir}}/libpython%{py_ver}.a
ln -sf libpython%{py_ver}.a $RPM_BUILD_ROOT%{_libdir}/libpython.a
ln -sf libpython%{py_ver}.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libpython.so
ln -sf libpython%{py_ver}.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libpython%{py_ver}.so

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a Tools Demo $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

#
# create several useful aliases, such as timeit.py, profile.py, pdb.py, smtpd.py
#

# for python devel tools
for script in timeit profile pdb pstats; do
    echo alias ${script}%{py_ver}.py=\"python%{py_ver} -m ${script}\"
done > $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh

echo alias pygettext%{py_ver}.py='"pygettext%{py_ver}"' \
	>> $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh

sed 's/=/ /' \
	< $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.sh \
	> $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-devel.csh

# for python modules
for script in smtpd webbrowser; do
    echo alias ${script}%{py_ver}.py=\"python%{py_ver} -m ${script}\"
done > $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-modules.sh

sed 's/=/ /' \
	< $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-modules.sh \
	> $RPM_BUILD_ROOT/etc/shrc.d/python%{py_ver}-modules.csh

# xgettext specific for Python code
#
# we will have two commands: pygettext.py (an alias) and pygettext;
# this way there are no import (which is impossible now) conflicts and
# pygettext.py is provided for compatibility
install Tools/i18n/pygettext.py $RPM_BUILD_ROOT%{_bindir}/pygettext%{py_ver}

# add py_ver
for script in idle pydoc; do
	mv $RPM_BUILD_ROOT%{_bindir}/${script} $RPM_BUILD_ROOT%{_bindir}/${script}%{py_ver}
done
mv $RPM_BUILD_ROOT%{_mandir}/man1/python.1 $RPM_BUILD_ROOT%{_mandir}/man1/python%{py_ver}.1

# just to cut the noise, as they are not packaged (now)
# first tests
rm -rf $RPM_BUILD_ROOT%{py_scriptdir}/test
rm -rf $RPM_BUILD_ROOT%{py_scriptdir}/bsddb/test
rm -rf $RPM_BUILD_ROOT%{py_scriptdir}/ctypes/test
rm -rf $RPM_BUILD_ROOT%{py_scriptdir}/distutils/tests
rm -rf $RPM_BUILD_ROOT%{py_scriptdir}/email/test
rm -rf $RPM_BUILD_ROOT%{py_scriptdir}/sqlite3/test

# other files
rm -rf $RPM_BUILD_ROOT%{py_scriptdir}/plat-*/regen
find $RPM_BUILD_ROOT%{py_scriptdir} -name \*.egg-info -exec rm {} \;
find $RPM_BUILD_ROOT%{py_scriptdir} -name \*.bat -exec rm {} \;
find $RPM_BUILD_ROOT%{py_scriptdir} -name \*.txt -exec rm {} \;
find $RPM_BUILD_ROOT%{py_scriptdir} -name README\* -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post doc-info	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun doc-info	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/python
%attr(755,root,root) %{_bindir}/python%{py_ver}
%{_mandir}/man1/*

%files modules
%defattr(644,root,root,755)
/etc/shrc.d/python*-modules*
%exclude %{py_scriptdir}/UserDict.py[co]
%exclude %{py_scriptdir}/codecs.py[co]
%exclude %{py_scriptdir}/copy_reg.py[co]
%exclude %{py_scriptdir}/locale.py[co]
%exclude %{py_scriptdir}/posixpath.py[co]
%exclude %{py_scriptdir}/pdb.py[co]
%exclude %{py_scriptdir}/profile.py[co]
%exclude %{py_scriptdir}/pstats.py[co]
%exclude %{py_scriptdir}/pydoc.py[co]
%exclude %{py_scriptdir}/site.py[co]
%exclude %{py_scriptdir}/stat.py[co]
%exclude %{py_scriptdir}/timeit.py[co]
%exclude %{py_scriptdir}/os.py[co]
%exclude %{py_scriptdir}/encodings/*.py[co]
%exclude %{py_scriptdir}/types.py[co]

%{py_scriptdir}/*.py[co]

%{py_dyndir}/*.egg-info

#
# list .so modules to be sure that all of them are built
#

# three modules below do not work on 64-bit architectures
# see Python README file for explanation
%ifnarch alpha ia64 ppc64 sparc64 %{x8664}
%attr(755,root,root) %{py_dyndir}/audioop.so
%attr(755,root,root) %{py_dyndir}/rgbimg.so
%attr(755,root,root) %{py_dyndir}/imageop.so
# sizeof(long) != sizeof(int), so dl module will not be built on 64-bit
# platforms
%attr(755,root,root) %{py_dyndir}/dl.so
%endif

%attr(755,root,root) %{py_dyndir}/array.so
%attr(755,root,root) %{py_dyndir}/atexit.so
%attr(755,root,root) %{py_dyndir}/audioop.so
%attr(755,root,root) %{py_dyndir}/binascii.so
%attr(755,root,root) %{py_dyndir}/_bisect.so
%attr(755,root,root) %{py_dyndir}/_bsddb.so
%attr(755,root,root) %{py_dyndir}/bz2.so
%attr(755,root,root) %{py_dyndir}/cmath.so
%attr(755,root,root) %{py_dyndir}/_codecs_cn.so
%attr(755,root,root) %{py_dyndir}/_codecs_hk.so
%attr(755,root,root) %{py_dyndir}/_codecs_iso2022.so
%attr(755,root,root) %{py_dyndir}/_codecs_jp.so
%attr(755,root,root) %{py_dyndir}/_codecs_kr.so
%attr(755,root,root) %{py_dyndir}/_codecs_tw.so
%attr(755,root,root) %{py_dyndir}/_collections.so
#%attr(755,root,root) %{py_dyndir}/cPickle.so
%attr(755,root,root) %{py_dyndir}/crypt.so
#%attr(755,root,root) %{py_dyndir}/cStringIO.so
%attr(755,root,root) %{py_dyndir}/_csv.so
%attr(755,root,root) %{py_dyndir}/_ctypes*.so
%attr(755,root,root) %{py_dyndir}/_curses_panel.so
%attr(755,root,root) %{py_dyndir}/_curses.so
%attr(755,root,root) %{py_dyndir}/datetime.so
%attr(755,root,root) %{py_dyndir}/_elementtree.so
%attr(755,root,root) %{py_dyndir}/_functools.so
%attr(755,root,root) %{py_dyndir}/_hashlib.so
%attr(755,root,root) %{py_dyndir}/_heapq.so
%attr(755,root,root) %{py_dyndir}/_locale.so
%attr(755,root,root) %{py_dyndir}/_lsprof.so
%attr(755,root,root) %{py_dyndir}/_multibytecodec.so
%attr(755,root,root) %{py_dyndir}/_random.so
%{?with_openssl097:%attr(755,root,root) %{py_dyndir}/_sha*.so}
%attr(755,root,root) %{py_dyndir}/_socket.so
%attr(755,root,root) %{py_dyndir}/_ssl.so
%attr(755,root,root) %{py_dyndir}/_testcapi.so
%attr(755,root,root) %{py_dyndir}/_weakref.so
%ifnarch sparc64
%attr(755,root,root) %{py_dyndir}/dbm.so
%endif
%attr(755,root,root) %{py_dyndir}/fcntl.so
%attr(755,root,root) %{py_dyndir}/gdbm.so
%attr(755,root,root) %{py_dyndir}/grp.so
%attr(755,root,root) %{py_dyndir}/itertools.so
#%attr(755,root,root) %{py_dyndir}/linuxaudiodev.so
%attr(755,root,root) %{py_dyndir}/math.so
%attr(755,root,root) %{py_dyndir}/mmap.so
%attr(755,root,root) %{py_dyndir}/nis.so
%attr(755,root,root) %{py_dyndir}/operator.so
%attr(755,root,root) %{py_dyndir}/ossaudiodev.so
%attr(755,root,root) %{py_dyndir}/parser.so
%attr(755,root,root) %{py_dyndir}/pyexpat.so
%attr(755,root,root) %{py_dyndir}/readline.so
%attr(755,root,root) %{py_dyndir}/resource.so
%attr(755,root,root) %{py_dyndir}/select.so
#%attr(755,root,root) %{py_dyndir}/strop.so
%attr(755,root,root) %{py_dyndir}/syslog.so
%attr(755,root,root) %{py_dyndir}/termios.so
%attr(755,root,root) %{py_dyndir}/time.so
%attr(755,root,root) %{py_dyndir}/spwd.so
%attr(755,root,root) %{py_dyndir}/unicodedata.so
%attr(755,root,root) %{py_dyndir}/zlib.so

%dir %{py_scriptdir}/plat-*
%{py_scriptdir}/plat-*/*.py[co]

%dir %{py_scriptdir}/bsddb
%{py_scriptdir}/bsddb/*.py[co]

#%dir %{py_scriptdir}/compiler
#%{py_scriptdir}/compiler/*.py[co]

%dir %{py_scriptdir}/ctypes
%dir %{py_scriptdir}/ctypes/macholib

%{py_scriptdir}/ctypes/*.py[co]
%{py_scriptdir}/ctypes/macholib/*.py[co]

%dir %{py_scriptdir}/curses
%{py_scriptdir}/curses/*.py[co]

%dir %{py_scriptdir}/distutils
%dir %{py_scriptdir}/distutils/command
%{py_scriptdir}/distutils/*.py[co]
%{py_scriptdir}/distutils/command/*.py[co]

%dir %{py_scriptdir}/email
%dir %{py_scriptdir}/email/mime
%{py_scriptdir}/email/*.py[co]
%{py_scriptdir}/email/mime/*.py[co]

%dir %{py_scriptdir}/logging
%{py_scriptdir}/logging/*.py[co]

%dir %{py_scriptdir}/wsgiref
%{py_scriptdir}/wsgiref/*.py[co]

%dir %{py_scriptdir}/xml
%dir %{py_scriptdir}/xml/dom
%dir %{py_scriptdir}/xml/etree
%dir %{py_scriptdir}/xml/parsers
%dir %{py_scriptdir}/xml/sax
%{py_scriptdir}/xml/*.py[co]
%{py_scriptdir}/xml/dom/*.py[co]
%{py_scriptdir}/xml/etree/*.py[co]
%{py_scriptdir}/xml/parsers/*.py[co]
%{py_scriptdir}/xml/sax/*.py[co]

%files modules-sqlite
%defattr(644,root,root,755)
%attr(755,root,root) %{py_dyndir}/_sqlite3.so
%dir %{py_scriptdir}/sqlite3
%{py_scriptdir}/sqlite3/*.py[co]

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpython*.so.*

%dir %{py_dyndir}
%dir %{py_scriptdir}
%dir %{py_libdir}
%dir %{py_sitescriptdir}
%dir %{py_sitedir}

# shared modules required by python library
%attr(755,root,root) %{py_dyndir}/_struct.so

# modules required by python library
%{py_scriptdir}/UserDict.py[co]
%{py_scriptdir}/codecs.py[co]
%{py_scriptdir}/copy_reg.py[co]
%{py_scriptdir}/locale.py[co]
%{py_scriptdir}/posixpath.py[co]
%{py_scriptdir}/site.py[co]
%{py_scriptdir}/stat.py[co]
%{py_scriptdir}/os.py[co]
# needed by the dynamic sys.lib patch
%{py_scriptdir}/types.py[co]

# encodings required by python library
%dir %{py_scriptdir}/encodings
%{py_scriptdir}/encodings/*.py[co]

%files -n pydoc30
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pydoc%{py_ver}
%{py_scriptdir}/pydoc.py[co]

%files -n idle30
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/idle%{py_ver}
%dir %{py_scriptdir}/idlelib
%dir %{py_scriptdir}/idlelib/Icons
%{py_scriptdir}/idlelib/*.py[co]
%{py_scriptdir}/idlelib/Icons/*
%{py_scriptdir}/idlelib/*.def

%files devel
%defattr(644,root,root,755)
%doc Misc/{ACKS,NEWS,README,README.valgrind,valgrind-python.supp}
%attr(755,root,root) %{_bindir}/python-config
%attr(755,root,root) %{_bindir}/python%{py_ver}-config
%attr(755,root,root) %{_libdir}/lib*.so
%dir %{py_incdir}
%{py_incdir}/*.h

%dir %{py_libdir}/config
%attr(755,root,root) %{py_libdir}/config/makesetup
%attr(755,root,root) %{py_libdir}/config/install-sh
%{py_libdir}/config/Makefile
%{py_libdir}/config/Makefile.pre.in
%{py_libdir}/config/Setup
%{py_libdir}/config/Setup.config
%{py_libdir}/config/Setup.local
%{py_libdir}/config/config.c
%{py_libdir}/config/config.c.in
%{py_libdir}/config/python.o

%files devel-src
%defattr(644,root,root,755)
%attr(-,root,root) %{py_scriptdir}/*.py
%{py_scriptdir}/plat-*/*.py
%{py_scriptdir}/bsddb/*.py
%{py_scriptdir}/ctypes/*.py
%{py_scriptdir}/ctypes/macholib/*.py
#%{py_scriptdir}/compiler/*.py
%{py_scriptdir}/curses/*.py
%{py_scriptdir}/distutils/*.py
%{py_scriptdir}/distutils/command/*.py
%{py_scriptdir}/email/*.py
%{py_scriptdir}/email/mime/*.py
%{py_scriptdir}/hotshot/*.py
%{py_scriptdir}/logging/*.py
%{py_scriptdir}/sqlite3/*.py
%{py_scriptdir}/wsgiref/*.py
%{py_scriptdir}/xml/*.py
%{py_scriptdir}/xml/dom/*.py
%{py_scriptdir}/xml/etree/*.py
%{py_scriptdir}/xml/parsers/*.py
%{py_scriptdir}/xml/sax/*.py
%{py_scriptdir}/encodings/*.py
%{py_scriptdir}/idlelib/*.py

%files devel-tools
%defattr(644,root,root,755)
%doc Lib/pdb.doc
/etc/shrc.d/python*-devel*

%attr(755,root,root) %{_bindir}/pygettext%{py_ver}

%attr(755,root,root) %{py_dyndir}/_hotshot.so
%dir %{py_scriptdir}/hotshot
%{py_scriptdir}/hotshot/*.py[co]
%{py_scriptdir}/pdb.py[co]
%{py_scriptdir}/profile.py[co]
%{py_scriptdir}/pstats.py[co]
%{py_scriptdir}/timeit.py[co]

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}


#%files doc
#%defattr(644,root,root,755)
#%doc Python-Docs-%{version}%{beta}/*

%if %{with info}
%files doc-info
%defattr(644,root,root,755)
%{_infodir}/*.info*
%endif

%if %{with tkinter}
%files tkinter
%defattr(644,root,root,755)
%{py_scriptdir}/lib-tk
%attr(755,root,root) %{py_dyndir}/_tkinter.so
%endif
