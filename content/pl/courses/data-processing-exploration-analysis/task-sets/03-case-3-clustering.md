---
title: "Grupowanie: Aurora Stream"
summary: "Case 3 z data-science-casebook w ośmiu lekcjach: od zapytań SQL do bazy SQLite, przez skalowanie cech i KMeans, wybór liczby klastrów, interpretację i stabilność segmentów, po notatkę decyzyjną dla Aurora Stream."
status: published
materials:
  - repository: data-science-casebook
    path: README.pl.md
    lang: pl
    label: "Opis kursu i szybki start: instalacja, uruchomienie JupyterLab, budowa lekcji"
  - repository: data-science-casebook
    path: cases/case_3_clustering/README.pl.md
    lang: pl
    label: "Case 3 — Grupowanie: Aurora Stream: zlecenie klienta i dane"
tasks:
  lekcja-1:
    materials:
      - repository: data-science-casebook
        path: cases/case_3_clustering/lessons/01_defining_the_question/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 1 — Definiowanie pytania"
  lekcja-2:
    materials:
      - repository: data-science-casebook
        path: cases/case_3_clustering/lessons/02_feature_selection_and_scaling/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 2 — Dobór i skalowanie cech"
  lekcja-3:
    materials:
      - repository: data-science-casebook
        path: cases/case_3_clustering/lessons/03_exploratory_data_analysis_for_clustering/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 3 — Eksploracyjna analiza danych do grupowania"
  lekcja-4:
    materials:
      - repository: data-science-casebook
        path: cases/case_3_clustering/lessons/04_why_segment_first_kmeans_attempt/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 4 — Po co segmentować? Pierwsza próba z KMeans"
  lekcja-5:
    materials:
      - repository: data-science-casebook
        path: cases/case_3_clustering/lessons/05_choosing_k_comparing_solutions/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 5 — Wybór k: porównanie rozwiązań"
  lekcja-6:
    materials:
      - repository: data-science-casebook
        path: cases/case_3_clustering/lessons/06_interpreting_and_naming_segments/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 6 — Interpretacja i nazywanie segmentów"
  lekcja-7:
    materials:
      - repository: data-science-casebook
        path: cases/case_3_clustering/lessons/07_segment_stability_and_overinterpretation_risk/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 7 — Stabilność segmentów i ryzyko nadinterpretacji"
  lekcja-8:
    materials:
      - repository: data-science-casebook
        path: cases/case_3_clustering/lessons/08_synthesis_decision_note/README.pl.md
        lang: pl
        label: "Instrukcja: Lekcja 8 — Synteza: notatka decyzyjna"
---
Ten zestaw to Case 3 z repozytorium data-science-casebook. Serwis streamingowy Aurora Stream chce
zrozumieć, jakich ma subskrybentów, żeby dopasować oferty retencyjne zamiast traktować wszystkich
tak samo. Przez osiem lekcji budujesz segmentację subskrybentów metodą `KMeans` na podstawie ich
zachowania podczas oglądania, sprawdzasz, jak stabilne są segmenty, a na koniec piszesz notatkę
decyzyjną dla klienta. Osiem zadań odpowiada lekcjom 1–8, w kolejności z repozytorium.

## Przygotowanie do zestawu

Opis kursu układa case'y w kolejności Case 1, Case 2, Case 3, z coraz mniejszym wsparciem. Case 3
korzysta z tego samego sposobu pracy z lekcją co [zestaw 1](case-1-regression.md) i
[zestaw 2](case-2-classification.md), ale daje mniej podpowiedzi przy interpretacji. Nowe jest to,
że nie ma tu zmiennej celu ani klasycznego podziału na zbiór treningowy i testowy. Pytanie nie
brzmi, jak trafny jest model, ale czy proponowany podział subskrybentów jest stabilny,
interpretowalny i wystarczająco użyteczny, żeby na nim działać.

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
`cases/case_3_clustering/lessons/<NN_nazwa>/` i ma te same pliki co w poprzednich case'ach:

- `README.pl.md` (po polsku) albo `README.md` (po angielsku) to instrukcja lekcji;
- `task.py` zawiera funkcje do uzupełnienia, z opisami `TODO` po angielsku;
- `check.py` to testy `pytest`, które sprawdzają Twoje funkcje;
- `lesson.ipynb` to notatnik po angielsku, w którym uruchamiasz swój kod, oglądasz wyniki i
  zapisujesz interpretację.

**Dane.** Wszystkie lekcje korzystają z bazy SQLite `cases/case_3_clustering/data/aurora_stream.sqlite`
z tabelami `subscribers` i `sessions`. Tabelę gotową do analizy wyciągasz zapytaniem SQL z
połączeniem tabel (JOIN) i agregacją. Opis case'u nazywa to główną nową umiejętnością techniczną
tego case'u.

## Samodzielna praca i sprawdzanie wyników

Najpierw spróbuj wykonać zadania samodzielnie. Testy pozwalają sprawdzić wybrane elementy kodu,
ale nie zastępują interpretacji wyników ani uzasadnienia wniosków.

Testy każdej lekcji uruchamiasz z jej katalogu poleceniem `uv run pytest`. Sprawdzają one tylko
funkcje z `task.py`: ich wyniki na danych Aurora Stream, takie jak kształty tabel, nazwy kolumn i
znane wartości. Nie czytają notatnika `lesson.ipynb`. Interpretacji wyników, uzasadnienia decyzji,
na przykład wyboru liczby segmentów i ich nazw, ani odpowiedzi w komórkach „Your notes” testy nie
sprawdzają. Test, który nie przechodzi, wskazuje funkcję, a jego komunikat zwykle mówi, czego
oczekiwał.

Repozytorium źródłowe zawiera również publiczne materiały referencyjne, które można wykorzystać
do porównania po własnej próbie. Ich obecność nie oznacza, że opisane tam rubryki są
automatycznie zasadami zaliczenia tego przedmiotu.

## Materiały

Instrukcje lekcji są po polsku i po angielsku. Kod, testy i notatniki są po angielsku. Każda
instrukcja ma części „Po co to robimy”, „Co masz zrobić” i „Sprawdź się” z pytaniami do notatek.
Niektóre instrukcje mają też część „Na co zwrócić uwagę” albo dodatkowe objaśnienia, na przykład o
redundancji cech w lekcji 3 i o rodzajach stabilności w lekcji 7.

## Zadania

### Definiowanie pytania {#lekcja-1}

**Cel:** zbudować z dwóch tabel bazy jedną tabelę cech, w której każdy wiersz opisuje jednego
subskrybenta.

**Zakres pracy:** w `task.py` uzupełnij `list_tables` i `load_subscriber_features`. Druga funkcja
łączy i agreguje obie tabele zapytaniem SQL. W notatniku wypisz tabele, wczytaj tabelę cech i
zobacz, którzy subskrybenci nie mają żadnej sesji, a potem zdecyduj, co to oznacza.

**Rezultat:** odpowiedzi w notatkach na pytanie o skutek użycia INNER JOIN zamiast LEFT JOIN i
uzasadniona decyzja, co zrobić z subskrybentami bez sesji. Instrukcja zaznacza, że nie ma tu jednej
słusznej odpowiedzi.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza nazwy tabel, kształt i kolumny tabeli
cech, wartości dla subskrybentów bez sesji (zera zamiast braków danych) i jeden znany wiersz.
Odpowiedzi w notatkach porównujesz z pytaniami z instrukcji.

### Dobór i skalowanie cech {#lekcja-2}

**Cel:** sprowadzić cztery cechy opisujące zachowanie subskrybenta do wspólnej skali, zanim trafią
do algorytmu opartego na odległości.

**Zakres pracy:** w `task.py` uzupełnij `load_subscriber_features` i `scale_features`. W notatniku
wczytaj ponownie tabelę cech, przeskaluj cztery cechy behawioralne i potwierdź, że mają średnią 0 i
odchylenie standardowe 1.

**Rezultat:** odpowiedzi w notatkach na pytania, dlaczego `plan_tier` i `country` nie są
skalowane i która cecha zdominowałaby odległość przed skalowaniem.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza kształt i kolumny przeskalowanej
tabeli, średnią i odchylenie standardowe każdej z czterech cech oraz jeden znany wiersz. Odpowiedzi
w notatkach porównujesz z pytaniami z instrukcji.

