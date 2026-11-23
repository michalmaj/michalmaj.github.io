---
title: "Widzenie komputerowe i reprezentacje"
summary: "Laboratoria 06–08 z repozytorium Deep Learning: projektowanie i analiza sieci konwolucyjnej na KMNIST, adaptacja pretrenowanego ResNet18 do zdjęć satelitarnych EuroSAT oraz wyszukiwanie podobnych obrazów na podstawie embeddingów. Laboratoria pobierają zbiory danych i wagi modelu przy pierwszym uruchomieniu."
status: published
materials:
  - repository: deep-learning
    path: README.pl.md
    lang: pl
    label: "Opis kursu: konfiguracja, uruchomienie JupyterLab i pamięć podręczna danych"
  - repository: deep-learning
    path: data/registry.yml
    lang: en
    label: "Rejestr danych: źródła, licencje i sposób pobierania KMNIST, EuroSAT i wag ResNet18"
tasks:
  lab-06:
    materials:
      - repository: deep-learning
        path: labs/06_cnn/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 06 — Projektowanie, trenowanie i analiza CNN"
      - repository: deep-learning
        path: labs/06_cnn/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/06_cnn/lab.ipynb"
      - repository: deep-learning
        path: lectures/06_cnn/lecture.md
        lang: pl
        label: "Wykład 06: Od pikseli do cech w konwolucyjnych sieciach neuronowych"
  lab-07:
    materials:
      - repository: deep-learning
        path: labs/07_transfer_learning/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 07 — Adaptacja modelu pretrained do nowego zadania"
      - repository: deep-learning
        path: labs/07_transfer_learning/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/07_transfer_learning/lab.ipynb"
      - repository: deep-learning
        path: lectures/07_transfer_learning/lecture.md
        lang: pl
        label: "Wykład 07: Transfer learning i ponowne wykorzystanie reprezentacji"
  lab-08:
    materials:
      - repository: deep-learning
        path: labs/08_embeddings/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 08 — System wyszukiwania podobnych obrazów"
      - repository: deep-learning
        path: labs/08_embeddings/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/08_embeddings/lab.ipynb"
      - repository: deep-learning
        path: lectures/08_embeddings/lecture.md
        lang: pl
        label: "Wykład 08: Embeddingi i geometria przestrzeni cech"
---
Ten zestaw obejmuje drugą grupę laboratoriów z repozytorium Deep Learning, nazwaną w opisie kursu
„Widzenie komputerowe i reprezentacje”. Najpierw projektujesz i porównujesz własne sieci
konwolucyjne (CNN), potem adaptujesz model wytrenowany na ImageNet do zdjęć satelitarnych, a na
koniec używasz jego reprezentacji do wyszukiwania podobnych obrazów. Trzy zadania odpowiadają
laboratoriom 06–08, w kolejności z repozytorium.

## Status materiałów

Repozytorium jest w rozbudowie i jego treści mogą się jeszcze zmieniać. Ta strona opisuje wersję z
gałęzi `main`, którą pobiera polecenie `git clone`. Wydanie `v1.0.0` z 19 października 2026 roku
zawiera starsze wersje instrukcji i notebooków. W laboratorium 07 część pracy, która w wydaniu była
w rdzeniu, na `main` jest rozszerzeniem opcjonalnym.

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
`TODO` i komórki Markdown na odpowiedzi. Laboratoria tego zestawu korzystają z pojęć z laboratoriów
01–05, na przykład z normalizacji bez przecieku danych z laboratorium 05.

- **Sprzęt:** według opisu kursu wystarcza procesor (CPU). Laboratoria korzystają ze zmniejszonych
  podzbiorów danych: w laboratorium 06 jest to 5000 obrazów treningowych, 1000 walidacyjnych i 1500
  testowych, a w laboratoriach 07 i 08 po 50 obrazów z każdej klasy. Notebooki laboratoriów 06 i 07
  wybierają kartę graficzną CUDA, jeśli jest dostępna, a w przeciwnym razie procesor. Laboratorium
  08 zawsze liczy na procesorze. Większy podzbiór albo dłuższy trening instrukcje proponują tylko
  jako rozszerzenie.
