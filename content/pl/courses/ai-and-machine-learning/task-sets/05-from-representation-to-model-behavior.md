---
title: "Od reprezentacji do zachowania modelu"
summary: "Piąta prowadzona ścieżka nauki w aplikacji Interactive ML Labs (wersja alfa): pięć lekcji, od PCA i embeddingów t-SNE / UMAP, przez kalibrację i monitoring modelu, po prognozy szeregów czasowych. Dwie lekcje są wspólne ze ścieżką z zestawu 3. W każdej lekcji wykonujesz dwa zadania w demie."
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
Ten zestaw prowadzi przez piątą ścieżkę nauki aplikacji Interactive ML Labs, „Od reprezentacji do
zachowania modelu”. Mapa kursu w aplikacji pokazuje ją jako krok 5, ostatni, po ścieżce z
[zestawu 4](from-features-to-model-decisions.md). Ścieżka ma pięć lekcji, a każda lekcja to jedno
zadanie tego zestawu. W lekcji uruchamiasz demo i wykonujesz dwa zadania, które aplikacja pokazuje
na liście „Zadania lekcji”. Nie piszesz kodu. Ta strona nie zastępuje lekcji: podaje, gdzie je
znaleźć, co w nich zrobić i co aplikacja sprawdza. Nazwy ekranów, zadań i przycisków są tu takie,
jak w polskiej wersji aplikacji. Nazwy dem i część pojęć aplikacja zostawia po angielsku.

