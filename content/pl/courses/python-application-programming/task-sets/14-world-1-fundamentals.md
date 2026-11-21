---
title: "Podstawy współbieżności: blokowanie i asyncio"
summary: "Pierwszy etap poziomu 7 kursu Python RPG Questbook (World 1: Fundamentals): dwie misje o tym, dlaczego długa symulacja blokuje aplikację, i o podstawach asyncio, a także projekt Async Quest Aggregator, który zamyka ten etap."
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
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: misje i projekty poziomu 7"
  - repository: python-rpg-questbook
    path: tools/course_status.py
    lang: en
    label: "Narzędzie postępu: podział poziomu 7 na etapy (World 1–3)"
  - repository: python-rpg-questbook
    path: level_7_concurrency_and_background_work/starter_blocking_rpg_api/README.md
    lang: en
    label: "Kod startowy poziomu 7: Blocking RPG Tournament API"
tasks:
  misja-01:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/missions/01_blocking_vs_background_work/README.md
        lang: en
        label: "Instrukcja: Mission 01 — Blocking vs Background Work"
  misja-02:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/missions/02_asyncio_basics/README.md
        lang: en
        label: "Instrukcja: Mission 02 — asyncio Basics"
  async-quest-aggregator:
    materials:
      - repository: python-rpg-questbook
        path: level_7_concurrency_and_background_work/projects/01_async_quest_aggregator/README.md
        lang: en
        label: "Instrukcja: Project 01 — Async Quest Aggregator"
---
Ten zestaw obejmuje pierwszy etap poziomu 7 kursu Python RPG Questbook, „World 1: Fundamentals”.
Poziom 7 zaczyna się od problemu z poziomu 6: API gry działa, ale symulacja wielu walk trwa długo,
a klient czeka na odpowiedź przez cały ten czas. W tym etapie mierzysz czas takiej blokującej
symulacji i poznajesz podstawy asyncio: funkcje `async def`, `await`, `asyncio.gather` i
`asyncio.wait_for`. Pierwsze dwa zadania to misje 01 i 02. Trzecie to projekt Async Quest
Aggregator, który opis poziomu nazywa punktem kontrolnym („Checkpoint”). Podział poziomu 7 na trzy
etapy pochodzi z narzędzia postępu kursu, `tools/course_status.py`. Mapa kursu i opis poziomu
wymieniają misje i projekty bez tego podziału. Instrukcje, kod, pliki danych i komunikaty skryptów
sprawdzających są po angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1. Poziom 7
korzysta z bibliotek standardowych Pythona (`asyncio`, `threading`, `concurrent.futures`) i z
FastAPI z poziomu 6, więc nie instalujesz nic nowego.

**Co wynosisz z wcześniejszych zestawów.** Opis poziomu 7 zakłada ukończony poziom 6, opisany w
zestawach 11–13. W tym etapie przyda się przede wszystkim rozumienie, jak FastAPI obsługuje
endpointy, z [zestawu 11](world-1-http-basics.md). Kolejne etapy poziomu 7 korzystają też z
routerów, zależności `Depends()`, klienta testowego i `dependency_overrides` z zestawów 12 i 13.
Własnego kodu z poziomu 6 nie potrzebujesz.

**Pliki.** Misja 01 ma własny `task.py`, katalog `data/` z plikiem `monsters.json` i własną kopię
pakietu `rpg/`, taką samą jak w kodzie startowym poziomu. Misja 02 i projekt mają własne pliki
`task.py` bez kodu gry. Kodu nie przenosisz między zadaniami.

**Kod startowy.** Poziom 7 ma przygotowaną wersję API turniejów, `starter_blocking_rpg_api/`, w
której `POST /tournaments` czeka na koniec całej symulacji. Opis poziomu każe uruchomić w jego
katalogu polecenia `uv run python cli.py simulate --battles 100` i `uv run pytest tests/ -q`. W
kontroli pierwsze kończyło się błędem „Got unexpected extra argument(s) (simulate)”. Opis startera
podaje działającą formę, bez słowa `simulate`. Katalog startera ma też własny `pyproject.toml` i
`uv.lock`. `uv run` wpisane w tym katalogu tworzy osobne środowisko `.venv`, a ponieważ w `uv.lock`
brakuje grupy `dev` z pytest, uv dopisuje ją do śledzonego pliku `uv.lock` i `git status` pokazuje
go jako zmieniony. Z katalogu głównego repozytorium polecenia działają bez tych skutków:

```bash
uv run python level_7_concurrency_and_background_work/starter_blocking_rpg_api/cli.py --battles 100
uv run pytest level_7_concurrency_and_background_work/starter_blocking_rpg_api/tests -q
```

Pierwsze polecenie wypisuje raport turnieju w Markdown, a drugie uruchamia siedem testów startera.

Opis startera uruchamia też API poleceniem `uv run fastapi dev api/main.py`. W kontroli kończyło
się ono błędem „No module named 'api'”, bo katalog startera ma plik `__init__.py` i FastAPI
importuje aplikację jako część pakietu `starter_blocking_rpg_api`. Działało polecenie z katalogu
głównego, w którym opcja `--app-dir` wskazuje katalog startera:

```bash
uv run uvicorn api.main:app --app-dir level_7_concurrency_and_background_work/starter_blocking_rpg_api
```

Serwer działa pod adresem `http://127.0.0.1:8000`, a zatrzymujesz go klawiszami Ctrl+C. Stronę
`/docs` opisuje [zestaw 11](world-1-http-basics.md#przygotowanie-do-zestawu). Opis startera mówi, że
podczas długiego turnieju serwer nie obsłuży innych żądań. W kontroli klient, który wysłał
`POST /tournaments` z 300 000 walk, czekał na wynik, ale `GET /health` odpowiadał w tym czasie bez
czekania na koniec turnieju. Endpoint zdefiniowany przez `def` działa bowiem w puli wątków FastAPI,
co wyjaśnia instrukcja misji 01. Blokadę całej aplikacji przez `async def` pokazuje misja 03 z
[zestawu 15](world-2-background-jobs.md#misja-03).

**Polecenia i katalog roboczy.** Polecenia `check.py` na tej stronie wpisujesz w katalogu głównym
repozytorium, jak w poprzednich zestawach. Katalogi misji i projektu z tego etapu nie mają
własnego `pyproject.toml`, więc `uv run python check.py` z instrukcji, wpisane w katalogu zadania,
też działa.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypty wywołują Twoje funkcje i sprawdzają ich wyniki. W
misji 02 i w projekcie mierzą też czas, żeby odróżnić wykonanie współbieżne od wykonywania po kolei.
W kontroli poprawne rozwiązania przechodziły te pomiary 20 razy na 20 na nieobciążonym komputerze i
10 razy na 10 przy pełnym obciążeniu procesora. Gdy wszystko się zgadza, skrypt wypisuje komunikat
o ukończeniu i zapisuje postęp w pliku `level_7_concurrency_and_background_work/.progress`, który
jest w `.gitignore` repozytorium. Gdy coś się nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy porównujesz z instrukcją samodzielnie. Jedno udane uruchomienie
programu współbieżnego nie dowodzi jeszcze, że jest poprawny, dlatego warto porównać z instrukcją
także te elementy, których skrypt nie mierzy. Część „Key insight” i podpowiedzi służą samodzielnej
pracy i `check.py` ich nie sprawdza.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### Blocking vs Background Work: ile trwa blokująca symulacja {#misja-01}

**Cel:** zmierzyć, ile trwa wywołanie `simulate_tournament()`, i zobaczyć, że zajmuje ono wątek do
końca wszystkich walk.

**Zakres pracy:** w `level_7_concurrency_and_background_work/missions/01_blocking_vs_background_work/`
jest `task.py` z gotowym obiektem usługi `_svc` (klasa `SimulationService`) i funkcją
`time_tournament(n)`, która zgłasza `NotImplementedError`. Według instrukcji funkcja ma wywołać
`_svc.simulate_tournament(n)`, zmierzyć czas tego wywołania i zwrócić słownik z kluczami
`battles`, `time_seconds` i `battles_per_second`.

**Rezultat:** na starcie skrypt zgłasza, że `time_tournament` nie jest zaimplementowana. Po
uzupełnieniu wypisuje czas dla 50 i dla 5000 walk. Część „Key insight” instrukcji wyjaśnia, że
czas rośnie mniej więcej proporcjonalnie do liczby walk, i opisuje, jak FastAPI uruchamia
endpointy `def`.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/missions/01_blocking_vs_background_work/check.py`.
Skrypt sprawdza:

- że `time_tournament(7)` naprawdę wywołuje `_svc.simulate_tournament(7)`, a wynik ma
  `battles` równe 7;
- że wynik dla 50 walk ma wszystkie trzy klucze, `battles` równe 50 i nieujemne `time_seconds`.

Nie sprawdza, czy zmierzony czas jest prawdziwy, ani wartości `battles_per_second`. W kontroli
przechodziła funkcja, która wpisywała stały, bardzo mały czas, i funkcja ze stałą wartością
przepustowości. Wzór na `battles_per_second` porównaj z instrukcją.

### asyncio Basics: async/await, gather i wait_for {#misja-02}

**Cel:** poznać trzy podstawowe elementy asyncio: funkcje `async def` z `await`, współbieżne
uruchamianie przez `asyncio.gather` i limit czasu przez `asyncio.wait_for`.

**Zakres pracy:** w `level_7_concurrency_and_background_work/missions/02_asyncio_basics/` jest
`task.py` z trzema funkcjami do uzupełnienia. Według instrukcji:

1. `fetch_monster_data(name)` udaje wolne zapytanie przez `await asyncio.sleep(0.05)` i zwraca
   słownik `{"name": name, "fetched": True}`.
2. `fetch_all_monsters(names)` pobiera wszystkie potwory współbieżnie przez `asyncio.gather`.
3. `fetch_with_timeout(name, timeout)` wywołuje `fetch_monster_data()` przez `asyncio.wait_for` i
   po przekroczeniu limitu czasu zwraca `None`.

**Rezultat:** na starcie skrypt kończy się wyjątkiem `NotImplementedError` z pełnym śladem
wywołań zamiast krótkiego komunikatu. Po uzupełnieniu trzy potwory pobierają się w czasie bliskim
0,05 s, a nie 0,15 s, a wywołanie z limitem 0,01 s zwraca `None`.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/missions/02_asyncio_basics/check.py`.
Skrypt sprawdza:

- że `fetch_monster_data("Goblin")` zwraca słownik z `name` równym `"Goblin"`;
- że `fetch_all_monsters()` dla trzech nazw zwraca trzy wyniki w czasie nie dłuższym niż 0,12 s;
- że `fetch_with_timeout()` z limitem 1,0 s zwraca wynik, a z limitem 0,01 s zwraca `None`.

Nie sprawdza klucza `fetched`, czasu oczekiwania 0,05 s ani tego, czy `fetch_all_monsters()`
używa `asyncio.gather`. W kontroli przechodziła wersja, która czekała 0,02 s i pobierała potwory po
kolei, bo trzy takie pobrania mieszczą się w progu 0,12 s. Porównaj kod z krokami instrukcji.

### Async Quest Aggregator: zadania z kilku źródeł z limitem czasu {#async-quest-aggregator}

Opis poziomu nazywa ten projekt punktem kontrolnym („Checkpoint”), a narzędzie postępu umieszcza go
na końcu etapu World 1. Instrukcja projektu nie podaje wymagań wstępnych.

**Cel:** pobrać zadania z trzech źródeł jednocześnie, tak żeby źródło, które przekroczy limit
czasu, nie opóźniało pozostałych, a jego zadania po prostu nie pojawiły się w wyniku.

**Zakres pracy:** w `level_7_concurrency_and_background_work/projects/01_async_quest_aggregator/`
jest `task.py` z klasami `Quest` i `AggregateResult`, trzema gotowymi źródłami, które odpowiadają
po 0,1 s, 0,05 s i 0,2 s, oraz słownikiem `SOURCES`. Źródeł i słownika nie zmieniasz. Uzupełniasz
funkcję `aggregate_all_quests(timeout)`. Według instrukcji:

- wszystkie źródła uruchamia jedno `asyncio.gather(..., return_exceptions=True)`;
- każde źródło ma własny limit czasu przez `asyncio.wait_for(..., timeout=timeout)`;
- nazwy źródeł, które przekroczyły limit albo zgłosiły wyjątek, trafiają do `failed_sources`, a
  zadania z pozostałych do `quests`;
- `elapsed` to czas całego wywołania zmierzony przez `time.monotonic`.

Instrukcja zawiera też rozwijaną podpowiedź z kodem całej funkcji.

**Rezultat:** na starcie skrypt potwierdza pola `AggregateResult` i zgłasza, że funkcja nie jest
zaimplementowana. Po uzupełnieniu z limitem 5,0 s wszystkie źródła się udają, a z limitem 0,15 s
do `failed_sources` trafia tylko najwolniejsze źródło, `royal`.

**Sprawdź się:**
`uv run python level_7_concurrency_and_background_work/projects/01_async_quest_aggregator/check.py`.
Skrypt sprawdza:

- że `AggregateResult` jest klasą danych z polami `quests`, `failed_sources` i `elapsed`;
- że z limitem 5,0 s żadne źródło nie zawodzi, a zadań jest co najmniej trzy;
- że z limitem 0,15 s źródło `royal` jest w `failed_sources`, a `guild` nie i ma zadania;
- że po podmianie źródeł na trzy testowe, każde po 0,15 s, całe wywołanie trwa krócej niż 0,3 s;
- że w funkcji `aggregate_all_quests` jest wywołanie `gather`.

Tabela w instrukcji podaje dla pomiaru czasu próg 0,4 s, a skrypt używa progu 0,3 s dla źródeł
testowych. Skrypt nie sprawdza wartości `elapsed` ani wyniku źródła `village` przy krótkim limicie.
W kontroli przechodziła funkcja, która zawsze zwracała `elapsed` równe 0. Bez
`return_exceptions=True` skrypt kończył się wyjątkiem z pełnym śladem wywołań zamiast krótkiego
komunikatu.

## Oczekiwane rezultaty

- `check.py` misji 01 i 02 i projektu Async Quest Aggregator kończy się komunikatem o ukończeniu.
- Zmierzony czas pokazuje, że blokująca symulacja trwa tym dłużej, im więcej jest walk.
- Funkcje asyncio pobierają dane współbieżnie, a źródło, które przekroczy limit czasu, nie
  zatrzymuje pozostałych.

## Wskazówki

- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. Jeśli
  nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań na tej stronie.
- Następny etap poziomu 7 opisuje [zestaw 15](world-2-background-jobs.md).
