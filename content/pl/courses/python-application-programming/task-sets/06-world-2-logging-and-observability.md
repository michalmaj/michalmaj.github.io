---
title: "Logowanie zdarzeń i pliki logów"
summary: "Drugi etap poziomu 4 kursu Python RPG Questbook (World 2: Logging and Observability): dwie misje o zastąpieniu print() modułem logging i o zapisie logów do plików oraz projekt Observable Battle Runner, który zamyka ten etap."
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
tasks:
  misja-03:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/missions/03_stdlib_logging/README.md
        lang: en
        label: "Instrukcja: Mission 03 — stdlib logging"
  misja-04:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/missions/04_log_files/README.md
        lang: en
        label: "Instrukcja: Mission 04 — Log Files"
  observable-battle-runner:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/projects/02_observable_battle_runner/README.md
        lang: en
        label: "Instrukcja: Project 02 — Observable Battle Runner"
---
Ten zestaw obejmuje drugi etap poziomu 4 kursu Python RPG Questbook, „World 2: Logging and
Observability”. Gra oddziela komunikaty dla gracza od zdarzeń technicznych. Zdarzenia trafiają do
loggera z poziomem ważności, od szczegółów (`DEBUG`) po błędy (`ERROR`), a potem także do plików,
które zostają po zakończeniu programu. Pierwsze dwa zadania to misje 03 i 04. Trzecie to projekt
Observable Battle Runner, który mapa kursu nazywa punktem kontrolnym („Checkpoint”) i umieszcza na
końcu tego etapu. Instrukcje, kod, pliki danych i komunikaty skryptów sprawdzających są po
angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Zestaw jest dalszym ciągiem [zestawu 5](world-1-command-line-interface.md). Instalację
repozytorium, budowę misji i miejsce wpisywania poleceń opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1. Moduł
`logging` należy do biblioteki standardowej Pythona.

**Co wynosisz z wcześniejszych zestawów.** Misje 03 i 04 pracują na pełnej grze z poziomu 3, z
modelami Pydantic i zapisem gry, ale tego kodu nie piszesz: jest w plikach misji gotowy. Misja 04
zawiera gotową część misji 03: funkcję `setup_logging()` i wywołania loggera. Projekt korzysta z
Typera z zestawu 5 (`typer.echo()`, `typer.Exit`) i z logowania z misji 03 i 04. Instrukcja podaje
„Requires: Level 4, Missions 01–04”. Opis kursu przedstawia projekty punktów kontrolnych jako
samodzielne ćwiczenia: projekt ma własne polecenie i dane i nie korzysta z kodu projektu Quest
Master CLI.

**Pliki i dane.** Misje 03 i 04 mają własne pliki `task.py` i katalogi `data/` z plikami
`monsters.json` (obiekt `{"monsters": [...]}` z polami `name`, `hp`, `atk`, `def` i `gold`) oraz
`hero_classes.json` (klasy bohatera z polami `hp`, `atk`, `def` i `description`). Obie misje to gra
interaktywna: pyta o imię, klasę i kolejne akcje. Zapis gry i dziennik walk trafiają do katalogu
`saves/` misji, a w misji 04 logi do katalogu `logs/`.

**Polecenia.** Polecenia misji wpisujesz w katalogu głównym repozytorium. Projekt uruchamiasz,
zgodnie z jego instrukcją, z katalogu projektu,
`level_4_interfaces/projects/02_observable_battle_runner/`.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypty misji wczytują Twój `task.py` jako moduł i wywołują
jego funkcje na własnych danych w katalogu tymczasowym. Gry nie uruchamiają. Skrypt projektu
uruchamia `task.py` jako program w katalogu tymczasowym i czyta zapisane tam logi. Gdy wszystko się
zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się nie zgadza,
wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy sprawdzasz samodzielnie: uruchamiasz `task.py`, czytasz logi i
porównujesz wynik z instrukcją. Części instrukcji „Break it on purpose” i „Fix it”, zadania
poboczne („Side quest”) i lista „Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### stdlib logging: logger zamiast print() {#misja-03}

**Cel:** zastąpić `print()` dla zdarzeń technicznych wywołaniami loggera z właściwym poziomem
ważności, a komunikaty dla gracza zostawić jako `print()`.

