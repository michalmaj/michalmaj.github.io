---
title: "Testy API i dokumentacja OpenAPI"
summary: "Trzeci etap poziomu 6 kursu Python RPG Questbook (World 3: Quality and Polish): dwie misje o testach API z TestClient i podmianą zależności oraz o opisie API w dokumentacji OpenAPI, a także projekt RPG Battle API, który łączy elementy całego poziomu 6 i go zamyka."
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
  misja-07:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/missions/07_api_tests/README.md
        lang: en
        label: "Instrukcja: Mission 07 — API Tests with TestClient"
  misja-08:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/missions/08_openapi_and_api_polish/README.md
        lang: en
        label: "Instrukcja: Mission 08 — OpenAPI and API Polish"
  rpg-battle-api:
    materials:
      - repository: python-rpg-questbook
        path: level_6_api/projects/03_rpg_battle_api/README.md
        lang: en
        label: "Instrukcja: Boss Fight — RPG Battle API"
---
Ten zestaw obejmuje trzeci, ostatni etap poziomu 6 kursu Python RPG Questbook, „World 3: Quality
and Polish”. Najpierw piszesz testy API, które wysyłają żądania przez klienta testowego i podmieniają
zależności, a potem uzupełniasz opis API widoczny w `/docs`. Na końcu budujesz całą warstwę HTTP
gry: siedem endpointów, zapis sesji walki w plikach JSON i testy. Pierwsze dwa zadania to misje 07
i 08. Trzecie to projekt RPG Battle API, który mapa kursu nazywa walką z bossem („Boss Fight”) i
umieszcza na końcu poziomu 6. Instrukcje, kod, pliki danych i komunikaty skryptów sprawdzających są
po angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Instalację repozytorium opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1.
Uruchamianie serwera, stronę `/docs` i ostrzeżenie `StarletteDeprecationWarning` opisuje część
[„Przygotowanie do zestawu”](world-1-http-basics.md#przygotowanie-do-zestawu) zestawu 11, a pakiet
`task/` i polecenie `uv run uvicorn task.main:app --reload` część
[„Przygotowanie do zestawu”](world-2-structure-and-di.md#przygotowanie-do-zestawu) zestawu 12.

**Co wynosisz z wcześniejszych zestawów.** Ten etap korzysta z wiedzy z zestawów 11 i 12:
routerów, zależności `Depends()`, sesji walki i kodów statusu. Testy piszesz biblioteką pytest, z
fixture jak w [zestawie 9](world-2-testing.md). Plików ani wyników z wcześniejszych zestawów nie
potrzebujesz.

**Pliki.** Misje 07 i 08 mają w pakiecie `task/` gotową aplikację z routerami potworów, walk, sesji
i bohaterów, zależnościami i schematami, taką jak po misji 06. Misja 07 ma w
`task/tests/test_api.py` szkielety testów do uzupełnienia. Misja 08 ma w tym samym pliku gotowe
testy, których, według opisu na początku pliku, nie zmieniasz. Projekt ma własny pakiet `rpg/` z
gotową warstwą domeny, repozytoriów i usług, plikami warstwy HTTP do uzupełnienia, katalogiem
`data/` i katalogiem `tests/`. Kodu nie przenosisz między zadaniami.

**Polecenia.** Polecenia `check.py` i pytest wpisujesz w katalogu głównym repozytorium. Pakiet
projektu nazywa się `rpg`, tak samo jak pakiet z projektu Installable CLI Tool z poziomu 4,
zainstalowany w środowisku kursu. W kontroli testy, ruff i skrypt projektu korzystały z pakietu
`rpg/` tego projektu, zarówno z katalogu głównego, jak i z katalogu projektu.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`. Skrypt misji 07 uruchamia Twoje testy z gotową aplikacją, a
potem po kolei psuje w niej jedno zachowanie i sprawdza, czy testy to wykrywają. Po każdej próbie
przywraca oryginalny plik. Skrypty misji 08 i projektu wysyłają żądania przez klienta testowego, jak
w zestawach 11 i 12, i uruchamiają testy pytest. Skrypt misji 08 sprawdza też wybrane napisy w
plikach, a skrypt projektu uruchamia ruffa. Gdy wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje
postęp w pliku `level_6_api/.progress`. Gdy coś się nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy porównujesz z instrukcją samodzielnie. Części instrukcji „Try It
Yourself”, „Break It”, „Fix It” i „Side Quest” oraz lista „Checklist” służą samodzielnej pracy i
`check.py` ich nie sprawdza.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO`, pliki danych i
komunikaty skryptów `check.py`.

## Zadania

### API Tests: testy z TestClient i dependency_overrides {#misja-07}

**Cel:** napisać testy pytest całego API z klientem testowym FastAPI. Repozytorium sesji w testach
podmieniasz przez `app.dependency_overrides`, bez `unittest.mock` i bez `@patch`.

**Zakres pracy:** w `level_6_api/missions/07_api_tests/` jest pakiet `task/` z gotową aplikacją. W
`task/tests/test_api.py` jest gotowa fixture `client` i sześć funkcji testowych, które zgłaszają
`NotImplementedError`. Fixture podmienia `get_session_repo` na repozytorium w katalogu tymczasowym
`tmp_path`, a po teście czyści podmianę. Instrukcja każe jej nie zmieniać. Uzupełniasz sześć testów
opisanych w instrukcji i w komentarzach `TODO`: `/health`, listę potworów, walkę, walkę z nieznanym
potworem, zapis i odczyt sesji oraz brakującą sesję.

```bash
uv run pytest level_6_api/missions/07_api_tests/task/tests/test_api.py -v
```

**Rezultat:** na starcie wszystkie sześć testów kończy się błędem `NotImplementedError`. Po
uzupełnieniu sześć testów przechodzi, a podsumowanie pytest zawiera ostrzeżenie opisane w zestawie
11. Część „Break It” każe zmienić w teście `/health` oczekiwany kod na 201 i zobaczyć, że test
przestaje przechodzić.

**Asercja w teście walki.** Instrukcja i komentarz TODO 3 każą sprawdzić w teście walki kod 200 i
obecność pola `winner` w odpowiedzi. Taki test nie wykrywa zepsutej wersji aplikacji, w której
walkę zawsze wygrywa potwór. Skrypt kończy się wtedy błędem „❌ Your tests did not catch this bug:
POST /battle/simulate ignores the real outcome and always reports the monster winning” i
podpowiada, żeby sprawdzać dane odpowiedzi, a nie tylko kod statusu. Komunikat i komentarz w skrypcie
wyjaśniają, że dla danych z instrukcji, czyli klasy warrior przeciw Goblinowi, wygrana bohatera jest
pewna niezależnie od rzutów kośćmi. Test może więc sprawdzić wartość pola `winner`.

**Sprawdź się:** `uv run python level_6_api/missions/07_api_tests/check.py`. Skrypt sprawdza:

- że `test_api.py` zawiera napisy `TestClient` i `dependency_overrides`, nie zawiera
  `unittest.mock` ani `@patch` i ma co najmniej sześć funkcji `test_`;
- że testy przechodzą z gotową aplikacją;
- że testy nie przechodzą po każdej z sześciu zmian w aplikacji: inny status w `/health`, pusta
  lista potworów, walka zawsze wygrana przez potwora, nieznany potwór z kodem 200 zamiast 404,
  sesja, której endpoint nie zapisuje, i nieistniejąca sesja z kodem 200 zamiast 404.

Skrypt na czas każdej próby zmienia pliki aplikacji w `task/` i zakłada, że są niezmienione,
zgodnie z instrukcją. W kontroli po zmianie jednego wiersza w `task/routers/monsters.py` skrypt
kończył się komunikatem „❌ internal check error: mutant anchor not found”. Skrypt nie sprawdza nazw
testów ani dodatkowych testów z części „Try It Yourself”.

### OpenAPI and API Polish: opis API w /docs {#misja-08}

**Cel:** uzupełnić metadane aplikacji, czyli tytuł, opis i wersję, pogrupować endpointy tagami i
dodać krótkie opisy endpointów (`summary=`), tak żeby dokumentacja w `/docs` była czytelna.

**Zakres pracy:** w `level_6_api/missions/08_openapi_and_api_polish/` jest ta sama aplikacja co w
misji 07, z `FastAPI()` bez argumentów, czterema wywołaniami `include_router()` bez tagów i gotowymi
testami. Według kroków instrukcji:

1. W `task/main.py` podaj `title`, `description` i `version` z instrukcji.
2. Dodaj `tags=` do każdego wywołania `include_router()`. Nazwy tagów podaje instrukcja.
3. Dodaj `summary=` do co najmniej trzech endpointów w modułach routerów.
4. Otwórz `/docs`.

Instrukcja uruchamia serwer poleceniem `fastapi dev` w katalogu misji. Po przejściu do niego
poleceniem `cd level_6_api/missions/08_openapi_and_api_polish`:

```bash
uv run fastapi dev task/main.py
```

To polecenie uruchamia serwer uvicorn pod tym samym adresem `http://127.0.0.1:8000`, ze
śledzeniem zmian plików w katalogu misji. Zatrzymujesz go klawiszami Ctrl+C.

**Rezultat:** na starcie skrypt zgłasza brak `title=` w `FastAPI()`. Po zmianach `/docs` pokazuje
tytuł, opis i wersję oraz endpointy w grupach odpowiadających tagom. `/openapi.json` ma opis w polu
`info.description`. Część „Break It” każe usunąć `description=`, a skrypt wypisuje wtedy komunikat
podany w instrukcji. Strona `/redoc` z części „Try It Yourself” to drugi widok tej samej
dokumentacji. Ona też wczytuje skrypty z internetu.

**Sprawdź się:** `uv run python level_6_api/missions/08_openapi_and_api_polish/check.py`. Skrypt
sprawdza:

- że `task/main.py` zawiera napisy `title=`, `description=` i `version=`;
- że co najmniej dwa niezakomentowane wiersze z `include_router` mają `tags=`;
- że moduły routerów mają łącznie co najmniej trzy niezakomentowane wiersze z `summary=`;
- że schemat z `/openapi.json` ma tagi i niepusty opis w `info.description`, a `/docs` zwraca 200;
- że gotowe testy w `task/tests/test_api.py` przechodzą.

Instrukcja każe dodać tagi do każdego routera, a skrypt wymaga dwóch. W kontroli przechodziła
aplikacja z tagami tylko przy dwóch routerach. Porównaj `/docs` z krokiem 2 instrukcji.

### RPG Battle API: kompletne API gry z testami {#rpg-battle-api}

Mapa kursu nazywa ten projekt walką z bossem („Boss Fight”) i umieszcza go na końcu etapu World 3,
czyli na końcu poziomu 6. Według mapy łączy osiem elementów z misji w przetestowane API z siedmioma
endpointami i zapisem sesji w plikach JSON. Instrukcja zakłada, że znasz elementy z misji 01–08.

**Cel:** zbudować całą warstwę HTTP gry nad gotową warstwą domeny, repozytoriów i usług: zależności,
aplikację, pięć routerów z siedmioma endpointami i osiem testów API.

**Zakres pracy:** w `level_6_api/projects/03_rpg_battle_api/` jest pakiet `rpg/` z gotowymi
modułami `domain.py`, `repositories.py` i `services.py` oraz gotowymi schematami w
`rpg/api/schemas.py`: `MonsterOut`, `BattleRequest`, `BattleResultOut` i `SessionCreated`. Komentarze
`TODO` są w `rpg/api/dependencies.py`, `rpg/api/main.py`, modułach w `rpg/api/routers/` i
`tests/test_api.py`. Według instrukcji:

1. W `rpg/api/dependencies.py` napisz trzy funkcje zależności. Katalog danych wyznacza
   `Path(__file__).parents[2] / "data"`.
2. W `rpg/api/main.py` utwórz aplikację z metadanymi i dołącz pięć routerów.
3. W `rpg/api/routers/` dodaj endpointy: `GET /health` z polami `status` i `version`,
   `GET /monsters`, `GET /heroes/classes`, `POST /battle/simulate` z 404 dla nieznanego potwora,
   `POST /sessions` z kodem 201, `GET /sessions/{id}` z 404 dla brakującej sesji i
   `GET /reports/{id}`, który zwraca raport walki w Markdown jako zwykły tekst.
4. W `tests/test_api.py` napisz osiem testów opisanych w komentarzach `TODO`, tylko z `TestClient`
   i `app.dependency_overrides`.

Instrukcja zaleca kolejność: najpierw przeczytać gotowe warstwy i schematy, potem napisać
zależności, `health.py` i kolejne routery, a testy na końcu albo równolegle z routerami.

**Pola potwora.** Schemat `MonsterOut` projektu ma pole `defense`, a klasa domeny `Monster` pole
`def_`. Przykład w komentarzu `TODO` w `routers/monsters.py` zwraca obiekty domeny bez zmian. W
kontroli taki endpoint zwracał kod 500, bo odpowiedź nie pasowała do `MonsterOut`, a skrypt kończył
się błędem „❌ GET /monsters returned 500”. Przepisanie pól z klasy domeny do schematu pokazuje
zadanie 5 misji 06 z [zestawu 12](world-2-structure-and-di.md#misja-06).

```bash
uv run pytest level_6_api/projects/03_rpg_battle_api/tests/test_api.py -v
uv run ruff check level_6_api/projects/03_rpg_battle_api/rpg/api/
```

Instrukcja podaje te polecenia w katalogu projektu: `uv run pytest tests/test_api.py -v` i
`uv run ruff check rpg/api/`. W kontroli obie formy dawały ten sam wynik, a ruff korzystał z
konfiguracji z `pyproject.toml` repozytorium, tak jak skrypt projektu.

Instrukcja nie podaje polecenia, które uruchamia serwer tego projektu. Wzór z zestawu 12 działa w
katalogu projektu z modułem `rpg.api.main`. Po przejściu do katalogu projektu poleceniem
`cd level_6_api/projects/03_rpg_battle_api`:

```bash
uv run uvicorn rpg.api.main:app --reload
```

Wywołanie `POST /sessions` na działającym serwerze zapisuje plik sesji w katalogu `data/sessions/`
projektu. `git status` pokazuje ten plik jako nieśledzony.

**Rezultat:** na starcie skrypt zgłasza „❌ GET /health returned 404”, bo aplikacja nie ma jeszcze
routerów. Po wykonaniu wszystkich kroków skrypt przechodzi kolejne sprawdzenia, a pytest uruchamia
osiem testów API. Raport z `GET /reports/{id}` zaczyna się od nagłówka „## Battle Report” i ma typ
`text/plain`.

**Sprawdź się:** `uv run python level_6_api/projects/03_rpg_battle_api/check.py`. Instrukcja podaje
to polecenie w tej samej postaci, z katalogu głównego. Skrypt podmienia repozytorium sesji na
katalog tymczasowy i sprawdza:

- że `GET /health`, `GET /monsters` i `GET /heroes/classes` zwracają 200, a obie listy nie są
  puste;
- że walka z danymi `{"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"}`
  zwraca 200 i pole `winner`, a nieznana klasa bohatera daje 422;
- że `POST /sessions` zwraca 201 i `session_id`, odczyt tej sesji 200, a nieistniejąca sesja 404;
- że raport tej sesji ma typ `text/plain` i zawiera `##`;
- że polecenie `pytest tests/test_api.py` w katalogu projektu kończy się kodem 0;
- że `ruff check` z konfiguracją repozytorium nie zgłasza błędów w `rpg/api/`.

Tabela sprawdzeń w instrukcji nie wymienia kodu 422 ani typu `text/plain`. Komentarz `TODO` w
`routers/sessions.py` podpowiada `PlainTextResponse` dla raportu.

Skrypt nie sprawdza treści testów: wystarczy, że pytest kończy się kodem 0. W kontroli przechodził
plik z jednym pustym testem. Nie sprawdza też pola `version` w `/health`, kodu 404 dla nieznanego
potwora w walce i dla brakującego raportu ani katalogu, w którym działający serwer zapisuje sesje. W
kontroli przechodziła zależność, która wskazywała nieistniejący katalog. ruff sprawdza tylko
`rpg/api/`, a nie testy. Testy porównaj z komentarzami `TODO` w `tests/test_api.py`, a endpointy z
tabelą w instrukcji.

## Oczekiwane rezultaty

- `check.py` misji 07 i 08 i projektu RPG Battle API kończy się komunikatem o ukończeniu.
- Testy misji 07 przechodzą z gotową aplikacją i wykrywają sześć zepsutych zachowań. `/docs` misji
  08 pokazuje metadane, tagi i opisy endpointów.
- Projekt ma siedem endpointów, zapis sesji w plikach JSON, raport w Markdown i osiem testów API, a
  ruff nie zgłasza błędów w `rpg/api/`.

## Wskazówki

- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`. W tym
  zestawie kieruj się kolejnością zadań na tej stronie.
- Po poziomie 6 mapa kursu przechodzi do poziomu 7, „Concurrency and Background Work”.
