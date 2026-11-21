---
title: "Podstawy HTTP: pierwsze API w FastAPI"
summary: "Pierwszy etap poziomu 6 kursu Python RPG Questbook (World 1: HTTP Basics): trzy misje o pierwszej aplikacji FastAPI, schematach Pydantic dla żądań i odpowiedzi oraz endpointach, które przekazują pracę warstwie usług, a także projekt Battle Preview API, który zamyka ten etap."
status: published
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu: instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: level_6_api/README.md
    lang: en
    label: "Poziom 6 — API Interface with FastAPI: założenia, misje i projekty"
  - repository: python-rpg-questbook
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: podział poziomu 6 na etapy (World 1–3)"
  - repository: python-rpg-questbook
    path: level_6_api/starter_service_ready_rpg/README.md
    lang: en
    label: "Kod startowy poziomu 6: Service-Ready RPG"
tasks:
  misja-01:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/missions/01_first_fastapi_app/README.md
        lang: en
        label: "Instrukcja: Mission 01 — First FastAPI App"
  misja-02:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/missions/02_request_response_schemas/README.md
        lang: en
        label: "Instrukcja: Mission 02 — Request/Response Schemas"
  misja-03:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/missions/03_routes_call_services/README.md
        lang: en
        label: "Instrukcja: Mission 03 — Routes Call Services"
  battle-preview-api:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/projects/01_battle_preview_api/README.md
        lang: en
        label: "Instrukcja: Project 01 — Battle Preview API"
---
Ten zestaw obejmuje pierwszy etap poziomu 6 kursu Python RPG Questbook, „World 1: HTTP Basics”.
Poziom 6 udostępnia działający silnik gry przez HTTP. Zamiast wpisywać polecenia w terminalu, klient
wysyła żądania do API zbudowanego biblioteką FastAPI i dostaje odpowiedzi w formacie JSON. W tym
etapie tworzysz pierwszą aplikację FastAPI, opisujesz dane wejściowe i wyjściowe schematami Pydantic
i przenosisz logikę walki z endpointu do warstwy usług. Pierwsze trzy zadania to misje 01–03.
Czwarte to projekt Battle Preview API, który mapa kursu nazywa punktem kontrolnym („Checkpoint”) i
umieszcza na końcu tego etapu. Instrukcje, kod, pliki danych i komunikaty skryptów sprawdzających są
po angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1. FastAPI
z serwerem uvicorn oraz biblioteka httpx, z której korzysta klient testowy FastAPI, są w
zależnościach kursu w pliku `pyproject.toml` repozytorium (`fastapi[standard]` i `httpx`). Instaluje
je polecenie `uv sync` z przygotowania do zestawu 1, więc nie musisz ich dodawać.

**Co wynosisz z wcześniejszych zestawów.** Opis poziomu 6 zakłada ukończony poziom 5, opisany w
zestawach 8–10. Kod gry w zadaniach jest gotowy, więc własnego kodu z wcześniejszych poziomów nie
potrzebujesz. Przyda się znajomość modeli Pydantic z [zestawu 1](world-1-trusted-data.md), bo z nich
budujesz schematy żądań i odpowiedzi, oraz klas danych (`@dataclass`), z których zbudowane są
obiekty gry.

**Pliki.** Każda misja ma własny `task.py`, skrypt `check.py`, katalog `data/` z plikiem
`monsters.json` i własną kopię pakietu `rpg/` z warstwą domeny, repozytoriów i usług. Ta kopia jest
taka sama jak w kodzie startowym poziomu. Kolejne misje zaczynają od gotowego wyniku poprzedniej:
`task.py` misji 02 ma już aplikację i endpointy z misji 01, a `task.py` misji 03 ma już schematy z
misji 02. Nie przenosisz więc kodu między misjami. Projekt ma własny `task.py` z wbudowanym
katalogiem potworów i własnymi regułami walki, bez pakietu `rpg/`.

**Kod startowy.** Poziom 6 ma przygotowaną wersję gry z warstwą usług,
`starter_service_ready_rpg/`. Jego opis mówi, że z tych plików korzysta API budowane w misjach, a w
czasie misji ich nie zmieniasz. Opis poziomu każe najpierw uruchomić demonstrację i testy. Z
katalogu głównego repozytorium:

