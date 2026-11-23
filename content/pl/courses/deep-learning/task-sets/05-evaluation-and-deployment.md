---
title: "Ewaluacja i wdrażanie"
summary: "Laboratoria 14–15 z repozytorium Deep Learning: audyt błędów i interpretacja decyzji klasyfikatora obrazów EuroSAT (metryki, confidence, Grad-CAM, occlusion) oraz lokalna usługa inferencyjna z artefaktem modelu, benchmarkiem i monitoringiem driftu. Ostatnie laboratoria kursu."
status: published
materials:
  - repository: deep-learning
    path: README.pl.md
    lang: pl
    label: "Opis kursu: konfiguracja, uruchomienie JupyterLab i pamięć podręczna danych"
  - repository: deep-learning
    path: data/registry.yml
    lang: en
    label: "Rejestr danych: źródła, licencje i sposób pobierania EuroSAT i wag ResNet18"
tasks:
  lab-14:
    materials:
      - repository: deep-learning
        path: labs/14_evaluation_interpretability/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 14 — Audyt błędów i interpretacja decyzji klasyfikatora obrazów"
      - repository: deep-learning
        path: labs/14_evaluation_interpretability/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/14_evaluation_interpretability/lab.ipynb"
      - repository: deep-learning
        path: lectures/14_evaluation_interpretability/lecture.md
        lang: pl
        label: "Wykład 14: Jak oceniać i interpretować modele, którym chcemy zaufać?"
  lab-15:
    materials:
      - repository: deep-learning
        path: labs/15_production/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 15 — Lokalna usługa inferencyjna z monitoringiem (EuroSAT + ResNet18)"
      - repository: deep-learning
        path: labs/15_production/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/15_production/lab.ipynb"
      - repository: deep-learning
        path: labs/15_production/
        lang: en
        label: "Kod laboratorium 15: aplikacja app/, benchmark.py, monitoring.py i skrypty"
      - repository: deep-learning
        path: lectures/15_production/lecture.md
        lang: pl
        label: "Wykład 15: Od modelu w notebooku do systemu, który można obserwować i utrzymywać"
---
Ten zestaw obejmuje piątą, ostatnią grupę laboratoriów z repozytorium Deep Learning, nazwaną w
opisie kursu „Ewaluacja i wdrażanie”. W laboratorium 14 przygotowujesz audyt klasyfikatora zdjęć
satelitarnych: metryki na niezależnym zbiorze, najczęstsze błędy, pewność predykcji i interpretację
decyzji przez Grad-CAM i occlusion. W laboratorium 15, ostatnim w kursie, budujesz lokalną usługę
inferencyjną dla tego typu modelu, mierzysz jej koszt, monitorujesz drift i piszesz raport o decyzji
wdrożeniowej. Dwa zadania odpowiadają laboratoriom 14–15, w kolejności z repozytorium.

## Status materiałów

Repozytorium jest w rozbudowie i jego treści mogą się jeszcze zmieniać. Ta strona opisuje
instrukcje, notebooki i kod z gałęzi `main` (commit `0ffe385`), którą pobiera polecenie `git clone`.
Wydanie `v1.0.0` z 19 października 2026 roku zawiera starsze wersje: w laboratorium 14 inną wersję
notebooka, a w laboratorium 15 inną wersję instrukcji, notebooka i kodu aplikacji (m.in.
zabezpieczenia uploadu i kontrakt artefaktu). Instrukcji, notebooka i plików aplikacji korzystaj z
tej samej wersji.

## Przygotowanie do zestawu

Środowisko jest takie samo jak w [zestawie 1](fundamentals.md): uv, Python 3.12 i polecenia z sekcji
„Konfiguracja” w opisie kursu:

```bash
git clone https://github.com/michalmaj/deep-learning.git
cd deep-learning
uv sync
uv run jupyter lab
```

