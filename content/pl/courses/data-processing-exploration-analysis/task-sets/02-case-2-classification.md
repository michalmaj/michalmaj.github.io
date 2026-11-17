---
title: "Klasyfikacja: Meridian Outlet"
summary: "Case 2 z data-science-casebook w ośmiu lekcjach: od wieloarkuszowego Excela, przez niezbalansowane klasy, pierwszy klasyfikator i dobór progu, po przedziały ryzyka i notatkę decyzyjną dla Meridian Outlet."
status: published
materials:
  - repository: data-science-casebook
    path: README.pl.md
    lang: pl
    label: "Opis kursu i szybki start: instalacja, uruchomienie JupyterLab, budowa lekcji"
  - repository: data-science-casebook
    path: cases/case_2_classification/README.pl.md
    lang: pl
    label: "Case 2 — Klasyfikacja: Meridian Outlet: zlecenie klienta i dane"
tasks:
  lekcja-1:
    materials:
      - repository: data-science-casebook
        path: cases/case_2_classification/lessons/01_defining_the_question/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 1 — Definiowanie pytania"
  lekcja-2:
    materials:
      - repository: data-science-casebook
        path: cases/case_2_classification/lessons/02_data_wrangling_multi_sheet_excel/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 2 — Porządkowanie danych: wielo-arkuszowy Excel"
  lekcja-3:
    materials:
      - repository: data-science-casebook
        path: cases/case_2_classification/lessons/03_exploratory_data_analysis_for_classification/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 3 — Eksploracyjna analiza danych do klasyfikacji"
  lekcja-4:
    materials:
      - repository: data-science-casebook
        path: cases/case_2_classification/lessons/04_imbalanced_classes_and_baseline/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 4 — Niezbalansowane klasy i model bazowy"
  lekcja-5:
    materials:
      - repository: data-science-casebook
        path: cases/case_2_classification/lessons/05_train_test_split_and_first_classifier/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 5 — Podział na train/test i pierwszy klasyfikator"
  lekcja-6:
    materials:
      - repository: data-science-casebook
        path: cases/case_2_classification/lessons/06_threshold_selection_and_metric_choice/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 6 — Dobór progu i wybór metryki"
  lekcja-7:
    materials:
      - repository: data-science-casebook
        path: cases/case_2_classification/lessons/07_communicating_uncertainty/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 7 — Komunikowanie niepewności"
  lekcja-8:
    materials:
      - repository: data-science-casebook
        path: cases/case_2_classification/lessons/08_synthesis_decision_note/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 8 — Synteza: notatka decyzyjna"
---
Ten zestaw to Case 2 z repozytorium data-science-casebook. Sklep internetowy Meridian Outlet ma
za dużo zwrotów i chce wiedzieć, które zamówienia są ryzykowne, zanim je wyśle. Przez osiem lekcji
budujesz model klasyfikacyjny, który szacuje ryzyko zwrotu na podstawie informacji dostępnych w
chwili zamówienia, wybierasz próg decyzyjny, a na koniec piszesz notatkę decyzyjną dla klienta.
Osiem zadań odpowiada lekcjom 1–8, w kolejności z repozytorium.

## Przygotowanie do zestawu

Case 2 zakłada, że znasz sposób pracy z lekcją z [zestawu 1](case-1-regression.md): opis case'u
zaznacza, że go nie powtarza. Nowe jest to, że zmienna celu jest binarna i rzadka, a klasyfikator
potrzebuje świadomie wybranego progu decyzyjnego.

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

**Budowa lekcji.** Każda lekcja jest w osobnym katalogu
`cases/case_2_classification/lessons/<NN_nazwa>/` i ma te same pliki co w Case 1:

- `README.pl.md` (po polsku) albo `README.md` (po angielsku) to instrukcja lekcji;
- `task.py` zawiera funkcje do uzupełnienia, z opisami `TODO` po angielsku;
- `check.py` to testy `pytest`, które sprawdzają Twoje funkcje;
- `lesson.ipynb` to notatnik po angielsku, w którym uruchamiasz swój kod, oglądasz wyniki i
  zapisujesz interpretację.