```bash
uv run python level_6_api/starter_service_ready_rpg/main.py
uv run pytest level_6_api/starter_service_ready_rpg/tests -q
```

Pierwsze polecenie wypisuje listę potworów i wynik jednej walki. Drugie uruchamia dziesięć testów.
Według opisu startera wszystkie mają przechodzić przed misją 01.

**Polecenia i katalog roboczy.** Polecenia `check.py` i pytest na tej stronie wpisujesz w katalogu
głównym repozytorium, jak w poprzednich zestawach. Katalogi zadań poziomu 6 nie mają własnego
`pyproject.toml`, więc `uv run` korzysta ze środowiska repozytorium także w katalogu zadania.
Polecenie `uv run python check.py` z instrukcji, wpisane w katalogu zadania, też działa.

**Serwer lokalny.** Instrukcje każą uruchomić aplikację serwerem uvicorn i obejrzeć ją w
przeglądarce. Serwer uruchamiasz w katalogu zadania, bo napis `task:app` wskazuje obiekt `app` w
pliku `task.py` z bieżącego katalogu. Serwer zajmuje terminal do chwili zatrzymania, więc uruchom go
w osobnym oknie terminala. Dla misji 01:

```bash
cd level_6_api/missions/01_first_fastapi_app
uv run uvicorn task:app --reload
```

Serwer działa pod adresem `http://127.0.0.1:8000`, dostępnym tylko z Twojego komputera.
Zatrzymujesz go klawiszami Ctrl+C. Opcja `--reload` każe mu śledzić zmiany plików w katalogu
zadania i wczytywać kod ponownie. Jeśli po zapisaniu zmian odpowiedzi się nie zmieniają, zatrzymaj
serwer i uruchom go jeszcze raz. Wszystkie zadania używają tego samego portu, więc zatrzymaj serwer
jednego zadania, zanim uruchomisz następny. W kontroli drugi serwer uruchomiony obok pierwszego
kończył się błędem „[Errno 48] Address already in use”. Instrukcje misji 02 i 03 w części „Try It
Yourself” podają polecenie `uvicorn task:app --reload` bez `uv run`. Takie polecenie działa tylko w
aktywnym środowisku `.venv`.

Strona `http://127.0.0.1:8000/docs` to interaktywna dokumentacja API. Przycisk „Try it out” wysyła
z niej żądania do działającego serwera. Ta strona wczytuje skrypty interfejsu z internetu, z adresu
`cdn.jsdelivr.net`, więc przeglądarka potrzebuje połączenia z siecią. Sam serwer API działa na Twoim
komputerze.

**Ostrzeżenie na początku wyniku.** Skrypty `check.py`, które korzystają z klienta testowego
FastAPI, wypisują na początku ostrzeżenie:

```text
StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
```

Pochodzi z biblioteki Starlette, na której opiera się FastAPI, w wersji zapisanej w pliku `uv.lock`
kursu. Klient testowy korzysta z pakietu httpx z zależności kursu, a ta wersja Starlette zaleca
zamiast niego nowszy pakiet httpx2. W kontroli z 21 listopada 2026 r. ostrzeżenie pojawiało się w
wynikach tych skryptów i jako „1 warning” w podsumowaniu pytest. Nie wpływało na wynik:
skrypty kończyły się komunikatem o ukończeniu, gdy zadanie było wykonane. Do wykonania zadań nie
musisz instalować dodatkowych pakietów.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypty tego zestawu nie uruchamiają serwera. Wysyłają żądania
do aplikacji przez klienta testowego FastAPI (`TestClient`), który wywołuje ją w tym samym procesie,
bez otwierania portu. Sprawdzają kody statusu i wybrane pola odpowiedzi, a niektóre także napisy w
pliku `task.py`. Gdy wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp
w pliku `level_6_api/.progress`, który jest w `.gitignore` repozytorium. Gdy coś się nie zgadza,
wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. To, że serwer się uruchamia, a `/docs` pokazuje endpointy, nie oznacza jeszcze, że
API działa tak, jak opisuje instrukcja. Przejście skryptu też tego nie gwarantuje. Pozostałe
elementy porównujesz z instrukcją samodzielnie, na przykład wysyłając żądania z `/docs`. Części
instrukcji „Try It Yourself”, „Break It”, „Fix It” i „Side Quest” oraz lista „Checklist” służą
samodzielnej pracy i `check.py` ich nie sprawdza.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### First FastAPI App: pierwsza aplikacja i strona /docs {#misja-01}

