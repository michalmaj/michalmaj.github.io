---
title: "Lepszy projekt klas"
summary: "Drugi etap poziomu 2 kursu Python RPG Questbook (World 2: Design): cztery misje o adnotacjach typów, typach wyliczeniowych, właściwościach i klasach danych oraz projekt Character Sheet Builder, który zamyka ten etap."
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
tasks:
  misja-04:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/04_type_hints/README.md
        lang: en
        label: "Instrukcja: Mission 04 — Type Hints"
  misja-05:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/05_enums/README.md
        lang: en
        label: "Instrukcja: Mission 05 — Enums"
  misja-06:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/06_properties/README.md
        lang: en
        label: "Instrukcja: Mission 06 — Properties"
  misja-07:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/missions/07_dataclasses/README.md
        lang: en
        label: "Instrukcja: Mission 07 — Dataclasses"
  character-sheet-builder:
    materials:
      - repository: python-rpg-questbook
        path: level_2_oop_and_design/projects/02_character_sheet_builder/README.md
        lang: en
        label: "Instrukcja: Project 02 — Character Sheet Builder"
---
Ten zestaw obejmuje drugi etap poziomu 2 kursu Python RPG Questbook, „World 2: Design”. W tym etapie
poprawiasz projekt klas gry: dodajesz adnotacje typów, zastępujesz napisy typem wyliczeniowym
(`Enum`), wprowadzasz właściwości (`@property`) i klasy danych (`@dataclass`). Pierwsze cztery
zadania to misje 04–07. Piąte to projekt Character Sheet Builder, który według opisu poziomu 2 i
mapy kursu zamyka ten etap. Instrukcje, kod i komunikaty skryptów sprawdzających są po angielsku. Ta
strona streszcza je po polsku i odsyła do instrukcji.

## Przygotowanie do zestawu

Zestaw jest dalszym ciągiem [zestawu 1](world-1-objects.md). Misje korzystają z klas `Character`,
`Hero` i `Monster` z etapu World 1, ale każde zadanie ma własny plik `task.py` z gotowym punktem
wyjścia. Nie potrzebujesz więc plików z zestawu 1. Instrukcja projektu Character Sheet Builder podaje
„Requires: Level 2, Missions 01–07”, czyli zakłada znajomość także misji 01–03.