Lekcje 3 i 4, o kalibracji i o monitoringu, należą też do ścieżki z
[zestawu 3](from-good-scores-to-trustworthy-models.md). Jak aplikacja zapisuje ich postęp, opisuje
część [„Lekcje wspólne z zestawem 3”](#lekcje-wspolne-z-zestawem-3).

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
2. W „Mapie kursu” wybierz „Krok 5: Od reprezentacji do zachowania modelu”. Zobaczysz listę pięciu
   lekcji.
3. Wybierz lekcję. Na ekranie intro `Enter` uruchamia demo, a `T` otwiera teorię.

Po ukończeniu ścieżek z zestawów 1–4 ekran startowy proponuje pierwszą lekcję tej ścieżki, a
klawisz `C` od razu ją otwiera. Nawigacja, ekran „Lekcja ukończona” i pauza działają tak samo jak
w zestawie 1. Lekcje otwieraj przez „Prowadzone ścieżki nauki”. To samo demo uruchomione przez
„Przeglądaj dema według poziomu” nie zapisuje postępu lekcji. Każdą lekcję możesz otworzyć od razu,
choć aplikacja poleca kolejność z listy.

## Lekcje wspólne z zestawem 3

Lekcje „Sprawdź, czy confidence mówi prawdę” i „Monitoruj model po wdrożeniu” są w ścieżce tego
zestawu i w ścieżce „Od dobrych wyników do zaufanych modeli” (zestaw 3). W obu ścieżkach to ta sama
lekcja: ten sam tytuł, to samo demo i te same zadania. Aplikacja zapisuje postęp jednej lekcji, a
nie osobno dla każdej ścieżki:

- Zadanie odhaczone w jednej ścieżce jest odhaczone także w drugiej. Lekcja ukończona w jednej
  ścieżce ma `[x]` na liście lekcji obu ścieżek.
- Mapa kursu liczy tę lekcję w obu ścieżkach. Jeśli ścieżka z zestawu 3 jest ukończona, mapa
  pokazuje przy kroku 5 „[2/5]”, zanim otworzysz pierwszą lekcję tej ścieżki.
- Ekran startowy liczy lekcje, zadania i odznaki według ścieżek: razem 24 lekcje, 48 zadań i 24
  odznaki we wszystkich pięciu ścieżkach. Lekcja wspólna liczy się w nim dwa razy.
- Ekran „Lekcja ukończona” pojawia się tylko wtedy, gdy lekcja zostaje ukończona. Jeśli lekcje
  wspólne masz już za sobą, „Następna lekcja” po lekcji 2 otwiera kalibrację, która ma już `[x]`.
  Demo działa, ale ekran ukończenia się nie pojawi. Wróć wtedy do ekranu startowego. Klawisz `C`
  otworzy pierwszą nieukończoną lekcję w kolejności mapy kursu, a po ukończeniu ścieżek z zestawów
  1–4 będzie to lekcja „Sprawdź forecast względem czasu”. Możesz też wybrać ją z listy lekcji.
- Jeśli przechodzisz tę ścieżkę przed zestawem 3, lekcje wspólne wykonujesz tutaj, a „Następna
  lekcja” prowadzi w kolejności tej ścieżki.

Na liście lekcji tej ścieżki „Wymagania” przy kalibracji wskazują lekcję „Czytaj metryki dla
niezbalansowanych danych”, która jest tylko w ścieżce z zestawu 3. Jak przy innych lekcjach,
aplikacja tego nie wymusza.

## Postęp w aplikacji a zrozumienie tematu

Zasady są te same co w zestawie 1, opisane w części
[„Postęp w aplikacji a zrozumienie tematu”](how-models-learn-from-error.md#postep-w-aplikacji-a-zrozumienie-tematu).
W skrócie:

- **Wykonanie działań.** Każde zadanie lekcji mówi, co zrobić w demie i na co patrzeć.
- **Oznaczenie postępu.** Aplikacja odhacza zadanie (`[x]`) po konkretnej czynności w demie. W tej
  ścieżce dwa zadania wymagają też konkretnego stanu dema: niższego ECE w kalibracji i aktywnego
  alertu w monitoringu. Przy każdej lekcji niżej opisano, co odhacza zadanie i czego aplikacja nie
  sprawdza.
- **Zrozumienie tematu.** Aplikacja nie sprawdza obserwacji ani wniosków. Na przykład zadanie
  „Sprawdź ryzyko forecastu” zostaje odhaczone po pierwszym przełączeniu widoku albo scenariusza, a
  aplikacja nie sprawdza, czy zauważono, gdzie forecast staje się mniej wiarygodny. Ukończona lekcja
  nie potwierdza więc opanowania tematu.

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

Wszystkie pięć dem tej ścieżki jest wbudowanych w aplikację i należy do poziomu 3. Nie mają w
repozytorium własnych plików z teorią ani zadaniami. Ich sterowanie opisuje instrukcja, a teorię
każdej lekcji otwierasz klawiszem `T`. Notatki dla studentów zaznaczają, że część tematów jest
celowo uproszczona: t-SNE / UMAP Exploration Lab używa koncepcyjnych toy embeddings zamiast pełnej
implementacji tych algorytmów.

## Zadania

### Zachowaj sygnał w mniejszej liczbie wymiarów (PCA Lab) {#representation-explained-variance}

**Cel:** według aplikacji zrozumieć, że PCA to kompromis kompresji: projekcja może zachować większość
wariancji, ale nadal tracić część szczegółów rekonstrukcji.

**Zakres pracy:** demo pokazuje punkty, kierunek projekcji i ich projekcję na jedną linię. Panel
podaje tryb (ręczny kierunek albo „fit PCA”), dane, noise, stan residual lines, kąt projekcji,
zachowaną wariancję i błąd rekonstrukcji. `1`–`3` zmieniają preset danych („Linear cloud”, „Noisy
cloud”, „Two bands”), `-` / `=` zmieniają noise, `N` losuje nową próbkę, `Left` / `Right` obracają
kierunek projekcji, `F` przełącza ręczny kierunek i dopasowany kierunek PCA, `C` pokazuje albo
ukrywa residual lines, a `R` resetuje kierunek projekcji. Zadania lekcji:

- **Porównaj zachowaną i utraconą wariancję:** obróć projekcję albo dopasuj PCA, a potem porównaj,
  ile wariancji zostaje, a ile znika.
- **Sprawdź residuals rekonstrukcji:** przełącz linie residuals i potraktuj je jako widoczny koszt
  redukcji danych do jednego wymiaru. Wskazówka w aplikacji: wysoka zachowana wariancja nie znaczy,
  że każdy punkt jest odtworzony idealnie.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 3”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-3).

**Rezultat:** „Porównaj zachowaną i utraconą wariancję” zostaje odhaczone po przełączeniu na
dopasowany kierunek PCA (`F`) albo gdy po obrocie, zmianie noise, presetu albo nowej próbce panel
pokaże inną zachowaną wariancję niż wcześniej w tym uruchomieniu dema. Obrót, po którym ta wartość
się nie zmienia, nie wystarcza: w kontroli pierwszy obrót zmienił kąt, ale wariancja została na 98%.
„Sprawdź residuals rekonstrukcji” zostaje odhaczone po pierwszym `C`. Residual lines są domyślnie
widoczne, więc pierwsze naciśnięcie je ukrywa. Aplikacja nie sprawdza, czy porównano wariancję z
błędem rekonstrukcji.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Co zachował kierunek dopasowany przez PCA i gdzie
residuals pokazały utratę informacji?”. Podpowiedź: „PCA najłatwiej zrozumieć wtedy, gdy student
czyta zachowaną wariancję razem z błędem rekonstrukcji, a nie jak jedną magiczną metrykę”. Pytania
sprawdzające proszą o wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema.

### Kwestionuj ładne embeddingi (t-SNE / UMAP Exploration Lab) {#representation-embedding-skeptic}

**Cel:** według aplikacji zrozumieć, że t-SNE i UMAP są użytecznymi widokami struktury sąsiedztwa,
ale ich układ 2D może kusić mylącą interpretacją.

**Zakres pracy:** demo pokazuje koncepcyjny toy embedding z kolorami etykiet i liniami do lokalnych
sąsiadów oraz porównanie widoków raw, t-SNE i UMAP. Panel podaje algorytm, perplexity
albo neighbors, wariant seed, local trust, global spread i stan raw layout oraz linii. `1`–`3`
zmieniają preset danych („Separated clusters”, „Bridge”, „Nested groups”), `M` przełącza t-SNE i
UMAP, `-` / `=` zmieniają perplexity albo neighbors, `S` zmienia wariant seed, `L` pokazuje albo
ukrywa linie sąsiadów, `O` pokazuje albo ukrywa raw high-dimensional layout, a `R` resetuje
podgląd. Zadania lekcji:

- **Porównaj raw view i embedding:** pokaż albo ukryj raw layout i porównaj go z aktywnym
  embeddingiem, zanim wyciągniesz wnioski z obrazu 2D.
- **Sprawdź stabilność embeddingu:** zmień algorytm, parametr sąsiedztwa albo seed i zauważ, która
  historia na wykresie się zmienia. Wskazówka w aplikacji: klaster, który pojawia się tylko po
  jednej zmianie ustawień, zasługuje na sceptycyzm.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 3”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-3).