**Cel:** utworzyć aplikację FastAPI z dwoma endpointami i obejrzeć dokumentację `/docs`, którą
FastAPI tworzy automatycznie.

**Zakres pracy:** w `level_6_api/missions/01_first_fastapi_app/` jest `task.py` z gotowym obiektem
usługi `_service` (klasa `BattleService` z pakietu `rpg/` misji) i komentarzami `TODO`. Według
kroków instrukcji:

1. Utwórz obiekt `app` klasy `FastAPI` z tytułem i wersją podanymi w instrukcji.
2. Dodaj endpoint `GET /health`, który zwraca `{"status": "ok"}`.
3. Dodaj endpoint `GET /monsters`, który zwraca listę nazw potworów (`list[str]`) z
   `_service.get_available_monsters()`.
4. Uruchom serwer i otwórz `/docs`.

```bash
cd level_6_api/missions/01_first_fastapi_app
uv run uvicorn task:app --reload
```

**Rezultat:** na starcie skrypt zgłasza, że nie może zaimportować `app` z `task.py`. Po wykonaniu
kroków `GET /health` zwraca `{"status":"ok"}`, a `GET /monsters` zwraca nazwy potworów z
`data/monsters.json`: Goblin, Orc i Dragon. Strona `/docs` pokazuje oba endpointy.

**Sprawdź się:** `uv run python level_6_api/missions/01_first_fastapi_app/check.py`. Skrypt
sprawdza:

- że `task.py` ma obiekt `app` klasy `FastAPI`;
- że `GET /health` zwraca kod 200 i JSON z polem `status`;
- że `GET /monsters` zwraca kod 200 i listę napisów z tymi samymi nazwami co w
  `data/monsters.json`.

Nie sprawdza wartości pola `status` ani tytułu i wersji aplikacji. W kontroli przechodziła aplikacja
bez tytułu i wersji oraz z innym napisem w polu `status`. Porównaj je z krokami 1 i 2 instrukcji.

### Request/Response Schemas: schematy Pydantic dla żądań i odpowiedzi {#misja-02}

**Cel:** opisać dane wejściowe i wyjściowe API modelami Pydantic, oddzielonymi od klas domeny gry,
i dodać endpoint symulacji walki.

**Zakres pracy:** w `level_6_api/missions/02_request_response_schemas/` jest `task.py` z aplikacją
i endpointami z misji 01 oraz sześcioma komentarzami `TODO`. Instrukcja podaje kod każdego kroku.
Według niej:

1. Zdefiniuj trzy schematy: `MonsterOut` ze statystykami potwora, `BattleRequest` z imieniem i
   klasą bohatera oraz nazwą potwora i `BattleResultOut` z wynikiem walki. Pola wymienia
   instrukcja.
2. Zmień `GET /monsters` tak, żeby zwracał listę obiektów `MonsterOut` i miał w dekoratorze
   `response_model=list[MonsterOut]`.
3. Dodaj `POST /battle/simulate`. Endpoint przyjmuje `BattleRequest`, tworzy bohatera funkcją
   `create_hero()`, przeprowadza walkę przez `_service.simulate()` i zwraca `BattleResultOut`. W
   dekoratorze ma `response_model=BattleResultOut`.

Serwer uruchamiasz w katalogu misji tak jak w misji 01:

```bash
cd level_6_api/missions/02_request_response_schemas
uv run uvicorn task:app --reload
```

