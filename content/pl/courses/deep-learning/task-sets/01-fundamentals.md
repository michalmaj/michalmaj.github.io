---
title: "Podstawy uczenia głębokiego"
summary: "Laboratoria 01–05 z repozytorium Deep Learning: regresja liniowa w PyTorchu, klasyfikacja za pomocą MLP, propagacja wsteczna od podstaw w NumPy, porównanie optymalizatorów oraz rozpoznawanie przeuczenia i dobór regularyzacji. W każdym laboratorium uzupełniasz notebook, wykonujesz eksperymenty i interpretujesz wyniki."
status: published
materials:
  - repository: deep-learning
    path: README.pl.md
    lang: pl
    label: "Opis kursu: konfiguracja, uruchomienie JupyterLab i proponowany rytm pracy"
tasks:
  lab-01:
    materials:
      - repository: deep-learning
        path: labs/01_intro/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 01 — Podstawy PyTorch, tensory, urządzenia i pierwszy model"
      - repository: deep-learning
        path: labs/01_intro/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/01_intro/lab.ipynb"
      - repository: deep-learning
        path: lectures/01_intro/lecture.md
        lang: pl
        label: "Wykład 01: Deep Learning, ML vs DL, tensory i podstawowy proces trenowania modelu"
  lab-02:
    materials:
      - repository: deep-learning
        path: labs/02_mlp/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 02 — Klasyfikacja danych tabularnych za pomocą MLP"
      - repository: deep-learning
        path: labs/02_mlp/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/02_mlp/lab.ipynb"
      - repository: deep-learning
        path: lectures/02_mlp/lecture.md
        lang: pl
        label: "Wykład 02: Perceptron, sieci wielowarstwowe (MLP) i funkcje aktywacji"
  lab-03:
    materials:
      - repository: deep-learning
        path: labs/03_backprop/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 03 — Backpropagation od podstaw w NumPy"
      - repository: deep-learning
        path: labs/03_backprop/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/03_backprop/lab.ipynb"
      - repository: deep-learning
        path: lectures/03_backprop/lecture.md
        lang: pl
        label: "Wykład 03: Backpropagation, reguła łańcuchowa i automatyczne różniczkowanie"
  lab-04:
    materials:
      - repository: deep-learning
        path: labs/04_optimization/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 04 — Eksperymentalne porównanie strategii optymalizacji"
      - repository: deep-learning
        path: labs/04_optimization/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/04_optimization/lab.ipynb"
      - repository: deep-learning
        path: lectures/04_optimization/lecture.md
        lang: pl
        label: "Wykład 04: Gradient descent, SGD, momentum i Adam"
  lab-05:
    materials:
      - repository: deep-learning
        path: labs/05_generalization/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 05 — Rozpoznawanie przeuczenia i dobór regularyzacji"
      - repository: deep-learning
        path: labs/05_generalization/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/05_generalization/lab.ipynb"
      - repository: deep-learning
        path: lectures/05_generalization/lecture.md
        lang: pl
        label: "Wykład 05: Generalizacja, overfitting i regularyzacja"
---
Ten zestaw obejmuje pierwszą grupę laboratoriów z repozytorium Deep Learning, nazwaną w opisie kursu
„Podstawy”. Zaczynasz od regresji liniowej zapisanej w PyTorchu, przechodzisz przez sieć
wielowarstwową (MLP) i ręcznie zaimplementowaną propagację wsteczną, a kończysz na porównaniu
optymalizatorów i doborze regularyzacji. Każde laboratorium składa się z instrukcji i notebooka z
gotowym szkieletem. Uzupełniasz w nim kod, wykonujesz eksperymenty i zapisujesz interpretację
wyników. Pięć zadań odpowiada laboratoriom 01–05, w kolejności z repozytorium.

## Status materiałów

Repozytorium jest w rozbudowie i jego treści mogą się jeszcze zmieniać. Ta strona opisuje wersję z
gałęzi `main`, którą pobiera polecenie `git clone`. Wydanie `v1.0.0` z 19 października 2026 roku
zawiera starsze wersje instrukcji i notebooków, więc jego opis zadań może się różnić od opisu na tej
stronie.

## Przygotowanie do zestawu

