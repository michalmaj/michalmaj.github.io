---
title: "Od dobrych wyników do zaufanych modeli"
summary: "Trzecia prowadzona ścieżka nauki w aplikacji Interactive ML Labs (wersja alfa): pięć lekcji, od podziału na train, validation i test, przez leakage i metryki przy niezbalansowanych klasach, po kalibrację i monitoring modelu po wdrożeniu. W każdej lekcji wykonujesz dwa zadania w demie."
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
---
Ten zestaw prowadzi przez trzecią ścieżkę nauki aplikacji Interactive ML Labs, „Od dobrych wyników
do zaufanych modeli”. Mapa kursu w aplikacji pokazuje ją jako krok 3, po ścieżkach z
[zestawu 1](how-models-learn-from-error.md) i [zestawu 2](from-distance-to-clusters.md). Ścieżka
ma pięć lekcji, a każda lekcja to jedno zadanie tego zestawu. W lekcji uruchamiasz demo i
wykonujesz dwa zadania, które aplikacja pokazuje na liście „Zadania lekcji”. Nie piszesz kodu. Ta
strona nie zastępuje lekcji: podaje, gdzie je znaleźć, co w nich zrobić i co aplikacja sprawdza.
Nazwy ekranów, zadań i przycisków są tu takie, jak w polskiej wersji aplikacji. Nazwy dem i część
pojęć aplikacja zostawia po angielsku.

