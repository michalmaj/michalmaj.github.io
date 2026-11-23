---
title: "Modelowanie generatywne"
summary: "Laboratoria 12–13 z repozytorium Deep Learning: wykrywanie anomalii przez błąd rekonstrukcji autoenkodera na Fashion-MNIST oraz samodzielna implementacja i ocena małego modelu dyfuzyjnego DDPM na zbiorze dwóch półksiężyców."
status: published
materials:
  - repository: deep-learning
    path: README.pl.md
    lang: pl
    label: "Opis kursu: konfiguracja, uruchomienie JupyterLab i pamięć podręczna danych"
  - repository: deep-learning
    path: data/registry.yml
    lang: en
    label: "Rejestr danych: źródło, licencja i sposób pobierania Fashion-MNIST"
tasks:
  lab-12:
    materials:
      - repository: deep-learning
        path: labs/12_autoencoders/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 12 — Detekcja anomalii za pomocą autoenkodera"
      - repository: deep-learning
        path: labs/12_autoencoders/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/12_autoencoders/lab.ipynb"
      - repository: deep-learning
        path: lectures/12_autoencoders/lecture.md
        lang: pl
        label: "Wykład 12: Autoenkodery, VAE i przestrzeń latentna"
  lab-13:
    materials:
      - repository: deep-learning
        path: labs/13_diffusion/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 13 — Samodzielna implementacja i analiza niewielkiego modelu dyfuzyjnego (DDPM)"
      - repository: deep-learning
        path: labs/13_diffusion/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/13_diffusion/lab.ipynb"
      - repository: deep-learning
        path: lectures/13_diffusion/lecture.md
        lang: pl
        label: "Wykład 13: Modele dyfuzyjne: uczenie generowania przez odszumianie"
---
Ten zestaw obejmuje czwartą grupę laboratoriów z repozytorium Deep Learning, nazwaną w opisie kursu
„Modelowanie generatywne”. W laboratorium 12 autoenkoder uczy się rekonstruować tylko obrazy jednej
klasy, a błąd rekonstrukcji służy do wykrywania anomalii, nie do generowania obrazów. W laboratorium
13 implementujesz od podstaw matematyczny rdzeń modelu dyfuzyjnego DDPM i oceniasz wygenerowane
próbki liczbowo, na niezależnym zbiorze i względem prostego modelu bazowego. Dwa zadania odpowiadają
laboratoriom 12–13, w kolejności z repozytorium.

## Status materiałów

Repozytorium jest w rozbudowie i jego treści mogą się jeszcze zmieniać. Ta strona opisuje instrukcje
i notebooki z gałęzi `main` (commit `0ffe385`), którą pobiera polecenie `git clone`. Wydanie
`v1.0.0` z 19 października 2026 roku zawiera starsze wersje: w laboratorium 12 inną wersję
instrukcji i notebooka, a w laboratorium 13 inną wersję notebooka (instrukcja się nie zmieniła).
Instrukcji i notebooka korzystaj z tej samej wersji.

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
`TODO` i komórki Markdown na odpowiedzi. W laboratorium 13 komórki na odpowiedzi mają tekst „(Twoja
odpowiedź tutaj.)”. Laboratorium 12 korzysta z zasad z wcześniejszych laboratoriów: próg i decyzje
wybierasz bez użycia zbioru testowego.

- **Sprzęt:** według opisu kursu wystarcza procesor (CPU). Notebooki obu laboratoriów zawsze liczą
  na procesorze (`device = torch.device("cpu")`).
- **Losowość:** oba notebooki ustawiają ziarno (`torch.manual_seed`). Laboratorium 13 losuje też
  szum przy treningu i generowaniu, a funkcja `ddpm_sample` ustawia własne ziarno.

## Dane do pobrania

Laboratorium 13 generuje dane syntetyczne w notebooku (funkcja `sample_two_moons`). Laboratorium 12
przy pierwszym uruchomieniu pobiera Fashion-MNIST przez `torchvision.datasets.FashionMNIST`: 60 000
obrazów treningowych i 10 000 testowych, 28 × 28 pikseli w skali szarości. Pliki zajmują około 85 MB
w katalogu `data_cache/` i nie trafiają do Gita. Potrzebujesz wtedy połączenia z internetem. Żadne z
laboratoriów nie pobiera wytrenowanych modeli ani wag.

