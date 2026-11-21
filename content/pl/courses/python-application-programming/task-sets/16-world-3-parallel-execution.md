---
title: "Równoległe wykonywanie: pule wątków i procesów"
summary: "Trzeci etap poziomu 7 kursu Python RPG Questbook (World 3: Parallel Execution): trzy misje o pulach wątków dla operacji na plikach, pulach procesów dla obliczeń i deterministycznych testach pracy w tle, a także projekt Concurrent Tournament Runner, który zamyka poziom 7."
status: published
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu: instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: level_7_concurrency_and_background_work/README.md
    lang: en
    label: "Poziom 7 — Concurrency and Background Work: założenia, misje i projekty"
  - repository: python-rpg-questbook
    path: tools/course_status.py
    lang: en
    label: "Narzędzie postępu: podział poziomu 7 na etapy (World 1–3)"
tasks:
  misja-06:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/missions/06_thread_pool_for_blocking_io/README.md
        lang: en
        label: "Instrukcja: Mission 06 — Thread Pool for Blocking I/O"
  misja-07:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/missions/07_process_pool_for_cpu_work/README.md
        lang: en
        label: "Instrukcja: Mission 07 — Process Pool for CPU-Bound Work"
  misja-08:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/missions/08_testing_background_work/README.md
        lang: en
        label: "Instrukcja: Mission 08 — Testing Background Work"
  concurrent-tournament-runner:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/projects/03_concurrent_tournament_runner/README.md
        lang: en
        label: "Instrukcja: Boss Fight — Concurrent Tournament Runner"