**Zakres pracy:** w `level_4_interfaces/missions/03_stdlib_logging/task.py` gotowe są logger
modułu, `logger = logging.getLogger(__name__)`, modele Pydantic `MonsterConfig` i `SaveGameModel`
oraz cała gra. Według instrukcji i komentarzy `TODO`:

- zaimplementuj `setup_logging(level)`: wywołanie `logging.basicConfig()` z poziomem zamienionym z
  napisu, na przykład `"INFO"`, na stałą modułu `logging` i z formatem, który zawiera czas, poziom,
  nazwę loggera i treść;
- zamień każdy `print()` oznaczony komentarzem `# REPLACE WITH LOGGING` na wywołanie loggera z
  poziomem podanym w tym komentarzu (`debug`, `info`, `warning` albo `exception`) i usuń komentarz;
- w `main()` wywołaj `setup_logging()` z poziomem ze zmiennej środowiskowej `RPG_LOG_LEVEL`, a gdy
  jej nie ma, z poziomem `INFO`.

Komentarz przy ataku bohatera stoi nad komunikatem dla gracza „You deal … damage”. Instrukcja
podaje ten komunikat jako przykład tekstu, który zostaje `print()`.

**Rezultat:** polecenie z części „Run” uruchamia grę. Logi trafiają do strumienia błędów (stderr),
a komunikaty gry do zwykłego wyjścia. Wiersze logów mają czas, poziom i nazwę loggera; uruchomiony
skrypt ma nazwę `__main__`. Przy domyślnym poziomie `INFO` widać między innymi ostrzeżenie o
niepoprawnym wyborze klasy, początek walki i zapis gry. Z drugim poleceniem z części „Run”,
`RPG_LOG_LEVEL=DEBUG uv run python …`, widać też szczegóły ataków i wierszy dziennika walk. Zanim
`main()` wywoła `setup_logging()`, gra działa z dotychczasowymi komunikatami `print()`.

**Sprawdź się:** `uv run python level_4_interfaces/missions/03_stdlib_logging/check.py`. Skrypt
sprawdza:

- że `setup_logging("DEBUG")` ustawia poziom głównego loggera na `DEBUG`, a następne
  `setup_logging("WARNING")` na `WARNING`;
- że w pliku jest `logging.getLogger(` i nie ma już komentarzy `# REPLACE WITH LOGGING`;
- na własnych danych, z obiektem zapisującym wywołania w miejscu loggera, że każde zdarzenie używa
  poziomu z komentarza: `warning` przy pominiętym błędnym potworze, niezgodnej wersji zapisu i
  niepoprawnym wyborze klasy; `exception` przy brakującym pliku danych i uszkodzonym zapisie; `info`
  po zapisie i odczycie gry oraz na początku walki; `debug` przy braku zapisu, wierszu dziennika
  walk i ataku bohatera;
- że `main()` wywołuje `setup_logging()`.