Dwie ostatnie lekcje tej ścieżki, o kalibracji i o monitoringu, należą też do ścieżki z
[zestawu 5](from-representation-to-model-behavior.md). Jak aplikacja zapisuje ich postęp, opisuje
część [„Lekcje wspólne z zestawem 5”](#lekcje-wspolne-z-zestawem-5).

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
2. W „Mapie kursu” wybierz „Krok 3: Od dobrych wyników do zaufanych modeli”. Zobaczysz listę pięciu
   lekcji.
3. Wybierz lekcję. Na ekranie intro `Enter` uruchamia demo, a `T` otwiera teorię.

Po ukończeniu ścieżek z zestawów 1 i 2 ekran startowy proponuje pierwszą lekcję tej ścieżki, a
klawisz `C` od razu ją otwiera. Nawigacja, ekran „Lekcja ukończona” i pauza działają tak samo jak
w zestawie 1. Lekcje otwieraj przez „Prowadzone ścieżki nauki”. To samo demo uruchomione przez
„Przeglądaj dema według poziomu” nie zapisuje postępu lekcji. Każdą lekcję możesz otworzyć od razu,
choć aplikacja poleca kolejność z listy.

## Lekcje wspólne z zestawem 5

Lekcje „Sprawdź, czy confidence mówi prawdę” i „Monitoruj model po wdrożeniu” są w ścieżce tego
zestawu i w ścieżce „Od reprezentacji do zachowania modelu” (zestaw 5). W obu ścieżkach to ta sama
lekcja: ten sam tytuł, to samo demo i te same zadania. Aplikacja zapisuje postęp jednej lekcji, a
nie osobno dla każdej ścieżki:

- Zadanie odhaczone w jednej ścieżce jest odhaczone także w drugiej. Lekcja ukończona w jednej
  ścieżce ma `[x]` na liście lekcji obu ścieżek.
- Mapa kursu liczy tę lekcję w obu ścieżkach. Po ukończeniu tej ścieżki mapa pokazuje przy kroku 5
  „[2/5]”, choć żadna lekcja tylko z zestawu 5 nie jest jeszcze zrobiona.
- Ekran startowy liczy lekcje, zadania i odznaki według ścieżek: razem 24 lekcje, 48 zadań i 24
  odznaki we wszystkich pięciu ścieżkach. Lekcja wspólna liczy się w nim dwa razy.
- Ekran „Lekcja ukończona” pojawia się tylko wtedy, gdy lekcja zostaje ukończona. Jeśli przechodzisz
  tę ścieżkę po zestawie 5, „Następna lekcja” po trzeciej lekcji otwiera kalibrację, która ma już
  `[x]`. Demo działa, ale aplikacja nie pokaże ekranu ukończenia ani ekranu „Ścieżka ukończona”.
  Mapa kursu pokazuje wtedy krok 3 jako ukończony.

## Postęp w aplikacji a zrozumienie tematu

Zasady są te same co w zestawie 1, opisane w części
[„Postęp w aplikacji a zrozumienie tematu”](how-models-learn-from-error.md#postep-w-aplikacji-a-zrozumienie-tematu).
W skrócie:

- **Wykonanie działań.** Każde zadanie lekcji mówi, co zrobić w demie i na co patrzeć.
- **Oznaczenie postępu.** Aplikacja odhacza zadanie (`[x]`) po konkretnej czynności w demie. W tej
  ścieżce kilka zadań wymaga też konkretnego stanu dema: wyboru ustawienia z najwyższym validation
  score, recall co najmniej 80%, niższego ECE albo aktywnego alertu. Przy każdej lekcji niżej
  opisano, co odhacza zadanie i czego aplikacja nie sprawdza.
- **Zrozumienie tematu.** Aplikacja nie sprawdza obserwacji ani wniosków. Na przykład zadanie
  „Porównaj scenariusze leakage” zostaje odhaczone po przełączeniu scenariusza, a aplikacja nie
  sprawdza, czy wiesz, jaki typ cechy powinien wzbudzić podejrzenia. Ukończona lekcja nie potwierdza
  więc opanowania tematu.

Ekran „Lekcja ukończona” zadaje pytanie do przemyślenia („Zatrzymaj się na chwilę”) i podpowiada, na
co zwrócić uwagę. Pod nim są dwa pytania sprawdzające: czy umiesz własnymi słowami wyjaśnić cel
lekcji i czy umiesz nazwać widoczny sygnał z dema, który go potwierdził. Na `main` ta część ma
nagłówek „Mini-check”, a w v0.0.9a „Sprawdź rozumienie”. Pytania służą refleksji i nie są oceniane.
Na `main` wybór „Rozumiem” albo „Do powtórki” w części „Samoocena” jest Twoją deklaracją, której
aplikacja nie sprawdza. W v0.0.9a w tym miejscu jest „Szybki self-check” z dwiema stałymi
wskazówkami, bez przycisków.

## Materiały

Aplikacja ma interfejs po polsku i po angielsku. Notatki dla studentów i instrukcja są po polsku i
po angielsku.

Wszystkie pięć dem tej ścieżki jest wbudowanych w aplikację. Nie mają w repozytorium własnych plików
z teorią ani zadaniami. Ich sterowanie opisuje instrukcja, a teorię każdej lekcji otwierasz
klawiszem `T`. Notatki dla studentów zaznaczają, że część tematów jest celowo uproszczona: Data
Leakage Lab używa stałych scenariuszy wyników, a nie wyników świeżo trenowanego modelu.

## Zadania

### Nie podglądaj test set (Train / Validation / Test Split Lab) {#trustworthy-split}

**Cel:** według aplikacji zrozumieć, czemu train, validation i test split odpowiadają na różne
pytania oraz czemu test set powinien poczekać do samego końca.

**Zakres pracy:** demo pokazuje train score, validation score i test score dla trzech ustawień
complexity modelu: „prosty”, „zbalansowany” i „zbyt elastyczny”. Panel „Wybór modelu” podaje
scenariusz, complexity, wszystkie trzy wyniki, train-val gap i diagnozę. `1`–`3` zmieniają
scenariusz splitu („Czysty sygnał”, „Szum w etykietach”, „Mały dataset”), `-` / `=` zmniejszają i
zwiększają complexity, `0` przywraca ustawienie „zbalansowany”, a `R` resetuje podgląd. Zadania
lekcji:

- **Porównaj złożoność modelu:** przełącz ustawienia złożoności i zobacz, jak rozjeżdżają się
  wyniki na train i validation. Wskazówka w aplikacji: najlepszy wynik train nie oznacza
  automatycznie najlepszego modelu.
- **Wybierz według validation score:** po porównaniu ustawień zatrzymaj się na modelu, który
  wybrałby validation score, zanim zajrzysz do test.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 2”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-2).

**Rezultat:** „Porównaj złożoność modelu” zostaje odhaczone, gdy po naciśnięciu `-`, `=` albo `0`
masz za sobą co najmniej dwa ustawienia complexity. Zmiana scenariusza klawiszami `1`–`3` się nie
liczy. „Wybierz według validation score” zostaje odhaczone, gdy po takim porównaniu ustawisz
complexity z najwyższym validation score w bieżącym scenariuszu. Aplikacja sprawdza więc wybór, ale
nie to, czy test score na niego wpłynął: panel pokazuje test score cały czas.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Który model wybrałby validation score i dlaczego
test set powinien poczekać do momentu tej decyzji?”. Pytania sprawdzające proszą o wyjaśnienie celu
lekcji własnymi słowami i o wskazanie widocznego sygnału z dema.

### Wykryj leakage, zanim zmyli metryki (Data Leakage Lab) {#trustworthy-leakage}

**Cel:** według aplikacji zrozumieć, jak leakage potrafi sztucznie podbić metryki, gdy model
korzysta z informacji niedostępnych w produkcji.

**Zakres pracy:** demo pokazuje stały scenariusz dydaktyczny, a nie wynik trenowania modelu. Panel
„Checklist leakage” podaje scenariusz, podejrzaną cechę, train accuracy, test accuracy, gap, typ
scenariusza i diagnozę. `1`–`3` zmieniają scenariusz („Kolumna po wyniku”, „Proxy targetu”,
„Agregat z przyszłości”), `L` usuwa podejrzaną cechę albo ją przywraca, a `R` resetuje podgląd.
Zadania lekcji:

- **Usuń podejrzaną cechę:** wyłącz cechę z leakage i zobacz, czy wynik robi się mniej efektowny,
  ale bardziej wiarygodny.
- **Porównaj scenariusze leakage:** przełącz scenariusze i zauważ, jaki typ cechy powinien
  wzbudzać podejrzenia.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 2”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-2).

