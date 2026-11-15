---
title: "Materiały przedmiotu"
summary: "Interactive ML Labs w wersji alfa: pięć prowadzonych ścieżek nauki z interaktywnymi demami, a uzupełniająco studia przypadków klasyfikacji i grupowania. Materiały są po polsku i po angielsku, część tylko w jednym z tych języków."
status: published
order: 1
materials:
  - repository: interactive-ml-labs
    path: docs/student_alpha_v0_0_9a.pl.md
    lang: pl
    label: "Notatki dla studentów do wersji alfa v0.0.9a: od nich zaczynasz"
  - repository: interactive-ml-labs
    path: USAGE.pl.md
    lang: pl
    label: "Instrukcja: instalacja, uruchamianie i sterowanie"
  - repository: interactive-ml-labs
    path: README.md
    lang: en
    label: "Opis projektu i bieżący stan prac"
  - repository: data-science-casebook
    path: README.pl.md
    lang: pl
    label: "Uzupełniająco: data-science-casebook — opis kursu i szybki start"
  - repository: data-science-casebook
    path: cases/case_2_classification/README.pl.md
    lang: pl
    label: "Uzupełniająco: Case 2 — Klasyfikacja: Meridian Outlet"
  - repository: data-science-casebook
    path: cases/case_3_clustering/README.pl.md
    lang: pl
    label: "Uzupełniająco: Case 3 — Grupowanie: Aurora Stream"
---
Aplikacja Interactive ML Labs ma interfejs po polsku i po angielsku. Języki dokumentacji są różne:

- **po polsku i po angielsku:** notatki dla studentów i instrukcja Interactive ML Labs oraz opisy
  kursu, studiów przypadków i lekcji w data-science-casebook;
- **tylko po angielsku:** opis repozytorium Interactive ML Labs, opisy pojedynczych dem oraz
  notebooki i kod w data-science-casebook;
- **tylko po polsku:** teoria i zadania przy sześciu demach Interactive ML Labs.

Ta strona wskazuje punkty wejścia i nie zawiera tłumaczeń.

## Materiał główny: Interactive ML Labs (wersja alfa)

Interactive ML Labs to aplikacja uruchamiana na własnym komputerze (Python, Pygame). Algorytmy
uczenia maszynowego poznajesz w niej przez interaktywne wizualizacje: zmieniasz ważne parametry,
obserwujesz, co robi model, i wyjaśniasz wynik. W lekcjach nie piszesz kodu.