Według
[dokumentacji modułu `logging`](https://docs.python.org/3/library/logging.html#logging.basicConfig)
`basicConfig()` nic nie robi, jeśli główny logger ma już handler, chyba że podasz `force=True`.
Wersja z samym poziomem i formatem, taka jak w komentarzu `TODO` i w gotowej funkcji
`setup_logging()` z misji 04, zmienia więc poziom tylko przy pierwszym wywołaniu. Skrypt zgłasza
wtedy błąd „setup_logging('WARNING') should set level to 30, got 10”.

Skrypt wymaga dokładnie poziomów z komentarzy. `logger.error()` zamiast `logger.exception()` przy
uszkodzonym zapisie nie przechodzi, choć lista „Checklist” dopuszcza w blokach `except` oba
wywołania. Nie sprawdza formatu logów, użycia zmiennej `RPG_LOG_LEVEL` ani tego, czy komunikaty dla
gracza zostały jako `print()`. Te elementy porównaj, uruchamiając grę.

### Log Files: logi zapisane w plikach {#misja-04}

**Cel:** zapisywać logi także do plików, które zostają po zakończeniu programu: wszystkie zdarzenia
od poziomu `INFO` do `app.log`, a zdarzenia walki do `combat.log`.

**Zakres pracy:** w `level_4_interfaces/missions/04_log_files/task.py` gotowe są `setup_logging()` i
wywołania loggera z misji 03, drugi logger, `combat_logger = logging.getLogger(__name__ +
".combat")`, i katalog `LOG_DIR`, czyli `logs/` w katalogu misji. Według instrukcji i komentarzy
`TODO`:

- zaimplementuj `add_file_handler(target_logger, path, level, fmt)`: utworzenie brakującego
  katalogu, handler `logging.FileHandler` z kodowaniem UTF-8, jego poziom i format oraz dodanie go
  do loggera;
- zaimplementuj `setup_log_files(log_dir)`: `app.log` na głównym loggerze z poziomem `INFO` i
  `combat.log` na `combat_logger` z poziomem `DEBUG`;
- zamień cztery `print()` oznaczone komentarzem `# USE combat_logger` na wywołania
  `combat_logger.debug()` albo `combat_logger.info()`, jak podaje komentarz.

Część „Goal” instrukcji opisuje `combat.log` jako „INFO and above”, a część „Your task” i komentarz
`TODO` podają dla niego poziom `DEBUG`.

**Rezultat:** po zagraniu (polecenie z części „Run”) w katalogu misji jest katalog `logs/` z plikami
`app.log` i `combat.log`, które wypisują polecenia `cat` z instrukcji. Logi nadal pojawiają się też
w terminalu. Wpisy loggera walki od poziomu `INFO` trafiają do obu plików, bo logger
`__main__.combat` przekazuje je do głównego loggera. Przy domyślnym poziomie `INFO` w `combat.log` są tylko wiersze o początku walki.
Wiersze `DEBUG` z atakami i turami zatrzymuje sam logger walki, który dziedziczy poziom `INFO` po
głównym loggerze, mimo że handler pliku ma poziom `DEBUG`. Pojawiają się po uruchomieniu z
`RPG_LOG_LEVEL=DEBUG`. Pliki logów rosną z każdym uruchomieniem. Zanim uzupełnisz
`setup_log_files()`, `task.py` wypisuje „TODO: implement setup_log_files() first.” i kończy pracę.

**Sprawdź się:** `uv run python level_4_interfaces/missions/04_log_files/check.py`. Skrypt w
katalogu tymczasowym sprawdza:

- że `add_file_handler()` dla pliku w nieistniejącym podkatalogu tworzy plik, a zapisany wpis
  zawiera treść i nazwę poziomu `INFO`;
- że `setup_log_files()` tworzy `app.log` i `combat.log`, wpis głównego loggera trafia do
  `app.log`, a wpis `DEBUG` loggera walki do `combat.log`;
- że w pliku nie ma już komentarzy `# USE combat_logger`.

Nie sprawdza poziomów handlerów (handler bez poziomu przechodzi) ani tego, że `combat.log` jest
podpięty do loggera walki: handler na głównym loggerze też przechodzi. Nie sprawdza, czy w miejscu
komentarzy są wywołania `combat_logger`, bo wystarczy usunąć same komentarze. Brak utworzenia
katalogu kończy się błędem `FileNotFoundError` z tracebackiem, a nie komunikatem skryptu. Skrypt nie
uruchamia gry. Te elementy porównaj, grając i czytając pliki logów.

### Observable Battle Runner: projekt zamykający etap {#observable-battle-runner}

Mapa kursu nazywa ten projekt punktem kontrolnym („Checkpoint”) i umieszcza go na końcu etapu
World 2. Narzędzie postępu wymienia go w tym etapie. Instrukcja misji 04 kieruje dalej do misji 05,
z pominięciem projektu. Instrukcja projektu kieruje do projektu 03, z pominięciem misji 05 i 06. W
tym zestawie kieruj się kolejnością zadań na tej stronie.

**Cel:** dodać do polecenia walki w Typerze logi w dwóch plikach: przebieg walki runda po rundzie w
`combat.log`, a początek, wynik i błędy w `app.log`. W terminalu zostają tylko komunikaty dla
użytkownika.

**Zakres pracy:** w `level_4_interfaces/projects/02_observable_battle_runner/task.py` gotowe są
ścieżki `APP_LOG` i `COMBAT_LOG`, dane trzech bohaterów i trzech potworów z HP i siłą ataku,
loggery `logging.getLogger("rpg")` i `logging.getLogger("rpg.combat")`, aplikacja Typera i szkielet
polecenia `battle --hero --monster`. Instrukcja przedstawia projekt jako Quest Master CLI rozszerzony
o logi, ale plik ma tylko polecenie `battle` i własne dane. Kodu projektu z zestawu 5 nie
potrzebujesz. Zaimplementuj:

- `setup_logging()`: handlery plików, czyli `app.log` dla loggera `rpg` od poziomu `INFO` i
  `combat.log` dla loggera `rpg.combat` od poziomu `DEBUG`, bez logów w terminalu;
- `battle`: wywołanie `setup_logging()` na początku, walkę z wpisem w `combat.log` dla każdej rundy
  i wynikiem w `app.log`;
- dla nieznanego bohatera albo potwora: komunikat `typer.echo(..., err=True)`, wpis
  `logger.error()` w `app.log` i `raise typer.Exit(1)`, bez tracebacku.

Instrukcja podaje przykładowe wiersze dziennika rund, ale nie podaje dokładnych zasad walki.

**Rezultat:** w katalogu projektu `uv run python task.py battle --hero Ada --monster Goblin`
wypisuje wynik walki, a w tym katalogu powstają `app.log` i `combat.log`. `battle --hero Ada
--monster Unknown` wypisuje komunikat o błędzie na stderr i kończy się kodem 1, a w `app.log`
pojawia się wpis o błędzie. Ścieżki obu plików są względne, więc pliki powstają w katalogu, z
którego uruchamiasz polecenie. Uruchomione z katalogu głównego zapisze je w katalogu głównym
repozytorium. Zanim uzupełnisz kod, polecenie kończy się błędem `NotImplementedError`.

**Sprawdź się:** w katalogu projektu `uv run python check.py`. Skrypt sprawdza:

- że `app` jest obiektem `typer.Typer`, a w pliku jest wywołanie `logging.getLogger()`, które ma
  już plik startowy;
- w katalogu tymczasowym, że `battle --hero Ada --monster Goblin` kończy się kodem 0 i tworzy oba
  pliki, `app.log` zawiera słowo „battle”, „combat”, „ada” albo „goblin”, a `combat.log` co
  najmniej jeden wiersz;
- że `battle --hero Ada --monster Unknown` kończy się kodem różnym od 0 i wypisuje komunikat bez
  tracebacku.

Wpis o błędzie w `app.log` skrypt tylko potwierdza, jeśli go znajdzie. Jego brak nie zatrzymuje
sprawdzenia. Nie sprawdza nieznanego bohatera, strumienia komunikatu o błędzie (stdout zamiast
stderr przechodzi), liczby wpisów o rundach ani tego, czy logi trafiają także do terminala. Te
elementy porównaj z instrukcją.

## Oczekiwane rezultaty

- `check.py` misji 03 i 04 oraz projektu Observable Battle Runner kończy się komunikatem o
  ukończeniu.
- W misjach 03 i 04 gra wypisuje logi z czasem, poziomem i nazwą loggera, a w misji 04 zapisuje je
  w `logs/app.log` i `logs/combat.log`.
- W projekcie walka zapisuje rundy w `combat.log`, a wynik i błędy w `app.log`. Nieznana nazwa
  kończy się komunikatem na stderr i kodem 1.

## Wskazówki

- Części „Break it on purpose” i „Fix it” każą w misji 03 wywołać celowo błąd w `load_game()` i
  zobaczyć traceback zapisany przez `logger.exception()`, a w misji 04 usunąć `app.log` w trakcie
  gry albo wyłączyć tworzenie katalogu i zobaczyć `FileNotFoundError`. Instrukcja nazywa ten wiersz
  `log_dir.mkdir(...)`, a w `add_file_handler()` jest to `path.parent.mkdir(...)`.
- Pliki `*.log`, `save_game.json` i `combat_log.csv` są w `.gitignore` repozytorium.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. Jeśli
  nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań na tej stronie.
- Ostatni etap poziomu 4, „World 3: User-Facing Output”, opisuje
  [zestaw 7](world-3-user-facing-output.md).
