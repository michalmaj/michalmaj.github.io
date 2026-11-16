---
title: "Demonstracje uzupełniające"
summary: "Siedem interaktywnych demonstracji wybranych zagadnień uczenia maszynowego z aplikacji Interactive ML Labs (wersja alfa). Materiały pomocnicze do samodzielnej nauki; nie obejmują całego zakresu sztucznej inteligencji."
status: published
order: 1
materials:
  - repository: interactive-ml-labs
    path: docs/student_alpha_v0_0_9a.pl.md
    lang: pl
    label: "Notatki dla studentów do wersji alfa v0.0.9a: od nich zaczynasz"
  - repository: interactive-ml-labs
    path: docs/student_alpha_v0_0_9a.md
    lang: en
    label: "Notatki dla studentów do wersji alfa v0.0.9a (wersja angielska)"
  - repository: interactive-ml-labs
    path: USAGE.pl.md
    lang: pl
    label: "Instrukcja: instalacja, uruchamianie i sterowanie"
  - repository: interactive-ml-labs
    path: USAGE.md
    lang: en
    label: "Instrukcja (wersja angielska)"
---
**Status:** Interactive ML Labs jest projektem w wersji alfa. Najnowsze wydanie,
[v0.0.9a](https://github.com/michalmaj/interactive-ml-labs/releases/tag/v0.0.9a), repozytorium
opisuje jako pierwszą wersję alfa przeznaczoną dla studentów. Aplikacja jest dalej rozwijana i może
się zmieniać.

Prezentowane demonstracje dotyczą wybranych zagadnień uczenia maszynowego. Stanowią materiały
pomocnicze do samodzielnej nauki, nie obejmują całego zakresu sztucznej inteligencji i nie określają
programu ani zasad zaliczenia przedmiotu.

## Jak korzystać z aplikacji

- **Uruchomienie:** Interactive ML Labs uruchamia się na własnym komputerze. Potrzebny jest
  Python 3.12 lub nowszy i uv, a polecenie uruchamiające aplikację jest w notatkach dla studentów i
  w instrukcji. W lekcjach nie trzeba pisać kodu.
- **Gdzie są demonstracje:** wszystkie siedem jest na pierwszym poziomie aplikacji. Wybierz
  „Przeglądaj dema według poziomu”, a potem „Poziom 1 - Fundamenty”. Należą też do prowadzonych
  ścieżek nauki (w menu „Prowadzone ścieżki nauki”): „Jak modele uczą się z błędu”, „Od odległości
  do klastrów” i „Od cech do decyzji modelu”.
- **Języki:** interfejs aplikacji oraz teoria i zadania w aplikacji są po polsku i po angielsku.
  Notatki dla studentów i instrukcja również. Języki materiałów w repozytorium są podane przy
  każdej demonstracji.

## Demonstracje

Kolejność jest taka jak na pierwszym poziomie aplikacji. Demonstracje otwiera się w aplikacji, a
linki prowadzą do materiałów w repozytorium. Cztery demonstracje mają własny katalog (link w
nazwie). Trzy działają tylko w aplikacji, a przy nich jest link do sekcji instrukcji, która opisuje
ich sterowanie.

- **Linear Regression Line Fit Lab** — ręczne dopasowanie prostej do danych: nachylenie, wyraz
  wolny, reszty, błąd średniokwadratowy (MSE) i porównanie z dopasowaniem metodą najmniejszych
  kwadratów. Działa tylko w aplikacji, po polsku i po angielsku. Sterowanie:
  [instrukcja, sekcja „Natywne laby Level 1”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-1)
  ([wersja angielska](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.md#app-only-level-1-labs)).
- **K-Means Intro Lab** — grupowanie algorytmem k-średnich krok po kroku: przypisywanie punktów,
  przesuwanie centroidów, liczba grup `k` i inercja oraz to, dlaczego niższa inercja nie mówi
  wszystkiego o grupowaniu. Działa tylko w aplikacji, po polsku i po angielsku. Sterowanie:
  [instrukcja, sekcja „Natywne laby Level 1”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-1)
  ([wersja angielska](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.md#app-only-level-1-labs)).
- **[Gradient Descent Playground](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_1_fundamentals/01_gradient_descent_playground)**
  — jak prosty model regresji liniowej uczy się metodą spadku gradientu, minimalizując błąd
  średniokwadratowy: spadek funkcji straty, zmiany parametrów krok po kroku oraz wpływ
  współczynnika uczenia i szumu w danych. W katalogu: opis (`README.md`) po angielsku, teoria
  (`THEORY.pl.md`) i zadania (`CHALLENGES.pl.md`) po polsku. W aplikacji po polsku i po angielsku.
- **Distance Metrics Lab** — najbliżsi sąsiedzi wybranego punktu przy odległości euklidesowej,
  Manhattan i Czebyszewa oraz to, dlaczego wynik k-NN zależy od metryki. Działa tylko w aplikacji,
  po polsku i po angielsku. Sterowanie:
  [instrukcja, sekcja „Natywne laby Level 1”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-1)
  ([wersja angielska](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.md#app-only-level-1-labs)).
- **[k-NN Vote Map](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_1_fundamentals/02_knn_vote_map)**
  — klasyfikacja metodą k najbliższych sąsiadów: najbliżsi sąsiedzi punktu, głosowanie
  większościowe, obszary decyzyjne oraz wpływ `k` i szumu w danych. W katalogu: opis (`README.md`)
  po angielsku, teoria (`THEORY.pl.md`) i zadania (`CHALLENGES.pl.md`) po polsku. W aplikacji po
  polsku i po angielsku.
- **[Logistic Regression Boundary Lab](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_1_fundamentals/03_logistic_regression_boundary_lab)**
  — klasyfikacja binarna regresją logistyczną: uczenie spadkiem gradientu, prawdopodobieństwo
  klasy, granica decyzyjna zależna od progu, entropia krzyżowa oraz dokładność (accuracy), precyzja
  (precision) i czułość (recall). W katalogu: opis (`README.md`) po angielsku, teoria
  (`THEORY.pl.md`) i zadania (`CHALLENGES.pl.md`) po polsku. W aplikacji po polsku i po angielsku.
- **[Decision Tree Splitter](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_1_fundamentals/04_decision_tree_splitter)**
  — jak drzewo decyzyjne dzieli przestrzeń cech na prostsze obszary: podziały wzdłuż osi,
  nieczystość Giniego, entropia, przyrost informacji, ręczna ocena podziału oraz intuicja
  przeuczenia i niedouczenia. W katalogu: opis (`README.md`) po angielsku, teoria (`THEORY.pl.md`)
  i zadania (`CHALLENGES.pl.md`) po polsku. W aplikacji po polsku i po angielsku.
