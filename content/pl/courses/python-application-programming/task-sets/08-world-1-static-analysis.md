---
title: "Analiza statyczna: ruff, mypy i pyright"
summary: "Pierwszy etap poziomu 5 kursu Python RPG Questbook (World 1: Static Analysis): trzy misje o narzędziach, które sprawdzają kod bez uruchamiania go (ruff, mypy i pyright), oraz projekt Quality Gate Rescue, który zamyka ten etap."
status: published
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu: instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: level_5_maintainability/README.md
    lang: en
    label: "Poziom 5 — Production Quality and Maintainability: założenia, misje i projekty"
  - repository: python-rpg-questbook
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: podział poziomu 5 na etapy (World 1–3)"
  - repository: python-rpg-questbook
    path: pyproject.toml
    lang: en
    label: "Konfiguracja repozytorium kursu: narzędzia poziomu 5 w grupie dev"
  - repository: python-rpg-questbook
    path: level_5_maintainability/starter_unqualified_rpg/
    lang: en
    label: "Kod startowy poziomu 5: katalog starter_unqualified_rpg"
tasks:
  misja-01:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/01_ruff_linting/README.md
        lang: en
        label: "Instrukcja: Mission 01 — Ruff Linting"
  misja-02:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/02_mypy_type_checking/README.md
        lang: en
        label: "Instrukcja: Mission 02 — mypy Type Checking"
  misja-03:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/03_pyright_strict/README.md
        lang: en
        label: "Instrukcja: Mission 03 — pyright Strict Mode"
  quality-gate-rescue:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/projects/01_quality_gate_rescue/README.md
        lang: en
        label: "Instrukcja: Project 01 — Quality Gate Rescue"
---
Ten zestaw obejmuje pierwszy etap poziomu 5 kursu Python RPG Questbook, „World 1: Static Analysis”.
Poziom 5 nie dodaje grze nowych funkcji. Pyta, czy ktoś inny zrozumie kod, bezpiecznie go zmieni i
wyda. W tym etapie poznajesz narzędzia, które sprawdzają kod bez uruchamiania go: ruff wykrywa
problemy ze stylem i typowe błędy, a mypy i pyright sprawdzają typy. Pierwsze trzy zadania to misje
01–03. Czwarte to projekt Quality Gate Rescue, który mapa kursu nazywa punktem kontrolnym
(„Checkpoint”) i umieszcza na końcu tego etapu. Instrukcje, kod, pliki konfiguracji i komunikaty
skryptów sprawdzających są po angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium i budowę misji opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1.
Narzędzia poziomu 5 są w grupie zależności deweloperskich (`dev`) w pliku `pyproject.toml`
repozytorium: ruff, mypy, pyright, pytest, pytest-cov i pre-commit. Instaluje je polecenie
`uv sync` z przygotowania do zestawu 1, więc nie musisz ich dodawać.

**Co wynosisz z wcześniejszych zestawów.** Opis poziomu 5 zakłada ukończony poziom 4, opisany w
zestawach 5–7. Kod misji to uproszczona gra z tamtego poziomu w jednym pliku. Ma polecenia
Typera, wynik przez Rich, modele Pydantic, logi i raporty z sesji. Własnego kodu z poziomu 4 nie
potrzebujesz. Opis poziomu zaznacza, że to wersja treningowa w jednym pliku, a nie pakiet z
projektu Installable CLI Tool. Narzędzia czytają ten kod, więc przyda się znajomość Typera z
[zestawu 5](world-1-command-line-interface.md) i modeli Pydantic z
[zestawu 1](world-1-trusted-data.md).

**Pliki.** Każda misja ma własny `task.py`, skrypt `check.py` i własny plik `pyproject.toml` z
konfiguracją narzędzi. Kolejne misje zaczynają od gotowego wyniku poprzedniej. `task.py` misji 02
przechodzi już ruff, a `task.py` misji 03 ma już adnotacje typów z misji 02. Nie przenosisz więc
kodu między misjami. Projekt ma własny pakiet `rpg/` i własne pliki konfiguracji.

