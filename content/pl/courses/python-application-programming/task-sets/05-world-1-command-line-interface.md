---
title: "Interfejs wiersza poleceń"
summary: "Pierwszy etap poziomu 4 kursu Python RPG Questbook (World 1: Command Line Interface): dwie misje o poleceniach gry uruchamianych z argumentami, z modułem argparse i z biblioteką Typer, oraz projekt Quest Master CLI, który zamyka ten etap."
status: published
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu: instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: level_4_interfaces/README.md
    lang: en
    label: "Poziom 4 — Interfaces and Reports: założenia, misje i projekty"
  - repository: python-rpg-questbook
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: podział poziomu 4 na etapy (World 1–3)"
  - repository: python-rpg-questbook
    path: level_4_interfaces/starter_verbose_rpg/
    lang: en
    label: "Kod startowy poziomu 4: katalog starter_verbose_rpg"
tasks:
  misja-01:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/missions/01_argparse_baseline/README.md
        lang: en
        label: "Instrukcja: Mission 01 — argparse Baseline"
  misja-02:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/missions/02_typer_cli/README.md
        lang: en
        label: "Instrukcja: Mission 02 — Typer CLI"
  quest-master-cli:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/projects/01_quest_master_cli/README.md
        lang: en
        label: "Instrukcja: Project 01 — Quest Master CLI"
---
Ten zestaw obejmuje pierwszy etap poziomu 4 kursu Python RPG Questbook, „World 1: Command Line
Interface”. Gra przestaje pytać o wszystko przez `input()`: polecenie i jego opcje podajesz przy
uruchomieniu programu. Najpierw budujesz polecenia modułem `argparse` z biblioteki standardowej,
potem te same polecenia biblioteką Typer. Pierwsze dwa zadania to misje 01 i 02. Trzecie to projekt
Quest Master CLI, który mapa kursu nazywa punktem kontrolnym („Checkpoint”) i umieszcza na końcu
tego etapu. Instrukcje, kod i komunikaty skryptów sprawdzających są po angielsku. Ta strona
streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium, budowę misji i miejsce wpisywania poleceń opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1.
Biblioteki Typer i Rich, z których korzysta poziom 4, instalują się razem z innymi zależnościami.

**Co wynosisz z wcześniejszych zestawów.** Opis poziomu 4 zakłada ukończony poziom 3, opisany w
zestawach 1–3. Mapa kursu umieszcza przed poziomem 4 także etap Data Recall Checkpoint
([zestaw 4](data-recall-checkpoint.md)), ale zadania poziomu 4 nie korzystają z NumPy ani pandas.
W tym etapie nie potrzebujesz kodu z poziomu 3: zapis i odczyt bohatera oraz uproszczona walka są
w plikach misji gotowe. Przydaje się znajomość klas danych (`@dataclass`) i wyliczeń (`Enum`) z
poziomu 2.

**Pliki.** Każda misja i projekt mają własny, samodzielny plik `task.py`. Misje 01 i 02 zawierają
gotowy, uproszczony model bohatera i potworów, symulację walk oraz zapis bohatera do pliku JSON. Ty
piszesz tylko warstwę poleceń. Misja 02 przepisuje polecenia z misji 01 na Typer, ale ma własny plik
i nie korzysta z kodu misji 01. Projekt ma dane bohaterów i potworów wpisane w kod i nie czyta
żadnych plików.

**Kod tylko do przeczytania.** Poziom 4 ma przygotowaną wersję gry, `starter_verbose_rpg/`: grę z
poziomu 3 z walidacją Pydantic. Komentarz na początku `main.py` wymienia sześć problemów warstwy
interfejsu („interface smells”) i misje, które je naprawiają. Ten etap dotyczy pierwszego z nich:
gra zawsze pyta o imię, klasę i polecenia przez `input()`, więc nie da się jej uruchomić
automatycznie. Opis poziomu zachęca, by przeczytać ten komentarz na początku. Polecenie `open` z
części „How to start” działa w systemie macOS; w innych systemach otwórz plik w edytorze. Misje
pracują we własnych plikach i nie korzystają z tego kodu.