**Rezultat:** „Usuń podejrzaną cechę” zostaje odhaczone, gdy `L` usunie cechę. Przywrócenie cechy
tego zadania nie odhacza. „Porównaj scenariusze leakage” zostaje odhaczone po pierwszym przejściu
do innego scenariusza. Naciśnięcie numeru bieżącego scenariusza się nie liczy. Aplikacja nie
sprawdza, czy umiesz powiedzieć, czy cecha istniałaby w czasie predykcji.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Która cecha sprawiła, że score wyglądał
podejrzanie, i czemu taka cecha nie byłaby bezpieczna w produkcji?”. Pytania sprawdzające proszą o
wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema.

### Czytaj metryki dla niezbalansowanych danych (Class Imbalance Lab) {#trustworthy-imbalance}

**Cel:** według aplikacji zrozumieć, czemu accuracy potrafi ukryć słaby recall klasy
mniejszościowej i czemu wybór threshold jest również decyzją produktową.

**Zakres pracy:** demo pokazuje accuracy, precision i recall przy bieżącym decision threshold oraz
confusion matrix (TP, FP, FN, TN). Panel „Czytaj wynik” podaje scenariusz, klasę pozytywną i jej
udział, threshold, metryki, liczbę false negatives i diagnozę. Threshold ma trzy wartości: 30%, 50%
(domyślnie) i 70%. `1`–`3` zmieniają scenariusz („Fraud screening”, „Medical triage”, „Churn
watchlist”), `-` / `=` zmniejszają i zwiększają threshold, `0` przywraca 50%, a `R` resetuje
podgląd. Zadania lekcji:

- **Ustaw decision threshold:** przesuń threshold i obserwuj kompromis między precision, recall,
  false positives i false negatives.
- **Uzyskaj mocniejszy recall:** znajdź ustawienie z mocniejszym recall i nazwij koszt w precision
  albo liczbie spraw do ręcznego sprawdzenia.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 2”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-2).

**Rezultat:** „Ustaw decision threshold” zostaje odhaczone po pierwszej zmianie threshold.
Naciśnięcie `-` przy 30% albo `=` przy 70% nic nie zmienia i się nie liczy. „Uzyskaj mocniejszy
recall” zostaje odhaczone, gdy po zmianie threshold recall wynosi co najmniej 80%. Aplikacja nie
sprawdza, czy nazwano koszt tej zmiany.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Co zyskałeś przez zwiększenie recall i jaki koszt
pojawił się w precision albo liczbie spraw do sprawdzenia?”. Pytania sprawdzające proszą o
wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema.

### Sprawdź, czy confidence mówi prawdę (Calibration Lab) {#trustworthy-calibration}

**Cel:** według aplikacji zrozumieć, że model może dobrze porządkować przykłady, a mimo to dawać
probabilities, które wymagają kalibracji.

**Zakres pracy:** demo pokazuje reliability diagram (confidence i częstość obserwacji), rozkład
score przed temperature scaling i po nim oraz panel „Kalibracja” z Brier score, ECE, accuracy@0.5,
największą luką i bieżącą temperature. `1`–`3` zmieniają preset („Overconfident”,
„Underconfident”, „Lepiej skalibrowane”), `-` / `=` zmieniają temperature scaling (od 0.50 do
3.00, domyślnie 1.00), `E` pokazuje albo ukrywa error bars, `O` pokazuje albo ukrywa raw score sprzed
temperature scaling, a `R` resetuje podgląd. Zadania lekcji:

- **Popraw ECE:** zmień temperature scaling tak, żeby ECE było lepsze niż przy raw score.
- **Sprawdź calibration gaps:** użyj widoku gap/error bars, żeby zobaczyć, gdzie confidence
  rozmija się z obserwowaną częstością.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 3”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-3).
W aplikacji to demo należy do poziomu 3.

