---
title: "Czytelne wyniki, raporty i polecenie rpg"
summary: "Trzeci etap poziomu 4 kursu Python RPG Questbook (World 3: User-Facing Output): dwie misje o czytelnym wyniku w terminalu z biblioteką Rich i o raportach z sesji gry oraz projekt Installable CLI Tool, który zamyka ten etap i cały poziom 4."
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
    path: pyproject.toml
    lang: en
    label: "Konfiguracja repozytorium kursu: wpis [project.scripts] z poleceniem rpg"
tasks:
  misja-05:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/missions/05_rich_terminal_output/README.md
        lang: en
        label: "Instrukcja: Mission 05 — Rich Terminal Output"
  misja-06:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/missions/06_session_reports/README.md
        lang: en
        label: "Instrukcja: Mission 06 — Session Reports"
  installable-cli-tool:
    materials:
      - repository: python-rpg-questbook
        path: level_4_interfaces/projects/03_installable_cli_tool/README.md
        lang: en
        label: "Instrukcja: Project 03 — Installable CLI Tool"
---
Ten zestaw obejmuje trzeci, ostatni etap poziomu 4 kursu Python RPG Questbook, „World 3:
User-Facing Output”. Najpierw porządkujesz to, co widzi gracz: statystyki w tabeli, walkę w
panelach, błędy w osobnym strumieniu. Potem zapisujesz podsumowanie sesji w dwóch raportach, JSON i
Markdown. Na końcu łączysz wszystko z poziomu 4 w jeden pakiet uruchamiany poleceniem `rpg`.
Pierwsze dwa zadania to misje 05 i 06. Trzecie to projekt Installable CLI Tool, który mapa kursu
nazywa walką z bossem („Boss Fight”) i umieszcza na końcu poziomu 4. Instrukcje, kod, pliki danych i
komunikaty skryptów sprawdzających są po angielsku. Ta strona streszcza je po polsku i odsyła do
instrukcji.

## Przygotowanie do zestawu

Zestaw jest dalszym ciągiem [zestawu 5](world-1-command-line-interface.md) i
[zestawu 6](world-2-logging-and-observability.md). Instalację repozytorium, budowę misji i miejsce
wpisywania poleceń opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1.
Biblioteka Rich instaluje się razem z innymi zależnościami.