- **Pomiary czasu:** laboratoria każą mierzyć czas treningu i inferencji (06), treningu (07) oraz
  ekstrakcji embeddingów (08). Opis kursu zaznacza, że czas zależy od komputera i żaden materiał nie
  zależy od konkretnej szybkości.

## Dane i modele do pobrania

Notebooki pobierają dane i wagi automatycznie przy pierwszym uruchomieniu sekcji 1. Potrzebujesz
wtedy połączenia z internetem. Kolejne uruchomienia korzystają z plików zapisanych w pamięci
podręcznej.

- **KMNIST** (laboratorium 06): odręcznie pisane znaki kuzushiji, 60 000 obrazów treningowych i
  10 000 testowych, 28 × 28 pikseli w skali szarości, 10 klas. Pobiera je
  `torchvision.datasets.KMNIST`. Na dysku zajmują około 75 MB.
- **EuroSAT** (laboratoria 07 i 08): 27 000 zdjęć satelitarnych RGB 64 × 64 piksele, 10 klas użycia
  terenu. Pobiera je `torchvision.datasets.EuroSAT` z kopii zbioru w Hugging Face. Archiwum i
  rozpakowane pliki zajmują około 230 MB.
- **Wagi ResNet18 `IMAGENET1K_V1`** (laboratoria 07 i 08): pobiera je torchvision z
  `download.pytorch.org`. Zajmują około 45 MB.

Zbiory danych zapisują się w katalogu `data_cache/` w głównym katalogu repozytorium, a opis kursu
podaje zmienną `DEEP_LEARNING_DATA_CACHE`, którą możesz wskazać inny katalog (ścieżka bezwzględna).
Wagi ResNet18 trafiają do pamięci podręcznej PyTorcha, domyślnie `~/.cache/torch`, a nie do
`data_cache/`. Żadne z tych plików nie trafiają do Gita. Rejestr danych w materiałach zestawu podaje
dla każdego zbioru autorów, licencję oraz sposób pobierania i weryfikacji plików.

## Samodzielna praca i sprawdzanie wyników

Sprawdzanie działa tak samo jak w [zestawie 1](fundamentals.md). Testy repozytorium sprawdzają tylko
szkielet notebooka, czyli to, że dostarczony kod działa do pierwszego `TODO`. Testy laboratoriów
06–08 pobierają dane, dlatego są oznaczone jako `network`. Gotowe asercje w notebookach sprawdzają
wybrane elementy, a opis każdego zadania podaje, które. Wyniki eksperymentów pochodzą z Twojego
przebiegu, a interpretacji w komórkach Markdown nic nie sprawdza automatycznie. Repozytorium nie
zawiera rozwiązań laboratoriów.

W laboratoriach 06 i 07 instrukcja wymaga, żeby o wyborze modelu albo strategii decydował zbiór
walidacyjny, a zbiór testowy był użyty dopiero w sekcji porównania. We wszystkich trzech
laboratoriach wnioski mają się odwoływać do Twoich wyników i pokazanych przykładów.

Każda instrukcja kończy się sekcją „Kryteria oceny”. Opisuje ona, po czym poznać merytorycznie
kompletny wynik laboratorium, i możesz jej używać do samodzielnego sprawdzenia pracy. Ta strona nie
przenosi tej sekcji i nie traktuje jej jako zasad zaliczenia przedmiotu.

## Materiały

Instrukcje i notebooki są po polsku i po angielsku. Instrukcja opisuje problem i dane, kolejne
sekcje notebooka, pytania do wniosków i kryteria oceny. Rejestr danych jest po angielsku. Pełną
listę wykładów i laboratoriów znajdziesz na stronie [„Materiały
przedmiotu”](../guides/course-materials.md).

## Zadania

### Projektowanie, trenowanie i analiza CNN {#lab-06}

Obrazy KMNIST to odręcznie pisane znaki kuzushiji z dziesięciu klas. Celem nie jest kolejne
porównanie CNN z MLP. Laboratorium sprawdza, jak decyzje projektowe dotyczące samej sieci
konwolucyjnej wpływają na jakość, rozmiar i koszt modelu.

