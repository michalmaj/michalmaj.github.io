---
title: "Dziennik walk, ustawienia i SQLite"
summary: "Trzeci etap poziomu 3 kursu Python RPG Questbook (World 3: Integration): dwie misje o repozytorium dziennika walk i o ustawieniach aplikacji oraz projekt SQLite Repository Backend, który zamyka ten etap i cały poziom 3."
status: published
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu: instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: level_3_validation_and_persistence/README.md
    lang: en
    label: "Poziom 3 — Validation and Persistence: założenia, misje i projekty"
  - repository: python-rpg-questbook
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: podział poziomu 3 na etapy (World 1–3)"
tasks:
  misja-06:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/missions/06_combat_log_repository/README.md
        lang: en
        label: "Instrukcja: Mission 06 — Combat Log Repository"
  misja-07:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/missions/07_settings_and_paths/README.md
        lang: en
        label: "Instrukcja: Mission 07 — Settings and Paths"
  sqlite-repository-backend:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/projects/03_sqlite_repository_backend/README.md
        lang: en
        label: "Instrukcja: Project 03 — SQLite Repository Backend"
---
Ten zestaw obejmuje trzeci, ostatni etap poziomu 3 kursu Python RPG Questbook, „World 3:
Integration”. Najpierw przenosisz zapis dziennika walk do repozytorium, które sprawdza każdy wiersz.
Potem zbierasz ścieżki i ustawienia gry w jednym obiekcie, który można zmieniać zmiennymi
środowiskowymi. Na końcu dodajesz drugi sposób przechowywania danych, bazę SQLite, bez zmian w
logice gry. Pierwsze dwa zadania to misje 06 i 07. Trzecie to projekt SQLite Repository Backend,
który mapa kursu nazywa walką z bossem („Boss Fight”) i umieszcza na końcu poziomu 3. Instrukcje,
kod, pliki danych i komunikaty skryptów sprawdzających są po angielsku. Ta strona streszcza je po
polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Zestaw jest dalszym ciągiem [zestawu 1](world-1-trusted-data.md) i
[zestawu 2](world-2-persistence.md). Instalację repozytorium, budowę misji i miejsce wpisywania
poleceń opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1. Biblioteka
pydantic-settings, z której korzysta misja 07, instaluje się razem z innymi zależnościami.

**Co wynosisz z wcześniejszych zestawów.** Misja 06 stosuje wzorzec repozytorium z misji 05
(interfejs `Protocol` i wersję w pamięci) do dziennika walk i korzysta z walidacji Pydantic z
zestawu 1. Misja 07 jest osobnym tematem: ustawieniami aplikacji. Projekt łączy wszystko z poziomu
3. Jego instrukcja odwołuje się do interfejsów z misji 05 i 06.

**Pliki.** Misje 06 i 07 mają własne, samodzielne pliki. Projekt ma własny pakiet `rpg/` z gotowymi
częściami. Twoje rozwiązania misji 05 i 06 są punktem wyjścia dla kroków 1 i 2 projektu: instrukcja
każe przenieść do pakietu `rpg/` klasy `JsonSaveRepository` i `CsvCombatLogRepository` w taki sam
sposób jak w tych misjach. Nie są to jednak te same pliki. W projekcie zamianę modelu na bohatera
wykonują gotowe funkcje pomocnicze, a `CombatLogRow` pochodzi z `rpg/schemas.py`. Kod przenosisz
więc ręcznie i dopasowujesz. Projekt nie importuje plików misji.

**Kod tylko do przeczytania.** Część „Game problem” instrukcji misji 06 pokazuje funkcję
`_append_log_row()`, którą `run_combat()` w kodzie startowym poziomu 3,
[`starter_raw_rpg/main.py`](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_3_validation_and_persistence/starter_raw_rpg/main.py),
wywołuje wprost. Komentarz na początku pliku opisuje to jako „Smell 4 (M06)”. Misja 07 korzysta z
tego kodu jako przykładu konfiguracji: ścieżki do katalogów kodu startowego są wartościami
domyślnymi jej ustawień. Tego kodu nie edytujesz.

**Dane.** Wiersz dziennika walk to jedna tura walki: `CombatLogRow` z polami `battle_id`, `turn`,
`hero_name`, `hero_class`, `monster`, `action` (`attack` albo `potion`), `damage_dealt`,
`damage_taken`, `hero_hp`, `monster_hp` i `result` (`ongoing`, `win` albo `loss`). Tak samo wygląda
tabela `combat_log` w projekcie. Projekt zapisuje też bohatera w modelu `SaveGameModel` takim jak w misji 04 z zestawu 2.