**Dane.** Wszystkie lekcje korzystają z pliku `cases/case_2_classification/data/orders.xlsx`.
To eksport Excela z dwoma arkuszami, „Orders” i „Customers”, przygotowany dla człowieka, a nie dla
skryptu. Do jego wczytania potrzebny jest pakiet `openpyxl`, który `uv sync` instaluje razem z
pozostałymi zależnościami. Od lekcji 5 wszystkie lekcje korzystają z tego samego podziału na zbiór
treningowy i testowy.

## Samodzielna praca i sprawdzanie wyników

Najpierw spróbuj wykonać zadania samodzielnie. Testy pozwalają sprawdzić wybrane elementy kodu,
ale nie zastępują interpretacji wyników ani uzasadnienia wniosków.

Testy każdej lekcji uruchamiasz z jej katalogu poleceniem `uv run pytest`. Sprawdzają one tylko
funkcje z `task.py`: ich wyniki na danych Meridian Outlet, takie jak kształty tabel, nazwy kolumn i
znane wartości. Nie czytają notatnika `lesson.ipynb`. Interpretacji wyników, uzasadnienia decyzji,
na przykład wyboru progu, ani odpowiedzi w komórkach „Your notes” testy nie sprawdzają. Test, który
nie przechodzi, wskazuje funkcję, a jego komunikat zwykle mówi, czego oczekiwał.

Repozytorium źródłowe zawiera również publiczne materiały referencyjne, które można wykorzystać
do porównania po własnej próbie. Ich obecność nie oznacza, że opisane tam rubryki są
automatycznie zasadami zaliczenia tego przedmiotu.

## Materiały

Instrukcje lekcji są po polsku i po angielsku. Kod, testy i notatniki są po angielsku. Każda
instrukcja ma części „Po co to robimy”, „Co masz zrobić” i „Sprawdź się” z pytaniami do notatek,
a większość także część „Na co zwrócić uwagę”.

## Zadania

### Definiowanie pytania {#lekcja-1}

**Cel:** ustalić, co dokładnie Meridian Outlet chce przewidywać, i zobaczyć, w jakim stanie jest
eksport z Excela.

**Zakres pracy:** w `task.py` uzupełnij `list_sheet_names`, `load_raw_orders_sheet` i
`target_column_name`. W notatniku wypisz nazwy arkuszy, wczytaj arkusz „Orders” z domyślnymi
ustawieniami pandas i przyjrzyj się nazwom kolumn i kształtowi. Potwierdź, że mimo bałaganu da się
wskazać kolumnę celu.

**Rezultat:** w komórce „Your notes” konkretny opis tego, co jest nie tak z surowym wczytaniem, i
odpowiedź na pytanie z instrukcji o dwa dodatkowe wiersze.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza nazwy arkuszy, kształt i pierwszą
kolumnę surowego wczytania oraz nazwę kolumny celu. Odpowiedzi w notatkach porównujesz z pytaniami
z instrukcji.

### Porządkowanie danych: wielo-arkuszowy Excel {#lekcja-2}

**Cel:** poprawnie wczytać oba arkusze i połączyć je w jedną tabelę zamówień.

**Zakres pracy:** w `task.py` uzupełnij `load_customers` i `load_and_merge_orders`. W notatniku
wczytaj arkusz „Customers” i potwierdź, że jego kolumna identyfikatora pasuje do `customer_id` z
arkusza „Orders”. Potem wczytaj i połącz arkusz „Orders”, porównaj kształt i kolumny z surowym
wczytaniem z lekcji 1 i potwierdź, że połączona tabela nie ma braków danych i ma stopę zwrotów z
instrukcji.

**Rezultat:** połączona tabela zamówień oraz odpowiedzi w notatkach na pytania o kolejność zmiany
nazwy kolumny i łączenia arkuszy i o to, co po cichu przestałoby działać przy zmianie eksportu.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza tabelę klientów (kształt, nazwy kolumn,
brak braków) i połączoną tabelę: kształt, kolejność kolumn, brak braków, liczbę i udział zwrotów oraz
jeden znany wiersz. Odpowiedzi w notatkach porównujesz z pytaniami z instrukcji.

### Eksploracyjna analiza danych do klasyfikacji {#lekcja-3}

**Cel:** ocenić, jak rzadkie są zwroty i które zapisane czynniki faktycznie się z nimi wiążą,
zanim powstanie jakikolwiek klasyfikator.

**Zakres pracy:** w `task.py` uzupełnij `load_and_merge_orders`, `class_balance`,
`return_rate_by_category` i `correlation_with_return`. W notatniku sprawdź udział obu klas, stopę
zwrotów w kategoriach produktów i korelację ze zwrotem dla `discount_percent`,
`previous_returns_count` i `account_age_days`.