### Eksploracyjna analiza danych do grupowania {#lekcja-3}

**Cel:** sprawdzić, czy cztery cechy niosą cztery różne sygnały, czy niektóre opowiadają tę samą
historię.

**Zakres pracy:** w `task.py` uzupełnij `load_scaled_features` i `feature_correlations`. W
notatniku policz macierz korelacji czterech cech i przyjrzyj się, jak `tenure_days` odnosi się do
pozostałych. Instrukcja pokazuje też, że jedna z cech jest dokładnie wyliczana z dwóch innych.

**Rezultat:** odpowiedzi w notatkach na pytania, co silna korelacja trzech cech mówi o liczbie
różnych sygnałów i które dwie liczby wybrać do opisu subskrybentów.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza kształt tabeli, macierz korelacji 4 × 4
z jedynkami na przekątnej, dwie znane wartości korelacji, silną korelację trzech cech dotyczących
oglądania i ich słaby związek z `tenure_days`. Odpowiedzi w notatkach porównujesz z pytaniami z
instrukcji.

### Po co segmentować? Pierwsza próba z KMeans {#lekcja-4}

**Cel:** dopasować pierwszy model KMeans z liczbą klastrów przyjętą na razie bez uzasadnienia i
zobaczyć, co z tego wynika.

**Zakres pracy:** w `task.py` uzupełnij `load_scaled_features` i `fit_kmeans`. W notatniku dopasuj
model z domyślnym `k=4`, sprawdź bezwładność (inertia) i liczbę subskrybentów w każdym klastrze.

**Rezultat:** odpowiedzi w notatkach na pytania, co sprawdzić przed zbudowaniem oferty wokół
jednego z mniejszych klastrów i co dla rekomendacji oznacza nieuzasadnione `k=4`.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza liczbę klastrów i kształt ich
środków, wartość inertia, liczebności klastrów i to, że wynik jest powtarzalny. Odpowiedzi w
notatkach porównujesz z pytaniami z instrukcji.

### Wybór k: porównanie rozwiązań {#lekcja-5}

**Cel:** porównać rozwiązania dla różnych liczb klastrów i sprawdzić, czy metoda łokcia i
silhouette score wskazują to samo.

**Zakres pracy:** w `task.py` uzupełnij `load_scaled_features`, `cluster_metrics_by_k` i
`compare_feature_sets`. W notatniku policz inertia i silhouette score dla k od 2 do 8, a potem
porównaj przy `k=2` i `k=4` segmentację na pełnym zestawie cech i na zestawie zredukowanym
(`REDUCED_FEATURE_COLUMNS`).

**Rezultat:** odpowiedzi w notatkach na pytania o poleganie na jednej metryce, o wpływ wyboru cech
na tę odpowiedź i o rekomendację, gdy dwie standardowe metody wyboru k się nie zgadzają.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza:

- kształt tabeli metryk i listę wartości k;
- znane wartości inertia i silhouette;
- spadek inertia ze wzrostem k i położenie szczytu silhouette;
- nieregularny przebieg silhouette po szczycie;
- wyniki porównania zestawów cech przy `k=2` i `k=4`.

Odpowiedzi w notatkach porównujesz z pytaniami z instrukcji.

### Interpretacja i nazywanie segmentów {#lekcja-6}

**Cel:** opisać, co odróżnia dwa segmenty rozwiązania `k=2`, i nadać im nazwy, których użyłby
ktoś z biznesu.

**Zakres pracy:** w `task.py` uzupełnij `load_scaled_features`, która tym razem zachowuje cechy w
oryginalnych jednostkach i przeskalowane, oraz `segment_profiles`. W notatniku porównaj trzy cechy
intensywności oglądania i `tenure_days` w obu klastrach i sprawdź, czy poziom planu lub kraj
pokrywają się z klastrami, choć grupowanie ich nie widziało.