**Polecenia.** Wszystkie polecenia zestawu, także projektu, wpisujesz w katalogu głównym
repozytorium.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`, który sprawdza Twój kod na własnych przykładach w plikach
tymczasowych. Gdy wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp
lokalnie. Gdy coś się nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy sprawdzasz samodzielnie: uruchamiasz `task.py` i porównujesz
wynik z instrukcją. Części instrukcji „Break it on purpose” i „Fix it”, zadania poboczne („Side
quest”) i lista „Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### Combat Log Repository: dziennik walk z walidacją {#misja-06}

**Cel:** wydzielić zapis dziennika walk z pętli walki do repozytorium, które przyjmuje tylko
poprawne wiersze `CombatLogRow`.

**Zakres pracy:** w `level_3_validation_and_persistence/missions/06_combat_log_repository/task.py`
gotowe są model `CombatLogRow` z ograniczeniami pól (`Literal` dla `action` i `result`, nieujemne
liczby), interfejs `CombatLogRepository` i lista kolumn `FIELDNAMES`. Komentarz na początku pliku
mówi też o zdefiniowaniu modelu i interfejsu, ale oba są już gotowe. Zaimplementuj:

- `CsvCombatLogRepository.append(row)`: dopisanie wiersza do pliku CSV, z nagłówkiem tylko wtedy,
  gdy pliku jeszcze nie ma; komentarz `TODO` dodaje utworzenie brakującego katalogu;
- `CsvCombatLogRepository.read_all()`: pusta lista, gdy pliku nie ma, a w przeciwnym razie lista
  wierszy zamienionych na `CombatLogRow`;
- `InMemoryCombatLogRepository.append(row)` i `InMemoryCombatLogRepository.read_all()`: lista w
  pamięci; `read_all()` zwraca jej kopię.

W katalogu misji jest też plik `sample_log.csv` z ośmioma przykładowymi wierszami w tym samym
formacie. Instrukcja, `task.py` i `check.py` z niego nie korzystają.

**Rezultat:** uruchomiony `task.py` dopisuje dwie tury walki z goblinem do pliku
`logs/combat_log.csv` w katalogu misji i wypisuje je: „Logged 2 turns”, a druga tura ma wynik `win`.
Dziennik tylko przyrasta, więc każde kolejne uruchomienie dopisuje dwie tury i liczba wypisanych tur
rośnie. Zanim uzupełnisz kod, `task.py` wypisuje przypomnienie, co zostało do zrobienia.

**Sprawdź się:**
`uv run python level_3_validation_and_persistence/missions/06_combat_log_repository/check.py`.
Skrypt sprawdza:

- że gotowy model `CombatLogRow` odrzuca `battle_id` równe 0 i akcję `run`;
- w katalogu tymczasowym, że `read_all()` przed zapisem zwraca pustą listę, a po dwóch wywołaniach
  `append` dwa obiekty `CombatLogRow`: pierwszy z `damage_dealt` równym 12, drugi z wynikiem `win`;
- że repozytorium w pamięci zwraca na początku pustą listę, a po zapisie jeden wiersz z poprawnym
  imieniem bohatera.

Nagłówek dopisywany przy każdym wierszu skrypt wykrywa pośrednio: odczyt kończy się wtedy błędem
walidacji. Nie sprawdza, czy `read_all()` repozytorium w pamięci zwraca kopię listy, ani tworzenia
brakującego katalogu. Ten brak widać przy uruchomieniu `task.py`, dopóki w katalogu misji nie ma
katalogu `logs/`. Nie sprawdza też zadania pobocznego.

### Settings and Paths: ustawienia w jednym obiekcie {#misja-07}

**Cel:** zastąpić ścieżki rozproszone po kodzie jednym obiektem ustawień `GameSettings` z
biblioteki pydantic-settings. Ma on wartości domyślne, które można zmienić zmiennymi środowiskowymi
albo plikiem `.env`.

**Zakres pracy:** w `level_3_validation_and_persistence/missions/07_settings_and_paths/task.py`
według instrukcji i komentarzy `TODO`:

- odkomentuj importy i zdefiniuj `GameSettings(BaseSettings)` z polami `data_dir`, `saves_dir`,
  `log_file` (ścieżki `Path`) i `max_potions` (liczba całkowita) oraz z ustawieniem
  `model_config = SettingsConfigDict(env_prefix="RPG_", env_file=".env")`; wartości domyślne podaje
  komentarz `TODO`: katalogi `data` i `saves` kodu startowego, plik `combat_log.csv` w katalogu
  `saves` i 5 mikstur;
- zdefiniuj `get_settings()`, która tworzy obiekt ustawień raz i przy kolejnych wywołaniach zwraca
  ten sam obiekt;
- odkomentuj wiersze w `main()`.

Komentarz na początku pliku dopuszcza też zwykły `BaseModel`. Instrukcja wymaga jednak
`BaseSettings`, a `check.py` sprawdza zmianę ustawienia zmienną środowiskową, której `BaseModel` nie
obsługuje.

**Rezultat:** uruchomiony `task.py` wypisuje cztery ustawienia ze ścieżkami w katalogu
`starter_raw_rpg/` i wiersz „data_dir exists: True”. Przed uzupełnieniem kodu nic nie wypisuje, bo
`main()` zawiera tylko zakomentowane wiersze. Drugie polecenie z instrukcji pokazuje zmianę ustawienia
zmienną środowiskową: wiersz `saves_dir` wskazuje wtedy podany katalog.

```bash
uv run python level_3_validation_and_persistence/missions/07_settings_and_paths/task.py
RPG_SAVES_DIR=/tmp/my_saves uv run python level_3_validation_and_persistence/missions/07_settings_and_paths/task.py
```

Zapis `RPG_SAVES_DIR=… polecenie` działa w powłokach takich jak bash i zsh. Instrukcja podaje też
drugi sposób: plik `.env` z wierszem `RPG_SAVES_DIR=…` w katalogu, z którego uruchamiasz polecenie,
czyli w katalogu głównym repozytorium. Ustawienia z tego pliku działają także podczas `check.py`.
Błędna wartość zapisana w pliku `.env`, na przykład z części „Break it on purpose”, zatrzyma więc
również sprawdzenie.

**Sprawdź się:**
`uv run python level_3_validation_and_persistence/missions/07_settings_and_paths/check.py`. Skrypt
sprawdza:

- że w `task.py` są `GameSettings` i `get_settings` i że obiekt ustawień ma cztery pola;
- że `data_dir` i `saves_dir` są ścieżkami `Path`, a `max_potions` liczbą całkowitą większą od 0;
- że `get_settings()` przy kolejnym wywołaniu zwraca ten sam obiekt;
- że ustawiona zmienna środowiskowa `RPG_SAVES_DIR` zmienia `saves_dir` nowego obiektu
  `GameSettings`.

Nie sprawdza wartości domyślnych, typu `log_file`, odczytu pliku `.env`, odkomentowania wierszy w
`main()` ani zadania pobocznego (pole `debug`). Te elementy porównaj z instrukcją, uruchamiając
`task.py`.

### SQLite Repository Backend: drugi sposób przechowywania danych {#sqlite-repository-backend}

Mapa kursu nazywa ten projekt walką z bossem („Boss Fight”) i umieszcza go na końcu etapu World 3,
czyli na końcu poziomu 3. Narzędzie postępu wymienia go w tym etapie. Opis kursu przedstawia walkę z
bossem jako duże zadanie, które łączy wszystko z poziomu. Instrukcja misji 07 kieruje dalej właśnie
do tego projektu.

**Cel:** dodać bazę SQLite jako drugi sposób przechowywania zapisu gry i dziennika walk, z tymi
samymi interfejsami co w misjach 05 i 06. Logika gry ma się przy tym nie zmienić: zmienia się tylko
obiekt repozytorium przekazany do gry.

**Zakres pracy:** w katalogu `level_3_validation_and_persistence/projects/03_sqlite_repository_backend/`
gotowe są:

- `rpg/domain.py` z klasami `Hero` i `HeroClass` bez Pydantic; komentarz w pliku każe je
  skopiować z poziomu 2, ale są już zdefiniowane;
- `rpg/schemas.py` z modelami `SaveGameModel` i `CombatLogRow`;
- interfejsy w `rpg/save_repo.py` i `rpg/log_repo.py`, funkcje pomocnicze `_model_to_hero()` i
  `_hero_to_model()` oraz lista kolumn `FIELDNAMES`;
- `task.py`, który uruchamia tę samą funkcję `run_demo()` najpierw z zapisem JSON i dziennikiem CSV,
  a potem z SQLite.

Według kroków z instrukcji:

1. W `rpg/save_repo.py` przenieś `JsonSaveRepository.save()` i `JsonSaveRepository.load()` z misji
   05.
2. W `rpg/log_repo.py` przenieś `CsvCombatLogRepository.append()` i
   `CsvCombatLogRepository.read_all()` z misji 06.
3. Zaimplementuj `SqliteSaveRepository`. Metoda `__init__` tworzy tabelę `saves`, jeśli jeszcze nie
   istnieje. `save()` zapisuje jeden wiersz o `id` równym 1 poleceniem `INSERT OR REPLACE`. `load()`
   zwraca `None`, gdy wiersza nie ma, i zgłasza `ValueError` przy niezgodnej wersji schematu.
4. Zaimplementuj `SqliteCombatLogRepository`. Metoda `__init__` tworzy tabelę `combat_log`,
   `append()` dopisuje wiersz poleceniem `INSERT`, a `read_all()` czyta wiersze w kolejności `id` i
   zamienia je na `CombatLogRow`.
5. Uruchom `task.py`.

Schematy obu tabel podają instrukcja i docstringi klas. Moduł `sqlite3` należy do biblioteki
standardowej Pythona, więc nie trzeba niczego instalować.

**Rezultat:** uruchomiony `task.py` wypisuje dla obu sposobów przechowywania te same wiersze: zapis i
odczyt bohatera o imieniu Ada („gold=50, wins=1”) oraz „Logged 2 combat rows. Final result: win”. W
katalogu projektu powstają pliki `save_game.json` i `combat_log.csv` oraz baza `saves.db` z tabelami
`saves` i `combat_log`. Przy kolejnym uruchomieniu zapis bohatera jest zastępowany, a oba dzienniki
zachowują wcześniejsze wiersze, więc wypisują „Logged 4 combat rows”. Zanim uzupełnisz kod, `task.py`
kończy się błędem `NotImplementedError`, bez przypomnienia takiego jak w misjach.

**Sprawdź się:**
`uv run python level_3_validation_and_persistence/projects/03_sqlite_repository_backend/check.py`.
Skrypt pracuje na nowych plikach w katalogu tymczasowym i sprawdza:

- że `rpg/domain.py` nie importuje Pydantic;
- `SqliteSaveRepository`: na nowej bazie `load()` zwraca `None`; po zapisie zwraca bohatera z
  poprawnym imieniem i złotem; po zmianie `schema_ver` w tabeli na 99 zgłasza `ValueError`;
- przeniesiony `JsonSaveRepository`: wynik `None` przed zapisem, po zapisie imię, złoto, liczbę
  zwycięstw i klasę bohatera, a przy `schema_version` równym 99 `ValueError`;
- `SqliteCombatLogRepository`: na nowej bazie pustą listę, a po dwóch zapisach dwa wiersze
  `CombatLogRow`, z których drugi ma wynik `win`;
- przeniesiony `CsvCombatLogRepository`: pustą listę, a po dwóch zapisach dwa wiersze, pierwszy z
  `damage_dealt` równym 20, drugi z wynikiem `win`.

Nie sprawdza pozostałych pól bohatera i wierszy dziennika odczytanych z SQLite, na przykład `wins`
albo `damage_dealt`. Nie sprawdza zastępowania zapisu: zwykłe `INSERT` zamiast `INSERT OR REPLACE`
przechodzi sprawdzenie, a `task.py` kończy się wtedy błędem przy drugim zapisie bohatera. Nie
sprawdza też, czy dziennik naprawdę trafia do bazy: dziennik trzymany tylko w pamięci obiektu
przechodzi sprawdzenie, a różnicę widać dopiero przy drugim uruchomieniu `task.py` (2 wiersze
zamiast 4). Nie uruchamia `task.py` i nie sprawdza zadania pobocznego. Te elementy porównaj
samodzielnie z instrukcją.

## Oczekiwane rezultaty

- `check.py` misji 06 i 07 oraz projektu SQLite Repository Backend kończy się komunikatem o
  ukończeniu.
- Pliki `task.py` misji 06 i 07 uruchamiają się bez błędów i wypisują wyniki opisane przy zadaniach;
  w misji 07 zmienna `RPG_SAVES_DIR` zmienia wypisany katalog `saves_dir`.
- W projekcie `task.py` daje te same wyniki dla zapisu JSON i dziennika CSV oraz dla SQLite, a przy
  drugim uruchomieniu oba dzienniki mają cztery wiersze.

## Wskazówki

- Misje 06 i 07 mają własne pliki. W projekcie wykorzystujesz własny kod z misji 05 i 06, ale
  przenosisz go do pakietu `rpg/` ręcznie.
- Dzienniki tylko przyrastają: misja 06 dopisuje wiersze do `logs/combat_log.csv`, a projekt do
  `combat_log.csv` i tabeli `combat_log` w `saves.db`. Po usunięciu tych plików `task.py` zaczyna
  od pustego dziennika i nowej bazy. Plik `saves.db`, w odróżnieniu od `save_game.json` i
  `combat_log.csv`, nie jest wymieniony w `.gitignore` repozytorium.
- Części „Break it on purpose” i „Fix it” każą utworzyć wiersz dziennika z akcją `run` albo ujemnymi
  obrażeniami (misja 06), ustawić `RPG_MAX_POTIONS=abc` (misja 07) albo zmienić `schema_ver` w bazie
  `saves.db` na 99 przeglądarką SQLite lub narzędziem `sqlite3` (projekt). Za każdym razem walidacja
  ma zgłosić błąd, zanim złe dane trafią do gry.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`.
  Jeśli nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym
  zestawie kieruj się kolejnością zadań powyżej.
- Po poziomie 3 mapa kursu umieszcza etap Data Recall Checkpoint, opisany w
  [zestawie 4](data-recall-checkpoint.md).
