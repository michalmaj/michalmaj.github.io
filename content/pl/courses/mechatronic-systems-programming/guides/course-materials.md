---
title: "Materiały przedmiotu"
summary: "Gdzie znaleźć dokumentację modułów, kod startowy i projekt końcowy."
status: published
order: 1
materials:
  - repository: mechatronic-systems-programming
    path: README.md
    lang: pl
    label: "Opis kursu: dla kogo, co zbudujesz, jak wygląda nauka"
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta"
  - repository: mechatronic-systems-programming
    path: docs/handbook.md
    lang: pl
    label: "Podręcznik kursu"
  - repository: mechatronic-systems-programming
    path: course/README.md
    lang: pl
    label: "Materiał modułów: treść misji i zasady pracy z kodem"
  - repository: mechatronic-systems-programming
    path: final_project/README.md
    lang: pl
    label: "Projekt końcowy"
  - repository: mechatronic-systems-programming
    ref: final-project-start-v3
    lang: pl
    label: "Kod startowy projektu końcowego"
---
## Jak korzystać z repozytorium

- **Dokumentację czytasz na gałęzi `main`.** Tam są moduły, plan pracy i podręcznik w aktualnej
  wersji. Dokumentacja jest po polsku; wersje angielskie mają w nazwie pliku `.en`.
- **Kod piszesz na własnej gałęzi utworzonej z tagu startowego modułu** (`module-XX-start`). Tagi
  są niezmienne, więc punkt startowy każdego modułu zawsze wygląda tak samo.
- **Zaczynasz od Modułu 0:** orientacja, terminal i instalacja narzędzi. Polecenia i kolejność pracy
  opisuje plan pracy studenta.

## Moduły

| Moduł | Dokumentacja (`main`) | Kod startowy (tag) |
|---|---|---|
| 0. Orientacja i narzędzia | [dokumentacja modułu 0](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_00_tooling) | brak tagu — praca na `main` |
| 1. Podstawy sterowania | [dokumentacja modułu 1](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_01_control_basics) | [`module-01-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-01-start) |
| 2. Klasa Diverter | [dokumentacja modułu 2](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_02_diverter_class) | [`module-02-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-02-start) |
| 3. Engine | [dokumentacja modułu 3](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_03_engine) | [`module-03-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-03-start) |
| 4. Pas i tryb pracy | [dokumentacja modułu 4](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_04_belt_and_mode) | [`module-04-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-04-start) |
| 5. Awaryjny stop | [dokumentacja modułu 5](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_05_estop) | [`module-05-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-05-start) |
| 6. Czujniki | [dokumentacja modułu 6](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_06_sensors) | [`module-06-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-06-start) |
| 7. Tryb awarii | [dokumentacja modułu 7](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_07_fault_mode) | [`module-07-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-07-start) |
| 8. Wiele paczek | [dokumentacja modułu 8](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_08_multiple_items) | [`module-08-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-08-start) |
| 9. Scenariusze zapisane w danych | [dokumentacja modułu 9](https://github.com/michalmaj/mechatronic-systems-programming/tree/main/course/module_09_scripted_scenarios) | [`module-09-start`](https://github.com/michalmaj/mechatronic-systems-programming/tree/module-09-start) |

## Projekt końcowy

Opis projektu końcowego czytasz na `main`, a kod startowy pochodzi z tagu `final-project-start-v3`
(oba odnośniki w materiałach powyżej).
