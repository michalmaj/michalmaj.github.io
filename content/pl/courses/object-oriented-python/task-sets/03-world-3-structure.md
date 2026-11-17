---
title: "Podział, testy i rozdzielenie odpowiedzialności"
summary: "Trzeci etap poziomu 2 kursu Python RPG Questbook (World 3: Structure): trzy misje o podziale kodu na moduły, funkcjach czystych i testach w pytest oraz projekt Refactored RPG, w którym odbudowujesz grę jako uporządkowany pakiet."
status: published
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu: instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: level_2_oop_and_design/README.md
    lang: en
    label: "Poziom 2 — OOP and Design: jak zacząć i etapy poziomu"
  - repository: python-rpg-questbook
    path: level_2_oop_and_design/starter_legacy_rpg/README.md
    lang: en
    label: "Kod startowy poziomu 2: jak uruchomić i czytać starą wersję gry"
tasks:
  misja-08:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/08_module_split/README.md
        lang: en
        label: "Instrukcja: Mission 08 — Module Split"
  misja-09:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/09_pure_functions/README.md
        lang: en
        label: "Instrukcja: Mission 09 — Pure Functions"
  misja-10:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/10_add_tests/README.md
        lang: en
        label: "Instrukcja: Mission 10 — Add Tests"
  refactored-rpg:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/projects/03_refactored_rpg/README.md
        lang: en
        label: "Instrukcja: Project 03 — Refactored RPG"
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/starter_legacy_rpg/main.py
        lang: en
        label: "Stara wersja gry, którą odbudowujesz: starter_legacy_rpg/main.py"
---
Ten zestaw obejmuje trzeci, ostatni etap poziomu 2 kursu Python RPG Questbook, „World 3:
Structure”. W tym etapie dzielisz kod gry na moduły, wydzielasz obliczenia do funkcji czystych i
piszesz testy w pytest. Pierwsze trzy zadania to misje 08–10. Czwarte to projekt Refactored RPG, w
którym odbudowujesz starą wersję gry jako uporządkowany pakiet. Opis poziomu 2 i mapa kursu nazywają
go walką z bossem („Boss Fight”) tego etapu. Instrukcje, kod i komunikaty skryptów sprawdzających są
po angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Zestaw jest dalszym ciągiem [zestawu 1](world-1-objects.md) i [zestawu 2](world-2-design.md). Misje
08–10 mają własne pliki z gotowym punktem wyjścia, więc nie potrzebujesz plików z wcześniejszych
zestawów. Projekt Refactored RPG jest inny: instrukcja podaje „Requires: Level 2, Missions 01–10”, a
jej część „Where to start” każe przenieść do pakietu klasy i funkcje z misji 01–10. Przyda Ci się
więc Twój kod z tych misji.