**Instalacja.** Jeśli nie masz jeszcze repozytorium, potrzebujesz [uv](https://docs.astral.sh/uv/)
i Pythona 3.12 lub nowszego. Pobierz repozytorium i zainstaluj zależności poleceniami z sekcji
„Setup” w opisie kursu:

```bash
git clone https://github.com/michalmaj/python-rpg-questbook.git
cd python-rpg-questbook
uv sync
```

`uv sync` instaluje też mypy, którego opcjonalnie używa misja 04.

**Jak wygląda misja.** Każda misja ma katalog w `level_2_oop_and_design/missions/` z instrukcją
`README.md`, plikiem `task.py` z komentarzami `TODO` i skryptem `check.py`. Najpierw czytasz
instrukcję, potem uzupełniasz `task.py` i go uruchamiasz, a na końcu uruchamiasz `check.py`.
Polecenia misji wpisujesz w katalogu głównym repozytorium. Projekt ma własny katalog w
`level_2_oop_and_design/projects/`.

## Sprawdzanie własnej pracy

Każde zadanie ma skrypt `check.py`, który importuje Twój kod z `task.py` i go sprawdza. Gdy
wszystko się zgadza, skrypt wypisuje komunikat o ukończeniu i zapisuje postęp lokalnie. Gdy coś się
nie zgadza, wypisuje, czego oczekiwał.

Skrypt sprawdza tylko wybrane elementy zadania. Co dokładnie, opisuje część „Sprawdź się” przy
każdym zadaniu. Resztę sprawdzasz sam: uruchamiasz `task.py` i porównujesz wynik z instrukcją.
Części instrukcji „Break it on purpose” i „Fix it”, zadania poboczne („Side quest”) i lista
„Checklist” służą samodzielnej pracy i `check.py` ich nie sprawdza.

Nie uruchamiaj `uv run pytest` ani `uv run ruff check .` dla całego repozytorium. Pliki startowe
są celowo niekompletne, więc zobaczysz błędy. Według opisu kursu te polecenia są narzędziami autora
kursu, nie studentów.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcje, kod z komentarzami `TODO` i komunikaty
skryptów `check.py`.

## Zadania

### Type Hints: adnotacje typów {#misja-04}

**Cel:** opisać typami wszystkie parametry, wartości zwracane i atrybuty klas `Character`, `Hero` i
`Monster`.

**Zakres pracy:** w `level_2_oop_and_design/missions/04_type_hints/task.py` są klasy z misji 03 bez
adnotacji. Dodaj typy parametrów i wartości zwracanych we wszystkich metodach, także `-> None` w
`__init__`, oraz adnotacje atrybutów w `__init__`. Metoda `use_potion` ma celowy błąd logiczny.
Zostaw go: instrukcja pokazuje na nim, że adnotacje sprawdzają typy, a nie logikę, i zapowiada, że
błąd tego rodzaju wykryjesz testem w misji 10.

**Rezultat:** uruchomiony `task.py` wypisuje HP bohatera i goblina, tak jak przed zmianami.
Instrukcja podaje też opcjonalne polecenie, które sprawdza plik narzędziem mypy:

```bash
uv run mypy level_2_oop_and_design/missions/04_type_hints/task.py --ignore-missing-imports
```

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/04_type_hints/check.py`. Skrypt
sprawdza typy parametrów i wartości zwracanych w `__init__` wszystkich trzech klas oraz w
`is_alive`, `take_damage` i `use_potion`. Typ musi być właściwy (`str`, `int`, `bool` albo `None`),
a nie zastępczy, jak `object`. Skrypt sprawdza też, że klasy nadal działają. Nie sprawdza adnotacji
atrybutów (`self.hp: int`), choć wspomina o nich komunikat o ukończeniu. Nie sprawdza błędu w
`use_potion` ani zadania pobocznego i nie uruchamia mypy.

### Enums: typ wyliczeniowy klas bohatera {#misja-05}

**Cel:** zastąpić napisy `"warrior"`, `"mage"` i `"rogue"` typem wyliczeniowym `HeroClass`.

**Zakres pracy:** w `level_2_oop_and_design/missions/05_enums/task.py` zdefiniuj `HeroClass(Enum)` z
elementami `WARRIOR`, `MAGE` i `ROGUE` o wartościach `"warrior"`, `"mage"` i `"rogue"`. Potem:

- zmień typ parametru `hero_class` w `Hero.__init__` z `str` na `HeroClass`;
- w metodzie `class_bonus()` porównuj z elementami `HeroClass` zamiast z napisami;
- w bloku `if __name__ == "__main__":` utwórz bohaterów z `HeroClass.WARRIOR` i `HeroClass.MAGE`.

**Rezultat:** uruchomiony `task.py` wypisuje premię do ataku wojownika (2) i maga (0).

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/05_enums/check.py`. Skrypt sprawdza:

- że `HeroClass` dziedziczy po `Enum` i ma trzy elementy o podanych wartościach;
- że `Hero` przechowuje element `HeroClass`, a nie napis;
- że `class_bonus()` zwraca 2 dla wojownika, 0 dla maga i 4 dla łotrzyka (`ROGUE`).

Nie sprawdza bloku `if __name__ == "__main__":` w `task.py` ani zadania pobocznego (`MonsterTier`).

### Properties: wartości wyliczane {#misja-06}

**Cel:** dodać do klasy `Character` właściwości, które wyliczają wartości z istniejących atrybutów
zamiast przechowywać je osobno.

**Zakres pracy:** w `level_2_oop_and_design/missions/06_properties/task.py` dodaj do `Character` trzy
właściwości (`@property`):

- `is_alive`: `True`, gdy `hp` jest większe od 0;
- `hp_percent`: HP jako procent `max_hp`, liczba od 0.0 do 100.0;
- `status`: `"healthy"`, gdy `hp_percent` wynosi co najmniej 50, `"wounded"`, gdy co najmniej 20, a
  w pozostałych przypadkach `"critical"`.

**Rezultat:** uruchomiony `task.py` wypisuje HP, procent HP i stan bohatera po kolejnych
obrażeniach.

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/06_properties/check.py`. Skrypt
sprawdza:

- że wszystkie trzy nazwy są właściwościami, a nie zwykłymi metodami;
- `is_alive` przy HP równym 100 i 0;
- `hp_percent` dla siedmiu par HP i maksymalnego HP;
- `status` po obu stronach progów 50% i 20% i dokładnie na nich;
- że przypisanie wartości do `is_alive` kończy się błędem `AttributeError`.

Nie sprawdza zadania pobocznego (`summary`).

### Dataclasses: klasa danych szablonu potwora {#misja-07}

**Cel:** zastąpić ręcznie napisany `__init__` klasy `MonsterTemplate` dekoratorem `@dataclass` i
zobaczyć, co dekorator generuje sam.

**Zakres pracy:** w `level_2_oop_and_design/missions/07_dataclasses/task.py` dodaj `@dataclass` do
`MonsterTemplate`, zapisz pola `name`, `hp`, `atk`, `def_` i `gold` z adnotacjami typów na poziomie
klasy i usuń `__init__`. Potem utwórz cztery szablony: `goblin_template`, `orc_template`,
`troll_template` i `dragon_template`. Ich wartości z tabeli potworów starej wersji gry podaje
`task.py`.

**Rezultat:** uruchomiony `task.py` wypisuje cztery szablony w postaci wygenerowanej przez
`__repr__` oraz wynik porównania dwóch goblinów o tych samych wartościach (`True`).

**Sprawdź się:** `uv run python level_2_oop_and_design/missions/07_dataclasses/check.py`. Skrypt
sprawdza:

- że `MonsterTemplate` jest klasą danych z pięcioma polami;
- nazwy i HP czterech szablonów;
- że `__repr__` zawiera nazwę klasy i nazwę potwora;
- że goblin jest równy nowemu obiektowi o tych samych wartościach, a więc wszystkie wartości goblina,
  i różny od orka.

Nie sprawdza `atk`, `def_` ani `gold` orka, trolla i smoka. Nie sprawdza też zadania pobocznego
(`frozen=True`).

### Character Sheet Builder: projekt zamykający etap {#character-sheet-builder}

Według opisu poziomu 2 i mapy kursu ten projekt to punkt kontrolny („Checkpoint”) zamykający etap
World 2. Jego instrukcja wymaga misji 01–07. Instrukcja misji 07 kieruje dalej od razu do misji 08,
ale w mapie kursu przed nią jest właśnie ten projekt.

**Cel:** połączyć w jednej karcie postaci typ wyliczeniowy, klasy danych, właściwości i adnotacje
typów.

**Zakres pracy:** w `level_2_oop_and_design/projects/02_character_sheet_builder/task.py` typ
wyliczeniowy `HeroClass` (`WARRIOR`, `MAGE`, `RANGER`) i klasy danych `Weapon`, `Armor` i
`CharacterSheet` są już zdefiniowane, choć tabela w instrukcji wymienia je wśród wymagań. Zastąp
`NotImplementedError` własnym kodem w czterech miejscach:

- `total_weight`: suma wag broni i pancerza, przy czym puste miejsce waży 0.0;
- `power_score`: `damage + defense - int(total_weight // 5)`, gdzie brak broni daje 0 obrażeń, a
  brak pancerza 0 obrony; wynik nie może być ujemny;
- `is_encumbered`: `True`, gdy `total_weight` przekracza 20.0;
- `summary()`: czytelny napis w jednym wierszu z imieniem i klasą postaci.

**Rezultat:** właściwości i metoda dają wyniki z przykładu w instrukcji: dla Ady z mieczem i
skórzaną kamizelką waga wynosi 9.5, a siła 17. Przykład w opisie `summary()` w `task.py` podaje
„Power: 18”, ale ze wzoru wynika 17.

**Sprawdź się:** polecenie z instrukcji, wpisane w katalogu głównym repozytorium:

```bash
cd level_2_oop_and_design/projects/02_character_sheet_builder
uv run python check.py
```

Skrypt działa też uruchomiony z katalogu głównego. Sprawdza:

- że `HeroClass` jest typem wyliczeniowym z trzema elementami, a `Weapon` i `Armor` są klasami
  danych;
- `total_weight` z pełnym wyposażeniem, bez broni i bez wyposażenia;
- `power_score` z przykładu w instrukcji (17) oraz to, że wynik nie spada poniżej 0, także gdy wzór
  daje liczbę ujemną;
- `is_encumbered` przy 9.5 kg (`False`) i 21.5 kg (`True`);
- że `summary()` zwraca niepusty napis z imieniem i klasą postaci.

Nie sprawdza formatu napisu z `summary()` poza imieniem i klasą, wyniku przy dokładnie 20.0 kg ani
karty z samą bronią. Te elementy porównaj samodzielnie ze specyfikacją i przykładem w instrukcji.

## Oczekiwane rezultaty

- `check.py` misji 04–07 i projektu Character Sheet Builder kończy się komunikatem o ukończeniu.
- Pliki `task.py` misji 04–07 uruchamiają się bez błędów i wypisują wyniki opisane przy zadaniach.
- W projekcie Character Sheet Builder właściwości i `summary()` dają wyniki zgodne z przykładem w
  instrukcji.

## Wskazówki

- Każde zadanie ma własny `task.py`. Klasy z wcześniejszych misji nie przechodzą same do kolejnych:
  każde zadanie definiuje je od nowa według swojej instrukcji.
- Części „Break it on purpose” i „Fix it” każą celowo zepsuć kod i obejrzeć skutek: przekazać napis
  zamiast liczby, użyć błędnej wartości typu wyliczeniowego, przypisać wartość właściwości albo
  usunąć adnotacje pól klasy danych.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`.
  Jego wiersz „Next up” wskazuje pierwsze nieukończone zadanie, licząc od poziomu 1. W tym zestawie
  kieruj się kolejnością zadań powyżej.