**Rezultat:** na starcie skrypt zgłasza brak klasy `MonsterOut`. Po wykonaniu kroków `GET /monsters`
zwraca obiekty z polami `name`, `hp`, `atk`, `def_` i `gold`. `POST /battle/simulate` z przykładem
z instrukcji zwraca wynik walki z polami `winner`, `rounds` i `gold_earned`. Klasa bohatera spoza
listy, na przykład `"knight"` z części „Break It”, daje kod 422 z opisem błędu walidacji, zanim
wykona się kod endpointu.

**Sprawdź się:** `uv run python level_6_api/missions/02_request_response_schemas/check.py`. Skrypt
sprawdza:

- że `task.py` ma niezakomentowane definicje klas `MonsterOut`, `BattleRequest` i
  `BattleResultOut`;
- że `GET /monsters` zwraca kod 200 i niepustą listę obiektów z polem `name`;
- że dekoratory obu endpointów mają `response_model=`. Skrypt szuka tego napisu w tym samym wierszu
  co ścieżka `monsters` albo `simulate`;
- że `POST /battle/simulate` z danymi `{"hero_name": "Ada", "hero_class": "warrior",
  "monster_name": "Goblin"}` zwraca kod 200 i wszystkie pola `BattleResultOut`.

Nie sprawdza pozostałych pól `MonsterOut` ani odpowiedzi 422. W kontroli przechodził `MonsterOut` z
samym polem `name`. Pola porównaj z krokiem 2 instrukcji.

### Routes Call Services: endpoint przekazuje pracę usłudze {#misja-03}

**Cel:** przenieść logikę walki z endpointu do warstwy usług. Endpoint ma tylko przyjąć żądanie,
wywołać usługę i zwrócić odpowiedź.

**Zakres pracy:** w `level_6_api/missions/03_routes_call_services/` jest `task.py` ze schematami z
misji 02 i endpointem `POST /battle/simulate`, który sam przeprowadza walkę. Endpoint kopiuje
potwora, rzuca kośćmi i tworzy bohatera ze statystykami wpisanymi na sztywno. Według kroków
instrukcji:

1. Zmień importy: dodaj `dataclasses` i `create_hero`, usuń `copy` i `random`.
2. Zastąp ciało endpointu. Bohatera tworzy `create_hero()`, walkę przeprowadza
   `_service.simulate()`, a wynik zamieniasz na `BattleResultOut`. Błąd `ValueError` dla
   nieznanego potwora zamieniasz na `HTTPException` z kodem 404.

```bash
cd level_6_api/missions/03_routes_call_services
uv run uvicorn task:app --reload
```

**Rezultat:** na starcie skrypt zgłasza napis `random.randint` w `task.py`. Po zmianie endpoint
zwraca wynik walki dla każdej z trzech klas bohatera, ze statystykami z `create_hero()`. Nazwa
potwora, którego nie ma w danych, daje kod 404 z komunikatem z usługi. Według części „Break It” bez
bloku `try/except` ten sam przypadek kończy się kodem 500.

**Sprawdź się:** `uv run python level_6_api/missions/03_routes_call_services/check.py`. Skrypt
sprawdza:

- że niezakomentowane wiersze `task.py` nie zawierają napisów `random.randint` ani
  `copy.deepcopy`;
- że w `task.py` jest wywołanie `.simulate(` i że bohater powstaje przez `create_hero(` albo
  `Hero(`;
- że `POST /battle/simulate` z tymi samymi danymi co w misji 02 zwraca kod 200 i pole `winner`, a
  `GET /monsters` nadal zwraca kod 200.

Nie sprawdza odpowiedzi 404 dla nieznanego potwora, statystyk bohatera ani usunięcia importów. W
kontroli przechodził endpoint bez `try/except`, który dla nieznanego potwora zwracał 500, i endpoint
z bohaterem tworzonym przez `Hero(...)` ze statystykami wpisanymi na sztywno. Kod 404 sprawdź w
`/docs` nazwą potwora spoza danych, a pozostałe elementy porównaj z listą „Checklist”.

### Battle Preview API: trzy endpointy w jednym pliku {#battle-preview-api}

Mapa kursu nazywa ten projekt punktem kontrolnym („Checkpoint”) i umieszcza go na końcu etapu
World 1. Instrukcja wymaga ukończenia misji 01–03.

