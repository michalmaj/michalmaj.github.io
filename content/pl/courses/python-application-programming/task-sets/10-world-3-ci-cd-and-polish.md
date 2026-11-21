---
title: "Obsługa błędów, pre-commit i CI"
summary: "Trzeci etap poziomu 5 kursu Python RPG Questbook (World 3: CI/CD and Polish): trzy misje o własnej hierarchii wyjątków, hookach pre-commit i workflow GitHub Actions oraz projekt Full Release Pipeline, który zamyka ten etap i cały poziom 5."
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
  misja-07:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/07_error_handling/README.md
        lang: en
        label: "Instrukcja: Mission 07 — Error Handling"
  misja-08:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/08_pre_commit/README.md
        lang: en
        label: "Instrukcja: Mission 08 — Pre-commit Hooks"
  misja-09:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/missions/09_github_actions_ci/README.md
        lang: en
        label: "Instrukcja: Mission 09 — GitHub Actions CI"
  full-release-pipeline:
    materials:
      - repository: python-rpg-questbook
        path: level_5_maintainability/projects/03_full_release_pipeline/README.md
        lang: en
        label: "Instrukcja: Boss Fight — Full Release Pipeline"
---
Ten zestaw obejmuje trzeci, ostatni etap poziomu 5 kursu Python RPG Questbook, „World 3: CI/CD and
Polish”. Najpierw zastępujesz ciche połykanie błędów własną hierarchią wyjątków. Potem ustawiasz
hooki pre-commit, które sprawdzają kod przed każdym commitem, i workflow GitHub Actions, który ma
sprawdzać go po wysłaniu na GitHub. Na końcu przeprowadzasz kod startowy gry przez wszystkie
narzędzia poziomu 5. Pierwsze trzy zadania to misje 07–09. Czwarte to projekt Full Release
Pipeline, który mapa kursu nazywa walką z bossem („Boss Fight”) i umieszcza na końcu poziomu 5.
Instrukcje, kod, pliki konfiguracji i komunikaty skryptów sprawdzających są po angielsku. Ta strona
streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium i narzędzia poziomu 5 opisuje część
[„Przygotowanie do zestawu”](world-1-static-analysis.md#przygotowanie-do-zestawu) zestawu 8. Tam
jest też wyjaśnienie, dlaczego polecenia `uv run` nie działają w katalogach z własnym
`pyproject.toml`, i informacja o pyright i Node.js.

**Co wynosisz z wcześniejszych zestawów.** Misje mają własne pliki. `task.py` misji 07 to gra z
adnotacjami typów, która przechodzi `mypy --strict`. Korzysta z logów z
[zestawu 6](world-2-logging-and-observability.md) i poleceń Typera z
[zestawu 5](world-1-command-line-interface.md). `task.py` misji 08 i 09 ma już gotową hierarchię
wyjątków, wynik misji 07. Misja 08 używa ruffa i mypy z [zestawu 8](world-1-static-analysis.md), a
misja 09 dodatkowo pytest z [zestawu 9](world-2-testing.md). Projekt zaczyna od kodu startowego
poziomu: jego `rpg.py` to ten sam plik co `starter_unqualified_rpg/main.py`. Projekt stosuje na tym
kodzie narzędzia z całego poziomu 5. Konfigurację, testy, hooki i workflow piszesz od nowa, w
katalogu projektu, według misji z zestawów 8–10. Projekt nie importuje plików misji.

**Polecenia.** Wszystkie polecenia zestawu wpisujesz w katalogu głównym repozytorium. Katalogi misji
07–09 nie mają własnego `pyproject.toml`, więc polecenia z instrukcji działają też w nich. Projekt
tworzy w kroku 1 własny `pyproject.toml` bez sekcji `[project]`. Od tej chwili polecenia `uv run` z
jego instrukcji nie działają w katalogu projektu, tak jak w misjach 01–03 z zestawu 8. Polecenia
projektu na tej stronie są więc podane dla katalogu głównego.

**Kroki na GitHubie.** Misja 09 i projekt kończą się krokami na GitHubie: wysłaniem zmian
(`git push`), pull requestem, uruchomieniem workflow w GitHub Actions i, w projekcie, tagiem
`v1.0.0`. Skrypty `check.py` tych kroków nie sprawdzają, bo czytają tylko pliki lokalnie. Kroki te
wymagają własnego repozytorium na GitHubie. W klonie kursu `origin` wskazuje repozytorium kursu,
więc nie wysyłaj tam zmian ani tagów. Kurs nie opisuje, jak przygotować własne repozytorium do tych
kroków, i ta strona też tego nie robi. Przy obu zadaniach opisano, co sprawdzono lokalnie, a czego
nie.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypt misji 07 wczytuje `task.py` jako moduł i wywołuje jego
funkcje w sytuacjach błędów w katalogu tymczasowym: przy braku pliku, uszkodzonym JSON i
nieudanym zapisie. Skrypt misji 08 uruchamia hooki pre-commit dla `task.py`. Skrypty misji 09 i
projektu czytają pliki konfiguracji jako tekst i uruchamiają narzędzia lokalnie. Gdy wszystko się
zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się nie zgadza,
wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy porównujesz z instrukcją samodzielnie. Części instrukcji „Break
It”, „Fix It”, „Try It Yourself” i „Side Quest” oraz lista „Checklist” służą samodzielnej pracy i
`check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### Error Handling: własna hierarchia wyjątków {#misja-07}

**Cel:** zastąpić ciche `except Exception:` własną hierarchią wyjątków, która mówi, co poszło nie
tak i dlaczego. Wyjątki dziedziczą po `RPGError`, a nowe wyjątki mają wskazywać pierwotną
przyczynę (`raise … from e`). Błąd przechwytuje dopiero warstwa poleceń.

**Zakres pracy:** w `level_5_maintainability/missions/07_error_handling/` są `task.py` i katalog
`data/` z `monsters.json` i `hero_classes.json`. Komentarze w `task.py` oznaczają problemy Smell
A–D. Według kroków instrukcji:

1. Zdefiniuj `RPGError` i co najmniej dwie klasy pochodne, `MonsterLoadError` i `SaveFileError`.
   `CombatError` jest opcjonalny.
2. Smell A: `load_monsters()` przy braku pliku i niepoprawnym JSON zgłasza `MonsterLoadError`
   powiązany z pierwotnym wyjątkiem. Polecenie `simulate` przechwytuje ten wyjątek zamiast
   sprawdzać pustą listę.
3. Smell B: `load_hero()` zwraca `None`, gdy zapisu nie ma, a zgłasza `SaveFileError`, gdy zapis
   jest uszkodzony.
4. Smell C: `save_hero()` przy błędzie zapisu zapisuje błąd w logu i zgłasza `SaveFileError`,
   zamiast wypisywać surowy komunikat.
5. Krok 4b, dodatkowy: Smell D w `load_hero_classes()`.

```bash
uv run python level_5_maintainability/missions/07_error_handling/task.py new-game --name Ada --class warrior
uv run python level_5_maintainability/missions/07_error_handling/task.py simulate
```

**Rezultat:** część „Break It” każe usunąć `data/monsters.json` i uruchomić `simulate`. Polecenie
najpierw wczytuje bohatera. Bez zapisu kończy się komunikatem „No save found. Run new-game first.”,
zanim dojdzie do potworów. Opisany efekt widać więc dopiero po utworzeniu bohatera poleceniem
`new-game`. Przed poprawką `simulate` wypisuje wtedy „No monsters found in data/.”. Po poprawce
wypisuje komunikat z `MonsterLoadError` ze ścieżką do katalogu `data/`. Tracebacku nie ma, bo
skrypt wymaga, by `simulate` przechwycił błąd. Instrukcja mówi, że zobaczysz `MonsterLoadError`:
widać jego komunikat, nie wyjątek. Część „Fix It” przywraca plik kopią z
`starter_unqualified_rpg/data/`. Oba pliki są identyczne. `simulate` zapisuje bohatera w `saves/`,
a raporty w `reports/` katalogu misji. Raportów nie ma w `.gitignore` repozytorium.

**Sprawdź się:** `uv run python level_5_maintainability/missions/07_error_handling/check.py`.
Skrypt sprawdza:

- że w `task.py` jest `RPGError`, klasa pochodna `Exception`, i co najmniej dwie klasy pochodne
  `RPGError`;
- w katalogu tymczasowym, że `load_monsters()` przy braku katalogu danych i przy uszkodzonym JSON
  zgłasza wyjątek z hierarchii z ustawioną przyczyną (`__cause__`);
- że `load_hero()` bez zapisu zwraca `None`, a przy uszkodzonym zapisie zgłasza wyjątek z
  hierarchii z przyczyną;
- że `save_hero()` przy zapisie, który zgłasza `OSError`, zgłasza wyjątek z hierarchii z przyczyną
  `OSError` i nie wypisuje surowego komunikatu;
- że `simulate --battles 1` przy braku danych kończy się kodem różnym od 0, bez nieprzechwyconego
  wyjątku i bez tracebacku;
- że w `task.py` nie ma `except:`.

Nie sprawdza zapisu błędu w logu przy nieudanym zapisie (`logger.error` z kroku 4 instrukcji). W
kontroli przechodziła wersja bez niego. Nie sprawdza też kroku 4b ani treści komunikatu
`simulate`. Sprawdza tylko kod wyjścia i brak tracebacku. Te elementy porównaj z instrukcją,
uruchamiając polecenia wyżej.

### pre-commit: hooki sprawdzające kod przed commitem {#misja-08}

**Cel:** ustawić hooki pre-commit dla ruffa i mypy, które sprawdzają styl i typy przed commitem, i
uruchomić je dla `task.py` misji.

**Zakres pracy:** w `level_5_maintainability/missions/08_pre_commit/` jest `task.py` z hierarchią
wyjątków z misji 07. W tym katalogu utwórz plik `.pre-commit-config.yaml` z hookami `ruff` i
`ruff-format` z repozytorium `ruff-pre-commit` oraz `mypy` z repozytorium `mirrors-mypy`. Każde
repozytorium hooków ma mieć przypiętą wersję `rev:`, a hook mypy ma mieć `additional_dependencies`
z pakietami `pydantic`, `typer` i `rich`. Instrukcja podaje cały przykład. Instrukcja każe
zainstalować pre-commit poza repozytorium poleceniem `uv tool install pre-commit`. pre-commit jest
też w grupie `dev` kursu, więc po `uv sync` działa polecenie `uv run pre-commit`, a `check.py`
uruchomiony przez `uv run` korzysta z tej instalacji. pre-commit działa tylko w repozytorium git.
Klon z przygotowania do zestawu 1 nim jest.

```bash
uv run pre-commit run --files level_5_maintainability/missions/08_pre_commit/task.py --config level_5_maintainability/missions/08_pre_commit/.pre-commit-config.yaml
```

Nie używaj `--all-files`, choć podpowiada to komentarz na początku `task.py`. Ta opcja uruchamia
hooki na wszystkich plikach repozytorium kursu, a hooki `ruff` z `--fix` i `ruff-format` zmieniają
pliki. W kontroli jedno takie uruchomienie zmieniło 258 plików na wszystkich poziomach kursu.
Instrukcja słusznie każe używać `--files`. Kroki instrukcji uruchamiają hooki ręcznie i nie
instalują ich w repozytorium. Instalację hooka obejmuje projekt Full Release Pipeline.

**Rezultat:** pierwsze uruchomienie pobiera hooki z internetu i instaluje dla nich osobne
środowiska. Trwa to kilka minut. Za pierwszym razem hook `ruff-format` przeformatowuje jedno
wywołanie w `task.py`, łącząc je w jeden wiersz. Wypisuje wtedy „files were modified by this hook”
i kończy się wynikiem Failed. Drugie uruchomienie przechodzi i przy wszystkich trzech hookach
wypisuje „Passed”. Tak było w kontroli z wersjami hooków z instrukcji i z nowszymi. To samo dotyczy
pierwszego uruchomienia `check.py`.

Pierwsze uruchomienie hooków może zakończyć się wynikiem `Failed`, ponieważ `ruff-format` zmienia
formatowanie pliku `task.py`. Nie oznacza to samo w sobie błędu implementacji. Przejrzyj zmianę
poleceniem `git diff level_5_maintainability/missions/08_pre_commit/task.py`, a następnie uruchom
hooki ponownie.

Część „Break It” każe zmienić typ wyniku `compute_damage()` na `str`. Hook mypy zgłasza wtedy
niezgodność typów. Część „Fix It” cofa zmianę.

**Sprawdź się:** `uv run python level_5_maintainability/missions/08_pre_commit/check.py`. Skrypt
sprawdza:

- że w katalogu misji jest `.pre-commit-config.yaml` z napisami `repos:`, `ruff`, `ruff-format`,
  `mypy` i `rev:`;
- że `pre-commit run --files task.py` z tą konfiguracją, uruchomione w katalogu misji, kończy się
  kodem 0.

Nie sprawdza `additional_dependencies`: w kontroli hooki przechodziły także bez nich. Listę
pakietów porównaj z krokiem 2 instrukcji.

### GitHub Actions CI: workflow dla każdego wysłania zmian {#misja-09}

**Cel:** utworzyć plik `.github/workflows/ci.yml`, czyli workflow GitHub Actions, który przy każdym
wysłaniu zmian i pull requeście uruchamia ruff, mypy i pytest w Pythonie 3.12 i 3.13.

**Zakres pracy:** w `level_5_maintainability/missions/09_github_actions_ci/` jest gotowy `task.py`,
który przechodzi ruff i `mypy --strict` od początku. W katalogu misji utwórz katalog
`.github/workflows/` i w nim plik `ci.yml` według instrukcji, która podaje cały workflow. Plik ma
zawierać:

- wyzwalacze `push` i `pull_request`;
- sekcję `jobs:`;
- instalację uv akcją `astral-sh/setup-uv`;
- kroki ruff, mypy i pytest, w tej kolejności;
- macierz z wersjami `"3.12"` i `"3.13"`.

**Rezultat:** `check.py` przechodzi z workflow z instrukcji. Część „Break It” każe przestawić
pytest przed mypy. `check.py` wypisuje wtedy „❌ Step order must be: ruff → mypy → pytest”, a nie
komunikat cytowany w instrukcji. Część „Fix It” przywraca kolejność.

**Co sprawdzono lokalnie, a czego nie.** `check.py` czyta `ci.yml` jako tekst i uruchamia lokalnie
ruff i mypy na `task.py`. Workflow nie uruchamia. Krok 4 instrukcji, czyli skopiowanie pliku do
własnego repozytorium i wysłanie go na GitHub, wymaga własnego repozytorium. GitHub uruchamia tylko
workflow z katalogu `.github/workflows/` w katalogu głównym repozytorium. Kurs nie opisuje, jak
przygotować takie repozytorium. Przy przygotowaniu tej strony workflow nie był uruchamiany na
GitHubie. Wynik lokalnej próby tych samych poleceń workflow opisuje projekt
[Full Release Pipeline](#full-release-pipeline).

**Sprawdź się:**
`uv run python level_5_maintainability/missions/09_github_actions_ci/check.py`. Skrypt sprawdza:

- że w katalogu misji jest `.github/workflows/ci.yml` z napisami `on:`, `jobs:`, `uv`, `ruff`,
  `mypy`, `pytest`, `3.12` i `3.13`;
- że pierwsze wiersze `run:` z ruff, mypy i pytest występują w tej kolejności;
- że ruff i `mypy --strict` przechodzą dla `task.py`.

Skrypt nie odczytuje pliku jako YAML. W kontroli przechodził plik z niepoprawnymi wcięciami, z
wyzwalaczem bez `push` i `pull_request` oraz bez macierzy, z wersjami Pythona tylko w komentarzu.
`task.py` przechodzi ruff i mypy od początku, więc wynik skryptu zależy w praktyce tylko od tekstu
`ci.yml`. Plik porównaj z listą „Checklist” instrukcji.

### Full Release Pipeline: wszystkie narzędzia poziomu 5 {#full-release-pipeline}

Mapa kursu nazywa ten projekt walką z bossem („Boss Fight”) i umieszcza go na końcu etapu World 3,
czyli na końcu poziomu 5. Opis poziomu przedstawia go jako połączenie wszystkich dziewięciu
narzędzi. Instrukcja projektu nie podaje wymagań wstępnych i każe wykonywać kroki po kolei.

**Cel:** przeprowadzić kod startowy gry, `rpg.py` z sześcioma problemami jakości, przez wszystkie
narzędzia poziomu 5. Projekt obejmuje konfigurację, poprawki ruffa i mypy, testy z pokryciem,
`CHANGELOG.md`, hooki pre-commit i workflow GitHub Actions.

**Zakres pracy:** w `level_5_maintainability/projects/03_full_release_pipeline/` są `rpg.py`,
katalog `data/` i `check.py`. Według dziewięciu kroków instrukcji:

1. Utwórz `pyproject.toml` z sekcjami `[tool.ruff]` (reguły E, F, W, I i UP), `[tool.mypy]` (tryb
   strict), `[tool.pyright]`, `[tool.coverage]` (minimum 80%) i `[tool.pytest.ini_options]`.
2. Popraw naruszenia ruffa w `rpg.py`: rozdziel importy z jednego wiersza, usuń nieużywany import
   `csv`, zamień `Optional` i `List` na nowszą składnię i skróć długie wiersze.
3. Dodaj adnotacje typów wymagane przez `mypy --strict` i zamień `except:` na `except Exception:`.
4. Napisz `tests/conftest.py` i `tests/test_combat.py` dla `compute_damage`, `Hero.take_damage`,
   `Hero.use_potion`, `Monster.take_damage`, `simulate_one` i `make_hero`.
5. Sprawdź, że pokrycie `rpg.py` wynosi co najmniej 80%.
6. Utwórz `CHANGELOG.md` w formacie Keep a Changelog z sekcją `## [1.0.0]`.
7. Utwórz `.pre-commit-config.yaml` z hookami ruff, ruff-format i mypy, zainstaluj hook i uruchom
   hooki dla `rpg.py`.
8. Utwórz `.github/workflows/ci.yml` z uv, ruff, mypy i pytest w macierzy Pythona 3.12 i 3.13.
9. Uruchom `check.py`.

Lista ma dziewięć punktów, a punkt 9 mówi „All 7 steps must pass”. Przykładowy wynik w części
„Running check.py” podaje pokrycie 85%, a próg w kroku 1 i w skrypcie wynosi 80%.

Polecenia z katalogu głównego, przepisane z wywołań w `check.py`:

```bash
uv run ruff check level_5_maintainability/projects/03_full_release_pipeline/rpg.py --config level_5_maintainability/projects/03_full_release_pipeline/pyproject.toml
uv run mypy level_5_maintainability/projects/03_full_release_pipeline/rpg.py --strict --config-file level_5_maintainability/projects/03_full_release_pipeline/pyproject.toml
uv run python -m pyright level_5_maintainability/projects/03_full_release_pipeline/rpg.py --project level_5_maintainability/projects/03_full_release_pipeline
uv run pytest level_5_maintainability/projects/03_full_release_pipeline/tests --cov=rpg --cov-config=level_5_maintainability/projects/03_full_release_pipeline/pyproject.toml --cov-report=term-missing
```

Opcja `--cov-config` w ostatnim poleceniu działa tak jak w misji 06 z
[zestawu 9](world-2-testing.md#misja-06): wskazuje konfigurację pokrycia z `pyproject.toml`
projektu.

**Testy i pakiet `rpg` z poziomu 4.** Pakiet `rpg` z projektu Installable CLI Tool jest
zainstalowany w środowisku repozytorium (zobacz
[przygotowanie do zestawu 7](world-3-user-facing-output.md#przygotowanie-do-zestawu)). W kontroli
testy z katalogu `tests/` uruchomione ostatnim poleceniem wyżej znajdowały tamten pakiet zamiast
`rpg.py` tego projektu. Kończyły się wtedy błędem „cannot import name 'Hero' from 'rpg'”. Pomaga
wpis `pythonpath = ["."]` w sekcji `[tool.pytest.ini_options]`, którą krok 1 każe utworzyć w
`pyproject.toml` projektu. Ten sam wpis ma dostarczony `pyproject.toml` misji 06. Kropka oznacza
katalog, w którym leży ten `pyproject.toml`, czyli katalog projektu: pytest pokazuje go wtedy w
wierszu „rootdir”. `check.py` uruchamia pytest w katalogu projektu i znajduje `rpg.py` także bez
tego wpisu.

**Hook pre-commit (krok 7).** Instrukcja każe wpisać `uv run pre-commit install` w katalogu
projektu, gdzie `uv` po kroku 1 nie działa. Z katalogu głównego polecenie potrzebuje opcji
`--config` ze ścieżką do konfiguracji projektu:

```bash
uv run pre-commit install --config level_5_maintainability/projects/03_full_release_pipeline/.pre-commit-config.yaml
uv run pre-commit run --files level_5_maintainability/projects/03_full_release_pipeline/rpg.py --config level_5_maintainability/projects/03_full_release_pipeline/.pre-commit-config.yaml
```

Pierwsze polecenie instaluje ten sam hook co polecenie z instrukcji. Bez `--config` hook szukałby
pliku `.pre-commit-config.yaml` w katalogu głównym repozytorium, którego kurs nie ma. Każdy kolejny
commit kończyłby się wtedy błędem „No .pre-commit-config.yaml file was found”.

`pre-commit install` to nie jednorazowe uruchomienie narzędzia, tylko zmiana konfiguracji
repozytorium. Polecenie zapisuje hook w pliku `.git/hooks/pre-commit` klonu kursu. Od tej chwili
każdy `git commit` w tym klonie uruchamia hooki z konfiguracji tego projektu na zatwierdzanych
plikach Pythona, także przy pracy nad innymi poziomami. W kontroli commit pliku z poziomu 6 został
zatrzymany: `ruff-format` przeformatował cały ten plik („files were modified by this hook”), a mypy
zgłosił błędy.

Po projekcie możesz usunąć ten hook poleceniem `uv run pre-commit uninstall` w katalogu głównym.
To też zmiana konfiguracji repozytorium. Polecenie usuwa hook zainstalowany przez pre-commit. Jeśli
w klonie był wcześniej inny, własny hook `pre-commit`, polecenie `install` zachowało go jako
`.git/hooks/pre-commit.legacy`, a `uninstall` go przywraca. Hook zainstalowany wcześniej przez samo
pre-commit, na przykład z inną konfiguracją, `install` zastępuje bez kopii.

**Co sprawdzono lokalnie, a czego nie.**

- **Polecenia lokalne.** Polecenia narzędzi i pre-commit wyżej oraz `check.py` sprawdzono w
  świeżej kopii repozytorium kursu, z katalogu głównego.
- **Konfiguracja workflow.** `check.py` sprawdza tylko, czy `ci.yml` zawiera napisy `ruff`, `mypy`,
  `pytest`, `uv`, `3.12` i `3.13`. W kontroli polecenia workflow z misji 09 odtworzono lokalnie w
  osobnej kopii katalogu projektu. `uv sync` kończy się bez błędu, ale nie instaluje narzędzi, bo
  `pyproject.toml` z kroku 1 nie deklaruje zależności. Krok `uv run ruff check .` kończy się więc
  błędem „Failed to spawn: `ruff`”. Kontrolę powtórzono z narzędziami ze środowiska kursu.
  Polecenia z celem `.` sprawdzają wtedy także dostarczony `check.py`, który nie przechodzi
  `ruff check`, `ruff format --check` i `mypy --strict`. Workflow z instrukcji nie przechodzi więc
  w całości nawet lokalnie. Ta strona nie podaje jego poprawionej wersji.
- **Własne repozytorium.** Część „Final Step” obejmuje commit, `git push`, pull request, zielony
  znacznik CI i tag `v1.0.0`. Wymaga własnego repozytorium na GitHubie. W klonie kursu `origin`
  wskazuje repozytorium kursu, a `ci.yml` leży w katalogu projektu, nie w `.github/workflows/`
  katalogu głównego. Kurs nie opisuje przygotowania takiego repozytorium.
- **Operacje, których nie wykonano.** Przy przygotowaniu tej strony nie sprawdzano wysłania
  zmian, pull requestu, uruchomienia w GitHub Actions ani tagu. Końcowy komunikat `check.py`
  („Final step: push your branch…”) nie oznacza, że te kroki zostały sprawdzone.

**Sprawdź się:**
`uv run python level_5_maintainability/projects/03_full_release_pipeline/check.py`. Skrypt
sprawdza:

- że `pyproject.toml` zawiera napisy `[tool.ruff]`, `[tool.mypy]`, `[tool.pyright]` i
  `[tool.coverage`;
- że `.pre-commit-config.yaml` zawiera `ruff`, `ruff-format`, `mypy` i `repos:`, a `ci.yml` zawiera
  `ruff`, `mypy`, `pytest`, `uv`, `3.12` i `3.13`;
- że `CHANGELOG.md` zawiera napis `1.0.0`;
- że ruff i `mypy --strict` z konfiguracją projektu przechodzą dla `rpg.py`, a pyright przechodzi z
  opcją `--project`;
- że katalog `tests/` ma pliki `test_*.py`, testy przechodzą, a pokrycie `rpg.py` wynosi co
  najmniej 80%.

Skrypt nie uruchamia hooków pre-commit ani workflow. W kontroli przechodziły pliki z samymi napisami
w komentarzach. Nie sprawdza formatu Keep a Changelog, bo wystarcza napis „1.0.0”. Nie sprawdza
reguł ruffa (W, I i UP) ani sekcji `[tool.pytest.ini_options]`. Tryb strict dla pyright podaje
tylko komunikat skryptu: w kontroli przechodził też `typeCheckingMode = "basic"`, a krok 1 każe
ustawić tryb strict tylko dla mypy. Gdy pyright nie może się uruchomić z powodu błędu „nodeenv
failed”, skrypt wypisuje „❌ pyright failed — fix type errors…”, choć w kodzie nie ma błędów. Te
elementy porównaj z listą kroków instrukcji.

## Oczekiwane rezultaty

- `check.py` misji 07–09 i projektu Full Release Pipeline kończy się komunikatem o ukończeniu.
- Gra z misji 07 zgłasza błędy danych i zapisu własnymi wyjątkami, a polecenie `simulate` wypisuje
  czytelny komunikat zamiast tracebacku.
- Hooki z misji 08 przechodzą dla `task.py`, a workflow z misji 09 ma kroki ruff, mypy i pytest w
  macierzy Pythona 3.12 i 3.13.
- W projekcie `rpg.py` przechodzi ruff, mypy i pyright z konfiguracją projektu, testy mają co
  najmniej 80% pokrycia, a `CHANGELOG.md`, hooki i workflow są w katalogu projektu. Kroki na
  GitHubie wymagają własnego repozytorium i nie są częścią lokalnego sprawdzenia.

## Wskazówki

- Pierwsze uruchomienie hooków pre-commit wymaga dostępu do internetu. Kolejne korzystają z
  pobranych środowisk.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. Jeśli
  nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań na tej stronie.
- Po poziomie 5 mapa kursu przechodzi do poziomu 6, „API Interface with FastAPI”.