## Samodzielna praca i sprawdzanie wyników

Sprawdzanie działa tak samo jak w [zestawie 1](fundamentals.md). Testy repozytorium sprawdzają
szkielet notebooka, czyli to, że dostarczony kod działa do pierwszego `TODO`. Oba laboratoria mają
też osobne testy wzorów, które opisują instrukcje (np. metryki na znanym przykładzie, ostatni krok
próbkowania bez szumu, MMD). Te testy nie uruchamiają Twojego notebooka. Test szkieletu laboratorium
12 pobiera dane, dlatego jest oznaczony jako `network`. Gotowe asercje w notebookach sprawdzają
wybrane elementy, a opis każdego zadania podaje, które. Jakości wygenerowanych próbek i
interpretacji w komórkach Markdown nic nie sprawdza automatycznie. Repozytorium nie zawiera
rozwiązań laboratoriów.

Każda instrukcja kończy się sekcją „Kryteria oceny”. Opisuje ona, po czym poznać merytorycznie
kompletny wynik laboratorium, i możesz jej używać do samodzielnego sprawdzenia pracy. Ta strona nie
przenosi tej sekcji i nie traktuje jej jako zasad zaliczenia przedmiotu.

## Materiały

Instrukcje i notebooki są po polsku i po angielsku. Instrukcja opisuje problem i dane, kolejne
sekcje notebooka, pytania do wniosków i kryteria oceny. Rejestr danych jest po angielsku. Pełną
listę wykładów i laboratoriów znajdziesz na stronie [„Materiały
przedmiotu”](../guides/course-materials.md).

## Zadania

### Detekcja anomalii za pomocą autoenkodera {#lab-12}

Klasą normalną jest *Sneaker* (7), a pozostałe dziewięć klas Fashion-MNIST to anomalie. Autoenkoder
uczy się wyłącznie rekonstrukcji obrazów klasy normalnej, bez etykiet i bez przykładów anomalii.
Instrukcja zaznacza, że to nie jest klasyfikacja dziesięciu klas.

**Cel:** przygotować rozłączne podzbiory bez przecieku, wyznaczyć próg tylko z danych normalnych,
samodzielnie zaimplementować i sprawdzić metryki detekcji oraz uczciwie porównać autoenkoder z
prostym modelem bazowym, łącznie z przypadkami, w których metoda zawodzi.

**Zakres pracy:**

- **Dane i podział (sekcja 1):** tworzysz `ae_train_X`, `val_normal_X`, `val_anomaly_X`,
  `test_normal_X` oraz `test_anomaly_X` z `test_anomaly_labels`, wypisujesz ich rozmiary i w kodzie
  potwierdzasz rozłączność indeksów. Podzbiory testowe służą tylko do jednorazowej oceny końcowej.
- **Autoenkoder (sekcja 2):** trenujesz model wyłącznie na `ae_train_X`, z wymiarem latentnym 16. W
  notebooku klasa `AE` i funkcja `train_ae` są gotowe, choć instrukcja opisuje je jako część do
  zaimplementowania.
- **Błąd rekonstrukcji (sekcja 3):** `per_image_error(model, X)` zwraca błąd dla każdego obrazu. Dla
  `val_normal` i `val_anomaly` podajesz średnią, odchylenie standardowe i medianę i rysujesz oba
  rozkłady na wspólnym histogramie.
- **Próg (sekcja 4):** wyznaczasz go wyłącznie z rozkładu błędów `val_normal`, na przykład jako
  średnią powiększoną o uzasadnioną wielokrotność odchylenia standardowego.
- **Metryki (sekcja 5):** `confusion_counts` i `precision_recall_f1` sprawdzasz najpierw na znanym
  przykładzie z instrukcji, a ROC-AUC i PR-AUC implementujesz samodzielnie, bo repozytorium nie ma
  `scikit-learn`. Na zbiorze testowym podajesz precision, recall, F1, macierz pomyłek 2 × 2, ROC-AUC
  i PR-AUC.
- **Model bazowy i analiza błędów (sekcja 6):** liczysz te same metryki dla odległości od średniego
  obrazu klasy normalnej i porównujesz z autoenkoderem, bez zakładania z góry przewagi którejś
  metody. Pokazujesz i opisujesz jeden false negative (anomalia z niskim błędem) i jeden false
  positive (obraz klasy Sneaker z wysokim błędem).