**Rezultat:** w notatkach nazwy obu segmentów, propozycja innego postępowania z każdym z nich i
odpowiedź na pytanie, na jakie różnice między subskrybentami ta segmentacja może być ślepa.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza kolumny wczytanej tabeli, kształt
profili, średnią liczbę sesji i liczebność obu segmentów, wyraźną różnicę w cechach oglądania i
niewielką różnicę stażu. Nazw segmentów ani rekomendacji testy nie sprawdzają.

### Stabilność segmentów i ryzyko nadinterpretacji {#lekcja-7}

**Cel:** sprawdzić, czy segmenty przetrwają inną próbkę subskrybentów i inny losowy start KMeans,
zanim Aurora Stream oprze na nich strategię retencji.

**Zakres pracy:** w `task.py` uzupełnij `load_scaled_features`, `subsample_stability`,
`initialization_stability` i `stability_comparison_table`. W notatniku sprawdź stabilność na
podpróbkach dla `k=2` i `k=4`, stabilność względem inicjalizacji dla k od 2 do 5 i tabelę
porównawczą dla tych samych k. Instrukcja rozróżnia cztery pytania nazywane „stabilnością”, w tym
stabilność w czasie, o której te dane nic nie mówią.

**Rezultat:** odpowiedzi w notatkach na pytania, skąd bierze się dodatkowa kruchość `k=4` i co
jeszcze trzeba by sprawdzić, zanim podział na dwa segmenty uzna się za trwały fakt.

**Sprawdź się:** `uv run pytest` w katalogu lekcji sprawdza:

- kształt i kolumny wyników obu badań stabilności;
- pełną zgodność podpróbek dla `k=2` i znane wartości dla `k=4`;
- to, że `k=2` jest stabilniejsze od `k=4`;
- pełną stabilność względem inicjalizacji dla k od 2 do 5;
- kolumny i wartości tabeli porównawczej.

Odpowiedzi w notatkach porównujesz z pytaniami z instrukcji.

### Synteza: notatka decyzyjna {#lekcja-8}

**Cel:** przełożyć wyniki całego case'u na rekomendację, z której zespół retencji Aurora Stream
może skorzystać.

**Zakres pracy:** w `task.py` uzupełnij `load_scaled_features` i nową funkcję
`final_segment_table`, która zestawia profile cech, liczebności i udziały obu segmentów. W
notatniku wygeneruj tabelę segmentów i wypełnij pod nią siedem sekcji notatki decyzyjnej prostym
językiem. Szablon notatki ma nagłówki sekcji po angielsku i po polsku.

**Rezultat:** kompletna notatka decyzyjna, czyli główny rezultat całego Case 3.

**Sprawdź się:**

- Kod i tabela segmentów: `uv run pytest` w katalogu lekcji sprawdza wczytanie danych oraz układ i
  liczby w tabeli segmentów.
- Notatka decyzyjna: testy jej nie sprawdzają, więc ich przejście nie oznacza, że notatka jest
  poprawna. Jakość interpretacji, argumentacji i wniosków oceniasz samodzielnie: wróć do części
  „Na co zwrócić uwagę” w instrukcji i odpowiedz na pytanie z części „Sprawdź się”.

## Oczekiwane rezultaty

- W każdej lekcji testy uruchamiane poleceniem `uv run pytest` przechodzą.
- W notatnikach lekcji 1–7 komórki „Your notes” zawierają Twoje interpretacje i odpowiedzi na
  pytania z instrukcji.
- W notatniku lekcji 8 jest kompletna notatka decyzyjna dla Aurora Stream.

## Wskazówki

- Najpierw uzupełnij `task.py` i doprowadź do przejścia testów, a dopiero potem otwórz notatnik.
- Jeśli zmienisz `task.py` po zaimportowaniu go w notatniku, zrestartuj kernel albo ponownie
  uruchom komórkę z importem.
- Kolejne lekcje powtarzają funkcje z poprzednich, na przykład `load_scaled_features`. Każda lekcja
  ma własny `task.py`, więc uzupełniasz je w każdej lekcji, w której pojawiają się na liście.
- Lekcje przechodzisz po kolei, w porządku numerycznym katalogów.