**Rezultat:** „Popraw ECE” zostaje odhaczone, gdy po zmianie temperature ECE w bieżącym presecie
jest niższe niż przy temperature 1.00. Nie każda zmiana to daje: w kontroli w presecie
„Overconfident” temperature 0.75 ECE pogorszyła, a 1.50 poprawiła. „Sprawdź calibration gaps”
zostaje odhaczone po pierwszym naciśnięciu `E`. Error bars są domyślnie widoczne, więc pierwsze
naciśnięcie je ukrywa. Aplikacja nie sprawdza, czy znaleziono biny, w których confidence najbardziej
rozmija się z częstością.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Gdzie confidence rozmijało się z obserwowaną
częstością i jak temperature scaling zmienił tę różnicę?”. Pytania sprawdzające proszą o
wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema.

### Monitoruj model po wdrożeniu (Model Monitoring Drift Lab) {#trustworthy-monitoring}

**Cel:** według aplikacji zrozumieć, czemu nawet zaufany model wymaga monitoringu: data drift i
metric drift mogą pojawić się w różnym momencie.

**Zakres pracy:** demo pokazuje w czasie aktywny sygnał i, dla porównania, drugi sygnał, alert
threshold oraz baseline window i current window. Panel „Sterowanie i sygnały” podaje między innymi
sygnał, threshold, pierwszy alert, lead signal, lukę między oknami, severity i stan analizy.
`1`–`4` zmieniają preset („Stable baseline”, „Data drift first”, „Metric drift first”,
„Jednorazowy pik”), `D` / `M` wybierają sygnał data drift albo metric drift, `-` / `=` zmieniają
alert threshold (od 10% do 30%, domyślnie 20%), `0` go przywraca, `A` potwierdza aktywny alert do
analizy, a `R` resetuje podgląd. Zadania lekcji:

- **Porównaj sygnały drift:** przełącz data drift i metric drift, a potem wskaż, który sygnał
  pojawia się pierwszy.
- **Potwierdź sensowny alert:** wywołaj realny alert i potwierdź analizę dopiero wtedy, gdy current
  window naprawdę wymaga uwagi.

Sterowanie i to, na co patrzeć w panelu, opisuje
[instrukcja, sekcja „Natywne laby Level 3”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-3).

**Rezultat:** „Porównaj sygnały drift” zostaje odhaczone, gdy w tym uruchomieniu dema były aktywne
oba sygnały. Demo zaczyna od data drift, więc wystarczy pierwsze `M`. „Potwierdź sensowny alert”
zostaje odhaczone po `A`, ale tylko przy aktywnym alercie, czyli gdy luka między current window a
baseline window jest co najmniej równa alert threshold. Panel pokazuje wtedy „analiza: do
sprawdzenia”, a po `A` „analiza: potwierdzona”. Bez aktywnego alertu `A` nic nie zmienia. Aplikacja
nie sprawdza, czy wskazano sygnał, który pojawił się pierwszy.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Który sygnał pojawił się pierwszy, data drift czy
metric drift, i co sprawdziłbyś przed retrainingiem?”. Pytania sprawdzające proszą o wyjaśnienie
celu lekcji własnymi słowami i o wskazanie sygnału z dema.

## Oczekiwane rezultaty

- Na liście lekcji wszystkie pięć lekcji ma `[x]`, a mapa kursu pokazuje krok 3 jako ukończony.
  Jeśli ostatnia lekcja zostaje ukończona w tej ścieżce, ekran „Ścieżka ukończona” pokazuje 5/5
  lekcji, 10/10 zadań i 5/5 odznak.
- Na pytania z ekranów „Lekcja ukończona” odpowiadasz własnymi słowami. Aplikacja tych odpowiedzi
  nie sprawdza.

## Wskazówki

- Notatki dla studentów radzą otwierać teorię, kiedy potrzebujesz kontekstu: `T` w demie albo na
  ekranie intro. Teoria lekcji ma mini-zadania, których aplikacja nie odhacza. W Train / Validation
  / Test Split Lab proponuje na przykład znalezienie przypadku, w którym train score rośnie, a
  validation score spada.
- Jeśli „Następna lekcja” otworzy lekcję, która ma już `[x]`, wróć do ekranu startowego. Kolejną
  lekcję wybierzesz z listy lekcji („Prowadzone ścieżki nauki”, potem krok 3) albo klawiszem `C`,
  który otwiera pierwszą nieukończoną lekcję w kolejności mapy kursu.
- Ekran „Ścieżka ukończona” proponuje jako kolejną ścieżkę „Od cech do decyzji modelu”, opisaną w
  [zestawie 4](from-features-to-model-decisions.md).
