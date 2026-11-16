---
title: "Obiekty zamiast stanu globalnego"
summary: "Pierwszy etap poziomu 2 kursu Python RPG Questbook (World 1: Objects): trzy misje o klasach, metodach i dziedziczeniu oraz projekt Arena Roster, który zamyka ten etap."
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
  misja-01:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/01_extract_hero/README.md
        lang: en
        label: "Instrukcja: Mission 01 — Extract Hero"
  misja-02:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/02_monster_class/README.md
        lang: en
        label: "Instrukcja: Mission 02 — Monster Class"
  misja-03:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/03_character_base/README.md
        lang: en
        label: "Instrukcja: Mission 03 — Character Base"
  arena-roster:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/projects/01_arena_roster/README.md
        lang: en
        label: "Instrukcja: Project 01 — Arena Roster"
---
Ten zestaw obejmuje pierwszy etap poziomu 2 kursu Python RPG Questbook, „World 1: Objects”. W tym
etapie zastępujesz stan globalny starej wersji gry obiektami. Pierwsze trzy zadania to misje 01–03.
Czwarte to projekt Arena Roster, który według opisu poziomu 2 i mapy kursu zamyka ten etap.
Instrukcje, kod i komunikaty skryptów sprawdzających są po angielsku. Ta strona streszcza je po
polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Questbook zakłada ukończony poziom 1 albo równoważną znajomość podstaw Pythona. Jeśli chcesz
najpierw powtórzyć podstawy, możesz potraktować
[poziom 1](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_1_python_basics/missions/01_hero_stats/README.md)
jako materiał przygotowawczy: buduje tę samą grę od pierwszych zmiennych i funkcji. Do pracy na
poziomie 2 nie potrzebujesz żadnych plików z poziomu 1.

