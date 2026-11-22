---
title: "Od cech do decyzji modelu"
summary: "Czwarta prowadzona ścieżka nauki w aplikacji Interactive ML Labs (wersja alfa): pięć lekcji, od skali i sygnału cech, przez splity drzewa decyzyjnego i głosowanie Random Forest, po porównanie założeń różnych rodzin modeli. W każdej lekcji wykonujesz dwa zadania w demie."
status: published
materials:
  - repository: interactive-ml-labs
    path: docs/student_alpha_v0_0_9a.pl.md
    lang: pl
    label: "Notatki dla studentów do wersji alfa v0.0.9a: zalecana trasa przez aplikację"
  - repository: interactive-ml-labs
    path: USAGE.pl.md
    lang: pl
    label: "Instrukcja: instalacja, uruchamianie i sterowanie"
tasks:
  feature-decision-tree-split:
    materials:
      - repository: interactive-ml-labs
        path: demos/level_1_fundamentals/04_decision_tree_splitter/THEORY.pl.md
        lang: pl
        label: "Teoria do dema Decision Tree Splitter"
      - repository: interactive-ml-labs
        path: demos/level_1_fundamentals/04_decision_tree_splitter/CHALLENGES.pl.md
        lang: pl
        label: "Zadania do dema Decision Tree Splitter (poza aplikacją)"
  feature-decision-forest-vote:
    materials:
      - repository: interactive-ml-labs
        path: demos/level_2_practical_ml/01_random_forest_bagging_lab/THEORY.pl.md
        lang: pl
        label: "Teoria do dema Random Forest Bagging Lab"
      - repository: interactive-ml-labs
        path: demos/level_2_practical_ml/01_random_forest_bagging_lab/CHALLENGES.pl.md
        lang: pl
        label: "Zadania do dema Random Forest Bagging Lab (poza aplikacją)"
---
Ten zestaw prowadzi przez czwartą ścieżkę nauki aplikacji Interactive ML Labs, „Od cech do decyzji
modelu”. Mapa kursu w aplikacji pokazuje ją jako krok 4, po ścieżce z
[zestawu 3](from-good-scores-to-trustworthy-models.md). Ścieżka ma pięć lekcji, a każda lekcja to
jedno zadanie tego zestawu. W lekcji uruchamiasz demo i wykonujesz dwa zadania, które aplikacja
pokazuje na liście „Zadania lekcji”. Nie piszesz kodu. Ta strona nie zastępuje lekcji: podaje, gdzie
je znaleźć, co w nich zrobić i co aplikacja sprawdza. Nazwy ekranów, zadań i przycisków są tu takie,
jak w polskiej wersji aplikacji. Nazwy dem i część pojęć aplikacja zostawia po angielsku.

## Status aplikacji