**Instalacja.** Jeśli nie masz jeszcze repozytorium, potrzebujesz [uv](https://docs.astral.sh/uv/)
i Pythona 3.12 lub nowszego. Pobierz repozytorium i zainstaluj zależności poleceniami z sekcji
„Setup” w opisie kursu:

```bash
git clone https://github.com/michalmaj/python-rpg-questbook.git
cd python-rpg-questbook
uv sync
```

`uv sync` instaluje też pytest, którego używają misja 10 i projekt.

**Stara wersja gry.** Projekt odtwarza grę z katalogu `starter_legacy_rpg/`. Uruchom ją z katalogu
głównego repozytorium poleceniem
`uv run python level_2_oop_and_design/starter_legacy_rpg/main.py`, żeby wiedzieć, jak ma działać
odbudowana wersja.

**Jak wygląda misja.** Każda misja ma katalog w `level_2_oop_and_design/missions/` z instrukcją
`README.md` i skryptem `check.py`. Kod uzupełniasz tam, gdzie wskazuje instrukcja: w misji 08 w
pakiecie `rpg/`, w misji 09 w `task.py`, a w misji 10 w pliku testów `test_combat.py`. Polecenia misji
wpisujesz w katalogu głównym repozytorium.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`, który importuje Twój kod i go sprawdza. W misji 10 i w projekcie
skrypt uruchamia też Twoje testy. Gdy wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i
zapisuje postęp lokalnie. Gdy coś się nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Resztę sprawdzasz sam: uruchamiasz swój kod i porównujesz wynik z instrukcją.
Części instrukcji „Break it on purpose” i „Fix it”, zadania poboczne („Side quest”) i lista
„Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów. Polecenie z instrukcji misji 10 uruchamia pytest tylko dla katalogu tej misji.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO` i komunikaty
skryptów `check.py`.

## Zadania

### Module Split: pakiet zamiast jednego pliku {#misja-08}

**Cel:** zobaczyć grę podzieloną na moduły pakietu `rpg` i dokończyć moduł walki.

**Zakres pracy:** w `level_2_oop_and_design/missions/08_module_split/` jest pakiet `rpg/` z plikiem
`__init__.py` i gotowymi modułami `hero.py` (`Hero` i `HeroClass`) oraz `monster.py`
(`MonsterTemplate`, `Monster` i lista `MONSTER_TEMPLATES`). W `rpg/combat.py` zaimplementuj według
komentarzy `TODO` trzy funkcje:

- `compute_damage(atk, def_)`: atak plus rzut kostką sześciościenną minus obrona, co najmniej 1;
- `hero_turn(hero, monster)`: rzut kostką dwudziestościenną, przy którym 20 oznacza trafienie
  krytyczne i podwaja atak, potem obrażenia zadane potworowi i wynik `(obrażenia, czy_krytyczne)`;
- `monster_turn(monster, hero)`: to samo w drugą stronę.

Instrukcja opisuje cztery moduły, w tym `game.py` z funkcją `main()`, ale w pakiecie misji nie ma
`game.py`. Walkę uruchamia `task.py`.

**Rezultat:** `uv run python level_2_oop_and_design/missions/08_module_split/task.py` rozgrywa do
trzech tur walki Ady z losowym potworem.

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/08_module_split/check.py`. Skrypt
sprawdza:

- `compute_damage` na wielu wywołaniach dla trzech par ataku i obrony: czy wyniki mieszczą się w
  oczekiwanym zakresie i zmieniają się z rzutem kostki;
- dolną granicę 1 przy bardzo wysokiej obronie;
- że `hero_turn` i `monster_turn` zwracają parę: liczbę co najmniej 1 i wartość logiczną, oraz
  zmniejszają HP celu;
- że w pakiecie są pliki `__init__.py`, `hero.py`, `monster.py` i `combat.py`.

Nie sprawdza trafień krytycznych, czyli podwojenia ataku przy wyniku 20, ani zadania pobocznego
(`config.py`).

### Pure Functions: obliczenia bez skutków ubocznych {#misja-09}

**Cel:** wydzielić obliczanie obrażeń z funkcji, która jednocześnie liczy, zmienia stan potwora i
wypisuje tekst.

**Zakres pracy:** w `level_2_oop_and_design/missions/09_pure_functions/task.py` jest pozostawiona do
porównania funkcja `hero_attacks_legacy()` ze starej wersji gry. Nie zmieniaj jej. Nad nią zdefiniuj:

- `compute_damage(atk, def_, dice_roll)`: funkcję czystą, która zwraca `atk + dice_roll - def_`, co
  najmniej 1, bez losowania i bez wypisywania;
- `resolve_hit(atk, def_)`: funkcję, która rzuca kostką sześciościenną i wywołuje `compute_damage`,
  bez wypisywania.

**Rezultat:** uruchomiony `task.py` wypisuje `compute_damage(15, 5, 4) = 14`,
`compute_damage(5, 20, 1) = 1` i trzy wyniki `resolve_hit(15, 5)`.

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/09_pure_functions/check.py`. Skrypt
sprawdza:

- wyniki `compute_damage` dla czterech zestawów argumentów, w tym dolną granicę 1;
- że `compute_damage` i `resolve_hit` niczego nie wypisują;
- że `resolve_hit(15, 5)` zwraca liczby od 11 do 16.

Nie sprawdza, czy `resolve_hit` wywołuje `compute_damage`, ani zadania pobocznego
(`simulate_battle`).

### Add Tests: testy w pytest {#misja-10}

**Cel:** napisać testy w pytest dla funkcji czystej, która oblicza obrażenia.

**Zakres pracy:** w `level_2_oop_and_design/missions/10_add_tests/test_combat.py` jest pięć pustych
testów. W każdym zastąp `pass` asercją (`assert`) opisaną w komentarzu. Testowana funkcja
`compute_damage` jest w pliku `combat.py` w tym samym katalogu. Ten plik jest kompletny i według jego
nagłówka nie należy go zmieniać. Wyjątkiem jest część „Break it on purpose”, po której przywracasz
go w części „Fix it”.

**Rezultat:** polecenie z instrukcji pokazuje, że przechodzi wszystkie pięć testów:

```bash
uv run pytest level_2_oop_and_design/missions/10_add_tests/ -v
```

To samo pokazuje ono także na starcie, bo puste testy nie mają asercji. Dlatego liczy się wynik
`check.py`.

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/10_add_tests/check.py`. Skrypt:

- uruchamia Twoje testy na oryginalnym `combat.py` i wymaga, żeby przeszły;
- wymaga w pliku testów co najmniej pięciu instrukcji `assert`;
- na czas sprawdzania podmienia `combat.py` na pięć wersji, z których każda ma jeden celowy błąd:
  brak dolnej granicy 1, pominiętą obronę, pominięty atak, pominięty rzut kostką albo błąd tylko przy
  obronie 0. Dla każdej wersji sprawdza, czy Twoje testy ją wykrywają, a na koniec przywraca
  oryginalny plik.

Nie sprawdza, czy każda z pięciu funkcji testowych ma własną asercję, ani zadania pobocznego, czyli
testów klas `Hero` i `Monster`.

### Refactored RPG: gra od nowa jako pakiet {#refactored-rpg}

Według opisu poziomu 2 i mapy kursu ten projekt to walka z bossem („Boss Fight”) etapu World 3. Jego
instrukcja wymaga misji 01–10.

**Cel:** odbudować grę z `starter_legacy_rpg/main.py` jako uporządkowany pakiet. Dla gracza gra ma
działać tak samo, zmienia się tylko kod.

**Zakres pracy:** w `level_2_oop_and_design/projects/03_refactored_rpg/` uzupełnij pliki według
komentarzy w nich i kolejności z części „Where to start” instrukcji:

- `rpg/hero.py`: typ wyliczeniowy `HeroClass` (`WARRIOR`, `MAGE`, `ROGUE`) i klasa `Hero` z
  adnotacjami typów, właściwością `is_alive` oraz metodami `take_damage()` i `heal()`;
- `rpg/monster.py`: klasa danych `MonsterTemplate`, klasa `Monster` z właściwością `is_alive` i
  metodą `take_damage()` oraz lista `MONSTER_TEMPLATES` z czterema potworami ze starej wersji gry;
- `rpg/combat.py`: funkcja czysta `compute_damage(atk, def_, dice_roll)` oraz `resolve_hit(atk,
  def_)`, `hero_turn(hero, monster)` i `monster_turn(monster, hero)` z trafieniami krytycznymi;
- `rpg/game.py`: funkcje `choose_hero()`, `run_combat(hero, monster)`, `save_log()`, `save_game()`,
  `load_game()` i `main()` z menu lochu (walka, statystyki, zapis, wyjście), przeniesione ze starej
  wersji gry;
- `tests/test_combat.py`: co najmniej pięć testów z prawdziwymi asercjami. Plik zawiera pięć pustych
  testów jako przykład budowy.

Tabela w instrukcji wymaga też wspólnej klasy bazowej `Character` dla `Hero` i `Monster` (misja 03)
oraz adnotacji typów w każdej funkcji i metodzie. Instrukcja każe napisać kod od nowa i tłumaczyć
starą wersję, a nie ją kopiować.

**Rezultat:** odbudowana gra działa tak jak stara wersja, a testy z `tests/` przechodzą.

**Sprawdź się:** `uv run python level_2_oop_and_design/projects/03_refactored_rpg/check.py`. Skrypt
sprawdza:

- że istnieje sześć plików: `rpg/__init__.py`, `rpg/hero.py`, `rpg/monster.py`, `rpg/combat.py`,
  `rpg/game.py` i `tests/test_combat.py`;
- import `Hero` i `HeroClass` z `rpg.hero`, `Monster` i `MonsterTemplate` z `rpg.monster` oraz
  `compute_damage` z `rpg.combat`;
- że `HeroClass` jest typem wyliczeniowym, a `MonsterTemplate` klasą danych;
- właściwość `is_alive` przed obrażeniami i po nich u bohatera i potwora. Skrypt tworzy je tak jak w
  misji 08: `Hero("Ada", HeroClass.WARRIOR, hp=120, max_hp=120, atk=15, def_=8, potions=2,
  gold=20)` i `Monster(template)`;
- że `compute_damage(15, 5, 4)` zwraca 14, `compute_damage(1, 100, 1)` zwraca 1, a funkcja niczego
  nie wypisuje;
- że Twoje testy przechodzą, a plik testów ma co najmniej pięć instrukcji `assert`.

Nie sprawdza klasy `Character`, choć wymienia ją część „Acceptance criteria” instrukcji. Nie
sprawdza też adnotacji typów, listy `MONSTER_TEMPLATES`, funkcji `resolve_hit`, `hero_turn` i
`monster_turn` ani zawartości `game.py` poza tym, że plik istnieje. Nie uruchamia gry. Te elementy
porównaj samodzielnie z instrukcją i ze starą wersją gry.

**Uruchamianie gry i testów projektu.** W obecnej wersji kursu polecenia z części „How to play” i
„How to test” instrukcji kończą się błędem `ModuleNotFoundError` (`No module named 'rpg.hero'` albo
`No module named 'rpg.combat'`), także gdy projekt jest kompletny. Po `uv sync` nazwa `rpg` wskazuje
bowiem pakiet zainstalowany z projektu poziomu 4 (`level_4_interfaces/projects/03_installable_cli_tool`).
`check.py` tego problemu nie ma, bo importuje pakiet i uruchamia testy z katalogu projektu. Z tego
katalogu działają też gra i testy:

```bash
cd level_2_oop_and_design/projects/03_refactored_rpg
uv run python -m rpg.game
uv run python -m pytest tests/ -v
```

## Oczekiwane rezultaty

- `check.py` misji 08–10 i projektu Refactored RPG kończy się komunikatem o ukończeniu.
- Pliki `task.py` misji 08 i 09 uruchamiają się bez błędów i wypisują wyniki opisane przy zadaniach.
- Odbudowana gra działa tak jak stara wersja z `starter_legacy_rpg/main.py`.

## Wskazówki

- Uruchamiaj `check.py` misji 10, gdy `combat.py` ma oryginalną postać. Jeśli plik został zmieniony
  w części „Break it on purpose”, najpierw go przywróć, jak każe część „Fix it”.
- Projekt Refactored RPG zaczyna się od pustych plików z komentarzami. Kolejność z części „Where to
  start” prowadzi od klas bohatera i potwora, przez walkę i pętlę gry, do testów.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`.
  Jego wiersz „Next up” wskazuje pierwsze nieukończone zadanie, licząc od poziomu 1. W tym zestawie
  kieruj się kolejnością zadań powyżej.
