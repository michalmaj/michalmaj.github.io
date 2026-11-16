---
title: "Regresja: TransLine Logistics"
summary: "Case 1 z data-science-casebook w ośmiu lekcjach: od zdefiniowania pytania klienta, przez jakość danych, podział, eksplorację, model bazowy i analizę reszt, po notatkę decyzyjną dla TransLine."
status: published
materials:
  - repository: data-science-casebook
    path: README.pl.md
    lang: pl
    label: "Opis kursu i szybki start: instalacja, uruchomienie JupyterLab, budowa lekcji"
  - repository: data-science-casebook
    path: cases/case_1_regression/README.pl.md
    lang: pl
    label: "Case 1 — Regresja: TransLine Logistics: zlecenie klienta i dane"
tasks:
  lekcja-1:
    materials:
      - repository: data-science-casebook
        path: cases/case_1_regression/lessons/01_defining_the_question/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 1 — Definiowanie pytania"
  lekcja-2:
    materials:
      - repository: data-science-casebook
        path: cases/case_1_regression/lessons/02_data_quality_and_cleaning/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 2 — Jakość danych i czyszczenie"
  lekcja-3:
    materials:
      - repository: data-science-casebook
        path: cases/case_1_regression/lessons/03_train_test_split/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 3 — Podział train/test i zapieczętowana koperta"
  lekcja-4:
    materials:
      - repository: data-science-casebook
        path: cases/case_1_regression/lessons/04_exploratory_data_analysis/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 4 — Eksploracyjna analiza danych"
  lekcja-5:
    materials:
      - repository: data-science-casebook
        path: cases/case_1_regression/lessons/05_baseline_and_first_model/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 5 — Model bazowy i pierwszy model"
  lekcja-6:
    materials:
      - repository: data-science-casebook
        path: cases/case_1_regression/lessons/06_residual_interpretation/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 6 — Interpretacja reszt"
  lekcja-7:
    materials:
      - repository: data-science-casebook
        path: cases/case_1_regression/lessons/07_correlation_vs_prediction_vs_causation/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 7 — Korelacja vs. predykcja vs. przyczynowość"
  lekcja-8:
    materials:
      - repository: data-science-casebook
        path: cases/case_1_regression/lessons/08_synthesis_decision_note/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 8 — Synteza: notatka decyzyjna"
---
Ten zestaw to Case 1 z repozytorium data-science-casebook. Regionalny operator transportowy
TransLine Logistics chce wiedzieć, jak bardzo opóźni się przesyłka i co naprawdę na to wpływa.
Przez osiem lekcji budujesz model regresji szacujący opóźnienie na podstawie informacji znanych
w chwili wysyłki, a na koniec piszesz notatkę decyzyjną dla klienta. Osiem zadań odpowiada
lekcjom 1–8, w kolejności z repozytorium.

## Przygotowanie do zestawu

Kurs zakłada podstawy Pythona i pierwszy kontakt z pojęciami uczenia maszynowego.

