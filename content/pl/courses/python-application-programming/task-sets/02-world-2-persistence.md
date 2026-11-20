---
title: "Zapis i odczyt stanu gry"
summary: "Drugi etap poziomu 3 kursu Python RPG Questbook (World 2: Persistence): dwie misje o zapisie gry w pliku JSON z numerem wersji schematu i o wzorcu repozytorium oraz projekt Save Slot Manager, który zamyka ten etap."
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
  misja-04:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/missions/04_save_and_load_game_json/README.md
        lang: en
        label: "Instrukcja: Mission 04 — Save and Load Game JSON"
  misja-05:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/missions/05_repository_pattern/README.md
        lang: en
        label: "Instrukcja: Mission 05 — Repository Pattern"
  save-slot-manager:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/projects/02_save_slot_manager/README.md
        lang: en
        label: "Instrukcja: Project 02 — Save Slot Manager"
---
Ten zestaw obejmuje drugi etap poziomu 3 kursu Python RPG Questbook, „World 2: Persistence”. Uczysz
się w nim zapisywać i wczytywać stan gry tak, żeby dane były sprawdzane także w drodze do pliku.
Najpierw zapisujesz bohatera w pliku JSON z numerem wersji schematu. Potem ukrywasz zapis za wspólnym
interfejsem, czyli stosujesz wzorzec repozytorium. Pierwsze dwa zadania to misje 04 i 05. Trzecie to
projekt Save Slot Manager, który według mapy kursu zamyka ten etap. Instrukcje, kod i komunikaty
skryptów sprawdzających są po angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Zestaw jest dalszym ciągiem [zestawu 1](world-1-trusted-data.md). Instalację repozytorium, budowę
misji i miejsce wpisywania poleceń opisuje jego część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu). Jeśli repozytorium
jest już zainstalowane, nie potrzebujesz niczego więcej: Pydantic instaluje się razem z innymi
zależnościami.

**Co wynosisz z zestawu 1.** Misje korzystają z tego, co poznajesz w zestawie 1: modeli Pydantic
(`BaseModel`, `Field`, `ValidationError`) i podziału na model walidujący dane na granicy oraz klasę
danych używaną w grze. Instrukcja projektu podaje „Requires: Level 3, Missions 01–05”, czyli zakłada
znajomość także misji 01–03.

**Pliki.** Nie potrzebujesz plików ani wyników z zestawu 1 ani z wcześniejszych misji tego zestawu.
Każde zadanie ma własny `task.py` z gotowym punktem wyjścia. Misja 05 dostaje gotowy model zapisu z
misji 04, a projekt ma własny, inny model zapisu.

**Kod tylko do przeczytania.** Części „Game problem” instrukcji misji 04 i 05 pokazują fragmenty
kodu startowego poziomu 3,
[`starter_raw_rpg/main.py`](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_3_validation_and_persistence/starter_raw_rpg/main.py):
funkcje `save_game()` i `load_game()`, które zapisują zwykły słownik bez wersji schematu, oraz grę,
która wywołuje je bezpośrednio. Komentarz na początku pliku opisuje te problemy jako „Smell 2 (M04)”
i „Smell 3 (M05)”. Tego kodu nie edytujesz.

**Dane.** Misje 04 i 05 zapisują bohatera, czyli obiekt klasy danych `Hero` z polami `name`,
`hero_class`, `hp`, `max_hp`, `atk`, `def_`, `potions`, `gold`, `wins` i `losses`. Plik JSON
zawiera te pola i dodatkowe pole `schema_version`. Projekt ma prostszy model zapisu: `slot` (od 1 do
3), `hero_name`, `hero_hp`, `level`, `gold` i `schema_version`.

