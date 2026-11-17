---
title: "Projekt końcowy: wybierz swoje zlecenie"
summary: "Projekt końcowy z data-science-casebook: wybierasz jedno z trzech zleceń klientów i przechodzisz z nim sześć lekcji, od zdefiniowania pytania po notatkę decyzyjną. Lekcje 7 i 8 są opcjonalnymi rozszerzeniami."
status: published
materials:
  - repository: data-science-casebook
    path: README.pl.md
    lang: pl
    label: "Opis kursu i szybki start: instalacja, uruchomienie JupyterLab, budowa lekcji"
  - repository: data-science-casebook
    path: cases/capstone/README.pl.md
    lang: pl
    label: "Projekt końcowy — Wybierz swoje zlecenie: trzy zlecenia i to, co jest inne w projekcie"
tasks:
  lekcja-1:
    materials:
      - repository: data-science-casebook
        path: cases/capstone/lessons/01_defining_the_question/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 1 — Definiowanie pytania"
  lekcja-2:
    materials:
      - repository: data-science-casebook
        path: cases/capstone/lessons/02_data_preparation/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 2 — Przygotowanie danych"
  lekcja-3:
    materials:
      - repository: data-science-casebook
        path: cases/capstone/lessons/03_exploration/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 3 — Eksploracja"
  lekcja-4:
    materials:
      - repository: data-science-casebook
        path: cases/capstone/lessons/04_modeling/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 4 — Modelowanie"
  lekcja-5:
    materials:
      - repository: data-science-casebook
        path: cases/capstone/lessons/05_evaluation/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 5 — Ewaluacja"
  lekcja-6:
    materials:
      - repository: data-science-casebook
        path: cases/capstone/lessons/06_synthesis_decision_note/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 6 — Synteza: notatka decyzyjna"
  lekcja-7:
    optional: true
    materials:
      - repository: data-science-casebook
        path: cases/capstone/lessons/07_packaging_for_deployment/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 7 (opcjonalna) — Pakowanie preprocessingu jako Pipeline"
  lekcja-8:
    optional: true
    materials:
      - repository: data-science-casebook
        path: cases/capstone/lessons/08_explainability_and_limits/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 8 (opcjonalna, tylko LendWell) — Wyjaśnialność i granice"
---
Ten zestaw to projekt końcowy z repozytorium data-science-casebook. W poprzednich case'ach klient
i pytanie były dane. Tym razem wybierasz jedno z trzech zleceń i sam zamieniasz niejasną skargę
klienta w pytanie analityczne. Z wybranym zleceniem przechodzisz sześć podstawowych lekcji, od
zdefiniowania pytania po notatkę decyzyjną. Lekcje 7 i 8 są opcjonalnymi rozszerzeniami, a lekcja 8
dotyczy tylko jednego zlecenia. Osiem zadań odpowiada lekcjom 1–8, w kolejności z repozytorium.

## Wybór zlecenia

Opis projektu podaje trzech klientów z krótkimi zleceniami. Wybierasz jednego w lekcji 1 i
pracujesz z nim przez wszystkie sześć podstawowych lekcji. Nie realizujesz trzech projektów.

| Klient | Plik danych | Zlecenie w opisie projektu |
|---|---|---|
| Riverside Community Clinic | `clinic_wait_times.csv` | pacjenci skarżą się na czas oczekiwania, a klinika nie wie, co na niego wpływa |
| LendWell Financial | `lendwell_loan_default.csv` | pożyczki są zatwierdzane bez systematycznej oceny ryzyka |
| Northfield Retail Group | `retail_store_segments.csv` | sklepy są traktowane w planowaniu tak samo, choć zapewne tworzą naturalne grupy |

Żadne zlecenie nie podaje zmiennej celu, metryki sukcesu ani dokładnego pytania. Te decyzje, razem
z wyborem techniki, podejmujesz sam w lekcji 1.

Od lekcji 2 instrukcje rozróżniają ścieżki. Dwie ścieżki predykcyjne, klinika i LendWell, od
początku dzielą dane na zbiór treningowy i testowy. Ścieżka Northfield nie ma zmiennej celu ani
podziału do ochrony. W notatnikach lekcji 1–7 ustawiasz `DATASET_NAME` na wybrany zbiór; domyślnie
jest tam `clinic_wait_times`.