---
Ten zestaw obejmuje trzeci, ostatni etap poziomu 7 kursu Python RPG Questbook, „World 3: Parallel
Execution”. Operacje na plikach rozdzielasz między wątki, a obliczenia między procesy. Potem
piszesz testy pracy w tle, które dają ten sam wynik przy każdym uruchomieniu. Na końcu budujesz
API turniejów, które od razu zwraca identyfikator zadania i liczy walki w wielu procesach. Pierwsze
trzy zadania to misje 06–08. Czwarte to projekt Concurrent Tournament Runner, który opis poziomu
nazywa walką z bossem („Boss Fight”) i umieszcza na końcu poziomu 7. Podział poziomu na etapy
pochodzi z narzędzia postępu kursu, jak opisuje [zestaw 14](world-1-fundamentals.md). Instrukcje,
kod, pliki danych i komunikaty skryptów sprawdzających są po angielsku. Ta strona streszcza je po
polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium i katalog roboczy poleceń opisuje część
[„Przygotowanie do zestawu”](world-1-fundamentals.md#przygotowanie-do-zestawu) zestawu 14, a
polecenie serwera z opcją `--app-dir` część
[„Przygotowanie do zestawu”](world-2-background-jobs.md#przygotowanie-do-zestawu) zestawu 15.

**Co wynosisz z wcześniejszych zestawów.** Ten etap korzysta z wzorca identyfikatora zadania,
repozytoriów zadań i klasy `SyncWorker` z [zestawu 15](world-2-background-jobs.md) oraz z testów z
klientem testowym i `dependency_overrides` z [zestawu 13](world-3-quality-and-polish.md). Plików z
wcześniejszych zestawów nie potrzebujesz.

**Pliki.** Misja 06 ma własny `task.py` i pięć plików sesji walk w `data/sessions/`. Misja 07 ma
własny `task.py` z uproszczonym modelem walki, bez pakietu gry. Misja 08 ma pakiet `task/` z
kompletną aplikacją i plikiem testów do uzupełnienia. Repozytoria i wykonawcy w tym pakiecie są
takie same jak w misji 05. Projekt ma własny katalog z pakietami `rpg/`, `jobs/` i `api/`, testami w
`tests/`, danymi w `data/` i plikiem `cli.py`. Kodu nie przenosisz między zadaniami.

**Polecenia projektu.** Katalog projektu Concurrent Tournament Runner ma własny `pyproject.toml` z
sekcją `[project]` i własny `uv.lock`, a w jego zależnościach nie ma ruffa. `uv run` wpisane w tym
katalogu tworzy osobne środowisko `.venv` z zależnościami projektu. W kontroli
`uv run python check.py` w katalogu projektu kończył się na ostatnim sprawdzeniu komunikatem
„❌ ruff check api/ tests/ fails — fix the lint errors above:”, choć pod nim nie było żadnych
błędów. Polecenie `uv run python -m ruff check api/ tests/` z instrukcji kończyło się tam błędem
„No module named ruff”. Z katalogu głównego oba sprawdzenia działają, tak jak polecenia narzędzi w
[zestawie 8](world-1-static-analysis.md#przygotowanie-do-zestawu). Dlatego polecenia projektu na tej
stronie podają ścieżki od katalogu głównego. Katalogi misji 06–08 nie mają własnego
`pyproject.toml`.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. W misjach 06 i 07 skrypty sprawdzają wyniki Twoich funkcji, a
potem podmieniają pulę na wersję, która wykonuje pracę od razu i zapisuje każde przekazane jej
zadanie. Dzięki temu widzą, czy praca naprawdę trafiła do puli. Skrypt misji 08 uruchamia Twoje
testy, a potem po kolei psuje jedno zachowanie w kodzie i sprawdza, czy testy to wykrywają. Skrypt
projektu wysyła żądania przez klient testowy z `SyncWorker`, uruchamia Twoje testy, sprawdza gotowy
wykonawcę z pulą procesów i uruchamia ruffa. Gdy wszystko się zgadza, skrypt wypisuje komunikat o
ukończeniu i zapisuje postęp w pliku `level_7_concurrency_and_background_work/.progress`. Gdy coś
się nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy porównujesz z instrukcją samodzielnie. Skrypty nie mierzą, czy
praca równoległa jest szybsza. Instrukcja misji 07 zaznacza, że przy małej liczbie walk pula
procesów może być wolniejsza od wykonania po kolei.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### Thread Pool for Blocking I/O: pula wątków dla plików {#misja-06}

**Cel:** eksportować raporty z sesji walk współbieżnie, w puli wątków `ThreadPoolExecutor`.

**Zakres pracy:** w `level_7_concurrency_and_background_work/missions/06_thread_pool_for_blocking_io/`
jest `task.py` z gotowymi funkcjami `export_one_session()`, która czyta jeden plik sesji i zapisuje
raport w Markdown, i `export_sessions_sequential()`, która robi to po kolei. Uzupełniasz
`export_sessions_parallel(session_ids, sessions_dir, output_dir, workers=4)`: tworzy pulę wątków z
podaną liczbą wątków, przekazuje do niej `export_one_session()` dla każdej sesji i zwraca listę
ścieżek plików. Instrukcja podaje dwa warianty z `pool.map()` albo `pool.submit()`. Część „Key
Insight” wyjaśnia, że wątki pomagają przy czekaniu na pliki, a przy obliczeniach w czystym Pythonie
ogranicza je GIL.

**Rezultat:** na starcie skrypt zgłasza, że `export_sessions_parallel` nie jest zaimplementowana.
Po uzupełnieniu skrypt eksportuje pięć raportów do katalogu tymczasowego, więc w repozytorium nie
powstają nowe pliki.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/missions/06_thread_pool_for_blocking_io/check.py`.
Skrypt sprawdza:

- że eksport po kolei i eksport w puli zwracają po pięć ścieżek, a pliki istnieją;
- że raport zawiera nagłówek „## Battle Report”;
- że po podmianie puli na wersję zapisującą zadania trafiają do niej co najmniej dwa osobne
  zadania, a wszystkie pięć sesji jest wyeksportowanych.

Nie sprawdza, czy do puli trafiają wszystkie sesje, ani parametru `workers`. W kontroli
przechodziła wersja, która przekazywała do puli dwie sesje, a resztę eksportowała po kolei, i
wersja z pulą zawsze jednowątkową. Porównaj kod z częścią „Your Task” instrukcji.

### Process Pool for CPU Work: pula procesów dla obliczeń {#misja-07}

**Cel:** rozdzielić symulację wielu walk między procesy w puli `ProcessPoolExecutor`.

**Zakres pracy:** w `level_7_concurrency_and_background_work/missions/07_process_pool_for_cpu_work/`
jest `task.py` z własnym, uproszczonym modelem walki. Gotowe są funkcja `_simulate_one(seed)`,
która rozgrywa jedną walkę deterministycznie dla podanego ziarna, i
`simulate_tournament_sequential(n)`. Uzupełniasz `simulate_tournament_parallel(n, workers=4)`, która
zwraca słownik w tym samym formacie. Według instrukcji:

- walki trafiają do puli jako osobne zadania: przez `pool.map()` albo wiele wywołań
  `pool.submit()`, także w małych porcjach ziaren;
- każde zadanie wywołuje `_simulate_one`, bez własnej logiki walki;
- `_simulate_one` zostaje funkcją na poziomie modułu, bo pula procesów przesyła ją do procesów
  potomnych przez `pickle`, a funkcji `lambda` ani funkcji zagnieżdżonych tak przesłać nie można.

Instrukcja zawiera też rozwijaną podpowiedź z gotową implementacją.

**Rezultat:** na starcie skrypt zgłasza, że `simulate_tournament_parallel` nie jest
zaimplementowana. Po uzupełnieniu liczba wygranych bohatera w wersji równoległej jest taka sama jak
w wersji wykonywanej po kolei, bo te same ziarna dają te same walki.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/missions/07_process_pool_for_cpu_work/check.py`.
Skrypt sprawdza:

- że dla 2000 walk wersja równoległa z czterema procesami zwraca te same `total_battles` i
  `hero_wins` co wersja wykonywana po kolei;
- że po podmianie puli na wersję zapisującą zadania trafiają do niej co najmniej dwa osobne
  zadania, żadne nie jest funkcją `lambda`, a przy zadaniach z pojedynczymi ziarnami pokryte są
  wszystkie ziarna;
- że `_simulate_one` da się zapisać przez `pickle` i uruchomić w prawdziwej puli procesów.

Nie sprawdza parametru `workers`. W kontroli przechodziła wersja ze stałą liczbą procesów i wersja
z dwiema porcjami ziaren, na którą instrukcja pozwala. Nie przechodziła wersja z pulą wątków ani
wersja, która przekazywała do puli cały turniej jako jedno zadanie.

### Testing Background Work: deterministyczne testy pracy w tle {#misja-08}

**Cel:** napisać testy systemu zadań w tle, które dają ten sam wynik przy każdym uruchomieniu,
dzięki `SyncWorker` zamiast wątków.

**Zakres pracy:** w `level_7_concurrency_and_background_work/missions/08_testing_background_work/`
jest pakiet `task/` z kompletną aplikacją, repozytorium `InMemoryJobRepository` i wykonawcami
`BackgroundWorker` oraz `SyncWorker`. W `task/tests/test_background.py` jest sześć funkcji
testowych, które zgłaszają `NotImplementedError`. Tabela w instrukcji opisuje, co ma sprawdzać
każda z nich: nowe zadanie ma status `pending`, po `submit()` status `completed`, wyjątek w zadaniu
daje status `failed` i zapisany błąd, wynik zostaje zapisany, dwa zadania nie nadpisują swoich
wyników, a nieznany identyfikator daje `None`. Zasady z instrukcji: `SyncWorker` zamiast
`BackgroundWorker`, bez `time.sleep()` i nowe obiekty w każdym teście.

```bash
uv run pytest level_7_concurrency_and_background_work/missions/08_testing_background_work/task/tests/test_background.py -v
```

**Rezultat:** na starcie wszystkie sześć testów kończy się błędem `NotImplementedError`. Po
uzupełnieniu sześć testów przechodzi.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/missions/08_testing_background_work/check.py`.
Skrypt sprawdza:

- że plik testów zawiera napis `SyncWorker`, jego niezakomentowany kod nie zawiera `time.sleep` i
  ma co najmniej sześć funkcji `test_`;
- że testy przechodzą z gotowym kodem;
- że testy nie przechodzą po każdej z sześciu zmian w `task/jobs.py` albo `task/workers.py`, po
  jednej dla każdego zachowania z tabeli w instrukcji.

Na czas każdej próby skrypt zmienia te dwa pliki, a potem je przywraca. Szuka tylko napisu
`time.sleep`. W kontroli przechodził test z `from time import sleep` i wywołaniem `sleep()`, choć
opis na początku pliku testów zabrania `sleep()` i `threading.Event`.

### Concurrent Tournament Runner: turnieje w tle i w wielu procesach {#concurrent-tournament-runner}

Opis poziomu nazywa ten projekt walką z bossem („Boss Fight”), a narzędzie postępu umieszcza go na
końcu etapu World 3, czyli na końcu poziomu 7. Instrukcja projektu kieruje na koniec do epilogu
analitycznego Questbooka. Jego miejsce w Questbooku i w przedmiocie opisuje
[zestaw 17](final-analytics-epilogue.md).

**Cel:** zbudować API turniejów, które nie blokuje klienta: `POST` od razu zwraca `job_id`, walki
liczą się w tle, a klient sprawdza status i pobiera raport w Markdown, gdy zadanie się skończy.

**Zakres pracy:** w `level_7_concurrency_and_background_work/projects/03_concurrent_tournament_runner/`
gotowe są pakiety `rpg/` i `jobs/`. Plik `jobs/jobs.py` zawiera repozytoria zadań, `SyncWorker`,
`BackgroundWorker` i `ProcessPoolTournamentWorker`, który w wątku w tle rozdziela walki między
procesy. `api/dependencies.py` łączy aplikację z `JsonJobRepository` i z tym wykonawcą. Według
instrukcji:

1. W `api/routers/tournaments.py` uzupełniasz trzy endpointy: `POST /tournaments` z kodem 202 i
   `job_id`, `GET /tournaments/{job_id}` ze statusem i wynikiem albo 404 oraz
   `GET /tournaments/{job_id}/report` z raportem jako `text/plain`. Raport zwraca 404 dla nieznanego
   zadania i 425, gdy zadanie jeszcze się nie skończyło. Komentarze `TODO` opisują kroki.
2. W `tests/test_api.py` piszesz co najmniej sześć testów dla sześciu zachowań wymienionych w
   instrukcji, z `SyncWorker` podstawionym przez `dependency_overrides` i bez `time.sleep()`.
   Fixture `client` jest gotowa, a komentarz w pliku podpowiada, jak przygotować test kodu 425.

```bash
uv run pytest level_7_concurrency_and_background_work/projects/03_concurrent_tournament_runner/tests/test_api.py -v
uv run ruff check level_7_concurrency_and_background_work/projects/03_concurrent_tournament_runner/api/ level_7_concurrency_and_background_work/projects/03_concurrent_tournament_runner/tests/
```

Podsumowanie pytest zawiera ostrzeżenie opisane w
[zestawie 11](world-1-http-basics.md#przygotowanie-do-zestawu). ruff wywołany z katalogu głównego
korzysta z konfiguracji z `pyproject.toml` repozytorium, tak jak skrypt projektu.

Instrukcja nie podaje polecenia serwera. Z katalogu głównego działa:

```bash
uv run uvicorn api.main:app --app-dir level_7_concurrency_and_background_work/projects/03_concurrent_tournament_runner
```

W kontroli na serwerze `POST /tournaments` zwracał 202 po kilku milisekundach, status zmieniał się
z `running` na `completed`, a raport zwracał 425 w trakcie pracy i 200 po jej zakończeniu.
Zadania zapisują się jako pliki JSON w `data/jobs/`. Plik `.gitignore` w tym katalogu wyklucza je z
repozytorium.

**Rezultat:** na starcie skrypt potwierdza `GET /health` i zgłasza, że `POST /tournaments` zwraca
500 zamiast 202. Po uzupełnieniu przechodzą wszystkie sprawdzenia, a raport zaczyna się od nagłówka
„## Tournament Report”.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/projects/03_concurrent_tournament_runner/check.py`.
Skrypt sprawdza:

- z `SyncWorker`: `GET /health`, `POST /tournaments` z kodem 202 i `job_id`, status `completed` z
  wynikiem, raport `text/plain` z nagłówkiem „## Tournament Report”, 404 dla nieznanego zadania, 422
  dla `battles` równego 0 i 425 dla raportu zadania o statusie `running`;
- że `tests/test_api.py` ma co najmniej sześć funkcji `test_`, a pytest w katalogu projektu
  kończy się kodem 0;
- gotowy `ProcessPoolTournamentWorker`: że `_simulate_one` da się zapisać przez `pickle`, że
  `submit()` przyjmuje `job_id` i liczbę walk, że 40 walk kończy się w prawdziwej puli procesów i
  że w klasie nie ma funkcji `lambda`;
- że ruff z konfiguracją repozytorium nie zgłasza błędów w `api/` i `tests/`.

Nie sprawdza treści testów: wystarczy, że jest ich co najmniej sześć i przechodzą. W kontroli
przechodziło sześć pustych testów. Sprawdzenia `ProcessPoolTournamentWorker` dotyczą gotowej klasy,
więc przechodzą od początku, jeśli jej nie zmieniasz. Testy porównaj z listą zachowań w instrukcji.

## Oczekiwane rezultaty

- `check.py` misji 06–08 i projektu Concurrent Tournament Runner kończy się komunikatem o
  ukończeniu.
- Eksport sesji korzysta z puli wątków, a symulacja turnieju z puli procesów z tym samym wynikiem
  co wersja wykonywana po kolei.
- Testy pracy w tle przechodzą bez czekania i wykrywają zmiany zachowań z instrukcji.
- API projektu od razu zwraca `job_id`, pokazuje status zadania i zwraca raport dopiero po jego
  zakończeniu.

## Wskazówki

- Katalogi `.venv`, które `uv run` tworzy w katalogach projektu i startera, są w `.gitignore`
  repozytorium. Plik `uv.lock` startera jest śledzony, więc jego zmianę przez uv pokazuje
  `git status`, co opisuje [zestaw 14](world-1-fundamentals.md#przygotowanie-do-zestawu).
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. W tym
  zestawie kieruj się kolejnością zadań na tej stronie.
- Po poziomie 7 mapa kursu umieszcza Final Analytics Epilogue, opisany w
  [zestawie 17](final-analytics-epilogue.md).