Pracujesz tak samo jak w zestawie 1: instrukcja `README.pl.md`, notebook `lab.ipynb` z komórkami
`TODO` i komórki Markdown na odpowiedzi, które mają tu tekst „(Twoja odpowiedź tutaj.)”. Oba
laboratoria korzystają z ResNet18 z zamrożonym backbone'em i trenowaną głowicą, jak w [laboratorium
07](computer-vision-and-representations.md#lab-07), oraz z zasad ewaluacji z wcześniejszych
laboratoriów. W laboratorium 15 część pracy wykonujesz poza notebookiem, w plikach Pythona.

- **Sprzęt:** według opisu kursu wystarcza procesor (CPU). Notebooki obu laboratoriów zawsze liczą
  na procesorze (`device = torch.device("cpu")`). Oba korzystają z podzbioru EuroSAT, a nie z całego
  zbioru.
- **Pomiary czasu:** laboratorium 14 wypisuje czas treningu głowicy, a laboratorium 15 mierzy
  latencję i przepustowość API. Opis kursu zaznacza, że czas zależy od komputera.

## Dane i modele do pobrania

Oba laboratoria korzystają z tych samych zasobów co laboratoria 07 i 08. Jeśli masz je już w pamięci
podręcznej, nie pobierasz ich ponownie. Opis zasobów jest w [zestawie
2](computer-vision-and-representations.md#dane-i-modele-do-pobrania).

- **EuroSAT** przez `torchvision.datasets.EuroSAT` (archiwum i rozpakowane pliki około 230 MB w
  `data_cache/`).
- **Wagi ResNet18 `IMAGENET1K_V1`** (około 45 MB w pamięci podręcznej PyTorcha, domyślnie
  `~/.cache/torch`).

Artefakt modelu z laboratorium 15 (`weights.pt` i `metadata.json`) powstaje lokalnie, w katalogu
`artifacts/`, który nie trafia do Gita.

## Samodzielna praca i sprawdzanie wyników

Sprawdzanie działa tak samo jak w [zestawie 1](fundamentals.md). Testy repozytorium sprawdzają
szkielet notebooka, czyli to, że dostarczony kod działa do pierwszego `TODO`. Oba laboratoria mają
też osobne testy wzorów i gotowych części (np. Grad-CAM na zamrożonym backbonie, kontrakt artefaktu,
limity uploadu). Testy szkieletów pobierają dane, dlatego są oznaczone jako `network`. Gotowe
asercje w notebookach sprawdzają wybrane elementy, a opis każdego zadania podaje, które.
Interpretacji, raportów i wniosków nic nie sprawdza automatycznie. Repozytorium nie zawiera
rozwiązań laboratoriów.

Każda instrukcja kończy się sekcją „Kryteria oceny”. Opisuje ona, po czym poznać merytorycznie
kompletny wynik laboratorium, i możesz jej używać do samodzielnego sprawdzenia pracy. Ta strona nie
przenosi tej sekcji i nie traktuje jej jako zasad zaliczenia przedmiotu.

## Materiały

Instrukcje i notebooki są po polsku i po angielsku. Kod aplikacji laboratorium 15 i komentarze
`TODO` w nim są po angielsku. Rejestr danych jest po angielsku. Pełną listę wykładów i laboratoriów
znajdziesz na stronie [„Materiały przedmiotu”](../guides/course-materials.md).

## Zadania

### Audyt błędów i interpretacja decyzji klasyfikatora obrazów {#lab-14}

Klasyfikator zdjęć EuroSAT to ResNet18 `IMAGENET1K_V1` z zamrożonym backbone'em i nową głowicą
`nn.Linear` na 10 klas. Gotowy kod wczytuje dane i model oraz przygotowuje funkcję
`extract_features`, która liczy cechy backbone'u raz, przed treningiem głowicy. Instrukcja określa
wynik laboratorium jako raport audytu klasyfikatora, a nie pojedynczy wykres Grad-CAM.

**Cel:** ocenić klasyfikator na niezależnym zbiorze, przeanalizować jego najczęstsze i najbardziej
pewne błędy, samodzielnie zaimplementować Grad-CAM i porównać go z occlusion sensitivity oraz
sprawdzić jedno alternatywne wyjaśnienie zachowania modelu.

**Zakres pracy:**

- **Dane i trening (sekcje 1–2):** dzielisz podzbiór EuroSAT na rozłączne `train_idx`, `val_idx` i
  `test_idx` (instrukcja podaje przykład 1800/400/400), potwierdzasz to w kodzie, wypisujesz rozkład
  klas w każdym podzbiorze i komentujesz skutek użycia tego samego podziału do wyboru
  hiperparametrów i oceny. Głowicę trenujesz gotową funkcją `train_head` wyłącznie na `train_idx`.
- **Ewaluacja (sekcja 3):** na `test_idx` liczysz accuracy, macro-F1 oraz precision, recall i F1 dla
  każdej klasy, rysujesz macierz pomyłek 10 × 10 i komentujesz klasę o najniższym recall.
- **Błędy i confidence (sekcje 4–5):** z macierzy pomyłek odczytujesz dwie najczęściej mylone pary
  klas i komentujesz koszt jednej z pomyłek. Porównujesz rozkład confidence poprawnych i błędnych
  predykcji i zapisujesz najbardziej pewną błędną predykcję.
- **Wybór przykładów (sekcja 6):** jawna, odtwarzalna procedura wyboru trzech przykładów: poprawnej
  predykcji o wysokiej confidence, pomyłki o niskiej i pomyłki o wysokiej confidence.
- **Grad-CAM i occlusion (sekcje 7–8):** klasa `GradCAM` z forward hookiem,
  `register_full_backward_hook`, wagami z uśrednionego gradientu, ważoną sumą z ReLU, interpolacją
  dwuliniową i obsługą mapy o zerowej rozpiętości, dla `backbone.layer4`. Liczysz mapy dla trzech
  przykładów (dla klasy przewidzianej), a dla pierwszego także occlusion sensitivity (łata 32 × 32,
  krok 32, tło `BASELINE_GRAY`, a nie surowe zero), i komentujesz zgodność obu metod.
- **Podgrupy albo odporność (sekcja 9):** wybierasz jedną z dwóch opcji z instrukcji: accuracy dla
  obrazów jasnych i ciemnych ze sprawdzeniem rozkładu klas w grupach albo odporność na odbicie w
  poziomie ze wskazaniem przykładów, w których predykcja się zmieniła.
- **Zadanie diagnostyczne (sekcja 10):** gotowy `GradCAMColleague` ma dwa powiązane problemy:
  `torch.no_grad()` i brak `requires_grad` na wejściu przy zamrożonym backbonie. Podajesz konkretny
  błąd, wyjaśniasz, dlaczego samo usunięcie `no_grad()` nie wystarcza, naprawiasz oba problemy i
  sprawdzasz, że mapa jest skończona i ma niezerową rozpiętość.
- **Raport (sekcja 11):** odpowiedzi na siedem pytań z instrukcji, z ogólnymi wnioskami opartymi na
  całym zbiorze testowym, a nie na trzech ilustracjach.

**Rezultat:** notebook wykonany do końca, z rozłącznym podziałem, metrykami i macierzą pomyłek,
analizą błędów i confidence, jawnie wybranymi przykładami, działającym Grad-CAM i occlusion, analizą
z sekcji 9, poprawionym kodem z sekcji 10 i raportem.

**Sprawdź się:**

- Notebook nie ma gotowych asercji dla Twojego kodu. Gotowa komórka z sekcji 10 przechwytuje i
  wypisuje `RuntimeError` z kodu kolegi.
- Grad-CAM wymaga `x.requires_grad_(True)` na wejściu, bo backbone jest zamrożony. Bez tego gradient
  nie dociera do `layer4`, co instrukcja opisuje w sekcjach 7 i 10.
- Nic nie sprawdza, czy occlusion używa `BASELINE_GRAY`. Surowe zero też daje wynik bez błędu.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

### Lokalna usługa inferencyjna z monitoringiem (EuroSAT + ResNet18) {#lab-15}

Laboratorium kończy się działającym lokalnym API, odtwarzalnym artefaktem modelu, wynikami
benchmarku i raportem o decyzji wdrożeniowej. „Wdrażanie” oznacza tu lokalną aplikację FastAPI w
katalogu `labs/15_production/`. Instrukcja nie wymaga osobnego procesu serwera (`uvicorn`),
kontenera ani chmury: notebook wywołuje aplikację przez `fastapi.testclient.TestClient`, w tym samym
procesie, przez warstwę HTTP i walidacji.

**Cel:** przygotować i zweryfikować artefakt modelu, zaimplementować preprocessing, inferencję i
endpoint `/predict`, zmierzyć koszt usługi, wykrywać drift wskaźnikiem PSI i zdiagnozować
training-serving skew.

**Zakres pracy:**

- **Pliki:** gotowe są `prepare_artifact.py`, `load_artifact` w `app/model.py`, endpointy `/health`,
  `/ready` i `/model-info` w `app/server.py`, `send_requests` w `benchmark.py` oraz
  `histogram_counts` i `brightness_feature` w `monitoring.py`. Uzupełniasz `preprocess_image_bytes`
  i `predict` w `app/model.py`, `/predict` w `app/server.py`, `compute_stats` w `benchmark.py`,
  `psi` w `monitoring.py` oraz komórki `TODO` w notebooku.
- **Artefakt (sekcja 1):** uruchamiasz `prepare_artifact.py`, który trenuje głowicę na zamrożonych
  cechach i zapisuje `weights.pt` oraz `metadata.json`, a potem w kodzie potwierdzasz identyczne
  logity (`torch.equal`). Instrukcja porównuje model wczytany z artefaktu z modelem bezpośrednio po
  treningu, a komentarz `TODO` w notebooku opisuje porównanie `predict()` z ręcznym przejściem przez
  preprocessing i model wczytany z artefaktu.
- **Preprocessing i `/predict` (sekcje 2–3):** `preprocess_image_bytes` dekoduje obraz przez gotowe
  `decode_image_bytes` i stosuje `ResNet18_Weights.IMAGENET1K_V1.transforms()`, bez ręcznego
  odtwarzania kroków. `predict` zwraca `predicted_class`, `confidence` i `model_version`. `/predict`
  zwraca HTTP 503, gdy model nie jest gotowy, czyta plik przez `read_upload_limited()` i zwraca
  wynik `run_prediction(...)`.
- **Zgodność i błędne wejścia (sekcja 4):** odpowiedź API dla prawdziwego obrazu EuroSAT ma się
  dokładnie zgadzać z bezpośrednim wywołaniem `predict`. Komórka `TODO` sprawdza też uszkodzony plik
  i zbyt duży plik oraz to, że odpowiedź nie zawiera tracebacka ani ścieżek.
- **Benchmark (sekcja 5):** `compute_stats` liczy średnią, p50 i p95 w milisekundach oraz
  przepustowość. Mierzysz osobno pierwsze żądanie (cold) i co najmniej 20 kolejnych (warm), po
  jednym obrazie na żądanie.
- **PSI i scenariusze (sekcje 6–7):** `psi` z wygładzaniem zerowych częstości (`eps`), sprawdzone na
  znanym przykładzie z wykładu. Scenariusz A: niezależna próba z tej samej dystrybucji bez
  fałszywego alarmu. Scenariusz B: jedna transformacja (np. jasność albo kontrast) o jednej sile,
  wybrana przed sprawdzeniem accuracy. Scenariusz C: accuracy na danych ze scenariusza B porównana z
  wynikiem PSI, bez zakładania odpowiedzi z góry.
- **Zadanie diagnostyczne (sekcja 8):** gotowy `model_colleague.py` odtwarza preprocessing ręcznie.
  Porównujesz logity, wyjaśniasz, który krok się różni (`resize(256)` → `center_crop(224)` →
  normalizacja), liczysz na kilkunastu prawdziwych obrazach, ile predykcji się zmienia, i
  potwierdzasz, że Twoja implementacja zgadza się z wywołaniem zweryfikowanym w sekcji 4.
- **Raport (sekcja 9):** siedem punktów z instrukcji: wersja modelu i protokół ewaluacji, accuracy i
  ograniczenia, format API, latencja i przepustowość, scenariusze A/B/C, pewność interpretacji
  driftu, ryzyka i następne działania. Instrukcja zaznacza, że nie trzeba wymuszać wniosku o
  gotowości do produkcji.

**Rezultat:** artefakt i uzupełnione pliki aplikacji, notebook wykonany do końca z weryfikacją
artefaktu, zgodnością API, obsługą błędnych wejść, benchmarkiem cold i warm, sprawdzonym PSI,
scenariuszami A/B/C, diagnozą skew i raportem.

**Sprawdź się:**

- **Gdzie jest artefakt:** `prepare_artifact.py` zapisuje `artifacts/` w katalogu, z którego go
  uruchamiasz, albo w katalogu ze zmiennej `MODULE15_ARTIFACT_DIR`. Aplikacja (`app/server.py`)
  szuka artefaktu tak samo: w `artifacts/` względem bieżącego katalogu procesu, czyli w notebooku
  `labs/15_production/`, albo w katalogu ze zmiennej `MODULE15_ARTIFACT_DIR`. Komentarz `TODO` w
  sekcji 1 wczytuje `load_artifact("artifacts")`, też względem katalogu notebooka. Polecenie z
  instrukcji uruchomione z katalogu głównego repozytorium zapisuje więc artefakt w `artifacts/`
  katalogu głównego, a notebook i aplikacja go tam nie szukają i zgłaszają `FileNotFoundError`.
- **Testy z instrukcji:** `uv run pytest tests/test_lab_15_scaffold.py -v` sprawdza gotowe części
  aplikacji (kontrakt artefaktu, endpointy, limity uploadu, histogram) i to, że części do
  uzupełnienia jeszcze zgłaszają `NotImplementedError`. Po uzupełnieniu kodu testy z
  `not_yet_implemented` w nazwie i test
  `test_send_requests_given_scaffold_propagates_until_predict_is_implemented` kończą się
  niepowodzeniem, a pozostałe nadal sprawdzają gotowe części. Ich przejście nie potwierdza więc
  Twojej implementacji.
- Gotowy import w sekcji 6 obejmuje `histogram_counts` i `psi`. Funkcję `brightness_feature`,
  potrzebną w scenariuszach, trzeba zaimportować z `monitoring.py` samodzielnie.
- Notebook nie ma gotowych asercji. Porównanie z sekcji 4 sprawdza zgodność API z Twoim `predict`, a
  nie poprawność preprocessingu: wspólny błąd w `preprocess_image_bytes` przejdzie to porównanie.
  Preprocessing sprawdzasz w sekcjach 1 i 8.
- Wynik diagnozy z sekcji 8 jest pomiarem. Różnica preprocessingu zmienia logity, ale liczba
  zmienionych predykcji na kilkunastu obrazach może być mała.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

## Oczekiwane rezultaty

- Notebook laboratorium 14 wykonany od początku do końca bez błędu, z Twoim kodem w miejscach
  oznaczonych `TODO` i raportem audytu.
- W laboratorium 15 artefakt, uzupełnione pliki aplikacji i notebook wykonany do końca, z pomiarami,
  scenariuszami monitoringu i raportem o decyzji wdrożeniowej.

## Wskazówki

- Laboratoria 14 i 15 korzystają z tego samego zbioru EuroSAT i tych samych wag ResNet18 co
  laboratoria 07 i 08. Po wcześniejszym uruchomieniu tamtych laboratoriów zasoby są już w pamięci
  podręcznej.
- Jeśli zmienisz plik w `app/` albo `benchmark.py` po zaimportowaniu go w notebooku, zrestartuj
  kernel, żeby notebook wczytał nową wersję.
- Notebooki i instrukcje po angielsku (`lab.en.ipynb`, `README.md`) mają tę samą strukturę.
- To jest ostatni zestaw Deep Learning. Pozostałe laboratoria znajdziesz w zestawach
  [1](fundamentals.md), [2](computer-vision-and-representations.md), [3](sequences-and-language.md)
  i [4](generative-modeling.md).
