---
title: "Walidacja danych zewnętrznych"
summary: "Pierwszy etap poziomu 3 kursu Python RPG Questbook (World 1: Trusted Data): trzy misje o sprawdzaniu danych z plików JSON, ręcznie i z Pydantic, oraz projekt Validated Bestiary, który zamyka ten etap."
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
  - repository: python-rpg-questbook
    path: level_3_validation_and_persistence/starter_raw_rpg/
    lang: en
    label: "Kod startowy poziomu 3: katalog starter_raw_rpg"
tasks:
  misja-01:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/missions/01_external_data_is_untrusted/README.md
        lang: en
        label: "Instrukcja: Mission 01 — External Data Is Untrusted"
  misja-02:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/missions/02_pydantic_monster_config/README.md
        lang: en
        label: "Instrukcja: Mission 02 — Pydantic Monster Config"
  misja-03:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/missions/03_load_game_catalogs/README.md
        lang: en
        label: "Instrukcja: Mission 03 — Load Game Catalogs"
  validated-bestiary:
    materials:
      - repository: python-rpg-questbook
        path: level_3_validation_and_persistence/projects/01_validated_bestiary/README.md
        lang: en
        label: "Instrukcja: Project 01 — Validated Bestiary"
---
Ten zestaw obejmuje pierwszy etap poziomu 3 kursu Python RPG Questbook, „World 1: Trusted Data”.
Uczysz się w nim sprawdzać dane z plików JSON, zanim trafią do gry: najpierw ręcznie, potem
modelami Pydantic, a na końcu zamieniasz je na obiekty używane w grze. Pierwsze trzy zadania to
misje 01–03. Czwarte to projekt Validated Bestiary, który według mapy kursu zamyka ten etap.
Instrukcje, kod, pliki danych i komunikaty skryptów sprawdzających są po angielsku. Ta strona
streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Questbook zakłada ukończony poziom 2. Kod poziomu 3 korzysta z tego, co tam omawiano: klas, klas
danych (`@dataclass`) i adnotacji typów. Jeśli te elementy są dla Ciebie nowe, możesz najpierw
przejść
[poziom 2](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_2_oop_and_design/README.md).
Do pracy w tym zestawie nie potrzebujesz natomiast żadnych plików ani wyników z poziomu 2: każda
misja i projekt mają własne pliki.