Interactive ML Labs jest w wersji alfa i jest dalej rozwijana. Najnowsze wydanie,
[v0.0.9a](https://github.com/michalmaj/interactive-ml-labs/releases/tag/v0.0.9a) z 20 września
2026 r., repozytorium opisuje jako pierwszą alfę przeznaczoną dla studentów. Wydanie nie ma paczek
instalacyjnych: aplikację uruchamia się z kodu repozytorium.

Gałąź `main` zawiera późniejsze zmiany, które nie weszły jeszcze do żadnego wydania: samoocenę na
ekranie ukończenia lekcji i ekran „Raport postępu”. Lekcje tej ścieżki, ich zadania i sposób
zaliczania są w v0.0.9a i na `main` takie same. W kolejnych wersjach nazwy i działanie zadań mogą
się zmienić.

## Przygotowanie do zestawu

Instalację i uruchomienie opisuje część
[„Przygotowanie do zestawu”](how-models-learn-from-error.md#przygotowanie-do-zestawu) zestawu 1.
W skrócie: aplikacja działa na Twoim komputerze, w osobnym oknie programu (Pygame), i wymaga
Pythona 3.12 lub nowszego oraz narzędzia uv. W katalogu głównym repozytorium instalujesz
zależności i uruchamiasz aplikację:

```bash
uv sync
uv run --package interactive-ml-labs-app interactive-ml-labs
```

Postęp zapisany przy wcześniejszych ścieżkach zostaje.

## Gdzie znajdziesz ścieżkę

1. Na pierwszym ekranie wybierz „Polski”, a na ekranie startowym „Prowadzone ścieżki nauki”.
2. W „Mapie kursu” wybierz „Krok 4: Od cech do decyzji modelu”. Zobaczysz listę pięciu lekcji.
3. Wybierz lekcję. Na ekranie intro `Enter` uruchamia demo, a `T` otwiera teorię.

Po ukończeniu ścieżek z zestawów 1–3 ekran startowy proponuje pierwszą lekcję tej ścieżki, a
klawisz `C` od razu ją otwiera. Nawigacja, ekran „Lekcja ukończona” i pauza działają tak samo jak
w zestawie 1. Lekcje otwieraj przez „Prowadzone ścieżki nauki”. To samo demo uruchomione przez
„Przeglądaj dema według poziomu” nie zapisuje postępu lekcji. Każdą lekcję możesz otworzyć od razu,
choć aplikacja poleca kolejność z listy.

Ta ścieżka nie ma lekcji wspólnych z innymi ścieżkami.

## Postęp w aplikacji a zrozumienie tematu

Zasady są te same co w zestawie 1, opisane w części
[„Postęp w aplikacji a zrozumienie tematu”](how-models-learn-from-error.md#postep-w-aplikacji-a-zrozumienie-tematu).
W skrócie:

- **Wykonanie działań.** Każde zadanie lekcji mówi, co zrobić w demie i na co patrzeć.
- **Oznaczenie postępu.** Aplikacja odhacza zadanie (`[x]`) po konkretnej czynności w demie: po
  naciśnięciu klawisza albo zmianie ustawienia. W tej ścieżce żadne zadanie nie wymaga osiągnięcia
  konkretnego wyniku. Przy każdej lekcji niżej opisano, co odhacza zadanie i czego aplikacja nie
  sprawdza.
- **Zrozumienie tematu.** Aplikacja nie sprawdza obserwacji ani wniosków. Na przykład zadanie
  „Rozpoznaj rozjazd założeń” zostaje odhaczone po zmianie danych i parametru, a aplikacja nie
  sprawdza, czy wskazano założenie modelu. Ukończona lekcja nie potwierdza więc opanowania tematu.

Ekran „Lekcja ukończona” zadaje pytanie do przemyślenia („Zatrzymaj się na chwilę”) i podpowiada, na
co zwrócić uwagę. W tej ścieżce podpowiedź jest osobna dla każdej lekcji. Pod nią są dwa pytania
sprawdzające: czy umiesz własnymi słowami wyjaśnić cel lekcji i czy umiesz nazwać widoczny sygnał z
dema, który go potwierdził. Na `main` ta część ma nagłówek „Mini-check”, a w v0.0.9a „Sprawdź
rozumienie”. Pytania służą refleksji i nie są oceniane. Na `main` wybór „Rozumiem” albo „Do
powtórki” w części „Samoocena” jest Twoją deklaracją, której aplikacja nie sprawdza. W v0.0.9a w
tym miejscu jest „Szybki self-check” z dwiema stałymi wskazówkami, bez przycisków.

## Materiały

Aplikacja ma interfejs po polsku i po angielsku. Notatki dla studentów i instrukcja są po polsku i
po angielsku.

Dwa dema tej ścieżki mają w repozytorium własny katalog: Decision Tree Splitter i Random Forest
Bagging Lab. W każdym jest opis dema (`README.md`, po angielsku) oraz teoria (`THEORY.pl.md`) i
rozszerzone zadania z pytaniami kontrolnymi (`CHALLENGES.pl.md`), po polsku. Linki do teorii i
zadań są przy lekcjach.

Pliki z zadaniami opisują samodzielne uruchomienie dema poza aplikacją, poleceniami podanymi w
pliku. W tej wersji demo w aplikacji i poza nią ma to samo sterowanie, z wyjątkiem `Esc`: poza
aplikacją zamyka okno, a w aplikacji otwiera pauzę.
Zadania z tych plików nie zastępują zadań lekcji, a aplikacja ich nie odhacza. Pozostałe trzy dema
są wbudowane w aplikację. Ich sterowanie opisuje instrukcja, a teorię każdej lekcji otwierasz
klawiszem `T`.

## Zadania

### Zauważ, kiedy skala steruje modelem (Feature Scaling Lab) {#feature-decision-scaling}

**Cel:** według aplikacji zrozumieć, że model dostaje liczby, więc cecha o większym zakresie może
przed scalingiem dominować distance, coefficients albo optymalizację.

**Zakres pracy:** demo pokazuje zakresy dwóch cech przed scalingiem i po nim. Panel „Kontrola
scaling” podaje scenariusz, model, stan scaling, accuracy, iterations, range ratio i diagnozę.
`1`–`3` zmieniają scenariusz („Income vs age”, „Pixel intensity vs count”, „Jednostki sensorów”),
`S` włącza i wyłącza scaling, `M` przełącza model (k-NN, Logistic Regression, Gradient Descent), a
`R` resetuje podgląd. Demo zaczyna bez scalingu. Zadania lekcji:

- **Włącz i wyłącz scaling:** przełącz scaling i porównaj surowe zakresy cech z widokiem po
  scalingu. Wskazówka w aplikacji: wartości mogą opisywać sensowne cechy, ale ich jednostki nadal
  mają znaczenie.
- **Porównaj zachowanie wrażliwe na skalę:** po włączeniu scaling przełącz modele i zauważ, jak
  zmienia się wynik albo zbieżność.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 2”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-2).

**Rezultat:** „Włącz i wyłącz scaling” zostaje odhaczone po pierwszym `S`, bo demo zaczyna bez
scalingu. „Porównaj zachowanie wrażliwe na skalę” zostaje odhaczone, gdy w tym uruchomieniu dema
scaling był choć raz włączony i oglądano co najmniej dwa modele. Kolejność się nie liczy: w kontroli
`M` naciśnięte przed włączeniem scalingu, a potem `S` odhaczyły oba zadania naraz. Aplikacja nie
sprawdza, czy porównano accuracy i iterations.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Która cecha dominowała przed scalingiem i co
zmieniło się, gdy zakresy stały się porównywalne?”. Podpowiedź: „Scaling nie jest kosmetyką:
zmienia geometrię albo sygnał optymalizacji, który dostaje model”. Pytania sprawdzające proszą o
wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema.

### Ostrożnie czytaj sygnał z cech (Feature Importance Lab) {#feature-decision-importance}

**Cel:** według aplikacji zrozumieć, że feature importance może pokazać użyteczny sygnał, ale
korelacja, leakage i niestabilne rankingi mogą zniekształcić obraz.

**Zakres pracy:** demo pokazuje ranking cech według importance wraz ze stability. Panel
„Interpretacja” podaje scenariusz, metodę, top feature, top score, stability, korelację i diagnozę.
`1`–`3` zmieniają scenariusz („Skorelowane cechy”, „Podejrzenie leakage”, „Niestabilny ranking”),
`M` przełącza permutation importance i model importance, `C` pokazuje albo ukrywa grupy korelacji,
`L` pokazuje albo ukrywa ostrzeżenie leakage, a `R` resetuje lab. Zadania lekcji:

- **Porównaj metody importance:** przełącz permutation i model importance, a potem porównaj, które
  cechy zmieniają pozycję.
- **Sprawdź zniekształcony sygnał:** wejdź w scenariusz z korelacją, leakage albo niestabilnym
  rankingiem i nazwij, czemu najwyższy słupek nie mówi wszystkiego. Wskazówka w aplikacji:
  importance wyjaśnia zachowanie modelu, a nie automatycznie przyczynowość.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 2”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-2).

**Rezultat:** „Porównaj metody importance” zostaje odhaczone po pierwszym `M`. „Sprawdź
zniekształcony sygnał” zostaje odhaczone po naciśnięciu `1`–`3`, `C` albo `L`, gdy bieżący
scenariusz pokazuje korelację, leakage albo niestabilny ranking. Każdy z trzech scenariuszy dema
jest takim przypadkiem, więc wystarcza pierwsze takie naciśnięcie, nawet numer bieżącego
scenariusza. Aplikacja nie sprawdza, czy nazwano powód ostrożności.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Która cecha wyglądała na najmocniejszą i co kazało
Ci uważać, żeby nie traktować rankingu zbyt dosłownie?”. Podpowiedź: „Feature importance jest
wskazówką o zachowaniu modelu. Nadal wymaga kontekstu: skąd są dane, czy cechy są skorelowane i czy
nie ma leakage”. Pytania sprawdzające proszą o wyjaśnienie celu lekcji własnymi słowami i o
wskazanie sygnału z dema.

### Zbuduj decyzję z pytań o cechy (Decision Tree Splitter) {#feature-decision-tree-split}

**Cel:** według aplikacji zrozumieć, że decision tree przewiduje wynik przez sekwencję prostych
pytań o cechę i threshold.

**Zakres pracy:** demo ma dwa tryby: automatyczne drzewo („auto”) i ręczny split („manual”). Panel
podaje tryb, dataset (`axis_aligned` albo `xor`), criterion (Gini albo entropy), max depth,
accuracy, liczbę węzłów i liści, szum i seed. W trybie automatycznym pokazuje też regułę i gain
pierwszego splitu, a w ręcznym regułę, poprawność, gain i impurity Twojego splitu. Część „Cel”
pokazuje status, accuracy i głębokość względem celu dema. `M` przełącza tryb, `Up` / `Down`
zmieniają max depth, `Left` / `Right` szum, `D` dataset, `G` criterion, `F` cechę ręcznego splitu,
`Q` / `E` przesuwają jego threshold, `S` losuje nowy seed, a `R` resetuje układ. Zadania lekcji:

- **Przesuń split drzewa:** przełącz tryb manual split, zmień cechę albo threshold i zobacz, jak
  rozdzielają się klasy. Wskazówka w aplikacji: split to po prostu pytanie, czy ta cecha jest
  poniżej albo powyżej danej wartości.
- **Sprawdź pierwszy split:** zmień criterion albo max depth i odczytaj, jak pierwszy split zmienia
  strukturę drzewa.

Według teorii dema cel to accuracy co najmniej 0.95 przy max depth najwyżej 1 dla `axis_aligned`
i najwyżej 2 dla `xor`. To cel dema, a nie warunek zadań lekcji.

**Rezultat:** „Przesuń split drzewa” zostaje odhaczone po pierwszym naciśnięciu `M`, `F`, `Q` albo
`E`. Tryb ręczny nie jest wymagany: w kontroli `Q` w trybie automatycznym odhaczyło zadanie, a tryb
został „auto”. „Sprawdź pierwszy split” zostaje odhaczone po pierwszym naciśnięciu `G`, `Up` albo
`Down`. Aplikacja nie sprawdza, czy odczytano pierwszy split.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Jakie pytanie o cechę i threshold drzewo zadało
jako pierwsze i jak to pytanie rozdzieliło dane?”. Podpowiedź: „Decyzje drzewa są czytelne, bo
każdy split jest lokalną regułą, ale finalna predykcja nadal zależy od sekwencji reguł”. Pytania
sprawdzające proszą o wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema. Plik z
zadaniami do dema prowadzi przez dane `axis_aligned` i XOR, Gini, entropy i information gain,
ręczny split, decision stump, wpływ max depth i challenge. Ma też pytania kontrolne. Zadanie
dodatkowe w tym pliku prosi o zaprojektowanie własnego challenge. To część materiału dema, a ta
strona nie robi z niego wymagania.

### Stabilizuj decyzje przez głosowanie (Random Forest Bagging Lab) {#feature-decision-forest-vote}

**Cel:** według aplikacji zrozumieć, jak random forest łączy wiele drzew, żeby niestabilne decyzje
pojedynczego drzewa zamienić w stabilniejsze głosowanie.

**Zakres pracy:** demo pokazuje obok siebie pojedyncze drzewo („Single tree baseline”) i głosowanie
Random Forest. Kółka to punkty train, kwadraty punkty test, a X błędny punkt test. Panel podaje
dataset, szum, seed, liczbę drzew, max depth, bootstrap ratio i stan confidence view, train i test
accuracy oraz gap obu modeli. Część „Cel” pokazuje cel dema: test accuracy lasu co najmniej 0.90,
najwyżej 25 drzew i gap najwyżej 0.15. `Up` / `Down` zmieniają liczbę drzew, `W` / `S` max depth,
`Left` / `Right` szum, `B` / `V` bootstrap ratio, `D` dataset, `C` włącza i wyłącza confidence view,
`N` losuje nowy seed, a `R` resetuje układ. Zadania lekcji:

- **Porównaj jedno drzewo z Random Forest:** zmień liczbę drzew i porównaj wynik pojedynczego
  drzewa z głosowaniem Random Forest.
- **Sprawdź confidence Random Forest:** włącz confidence view i zmień bootstrap albo noise, żeby
  znaleźć miejsca, gdzie głosowanie jest mniej pewne. Wskazówka w aplikacji: majority vote może być
  poprawny, a jednocześnie mieć niską zgodność.

**Rezultat:** „Porównaj jedno drzewo z Random Forest” zostaje odhaczone po pierwszym `Up` albo
`Down`. „Sprawdź confidence Random Forest” zostaje odhaczone po włączeniu confidence view. Demo
zaczyna z wyłączonym widokiem, więc wystarcza pierwsze `C`. Zmiana bootstrap albo szumu nie jest
wymagana. Aplikacja nie sprawdza, czy porównano wyniki ani czy znaleziono mniej pewne miejsca.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Gdzie Random Forest wyglądał stabilniej niż jedno
drzewo i gdzie confidence view nadal pokazywał niepewność?”. Podpowiedź: „Random Forest nie usuwa
niepewności. Pokazuje ją przez głosy, confidence i porównanie modeli”. Pytania sprawdzające proszą o
wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema. Plik z zadaniami do dema ma
ćwiczenia z wersją tekstową (CLI) i z wizualizacją, a także ćwiczenia bez uruchamiania dema, z
bootstrap sampling i głosowaniem. Dotyczą one między innymi liczby drzew, max depth, szumu,
confidence view i challenge. Plik ma też pytania kontrolne i zadanie dodatkowe z własnym challenge,
którego ta strona nie robi wymaganiem.

### Porównaj założenia modeli (Model Comparison Lab) {#feature-decision-model-comparison}

**Cel:** według aplikacji zrozumieć, że różne rodziny modeli mogą podejmować różne decyzje na tych
samych danych, bo ich założenia kształtują decision boundary.

**Zakres pracy:** demo pokazuje decision boundary Logistic Regression, k-NN i Decision Tree na tych
samych punktach. Panel „Modele i wynik” podaje dla każdego modelu train i test accuracy oraz
parametr: threshold, k albo depth. Pod nim jest parametr aktywnego modelu i krótkie podsumowanie
błędów testowych (TP, FP, FN, TN, precision i recall). `1`, `2` i `3` wybierają Logistic
Regression, k-NN i Decision Tree, `-` / `=` zmieniają parametr aktywnego modelu, `D` zmienia preset
danych, `A` pokazuje albo ukrywa nieaktywne granice, `E` pokazuje albo ukrywa błędnie
sklasyfikowane punkty testowe, a `R` resetuje podgląd. Zadania lekcji:

- **Porównaj rodziny modeli:** sprawdź Logistic Regression, k-NN i Decision Tree na tym samym
  zbiorze danych.
- **Rozpoznaj rozjazd założeń:** zmień dataset i parametr modelu, a potem wskaż, które założenie
  modelu najlepiej tłumaczy widoczny spór. Wskazówka w aplikacji: słabszy score często podpowiada,
  że założenie modelu nie pasuje do danych.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 3”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-3).