**Polecenia.** Polecenia misji wpisujesz w katalogu głównym repozytorium. Projekt uruchamiasz,
zgodnie z jego instrukcją, z katalogu projektu, `level_4_interfaces/projects/01_quest_master_cli/`.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. W tym zestawie skrypt uruchamia Twój `task.py` jako osobny
program z różnymi argumentami i sprawdza kod wyjścia oraz to, co program wypisał. Gdy wszystko się
zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się nie zgadza,
wypisuje, czego oczekiwał. Skrypty misji 01 i 02 zapisują przy tym własnych bohaterów w katalogu
`saves/` misji, więc po sprawdzeniu zapis gry zawiera bohatera ze sprawdzenia.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy sprawdzasz samodzielnie: uruchamiasz `task.py` i porównujesz
wynik z instrukcją. Części instrukcji „Break it on purpose” i „Fix it”, zadania poboczne („Side
quest”) i lista „Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO` i komunikaty
skryptów `check.py`.

## Zadania

### argparse Baseline: polecenia z biblioteki standardowej {#misja-01}

**Cel:** dodać do gry trzy polecenia z argumentami, `new-game`, `simulate` i `status`, tak żeby
można ją było uruchomić bez pytań `input()`.

**Zakres pracy:** w `level_4_interfaces/missions/01_argparse_baseline/task.py` gotowe są
uproszczone klasy `HeroClass` i `Hero`, szablony klas bohatera, lista potworów oraz funkcje
`make_hero()`, `simulate_battles()`, `load_save()` i `save_hero()`. Komentarz na początku pliku
mówi o logice gry importowanej z modułu `game_logic`, ale takiego modułu nie ma: wszystko jest w
pliku. Gotowa jest też funkcja `main()`, którą instrukcja wymienia jako trzeci krok: wywołuje parser
i właściwe polecenie, a bez polecenia wypisuje pomoc i kończy się kodem 1. Według instrukcji i
komentarzy `TODO` zaimplementuj:

- `make_parser()`: parser z opisem „RPG Dungeon CLI” i trzema podpoleceniami: `new-game` z opcjami
  `--name` (domyślnie `Hero`) i `--class` (`warrior`, `mage` albo `rogue`, ograniczone przez
  `choices=`), `simulate` z opcją `--battles` (liczba całkowita, domyślnie 5) i `status` bez
  argumentów;
- `cmd_new_game(args)`: utworzenie i zapis bohatera oraz potwierdzenie „New game started: …”;
- `cmd_simulate(args)`: symulacja walk zapisanego bohatera i ponowny zapis, a gdy zapisu nie ma,
  komunikat o błędzie i wyjście z kodem 1;
- `cmd_status()`: imię, klasa, HP, złoto oraz liczba zwycięstw i porażek albo „No save found.”.

Przykład w części „Goal” instrukcji uruchamia plik `game.py`. W repozytorium takiego pliku nie ma:
polecenia uruchamiasz przez `task.py`, jak w części „Run”.

**Rezultat:** polecenie `new-game --name Ada --class warrior` wypisuje „New game started: Ada the
warrior” i zapisuje bohatera w `saves/save_game.json` w katalogu misji. `simulate --battles 3`
wypisuje podsumowanie trzech walk, `status` pokazuje zapisanego bohatera, a `--help` trzy polecenia.
Gotowa funkcja `simulate_battles()` dodaje bohaterowi złoto, ale nie zmienia liczby zwycięstw i
porażek, więc po symulacji `status` pokazuje więcej złota i bilans walk 0/0. Polecenie z części
„Break it on purpose”, `new-game --class wizard`, kończy się komunikatem `argparse` o niedozwolonej
wartości i kodem 2. Zanim uzupełnisz kod, `task.py` wypisuje tylko „TODO: implement make_parser()
first.”.

**Sprawdź się:** `uv run python level_4_interfaces/missions/01_argparse_baseline/check.py`. Skrypt
sprawdza:

- że `new-game` kończy się kodem 0 i wypisuje imię bohatera (Ada, a dla `--class mage` imię Zara i
  nazwę klasy);
- że `new-game --class wizard` kończy się kodem różnym od 0;
- że `simulate --battles 3` po utworzeniu bohatera kończy się kodem 0 i wypisuje liczbę 3, a bez
  zapisu (skrypt usuwa katalog `saves/`) kończy się kodem różnym od 0;
- że `status` bez zapisu kończy się kodem 0, a po zapisie wypisuje imię bohatera;
- że wywołanie bez polecenia kończy się kodem różnym od 0.

Nie sprawdza, czy `--class` ogranicza `choices=`: niedozwolona klasa przechodzi sprawdzenie także
wtedy, gdy program kończy się dalej w kodzie błędem `KeyError`. Nie sprawdza wartości domyślnych
(`Hero` i 5), danych w `status` poza imieniem, zapisu bohatera po symulacji ani wyniku `--help`. Te
elementy porównaj z instrukcją.

### Typer CLI: polecenia z adnotacji typów {#misja-02}

**Cel:** przepisać te same trzy polecenia na bibliotekę Typer, w której adnotacje typów parametrów
funkcji wyznaczają opcje polecenia, a wyliczenie `Enum` ogranicza dozwolone wartości.

**Zakres pracy:** w `level_4_interfaces/missions/02_typer_cli/task.py` gotowe są uproszczony model
(`HeroClass` jako wyliczenie z wartościami `warrior`, `mage` i `rogue`) oraz funkcje pomocnicze
`_make_hero()`, `_simulate_battles()`, `_load_save()` i `_save_hero()`. Instrukcja mówi, że są
importowane, ale są zdefiniowane w pliku. Według komentarzy `TODO`:

- utwórz `app = typer.Typer()` na poziomie modułu;
- zamień funkcje `new_game`, `simulate` i `status` w polecenia `new-game`, `simulate` i `status`
  dekoratorem `@app.command()`, z opcjami zapisanymi przez `Annotated` i `typer.Option()`: `--name`
  (domyślnie `Hero`), `--class` z drugą nazwą `--hero-class` (typ `HeroClass`, domyślnie `warrior`)
  i `--battles` (domyślnie 5);
- uzupełnij ich treść tak jak w misji 01, z `typer.echo()` zamiast `print()` i z `raise
  typer.Exit(1)` w `simulate`, gdy zapisu nie ma;
- dodaj na końcu pliku `if __name__ == "__main__": app()`.

Przykład w części „Goal” używa polecenia `rpg`. W repozytorium to polecenie uruchamia pakiet z
projektu Installable CLI Tool ([zestaw 7](world-3-user-facing-output.md#installable-cli-tool)), a
nie tę misję. Misję uruchamiasz przez `task.py`, jak w części „Run”.

**Rezultat:** te same wyniki poleceń co w misji 01. `--help` i `new-game --help` pokazują polecenia
i opcje w ramkach Typera. `new-game --class wizard` kończy się komunikatem „Invalid value for
'--class' / '--hero-class': 'wizard' is not one of 'warrior', 'mage', 'rogue'.” i kodem 2, a
wywołanie bez polecenia komunikatem „Missing command.” i kodem 2. Zanim dodasz `app()` na końcu
pliku, `task.py` nic nie wypisuje.

**Sprawdź się:** `uv run python level_4_interfaces/missions/02_typer_cli/check.py`. Skrypt
sprawdza:

- że w treści `task.py` są napisy `typer.Typer(` i `app()`; oba są już w komentarzach pliku
  startowego, więc ta część przechodzi od początku;
- te same wywołania `new-game`, `simulate` i `status` co w misji 01, bez wywołania bez polecenia;
- że `--help` wymienia `new-game`, `simulate` i `status`;
- że w pliku nie ma tekstu `import argparse`.

Nie sprawdza, czy `--class` korzysta z wyliczenia: klasa jako zwykły napis, z błędem dopiero przy
zamianie na `HeroClass`, też przechodzi. Import w postaci `from argparse import …` nie zostanie
wykryty. Nie sprawdza wartości domyślnych ani danych w `status` poza imieniem. Te elementy porównaj
z instrukcją i listą „Checklist”.

### Quest Master CLI: projekt zamykający etap {#quest-master-cli}

Mapa kursu nazywa ten projekt punktem kontrolnym („Checkpoint”) i umieszcza go na końcu etapu
World 1. Narzędzie postępu wymienia go w tym etapie, a instrukcja podaje „Requires: Level 4,
Missions 01–02”. Instrukcja misji 02 kieruje dalej do misji 03, z pominięciem projektu. Instrukcja
projektu kieruje do projektu 02, z pominięciem misji 03 i 04. W tym zestawie kieruj się kolejnością
zadań na tej stronie.

**Cel:** zbudować w Typerze trzy polecenia: kartę bohatera, listę potworów i symulację walki, z
przyjaznym komunikatem zamiast tracebacku, gdy nazwa jest nieznana.

**Zakres pracy:** w `level_4_interfaces/projects/01_quest_master_cli/task.py` gotowe są
`app = typer.Typer(...)`, dane trzech bohaterów (Ada, Zara, Rex) i trzech potworów (Goblin, Orc,
Dragon) z samymi punktami życia, szkielety poleceń z opcjami oraz wywołanie `app()`. Zaimplementuj:

- `hero --name`: kartę bohatera z imieniem, klasą i HP;
- `monsters`: listę wszystkich potworów z HP;
- `battle --hero --monster`: symulację walki i jej wynik;
- dla nieznanego bohatera albo potwora: komunikat przez `typer.echo()` i `raise typer.Exit(1)`, bez
  tracebacku Pythona.

Instrukcja podaje przykładowe wyniki, na przykład „Ada defeats Goblin after 4 rounds!” i „Error:
hero 'Unknown' not found. Try: Ada, Zara, Rex”, ale nie podaje zasad walki. Szkielet `hero` ma też
opcję `--class` („Filter by class”), której instrukcja nie opisuje. Tabela „Commands” zapisuje
polecenia jako `quest …`. W repozytorium nie ma polecenia `quest`: uruchamiasz je przez `task.py`,
jak w części „How to test”.

**Rezultat:** w katalogu projektu `uv run python task.py hero --name Ada` wypisuje kartę bohatera,
`monsters` listę potworów, a `battle --hero Ada --monster Goblin` wynik walki. `battle --hero
Unknown --monster Goblin` wypisuje komunikat o błędzie i kończy się kodem 1. Zanim uzupełnisz
polecenia, każde kończy się błędem `NotImplementedError`.

**Sprawdź się:** w katalogu projektu `uv run python check.py`. Skrypt sprawdza:

- że `app` jest obiektem `typer.Typer` z poleceniami `hero`, `monsters` i `battle`;
- że `hero --name Ada` kończy się kodem 0 i wypisuje imię Ada;
- że `monsters` kończy się kodem 0 i wypisuje co najmniej dwie z nazw Goblin, Orc i Dragon;
- że `battle --hero Ada --monster Goblin` kończy się kodem 0 i coś wypisuje;
- że `battle --hero Unknown --monster Goblin` kończy się kodem różnym od 0 i wypisuje komunikat bez
  słów „traceback” i „KeyError”.

Nie sprawdza nieznanego potwora: traceback przy `--monster Unknown` przechodzi sprawdzenie. Nie
sprawdza treści karty bohatera poza imieniem, pełnej listy potworów ani treści wyniku walki. Te
elementy porównaj z przykładami w instrukcji.

## Oczekiwane rezultaty

- `check.py` misji 01 i 02 oraz projektu Quest Master CLI kończy się komunikatem o ukończeniu.
- Polecenia z części „Run” misji i „How to test” projektu działają bez pytań `input()` i dają wyniki
  opisane przy zadaniach.
- Niedozwolona klasa bohatera, brak zapisu i nieznana nazwa kończą się komunikatem i kodem wyjścia
  różnym od 0.

## Wskazówki

- Kod wyjścia 0 oznacza sukces. `argparse` i Typer przy błędnych argumentach same kończą program
  kodem 2, a kod 1 ustawiasz w swoim kodzie (`sys.exit(1)` albo `raise typer.Exit(1)`). W
  powłokach bash i zsh kod ostatniego polecenia wypisuje `echo $?`.
- Części „Break it on purpose” i „Fix it” obu misji każą podać niedozwoloną klasę `wizard`.
  Komunikat o błędzie wypisuje wtedy biblioteka, a nie Twój kod.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. Jeśli
  nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań na tej stronie.
- Następny etap poziomu 4, „World 2: Logging and Observability”, opisuje
  [zestaw 6](world-2-logging-and-observability.md).