**Polecenia.** Polecenia misji wpisujesz w katalogu głównym repozytorium, tak jak w zestawie 1.
Sprawdzenie projektu instrukcja uruchamia z katalogu projektu.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`, który sprawdza Twój kod z `task.py` na własnych przykładach w
plikach tymczasowych. Gdy wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje
postęp lokalnie. Gdy coś się nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Pozostałe elementy sprawdzasz samodzielnie: uruchamiasz `task.py` i porównujesz
wynik z instrukcją. Części instrukcji „Break it on purpose” i „Fix it”, zadania poboczne („Side
quest”) i lista „Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO` i komunikaty
skryptów `check.py`.

## Zadania

### Save and Load Game JSON: zapis gry z wersją schematu {#misja-04}

**Cel:** zastąpić zapis i odczyt zwykłego słownika modelem Pydantic `SaveGameModel` z polem
`schema_version`. Dane mają być sprawdzane w obu kierunkach, a plik zapisany w innej wersji ma dawać
czytelny błąd zamiast awarii w konstruktorze `Hero`.

**Zakres pracy:** w `level_3_validation_and_persistence/missions/04_save_and_load_game_json/task.py`
klasy `HeroClass` i `Hero` są gotowe, a `SaveGameModel` ma na razie tylko pole `schema_version`.
Według instrukcji:

- dodaj do `SaveGameModel` wszystkie pola bohatera; `hero_class` przechowuj jako napis
  (`hero.hero_class.value`), a ograniczenia pól, na przykład `hp` co najmniej 0 i `max_hp` większe
  od 0, podaje komentarz `TODO`;
- zaimplementuj `to_hero()` i `from_hero(hero)`, które zamieniają model na obiekt `Hero` i odwrotnie;
- zaimplementuj `save_game(hero, path)`, która zapisuje wynik `model_dump_json(indent=2)` do pliku i
  w razie potrzeby tworzy jego katalog;
- zaimplementuj `load_game(path)`, która zwraca `None`, gdy pliku nie ma, zgłasza `ValueError`, gdy
  `schema_version` różni się od `CURRENT_SCHEMA_VERSION`, a w pozostałych przypadkach zwraca obiekt
  `Hero`. Komentarz `TODO` dodaje, że błąd walidacji też ma się kończyć `ValueError` z opisem.

**Rezultat:** uruchomiony `task.py` zapisuje bohatera o imieniu Ada do pliku
`saves/save_game.json` w katalogu misji i wypisuje jego zawartość: `"schema_version": 1` i wszystkie pola bohatera. Potem
wczytuje plik i wypisuje „Loaded: Ada (warrior), HP=100, gold=55”. Zanim uzupełnisz kod, wypisuje
tylko przypomnienie, co zostało do zrobienia.

**Sprawdź się:**
`uv run python level_3_validation_and_persistence/missions/04_save_and_load_game_json/check.py`.
Skrypt zapisuje i wczytuje bohatera w katalogu tymczasowym i sprawdza:

- że plik powstaje i zawiera `schema_version` równe 1;
- że wczytany obiekt jest typu `Hero` i ma wszystkie wartości pierwotnego bohatera, także klasę
  `WARRIOR`;
- że dla nieistniejącego pliku `load_game` zwraca `None`;
- że przy `schema_version` równym 99 `load_game` zgłasza `ValueError`.

Nie sprawdza ograniczeń pól modelu ani zamiany błędu walidacji, na przykład napisu w `hp`, na
`ValueError`. Nie sprawdza też tworzenia brakującego katalogu, bo katalog tymczasowy już istnieje.
Ten brak widać przy uruchomieniu `task.py`, dopóki w katalogu misji nie ma katalogu `saves/`.
Skrypt oczekuje `schema_version` równego 1. Jeśli po części „Fix it” zostawisz
`CURRENT_SCHEMA_VERSION = 2`, zgłosi błąd „schema_version should be 1, got 2”.

### Repository Pattern: zapis za wspólnym interfejsem {#misja-05}

**Cel:** ukryć zapis i odczyt za interfejsem `SaveRepository` (`Protocol`), tak aby kod gry nie
wiedział, czy bohater trafia do pliku JSON, czy tylko do pamięci.