**Cel:** zbudować w jednym pliku aplikację z trzema endpointami: sprawdzeniem działania, podglądem
bohatera z wyliczoną oceną siły `power_rating` i symulacją walki z potworem z wbudowanego katalogu.
Bez `APIRouter` i bez `Depends()`, które pojawiają się w następnym etapie.

**Zakres pracy:** w `level_6_api/projects/01_battle_preview_api/` jest `task.py` z katalogiem trzech
potworów (`MONSTERS`), gotowymi schematami `HeroIn`, `HeroPreview`, `BattleRequest` i
`BattleResult` oraz trzema endpointami, które zgłaszają `NotImplementedError`. Uzupełniasz:

- `GET /health`, który zwraca `{"status": "ok"}`;
- `POST /heroes/preview`, który zwraca dane bohatera z `power_rating` według wzoru z instrukcji;
- `POST /battle/simulate`, który przeprowadza walkę rundami według reguły obrażeń z instrukcji i
  zwraca zwycięzcę, liczbę rund i pozostałe punkty życia bohatera.

Katalog potworów projektu ma inne statystyki niż pliki danych misji. Schemat `BattleRequest`
przyjmuje nazwę potwora tylko małymi literami: `"goblin"`, `"orc"` albo `"dragon"`. Inną wartość,
także `"Goblin"`, walidacja Pydantic odrzuca kodem 422, zanim wykona się kod endpointu. Instrukcja
wyjaśnia, czym ten przypadek różni się od kodu 404 dla zasobu, którego nie znaleziono.

```bash
cd level_6_api/projects/01_battle_preview_api
uv run uvicorn task:app --reload
```

Instrukcja podaje też polecenia curl, które przy działającym serwerze wysyłają żądania do
`/health` i `/heroes/preview`.

**Rezultat:** na starcie skrypt wypisuje „❌ GET /health → 500, expected 200”, bo endpoint zgłasza
`NotImplementedError`. Po uzupełnieniu bohater z przykładu instrukcji, z `"atk": 15` i `"def_": 5`,
ma `power_rating` równe 2.5, a `"hp": -1` daje kod 422.

**Sprawdź się:** `uv run python level_6_api/projects/01_battle_preview_api/check.py`. Skrypt
sprawdza:

- że `GET /health` zwraca kod 200;
- że podgląd bohatera z przykładu instrukcji zwraca kod 200 i `power_rating` równe 2.5, a podgląd z
  `"hp": -1` daje 422;
- że walka z `"goblin"` zwraca kod 200 i pola `winner`, `rounds` i `hero_hp_remaining`, a `winner`
  ma wartość `"hero"` albo `"monster"`;
- że `"Goblin"` i nazwa spoza katalogu dają 422;
- że w `task.py` nie ma nazwy `APIRouter`.

Nie sprawdza przebiegu walki: liczby rund ani pozostałych punktów życia. W kontroli przechodziła
symulacja, która zawsze zwracała wygraną bohatera po jednej rundzie. Nie sprawdza też treści
odpowiedzi `/health`. Wynik walki porównaj z regułami z instrukcji.

Gdy `task.py` ma błąd importu, skrypt wypisuje „❌ Cannot import:” z przyczyną i podpowiada
polecenie `uv add fastapi httpx`. Oba pakiety są już w zależnościach kursu, a w kontroli to
polecenie niczego nie zmieniało. Przyczynę błędu podaje pierwszy wiersz komunikatu.

## Oczekiwane rezultaty

- `check.py` misji 01–03 i projektu Battle Preview API kończy się komunikatem o ukończeniu.
- Aplikacje misji zwracają listę potworów i wynik walki przez schematy Pydantic, a endpoint walki
  tylko wywołuje usługę i dla nieznanego potwora zwraca 404.
- Projekt ma trzy endpointy w jednym pliku, odrzuca niepoprawne dane kodem 422 i liczy walkę według
  reguł z instrukcji.

## Wskazówki

- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. Jeśli
  nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań na tej stronie.
- Następny etap poziomu 6 opisuje [zestaw 12](world-2-structure-and-di.md).