- **Zadanie diagnostyczne (sekcja 7):** gotowy kod wybiera próg z najwyższym F1 na etykietach zbioru
  testowego. Porównujesz ten próg i jego F1 z uczciwym wynikiem i wyjaśniasz, dlaczego procedura
  jest błędna niezależnie od wielkości różnicy w tym przebiegu.
- **Wnioski (sekcja 8):** pięć pytań, w odniesieniu do liczb i przykładów z sekcji 3–7.
- **Rozszerzenie opcjonalne (jedno z dwóch):** powtórzenie sekcji 2–5 dla wymiaru latentnego 4 i 32
  albo analogiczny VAE z błędem rekonstrukcji lub −ELBO jako wynikiem anomalii.

**Rezultat:** notebook wykonany do końca, z rozłącznymi podzbiorami, autoenkoderem trenowanym tylko
na danych normalnych, rozkładami błędów, progiem z `val_normal`, sprawdzonymi metrykami, porównaniem
z modelem bazowym, analizą FN i FP, diagnozą przecieku i wnioskami.

**Sprawdź się:**

- Notebook nie ma gotowych asercji dla Twojego kodu. Wartości oczekiwane dla znanego przykładu (TP =
  5, FP = 1, TN = 4, FN = 0, precision ≈ 0,833, recall = 1,0, F1 ≈ 0,909) podaje instrukcja, a
  komentarz `TODO` w sekcji 5 dodaje oczekiwane ROC-AUC = 0,84 i PR-AUC = 0,81.
- Nic nie sprawdza automatycznie, czy próg zależy tylko od `val_normal`, ani czy autoenkoder był
  trenowany wyłącznie na danych normalnych. Oba błędy dają wynik bez komunikatu.
- Gotowa komórka z sekcji 7 korzysta z Twoich zmiennych i funkcji z sekcji 3 i 5 (`err_test_normal`,
  `err_test_anomaly`, `confusion_counts`, `precision_recall_f1`), więc ich nazwy i sygnatury muszą
  się zgadzać z komentarzami `TODO`.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

### Samodzielna implementacja i analiza niewielkiego modelu dyfuzyjnego (DDPM) {#lab-13}

Dane to dwa półksiężyce (*two moons*) w dwóch wymiarach, inny problem niż mieszanina rozkładów
Gaussa z wykładu. Instrukcja podkreśla, że brak błędu wykonania nie jest dowodem poprawności modelu
generatywnego: jakość trzeba zmierzyć, a nie tylko ocenić wykres „na oko”.

**Cel:** samodzielnie zaimplementować harmonogram, zamkniętą postać forward diffusion, funkcję celu
i odwrotne próbkowanie DDPM, zweryfikować je i krytycznie ocenić wygenerowane próbki metrykami
ilościowymi względem niezależnego zbioru i modelu bazowego.

**Zakres pracy:**

- **Dane i harmonogram (sekcje 1–2):** rysujesz `X_train` i opisujesz, dlaczego pojedynczy rozkład
  Gaussa nie opisze tego kształtu. Harmonogram liniowy `betas`, `alphas` i `alphas_bar` budujesz dla
  `T = 500` i sprawdzasz, czy ᾱ_T jest wystarczająco bliskie 0.
- **Forward diffusion (sekcja 3):** `q_sample(x0, t, eps, alphas_bar)` i wymagana weryfikacja
  statystyczna: średnia i wariancja z zamkniętej postaci porównane z symulacją krok po kroku, bez
  oczekiwania identycznych pojedynczych próbek.
- **Sieć (sekcja 4):** `NoisePredictor`, której `forward(x, t)` łączy `x` z gotowym
  `sinusoidal_embedding(t)`. W komentarzu albo komórce Markdown wyjaśniasz, czego modelowi brakuje
  bez znajomości `t`.
- **Trening (sekcja 5):** krok treningowy wewnątrz gotowej pętli `train_ddpm`: losowy batch, osobne
  `t` dla każdego przykładu, szum, `q_sample`, strata MSE względem szumu, backward i krok
  optymalizatora. Gotowa komórka rysuje krzywą straty.