**Zakres pracy:** w `level_3_validation_and_persistence/missions/05_repository_pattern/task.py`
gotowe są klasy `HeroClass` i `Hero`, pełny `SaveGameModel` z misji 04, interfejs `SaveRepository`
i funkcja `run_game_session(repo)`. Komentarz na początku pliku mówi też o zdefiniowaniu
interfejsu, ale jest on już gotowy. Zaimplementuj:

- `JsonSaveRepository.save(hero)` i `JsonSaveRepository.load()`: zapis modelu do pliku `self.path` i
  odczyt z kontrolą `schema_version`, z wynikiem `None`, gdy pliku nie ma;
- `InMemorySaveRepository.save(hero)` i `InMemorySaveRepository.load()`: przechowywanie bohatera w
  atrybucie `self._data`, bez zapisu na dysku.

**Rezultat:** uruchomiony `task.py` wykonuje jedną sesję gry z repozytorium JSON i dwie z
repozytorium w pamięci. Pierwsza sesja w pamięci tworzy nowego bohatera, druga go wczytuje, a złoto
rośnie z 10 do 20. Plik `saves/save_game.json` zostaje w katalogu misji, więc przy każdym kolejnym
uruchomieniu sesja JSON wczytuje zapisanego bohatera i dodaje mu 10 sztuk złota.

**Sprawdź się:**
`uv run python level_3_validation_and_persistence/missions/05_repository_pattern/check.py`. Skrypt
sprawdza:

- w katalogu tymczasowym, że `JsonSaveRepository.save` tworzy plik, a `load` zwraca bohatera z
  poprawnym imieniem i złotem, oraz że dla nieistniejącego pliku `load` zwraca `None`;
- że `InMemorySaveRepository.load` zwraca `None` przed zapisem, a po zapisie bohatera o poprawnym
  imieniu.

Nie sprawdza kontroli `schema_version` w `JsonSaveRepository.load`, pozostałych pól bohatera, na
przykład `wins`, ani tworzenia brakującego katalogu. Nie sprawdza też funkcji `run_game_session`,
więc nie wykrywa zmiany z części „Break it on purpose”. Te elementy porównaj z instrukcją,
uruchamiając `task.py`.

### Save Slot Manager: projekt zamykający etap {#save-slot-manager}

Mapa kursu i opis poziomu 3 umieszczają ten projekt na końcu etapu World 2 jako punkt kontrolny
(„Checkpoint”), a narzędzie postępu wymienia go w tym etapie. Opis kursu przedstawia projekty tego
rodzaju jako samodzielne ćwiczenia z pojęć poziomu. Instrukcja projektu wymaga misji 01–05.
Instrukcja misji 05 kieruje dalej od razu do misji 06, ale w mapie kursu przed nią jest właśnie ten
projekt. Z kolei instrukcja projektu kieruje na końcu do projektu 03, a w mapie kursu przed nim są
jeszcze misje 06 i 07.

**Cel:** zbudować system zapisu z trzema miejscami na zapis (slotami), obsługiwany przez dwa
wymienne repozytoria: plikowe JSON i w pamięci. Oba mają ten sam interfejs czterech metod.

**Zakres pracy:** w `level_3_validation_and_persistence/projects/02_save_slot_manager/task.py` model
`SaveGameModel` i interfejs `SaveRepository` z metodami `save`, `load`, `list_slots` i `delete` są
już zdefiniowane, choć tabela w instrukcji wymienia je wśród elementów do zrobienia. Model ma
`schema_version` równe 1 i pole `slot` od 1 do 3. Zastąp `NotImplementedError` własnym kodem w obu
klasach, także w ich metodach `__init__`:

- `JsonSaveRepository(directory)`: każdy slot w osobnym pliku `slot_{n}.json` w podanym katalogu;
- `InMemorySaveRepository()`: sloty w słowniku, bez zapisu na dysku.