## Jedno zlecenie, wspólne testy

Na początku projektu wybierasz jedno z trzech zleceń. Analizę danych, notebooki i wnioski
przygotowujesz dla wybranego zlecenia.

Kod ćwiczeń zawiera jednak funkcje obsługujące wszystkie trzy warianty, a `uv run pytest` sprawdza
je wspólnie. Aby uzyskać komplet pozytywnych wyników testów danej lekcji, trzeba zaimplementować
wszystkie sprawdzane przez nie funkcje, również dla pozostałych wariantów.

Jeżeli wykonasz tylko część dotyczącą swojego zlecenia, niektóre testy mogą nadal kończyć się
niepowodzeniem. Nie oznacza to automatycznie, że analiza wybranego zlecenia jest niepoprawna.

W tym projekcie dotyczy to lekcji 2–7. Instrukcja każdej z nich wymienia sprawdzane funkcje w części
„Masz do dyspozycji”.

## Przygotowanie do zestawu

Opis kursu umieszcza projekt końcowy po trzech case'ach. Projekt korzysta z tego samego sposobu
pracy z lekcją co [zestaw 1](case-1-regression.md), [zestaw 2](case-2-classification.md) i
[zestaw 3](case-3-clustering.md), a jego ścieżki odpowiadają ich technikom.