**Co wynosisz z wcześniejszych zestawów.** Misje 05 i 06 mają własne, samodzielne pliki. Misja 06
korzysta z modelu Pydantic i metody `model_dump_json()`, znanych z zapisu gry w
[zestawie 2](world-2-persistence.md). Projekt łączy wszystkie misje poziomu 4. Kroki 2–4 jego
instrukcji każą przenieść do pakietu `rpg/` Twój kod z misji 03–06: funkcje wyniku z misji 05,
konfigurację logów z misji 03 i 04 oraz raporty z misji 06. Tak jak w projekcie SQLite Repository
Backend z [zestawu 3](world-3-integration.md#sqlite-repository-backend), przenosisz go ręcznie:
projekt nie importuje plików misji.

**Polecenie `rpg`.** Plik `pyproject.toml` w katalogu głównym repozytorium rejestruje polecenie
`rpg` i wskazuje katalog `rpg/` tego projektu jako pakiet `rpg`:

```toml
[project.scripts]
rpg = "rpg.cli:main"
```

Polecenie `uv sync` z przygotowania do zestawu 1 instaluje więc ten pakiet w trybie edytowalnym w
środowisku `.venv` repozytorium i tworzy tam polecenie `rpg`. Krok 6 instrukcji tylko to objaśnia:
nie zmieniasz `pyproject.toml` i nie instalujesz niczego ponownie, a zmiany w plikach `rpg/` działają
od razu. Poza środowiskiem `.venv` nic się nie instaluje. W świeżej kopii repozytorium polecenie
zachowuje się tak:

- `uv run rpg …` działa w każdym katalogu repozytorium i zawsze uruchamia pakiet z tego projektu.
  Poza repozytorium `uv` nie znajduje projektu i zgłasza „Failed to spawn: `rpg`”. Instrukcja mówi,
  że polecenie działa „from anywhere”. Poza repozytorium tak jest dopiero po aktywacji środowiska
  `.venv`.
- Katalogi `saves/`, `logs/` i `reports/` powstają w katalogu projektu niezależnie od tego, skąd
  uruchamiasz polecenie, bo ścieżki są liczone względem pakietu.
- `uv run python -m rpg.cli …`, które instrukcja podaje jako trzeci sposób uruchomienia, działa z
  katalogu głównego. W katalogach z własnym pakietem `rpg/`, na przykład w projektach końcowych
  poziomów 2 i 3, Python znajduje najpierw tamten pakiet i zgłasza „No module named rpg.cli”.
- `uv run rpg --help` działa od razu po instalacji i wymienia pięć poleceń, zanim cokolwiek
  zaimplementujesz. Działająca pomoc nie oznacza więc działających poleceń.

**Polecenia.** Wszystkie polecenia zestawu, także projektu, wpisujesz w katalogu głównym
repozytorium.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypty misji wczytują Twój `task.py` jako moduł i wywołują jego
funkcje na własnych przykładach, a wynik w terminalu albo w plikach tymczasowych porównują z
oczekiwanym. Skrypt projektu czyta pliki pakietu i uruchamia polecenia jako programy. Gdy wszystko
się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się nie
zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy sprawdzasz samodzielnie: uruchamiasz `task.py` albo polecenie
`rpg` i porównujesz wynik z instrukcją. Części instrukcji „Break it on purpose” i „Fix it”, zadania
poboczne („Side quest”) i lista „Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych,
konfiguracja `pyproject.toml` i komunikaty skryptów `check.py`.

## Zadania

### Rich Terminal Output: tabele i panele w terminalu {#misja-05}

**Cel:** pokazać statystyki bohatera jako tabelę, a początek i wynik walki jako panele biblioteki
Rich, z kolorem tylko tam, gdzie niesie znaczenie, i wysyłać komunikaty o błędach do strumienia
błędów (stderr).

**Zakres pracy:** w `level_4_interfaces/missions/05_rich_terminal_output/task.py` gotowe są dwie
konsole, `console = Console()` i `error_console = Console(stderr=True)`, importy `Table`, `Panel` i
`Text` oraz uproszczona gra. Gra wywołuje Twoje funkcje, a dopóki ich nie uzupełnisz, wypisuje te
same informacje zwykłym `print()`. Według instrukcji i komentarzy `TODO` zaimplementuj:

- `show_hero_stats(hero)`: tabelę `Table` z kolumnami Stat i Value i wierszami Name, Class, HP (na
  przykład „96 / 120”, na zielono od połowy HP, inaczej na czerwono), Gold, Potions oraz W / L;
- `show_combat_start(hero, monster)`: panel `Panel` z tytułem „⚔ Battle”, imionami i HP obu stron;
- `show_combat_result(winner, gold_gained)`: panel „Victory!” ze zdobytym złotem i zieloną ramką
  albo „Defeated!” z czerwoną;
- `show_error(message)`: wypisanie komunikatu przez `error_console` stylem `bold red`.

**Rezultat:** gra z polecenia z części „Run” pokazuje przed każdym wyborem tabelę statystyk, a w
walce panele. Nieznane polecenie w menu wypisuje komunikat o błędzie na stderr. Polecenie z części
„Break it on purpose” kończy się na `2>/dev/null`, czyli odrzuca stderr, a nie stdout, jak mówi
opis. Z poprawnym `show_error()` komunikat o nieznanym poleceniu przy tym poleceniu znika, a po
zmianie na `console` zostaje. Efekt z opisu daje przekierowanie stdout (`>/dev/null`), ale wtedy
nie widać też pytań gry.

**Sprawdź się:** `uv run python level_4_interfaces/missions/05_rich_terminal_output/check.py`.
Skrypt wywołuje funkcje dla bohatera Ada (HP 96/120, 30 sztuk złota) i goblina, przechwytując ich
wynik, i sprawdza:

- że `show_hero_stats()` wypisuje Ada, 96, 120 i 30;
- że `show_combat_start()` wypisuje imiona Ada i Goblin;
- że `show_combat_result()` coś wypisuje dla zwycięstwa i dla porażki;
- że `show_error()` wypisuje komunikat na stderr, a nie na stdout;
- że w treści czterech funkcji nie ma `print()`;
- że w pliku są napisy `Console()`, `Table` i `Panel`; wszystkie są już w pliku startowym.

Nie sprawdza więc, czy naprawdę używasz `Table` i `Panel`: zwykły tekst wypisany przez
`console.print()` przechodzi. Nie sprawdza kolorów ramek i HP ani wierszy Potions i W / L. Te
elementy porównaj, uruchamiając grę.

### Session Reports: raporty JSON i Markdown {#misja-06}

**Cel:** na koniec sesji zapisać jeden model danych, `SessionSummary`, w dwóch raportach: JSON dla
programów i Markdown dla gracza.

**Zakres pracy:** w `level_4_interfaces/missions/06_session_reports/task.py` gotowe są model
Pydantic `SessionSummary` z polami `started_at`, `hero_name`, `hero_class`, `battles`, `wins`,
`losses`, `gold_earned`, `final_hp` i `max_hp` oraz metodą `to_json()`, katalog `REPORTS_DIR`
(`reports/` w katalogu misji) i program, który losuje wyniki krótkiej sesji. Według instrukcji i
komentarzy `TODO` zaimplementuj:

- `SessionSummary.to_markdown()`: nagłówek z imieniem bohatera, datę z `started_at` w formacie
  `%Y-%m-%d %H:%M`, klasę, liczbę walk, zwycięstw i porażek, zdobyte złoto oraz końcowe i
  maksymalne HP;
- `generate_json_report(session, path)` i `generate_md_report(session, path)`: zapis obu raportów z
  utworzeniem brakującego katalogu;
- `generate_reports(session, reports_dir)`: nazwy plików `session_<data>_<godzina>.json` i `.md` z
  datą sesji w formacie `%Y-%m-%d_%H%M`, wywołanie obu funkcji i zwrócenie obu ścieżek.

**Rezultat:** `task.py` wypisuje ścieżki obu raportów w `reports/` i podsumowanie sesji. Nazwa
pliku ma dokładność do minuty, więc dwa uruchomienia w tej samej minucie zastępują te same pliki.
Zanim uzupełnisz `generate_reports()`, `task.py` wypisuje „TODO: implement generate_reports()
first.”.

**Sprawdź się:** `uv run python level_4_interfaces/missions/06_session_reports/check.py`. Skrypt
tworzy sesję z 1 lipca 2026, godz. 15:30 (Ada, warrior, 5 walk, 3 zwycięstwa, 2 porażki, 70 sztuk
złota) i sprawdza:

- że `to_markdown()` zawiera Ada, warrior, 3, 2, 70 i znak `#`;
- że `generate_json_report()` w nieistniejącym podkatalogu katalogu tymczasowego tworzy poprawny
  JSON z polami `hero_name` równym Ada i `wins` równym 3;
- że `generate_md_report()` tworzy plik z imieniem bohatera;
- że `generate_reports()` tworzy oba pliki z fragmentem `2026-07-01_1530` w nazwie i z
  rozszerzeniami `.json` i `.md`.

Nie sprawdza daty i końcowego HP w raporcie Markdown. Liczby zwycięstw i porażek też nie są
sprawdzone, bo cyfry 3 i 2 występują już w dacie. Nazwa z sekundami przechodzi, bo zawiera
wymagany fragment. Te elementy porównaj, otwierając wygenerowane raporty.

### Installable CLI Tool: jedno polecenie rpg {#installable-cli-tool}

Mapa kursu nazywa ten projekt walką z bossem („Boss Fight”) i umieszcza go na końcu etapu World 3,
czyli na końcu poziomu 4. Narzędzie postępu wymienia go w tym etapie. Opis kursu przedstawia walkę z
bossem jako duże zadanie, które łączy wszystko z poziomu. Instrukcja misji 06 kieruje dalej właśnie
do tego projektu.

**Cel:** połączyć wyniki misji 01–06 w jeden pakiet `rpg` z pięcioma poleceniami Typera, logami w
plikach, wynikiem przez Rich i raportami z sesji. Warstwa domeny zostaje bez zmian.

**Zakres pracy:** w katalogu `level_4_interfaces/projects/03_installable_cli_tool/` są pakiet
`rpg/`, katalog `data/` z plikami `monsters.json` (cztery potwory, z Dragon), `hero_classes.json` i
`weapons.json` oraz `task.py`, który uruchamia tę samą aplikację co polecenie `rpg`. Według kroków
instrukcji:

1. `rpg/domain.py` z klasami `Hero`, `HeroClass` i `Monster` jest już gotowy i ma zostać bez
   Pydantic, Typera i Rich. W `rpg/schemas.py` gotowe są `SaveGameModel`, `SessionSummary` i
   funkcje zapisu bohatera. Zostaje `SessionSummary.to_markdown()`, jak w misji 06.
2. W `rpg/output.py` uzupełnij cztery funkcje z misji 05. Obie konsole są gotowe.
3. W `rpg/logging_setup.py` uzupełnij `setup_logging()`, `add_file_handler()` i
   `setup_log_files()` z misji 03 i 04, z plikiem `combat.log` dla loggera `rpg.combat`.
4. W `rpg/game.py` uzupełnij `load_monsters()` z walidacją wpisów (model `MonsterConfig` skopiuj z
   kodu startowego poziomu 4 albo z poziomu 3), `load_hero_classes()`, `make_hero()`, interaktywną
   `run_combat()`, `simulate_battles()` bez `input()`, z wynikiem `SessionSummary`, oraz
   `generate_reports()` z misji 06. Ścieżki i funkcje zapisu i odczytu bohatera są gotowe.
   Instrukcja każe przenieść `simulate_battles()` z kodu startowego, ale kod startowy jej nie ma.
   Co ma robić, opisuje komentarz `TODO`, a uproszczoną walkę bez `input()` mają misje 01 i 02.
5. W `rpg/cli.py` uzupełnij treść pięciu poleceń: `new-game`, `play`, `simulate`, `report` i
   `status`. Szkielety z opcjami, funkcja `_setup()`, która włącza logi na początku każdego
   polecenia, i `main()` są gotowe.
6. Wpis `[project.scripts]` jest gotowy (zobacz „Polecenie `rpg`” wyżej).

Plik `weapons.json` nie jest używany w żadnym kroku.

**Rezultat:** polecenia z części „Run” instrukcji: `uv run rpg --help` wymienia pięć poleceń,
`uv run rpg new-game --name Ada --class warrior` zapisuje bohatera, a `uv run rpg simulate
--battles 5` symuluje walki, zapisuje bohatera i tworzy raporty JSON i Markdown w `reports/`.
`uv run rpg status` pokazuje tabelę statystyk, a `uv run rpg report` wypisuje najnowszy raport
Markdown. `uv run rpg play` uruchamia interaktywną grę. Logi trafiają do `logs/app.log` i
`logs/combat.log`, a także do terminala. Te same polecenia działają przez `uv run python
level_4_interfaces/projects/03_installable_cli_tool/task.py …`. Zanim uzupełnisz polecenia,
`--help` działa, a pozostałe kończą się błędem `NotImplementedError`.

Część „Break it on purpose” każe usunąć wpis `[project.scripts]` z `pyproject.toml`, wspólnego dla
całego repozytorium, i uruchomić `uv sync`. Polecenie `rpg` znika, a `task.py` nadal działa.
Komunikat różni się od podanego w instrukcji („No such command 'rpg'”): `uv run rpg --help`
zgłasza „Failed to spawn: `rpg`”, a powłoka bez `uv` zgłasza, że nie zna polecenia. Część „Fix it”
przywraca wpis i po `uv sync` polecenie wraca. Bez tego wpisu `check.py` projektu kończy się
błędem.

**Sprawdź się:**
`uv run python level_4_interfaces/projects/03_installable_cli_tool/check.py`. Skrypt sprawdza:

- w treści plików pakietu: brak `BaseModel`, `from pydantic`, `import typer` i `from rich` w
  `domain.py`, napis `typer.Typer(` i nazwy pięciu poleceń w `cli.py`, `SessionSummary` i
  `SaveGameModel` w `schemas.py` oraz nazwy funkcji w `output.py` i `logging_setup.py`; wszystko to
  jest już w plikach startowych;
- że `task.py --help` kończy się kodem 0 i wymienia `new-game`, `simulate` i `status`;
- w katalogu projektu, że `new-game --name CheckHero --class warrior`, potem `status`, `simulate
  --battles 2` i `report` kończą się kodem 0;
- że `pyproject.toml` ma wpis `[project.scripts]` z `rpg`, a `uv run rpg --help` uruchomione w
  katalogu głównym kończy się kodem 0 i wymienia te same trzy polecenia.

Skrypt zapisuje przy tym bohatera CheckHero w `saves/` projektu, zastępując Twój zapis, i dopisuje
logi oraz raporty. Nie uruchamia `play` i nie sprawdza treści wyników. Nie sprawdza, czy `simulate`
tworzy raporty i zapisuje bohatera, czy `report` wypisuje raport ani czy powstają logi:
nieuzupełniony `logging_setup.py` przechodzi, bo `_setup()` pomija `NotImplementedError`. Zastępczy
`typer.echo()` z komentarza `TODO` w `status` przechodzi także bez tabeli Rich. Te elementy porównaj
z częścią „Run” i listą „Checklist” instrukcji.

## Oczekiwane rezultaty

- `check.py` misji 05 i 06 oraz projektu Installable CLI Tool kończy się komunikatem o ukończeniu.
- Gra z misji 05 pokazuje tabelę i panele, a błędy wypisuje na stderr. Misja 06 tworzy raporty
  JSON i Markdown w `reports/`.
- Polecenie `rpg` uruchamia w katalogu repozytorium wszystkie pięć poleceń z wynikami opisanymi
  przy projekcie, z logami w `logs/` i raportami w `reports/`.

## Wskazówki

- Pakiet `rpg` jest zainstalowany w trybie edytowalnym, więc po zmianie pliku w `rpg/` od razu
  uruchamiasz polecenie ponownie, bez instalacji.
- Części „Break it on purpose” i „Fix it” każą w misji 06 usunąć tworzenie katalogu i zobaczyć
  `FileNotFoundError`. Instrukcja nazywa ten wiersz `reports_dir.mkdir(...)`, a w komentarzach
  `TODO` jest to `path.parent.mkdir(...)` w obu funkcjach zapisu. W projekcie dotyczą wpisu w
  `pyproject.toml`, opisanego przy projekcie.
- Pliki `*.log` i `save_game.json` są w `.gitignore` repozytorium, a raporty `session_*.json` i
  `session_*.md` nie są.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. Jeśli
  nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań na tej stronie.
- Po poziomie 4 mapa kursu przechodzi do poziomu 5, „Production Quality and Maintainability”.