**Kod tylko do przeczytania.** Poziom 5 ma przygotowaną wersję gry, `starter_unqualified_rpg/`.
Komentarz na początku `main.py` wymienia sześć problemów jakości („quality smells”) i misje, które
je naprawiają. Opis poziomu każe najpierw uruchomić grę. Z katalogu głównego repozytorium:

```bash
uv run python level_5_maintainability/starter_unqualified_rpg/main.py new-game --name Ada --class warrior
```

Gra zapisuje bohatera w katalogu `starter_unqualified_rpg/saves/`. Misje pracują we własnych
plikach. Z tego kodu korzysta dopiero projekt Full Release Pipeline z
[zestawu 10](world-3-ci-cd-and-polish.md#full-release-pipeline).

**Polecenia i katalog roboczy.** Wszystkie polecenia zestawu wpisujesz w katalogu głównym
repozytorium. Dotyczy to także poleceń narzędzi, które instrukcje misji każą wpisywać w katalogu
misji. Katalogi misji 01–03 mają własny `pyproject.toml` z konfiguracją narzędzi, ale bez sekcji
`[project]`. `uv run` szuka projektu od bieżącego katalogu w górę i traktuje taki plik jak osobny
projekt. W katalogu misji tworzy więc nowe, puste środowisko `.venv` i plik `uv.lock`, a w tym
środowisku nie ma narzędzi kursu. Polecenie kończy się wtedy błędem, na przykład:

```text
error: Failed to spawn: `ruff`
```

Nawet `uv run python check.py` w katalogu misji korzysta z tego pustego środowiska i zgłasza
mylący błąd. W kontroli wersje `uv` od 0.5 do 0.11 zachowywały się tak samo albo przerywały
polecenie wcześniej, z błędem „No `project` table found”. Inna wersja `uv` nie rozwiązuje więc
problemu. Środowisko `.venv` i plik `uv.lock` utworzone w katalogu misji nie są potrzebne do pracy
według tej strony.

W katalogu głównym `uv` korzysta ze środowiska repozytorium, tak jak w opisie kursu. Polecenia
narzędzi na tej stronie są przepisane z wywołań zapisanych w skryptach `check.py`. Każde podaje
ścieżkę do sprawdzanego pliku i plik konfiguracji zadania: `--config` dla ruffa, `--config-file`
dla mypy, a `--project` dla pyright. Narzędzie sprawdza więc tylko pliki zadania, z jego
konfiguracją, i nie zmienia plików innych zadań ani poziomów. Inne polecenia z instrukcji,
na przykład z części „Try It Yourself”, wpisujesz tak samo.

**pyright i Node.js.** pyright, instalowany przez `uv sync`, potrzebuje do działania Node.js. Jeśli
Node.js nie ma w systemie, pyright przy pierwszym uruchomieniu próbuje pobrać go automatycznie. W
kontroli z 20 listopada 2026 r. to automatyczne pobieranie kończyło się błędem, a pyright nie
sprawdzał kodu:

```text
RuntimeError: nodeenv failed
```

Przyczyną jest środowisko, nie kod kursu. Narzędzie, które pobiera Node.js, nie umie odczytać
numeru wersji testowej z początku listy wersji Node.js. Ograniczenie może zniknąć bez zmian w
kursie. W tej samej kontroli pyright
działał, gdy Node.js był zainstalowany w systemie. Dotyczy to tylko zadań z pyright: misji 03,
projektu Quality Gate Rescue i projektu Full Release Pipeline z zestawu 10. Gdy pojawia się błąd
„nodeenv failed”, pyright nie sprawdził kodu, więc zadania nie można uznać za sprawdzone, a jego
`check.py` kończy się błędem.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypty tego zestawu uruchamiają ruff, mypy i pyright na
plikach zadania z jego konfiguracją. Sprawdzają też wybrane napisy w plikach. Skrypt misji 02
dodatkowo wczytuje `task.py` jako moduł i odczytuje adnotacje wybranych funkcji. Gdy wszystko się
zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się nie zgadza,
wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Przejście skryptu oznacza, że narzędzia nie zgłaszają błędów przy konfiguracji z
plików zadania. Nie zawsze oznacza, że konfiguracja jest taka, jak każe instrukcja. Pozostałe
elementy porównujesz z instrukcją samodzielnie. Części instrukcji „Try It Yourself” i „Side Quest”
oraz lista „Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów. Polecenia z tej strony sprawdzają tylko pliki jednego zadania.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki
konfiguracji i komunikaty skryptów `check.py`.

## Zadania

### ruff Linting: reguły stylu i formatowanie {#misja-01}

**Cel:** skonfigurować ruff w `pyproject.toml` misji i usunąć z `task.py` wszystkie naruszenia
wybranych reguł oraz sformatować plik.

**Zakres pracy:** w `level_5_maintainability/missions/01_ruff_linting/` są `task.py` z grą,
w której są splątane importy, stara składnia typów, za długie wiersze i `except:` bez typu
wyjątku, oraz `pyproject.toml` z gotową sekcją `[tool.ruff]` (długość wiersza 88, Python 3.12) i
pustą listą reguł `select = []`. Według kroków instrukcji:

1. W `pyproject.toml` wpisz kategorie reguł `["E", "F", "I", "UP", "B"]`. Tabela w instrukcji
   objaśnia, co wykrywa każda kategoria.
2. Wyświetl naruszenia, popraw automatycznie to, co ruff potrafi, a resztę ręcznie. Na końcu
   sformatuj plik.

```bash
uv run ruff check level_5_maintainability/missions/01_ruff_linting/task.py --config level_5_maintainability/missions/01_ruff_linting/pyproject.toml
uv run ruff check --fix level_5_maintainability/missions/01_ruff_linting/task.py --config level_5_maintainability/missions/01_ruff_linting/pyproject.toml
uv run ruff format level_5_maintainability/missions/01_ruff_linting/task.py --config level_5_maintainability/missions/01_ruff_linting/pyproject.toml
uv run ruff format --check level_5_maintainability/missions/01_ruff_linting/task.py --config level_5_maintainability/missions/01_ruff_linting/pyproject.toml
```

Polecenia z `--fix` i `ruff format` zmieniają tylko `task.py` misji.

**Rezultat:** dopóki lista `select` jest pusta, `ruff check` wypisuje „All checks passed!”, bo
żadna reguła nie jest włączona. Po zmianie listy ruff zgłasza naruszenia. `--fix` poprawia część z
nich, na przykład importy i składnię typów. Do ręcznej poprawy instrukcja wymienia `except:` bez
typu wyjątku, długie wiersze i nieużywane importy. Część długich wierszy i dwie instrukcje w jednym
wierszu (E702) poprawia formatter. Ruff zgłasza też dwie reguły, których instrukcja nie omawia:

- B008, czyli wywołanie `typer.Option()` jako wartość domyślna parametru;
- UP042, czyli klasę `HeroClass(str, Enum)`, dla której ruff proponuje `StrEnum`.

Dostarczony `pyproject.toml` misji 02 wyłącza regułę B008 (`ignore = ["B008"]`). Jego komentarz
mówi, że `typer.Option()` w wartości domyślnej to zamierzony wzorzec. Po poprawkach `ruff check`
wypisuje „All checks passed!”, a `ruff format --check` wypisuje „1 file already formatted”.

**Sprawdź się:** `uv run python level_5_maintainability/missions/01_ruff_linting/check.py`. Skrypt
sprawdza:

- że `pyproject.toml` ma sekcję `[tool.ruff.lint]` i nie ma w nim napisu `select = []`;
- że `ruff check` i `ruff format --check` z konfiguracją misji przechodzą dla `task.py`;
- że w `task.py` nie ma napisów `except:`, `Optional[`, `List[`, `Dict[`, `Tuple[` ani
  `from typing import Optional`.

Nie sprawdza, jakie reguły wybrano. Przechodzi każda niepusta lista, na przykład z jedną kategorią,
jeśli ruff nie zgłasza dla niej błędów. W kontroli przechodził też plik z komentarzem
`# ruff: noqa`, który wyłącza reguły dla całego pliku. Listę reguł porównaj z krokiem 1 instrukcji.

### mypy Type Checking: adnotacje typów w trybie strict {#misja-02}

**Cel:** dodać adnotacje typów do wszystkich funkcji i metod w `task.py`, włączyć tryb strict mypy
w `pyproject.toml` misji i uzyskać wynik bez błędów.

**Zakres pracy:** w `level_5_maintainability/missions/02_mypy_type_checking/` jest `task.py` po
poprawkach ruffa, bez adnotacji typów. Komentarze w kodzie podpowiadają typy. Plik
`pyproject.toml` ma konfigurację ruffa i komentarz `TODO` w miejscu konfiguracji mypy. Według
kroków instrukcji:

1. W `pyproject.toml` dodaj sekcję `[tool.mypy]` z `strict = true`.
2. Dodaj adnotacje do 13 sygnatur z tabeli w kroku 3 instrukcji. Tabela obejmuje funkcje
   `compute_damage`, `load_monsters`, `load_hero_classes`, `save_hero`, `load_hero`, `make_hero`,
   `simulate_one` i `generate_reports` oraz właściwości i metody klas `Hero` i `Monster`.
3. Po każdej funkcji uruchom mypy ponownie, aż nie zgłosi błędów. Ruff ma nadal przechodzić.

```bash
uv run mypy level_5_maintainability/missions/02_mypy_type_checking/task.py --strict --config-file level_5_maintainability/missions/02_mypy_type_checking/pyproject.toml
uv run ruff check level_5_maintainability/missions/02_mypy_type_checking/task.py --config level_5_maintainability/missions/02_mypy_type_checking/pyproject.toml
```

**Rezultat:** na starcie mypy zgłasza brakujące adnotacje i wywołania funkcji bez adnotacji w kodzie
z adnotacjami („Call to untyped function … in typed context”). Po poprawkach wypisuje „Success: no
issues found in 1 source file”, a ruff nadal „All checks passed!”.

**Sprawdź się:** `uv run python level_5_maintainability/missions/02_mypy_type_checking/check.py`.
Skrypt sprawdza:

- że `pyproject.toml` ma sekcję `[tool.mypy]`;
- że ruff z konfiguracją misji nadal przechodzi;
- że `mypy --strict` z konfiguracją misji przechodzi;
- że co najmniej 8 wierszy `task.py` zawiera `def ` i ` -> `;
- po wczytaniu `task.py` jako modułu, że 13 sygnatur z tabeli instrukcji ma adnotacje wymienionych
  parametrów i wyniku i że żadna nie zawiera `Any`, także wewnątrz typu, jak `list[Any]`;
- że w `task.py` nie ma `except:` ani starej składni typów.

Skrypt sam podaje mypy opcję `--strict`, więc nie sprawdza, czy sekcja `[tool.mypy]` zawiera
`strict = true`. W kontroli przechodziła sekcja pusta. Nie porównuje też adnotacji z tabelą:
sprawdza tylko, że są i nie zawierają `Any`. Typy porównaj z tabelą w instrukcji.

### pyright Strict: drugi program sprawdzający typy {#misja-03}

**Cel:** dodać do `pyproject.toml` misji sekcję `[tool.pyright]` z trybem strict i poprawić jedyny
błąd, który pyright zgłasza, a mypy nie.

**Zakres pracy:** w `level_5_maintainability/missions/03_pyright_strict/` jest `task.py` z
adnotacjami z misji 02, który przechodzi `mypy --strict`. Plik `pyproject.toml` ma konfigurację
ruffa i mypy (`strict = true`, `ignore_missing_imports = true`) oraz komentarz `TODO` w miejscu
konfiguracji pyright. Według kroków instrukcji:

1. Dodaj sekcję `[tool.pyright]` z `pythonVersion = "3.12"` i `typeCheckingMode = "strict"`.
2. Uruchom pyright i przeczytaj błędy.
3. Popraw błąd w `load_monsters()`. Pusta lista `monsters` nie ma adnotacji typu, więc pyright
   traktuje jej elementy jako nieznane. Poprawkę podaje tabela w kroku 3 instrukcji.
4. Sprawdź, że mypy nadal przechodzi.

```bash
uv run python -m pyright level_5_maintainability/missions/03_pyright_strict/task.py --project level_5_maintainability/missions/03_pyright_strict
uv run mypy level_5_maintainability/missions/03_pyright_strict/task.py --strict --config-file level_5_maintainability/missions/03_pyright_strict/pyproject.toml
```

Opcja `--project` wskazuje katalog misji, więc pyright czyta sekcję `[tool.pyright]` z jej
`pyproject.toml`.

**Rezultat:** bez sekcji `[tool.pyright]` pyright nie zgłasza błędów. Po jej dodaniu zgłasza dwa
błędy w `load_monsters()` (`reportUnknownMemberType` i `reportUnknownVariableType`), tak jak opisuje
instrukcja. Po poprawce wypisuje „0 errors, 0 warnings, 0 informations”, a mypy nadal nie zgłasza
błędów. Zadanie poboczne instaluje basedpyright poleceniem `uv add --dev basedpyright`. To
polecenie dopisuje pakiet do wspólnych plików `pyproject.toml` i `uv.lock` w katalogu głównym
repozytorium.

**Sprawdź się:** `uv run python level_5_maintainability/missions/03_pyright_strict/check.py`.
Skrypt sprawdza:

- że `pyproject.toml` ma sekcję `[tool.pyright]`, w której występuje słowo „strict”;
- że `mypy --strict` z konfiguracją misji nadal przechodzi;
- że pyright z konfiguracją misji przechodzi.

Skrypt szuka w sekcji `[tool.pyright]` tylko słowa „strict”. W kontroli przechodził też tryb
`basic` ze słowem „strict” w komentarzu, a w tym trybie pyright nie zgłasza błędu z kroku 3. Tryb
porównaj z krokiem 1 instrukcji. Gdy pyright nie może się uruchomić (zobacz „pyright i Node.js”
wyżej), skrypt wypisuje samo „❌ pyright fails:” bez przyczyny. Przyczynę pokazuje pierwsze z
poleceń wyżej.

### Quality Gate Rescue: trzy bramki jakości {#quality-gate-rescue}

Mapa kursu nazywa ten projekt punktem kontrolnym („Checkpoint”) i umieszcza go na końcu etapu
World 1. Instrukcja wymaga ukończenia misji 01–03.

**Cel:** poprawić pakiet `rpg/`, tak by ruff, mypy w trybie strict i pyright przechodziły bez
błędów, i opisać w pliku `QUALITY_REPORT.md`, co znalazło każde z narzędzi.

**Zakres pracy:** w `level_5_maintainability/projects/01_quality_gate_rescue/` jest pakiet `rpg/` z
plikami `domain.py` i `combat.py` do poprawienia. Są tam też trzy pliki konfiguracji, których
instrukcja każe nie zmieniać:

- `ruff.toml` z regułami E, F, UP i I;
- `mypy.ini` z trybem strict;
- `pyrightconfig.json` z trybem strict.

Tabela w instrukcji wymienia problemy: nieużywany `import os`, `List`, `Optional` i `Dict` z modułu
`typing`, brak typów wyniku, `Any` tam, gdzie da się podać konkretny typ, i wiersz dłuższy niż 88
znaków. Instrukcja każe pracować narzędzie po narzędziu: najpierw ruff (z `--fix`), potem typy
wyniku, potem zamiana `Any` na konkretne typy, a na końcu pyright. Potem utwórz
`QUALITY_REPORT.md` z co najmniej trzema sekcjami, `## ruff`, `## mypy` i `## pyright`, według
wzoru z instrukcji.

Instrukcja każe uruchamiać polecenia z katalogu głównego, ale polecenia bramek podaje względem
katalogu projektu (`ruff check rpg/` i tak dalej). Ten katalog nie ma własnego `pyproject.toml`,
więc polecenia z `uv run` działają też w nim. Z katalogu głównego wpisujesz je tak:

```bash
uv run ruff check level_5_maintainability/projects/01_quality_gate_rescue/rpg/ --config level_5_maintainability/projects/01_quality_gate_rescue/ruff.toml
uv run ruff check level_5_maintainability/projects/01_quality_gate_rescue/rpg/ --fix --config level_5_maintainability/projects/01_quality_gate_rescue/ruff.toml
uv run mypy --strict level_5_maintainability/projects/01_quality_gate_rescue/rpg/ --config-file level_5_maintainability/projects/01_quality_gate_rescue/mypy.ini
uv run python -m pyright level_5_maintainability/projects/01_quality_gate_rescue/rpg/ --project level_5_maintainability/projects/01_quality_gate_rescue
```

Skrypt uruchamia te narzędzia w katalogu projektu, gdzie same znajdują jego pliki konfiguracji. Z
katalogu głównego wskazują je opcje `--config`, `--config-file` i `--project`. W kontroli wyniki z
obu katalogów były takie same.

**Rezultat:** na starcie ruff zgłasza 11 naruszeń, mypy 8 błędów, a pyright jeden. Tabela
instrukcji przypisuje nieużywany `import os` ruffowi (F401). W `domain.py` ten import ma jednak
komentarz `# noqa: F401`, więc ruff go pomija. Zgłasza go pyright jako jedyny błąd na starcie, a
komentarz przy imporcie każe usunąć ten wiersz. Po poprawkach ruff wypisuje „All checks passed!”,
mypy „Success: no issues found in 3 source files”, a pyright „0 errors”.

**Sprawdź się:**
`uv run python level_5_maintainability/projects/01_quality_gate_rescue/check.py`. Skrypt sprawdza:

- w katalogu projektu, że `ruff check rpg/`, `mypy --strict rpg/` i `pyright rpg/` z plikami
  konfiguracji projektu przechodzą;
- że `QUALITY_REPORT.md` istnieje, ma co najmniej trzy wiersze zaczynające się od `## ` i wymienia
  ruff, mypy i pyright, bez względu na wielkość liter.

Nie sprawdza treści raportu: w kontroli przechodził raport z samymi trzema nagłówkami. Opis, co
znalazło każde narzędzie, porównaj z wzorem w instrukcji. Jeśli moduł pyright nie jest
zainstalowany, skrypt pomija tę bramkę z ostrzeżeniem „pyright not installed — skipping” i kończy
się sukcesem. `uv sync` instaluje pyright, więc takie ostrzeżenie oznacza, że pyright nie
sprawdził kodu. Gdy pyright nie może się uruchomić z powodu błędu „nodeenv failed”, skrypt
wypisuje „❌ pyright rpg/ still has errors:” bez listy błędów. Wtedy to nie są błędy w kodzie.

## Oczekiwane rezultaty

- `check.py` misji 01–03 i projektu Quality Gate Rescue kończy się komunikatem o ukończeniu.
- `task.py` misji 01 przechodzi ruff i formatowanie z regułami z instrukcji, misji 02 przechodzi
  `mypy --strict` z typami z tabeli, a misji 03 przechodzi pyright w trybie strict.
- Pakiet `rpg/` projektu przechodzi trzy bramki, a `QUALITY_REPORT.md` opisuje wyniki ruffa, mypy
  i pyright.

## Wskazówki

- pyright przy każdym uruchomieniu sprawdza, czy jest nowsza wersja, i może wypisać „WARNING: there
  is a new pyright version available”. To ostrzeżenie nie zmienia wyniku. Wersję pyright ustala
  plik `uv.lock` repozytorium.
- Narzędzia zapisują pamięć podręczną w katalogach `.ruff_cache/` i `.mypy_cache/`, w katalogu
  głównym i w katalogach zadań. Te katalogi są w `.gitignore` repozytorium.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. Jeśli
  nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań na tej stronie.
- Kolejny etap poziomu 5, testy automatyczne, opisuje [zestaw 9](world-2-testing.md).