Obie klasy mają spełniać ten sam kontrakt z instrukcji. `save(model)` zapisuje slot `model.slot`.
`load(slot)` zwraca model albo `None` dla pustego slotu i nigdy nie zgłasza `FileNotFoundError`.
`list_slots()` zwraca posortowaną listę zajętych slotów. `delete(slot)` usuwa slot, a dla pustego
slotu nic nie robi. Plik JSON zachowuje wszystkie pola, także `schema_version`.

**Rezultat:** projekt nie ma w `task.py` części uruchamiającej. Rezultat to dwie klasy, z którymi
przykład z instrukcji daje opisany wynik: po zapisie slotu 1 `load(1)` zwraca model z imieniem Ada,
`list_slots()` zwraca `[1]`, a po `delete(1)` wywołanie `load(1)` zwraca `None`.

**Sprawdź się:** polecenie z instrukcji projektu:

```bash
cd level_3_validation_and_persistence/projects/02_save_slot_manager
uv run python check.py
```

Skrypt działa też uruchomiony z katalogu głównego. Zanim uzupełnisz klasy, kończy się komunikatem
błędu Pythona `NotImplementedError` zamiast krótkiego opisu, czego brakuje. Sprawdza:

- że `SaveGameModel` jest modelem Pydantic z polem `schema_version` o domyślnej wartości 1;
- dla obu repozytoriów ten sam ciąg kroków: zapis i odczyt slotu 1 (imię, HP i `schema_version`),
  zapis slotu 2 i listę zawierającą sloty 1 i 2 w porządku rosnącym, wynik `None` dla pustego slotu
  3, usunięcie slotu 1 i jego brak na liście oraz usunięcie pustego slotu bez wyjątku;
- dla repozytorium JSON, że po zapisie slotu 3 w katalogu jest plik o nazwie zaczynającej się od
  `slot_3` i że zawiera pola `schema_version` i `hero_name`.

Nie sprawdza pól `level` i `gold` po odczycie, choć komunikat skryptu mówi o wszystkich polach. Nie
sprawdza dokładnej nazwy `slot_3.json` ani tworzenia brakującego katalogu. Nie sprawdza też, czy
nowy obiekt `JsonSaveRepository` dla tego samego katalogu widzi wcześniejsze zapisy: repozytorium,
które zapisuje pliki, ale odczytuje dane tylko z pamięci, przechodzi sprawdzenie. Porządek listy
skrypt sprawdza tylko dla slotów zapisanych w kolejności 1, 2. Te elementy porównaj samodzielnie z
kontraktem i regułami w instrukcji.

## Oczekiwane rezultaty

- `check.py` misji 04 i 05 oraz projektu Save Slot Manager kończy się komunikatem o ukończeniu.
- Pliki `task.py` misji 04 i 05 uruchamiają się bez błędów i wypisują wyniki opisane przy zadaniach.
- W projekcie Save Slot Manager oba repozytoria spełniają kontrakt z instrukcji, a przykład z
  instrukcji daje opisany wynik.

## Wskazówki

- Każde zadanie ma własne pliki. Misja 05 dostaje gotowy model z misji 04, a projekt ma własny model
  zapisu z numerem slotu.
- Pliki zapisu misji powstają w ich katalogach `saves/` i są wymienione w `.gitignore` repozytorium.
  Plik misji 05 zostaje między uruchomieniami. Po jego usunięciu sesja JSON znowu zaczyna od nowego
  bohatera.
- Części „Break it on purpose” i „Fix it” każą zmienić `schema_version` w zapisanym pliku i zobaczyć
  `ValueError` (misja 04) albo obejść interfejs w `run_game_session` i zobaczyć, że repozytorium w
  pamięci jest wtedy pomijane (misja 05).
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`.
  Jeśli nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym
  zestawie kieruj się kolejnością zadań powyżej.