**Rezultat:** odpowiedzi w notatkach na pytania o to, co jest nie tak z oceną klasyfikatora tylko
na podstawie accuracy, i o accuracy modelu, który zawsze przewiduje „brak zwrotu”.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza liczbę wierszy, udział obu klas, stopy
zwrotów i kolejność kategorii oraz wartości trzech korelacji i to, która z nich jest najsilniejsza.
Odpowiedzi w notatkach porównujesz z pytaniami z instrukcji.

### Niezbalansowane klasy i model bazowy {#lekcja-4}

**Cel:** zbudować model bazowy, który zawsze przewiduje klasę większościową, i zobaczyć, co ukrywa
jego accuracy.

**Zakres pracy:** w `task.py` uzupełnij `load_and_merge_orders`, `predict_majority_baseline`,
`accuracy` i `confusion_counts`. W notatniku potwierdź, że model bazowy przewiduje tę samą wartość
dla każdego zamówienia, porównaj jego accuracy z udziałem klas z lekcji 3 i zwróć uwagę na `tp` i
`fn` w macierzy pomyłek.

**Rezultat:** odpowiedzi w notatkach na pytania o to, dlaczego wysoka accuracy jest tu myląca, i
co warto by powiedzieć Meridian Outlet, gdyby to był jedyny dostępny model.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza, że model bazowy przewiduje tę samą
wartość dla każdego wiersza, jego accuracy i cztery liczby macierzy pomyłek. Odpowiedzi w notatkach
porównujesz z pytaniami z instrukcji.

### Podział na train/test i pierwszy klasyfikator {#lekcja-5}

**Cel:** podzielić dane, dopasować `LogisticRegression` na trzech cechach liczbowych z lekcji 3 i
sprawdzić, co robi z nim domyślny próg 0,5, bez zaglądania do zbioru testowego.

**Zakres pracy:** w `task.py` uzupełnij `load_and_merge_orders`, `split_orders`,
`split_orders_by_customer`, `fit_classifier` i `predict_return`. W notatniku przejdź sześć kroków
z instrukcji: od podziału 80/20, przez demonstracyjny podział `fit_df`/`val_df` wewnątrz
`train_df`, współczynniki modelu, macierz pomyłek i prawdopodobieństwa w próbie treningowej, po
porównanie podziału wierszowego z podziałem po kliencie. `test_df` powstaje w tej lekcji i zostaje
odłożony: nie czytasz jego zawartości do końca notatnika. Instrukcja wyjaśnia też, że główny tok
case'u odpowiada na pytanie o kolejne zamówienia klientów, których sklep już zna, a nie o zupełnie
nowych klientów.

**Rezultat:** odpowiedzi w notatkach na pytania o to, czy model jest bezużyteczny, czy próg 0,5
jest zły, dlaczego wyniki obu podziałów są bliskie i co stanie się po obniżeniu progu.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza:

- rozmiary i liczby zwrotów w podziale 80/20;
- rozmiary podziału po kliencie i to, że żaden klient nie jest po obu stronach;
- liczbę klientów wspólnych w podziale wierszowym;
- to, że podziały pomocnicze nie mają wspólnych wierszy z `test_df`;
- model z trzema cechami i macierz pomyłek w próbie treningowej przy progu 0,5.

Testy nie widzą notatnika, więc nie wykryją, że notatnik czyta `test_df`. Tego pilnujesz sam, a
odpowiedzi w notatkach porównujesz z pytaniami z instrukcji.

### Dobór progu i wybór metryki {#lekcja-6}

**Cel:** wybrać próg decyzyjny świadomie, łącząc precision i recall z kosztem fałszywego alarmu i
przeoczonego zwrotu.

**Zakres pracy:** w `task.py` uzupełnij `load_and_merge_orders`, `split_orders`,
`split_for_validation`, `fit_classifier`, `predict_at_threshold` i `classification_metrics`. W
notatniku porównaj progi 0,5, 0,3 i 0,2 na `val_df`, a nie na `test_df`. Dopiero w ostatniej
komórce douczasz model na pełnym `train_df` i jeden raz sprawdzasz wybrany próg na `test_df`.
Komórka ma domyślnie próg 0,2 i komentarz, żeby zastąpić go własnym wyborem.