**Instalacja.** Potrzebujesz [uv](https://docs.astral.sh/uv/), a projekt wymaga Pythona 3.12 lub
nowszego. Pobierz repozytorium i zainstaluj zależności poleceniami z sekcji „Setup” w opisie
kursu:

```bash
git clone https://github.com/michalmaj/python-rpg-questbook.git
cd python-rpg-questbook
uv sync
```

**Kod startowy.** Poziom 2 zaczyna się od celowo nieuporządkowanej gry z katalogu
`starter_legacy_rpg/`, zbudowanej wyłącznie z konstrukcji poziomu 1. Uruchom ją z katalogu
głównego repozytorium poleceniem
`uv run python level_2_oop_and_design/starter_legacy_rpg/main.py`.
Gra jest interaktywna: podajesz imię bohatera, wybierasz klasę i wybierasz polecenia z menu.
Opis kodu startowego zaleca rozegrać walkę lub dwie, zapisać grę i ją wczytać, a potem przeczytać
`main.py` od początku do końca. Wyjaśnia też słowo kluczowe `global`, którego poziom 1 nie omawiał,
i podaje pytania, z którymi warto czytać ten kod.

**Jak wygląda misja.** Każda misja ma katalog w `level_2_oop_and_design/missions/` z instrukcją
`README.md`, plikiem `task.py` z komentarzami `TODO` i skryptem `check.py`. Najpierw czytasz
instrukcję, potem uzupełniasz `task.py` i go uruchamiasz, a na końcu uruchamiasz `check.py`.
Wszystkie polecenia wpisujesz w katalogu głównym repozytorium.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`, który importuje Twój kod z `task.py` i go sprawdza. Gdy
wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się
nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Części instrukcji „Break it on purpose” i „Fix it”, zadania poboczne („Side
quest”) i lista „Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO` i komunikaty
skryptów `check.py`.

## Zadania

### Extract Hero: klasa bohatera {#misja-01}

**Cel:** zebrać globalne zmienne bohatera ze starej wersji gry w jedną klasę `Hero`.

**Zakres pracy:** w `level_2_oop_and_design/missions/01_extract_hero/task.py` zdefiniuj klasę
`Hero` z metodą `__init__`, która przyjmuje `name`, `hero_class`, `hp`, `max_hp`, `atk`, `def_`,
`potions` i `gold` i zapisuje je jako atrybuty obiektu. Potem utwórz obiekt `hero` z wartościami
podanymi w pliku.

**Rezultat:** uruchomiony `task.py` wypisuje statystyki bohatera.

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/01_extract_hero/check.py`. Skrypt
sprawdza, czy `hero` jest obiektem klasy `Hero` z wartościami z `task.py` i czy drugi bohater
tworzy osobny obiekt. Nie sprawdza zadania pobocznego (`__repr__`).

### Monster Class: klasa potwora z metodami {#misja-02}

**Cel:** zastąpić słowniki potworów klasą `Monster`, która łączy dane z zachowaniem.

**Zakres pracy:** w `level_2_oop_and_design/missions/02_monster_class/task.py` zdefiniuj klasę
`Monster` z `__init__` (`name`, `hp`, `atk`, `def_`, `gold`) oraz metodami `is_alive()` i
`take_damage(amount)`, przy których HP nie spada poniżej 0. Potem utwórz potwory `goblin`, `orc` i
`dragon` z tabeli w starej wersji gry; ich wartości podaje `task.py`.

**Rezultat:** uruchomiony `task.py` wypisuje HP potworów oraz stan goblina przed obrażeniami i po
nich.

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/02_monster_class/check.py`. Skrypt
sprawdza atrybuty trzech potworów, wynik `is_alive()` przy HP równym 1 i 0 oraz działanie
`take_damage`, także to, że HP zatrzymuje się na 0. Nie sprawdza zadań pobocznych (`__repr__`,
`description()`).

### Character Base: wspólna klasa bazowa {#misja-03}

**Cel:** przenieść wspólny stan i zachowanie bohatera i potwora do klasy bazowej `Character`.
Instrukcja wyjaśnia też, kiedy dziedziczenie jest właściwym narzędziem: wzór obrażeń trafi później
do osobnej funkcji (misja 09), a nie do klasy bazowej.

**Zakres pracy:** w `level_2_oop_and_design/missions/03_character_base/task.py` zdefiniuj trzy
klasy:

- `Character` z atrybutami `name`, `hp`, `atk` i `def_` oraz metodami `is_alive()` i
  `take_damage(amount)`;
- `Hero(Character)` z dodatkowymi atrybutami `potions` i `gold`;
- `Monster(Character)` z dodatkowym atrybutem `gold`.

Obie podklasy wywołują `super().__init__(name, hp, atk, def_)`.

**Rezultat:** uruchomiony `task.py` tworzy bohatera i goblina, zadaje goblinowi obrażenia i
pokazuje, że jego HP zatrzymuje się na 0.

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/03_character_base/check.py`. Skrypt
sprawdza klasę bazową, to, że `Hero` i `Monster` dziedziczą po `Character` i wywołują jej
`__init__` zamiast powtarzać przypisania, ich dodatkowe atrybuty i odziedziczone metody. Nie
sprawdza zadania pobocznego (`roll_damage`).

### Arena Roster: projekt zamykający etap {#arena-roster}

Według opisu poziomu 2 i mapy kursu ten projekt to punkt kontrolny („Checkpoint”) zamykający etap
World 1. Jego instrukcja wymaga misji 01–03. Instrukcja misji 03 kieruje dalej od razu do misji 04,
ale w mapie kursu przed nią jest właśnie ten projekt.

**Cel:** po raz pierwszy zaprojektować kilka współpracujących klas według specyfikacji, bez gotowego
kodu do skopiowania.

**Zakres pracy:** w `level_2_oop_and_design/projects/01_arena_roster/task.py` zastąp
`NotImplementedError` własnym kodem:

- `Character` z atrybutami `name`, `hp`, `max_hp`, `atk` i `def_` oraz metodami
  `take_damage(amount)` (HP nie spada poniżej 0) i `is_alive()`;
- `Hero(Character)` z atrybutami `hero_class` i `potions`;
- `Monster(Character)` z atrybutem `reward_gold`;
- funkcja `build_roster()`, która zwraca co najmniej trzy postacie, bohaterów i potwory;
- funkcja `print_roster(roster)`, która wypisuje nazwę, typ i HP każdej postaci.

Kolejność kroków podaje część „Where to start” instrukcji.

**Rezultat:** klasy i funkcje zgodne ze specyfikacją; `print_roster` wypisuje listę postaci w
formie podobnej do przykładu w instrukcji.

**Sprawdź się:** `uv run python level_2_oop_and_design/projects/01_arena_roster/check.py`. Skrypt
sprawdza:

- dziedziczenie `Hero` i `Monster` po `Character`;
- `is_alive()` i `take_damage`, w tym to, że HP nie spada poniżej 0;
- atrybuty `reward_gold`, `hero_class` i `potions`;
- skład listy z `build_roster()`: co najmniej trzy postacie, w tym co najmniej jeden bohater i
  jeden potwór;
- to, że `print_roster()` wypisuje co najmniej jedną linię na postać.

Nie sprawdza `max_hp`, `atk` ani `def_`, użycia `super().__init__` ani treści i formatu
wypisywanych linii. Te elementy porównaj samodzielnie ze specyfikacją i przykładem w instrukcji.

## Oczekiwane rezultaty

- `check.py` misji 01–03 i projektu Arena Roster kończy się komunikatem o ukończeniu.
- Uruchomione pliki `task.py` misji 01–03 wypisują to, co opisują ich instrukcje.
- W projekcie Arena Roster `print_roster()` wypisuje listę postaci zgodną ze specyfikacją z
  instrukcji.

## Wskazówki

- Każde zadanie ma własny `task.py`. Klasy z wcześniejszych misji nie przechodzą same do kolejnych:
  każde zadanie definiuje je od nowa według swojej instrukcji.
- Części „Break it on purpose” i „Fix it” każą celowo zepsuć kod i obejrzeć błąd. Pokazują w ten
  sposób, po co jest `self` i `super().__init__()`.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`.
  Jeśli nie przechodzisz poziomu 1, jego wiersz „Next up” wskaże misję poziomu 1. W tym zestawie
  kieruj się kolejnością zadań powyżej.