Potrzebujesz [uv](https://docs.astral.sh/uv/getting-started/installation/) i Pythona 3.12. Nie
musisz instalować Pythona osobno, bo uv pobiera właściwy interpreter. Polecenia z sekcji
„Konfiguracja” w opisie kursu pobierają repozytorium, instalują zależności i uruchamiają JupyterLab:

```bash
git clone https://github.com/michalmaj/deep-learning.git
cd deep-learning
uv sync
uv run jupyter lab
```

- **Sprzęt:** według opisu kursu do wszystkich materiałów wystarcza procesor (CPU), a karta
  graficzna (GPU) nie jest wymagana. Notebooki laboratoriów 01, 02, 04 i 05 wybierają kartę
  graficzną CUDA, jeśli jest dostępna, a w przeciwnym razie procesor. Laboratorium 03 liczy w NumPy.
- **Dane:** laboratoria 01–05 nie pobierają żadnych plików. Dane są syntetyczne i generuje je gotowy
  kod w pierwszej sekcji każdego notebooka. Połączenie z internetem jest potrzebne do pobrania
  repozytorium i do `uv sync`.
- **Przygotowanie merytoryczne:** każde laboratorium rozwija temat jednego wykładu. Opis kursu
  proponuje dla każdego tematu taki rytm: notatki wykładu (`lecture.md`), notebook wykładowy z
  eksperymentami (`examples.ipynb`), w którym zmieniasz parametry i celowo coś psujesz, potem
  laboratorium, a na koniec krytyczne przeczytanie własnych wyników.

## Jak pracujesz z laboratorium

Każde laboratorium ma katalog `labs/<NN_nazwa>/`, na przykład `labs/01_intro/`, z czterema plikami:

- `README.pl.md` to instrukcja po polsku, a `README.md` to ta sama instrukcja po angielsku;
- `lab.ipynb` to notebook do uzupełnienia po polsku, a `lab.en.ipynb` to jego wersja angielska.

W notebooku komórki z kodem do uzupełnienia mają komentarze `# TODO` i do czasu uzupełnienia
zgłaszają `NotImplementedError`. Sekcje z dopiskiem „(gotowe)” zawierają kod dostarczony z
laboratorium. Odpowiedzi i analizy zapisujesz w komórkach Markdown z tekstem „(Miejsce na
odpowiedź.)”. Komórki uruchamiasz po kolei, bo kolejne sekcje korzystają z funkcji i wyników z
wcześniejszych.

Numery sekcji podane w opisach zadań pochodzą z notebooka. W laboratoriach 01 i 02 instrukcja
numeruje sekcje inaczej niż notebook, więc szukaj ich po nazwie.

## Samodzielna praca i sprawdzanie wyników

Najpierw spróbuj wykonać laboratorium samodzielnie. Repozytorium nie zawiera rozwiązań laboratoriów.
Wykonanie laboratorium ma cztery części, a każdą sprawdza się inaczej.

- **Szkielet notebooka.** Testy repozytorium (`uv run pytest`) sprawdzają, że dostarczony kod
  notebooka działa aż do pierwszego `TODO` i że pierwszym błędem jest oczekiwany
  `NotImplementedError`. Nie sprawdzają Twojego kodu, eksperymentów ani odpowiedzi. Po uzupełnieniu
  całego notebooka test szkieletu tego laboratorium przestaje przechodzić, bo nie znajduje już
  oczekiwanego błędu. Taki wynik nie mówi więc nic o jakości Twojej pracy.
- **Twój kod.** Niektóre notebooki mają gotowe asercje, które przerywają wykonanie, gdy wybrany
  element nie działa. Opis każdego zadania podaje, co sprawdzają. Przejście asercji nie oznacza, że
  cały kod jest poprawny.
- **Eksperyment.** Kryteria oceny laboratoriów 01, 02, 03 i 05 wymagają wprost, żeby notebook
  wykonał się do końca bez błędu. Tabele i wykresy mają pochodzić z Twojego przebiegu. Aby to
  sprawdzić, uruchom ponownie kernel i wykonaj wszystkie komórki od początku.
- **Interpretacja.** Odpowiedzi w komórkach Markdown nie są sprawdzane automatycznie. Instrukcja
  mówi, do czego mają się odwoływać, na przykład do konkretnych wartości, kształtu krzywych albo
  położenia punktów na wykresie.

Każda instrukcja kończy się sekcją „Kryteria oceny”. Opisuje ona, po czym poznać merytorycznie
kompletny wynik laboratorium: działający kod, poprawnie przeprowadzony eksperyment i uzasadnione
wnioski. Możesz jej używać do samodzielnego sprawdzenia pracy. Ta strona nie przenosi tej sekcji i
nie traktuje jej jako zasad zaliczenia przedmiotu.

## Materiały

Instrukcje i notebooki są po polsku i po angielsku. Instrukcja opisuje problem i dane, kolejne
sekcje notebooka, pytania do wniosków i kryteria oceny. Pełną listę wykładów i laboratoriów
znajdziesz na stronie [„Materiały przedmiotu”](../guides/course-materials.md).

## Zadania

### Podstawy PyTorch, tensory, urządzenia i pierwszy model {#lab-01}

Dane są syntetyczne. Wartość docelowa zależy od trzech cech, a jedna z nich wpływa na nią
nieliniowo. Model liniowy wielu zmiennych ma przewidzieć tę wartość, a analiza błędów ma pokazać,
czego taki model nie potrafi przedstawić.

**Cel:** zapisać regresję liniową wielu zmiennych w postaci macierzowej, wytrenować ją spadkiem
gradientu bez `nn.Module` i `optim`, porównać z rozwiązaniem w postaci zamkniętej i na podstawie
reszt wykryć ograniczenie modelu liniowego.

**Zakres pracy:**

- **Kod:** w sekcji 2 notebooka funkcje `train_val_split`, `mse` i `r2_score`; w sekcji 4
  `forward(X, w, b)`; w sekcji 5 `closed_form_solution` (rozwiązanie *normal equation* z kolumną
  jedynek dla biasu, za pomocą `torch.linalg.solve`); w sekcji 6 `train_linear_model`, czyli pętla
  forward → strata → backward → aktualizacja.
- **Eksperyment:** gotowe sekcje 7 i 8 porównują stratę walidacyjną modelu bazowego (średnia wartość
  `y` ze zbioru treningowego), rozwiązania w postaci zamkniętej i modelu trenowanego gradientowo
  oraz liczą MSE i R² na zbiorze walidacyjnym.
- **Analiza:** w sekcji 9 gotowy kod rysuje reszty względem każdej z trzech cech. W komórce Markdown
  piszesz w 3–5 zdaniach, która cecha ma systematyczny wzorzec, jak on wygląda i jakiej zależności
  model liniowy nie potrafi wyrazić. W sekcji 10 odpowiadasz na dwa pytania: czy pomogłaby nowa
  cecha bez zmiany modelu i dlaczego porównanie z rozwiązaniem w postaci zamkniętej testuje pętlę
  treningową.

**Rezultat:** notebook wykonany do końca, z porównaniem trzech strat, metrykami walidacyjnymi,
wykresem reszt i uzasadnionymi odpowiedziami.

**Sprawdź się:** notebook nie ma gotowych asercji. Według instrukcji model trenowany gradientowo i
rozwiązanie w postaci zamkniętej powinny dać zbliżone straty, bo problem jest wypukły i ma jedno
optimum. Duża różnica wskazuje błąd w pętli treningowej, na przykład w learning rate, kroku
aktualizacji albo liczbie epok. Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

### Klasyfikacja danych tabularnych za pomocą MLP {#lab-02}

Punkty z dwóch współśrodkowych okręgów z szumem trzeba przypisać do pierścienia albo do środka.
Żadna prosta nie oddziela tych klas, więc liniowy model bazowy wypada blisko losowego zgadywania.

**Cel:** zaimplementować metryki klasyfikacji i własną klasę `nn.Module`, sprawdzić, jak liczba
neuronów i funkcja aktywacji wpływają na wynik, i powiązać to ze zdolnością reprezentacyjną
architektury.

**Zakres pracy:**

- **Kod:** w sekcji 2 funkcje `confusion_counts`, `metrics_from_preds` (accuracy, precision i
  recall, klasa 1 to okrąg wewnętrzny), `predict` i `evaluate`; w sekcji 4 klasa `MLP(nn.Module)`
  bez `nn.Sequential`, z konfigurowalną liczbą neuronów warstwy ukrytej i funkcją aktywacji; w
  sekcji 5 `train_model`, która trenuje dowolny model `nn.Module` z `BCEWithLogitsLoss`.
- **Eksperymenty:** gotowa sekcja 6 porównuje domyślny MLP (16 neuronów, ReLU) z modelem bazowym. W
  sekcji 7 porównujesz co najmniej trzy konfiguracje różniące się liczbą neuronów lub funkcją
  aktywacji, w tym jedną celowo zbyt słabą, i zbierasz ich metryki testowe w jednym zestawieniu.
- **Analizy:** w sekcji 8 interpretujesz zestawienie w 3–5 zdaniach. W sekcji 9 gotowy kod rysuje
  granicę decyzyjną domyślnego MLP z sekcji 6 i zaznacza błędnie sklasyfikowane punkty testowe, a Ty
  opisujesz w 3–5 zdaniach, gdzie leżą i z czego wynikają te błędy. W sekcji 10 odpowiadasz na dwa
  pytania.

**Rezultat:** notebook wykonany do końca, z zestawieniem konfiguracji, wykresem błędów i
uzasadnionymi odpowiedziami.

**Sprawdź się:** notebook nie ma gotowych asercji. W sekcji 6 domyślny MLP powinien wyraźnie
wyprzedzić model bazowy. Instrukcja pisze o granicy decyzyjnej „najlepszego modelu”, ale gotowy kod
w sekcji 9 rysuje ją dla domyślnego MLP. Analiza ma wynikać z tego wykresu. Pozostałe elementy
porównaj z sekcją „Kryteria oceny” w instrukcji.

### Backpropagation od podstaw w NumPy {#lab-03}

Sieć z jedną warstwą ukrytą i aktywacją tanh dopasowuje się do nieliniowej funkcji jednej zmiennej.
Propagację w przód i wstecz piszesz w NumPy, bez `loss.backward()`, dla jednej ustalonej
architektury.

**Cel:** zaimplementować propagację wsteczną ze wzorów macierzowych, sprawdzić gradienty z PyTorch
autograd i zobaczyć, jak błąd we wzorze zmienia przebieg treningu.

**Zakres pracy:**

- **Kod:** w sekcji 2 `forward(X, W1, b1, W2, b2)`, która zwraca `Z1`, `A1` i `Z2`; w sekcji 3
  `backward(X, Y, Z1, A1, Z2, W2)`, która zwraca `(dW1, db1, dW2, db2)` o kształtach parametrów, z
  pochodną tanh i sumowaniem gradientów biasów po batchu; w sekcji 4 `gradient_check`, która buduje
  ten sam przebieg w PyTorch z `requires_grad=True` i zwraca maksymalną różnicę dla każdej z
  czterech tablic; w sekcji 5 `train(X, Y, hidden_size, lr, epochs)` z ręczną aktualizacją
  `W -= lr * dW`, bez `torch.optim`.
- **Eksperymenty:** gotowe komórki trenują sieć z 16 neuronami (`lr=0.05`, 3000 epok) i porównują
  stratę końcową z modelem bazowym, który przewiduje średnią. W sekcji 7 gotowy kod trenuje tę samą
  sieć z celowo błędną funkcją `backward_buggy`.
- **Analizy:** w sekcji 6 opisujesz w 3–5 zdaniach kształt i tempo spadku straty oraz jakość
  dopasowania w całym zakresie `x`. W sekcji 7 wskazujesz w 3–5 zdaniach brakujący element wzoru,
  odwołujesz się do wzoru z wykładu i wyjaśniasz, dlaczego błąd zmienia przebieg straty, ale nie
  powoduje błędu wykonania.

**Rezultat:** notebook wykonany do końca, z przechodzącą weryfikacją gradientu, krzywymi straty obu
wersji i uzasadnionymi analizami.

**Sprawdź się:** gotowa asercja w sekcji 4 przerywa notebook, gdy maksymalna różnica między Twoimi
gradientami a PyTorch przekracza `1e-8`. Instrukcja oczekuje różnic rzędu `1e-10` lub mniejszych i
każe zacząć trening dopiero po przejściu tej kontroli. Asercja porównuje gradienty dla jednego
zestawu wag startowych, a działanie `train` sprawdzisz po stracie końcowej, która powinna być
wyraźnie niższa niż strata modelu bazowego. Pozostałe elementy porównaj z sekcją „Kryteria oceny” w
instrukcji.

### Eksperymentalne porównanie strategii optymalizacji {#lab-04}

Dane regresyjne mają trzy cechy o celowo różnych skalach. Pierwsza należy do przedziału [−1, 1],
druga do [−40, 40], a trzecia do [−3, 3]. Zbiór jest podzielony na część treningową, walidacyjną i
testową w proporcji 70/15/15.

**Cel:** porównać SGD, momentum i Adama w kontrolowanym eksperymencie i wyjaśnić, dlaczego przy tych
danych SGD i momentum są wrażliwe na wybór learning rate, a Adam znacznie mniej.

**Zakres pracy:**

- **Kod:** w sekcji 2
  `train_model(opt_name, lr, epochs, batch_size, model_seed, data_seed, momentum)`. Funkcja tworzy
  model przez `make_model` i wybiera `torch.optim.SGD` z momentum albo bez niego lub
  `torch.optim.Adam`. Adama nie implementujesz od zera. Trening korzysta z mini-batchy z
  `iterate_minibatches` w kolejności `zero_grad() → forward → strata (MSE) → backward() → step()`, a
  straty treningowa i walidacyjna są liczone po każdej epoce w `torch.no_grad()`. Funkcja zwraca
  `(model, train_losses, val_losses)`.
- **Eksperymenty:** w sekcji 3 uruchamiasz `"sgd"`, `"momentum"` (`momentum=0.9`) i `"adam"` z
  `lr=0.01` i `epochs=20` i rysujesz krzywe strat na wspólnym wykresie. W sekcji 4 przeglądasz
  learning rate: dla SGD `[0.0001, 0.001, 0.01]`, dla momentum `[0.00005, 0.0005, 0.005]`, po 20
  epok, i zestawiasz końcowe straty walidacyjne. W sekcji 6 wybierasz po jednym `lr` dla każdego
  optymalizatora na podstawie straty walidacyjnej z sekcji 4 (dla Adama notebook dopuszcza `lr=0.01`
  z sekcji 3), trenujesz każdą konfigurację przez 25 epok i dopiero wtedy oceniasz wszystkie trzy na
  zbiorze testowym, dokładnie raz.
- **Analizy:** w sekcji 5 diagnoza w 4–6 zdaniach, która łączy wyniki przeglądu ze skalami cech i
  krzywizną funkcji straty. Samo stwierdzenie, że learning rate był za duży, nie wystarcza. W sekcji
  7 odpowiadasz na dwa pytania, odwołując się do wartości z sekcji 6.
- **Rozszerzenie opcjonalne:** dodatkowe wartości w przeglądzie `lr` albo `momentum` inne niż 0,9.

**Rezultat:** notebook wykonany do końca, z wykresem porównania, tabelą przeglądu, tabelą wyników
testowych (optymalizator, wybrany `lr`, strata testowa), diagnozą i wnioskami.

**Sprawdź się:** notebook nie ma gotowych asercji. Instrukcja zapowiada, że przy `lr=0.01` co
najmniej jeden optymalizator poza Adamem prawdopodobnie nie nauczy się niczego sensownego, a jego
strata może osiągnąć `nan`. Taki wynik jest materiałem do diagnozy w sekcji 5. Po sekcji 3
instrukcja radzi sprawdzić, czy każdy optymalizator nauczył się czegokolwiek użytecznego. Punktem
odniesienia jest gotowy model bazowy, który przewiduje średnią ze zbioru treningowego. Instrukcja
przeznacza zbiór testowy na jednokrotną ocenę wybranych konfiguracji w sekcji 6. Gotowa komórka z
modelem bazowym w sekcji 2 wypisuje też jego stratę testową (`baseline_test`). Pozostałe elementy
porównaj z sekcją „Kryteria oceny” w instrukcji.

### Rozpoznawanie przeuczenia i dobór regularyzacji {#lab-05}

Dane do klasyfikacji mają 14 cech: 4 niosą informację o klasie, a 10 to czysty szum. Dwie cechy mają
znacznie większą skalę niż pozostałe. Zbiór treningowy liczy 100 przykładów, a walidacyjny i testowy
po 200.

**Cel:** rozpoznać przeciek danych w normalizacji, zdiagnozować przeuczenie na podstawie krzywych
uczenia i porównać weight decay, dropout i early stopping w kontrolowanym eksperymencie.

**Zakres pracy:**

- **Przeciek danych (sekcja 1):** gotowy, celowo błędny kod liczy statystyki normalizacji na całym
  zbiorze przed podziałem. Diagnozę piszesz w 3–5 zdaniach. Potem uzupełniasz `normalize_correctly`,
  która liczy statystyki wyłącznie na `X_train_raw` i stosuje je do wszystkich trzech zbiorów.
  Gotowy kod porównuje błędne i poprawne statystyki pierwszej cechy oraz wyniki modeli trenowanych
  na obu wersjach danych.
- **Pętla treningowa (sekcja 3):**
  `train_model(model, epochs, lr, weight_decay=0.0, use_adamw=False)` z całym zbiorem treningowym w
  jednym batchu, `BCEWithLogitsLoss` i przełączaniem `model.train()` i `model.eval()`. Funkcja
  zwraca `(train_losses, val_losses)`. Po treningu modelu `[32,32]` bez regularyzacji przez 1000
  epok interpretujesz wykres w 3–5 zdaniach: podajesz dokładność treningową i walidacyjną oraz
  kształt krzywych, który świadczy o przeuczeniu.
- **Regularyzacja (sekcje 4 i 5):** porównujesz AdamW z `weight_decay` 0.0, 0.01, 0.1 i 0.3 oraz
  dropout z `p` 0.0, 0.2, 0.4 i 0.6, zbierając dokładność i stratę walidacyjną każdej konfiguracji.
  W `train_with_early_stopping` dopisujesz zapamiętywanie i przywracanie najlepszego stanu modelu.
- **Wybór i test (sekcja 6):** wybierasz jedną konfigurację o najniższej stracie walidacyjnej i
  oceniasz ją na zbiorze testowym, podając dokładność i stratę. Instrukcja mówi o ponownym treningu
  wybranej konfiguracji z tym samym ziarnem, a komentarz `TODO` w notebooku o użyciu modelu już
  wytrenowanego wcześniej, żeby inna losowość nie zmieniła wyniku.
- **Wnioski (sekcja 7):** trzy pytania. Odpowiedzi odwołują się do wartości z sekcji 4–6.
- **Rozszerzenie opcjonalne:** dodatkowe wartości `weight_decay` i `p` albo połączenie dropout z
  weight decay.

**Rezultat:** notebook wykonany do końca, z diagnozą przecieku, poprawną normalizacją, interpretacją
krzywych, tabelami regularyzacji, działającym early stopping, wynikiem testowym wybranej
konfiguracji i wnioskami.

**Sprawdź się:** gotowa asercja w sekcji 5 sprawdza, czy strata walidacyjna modelu po wyjściu z
`train_with_early_stopping` jest równa najlepszej zapamiętanej stracie. Kryteria oceny wymagają,
żeby ta asercja nie była pominięta ani usunięta. Komentarz `TODO` w sekcji 6 wskazuje tę sekcję jako
jedyne miejsce, w którym Ty używasz `X_test`. Gotowa komórka „Wpływ przecieku na wynik” z sekcji 1
też ocenia małe modele na zbiorze testowym. Pozostałe elementy porównaj z sekcją „Kryteria oceny” w
instrukcji.

## Oczekiwane rezultaty

- Pięć notebooków laboratoriów 01–05 wykonanych od początku do końca bez błędu, z Twoim kodem w
  miejscach oznaczonych `TODO`.
- W każdym notebooku tabele i wykresy z Twojego przebiegu oraz odpowiedzi w komórkach Markdown,
  które odwołują się do otrzymanych wartości.

## Wskazówki

- Jeśli zmienisz funkcję zdefiniowaną wcześniej, uruchom ponownie jej komórkę i komórki, które z
  niej korzystają. Notebook pamięta stan z poprzednich uruchomień.
- Notebooki i instrukcje po angielsku (`lab.en.ipynb`, `README.md`) mają tę samą strukturę. Możesz z
  nich korzystać, jeśli wolisz pracować po angielsku.
- Kolejny [zestaw 2, „Widzenie komputerowe i
  reprezentacje”](computer-vision-and-representations.md), obejmuje laboratoria 06–08.
