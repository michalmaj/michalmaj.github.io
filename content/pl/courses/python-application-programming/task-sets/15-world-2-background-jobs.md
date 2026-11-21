---
title: "Zadania w tle i śledzenie ich statusu"
summary: "Drugi etap poziomu 7 kursu Python RPG Questbook (World 2: Background Jobs): trzy misje o endpointach async def, zadaniach uruchamianych w tle z identyfikatorem job_id i repozytorium statusów zadań, a także projekt Background Report Queue, który zamyka ten etap."
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
  misja-03:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/missions/03_async_api_endpoints/README.md
        lang: en
        label: "Instrukcja: Mission 03 — Async API Endpoints"
  misja-04:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/missions/04_background_jobs/README.md
        lang: en
        label: "Instrukcja: Mission 04 — Background Jobs"
  misja-05:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/missions/05_job_status_repository/README.md
        lang: en
        label: "Instrukcja: Mission 05 — Job Status Repository"
  background-report-queue:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/projects/02_background_report_queue/README.md
        lang: en
        label: "Instrukcja: Project 02 — Background Report Queue"
---
Ten zestaw obejmuje drugi etap poziomu 7 kursu Python RPG Questbook, „World 2: Background Jobs”.
Najpierw sprawdzasz, kiedy `async def` w endpoincie pomaga, a kiedy szkodzi. Potem budujesz wzorzec
identyfikatora zadania: `POST` od razu zwraca kod 202 i `job_id`, praca trwa w wątku w tle, a klient
sprawdza jej status osobnym żądaniem. Na koniec przenosisz statusy zadań z globalnego słownika do
repozytorium. Pierwsze trzy zadania to misje 03–05. Czwarte to projekt Background Report Queue,
który opis poziomu nazywa punktem kontrolnym („Checkpoint”). Podział poziomu na etapy pochodzi z
narzędzia postępu kursu, jak opisuje [zestaw 14](world-1-fundamentals.md). Instrukcje, kod, pliki
danych i komunikaty skryptów sprawdzających są po angielsku. Ta strona streszcza je po polsku i
odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium, kod startowy poziomu i katalog roboczy poleceń opisuje część
[„Przygotowanie do zestawu”](world-1-fundamentals.md#przygotowanie-do-zestawu) zestawu 14.

**Co wynosisz z wcześniejszych zestawów.** Ten etap korzysta z wiedzy z zestawu 14 o blokującej
symulacji i o asyncio oraz z routerów, zależności `Depends()` i `dependency_overrides` z
[zestawów 12](world-2-structure-and-di.md) i [13](world-3-quality-and-polish.md). Plików z
wcześniejszych zestawów nie potrzebujesz.

**Pliki.** Misje 03–05 i projekt to pakiety `task/` w katalogach zadań. Każda misja ma własną
aplikację FastAPI, własną kopię pakietu gry `task/rpg/` i plik `task/data/monsters.json`. Misje nie
zaczynają od wyniku poprzedniej. Misja 04 ma nową aplikację z jednym routerem turniejów, a misja 05
dostaje gotowe repozytoria zadań i klasy wykonawców (`workers.py`). Projekt ma gotową aplikację,
pięć plików sesji walk w `task/data/sessions/` i jeden plik do uzupełnienia. Kodu nie przenosisz
między zadaniami.

**Serwer.** Instrukcje misji 03–05 nie podają polecenia serwera, bo skrypty `check.py` wysyłają
żądania przez klienta testowego. Jeśli chcesz obejrzeć aplikację zadania w `/docs`, z katalogu
głównego działa polecenie z opcją `--app-dir`, na przykład dla misji 05:

```bash
uv run uvicorn task.main:app --app-dir level_7_concurrency_and_background_work/missions/05_job_status_repository
```

W innych zadaniach zmieniasz tylko ścieżkę katalogu. Serwer zatrzymujesz klawiszami Ctrl+C.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypty wysyłają żądania do aplikacji przez klient testowy
FastAPI. Skrypty misji 04 i projektu dodatkowo zatrzymują pracę w tle i sprawdzają, czy odpowiedź
HTTP wraca, zanim ta praca się skończy. Skrypty misji 05 i projektu w części HTTP podmieniają
wykonawcę zadań na `SyncWorker`, który wykonuje pracę od razu, bez wątku. Te skrypty wyłączają
ostrzeżenia, więc ostrzeżenie `StarletteDeprecationWarning` z zestawu 11 się nie pojawia. Gdy
wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp w pliku
`level_7_concurrency_and_background_work/.progress`. Gdy coś się nie zgadza, wypisuje, czego
oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy porównujesz z instrukcją samodzielnie. Jedno udane uruchomienie
pracy w tle nie dowodzi, że kolejność zdarzeń jest zawsze poprawna, dlatego ważne są też elementy,
których skrypt nie mierzy.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### Async API Endpoints: kiedy async def pomaga {#misja-03}

**Cel:** zobaczyć, co zmienia `async def` w endpoincie, który wykonuje obliczenia bez żadnego
`await`.

**Zakres pracy:** w `level_7_concurrency_and_background_work/missions/03_async_api_endpoints/` jest
pakiet `task/` z aplikacją, która ma routery potworów, walk i turniejów. Według instrukcji w
`task/routers/tournaments.py` zmieniasz `def run_tournament(...)` na `async def run_tournament(...)`
i nic więcej. Komentarz `TODO 1` w `task/main.py` każe dodatkowo dopisać `description=` do
`FastAPI()`. Instrukcja tego nie wymaga, a skrypt tego nie sprawdza.

**Rezultat:** na starcie skrypt zgłasza, że `run_tournament` musi być `async def`. Po zmianie
`POST /tournaments` nadal zwraca wynik turnieju. Tabela w instrukcji wyjaśnia, że FastAPI
uruchamia endpoint `def` w puli wątków, a `async def` bezpośrednio w pętli zdarzeń. Dla obliczeń bez
`await` oznacza to blokadę całej aplikacji. W kontroli na serwerze `GET /health` wysłane w trakcie
turnieju z 300 000 walk czekało z `async def` do końca turnieju, a z `def` odpowiadało od razu.
Instrukcja wskazuje, że właściwe rozwiązanie dla takich obliczeń pokazuje misja 07 z
[zestawu 16](world-3-parallel-execution.md#misja-07).

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/missions/03_async_api_endpoints/check.py`.
Skrypt sprawdza:

- że niezakomentowany kod `task/routers/tournaments.py` zawiera `async def run_tournament`;
- że `task/main.py` zawiera `async def health`. Tak jest już na starcie;
- że `POST /tournaments` z 10 walkami zwraca kod 200 i `total_battles` równe 10.

Skrypt nie mierzy blokowania aplikacji. Zachowanie z tabeli w instrukcji widać tylko na
działającym serwerze.

### Background Jobs: identyfikator zadania i wątek w tle {#misja-04}

**Cel:** zbudować wzorzec identyfikatora zadania: `POST /tournaments` zwraca od razu kod 202 i
`job_id`, a `GET /jobs/{job_id}` pokazuje status pracy, która trwa w wątku w tle.

**Zakres pracy:** w `level_7_concurrency_and_background_work/missions/04_background_jobs/` jest
pakiet `task/`. W `task/routers/tournaments.py` są gotowe: globalny słownik `_jobs`, obiekt usługi
`_svc` i funkcja `_run_tournament(job_id, n)`, która ustawia status `running`, a potem `completed`
albo `failed`. Według instrukcji i komentarzy `TODO` uzupełniasz dwie funkcje:

1. `start_tournament`: tworzy `job_id`, zapisuje zadanie w `_jobs` ze statusem `pending`,
   uruchamia wątek `threading.Thread` z `daemon=True`, który wywołuje `_run_tournament`, i zwraca
   `JobStarted` z kodem 202.
2. `get_job`: odczytuje zadanie z `_jobs`, dla nieznanego `job_id` zgłasza 404, a w przeciwnym razie
   zwraca `JobOut` ze wszystkimi polami.

Część „The smell” instrukcji wymienia wady globalnego słownika. Naprawia je misja 05.

**Rezultat:** na starcie skrypt zgłasza, że symulacja nie została wywołana. Po uzupełnieniu
wypisuje wiersze podane w części „How to check” instrukcji. Na działającym serwerze w kontroli
pierwsze `POST` zwracało 202 po kilku milisekundach, a status zadania zmieniał się z `running` na
`completed`.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/missions/04_background_jobs/check.py`.
Skrypt podmienia `_svc.simulate_tournament` na wersję, która czeka na sygnał, i sprawdza:

- że `POST /tournaments` zwraca kod 202 i `job_id`, zanim symulacja się skończy;
- że w tym czasie `GET /jobs/{job_id}` zwraca status `pending` albo `running`;
- że po zwolnieniu symulacji zadanie kończy się w ciągu 10 s statusem `completed`, a wynik ma
  `total_battles` równe 20;
- że nieznany `job_id` daje 404, a `battles` równe 0 daje 422.

Kolejność kroków ma znaczenie. W kontroli wersja, która uruchamiała wątek przed zapisaniem zadania
w `_jobs`, nie przechodziła w 10 próbach na 10, bo wątek nie znajdował jeszcze zadania. Skrypt
wypisuje wtedy, że symulacja nie została wywołana. Nie przechodziła też wersja z `BackgroundTasks`
FastAPI zamiast wątku, bo klient testowy czeka na zakończenie takich zadań przed zwróceniem
odpowiedzi. Skrypt nie sprawdza `daemon=True`. W kontroli przechodził wątek bez tej opcji.

### Job Status Repository: repozytorium zadań zamiast słownika {#misja-05}

**Cel:** zastąpić globalny słownik z misji 04 repozytorium zadań (`JobRepository`) i wykonawcą
dostarczanym przez `Depends()`.

**Zakres pracy:** w `level_7_concurrency_and_background_work/missions/05_job_status_repository/`
jest pakiet `task/`. Instrukcja opisuje jako gotowe:

- `task/jobs.py` z protokołem `JobRepository` i klasami `InMemoryJobRepository` oraz
  `JsonJobRepository`;
- `task/workers.py` z klasą `BackgroundWorker`, która wykonuje pracę w wątku w tle, i klasą
  `SyncWorker`, która wykonuje ją od razu, na potrzeby testów.

W `task/routers/tournaments.py` uzupełniasz `start_tournament` i `get_job`. Obie funkcje dostają
`job_repo`, `worker` i `svc` przez `Depends()`. `start_tournament` tworzy zadanie w `job_repo`,
przekazuje symulację do `worker` i zwraca `JobStarted`. `get_job` zwraca `JobOut` albo 404.
Instrukcja zaznacza, że `BackgroundWorker` działa tylko w jednym procesie i nie zastępuje trwałej
kolejki zadań.

**Rezultat:** na starcie skrypt potwierdza działanie gotowych repozytoriów i `SyncWorker`, a potem
zgłasza, że `POST /tournaments` zwraca 500 zamiast 202. Skrypt w części HTTP używa `SyncWorker`,
więc prawdziwą pracę w tle widać tylko na serwerze, uruchomionym poleceniem z przygotowania do
zestawu. W kontroli `POST` zwracał 202, a status zmieniał się z `running` na `completed`.
`BackgroundWorker` ustawia `running` przed uruchomieniem wątku, więc status `pending` nie był
widoczny. Kolejne `POST` wysłane w trakcie trwających symulacji odpowiadały wolniej, bo wątki
jednego procesu dzielą procesor. Rolę GIL wyjaśnia misja 06 z
[zestawu 16](world-3-parallel-execution.md#misja-06).

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/missions/05_job_status_repository/check.py`.
Skrypt sprawdza:

- gotowe `InMemoryJobRepository`, `JsonJobRepository` i `SyncWorker`. Te punkty przechodzą już na
  starcie;
- że z `SyncWorker` podstawionym przez `dependency_overrides` `POST /tournaments` zwraca 202, a
  zadanie od razu ma status `completed` i wynik z `total_battles` równym 20 oraz sumą
  `hero_wins` i `monster_wins` równą 20;
- że nieznany `job_id` daje 404;
- że niezakomentowany kod routera nie zawiera napisu `_jobs`.

Skrypt nie sprawdza, czy endpoint korzysta z wykonawcy dostarczonego przez `Depends()`. W kontroli
przechodziła wersja, która liczyła turniej od razu w endpoincie, bez wykonawcy, i wersja, która
tworzyła własny `BackgroundWorker`. Ta druga przechodziła 10 razy na 10, bo 20 walk kończyło się,
zanim skrypt sprawdzał status. Porównaj kod z częścią „Your task” instrukcji.

### Background Report Queue: raport liczony w tle {#background-report-queue}

Opis poziomu nazywa ten projekt punktem kontrolnym („Checkpoint”), a narzędzie postępu umieszcza go
na końcu etapu World 2. Instrukcja projektu nie podaje wymagań wstępnych.

**Cel:** zaimplementować wykonawcę `BackgroundWorker`, tak żeby `POST /reports` od razu zwracał
kod 202 i `job_id`, a raport z sesji walk liczył się w wątku w tle.

**Zakres pracy:** w `level_7_concurrency_and_background_work/projects/02_background_report_queue/`
jest pakiet `task/`. Instrukcja oznacza jako gotowe i niezmieniane `main.py`, `routers/reports.py`,
`dependencies.py`, `schemas.py` i `report.py` z funkcją `compute_report()`, która czyta pięć plików
z `task/data/sessions/`. W `task/jobs.py` są gotowe `InMemoryJobRepository` i `SyncWorker`, których
też nie zmieniasz. Uzupełniasz metodę `BackgroundWorker.submit(job_id, fn)`. Według instrukcji:

- od razu ustawia status `running`;
- uruchamia wątek z `daemon=True`, który wywołuje `fn()`;
- po sukcesie zapisuje wynik przez `set_result`, a po wyjątku błąd przez `set_error`;
- wraca, zanim `fn()` się skończy.

W tym projekcie `set_result` i `set_error` repozytorium same ustawiają status `completed` albo
`failed`, inaczej niż w misji 05. Instrukcja zawiera też rozwijaną podpowiedź z kodem.

**Rezultat:** na starcie skrypt wypisuje kilka poprawnych wyników części HTTP, bo zastępuje Twój
wykonawcę klasą `SyncWorker`. Zatrzymuje się dopiero na sprawdzeniu, czy `BackgroundWorker` używa
`threading.Thread`. Komunikat skryptu o niezaimplementowanej metodzie się nie pojawia. Po
uzupełnieniu raport ma pięć sesji i odsetek wygranych bohatera równy 0,6, zgodnie z tabelą w
instrukcji. Na działającym serwerze w kontroli raport był gotowy już przy pierwszym sprawdzeniu
statusu.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/projects/02_background_report_queue/check.py`.
Skrypt sprawdza:

- z `SyncWorker`: `GET /health`, `POST /reports` z kodem 202 i `job_id`, raport ze statusem
  `completed`, pięcioma sesjami, `hero_win_rate` równym 0,6 i nagłówkiem „# Combat Report”, 404
  dla nieznanego zadania i 422 dla treści, która nie jest poprawnym JSON;
- że w `task/jobs.py` są klasy `BackgroundWorker` i `SyncWorker`, a `BackgroundWorker` używa
  `Thread`;
- że `BackgroundWorker.submit()` wraca w czasie krótszym niż 0,1 s, gdy zadanie jeszcze czeka, że
  w tym czasie status to `running`, a po zakończeniu `completed`;
- że zadanie, które zgłasza wyjątek, kończy się statusem `failed`.

Nie sprawdza `daemon=True`. W kontroli przechodził wątek bez tej opcji. W misji 05 skrypt nie
sprawdzał samego wykonawcy, a tutaj sprawdza go bezpośrednio, z prawdziwym wątkiem.

## Oczekiwane rezultaty

- `check.py` misji 03–05 i projektu Background Report Queue kończy się komunikatem o ukończeniu.
- `POST` zwraca kod 202 i `job_id`, zanim praca w tle się skończy, a status zadania można odczytać
  osobnym żądaniem.
- Statusy zadań są w repozytorium, a wykonawcę zadań można podmienić w testach na `SyncWorker`.

## Wskazówki

- Na działającym serwerze statusy zadań w misjach 04 i 05 i w projekcie są przechowywane w
  pamięci i znikają po zatrzymaniu serwera. Część „The smell” misji 04 i opis repozytoriów w misji
  05 wyjaśniają, kiedy przydaje się `JsonJobRepository`.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. W tym
  zestawie kieruj się kolejnością zadań na tej stronie.
- Ostatni etap poziomu 7 opisuje [zestaw 16](world-3-parallel-execution.md).