- **Odwrotne próbkowanie (sekcja 6):** `ddpm_reverse_step`, w którym ostatni krok (`t_idx == 0`) nie
  dodaje szumu. Gotowa `ddpm_sample` liczy kroki z szumem i bez szumu.
- **Generowanie i ocena (sekcja 7):** 1000 nowych próbek na wspólnym wykresie z danymi treningowymi,
  z podpisem, że to nowe próbki, a nie rekonstrukcje. Liczysz co najmniej jedną metrykę ilościową na
  niezależnym zbiorze testowym (nowa próbka two moons). Notebook ma gotowe `rbf_mmd2` (MMD z jądrem
  RBF), `mean_nn_distance` i sprawdzenie MMD na znanym przypadku.
- **Jedna zmiana konfiguracji (sekcja 8):** dokładnie jedna zmiana spośród trzech z instrukcji:
  liczba kroków próbkowania z poprawnym respacing, inny harmonogram albo inna liczba epok. Jej wpływ
  mierzysz tą samą metryką.
- **Model bazowy (sekcja 9):** jeden rozkład Gaussa dopasowany do `X_train`, 1000 próbek i te same
  metryki na tym samym zbiorze testowym. Jeśli jedna metryka jest niejednoznaczna, instrukcja prosi
  o drugą, bardziej czułą na kształt, i wyjaśnienie, czemu mogą dawać różne wnioski.
- **Zadanie diagnostyczne (sekcja 10):** gotowy `NoisePredictorColleague` przyjmuje `t`, ale go nie
  używa. Trenujesz go tak samo, generujesz próbki, porównujesz metryki z poprawnym modelem,
  wyjaśniasz przyczynę i weryfikujesz poprawę po przywróceniu warunkowania czasem.
- **Wnioski (sekcja 11):** sześć pytań, w odniesieniu do liczb i przykładów z sekcji 2–10, w tym o
  obszarach danych, których model nie generuje dobrze.

**Rezultat:** notebook wykonany do końca, z harmonogramem i sprawdzonym ᾱ_T, zweryfikowanym
`q_sample`, siecią warunkowaną czasem, krzywą straty, próbkami z poprawnie obsłużonym ostatnim
krokiem, metrykami na niezależnym zbiorze, porównaniem z jedną zmianą konfiguracji i z modelem
bazowym, diagnozą i wnioskami.

**Sprawdź się:**

- Gotowe asercje sprawdzają tylko funkcję MMD na znanym przypadku (sekcja 7). Twojego kodu nie
  sprawdza żadna asercja.
- Licznik kroków w `ddpm_sample` liczy kroki po indeksie pętli, więc wypisuje oczekiwane 499 kroków
  z szumem i 1 bez szumu także wtedy, gdy Twój `ddpm_reverse_step` dodaje szum w ostatnim kroku. To,
  że ostatni krok zwraca średnią bez szumu, sprawdzasz w swoim kodzie.
- Nic nie sprawdza, czy `t` jest losowane osobno dla każdego przykładu w batchu.
- Wygenerowanych próbek nie ocenia automatycznie żaden test. O jakości decydują metryki, które
  liczysz, i Twoja interpretacja.
- Pozostałe elementy porównaj z sekcją „Ocena generowania — wymagania” i „Kryteria oceny” w
  instrukcji.

## Oczekiwane rezultaty

- Dwa notebooki laboratoriów 12–13 wykonane od początku do końca bez błędu, z Twoim kodem w
  miejscach oznaczonych `TODO`.
- W każdym notebooku rozkłady, metryki i wykresy z Twojego przebiegu oraz odpowiedzi w komórkach
  Markdown, które odwołują się do otrzymanych liczb i przykładów.

## Wskazówki

- Zbiór testowy w laboratorium 12 i niezależny zbiór testowy w laboratorium 13 służą do oceny, a nie
  do wybierania progu, konfiguracji ani metryki.
- Jeśli zmienisz funkcję zdefiniowaną wcześniej, uruchom ponownie jej komórkę i komórki, które z
  niej korzystają. Notebook pamięta stan z poprzednich uruchomień.
- Notebooki i instrukcje po angielsku (`lab.en.ipynb`, `README.md`) mają tę samą strukturę.
- Kolejny [zestaw 5, „Ewaluacja i wdrażanie”](evaluation-and-deployment.md), obejmuje laboratoria
  14–15.