**Cel:** zaprojektować dwa warianty CNN różniące się nazwanym i uzasadnionym elementem, porównać je
z modelem bazowym pod względem accuracy, liczby parametrów i czasu oraz przeanalizować błędy
najlepszego wariantu.

**Zakres pracy:**

- **Dane (sekcje 1–2):** za pomocą `torch.bincount` liczysz przykłady każdej klasy w
  `train_full.targets` i oceniasz, czy zbiór jest zbalansowany i co to znaczy dla interpretacji
  accuracy. Uzupełniasz `make_split`, która wydziela zbiór walidacyjny z danych treningowych bez
  powtórzeń indeksów, oraz `normalize_with_train_stats`, która liczy średnią i odchylenie
  standardowe pikseli wyłącznie na `X_train_raw` i stosuje je do wszystkich trzech zbiorów.
- **Model bazowy (sekcja 3, gotowe):** `Flatten` i jedna warstwa `Linear` oraz gotowa funkcja
  `train_eval`, która trenuje model i zwraca jego metryki.
- **Wariant 1 (sekcje 4–5):** klasa `CNNVariant1(nn.Module)` z `nn.Conv2d`, funkcją aktywacji i
  opcjonalnie `nn.MaxPool2d`, która przyjmuje `(N, 1, 28, 28)` i zwraca `(N, 10)`. Gotowa funkcja
  `print_shapes` pokazuje kształt tensora po każdej warstwie. W 2–3 zdaniach opisujesz i uzasadniasz
  liczbę warstw i filtrów, rozmiar kernela i pooling. Potem trenujesz wariant przez `train_eval` i
  zapisujesz accuracy walidacyjną, liczbę parametrów i czas treningu.
- **Wariant 2 (sekcja 6):** najpierw zapisujesz w 2–3 zdaniach hipotezę, którą sprawdza zmiana, a
  potem piszesz `CNNVariant2`. Musi się różnić od wariantu 1 co najmniej jednym konkretnym
  elementem: liczbą filtrów, rozmiarem kernela, poolingiem albo głębokością. Kształty sprawdzasz tak
  samo jak w sekcji 4.
- **Porównanie (sekcja 7):** model bazowy i oba warianty trenujesz dla co najmniej dwóch ziaren
  losowości, na przykład `seed=0` i `seed=1`, przekazując do `train_eval` klasę modelu. Zestawienie
  obejmuje accuracy walidacyjną i testową, liczbę parametrów oraz czas treningu i inferencji.
- **Analiza błędów (sekcja 8):** dla wariantu najlepszego według walidacji rysujesz macierz pomyłek
  na zbiorze testowym i pokazujesz 6–8 błędnie sklasyfikowanych przykładów z prawdziwą i
  przewidzianą etykietą. W 3–5 zdaniach wskazujesz najczęściej mylone klasy i oceniasz podobieństwo
  wizualne tych znaków.
- **Wnioski (sekcja 9):** cztery pytania, w odniesieniu do wyników z sekcji 7 i 8.
- **Rozszerzenie opcjonalne:** trzeci wariant architektury, precision i recall dla każdej klasy albo
  powtórzenie porównania na większym podzbiorze lub z większą liczbą epok.

**Rezultat:** notebook wykonany do końca, z rozkładem klas, dwoma udokumentowanymi wariantami CNN,
zestawieniem trzech modeli dla co najmniej dwóch ziaren, macierzą pomyłek, przykładami błędów i
wnioskami.

**Sprawdź się:**

- Gotowe asercje w sekcji 2 sprawdzają, że zbiory treningowy i walidacyjny się nie nakładają oraz że
  `X_train` po normalizacji ma średnią bliską 0 i odchylenie standardowe bliskie 1. Druga asercja
  przechodzi także wtedy, gdy statystyki policzysz na wszystkich danych razem, więc nie wykrywa
  przecieku. To, czy statystyki pochodzą tylko z `X_train_raw`, zależy od Twojego kodu.
- Błędny rozmiar wejścia do `nn.Linear` ujawnia się już w `print_shapes`, przed treningiem.
- Gotowa funkcja `train_eval` zwraca też dokładność testową (`test_acc`), a gotowe komórki sekcji 3
  i 5 wypisują cały słownik wyników. Instrukcja każe wybierać model na podstawie walidacji i używać
  zbioru testowego dopiero w sekcji 7.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