**Rezultat:** w notatkach próg, który warto polecić Meridian Outlet, uzasadniony kosztem obu
rodzajów błędów, oraz porównanie wyniku na `test_df` z tym, co przewidziała walidacja.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza rozmiary podziałów, liczbę zamówień
oflagowanych przy trzech progach na `val_df`, precision, recall i F1 przy progach 0,5 i 0,2 na
`val_df` oraz wyniki modelu douczonego na `train_df` przy progu 0,2 na `test_df`. Testy nie
sprawdzają, który próg wybierasz ani jak go uzasadniasz.

### Komunikowanie niepewności {#lekcja-7}

**Cel:** zamienić prawdopodobieństwa w przedziały ryzyka Low, Medium i High i sprawdzić, czy te
przedziały odpowiadają rzeczywistemu ryzyku zwrotu.

**Zakres pracy:** w `task.py` uzupełnij `load_and_merge_orders`, `split_orders`, `fit_classifier`,
`risk_tier`, `risk_report`, `tier_summary` i `brier_score`. W notatniku odtwórz podział i model z
lekcji 5–6, zbuduj `risk_report` dla zbioru testowego, porównaj rzeczywistą stopę zwrotów w
przedziałach i przewidywane prawdopodobieństwo z rzeczywistym (`tier_summary`). Wynik `brier_score`
porównaj z modelem bazowym, który zawsze przewiduje stopę zwrotów ze zbioru treningowego.

**Rezultat:** odpowiedzi w notatkach na pytania o stopy zwrotów w przedziałach, kalibrację
przedziału High i o to, jak przekazać tę niepewność Meridian Outlet.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza granice przedziałów w `risk_tier`,
kształt `risk_report` i liczebność przedziałów, stopy zwrotów w przedziałach, kolumny i wartości
`tier_summary` oraz wartość `brier_score`. Porównania z modelem bazowym w notatniku testy nie
obejmują, a odpowiedzi w notatkach porównujesz z pytaniami z instrukcji.

### Synteza: notatka decyzyjna {#lekcja-8}

**Cel:** przełożyć wyniki całego case'u na rekomendację, z której menedżer operacyjny Meridian
Outlet może skorzystać.

**Zakres pracy:** w `task.py` uzupełnij nową funkcję `final_scorecard` oraz `load_and_merge_orders`,
`split_orders` i `fit_classifier`. Tabela wyników zestawia na tych samych danych testowych model
bazowy, model przy progu 0,5 i model przy progu 0,2. W notatniku wygeneruj tabelę i wypełnij pod nią
siedem sekcji notatki decyzyjnej prostym językiem. Szablon notatki ma nagłówki sekcji po angielsku i
po polsku.

**Rezultat:** kompletna notatka decyzyjna, czyli główny rezultat całego Case 2.

**Sprawdź się:**

- Kod i tabela wyników: `uv run pytest` w katalogu lekcji sprawdza wczytanie i podział danych,
  model oraz układ i liczby w tabeli wyników.
- Notatka decyzyjna: testy jej nie sprawdzają, więc ich przejście nie oznacza, że notatka jest
  poprawna. Jakość interpretacji, argumentacji i wniosków oceniasz samodzielnie: wróć do części
  „Na co zwrócić uwagę” w instrukcji i odpowiedz na pytanie z części „Sprawdź się”.

## Oczekiwane rezultaty

- W każdej lekcji testy uruchamiane poleceniem `uv run pytest` przechodzą.
- W notatnikach lekcji 1–7 komórki „Your notes” zawierają Twoje interpretacje i odpowiedzi na
  pytania z instrukcji.
- W notatniku lekcji 8 jest kompletna notatka decyzyjna dla Meridian Outlet.

## Wskazówki

- Najpierw uzupełnij `task.py` i doprowadź do przejścia testów, a dopiero potem otwórz notatnik.
- Jeśli zmienisz `task.py` po zaimportowaniu go w notatniku, zrestartuj kernel albo ponownie
  uruchom komórkę z importem.
- Kolejne lekcje powtarzają funkcje z poprzednich, na przykład `load_and_merge_orders`. Każda lekcja
  ma własny `task.py`, więc uzupełniasz je w każdej lekcji, w której pojawiają się na liście.
- Lekcje przechodzisz po kolei, w porządku numerycznym katalogów.