**Instalacja.** Jeśli nie masz jeszcze repozytorium, zainstaluj [uv](https://docs.astral.sh/uv/).
Narzędzie samo pobierze potrzebną wersję Pythona. Potem pobierz repozytorium i zainstaluj
zależności, a do pracy z notatnikami uruchom JupyterLab. Polecenia podaje szybki start w opisie
kursu:

```bash
git clone https://github.com/michalmaj/data-science-casebook.git
cd data-science-casebook
uv sync
uv run jupyter lab
```

**Budowa lekcji.** Każda lekcja jest w osobnym katalogu `cases/capstone/lessons/<NN_nazwa>/` i ma
te same pliki co w case'ach:

- `README.pl.md` (po polsku) albo `README.md` (po angielsku) to instrukcja lekcji;
- `task.py` zawiera funkcje do uzupełnienia, z opisami `TODO` po angielsku;
- `check.py` to testy `pytest`, które sprawdzają Twoje funkcje;
- `lesson.ipynb` to notatnik po angielsku, w którym uruchamiasz swój kod, oglądasz wyniki i
  zapisujesz interpretację.

**Dane.** Trzy pliki CSV w `cases/capstone/data/`, po jednym na klienta: `clinic_wait_times.csv`
(400 wizyt), `lendwell_loan_default.csv` (400 pożyczek) i `retail_store_segments.csv` (250 sklepów).
Każdy ma braki danych, którymi zajmuje się lekcja 2.

## Samodzielna praca i sprawdzanie wyników

Najpierw spróbuj wykonać zadania samodzielnie. Testy pozwalają sprawdzić wybrane elementy kodu,
ale nie zastępują interpretacji wyników ani uzasadnienia wniosków.

Testy każdej lekcji uruchamiasz z jej katalogu poleceniem `uv run pytest`. Sprawdzają one tylko
funkcje z `task.py`, na wszystkich trzech zbiorach danych: w lekcjach 1–3 strukturę i rozsądność
wyników, a od lekcji 4 także dokładne wartości dla zestawów cech sugerowanych w notatnikach. Nie
czytają notatnika `lesson.ipynb`. Jak mówi opis projektu, nie sprawdzają, które zlecenie wybierasz,
czy Twoje pytanie, zmienna celu i metryka są dobre ani czy model, cechy, próg, liczba klastrów i
rekomendacja są właściwe dla Twojego pytania. Te decyzje uzasadniasz sam w komórkach „Your notes”
i w notatce decyzyjnej. Test, który nie przechodzi, wskazuje funkcję, a jego komunikat zwykle mówi,
czego oczekiwał.

Repozytorium źródłowe zawiera również publiczne materiały referencyjne, które można wykorzystać
do porównania po własnej próbie. Ich obecność nie oznacza, że opisane tam rubryki są
automatycznie zasadami zaliczenia tego przedmiotu.

## Materiały

Instrukcje lekcji są po polsku i po angielsku. Kod, testy i notatniki są po angielsku. Instrukcje
projektu końcowego mają części „Decyzja do podjęcia”, „Masz do dyspozycji” i „Uzasadnij” z
pytaniami do notatek, a niektóre także „Zanim zdecydujesz”.

## Zadania

### Definiowanie pytania {#lekcja-1}

**Cel:** wybrać jednego klienta i zamienić jego niejasną skargę w konkretne pytanie analityczne ze
zmienną celu i metryką sukcesu.

**Zakres pracy:** przeczytaj zlecenia w opisie projektu i wybierz jedno. W `task.py` uzupełnij
`list_datasets`, `load_dataset` i `missing_value_counts`. W notatniku wypisz dostępne zbiory,
wczytaj wybrany, sprawdź jego kształt i braki danych i zapisz pytanie, zmienną celu i metrykę.
Zdecyduj też, która technika, regresja, klasyfikacja czy klasteryzacja, pasuje do problemu.

**Rezultat:** w komórce „Your notes” uzasadnienie wyboru zmiennej celu i metryki oraz odpowiedzi na
pytania z części „Uzasadnij”.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza listę trzech zbiorów, kształt i kolumny
każdego z nich, liczbę braków w znanych kolumnach i rozkład wartości `defaulted` w zbiorze LendWell.
Instrukcja zaznacza, że testy nie wiedzą, które zlecenie wybrano, ani czy pytanie jest dobre.

### Przygotowanie danych {#lekcja-2}

**Cel:** świadomie zdecydować, jak uzupełnić braki danych, zamiast mechanicznie powtarzać medianę i
modę z poprzednich case'ów.

**Zakres pracy:** w `task.py` uzupełnij `load_dataset`, `missing_value_counts`, `clean_dataset`,
`split_dataset` i `impute_missing`. W notatniku sprawdź braki przed czyszczeniem. Na ścieżkach
kliniki i LendWell najpierw podziel dane na `train_df` i `test_df`, a potem uzupełnij braki
statystykami z samego `train_df`. Na ścieżce Northfield uruchom `clean_dataset` na całym zbiorze.

**Rezultat:** odpowiedzi w notatkach na pytania o realny powód braków w wybranej kolumnie i o
ryzyko jednej generycznej strategii czyszczenia dla różnych danych.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza liczbę wierszy i braków, to, że
`clean_dataset` usuwa wszystkie braki bez zmiany kształtu i wpisuje znane wartości, rozłączny podział
zbioru LendWell i uzupełnianie braków medianą z samego `train_df`. Nie sprawdza, czy ta strategia
jest właściwa dla Twojego zbioru.

### Eksploracja {#lekcja-3}

**Cel:** zbadać zależności między cechami liczbowymi i wyrobić sobie wstępny, oparty na danych
pogląd, które cechy mają znaczenie dla pytania z lekcji 1.

**Zakres pracy:** w `task.py` uzupełnij `load_dataset`, `split_dataset`, `impute_missing`,
`load_clean_dataset` i `numeric_correlations`. W notatniku, na ścieżkach kliniki i LendWell, użyj
tego samego podziału i uzupełniania co w lekcji 2 i policz macierz korelacji tylko na `train_df`.
Na ścieżce Northfield wczytaj i wyczyść cały zbiór jednym krokiem. Posortuj zależności, żeby
zobaczyć, które się wyróżniają.

**Rezultat:** odpowiedzi w notatkach na pytania, która cecha najbardziej przekonuje, którą kusi
pominąć i co sprawdzić, zanim zdecydujesz.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza kształt zbiorów po `load_clean_dataset`,
kształt i kolumny macierzy korelacji każdego zbioru oraz znane wartości korelacji. Dla ścieżek
kliniki i LendWell są to wartości policzone na części treningowej z `split_dataset`. Testy same
przygotowują tę część, więc nie sprawdzają, czy Twój notatnik patrzy wyłącznie na `train_df`. Tego
pilnujesz sam.

### Modelowanie {#lekcja-4}

**Cel:** dopasować model bazowy i model pasujący do wybranego zbioru i sprawdzić, czy model bije
model bazowy.

**Zakres pracy:** w `task.py` uzupełnij `load_dataset`, `split_dataset`, `impute_missing`,
`scale_features` oraz trzy funkcje dopasowujące, po jednej na technikę:
`fit_regression_baseline_and_model`, `fit_classification_baseline_and_model` i
`fit_clustering_model`. W notatniku ustaw `DATASET_NAME` i uruchom komórkę, która wczytuje, dzieli,
uzupełnia braki, na ścieżce klasteryzacji skaluje i dopasowuje model. Korzystasz w niej z funkcji
dopasowującej, która pasuje do Twojego zbioru. Notatnik podaje sugerowany zestaw cech; możesz
wybrać własny na podstawie lekcji 3.

**Rezultat:** odpowiedzi w notatkach na pytania, o ile model jest lepszy od modelu bazowego i czy
ta różnica ma znaczenie, co sugerowałoby zapamiętywanie zbioru treningowego, a na ścieżce
klasteryzacji także uzasadnienie decyzji o skalowaniu.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza podział i uzupełnianie braków oraz
wszystkie trzy funkcje dopasowujące na sugerowanych zestawach cech, łącznie z dokładnymi
wartościami. Nie sprawdza, czy Twój wybór cech i modelu jest najlepszy dla Twojego pytania.

### Ewaluacja {#lekcja-5}

**Cel:** sprawdzić, czy model faktycznie czegoś się nauczył, i zdecydować, czy wynik jest
wystarczająco dobry, żeby na nim działać.

**Zakres pracy:** w `task.py` uzupełnij siedem funkcji z lekcji 4 i nowe: `evaluate_regression`,
`evaluate_classification` z opcjonalnym progiem, `evaluate_clustering`, `cluster_stability`,
`split_for_validation`, `metrics_at_threshold` i `cluster_metrics_by_k`. W notatniku uruchom
komórkę pasującą do typu problemu. Na ścieżce klasyfikacji próg wybierasz na `val_df` z
`split_for_validation` i dopiero potem raz sprawdzasz go na `test_df`. Na ścieżce klasteryzacji
liczbę klastrów wybierasz, patrząc na inertia, silhouette i stabilność; instrukcja wyjaśnia, że
silhouette liczy się na tych samych danych, na których dopasowano model.

**Rezultat:** odpowiedzi w notatkach na pytania, czy model warto polecić klientowi w obecnej formie,
z wybranym progiem albo liczbą klastrów i uzasadnieniem, oraz co oznaczałaby duża różnica między
wynikiem na zbiorze treningowym i testowym.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza wyniki ewaluacji dla sugerowanych
zestawów cech na wszystkich ścieżkach: błąd modelu i modelu bazowego, metryki klasyfikacji przy
progach 0,5 i 0,3, rozłączny podział walidacyjny, silhouette, metryki dla kolejnych k i
stabilność klastrów. Nie sprawdza, jaki próg albo jaką liczbę klastrów wybierasz ani czy model jest
wystarczająco dobry dla Twojego pytania.

### Synteza: notatka decyzyjna {#lekcja-6}

**Cel:** przełożyć wyniki projektu na rekomendację, z której wybrany klient może skorzystać.

**Zakres pracy:** w `task.py` uzupełnij funkcje z lekcji 4–5 i trzy nowe:
`final_regression_scorecard`, `final_classification_scorecard` z progiem wybranym w lekcji 5 i
`final_clustering_summary`. W notatniku wygeneruj tabelę wyników albo podsumowanie segmentów. Na
ścieżce LendWell ustaw `CHOSEN_THRESHOLD` na próg z lekcji 5, a nie na domyślne 0,5. Potem wypełnij
siedem sekcji notatki decyzyjnej prostym językiem. Szablon notatki ma nagłówki sekcji po angielsku i
po polsku.

**Rezultat:** kompletna notatka decyzyjna, czyli główny rezultat projektu końcowego.

**Sprawdź się:**

- Kod i tabele: `uv run pytest` w katalogu lekcji sprawdza liczby w tabelach wyników i w
  podsumowaniu segmentów dla sugerowanych zestawów cech.
- Notatka decyzyjna: testy jej nie sprawdzają, więc ich przejście nie oznacza, że notatka jest
  poprawna. Jakość interpretacji, argumentacji i wniosków oceniasz samodzielnie: wróć do pytania z
  części „Decyzja do podjęcia” w instrukcji, czyli co klient powinien zrobić i jak bardzo powinien
  być tego pewien, i odpowiedz na pytania z części „Uzasadnij”.

### Pakowanie preprocessingu jako Pipeline {#lekcja-7}

Lekcja opcjonalna, po sześciu podstawowych, dla wszystkich trzech ścieżek. Instrukcja przedstawia
ją jako rundę bonusową bez zadania do wykonania; pytania do notatek są ćwiczeniem.

**Cel:** użyć kolumny kategorycznej, której wcześniejsze lekcje nie używały, i spakować cały
preprocessing w jeden `Pipeline` z `ColumnTransformer`.

**Zakres pracy:** w `task.py` uzupełnij `load_dataset`, `split_dataset` i siedem nowych funkcji:
`build_preprocessor` oraz po jednej funkcji `build_and_fit_*_pipeline` i `evaluate_pipeline_*` na
typ problemu. W notatniku ustaw `DATASET_NAME`, uruchom komórkę, która buduje, dopasowuje i ocenia
`Pipeline`, i porównaj wynik z lekcją 6. Notatnik wyjaśnia, dlaczego mogło zmienić się więcej niż
jedno naraz.

**Rezultat:** opcjonalnie notatki o tym, czy dodana kolumna kategoryczna pomogła modelowi.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza kształt danych po `build_preprocessor`
dla trzech zbiorów i znane wyniki trzech pipeline'ów. Nie sprawdza, czy dodanie kolumny
kategorycznej było dobrym wyborem analitycznym.

### Wyjaśnialność i granice: ścieżka LendWell {#lekcja-8}

Lekcja opcjonalna, tylko dla ścieżki LendWell. Instrukcja zaznacza, że pozostałe ścieżki nie mają
takiej decyzji do wyjaśnienia. Tak jak lekcja 7 nie ma zadania do wykonania; pytania do notatek są
ćwiczeniem.

**Cel:** zobaczyć, które cechy stoją za decyzją modelu o odmowie dla konkretnego wnioskodawcy, i
zastanowić się, czego wymaga odpowiedzialne użycie takiego modelu.

**Zakres pracy:** w `task.py` uzupełnij pięć funkcji z lekcji 4 i dwie nowe: `reason_codes` i
`reason_code_frequency`. W notatniku uruchom komórkę przygotowawczą, wywołaj `reason_codes` dla
wnioskodawcy, któremu model by odmówił, i `reason_code_frequency` na całym zbiorze testowym.

**Rezultat:** opcjonalnie notatka o jednym z pięciu pytań z instrukcji.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza trzy najważniejsze powody odmowy dla
znanego wnioskodawcy, ich kolejność i znak, oraz częstość powodów w zbiorze testowym. Nie sprawdza,
czy model i zestaw cech są właściwym wyborem.

## Oczekiwane rezultaty

- W lekcjach 1–6 funkcje z `task.py` są uzupełnione. Komplet pozytywnych wyników `uv run pytest`
  wymaga wszystkich sprawdzanych funkcji, także dla pozostałych wariantów (zobacz „Jedno zlecenie,
  wspólne testy”).
- W notatnikach lekcji 1–5 komórki „Your notes” zawierają Twoje uzasadnienia dla wybranego zlecenia
  i odpowiedzi na pytania z instrukcji.
- W notatniku lekcji 6 jest kompletna notatka decyzyjna dla wybranego klienta.
- Lekcja 7 i, na ścieżce LendWell, lekcja 8 są opcjonalne.

## Wskazówki

- Najpierw uzupełnij `task.py` i uruchom testy, a dopiero potem otwórz notatnik.
- Jeśli zmienisz `task.py` po zaimportowaniu go w notatniku, zrestartuj kernel albo ponownie
  uruchom komórkę z importem.
- W każdym notatniku lekcji 1–7 sprawdź, czy `DATASET_NAME` wskazuje wybrany zbiór.
- Na ścieżkach kliniki i LendWell kolejne lekcje korzystają z tego samego podziału danych co lekcja
  2, więc wyniki z różnych lekcji dają się porównywać.
