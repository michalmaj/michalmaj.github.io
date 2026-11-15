---
title: "Materiały przedmiotu"
summary: "Poziom 2 kursu Python RPG Questbook, mapa kursu i opcjonalne przygotowanie na poziomie 1. Materiały są po angielsku."
status: published
order: 1
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu, instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: level_2_oop_and_design/README.md
    lang: en
    label: "Poziom 2 — OOP and Design: od niego zaczynasz"
  - repository: python-rpg-questbook
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: wszystkie poziomy i misje"
  - repository: python-rpg-questbook
    path: level_1_python_basics/missions/01_hero_stats/README.md
    lang: en
    label: "Uzupełniająco, opcjonalnie: poziom 1 jako przygotowanie (pierwsza misja: Hero Stats)"
---
Instrukcje, mapa kursu i dokumentacja techniczna Questbooka są dostępne po angielsku. Ta strona
wskazuje punkty wejścia i nie zawiera tłumaczeń.

## Materiał główny: poziom 2 „OOP and Design”

Przez cały poziom rozwijasz jeden projekt: terminalową grę RPG. Punktem wyjścia jest celowo
nieuporządkowana wersja gry,
[`starter_legacy_rpg/`](https://github.com/michalmaj/python-rpg-questbook/tree/main/level_2_oop_and_design/starter_legacy_rpg),
zbudowana wyłącznie z konstrukcji poznanych na poziomie 1. Gra działa, a kolejne misje porządkują ją
krok po kroku.

- **Od czego zacząć:** zainstaluj projekt według sekcji „Setup” w opisie repozytorium, uruchom starą
  wersję gry, a potem przejdź do
  [pierwszej misji poziomu 2 (Extract Hero)](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_2_oop_and_design/missions/01_extract_hero/README.md).
- **Jak wygląda misja:** każda ma instrukcję (`README.md`), plik do edycji (`task.py`) i skrypt
  sprawdzający (`check.py`). Polecenia do uruchamiania są w opisie repozytorium.
- **Mapa kursu** (`COURSE_MAP.md`) pokazuje misje poziomu 2 w sekcji „Level 2: OOP and Design” i
  miejsce tego poziomu w całym Questbooku.

| Etap poziomu 2 | Czego dotyczy | Projekt na zakończenie etapu |
|---|---|---|
| World 1: Objects | obiekty zamiast stanu globalnego: klasy, metody, dziedziczenie | [Project 01: Arena Roster](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_2_oop_and_design/projects/01_arena_roster/README.md) |
| World 2: Design | adnotacje typów, typy wyliczeniowe, właściwości, klasy danych | [Project 02: Character Sheet Builder](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_2_oop_and_design/projects/02_character_sheet_builder/README.md) |
| World 3: Structure | podział na moduły, funkcje czyste, testy | [Project 03: Refactored RPG](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_2_oop_and_design/projects/03_refactored_rpg/README.md) |

## Materiał uzupełniający (opcjonalny): poziom 1 jako przygotowanie

Poziom 1 buduje tę samą grę od pierwszych zmiennych, warunków, pętli i funkcji, a potem analizuje jej
dane (w mapie kursu: „Part 1: Python Core” i „Part 2: Game Data Analysis”). Możesz z niego skorzystać,
jeśli chcesz powtórzyć podstawy Pythona przed poziomem 2. Poziom zaczyna się od
[pierwszej misji poziomu 1 (Hero Stats)](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_1_python_basics/missions/01_hero_stats/README.md).