**Instalacja.** Potrzebujesz [uv](https://docs.astral.sh/uv/), a projekt wymaga Pythona 3.12 lub
nowszego. Pobierz repozytorium i zainstaluj zależności poleceniami z sekcji „Setup” w opisie
kursu. Zależności obejmują bibliotekę Pydantic, z której korzystają misje 02 i 03 oraz projekt.

```bash
git clone https://github.com/michalmaj/python-rpg-questbook.git
cd python-rpg-questbook
uv sync
```

**Kod startowy.** Poziom 3 ma przygotowaną wersję gry, `starter_raw_rpg/`. Jest uporządkowana
obiektowo, ale wczytuje i zapisuje dane bez żadnej walidacji. Komentarz na początku `main.py`
wymienia te problemy i wskazuje misje, które je naprawiają. Według opisu poziomu 3 nie edytujesz
tego kodu: każda misja pracuje we własnych plikach, a misja 07 korzysta z niego jako przykładu
konfiguracji. Opis zachęca, by zajrzeć do `main.py` na początku. Jeśli chcesz zobaczyć grę w
działaniu, uruchom ją z katalogu głównego repozytorium:

```bash
uv run python level_3_validation_and_persistence/starter_raw_rpg/main.py
```

Gra jest interaktywna i zapisuje stan oraz dziennik walk w katalogu `starter_raw_rpg/saves/`.

**Dane.** Misje czytają pliki JSON z obiektem `{"monsters": [...]}`, w którym każdy potwór ma pola
`name`, `hp`, `atk`, `def` i `gold`. Misja 03 czyta też `{"weapons": [...]}` z polami `name`,
`atk_bonus` i `price`. Projekt Validated Bestiary ma inny format: plik jest listą rekordów z polami
`name`, `hp`, `attack_type` i `gold`.

**Jak wygląda misja.** Każda misja ma katalog w `level_3_validation_and_persistence/missions/` z
instrukcją `README.md`, plikiem `task.py`, skryptem `check.py` i plikami danych JSON, jeśli są
potrzebne. Najpierw czytasz instrukcję, potem uzupełniasz `task.py` i go uruchamiasz, a na końcu
uruchamiasz `check.py`. Polecenia misji wpisujesz w katalogu głównym repozytorium. Sprawdzenie
projektu uruchamiasz, zgodnie z jego instrukcją, z katalogu projektu.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`, który sprawdza Twój kod z `task.py` na własnych przykładach:
zapisanych w skrypcie, w plikach misji albo w plikach tymczasowych. Gdy wszystko się zgadza,
skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się nie zgadza,
wypisuje, czego oczekiwał.

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

### External Data Is Untrusted: ręczna walidacja danych {#misja-01}

**Cel:** zobaczyć, co się dzieje, gdy gra wczytuje niesprawdzony plik JSON, i napisać ręczny
walidator, który wykrywa problemy.

**Zakres pracy:** w `level_3_validation_and_persistence/missions/01_external_data_is_untrusted/task.py`
najpierw uruchom gotową funkcję `naive_load()`. Zobacz, jak traktuje dane z `broken_monsters.json`:
pięć potworów, z których jeden jest poprawny, trzy mają błędne `hp`, a jeden ma dodatkowe pole.
Potem zaimplementuj `validate_monster(raw)`, która zwraca listę komunikatów o błędach albo pustą
listę. Instrukcja wymaga sprawdzenia pól `name` (tekst), `hp` (liczba całkowita większa od 0),
`atk` (co najmniej 1), `def` (co najmniej 0) i `gold` (co najmniej 0). Dodatkowe, nieznane pole nie
jest błędem.

**Rezultat:** uruchomiony `task.py` pokazuje, co robi naiwne wczytanie, a potem dla każdego
potwora z pliku wypisuje, czy jest poprawny, a jeśli nie, jakie ma błędy.

**Sprawdź się:**
`uv run python level_3_validation_and_persistence/missions/01_external_data_is_untrusted/check.py`.
Skrypt sprawdza na własnych przykładach, że poprawny potwór i potwór z dodatkowym polem nie dają
błędów. Sprawdza też, że błędy w `hp` (wartość ujemna, tekst, brak pola), w `name` (brak pola,
liczba), `atk` równe 0 i ujemne `gold` dają komunikat zawierający nazwę pola. Nie sprawdza reguł
dla `def`, typu i braku pól `atk` i `gold` ani zadania pobocznego. Te reguły porównaj samodzielnie
z instrukcją.

### Pydantic Monster Config: modele walidacyjne {#misja-02}

**Cel:** zastąpić ręczną walidację modelami Pydantic.

**Zakres pracy:** w `level_3_validation_and_persistence/missions/02_pydantic_monster_config/task.py`
zdefiniuj dwa modele:

- `MonsterConfig` z polami `name`, `hp` (większe od 0), `atk` (co najmniej 1), `def_` (co najmniej
  0, z aliasem `def` dla klucza w JSON) i `gold` (co najmniej 0) oraz ustawieniem
  `populate_by_name=True`;
- `WeaponConfig` z polami `name`, `atk_bonus` (co najmniej 0) i `price` (co najmniej 0).

Potem odkomentuj import i wiersze w `main()`, żeby zobaczyć walidację na potworach z
`monsters.json` i na błędnych przykładach.

**Rezultat:** uruchomiony `task.py` pokazuje cztery poprawne potwory z `monsters.json` i błędy
walidacji dla trzech złych przykładów zapisanych w `task.py`.

**Sprawdź się:**
`uv run python level_3_validation_and_persistence/missions/02_pydantic_monster_config/check.py`.
Skrypt sprawdza oba modele na przykładach zapisanych w samym skrypcie. Dla potwora: wczytanie
poprawnego wpisu przez klucz `def` z wartościami `hp`, `atk`, `def_` i `gold` oraz odrzucenie `hp`
równego -50 i 0, braku `hp`, `atk` równego 0 i ujemnego `gold`. Dla broni: wartości `atk_bonus` i
`price` poprawnego wpisu oraz odrzucenie ujemnych `atk_bonus` i `price` i braku `name`. Nie sprawdza `populate_by_name`, ujemnego `def`,
odkomentowania `main()` ani zadania pobocznego.

### Load Game Catalogs: od pliku JSON do obiektów gry {#misja-03}

**Cel:** połączyć cały przepływ: plik JSON, model Pydantic i klasa danych używana w grze. Logika
gry ma działać na klasach danych i nie znać Pydantic.

**Zakres pracy:** w `level_3_validation_and_persistence/missions/03_load_game_catalogs/task.py`
klasy danych `Monster` i `Weapon` oraz modele `MonsterConfig` i `WeaponConfig` są już gotowe.
Uzupełnij metody `to_domain()` obu modeli oraz funkcje `load_monsters(path)` i
`load_weapons(path)`. Funkcje czytają `monsters.json` i `weapons.json` z katalogu misji, walidują
każdy wpis, pomijają błędne z ostrzeżeniem i zwracają listę obiektów gry.

**Rezultat:** uruchomiony `task.py` wypisuje cztery potwory i trzy bronie. Zanim uzupełnisz
funkcje, wypisuje tylko przypomnienie, co zostało do zrobienia.

**Sprawdź się:**
`uv run python level_3_validation_and_persistence/missions/03_load_game_catalogs/check.py`.
Skrypt sprawdza, że:

- `to_domain()` zwraca obiekt `Monster` z poprawnymi `name`, `hp` i `def_` oraz obiekt `Weapon`;
- funkcje wczytują cztery potwory i trzy bronie z plików misji;
- z pliku tymczasowego z jednym błędnym wpisem funkcje zwracają dwa pozostałe wpisy, nie zgłaszając
  wyjątku.

Nie sprawdza, czy przy pominiętym wpisie wypisujesz ostrzeżenie, wartości broni po konwersji ani
zadania pobocznego (`hero_classes.json`).

### Validated Bestiary: projekt zamykający etap {#validated-bestiary}

Mapa kursu umieszcza ten projekt na końcu etapu World 1 jako punkt kontrolny („Checkpoint”), a
narzędzie postępu wymienia go w tym etapie. Jego instrukcja wymaga misji 01–03. Instrukcja misji 03 kieruje dalej od razu do
misji 04, ale w mapie kursu przed nią jest właśnie ten projekt.

**Cel:** zbudować wczytywanie katalogu potworów, które waliduje każdy rekord i zbiera błędy, zamiast
przerywać pracę na pierwszym złym rekordzie.

**Zakres pracy:** w `level_3_validation_and_persistence/projects/01_validated_bestiary/task.py`
model `MonsterModel` i klasa danych `MonsterDomain` są już zdefiniowane, choć tabela w instrukcji
wymienia je wśród elementów do zrobienia. Model przyjmuje tylko niepustą nazwę, `hp` większe od 0,
`gold` co najmniej 0 i `attack_type` równe `melee`, `ranged` albo `magic`. Zaimplementuj:

- `to_domain(model)`, która zamienia `MonsterModel` na `MonsterDomain`;
- `load_bestiary(path)`, która czyta plik JSON z listą rekordów i zwraca parę: listę poprawnych
  potworów i listę czytelnych komunikatów o odrzuconych rekordach. Błędny rekord nie może
  zatrzymać wczytywania pozostałych.

Plik `data/monsters.json` (osiem rekordów: cztery poprawne i cztery błędne) służy do własnych
prób.

**Rezultat:** dla `data/monsters.json` funkcja `load_bestiary` zwraca cztery potwory i cztery
komunikaty o błędach, jak w przykładzie w instrukcji.

**Sprawdź się:** polecenie z instrukcji projektu:

```bash
cd level_3_validation_and_persistence/projects/01_validated_bestiary
uv run python check.py
```

Skrypt sprawdza:

- że `MonsterModel` jest modelem Pydantic z polami `name`, `hp`, `attack_type` i `gold`;
- że `load_bestiary` zwraca parę list;
- że `to_domain()` zwraca zwykły obiekt (nie model Pydantic) z czterema atrybutami i poprawnymi
  `name` i `hp`;
- na własnych plikach tymczasowych: dwa poprawne rekordy dają dwa obiekty i zero błędów, pięć
  błędnych daje zero obiektów i pięć niepustych komunikatów, a plik mieszany dwa obiekty i jeden
  błąd.

Nie sprawdza przykładowego pliku `data/monsters.json`, wartości `attack_type` i `gold` po
konwersji ani tego, czy komunikaty są czytelne, a jedynie to, że nie są puste. Te elementy sprawdź
samodzielnie, na przykład na przykładzie z instrukcji uruchomionym dla `data/monsters.json`.

## Oczekiwane rezultaty

- `check.py` misji 01–03 i projektu Validated Bestiary kończy się komunikatem o ukończeniu.
- Pliki `task.py` misji 01–03 uruchamiają się bez błędów i wypisują wyniki opisane przy zadaniach.
- Dla `data/monsters.json` projektu `load_bestiary` zwraca cztery potwory i cztery czytelne
  komunikaty o błędach.

## Wskazówki

- Każde zadanie ma własne pliki. W misji 03 modele z misji 02 są już gotowe, a projekt ma własne
  modele i własny format danych.
- Części „Break it on purpose” i „Fix it” każą celowo zepsuć dane albo regułę walidacji i sprawdzić,
  czy Twój kod to wykrywa.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`.
  Jeśli nie przechodzisz poziomów 1 i 2, jego wiersz „Next up” wskaże misję poziomu 1. W tym
  zestawie kieruj się kolejnością zadań powyżej.