### Adaptacja modelu pretrained do nowego zadania {#lab-07}

Zdjęcia satelitarne EuroSAT wizualnie bardzo różnią się od codziennych zdjęć z ImageNet.
Laboratorium sprawdza, czy transfer learning z ResNet18 nadal pomaga i czy częściowy fine-tuning
poprawia wynik zamrożonego backbone'u. Gotowy kod wybiera 500 zbalansowanych obrazów, po 50 z każdej
klasy, i dzieli je na zbiory treningowy, walidacyjny i testowy po 30, 10 i 10 obrazów na klasę.

**Cel:** poprawnie przygotować pretrenowany model do nowego zadania, wytrenować samą głowicę na
zamrożonym backbonie, wykonać częściowy fine-tuning z dwoma learning rate i zdiagnozować błąd,
którego nie widać w `requires_grad`.

**Zakres pracy:**

- **Dane i preprocessing (sekcje 1–2):** po obejrzeniu jednego obrazu z każdej klasy zapisujesz w
  jednym zdaniu, czy dane przypominają ImageNet i czy transfer powinien pomóc. Do tej intuicji
  wracasz we wnioskach. Funkcja `build_preprocess()` zwraca transformację z
  `ResNet18_Weights.IMAGENET1K_V1` przez `weights.transforms()`, bez ręcznego przepisywania wartości
  normalizacji.
- **Model (sekcja 4):** w `build_model` wczytujesz `resnet18` z jawnie wskazanymi wagami
  `IMAGENET1K_V1`, bez aliasu `DEFAULT`, i zastępujesz `model.fc` warstwą `nn.Linear` z 10
  wyjściami. Potem sprawdzasz w kodzie liczbę wyjść i to, że `model.fc` wskazuje na nową warstwę.
- **Zamrożony backbone (sekcja 5):** zamrażasz parametry backbone'u, zostawiasz trenowalną głowicę i
  ustawiasz tryb modelu tak, żeby statystyki BatchNorm w backbonie się nie zmieniały. Kolejność ma
  znaczenie: najpierw wymiana głowicy, potem zamrożenie i optymalizator. Głowicę trenujesz gotową
  funkcją `train_eval` przez 15 epok i zapisujesz accuracy walidacyjną oraz czas treningu. Na koniec
  sprawdzasz w kodzie, że parametry backbone'u się nie zmieniły.
- **Częściowy fine-tuning (sekcja 6):** odmrażasz `layer4` i głowicę oraz budujesz dwie grupy
  parametrów, w których `layer4` ma niższy learning rate niż głowica. W 2–3 zdaniach podajesz obie
  wartości i uzasadniasz ich stosunek. Po treningu przez 8 epok sprawdzasz, że `layer1`–`layer3` się
  nie zmieniły.
- **Zadanie diagnostyczne (sekcja 7):** gotowy kod nie zgłasza wyjątku, ale strata nie maleje, a
  accuracy zostaje na poziomie losowego zgadywania. Hipotezę weryfikujesz w kodzie, jak podpowiada
  komentarz `TODO`. W 4–6 zdaniach wskazujesz konkretną linię, opisujesz stratę, `requires_grad` i
  zawartość `param_groups` oraz wyjaśniasz, dlaczego samo sprawdzenie `requires_grad` nie ujawnia
  błędu.
- **Porównanie (sekcja 8):** zestawiasz zamrożony backbone i częściowy fine-tuning pod względem
  accuracy walidacyjnej i testowej, liczby trenowalnych parametrów oraz czasu treningu. Zbiór
  testowy może zostać użyty dopiero tutaj. Komentarz `TODO` w notebooku wymienia tylko accuracy i
  czas, a instrukcja dodaje liczbę trenowalnych parametrów.
- **Analiza błędów (sekcja 9):** dla strategii wybranej na walidacji rysujesz macierz pomyłek na
  zbiorze testowym i pokazujesz 6–8 błędnie sklasyfikowanych obrazów. Do wyświetlenia trzeba
  odwrócić normalizację. W 3–5 zdaniach wskazujesz najczęściej mylone klasy i oceniasz, czy wyjaśnia
  je podobny wygląd terenu z lotu ptaka.
