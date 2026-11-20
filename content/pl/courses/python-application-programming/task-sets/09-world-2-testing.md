---
title: "Testy automatyczne i pokrycie kodu"
summary: "Drugi etap poziomu 5 kursu Python RPG Questbook (World 2: Testing): trzy misje o testach pytest z fixture i parametryzacją oraz o pomiarze pokrycia kodu, a także projekt Combat Regression Suite, który zamyka ten etap."
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
tasks:
  misja-04:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/04_pytest_fixtures/README.md
        lang: en
        label: "Instrukcja: Mission 04 — pytest Fixtures"
  misja-05:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/05_pytest_parametrize/README.md
        lang: en
        label: "Instrukcja: Mission 05 — pytest Parametrize"
  misja-06:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/06_coverage/README.md
        lang: en
        label: "Instrukcja: Mission 06 — Coverage"
  combat-regression-suite:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/projects/02_combat_regression_suite/README.md
        lang: en
        label: "Instrukcja: Project 02 — Combat Regression Suite"
---
Ten zestaw obejmuje drugi etap poziomu 5 kursu Python RPG Questbook, „World 2: Testing”. Piszesz
automatyczne testy biblioteką pytest dla funkcji walki: dane testowe w fixture, wiele przypadków
jednym testem dzięki parametryzacji i pomiar, które wiersze kodu testy naprawdę wykonują. Pierwsze
trzy zadania to misje 04–06. Czwarte to projekt Combat Regression Suite, który mapa kursu nazywa
punktem kontrolnym („Checkpoint”) i umieszcza na końcu tego etapu. Instrukcje, kod, pliki
konfiguracji i komunikaty skryptów sprawdzających są po angielsku. Ta strona streszcza je po polsku
i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium i narzędzia poziomu 5 opisuje część
[„Przygotowanie do zestawu”](world-1-static-analysis.md#przygotowanie-do-zestawu) zestawu 8.
pytest i pytest-cov instaluje polecenie `uv sync`. Instrukcja misji 06 i komunikat jej skryptu
podają polecenie `uv add --dev pytest-cov`, ale pakiet jest już zainstalowany.

**Co wynosisz z wcześniejszych zestawów.** Ten etap nie korzysta z plików ani wyników zestawu 8.
Każda misja ma własny, taki sam plik `rpg.py` z uproszczonymi klasami `Hero` i `Monster` oraz
funkcjami `compute_damage()` i `simulate_turn()`. Testujesz ten kod. Instrukcja misji 04 każe go
nie edytować, poza próbą z części „Break It”. Projekt ma inny moduł walki, z klasą `Fighter`.
Przyda się znajomość klas danych (`@dataclass`) z poziomu 2, bo z nich zbudowane są postacie gry.

**Pliki.** Misja 04 ma do uzupełnienia `conftest.py` i `test_combat.py`. Misja 05 ma gotowe
fixture w `conftest.py` i testy z misji 04 w `test_combat.py`, z dwoma komentarzami `TODO`. Misja
06 ma gotowy zestaw testów, odziedziczony po misjach 04 i 05, oraz własny `pyproject.toml`. Projekt
ma własny pakiet `rpg/` i katalog `tests/`. Kodu nie przenosisz między zadaniami.

**Polecenia.** Wszystkie polecenia zestawu wpisujesz w katalogu głównym repozytorium. Instrukcje
misji 04 i 05 podają polecenie `pytest` bez `uv run`, do wpisania w katalogu misji. Takie
polecenie działa tylko w aktywnym środowisku `.venv`. Z `uv run` działa w katalogach misji 04 i 05,
ale nie w katalogu misji 06. Ten katalog ma własny `pyproject.toml`, tak jak katalogi misji 01–03,
co opisuje część „Polecenia i katalog roboczy” w
[przygotowaniu do zestawu 8](world-1-static-analysis.md#przygotowanie-do-zestawu). Polecenia pytest
na tej stronie podają ścieżkę do katalogu albo pliku testów zadania, więc uruchamiają tylko jego
testy.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypty tego zestawu uruchamiają Twoje testy w katalogu zadania.
Potem celowo psują po jednym zachowaniu w kodzie gry, w `rpg.py` albo w `rpg/combat.py`, i
sprawdzają, czy Twoje testy to wykrywają. Po każdej próbie przywracają oryginalny plik. Gdy wszystko
się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się nie
zgadza, wypisuje, czego oczekiwał, na przykład które zepsute zachowanie przeszło niezauważone.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy porównujesz z instrukcją samodzielnie. Części instrukcji „Break
It”, „Fix It”, „Try It Yourself” i „Side Quest” oraz lista „Checklist” służą samodzielnej pracy i
`check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` bez ścieżki, czyli dla całego repozytorium. Pliki startowe są celowo
niekompletne, więc zobaczysz błędy. Według opisu kursu to polecenie jest narzędziem autora kursu,
nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki
konfiguracji i komunikaty skryptów `check.py`.

## Zadania

### pytest Fixtures: dane testowe w conftest.py {#misja-04}

**Cel:** napisać w `conftest.py` trzy fixture, czyli funkcje przygotowujące dane testowe, i w
`test_combat.py` sześć testów funkcji walki z `rpg.py`.

**Zakres pracy:** w `level_5_maintainability/missions/04_pytest_fixtures/` jest `rpg.py`, którego
instrukcja każe nie edytować, oraz `conftest.py` i `test_combat.py` z zakomentowanymi szkieletami i
komentarzami `TODO`. Według kroków instrukcji:

1. W `conftest.py` uzupełnij fixture `warrior` (bohater klasy warrior), `goblin` (potwór) i
   `make_hero`. Fixture `make_hero` zwraca funkcję, która tworzy bohatera z podanymi statystykami.
2. W `test_combat.py` uzupełnij sześć testów: dwa dla `compute_damage()` (zwykłe trafienie i
   minimalne obrażenia), otrzymanie obrażeń przez `warrior`, leczenie miksturą, brak mikstur przy
   bohaterze z `make_hero(potions=0)` i wygraną bohatera w `simulate_turn()`. Oczekiwane wartości
   podaje instrukcja.

```bash
uv run pytest level_5_maintainability/missions/04_pytest_fixtures -v
uv run pytest level_5_maintainability/missions/04_pytest_fixtures/test_combat.py::test_compute_damage_normal_hit -v
```

Drugie polecenie uruchamia jeden test, jak w części „Try It Yourself”.

**Rezultat:** dopóki testy są zakomentowane, pytest wypisuje „no tests ran”. Po uzupełnieniu
wypisuje sześć testów ze statusem PASSED. Część „Break It” każe usunąć z `compute_damage()` w
`rpg.py` dolną granicę obrażeń. Niektóre testy przestają wtedy przechodzić. Potem przywracasz
oryginalny wzór. Część „Fix It” przypomina, że przy błędzie poprawiasz test albo fixture, a nie
`rpg.py`.

**Sprawdź się:** `uv run python level_5_maintainability/missions/04_pytest_fixtures/check.py`.
Skrypt sprawdza:

- że `conftest.py` ma co najmniej trzy niezakomentowane `@pytest.fixture` i funkcje `warrior`,
  `goblin` i `make_hero`;
- że `test_combat.py` ma co najmniej pięć funkcji `test_` i że któryś test wywołuje `make_hero(…)`;
- że testy przechodzą z oryginalnym `rpg.py`;
- że testy nie przechodzą po każdej z sześciu zmian w `rpg.py`: bez dolnej granicy obrażeń, z
  odwrotnym znakiem rzutu kością, z `take_damage()` ignorującym obrażenia, z miksturą, która nie
  leczy, z wyłączonym sprawdzeniem braku mikstur i z atakiem bohatera bez obrażeń w
  `simulate_turn()`.

Sześć zmian obejmuje zachowania z kroku 2 instrukcji. Skrypt nie sprawdza nazw testów ani tego, czy
testy korzystają z fixture `warrior` i `goblin`. Wymaga tylko, by fixture istniały.

### pytest Parametrize: wiele przypadków w jednym teście {#misja-05}

**Cel:** zastąpić prawie identyczne testy jednym testem z dekoratorem `@pytest.mark.parametrize`
i czytelnymi nazwami przypadków.

**Zakres pracy:** w `level_5_maintainability/missions/05_pytest_parametrize/` jest `rpg.py`,
gotowy `conftest.py` z fixture z misji 04 i `test_combat.py` z czterema zwykłymi testami oraz
dwoma komentarzami `TODO`. Według instrukcji:

1. TODO 1: test `compute_damage()` z trzema przypadkami i nazwami w `ids=`. Instrukcja podaje
   gotowy kod do odkomentowania.
2. TODO 2: test `simulate_turn()` z co najmniej trzema przypadkami i `ids=`: wygrana bohatera,
   przegrana bohatera i sytuacja, w której obie strony przeżywają. Instrukcja podpowiada, jak
   dobrać statystyki do każdego wyniku.

```bash
uv run pytest level_5_maintainability/missions/05_pytest_parametrize -v
```

**Rezultat:** na starcie pytest uruchamia cztery testy. Po uzupełnieniu jest co najmniej osiem
przypadków, a przypadki z parametryzacji mają w nazwie identyfikator z `ids=`, na przykład
`test_compute_damage_parametrized[normal]`. Część „Break It” każe zmienić jedną oczekiwaną wartość.
Komunikat o błędzie zawiera wtedy identyfikator przypadku. Część „Fix It” przywraca wartość.

**Sprawdź się:** `uv run python level_5_maintainability/missions/05_pytest_parametrize/check.py`.
Skrypt sprawdza:

- że `test_combat.py` ma co najmniej dwa niezakomentowane `@pytest.mark.parametrize` i `ids=` w
  co najmniej jednym niezakomentowanym wierszu;
- że każdy test z parametryzacją używa w treści któregoś ze swoich parametrów;
- że testy przechodzą z oryginalnym `rpg.py`, a pytest pokazuje co najmniej osiem przypadków ze
  statusem PASSED;
- że testy nie przechodzą po każdej z czterech zmian w `rpg.py`: bez dolnej granicy obrażeń, z
  odwrotnym znakiem rzutu kością, z atakiem bohatera bez obrażeń i z kontratakiem potwora bez
  obrażeń.

Zmiany nie obejmują wyniku, w którym obie strony przeżywają. W kontroli przechodził test
`simulate_turn()` bez tego przypadku. Trzy wyniki porównaj z TODO 2 w instrukcji.

### Coverage: pomiar pokrycia kodu testami {#misja-06}

**Cel:** zmierzyć, które wiersze i rozgałęzienia `rpg.py` wykonują testy, znaleźć jedyną lukę
pozostawioną przez odziedziczone testy i zamknąć ją testem, który sprawdza wynik, a nie tylko
wykonuje brakujący kod.

**Zakres pracy:** w `level_5_maintainability/missions/06_coverage/` są `rpg.py`, `conftest.py`,
`test_combat.py` z testami z misji 04 i 05 oraz `pyproject.toml` z konfiguracją ruffa, sekcją
`[tool.pytest.ini_options]` z `pythonpath = ["."]` i komentarzem `TODO`. Według kroków
instrukcji:

1. W `pyproject.toml` dodaj sekcję `[tool.coverage.run]` (`source`, `omit`, `branch = true`) i
   sekcję `[tool.coverage.report]` (`fail_under = 100`, `show_missing = true`), z wartościami z
   instrukcji.
2. Zmierz pokrycie i odczytaj w kolumnie „Missing” wiersz, którego żaden test nie wykonuje.
3. Napisz test dla wyniku `simulate_turn()`, w którym obie strony przeżywają, z asercjami dla obu
   zwracanych wartości.

```bash
uv run pytest level_5_maintainability/missions/06_coverage --cov=rpg --cov-branch --cov-config=level_5_maintainability/missions/06_coverage/pyproject.toml --cov-report=term-missing
```

Opcja `--cov-config` wskazuje `pyproject.toml` misji. Bez niej pytest-cov uruchomiony z katalogu
głównego szuka konfiguracji w katalogu głównym i pomija sekcje `[tool.coverage]` misji, w tym próg
`fail_under = 100`. Skrypt uruchamia pytest w katalogu misji, gdzie ta konfiguracja jest odczytywana
bez tej opcji. W kontroli wyniki z tą opcją i ze skryptu były takie same. Opcję `--cov-branch`
instrukcja każe podawać zawsze, bo pytest-cov w tym repozytorium nie zawsze odczytuje `branch = true`
z konfiguracji.

**Rezultat:** na starcie raport pokazuje 97% z jednym brakującym wierszem, `return True, True` w
`simulate_turn()`. Instrukcja podaje 98% wierszy i 97% rozgałęzień. Po dodaniu konfiguracji
polecenie kończy się błędem „FAIL Required test coverage of 100.0% not reached”. Po dodaniu testu
raport pokazuje 100% i „Required test coverage of 100.0% reached”. Część „Break It” każe usunąć
`branch = true`. `check.py` wypisuje wtedy „❌ [tool.coverage.run] must set branch = true”. Część
„Fix It” przywraca ten wiersz.

**Sprawdź się:** `uv run python level_5_maintainability/missions/06_coverage/check.py`. Skrypt
sprawdza:

- że `pyproject.toml` ma sekcję `[tool.coverage`, a sekcja `[tool.coverage.run]` zawiera słowa
  `branch` i `true`;
- że testy przechodzą;
- że pokrycie `rpg.py` z `--cov-branch` wynosi 100%;
- że testy nie przechodzą po zmianie w `rpg.py`, która odwraca wynik „obie strony przeżywają”.
  Test, który tylko wywołuje `simulate_turn()` bez asercji, daje 100%, ale tej próby nie przejdzie.

Nie sprawdza sekcji `[tool.coverage.report]` ani progu `fail_under = 100`. W kontroli przechodziła
konfiguracja bez tej sekcji. Próg sprawdzasz poleceniem wyżej: z sekcją z instrukcji kończy się
błędem, dopóki pokrycie jest niższe niż 100%.

### Combat Regression Suite: testy, które znajdują błąd {#combat-regression-suite}

Mapa kursu nazywa ten projekt punktem kontrolnym („Checkpoint”) i umieszcza go na końcu etapu
World 2. Instrukcja wymaga ukończenia misji 04–06.

**Cel:** napisać zestaw testów pytest dla `rpg/combat.py`, działającego modułu walki z jednym
ukrytym błędem. Testy mają objąć zwykłe zachowanie z fixture i parametryzacją, znaleźć błąd w
`compute_damage()` i udokumentować go dekoratorem `@pytest.mark.xfail(strict=True)`. Błędu nie
poprawiasz: instrukcja mówi, że testy ujawniają błędy, a `xfail` dokumentuje znane problemy.

**Zakres pracy:** w `level_5_maintainability/projects/02_combat_regression_suite/` jest pakiet
`rpg/` z `combat.py`, którego nie zmieniasz, i `tests/test_combat.py`, w którym piszesz testy.
Tabela wymagań w instrukcji:

- `pytest tests/test_combat.py` kończy się kodem 0 (test `xfail` liczy się jako przechodzący);
- pokrycie `rpg/combat.py` wynosi co najmniej 85%;
- co najmniej jedno `@pytest.mark.parametrize` i jedno `@pytest.fixture`;
- co najmniej jeden test z `@pytest.mark.xfail(strict=True)`, który wywołuje `compute_damage()`.

Instrukcja opisuje błąd: `compute_damage(atk=1, bonus=0, def_=10)` zwraca 0, a minimalne obrażenia
to 1. Opis na początku `tests/test_combat.py` podaje inne wymagania: co najmniej dwa fixture, trzy
parametryzacje i `xfail` bez `strict`. Skrypt sprawdza wymagania z tabeli w instrukcji.

```bash
uv run pytest level_5_maintainability/projects/02_combat_regression_suite/tests/test_combat.py -v
uv run pytest level_5_maintainability/projects/02_combat_regression_suite/tests/test_combat.py --cov=rpg --cov-report=term-missing
```

Instrukcja każe uruchamiać `check.py` w katalogu projektu. Ten katalog nie ma własnego
`pyproject.toml`, więc to polecenie też działa. W kontroli polecenia pytest z katalogu głównego
testowały pakiet `rpg/` tego projektu, a nie pakiet `rpg` z poziomu 4.

**Rezultat:** na starcie plik testów nie ma testów, więc pytest wypisuje „no tests ran”. Po
napisaniu testy przechodzą, a test dokumentujący błąd ma status XFAIL. Raport pokrycia pokazuje
`rpg/combat.py` z procentem i brakującymi wierszami.

**Sprawdź się:**
`uv run python level_5_maintainability/projects/02_combat_regression_suite/check.py`. Skrypt
sprawdza:

- że `tests/test_combat.py` istnieje, a pytest kończy się kodem 0;
- że pokrycie `rpg/combat.py` wynosi co najmniej 85%;
- że co najmniej jeden dekorator zawiera `parametrize`, a co najmniej jeden `fixture`;
- że któryś test z dekoratorem `xfail` wywołuje `compute_damage()`, a w pliku jest napis
  `strict=True`;
- że po chwilowej poprawce błędu w `rpg/combat.py` test `xfail` zmienia status na XPASS i cały
  zestaw nie przechodzi. Oznacza to, że test sprawdza prawdziwy błąd, a nie dowolną błędną
  wartość. Potem skrypt przywraca plik.

Nie sprawdza asercji w pozostałych testach. W kontroli przechodziły testy, które tylko wywoływały
funkcje bez asercji, bo dawały wymagane pokrycie. Skrypt zakłada, że `rpg/combat.py` jest
niezmieniony, zgodnie z instrukcją.

## Oczekiwane rezultaty

- `check.py` misji 04–06 i projektu Combat Regression Suite kończy się komunikatem o ukończeniu.
- Testy misji 04 i 05 przechodzą z `rpg.py` i nie przechodzą, gdy zachowania z instrukcji się
  zmienią. Misja 06 ma 100% pokrycia rozgałęzień z testem, który sprawdza wynik.
- Testy projektu przechodzą, mają co najmniej 85% pokrycia, a znany błąd jest opisany testem
  `xfail(strict=True)`.

## Wskazówki

- pytest i pytest-cov zapisują pliki pomocnicze `.pytest_cache/`, `__pycache__/` i `.coverage` w
  katalogu głównym albo w katalogu zadania. Wszystkie są w `.gitignore` repozytorium.
- Wpis `pythonpath = ["."]` z `pyproject.toml` misji 06 przyda się w projekcie Full Release
  Pipeline z [zestawu 10](world-3-ci-cd-and-polish.md#full-release-pipeline).
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. Jeśli
  nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań na tej stronie.
- Ostatni etap poziomu 5 opisuje [zestaw 10](world-3-ci-cd-and-polish.md).