**Rezultat:** „Porównaj raw view i embedding” zostaje odhaczone po pierwszym `O`. Raw layout jest
domyślnie widoczny, więc pierwsze naciśnięcie go ukrywa. „Sprawdź stabilność embeddingu” zostaje
odhaczone po pierwszej zmianie algorytmu (`M`), perplexity albo neighbors (`-` / `=`, jeśli wartość
się zmienia) albo seed (`S`). Zmiana presetu danych i linii sąsiadów się nie liczy. Aplikacja nie
sprawdza, czy zauważono, która część obrazu się zmieniła.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Która część embeddingu wyglądała stabilnie, a która
zmieniła się po zmianie założeń?”. Podpowiedź: „Embeddingi są świetne do rozmowy o danych, ale
sednem lekcji jest porównywanie widoków i parametrów, zanim uznamy obraz za strukturę”. Pytania
sprawdzające proszą o wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema.

### Sprawdź, czy confidence mówi prawdę (Calibration Lab) {#trustworthy-calibration}

Ta lekcja jest też w [zestawie 3](from-good-scores-to-trustworthy-models.md#trustworthy-calibration).
Postęp jest wspólny: jeśli ukończono ją w tamtej ścieżce, tutaj ma już `[x]`.

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

Ta lekcja jest też w [zestawie 3](from-good-scores-to-trustworthy-models.md#trustworthy-monitoring).
Postęp jest wspólny: jeśli ukończono ją w tamtej ścieżce, tutaj ma już `[x]`.

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

### Sprawdź forecast względem czasu (Time Series Forecasting Lab) {#representation-forecast-checker}

**Cel:** według aplikacji zrozumieć, że walidacja time series zależy od kolejności: forecast trzeba
oceniać na przyszłym holdout, residuals i ryzyku horyzontu.

**Zakres pracy:** demo pokazuje historię, holdout window, wartości rzeczywiste, forecast, residuals
i uncertainty band. Panel „Odczyt forecastu” podaje dataset, model, horizon, MAE, RMSE, bias,
uncertainty i diagnozę. `1`–`3` zmieniają scenariusz („Sezonowy popyt”, „Zmiana trendu”, „Szum
operacyjny”), `M` zmienia model forecastingu („naive last value”, „moving average”, „trend +
sezonowość”), `-` / `=` zmieniają forecast horizon (4, 6 albo 8), `U` pokazuje albo ukrywa
uncertainty band, `E` pokazuje albo ukrywa residuals, a `R` resetuje lab. Zadania lekcji:

- **Porównaj wybory forecastu:** zmień model albo forecast horizon i porównaj, jak reagują MAE,
  RMSE, bias oraz linia forecastu.
- **Sprawdź ryzyko forecastu:** użyj residuals, uncertainty albo innego preset time series, żeby
  zobaczyć, gdzie forecast na holdout staje się mniej wiarygodny. Wskazówka w aplikacji: gładka
  linia nadal może się mylić, gdy przyszłość zmienia kształt.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 3”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-3).

**Rezultat:** „Porównaj wybory forecastu” zostaje odhaczone po pierwszej zmianie modelu (`M`) albo
horizon (`-` / `=`, jeśli wartość się zmienia). „Sprawdź ryzyko forecastu” zostaje odhaczone po
pierwszym naciśnięciu `U`, `E` albo `1`–`3`, także numeru bieżącego scenariusza. Aplikacja nie
sprawdza, czy porównano MAE, RMSE i bias ani czy znaleziono miejsce, w którym forecast się myli.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Który wybór forecastu najmocniej zmienił holdout
error i jakie ostrzeżenie pokazały residuals albo uncertainty?”. Podpowiedź: „Time series pokazuje
dyscyplinę walidacji bardzo wyraźnie: modelowi można ufać dopiero wtedy, gdy potwierdza to przyszły
holdout”. Pytania sprawdzające proszą o wyjaśnienie celu lekcji własnymi słowami i o wskazanie
sygnału z dema.

## Oczekiwane rezultaty

- Na liście lekcji wszystkie pięć lekcji ma `[x]`, a mapa kursu pokazuje krok 5 jako ukończony. Po
  ostatniej lekcji ekran „Ścieżka ukończona” pokazuje 5/5 lekcji, 10/10 zadań i 5/5 odznak, razem
  z lekcjami wspólnymi.
- Na pytania z ekranów „Lekcja ukończona” odpowiadasz własnymi słowami. Aplikacja tych odpowiedzi
  nie sprawdza.

## Wskazówki

- Notatki dla studentów radzą otwierać teorię, kiedy potrzebujesz kontekstu: `T` w demie albo na
  ekranie intro. Teoria lekcji ma mini-zadania, których aplikacja nie odhacza. W PCA Lab proponuje
  na przykład porównanie presetów „Linear cloud”, „Noisy cloud” i „Two bands”.
- To ostatnia ścieżka w mapie kursu. Ekran „Ścieżka ukończona” proponuje wrócić do dowolnej ścieżki
  i wyjaśnić ją bez sterowania.