- **Wnioski (sekcja 10):** trzy pytania, w odniesieniu do wyników z sekcji 5–9 i do eksperymentu
  Caltech101 z wykładu.
- **Rozszerzenia opcjonalne:** inny stosunek learning rate albo odmrożenie `layer3` razem z `layer4`
  (komórka w sekcji 8), trening od zera albo pełny fine-tuning z porównaniem kosztu.

**Rezultat:** notebook wykonany do końca, z preprocessingiem zgodnym z wagami, wynikami obu
strategii i ich weryfikacją, diagnozą z sekcji 7, zestawieniem strategii, macierzą pomyłek z
przykładami błędów i wnioskami.

**Sprawdź się:**

- Gotowa asercja w sekcji 2 sprawdza tylko kształt obrazu po transformacji, `(3, 224, 224)`.
  Przechodzi więc także dla transformacji bez normalizacji ImageNet.
- Weryfikację głowicy i zamrożenia piszesz samodzielnie. Gotowy kod zapisuje do niej kopie
  parametrów sprzed treningu (`before_backbone`, `before_frozen_part`). Te kopie obejmują tylko
  parametry, nie statystyki BatchNorm. W sekcji 5 o tym, czy statystyki się nie zmieniają, decyduje
  tryb modelu, o który prosi instrukcja.
- W sekcji 6 komentarz `TODO` każe przełączyć model w `model.train()`, żeby BatchNorm w `layer4` się
  dostosowywał. W tym trybie zmieniają się też statystyki BatchNorm w zamrożonych warstwach, a
  porównanie z kopią parametrów tego nie pokazuje.
- Gotowa funkcja `train_eval` zwraca też dokładność testową (`test_acc`), a instrukcja każe używać
  zbioru testowego dopiero w sekcji 8.
- Komórka rozszerzenia opcjonalnego w sekcji 8 zgłasza `NotImplementedError`, dopóki jej nie
  uzupełnisz, więc zatrzymuje wykonywanie wszystkich komórek po kolei.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

### System wyszukiwania podobnych obrazów {#lab-08}

Mały system wyszukiwania obrazów EuroSAT ma dla obrazu zapytania zwrócić ranking najbardziej
podobnych obrazów z bazy. Gotowy kod dzieli dane na dwa rozłączne zbiory: `gallery` (40 obrazów z
każdej klasy, łącznie 400) i `queries` (10 innych obrazów z każdej klasy, łącznie 100).

**Cel:** wyodrębnić embeddingi z pretrenowanego ResNet18, zaimplementować wyszukiwanie top-k i
metrykę Precision@k bez gotowych funkcji wyszukiwania sąsiadów oraz sprawdzić, jak reprezentacja,
normalizacja i metryka wpływają na wynik.

**Zakres pracy:**

- **Dane (sekcja 1):** w kodzie potwierdzasz, że `gallery_indices` i `query_indices` nie mają
  wspólnych elementów. Gdyby obraz zapytania był też w `gallery`, wyszukiwarka znalazłaby go z
  podobieństwem 1,0 i sztucznie zawyżyła metryki.
- **Embeddingi (sekcja 2):** z `resnet18` z wagami `IMAGENET1K_V1` wyodrębniasz wyjście `avgpool`,
  nie logity z `fc`, dla obrazów obu zbiorów. Model ma działać w trybie, który nie aktualizuje
  statystyk BatchNorm, a obliczenia w kontekście bez budowania grafu gradientów. Mierzysz czas
  ekstrakcji. W 2–3 zdaniach wskazujesz cztery konkretne zmiany, które unieważniłyby cache
  embeddingów zapisany na dysku dla bazy 1000 razy większej.
- **Normalizacja i wyszukiwanie (sekcje 3–4):** `l2_normalize(X)` dzieli każdy embedding przez jego
  normę i chroni przed dzieleniem przez zero. `search(query_embedding, gallery_embeddings, k)`
  zwraca indeksy `k` obrazów o największym cosine similarity, od najlepszego, za pomocą mnożenia
  macierzowego i sortowania.