**Status:** najnowsze wydanie,
[v0.0.9a](https://github.com/michalmaj/interactive-ml-labs/releases/tag/v0.0.9a), repozytorium
opisuje jako pierwszą wersję alfa przeznaczoną dla studentów. Projekt jest dalej rozwijany. Notatki
do wydania wymieniają znane ograniczenia, między innymi:

- aplikację uruchamia się poleceniem `uv run`, a instalatory są dopiero planowane;
- niektóre tematy są celowo uproszczone: Data Leakage Lab korzysta ze stałych scenariuszy wyników,
  a t-SNE / UMAP Exploration Lab z koncepcyjnych przykładów zamiast pełnych implementacji tych
  algorytmów.

Jak pracować z aplikacją:

- **Od czego zacząć:** przygotuj środowisko (Python 3.12 lub nowszy i uv) i uruchom aplikację według
  instrukcji. Notatki dla studentów opisują zalecaną trasę: wybór języka, mapa kursu, pierwsza
  ścieżka nauki, wprowadzenie do lekcji, teoria i zadania w demie.
- **Mapa kursu** w aplikacji poleca kolejność ścieżek. Wszystkie 27 dem z trzech poziomów można też
  przeglądać swobodnie, przez wybór poziomu.

### Ścieżki nauki w aplikacji

- **Jak modele uczą się z błędu** — od błędów dopasowania prostej, przez minimalizowanie funkcji
  straty i granice klasyfikacji, po boosting, który skupia się na wcześniejszych pomyłkach.
  Laboratoria: Linear Regression Line Fit Lab, Gradient Descent Playground, Logistic Regression
  Boundary Lab, Boosting Mistake Lab.
- **Od odległości do klastrów** — od wyboru metryki odległości, przez głosowanie najbliższych
  sąsiadów, po grupowanie twarde i miękkie. Laboratoria: Distance Metrics Lab, k-NN Vote Map,
  K-Means Intro Lab, Clustering Lab, Gaussian Mixture Intro Lab.
- **Od dobrych wyników do zaufanych modeli** — od uczciwej walidacji, przez wyciek danych i
  kompromisy między metrykami, po kalibrację pewności modelu i monitorowanie po wdrożeniu.
  Laboratoria: Train / Validation / Test Split Lab, Data Leakage Lab, Class Imbalance Lab,
  Calibration Lab, Model Monitoring Drift Lab.
- **Od cech do decyzji modelu** — od skali i sygnału cech, przez reguły drzewa decyzyjnego i
  głosowanie lasu losowego, po porównanie założeń różnych rodzin modeli. Laboratoria: Feature
  Scaling Lab, Feature Importance Lab, Decision Tree Splitter, Random Forest Bagging Lab, Model
  Comparison Lab.
- **Od reprezentacji do zachowania modelu** — od redukcji wymiarowości i embeddingów, przez
  kalibrację i monitorowanie, po prognozowanie szeregów czasowych. Laboratoria: PCA Lab, t-SNE /
  UMAP Exploration Lab, Calibration Lab, Model Monitoring Drift Lab, Time Series Forecasting Lab.

Lekcje o kalibracji i monitorowaniu należą do dwóch ścieżek.

### Dema z teorią i zadaniami

Sześć dem ma w repozytorium własny katalog z opisem demo (`README.md`, po angielsku), teorią
(`THEORY.pl.md`) i zadaniami z pytaniami kontrolnymi (`CHALLENGES.pl.md`), oba po polsku. Te dema
można uruchomić także osobno, bez aplikacji; polecenia są w plikach z zadaniami.

- [Gradient Descent Playground](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_1_fundamentals/01_gradient_descent_playground)
  — ścieżka „Jak modele uczą się z błędu”
- [k-NN Vote Map](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_1_fundamentals/02_knn_vote_map)
  — ścieżka „Od odległości do klastrów”
- [Logistic Regression Boundary Lab](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_1_fundamentals/03_logistic_regression_boundary_lab)
  — ścieżka „Jak modele uczą się z błędu”
- [Decision Tree Splitter](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_1_fundamentals/04_decision_tree_splitter)
  — ścieżka „Od cech do decyzji modelu”
- [Random Forest Bagging Lab](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_2_practical_ml/01_random_forest_bagging_lab)
  — ścieżka „Od cech do decyzji modelu”
- [Boosting Mistake Lab](https://github.com/michalmaj/interactive-ml-labs/tree/main/demos/level_2_practical_ml/02_boosting_mistake_lab)
  — ścieżka „Jak modele uczą się z błędu”

## Materiały uzupełniające: studia przypadków z data-science-casebook

Dwa studia przypadków pokazują klasyfikację i grupowanie na realistycznych danych, w pełnym cyklu
analitycznym: od pytania klienta, przez przygotowanie danych i model, po notatkę decyzyjną z rekomendacją dla klienta. W
odróżnieniu od Interactive ML Labs tu piszesz kod (Python, pandas, scikit-learn) i pracujesz w
notebookach.

- **Case 2 — Klasyfikacja: Meridian Outlet** — model szacujący ryzyko zwrotu zamówienia (regresja
  logistyczna). W danych zwrotem kończy się 14% zamówień, więc case zajmuje się rzadką klasą, wyborem progu
  decyzyjnego i doborem metryki. W aplikacji te zagadnienia pokazują między innymi Logistic
  Regression Boundary Lab i Class Imbalance Lab.
- **Case 3 — Grupowanie: Aurora Stream** — segmentacja subskrybentów serwisu streamingowego metodą
  k-średnich: wybór liczby klastrów, interpretacja segmentów i ich stabilność. W aplikacji
  grupowanie pokazują między innymi K-Means Intro Lab i Clustering Lab.
- **Jak zacząć:** przygotuj środowisko według sekcji „Szybki start” w opisie kursu. Opis Case 2
  zakłada, że sposób pracy z lekcjami (plik do uzupełnienia, testy, notebook) znasz z Case 1; ten
  sposób opisuje też „Szybki start”.
