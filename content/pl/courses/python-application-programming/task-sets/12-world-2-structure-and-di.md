---
title: "Struktura API i wstrzykiwanie zależności"
summary: "Drugi etap poziomu 6 kursu Python RPG Questbook (World 2: Structure and DI): trzy misje o podziale API na routery, wstrzykiwaniu zależności przez Depends() oraz kodach statusu dla błędów, a także projekt Monster Catalog API, który zamyka ten etap."
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
tasks:
  misja-04:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/missions/04_api_routers/README.md
        lang: en
        label: "Instrukcja: Mission 04 — API Routers"
  misja-05:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/missions/05_dependencies_and_repositories/README.md
        lang: en
        label: "Instrukcja: Mission 05 — Dependencies and Repositories"
  misja-06:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/missions/06_api_errors_and_status_codes/README.md
        lang: en
        label: "Instrukcja: Mission 06 — API Errors and Status Codes"
  monster-catalog-api:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/projects/02_monster_catalog_api/README.md
        lang: en
        label: "Instrukcja: Project 02 — Monster Catalog API"
---
Ten zestaw obejmuje drugi etap poziomu 6 kursu Python RPG Questbook, „World 2: Structure and DI”.
Aplikacja z jednego pliku staje się pakietem. Endpointy trafiają do osobnych modułów z routerami,
obiekty usług i repozytoriów dostarcza mechanizm zależności FastAPI (`Depends()`), a błędy klienta
dostają właściwe kody statusu zamiast błędu serwera. Pierwsze trzy zadania to misje 04–06. Czwarte
to projekt Monster Catalog API, który mapa kursu nazywa punktem kontrolnym („Checkpoint”) i
umieszcza na końcu tego etapu. Instrukcje, kod, pliki danych i komunikaty skryptów sprawdzających są
po angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1.
Uruchamianie serwera, stronę `/docs` i ostrzeżenie
`StarletteDeprecationWarning` na początku wyników opisuje część
[„Przygotowanie do zestawu”](world-1-http-basics.md#przygotowanie-do-zestawu) zestawu 11.

**Co wynosisz z wcześniejszych zestawów.** Ten etap korzysta z wiedzy z
[zestawu 11](world-1-http-basics.md): endpointów, schematów Pydantic i warstwy usług. Plików ani
wyników z zestawu 11 nie potrzebujesz.

**Pliki.** W misjach 04–06 aplikacja jest pakietem `task/` w katalogu misji. Pakiet ma moduł
`task/main.py` z obiektem `app`, moduł `task/config.py` ze ścieżką do danych `DATA_DIR` i katalog
`task/rpg/` z tą samą warstwą domeny, repozytoriów i usług co w zestawie 11. Kolejne misje zaczynają
od gotowego wyniku poprzedniej: misja 05 ma routery z misji 04, a misja 06 ma `task/dependencies.py`
z misji 05. Nie przenosisz więc kodu między misjami. Projekt ma własny pakiet `task/` z
repozytorium potworów w pamięci, bez pliku danych.

**Polecenia.** Polecenia `check.py` wpisujesz w katalogu głównym repozytorium, tak jak w zestawie
11. Moduły pakietu importują się nawzajem z przedrostkiem `task.`, na przykład
`from task.config import DATA_DIR`. Serwer uruchamiasz w katalogu zadania, w osobnym oknie
terminala, i wskazujesz obiekt `app` w module `task.main`. Dla misji 04:

```bash
cd level_6_api/missions/04_api_routers
uv run uvicorn task.main:app --reload
```

Ten sam wzór działa w katalogach misji 05 i 06 i w katalogu projektu Monster Catalog API.

**Pliki sesji.** Misje 05 i 06 mają endpoint `POST /sessions`, który zapisuje wynik walki jako plik
JSON w katalogu `data/sessions/` misji. Gdy wywołasz go na działającym serwerze, na przykład z
`/docs`, plik zostaje w katalogu misji, a `git status` pokazuje go jako nieśledzony. Skrypty
`check.py` zapisują sesje w katalogu tymczasowym i nie zostawiają plików.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Tak jak w zestawie 11, skrypty nie uruchamiają serwera, tylko
wysyłają żądania do aplikacji przez klienta testowego FastAPI. Najpierw sprawdzają, czy wymagane
pliki istnieją i czy zawierają wybrane napisy, na przykład `include_router` w `task/main.py` albo
`Depends(` w modułach routerów. Potem sprawdzają kody statusu i wybrane pola odpowiedzi. Gdy
wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp w pliku
`level_6_api/.progress`. Gdy coś się nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy porównujesz z instrukcją samodzielnie, na przykład wysyłając
żądania z `/docs`. Części instrukcji „Try It Yourself”, „Break It”, „Fix It” i „Side Quest” oraz
lista „Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### API Routers: podział endpointów na moduły {#misja-04}

**Cel:** przenieść endpointy do osobnych modułów z obiektami `APIRouter` i dołączyć je do
aplikacji w `task/main.py`.

**Zakres pracy:** w `level_6_api/missions/04_api_routers/` jest pakiet `task/` z modułem `main.py`
(aplikacja i `GET /health`), modułem `config.py` i katalogiem `rpg/`. Według kroków instrukcji:

1. Utwórz pusty plik `task/routers/__init__.py`.
2. Utwórz `task/routers/monsters.py` z routerem i endpointem `GET /monsters` oraz
   `task/routers/battles.py` z routerem i endpointem `POST /battle/simulate`. Instrukcja podaje kod
   obu modułów, ze schematami z zestawu 11 i ze ścieżką `DATA_DIR` z `task.config`.
3. W `task/main.py` odkomentuj import routerów i dwa wywołania `app.include_router()`.

```bash
cd level_6_api/missions/04_api_routers
uv run uvicorn task.main:app --reload
```

**Rezultat:** na starcie skrypt zgłasza brak pliku `task/routers/__init__.py`. Po wykonaniu kroków
`/docs` pokazuje `GET /health`, `GET /monsters` i `POST /battle/simulate`, a `GET /monsters` zwraca
potwory Goblin, Orc i Dragon. Część „Break It” każe usunąć jedno wywołanie `include_router()`. Endpoint
tego routera zwraca wtedy 404, a skrypt zgłasza, że `include_router()` jest wywołane tylko raz.
Import `from config import DATA_DIR` bez przedrostka `task.` kończy się błędem
„No module named 'config'”.

**Sprawdź się:** `uv run python level_6_api/missions/04_api_routers/check.py`. Skrypt sprawdza:

- że istnieją `task/routers/__init__.py`, `task/routers/monsters.py` i `task/routers/battles.py`, a
  oba moduły routerów zawierają niezakomentowany napis `APIRouter`;
- że `task/main.py` ma co najmniej dwa niezakomentowane wiersze z `include_router`;
- że `GET /health`, `GET /monsters` i `POST /battle/simulate` z danymi `{"hero_name": "Ada",
  "hero_class": "warrior", "monster_name": "Goblin"}` zwracają kod 200, lista potworów nie jest
  pusta, a wynik walki ma pole `winner`.

Nie sprawdza pól potworów ani odpowiedzi 404 dla nieznanego potwora. Porównaj je z krokami 2 i 3
instrukcji.

### Dependencies and Repositories: zależności przez Depends() {#misja-05}

**Cel:** zastąpić obiekty usług tworzone w modułach routerów zależnościami FastAPI (`Depends()`) i
dodać endpointy zapisu i odczytu sesji walki.

**Zakres pracy:** w `level_6_api/missions/05_dependencies_and_repositories/` jest pakiet `task/` z
routerami `monsters.py` i `battles.py` z misji 04, w których obiekt `_service` powstaje przy
wczytaniu modułu, oraz modułem `routers/sessions.py` z komentarzami `TODO`. Instrukcja podaje kod
każdego kroku. Według niej:

1. Utwórz `task/dependencies.py` z trzema funkcjami: `get_monster_repo()`, `get_session_repo()` i
   `get_battle_service()`, która dostaje repozytorium potworów przez `Depends(get_monster_repo)`.
2. W `monsters.py` i `battles.py` usuń `_service` i dodaj usługę jako parametr endpointu z
   `Depends(get_battle_service)`.
3. W `sessions.py` dodaj `POST /sessions`, który zwraca kod 201 i `session_id`, oraz
   `GET /sessions/{session_id}`, który zwraca zapisany wynik walki albo 404.

```bash
cd level_6_api/missions/05_dependencies_and_repositories
uv run uvicorn task.main:app --reload
```

**Rezultat:** na starcie skrypt zgłasza brak pliku `task/dependencies.py`. Po wykonaniu kroków
`POST /sessions` z przykładem z instrukcji zwraca kod 201 i `session_id`.
`GET /sessions/{session_id}` z tym identyfikatorem zwraca wynik walki, a `GET /sessions/fake-id`
zwraca 404.

Część „Break It” podaje trzy próby. Pierwsza każe utworzyć `BattleService(...)` bezpośrednio w
endpoincie i mówi, że `check.py` nadal przejdzie. W kontroli skrypt kończył się wtedy błędem
„'BattleService(' found outside comments”, bo sprawdza, czy moduły routerów nie tworzą usług ani
repozytoriów same. Druga próba, bez pliku `task/dependencies.py`, daje komunikat podany w
instrukcji. Trzecia, z nieużywanym `Depends(get_session_repo)`, nie zmienia wyniku skryptu.

Część „Side Quest” proponuje parametr `sessions_dir` z wartością domyślną w `get_session_repo()`,
żeby testy mogły podmienić katalog sesji. W kontroli FastAPI potraktował ten parametr jako parametr
zapytania obu endpointów sesji. Pole `sessions_dir` pojawiło się w `/docs`, a żądanie
`POST /sessions?sessions_dir=…` zapisało plik sesji w katalogu wskazanym przez klienta. Misja 07
podmienia repozytorium sesji w testach przez `app.dependency_overrides`, bez takiego parametru.

**Sprawdź się:** `uv run python level_6_api/missions/05_dependencies_and_repositories/check.py`.
Skrypt sprawdza:

- że `task/dependencies.py` istnieje i zawiera nazwy `get_monster_repo`, `get_session_repo` i
  `get_battle_service`;
- że co najmniej jeden moduł w `task/routers/` ma niezakomentowane `Depends(`;
- że niezakomentowane wiersze `monsters.py`, `battles.py` i `sessions.py` nie zawierają
  `MonsterRepository(` ani `BattleService(`;
- że `GET /monsters` i `POST /battle/simulate` nadal zwracają kod 200;
- że z repozytorium sesji podmienionym na katalog tymczasowy `POST /sessions` zwraca 201 i
  `session_id`, odczyt tej sesji zwraca 200 i pole `winner`, a nieistniejąca sesja daje 404.

Nie sprawdza, czy z `Depends()` korzystają wszystkie endpointy: wystarczy jeden moduł. Z powodu
podmiany repozytorium nie sprawdza też zapisu do `data/sessions/`. Oba elementy porównaj z krokami
2 i 3 instrukcji.

### API Errors and Status Codes: kody statusu dla błędów {#misja-06}

**Cel:** zamienić błędy serwera (kod 500) na właściwe kody statusu z czytelnym komunikatem
`{"detail": "..."}` i dodać endpoint z listą klas bohatera.

**Zakres pracy:** w `level_6_api/missions/06_api_errors_and_status_codes/` jest pakiet `task/` z
`dependencies.py` z misji 05, wspólnymi schematami w `schemas.py` i routerami. Instrukcja dzieli
pracę na pięć zadań:

1. Schemat `ErrorOut` z polem `detail` w `task/schemas.py`. Plik startowy już go zawiera, razem z
   pozostałymi schematami.
2. W `routers/battles.py` zamień `ValueError` z `service.simulate()` na `HTTPException` z kodem
   404. Odpowiedź 404 opisz w dekoratorze przez `responses={404: {"model": ErrorOut}}`.
3. W `routers/heroes.py` dodaj `GET /heroes/classes` z listą klas bohatera z usługi.
4. Przeczytaj `routers/sessions.py`, w którym ten sam wzorzec jest już gotowy.
5. W `routers/monsters.py` popraw `GET /monsters/{name}`: dla nieznanej nazwy zwróć 404 zamiast
   błędu 500.

Schemat `MonsterOut` w tej misji ma pole `defense` zamiast `def_`. Instrukcja wyjaśnia, dlaczego
zmiana nazwy należy do granicy między schematem API a klasą domeny.

```bash
cd level_6_api/missions/06_api_errors_and_status_codes
uv run uvicorn task.main:app --reload
```

**Rezultat:** na starcie skrypt zgłasza „❌ Unknown monster should return 404, got 500”. Po
wykonaniu zadań `POST /battle/simulate` z `"FakeMonster"` zwraca 404, `GET /heroes/classes` zwraca
`["warrior","mage","rogue"]`, `GET /monsters/Goblin` zwraca potwora z polem `defense`, a
`GET /monsters/FakeMonster` zwraca 404. W `/openapi.json` endpoint `POST /battle/simulate` ma
opisaną odpowiedź 404 ze schematem `ErrorOut`.

Część „Break It” podaje trzy próby. Usunięcie `try/except` i kod 400 zamiast 404 dają błędy
skryptu opisane w instrukcji. Druga próba każe usunąć `task/schemas.py` i zdefiniować `ErrorOut` w
`battles.py`, a instrukcja odpowiada, że skrypt nadal przejdzie. W kontroli skrypt kończył się wtedy
błędem „Cannot import app from task.main: No module named 'task.schemas'”, bo schematy z tego pliku
importują także pozostałe moduły.

**Sprawdź się:** `uv run python level_6_api/missions/06_api_errors_and_status_codes/check.py`.
Skrypt sprawdza:

- że `task/schemas.py` albo któryś moduł routerów zawiera `class ErrorOut`;
- że któryś moduł routerów ma niezakomentowane `HTTPException`;
- że nieznany potwór w `POST /battle/simulate` daje 404, a Goblin 200;
- że nieistniejąca sesja daje 404;
- że `GET /heroes/classes` zwraca 200 i niepustą listę;
- że `GET /monsters/Goblin` zwraca 200 i pole `name`, a `GET /monsters/NonExistentMonster` daje
  404;
- że nieznana klasa bohatera daje 422.

Dwa pierwsze punkty są spełnione już na starcie: `ErrorOut` jest w `schemas.py`, a `HTTPException`
w gotowym `sessions.py`. Skrypt nie sprawdza opisu odpowiedzi 404 w dekoratorze (`responses=`). W
kontroli przechodził endpoint bez niego. Porównaj go z zadaniem 2 instrukcji i ze stroną `/docs`.

### Monster Catalog API: katalog potworów z routerem i zależnościami {#monster-catalog-api}

Mapa kursu nazywa ten projekt punktem kontrolnym („Checkpoint”) i umieszcza go na końcu etapu
World 2. Instrukcja wymaga ukończenia misji 04–06.

**Cel:** zbudować API katalogu potworów z trzema endpointami, w pakiecie z routerem, zależnością
`Depends()` i odpowiedzią 404 dla nieznanego potwora.

**Zakres pracy:** w `level_6_api/projects/02_monster_catalog_api/` jest pakiet `task/`. Instrukcja
oznacza jako gotowe moduły `main.py`, `schemas.py` (`MonsterOut` i `DifficultyOut`) oraz
`dependencies.py` z funkcją `get_monster_repo()`. Uzupełniasz:

- w `task/repository.py` klasę `InMemoryMonsterRepository`, czyli metody `list_all()` i
  `get_by_name()`, na danych z listy `_CATALOG` w tym samym pliku. `get_by_name()` ma nie
  rozróżniać wielkości liter;
- w `task/routers/monsters.py` trzy endpointy routera z przedrostkiem `/monsters`: listę potworów,
  jednego potwora po nazwie i ocenę trudności `easy`, `medium` albo `hard` według progów punktów
  życia z instrukcji. Dla nieznanej nazwy oba ostatnie zwracają 404.

Router ma korzystać z `Depends(get_monster_repo)` i nie może mieć słownika na poziomie modułu.

```bash
cd level_6_api/projects/02_monster_catalog_api
uv run uvicorn task.main:app --reload
```

Instrukcja podaje też polecenia curl, które przy działającym serwerze wysyłają żądania do trzech
endpointów.

**Rezultat:** na starcie skrypt wypisuje „❌ GET /monsters → 500, expected 200”, bo metody zgłaszają
`NotImplementedError`. Po uzupełnieniu `GET /monsters` zwraca cztery potwory z katalogu projektu,
`GET /monsters/Unknown` zwraca 404, Goblin ma trudność `easy`, a Dragon `hard`.

**Sprawdź się:** `uv run python level_6_api/projects/02_monster_catalog_api/check.py`. Skrypt
sprawdza:

- że `GET /monsters` zwraca 200 i te same potwory co lista `_CATALOG`, z nazwami i statystykami, bez
  względu na kolejność;
- że `GET /monsters/Goblin` zwraca 200 i Goblina, a `GET /monsters/Unknown` daje 404;
- że Goblin ma trudność `easy`, a Dragon `hard`;
- że `routers/monsters.py` używa nazw `APIRouter` i `Depends` i nie ma słownika na poziomie modułu.

Nie sprawdza ignorowania wielkości liter, trudności `medium` ani odpowiedzi 404 dla trudności
nieznanego potwora. W kontroli przechodziło repozytorium, które rozróżniało wielkość liter, ocena
bez poziomu `medium` i endpoint trudności, który dla nieznanej nazwy zwracał 500. Te zachowania
sprawdź w `/docs`, na przykład dla nazwy `goblin` i dla potwora `Troll`.

Gdy pakiet ma błąd importu, skrypt podpowiada polecenie `uv add fastapi httpx`, tak jak w projekcie
Battle Preview API z [zestawu 11](world-1-http-basics.md#battle-preview-api). Przyczynę podaje
pierwszy wiersz komunikatu.

## Oczekiwane rezultaty

- `check.py` misji 04–06 i projektu Monster Catalog API kończy się komunikatem o ukończeniu.
- Endpointy są w osobnych modułach routerów, usługi i repozytoria dostarcza `Depends()`, a sesje
  walki można zapisać i odczytać.
- Nieznany potwór i brakująca sesja dają kod 404 z polem `detail`, a niepoprawne dane wejściowe kod
  422.
- Projekt zwraca katalog potworów, pojedynczego potwora i ocenę trudności zgodnie z instrukcją.

## Wskazówki

- Pliki sesji zapisane przez działający serwer w `data/sessions/` misji 05 i 06 nie są potrzebne
  skryptom `check.py`.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. W tym
  zestawie kieruj się kolejnością zadań na tej stronie.
- Ostatni etap poziomu 6 opisuje [zestaw 13](world-3-quality-and-polish.md).