- **Precision@k (sekcja 5):**
  `precision_at_k(query_embeddings, query_labels, gallery_embeddings, gallery_labels, k)` zwraca
  średnie Precision@k dla wszystkich zapytań. Trafienie oznacza tę samą klasę co zapytanie.
  Instrukcja nazywa to uproszczeniem, do którego wracasz we wnioskach. Gotowa komórka liczy
  Precision@1, @5 i @10 dla znormalizowanych embeddingów.
- **Porównania (sekcje 6–7):** te same metryki dla surowych, spłaszczonych pikseli oraz Precision@5
  dla trzech wariantów: cosine similarity na embeddingach znormalizowanych L2, iloczyn skalarny i
  odległość euklidesowa na embeddingach nieznormalizowanych. Wszystkie porównania korzystają z tych
  samych zbiorów `gallery` i `queries`. W 3–4 zdaniach wskazujesz najlepszy wariant, wielkość
  różnicy i jej związek z rolą normy z wykładu.
- **Analiza błędów (sekcja 8):** wybierasz dokładnie dwa zapytania, z wysokim i z niskim
  Precision@5, i pokazujesz każde z pięcioma najlepszymi wynikami. Do wyświetlenia obrazów trzeba
  odwrócić normalizację. W 3–5 zdaniach oceniasz dla słabszego zapytania, czy błędne wyniki mają
  podobną teksturę lub klasę terenu, czy wyglądają przypadkowo, i wymieniasz konkretne klasy.
- **Wnioski (sekcja 9):** cztery pytania, w odniesieniu do wyników z sekcji 5–8.
- **Rozszerzenia opcjonalne:** najczęstsze błędne pary klas, cache na dysku z jawnym tagiem ważności
  albo wpływ rozmiaru `gallery`.

**Rezultat:** notebook wykonany do końca, z embeddingami, działającym wyszukiwaniem i Precision@k,
porównaniem z modelem bazowym na pikselach, porównaniem trzech wariantów metryki, dwoma
zwizualizowanymi zapytaniami i wnioskami.

**Sprawdź się:**

- Gotowe asercje sprawdzają, że normy po `l2_normalize` są bliskie 1 oraz że `search` i
  `precision_at_k` dają oczekiwany wynik na małym przykładzie z sześcioma wektorami 2D. Ten przykład
  przechodzi także wtedy, gdy `search` nie normalizuje wektorów, więc nie odróżnia cosine similarity
  od iloczynu skalarnego. Różnicę między wariantami pokazuje dopiero porównanie z sekcji 7.
- Tryb modelu i kontekst bez gradientów w sekcji 2 nie są sprawdzane automatycznie.
- Rozłączność zbiorów potwierdzasz w sekcji 1 własnym kodem. Kryteria oceny wymagają, żeby ta
  asercja przechodziła.
- Komentarz `TODO` w sekcji 7 nazywa wynik z sekcji 5 `p_cosine_norm`, ale gotowa komórka sekcji 5
  nie zapisuje go pod tą nazwą.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

## Oczekiwane rezultaty

- Trzy notebooki laboratoriów 06–08 wykonane od początku do końca bez błędu, z Twoim kodem w
  miejscach oznaczonych `TODO`.
- W każdym notebooku zestawienia, macierze pomyłek albo wizualizacje wyników z Twojego przebiegu
  oraz odpowiedzi w komórkach Markdown, które odwołują się do otrzymanych wartości i przykładów.

## Wskazówki

- Pierwsze uruchomienie sekcji 1 w laboratoriach 06–08 pobiera dane. Zrób je wtedy, gdy masz
  połączenie z internetem i wolne miejsce na dysku.
- Laboratoria 07 i 08 korzystają z tego samego zbioru EuroSAT i tych samych wag ResNet18, więc
  pobierasz je tylko raz.
- Jeśli zmienisz funkcję zdefiniowaną wcześniej, uruchom ponownie jej komórkę i komórki, które z
  niej korzystają. Notebook pamięta stan z poprzednich uruchomień.
- Notebooki i instrukcje po angielsku (`lab.en.ipynb`, `README.md`) mają tę samą strukturę.