**Instalacja.** Zainstaluj [uv](https://docs.astral.sh/uv/). Narzędzie samo pobierze potrzebną
wersję Pythona. Potem pobierz repozytorium i zainstaluj zależności, a do pracy z notatnikami
uruchom JupyterLab. Polecenia podaje szybki start w opisie kursu:

```bash
git clone https://github.com/michalmaj/data-science-casebook.git
cd data-science-casebook
uv sync
uv run jupyter lab
```

**Budowa lekcji.** Każda lekcja jest w osobnym katalogu
`cases/case_1_regression/lessons/<NN_nazwa>/` i ma te same pliki:

- `README.pl.md` (po polsku) albo `README.md` (po angielsku) to instrukcja lekcji;
- `task.py` zawiera funkcje do uzupełnienia, z opisami `TODO` po angielsku;
- `check.py` to testy `pytest`, które sprawdzają Twoje funkcje;
- `lesson.ipynb` to notatnik po angielsku, w którym uruchamiasz swój kod, oglądasz wyniki i
  zapisujesz interpretację.

**Dane.** Wszystkie lekcje korzystają z pliku `cases/case_1_regression/data/transport_delays.csv`
(500 przesyłek) i od lekcji 3 z tego samego podziału na zbiór treningowy i testowy.

## Samodzielna praca i sprawdzanie wyników

Najpierw spróbuj wykonać zadania samodzielnie. Testy pozwalają sprawdzić wybrane elementy kodu,
ale nie zastępują interpretacji wyników ani uzasadnienia wniosków.

Testy każdej lekcji uruchamiasz z jej katalogu poleceniem `uv run pytest`. Test, który nie
przechodzi, wskazuje funkcję, a jego komunikat zwykle mówi, czego oczekiwał.

Repozytorium źródłowe zawiera również publiczne materiały referencyjne, które można wykorzystać
do porównania po własnej próbie. Ich obecność nie oznacza, że opisane tam rubryki są
automatycznie zasadami zaliczenia tego przedmiotu.

## Materiały

Instrukcje lekcji są po polsku i po angielsku. Kod, testy i notatniki są po angielsku. Każda
instrukcja ma części „Po co to robimy”, „Co masz zrobić”, „Na co zwrócić uwagę” i „Sprawdź się”
z pytaniami do notatek.

## Zadania

### Definiowanie pytania {#lekcja-1}

**Cel:** zamienić skargę klienta w pytanie, na które da się odpowiedzieć danymi, i pierwszy raz
krytycznie spojrzeć na dane.

**Zakres pracy:** w `task.py` uzupełnij `load_shipments`, `target_column_name` i
`missing_value_counts`. W notatniku przejrzyj dane, wskaż kolumnę odpowiadającą na pytanie
TransLine i zapisz, które kolumny mają braki.

**Rezultat:** testy lekcji przechodzą, a komórka „Your notes” zawiera Twoje obserwacje o danych i
pytania do klienta, o które prosi instrukcja.

**Sprawdź się:** `uv run pytest` w katalogu lekcji; oczekiwany wynik testów i pytania do notatek
podaje instrukcja.

### Jakość danych i czyszczenie {#lekcja-2}

**Cel:** zdecydować, co zrobić z brakami danych, zależnie od tego, której kolumny dotyczą.

**Zakres pracy:** w `task.py` uzupełnij `load_shipments`, `rows_with_missing_data` i
`drop_missing_weather`. W notatniku sprawdź, których kolumn i wierszy dotyczą braki.

**Rezultat:** decyzja o brakach w obu kolumnach, z uzasadnieniem zapisanym w notatkach.

**Sprawdź się:** `uv run pytest` w katalogu lekcji oraz pytania do notatek z instrukcji.

### Podział train/test i zapieczętowana koperta {#lekcja-3}

**Cel:** wydzielić dane do uczciwej ewaluacji i uzupełniać braki bez przecieku informacji ze zbioru
testowego.

**Zakres pracy:** w `task.py` uzupełnij `load_shipments`, `split_shipments` i
`impute_driver_experience`. W notatniku potwierdź liczności zbiorów podane w instrukcji.

**Rezultat:** podział i uzupełnienie braków, z których korzystają wszystkie kolejne lekcje, oraz
notatka o tym, dlaczego dla uczciwej ewaluacji ma znaczenie, z jakich danych liczysz wartość
uzupełniającą.

**Sprawdź się:** `uv run pytest` w katalogu lekcji oraz pytanie do notatek z instrukcji.

### Eksploracyjna analiza danych {#lekcja-4}

**Cel:** ustalić, co naprawdę wiąże się z opóźnieniem, patrząc tylko na dane, na które wolno
patrzeć.

**Zakres pracy:** w `task.py` uzupełnij funkcje wymienione w instrukcji. Nowe są
`correlation_matrix`, `correlation_with_target` i `mean_delay_by_weather`, a funkcje z
poprzednich lekcji uzupełniasz ponownie. W notatniku obejrzyj rozkłady i korelacje.

**Rezultat:** lista cech, które weźmiesz do modelu, i tych, które pominiesz, z jednym zdaniem
uzasadnienia dla każdej.

**Sprawdź się:** `uv run pytest` w katalogu lekcji oraz pytania do notatek z instrukcji.

### Model bazowy i pierwszy model {#lekcja-5}

**Cel:** sprawdzić, czy regresja liniowa przewiduje opóźnienie lepiej niż proste zgadywanie, na
przesyłkach, których model nie widział.

**Zakres pracy:** w `task.py` uzupełnij funkcje wymienione w instrukcji: modele bazowe
(`predict_zero_baseline`, `predict_mean_baseline`), miary błędu (`mean_absolute_error`,
`root_mean_squared_error`) i model (`fit_model`, `predict_delay`) oraz funkcje z poprzednich
lekcji. W notatniku porównaj modele bazowe i model na zbiorze testowym.

**Rezultat:** porównanie modelu z modelami bazowymi i notatka o tym, o ile minut MAE model jest
lepszy od sprawiedliwego modelu bazowego.

**Sprawdź się:** `uv run pytest` w katalogu lekcji oraz pytania do notatek z instrukcji.

### Interpretacja reszt {#lekcja-6}

**Cel:** sprawdzić, czy błędy modelu są przypadkowe, czy mają wzorzec.

**Zakres pracy:** w `task.py` uzupełnij nowe funkcje `compute_residuals`,
`mean_residual_by_weather` i `residual_correlation_with_feature` oraz funkcje z poprzednich
lekcji wymienione w instrukcji. W notatniku przeanalizuj reszty.

**Rezultat:** opis prostym językiem, co model robi źle i dla jakich przesyłek, oraz jedna
propozycja poprawki, która nie wymaga nowych danych.

**Sprawdź się:** `uv run pytest` w katalogu lekcji oraz pytanie do notatek z instrukcji.

### Korelacja vs. predykcja vs. przyczynowość {#lekcja-7}

**Cel:** odróżnić współczynniki, na których można oprzeć rekomendację, od tych, których nie wolno
interpretować.

**Zakres pracy:** w `task.py` uzupełnij nowe funkcje `fit_model_on` i `coefficient_for` oraz
funkcje z poprzednich lekcji wymienione w instrukcji. W notatniku porównaj współczynniki
wytrenowane w różnych zestawach cech.

**Rezultat:** dla wybranego czynnika oddzielone to, co wiesz na pewno, od tego, czego się tylko
domyślasz.

**Sprawdź się:** `uv run pytest` w katalogu lekcji oraz pytania do notatek z instrukcji.

### Synteza: notatka decyzyjna {#lekcja-8}

**Cel:** przełożyć wyniki całego case'u na rekomendację, z której kierownik operacyjny TransLine
może skorzystać.

**Zakres pracy:** w `task.py` uzupełnij nową funkcję `final_scorecard` oraz funkcje z poprzednich
lekcji wymienione w instrukcji. W notatniku wygeneruj tabelę wyników i wypełnij siedem sekcji
notatki decyzyjnej prostym językiem.

**Rezultat:** kompletna notatka decyzyjna, czyli główny rezultat całego Case 1.

**Sprawdź się:**

- Kod i tabela wyników: `uv run pytest` w katalogu lekcji sprawdza wczytanie i podział danych
  oraz układ i liczby w tabeli wyników.
- Notatka decyzyjna: testy jej nie sprawdzają, więc ich przejście nie oznacza, że notatka jest
  poprawna. Jakość interpretacji, argumentacji i wniosków oceniasz samodzielnie: wróć do części
  „Na co zwrócić uwagę” w instrukcji i odpowiedz na pytanie z części „Sprawdź się”.

## Oczekiwane rezultaty

- W każdej lekcji testy uruchamiane poleceniem `uv run pytest` przechodzą.
- W notatnikach lekcji 1–7 komórki „Your notes” zawierają Twoje interpretacje i odpowiedzi na
  pytania z instrukcji.
- W notatniku lekcji 8 jest kompletna notatka decyzyjna dla TransLine.

## Wskazówki

- Najpierw uzupełnij `task.py` i doprowadź do przejścia testów, a dopiero potem otwórz notatnik.
- Jeśli zmienisz `task.py` po zaimportowaniu go w notatniku, zrestartuj kernel albo ponownie
  uruchom komórkę z importem.
- Sekcja „Na co zwrócić uwagę” w każdej instrukcji opisuje typowe pułapki danej lekcji.
- Lekcje przechodzisz po kolei, w porządku numerycznym katalogów.