W aplikacji to demo należy do poziomu 3.

**Rezultat:** „Porównaj rodziny modeli” zostaje odhaczone, gdy w tym uruchomieniu dema wybrano
wszystkie trzy modele. Demo zaczyna od Logistic Regression, więc wystarczą `2` i `3`. „Rozpoznaj
rozjazd założeń” zostaje odhaczone po co najmniej jednej zmianie presetu danych (`D`) i jednym
naciśnięciu `-`, `=` albo `E`, w dowolnej kolejności. `E` się liczy, choć nie zmienia parametru
modelu, tylko pokazuje albo ukrywa błędne punkty. Aplikacja nie sprawdza, czy wskazano założenie
modelu.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Która rodzina modeli najbardziej się różniła i
które założenie pomogło zrozumieć ten spór?”. Podpowiedź: „Porównanie modeli to nie tylko wybór
najwyższego score. To także dopasowanie założeń do kształtu danych”. Pytania sprawdzające proszą o
wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema.

## Oczekiwane rezultaty

- Na liście lekcji wszystkie pięć lekcji ma `[x]`, a mapa kursu pokazuje krok 4 jako ukończony.
  Ekran „Ścieżka ukończona” pokazuje 5/5 lekcji, 10/10 zadań i 5/5 odznak.
- Na pytania z ekranów „Lekcja ukończona” odpowiadasz własnymi słowami. Aplikacja tych odpowiedzi
  nie sprawdza.

## Wskazówki

- Notatki dla studentów radzą otwierać teorię, kiedy potrzebujesz kontekstu: `T` w demie albo na
  ekranie intro. Teoria lekcji ma mini-zadania, których aplikacja nie odhacza. W Feature Importance
  Lab proponuje na przykład decyzję, czy cechę `future_status` trzeba usunąć, zanim zaufasz modelowi.
- W demach tej ścieżki `S` ma różne znaczenia: w Feature Scaling Lab włącza i wyłącza scaling, w
  Decision Tree Splitter losuje nowy seed, a w Random Forest Bagging Lab zmniejsza max depth.
  Ustawienia aplikacji `S` otwiera tylko poza demem.
- Ekran „Ścieżka ukończona” proponuje jako kolejną ścieżkę „Od reprezentacji do zachowania modelu”,
  opisaną w [zestawie 5](from-representation-to-model-behavior.md).
