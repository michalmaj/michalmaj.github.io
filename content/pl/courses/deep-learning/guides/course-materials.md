---
title: "Materiały przedmiotu"
summary: "Piętnaście wykładów z notebookami i piętnaście laboratoriów, po polsku i po angielsku. Materiały są nadal rozwijane i mogą się zmieniać."
status: published
order: 1
materials:
  - repository: deep-learning
    path: README.pl.md
    lang: pl
    label: "Opis kursu, konfiguracja i sposób pracy: od niego zaczynasz"
  - repository: deep-learning
    path: README.md
    lang: en
    label: "Opis kursu w wersji angielskiej"
  - repository: deep-learning
    path: lectures/01_intro/lecture.md
    lang: pl
    label: "Pierwszy wykład: Deep Learning, ML vs DL, tensory i podstawowy proces trenowania modelu"
  - repository: deep-learning
    path: labs/01_intro/README.pl.md
    lang: pl
    label: "Pierwsze laboratorium: podstawy PyTorch, tensory, urządzenia i pierwszy model"
---
**Status:** materiały są nadal rozwijane i mogą się zmieniać. Repozytorium ma wydanie `v1.0.0`, ale
po nim treści są dalej poprawiane i przepisywane. Linki na tej stronie prowadzą do aktualnej wersji,
na gałęzi `main`.

## Jak korzystać z repozytorium

- **Od czego zacząć:** opis kursu proponuje trzy kroki: przeczytać pierwszy wykład, uruchomić jego
  notebook z przykładami, a potem wykonać pierwsze laboratorium.
- **Uruchamianie notebooków:** sekcja „Konfiguracja” w opisie kursu pokazuje, jak zainstalować
  zależności (Python 3.12 i uv) i otworzyć notebooki w JupyterLab. Do wszystkich eksperymentów
  wystarcza procesor (CPU); karta graficzna (GPU) tylko przyspiesza obliczenia. Część późniejszych
  modułów pobiera przy pierwszym uruchomieniu zbiór danych albo wytrenowany model.
- **Rytm pracy:** do każdego tematu są notatki wykładu, notebook wykładowy z eksperymentami i
  laboratorium. Opis kursu proponuje przechodzić je w tej kolejności.

## Wykłady

Każdy wykład ma notatki i notebook z przykładami, w obu językach. Oba pliki są w katalogu wykładu:
notatki to `lecture.md` (po polsku) i `lecture.en.md` (po angielsku), a notebook to `examples.ipynb`
(po polsku) i `examples.en.ipynb` (po angielsku).

| Nr | Wykład (po polsku) | English |
|---|---|---|
| 01 | [Deep Learning, ML vs DL, tensory i podstawowy proces trenowania modelu](https://github.com/michalmaj/deep-learning/blob/main/lectures/01_intro/lecture.md) | [Lecture 01](https://github.com/michalmaj/deep-learning/blob/main/lectures/01_intro/lecture.en.md) |
| 02 | [Perceptron, sieci wielowarstwowe (MLP) i funkcje aktywacji](https://github.com/michalmaj/deep-learning/blob/main/lectures/02_mlp/lecture.md) | [Lecture 02](https://github.com/michalmaj/deep-learning/blob/main/lectures/02_mlp/lecture.en.md) |
| 03 | [Backpropagation, reguła łańcuchowa i automatyczne różniczkowanie](https://github.com/michalmaj/deep-learning/blob/main/lectures/03_backprop/lecture.md) | [Lecture 03](https://github.com/michalmaj/deep-learning/blob/main/lectures/03_backprop/lecture.en.md) |
| 04 | [Gradient descent, SGD, momentum i Adam](https://github.com/michalmaj/deep-learning/blob/main/lectures/04_optimization/lecture.md) | [Lecture 04](https://github.com/michalmaj/deep-learning/blob/main/lectures/04_optimization/lecture.en.md) |
| 05 | [Generalizacja, overfitting i regularyzacja](https://github.com/michalmaj/deep-learning/blob/main/lectures/05_generalization/lecture.md) | [Lecture 05](https://github.com/michalmaj/deep-learning/blob/main/lectures/05_generalization/lecture.en.md) |
| 06 | [Od pikseli do cech w konwolucyjnych sieciach neuronowych](https://github.com/michalmaj/deep-learning/blob/main/lectures/06_cnn/lecture.md) | [Lecture 06](https://github.com/michalmaj/deep-learning/blob/main/lectures/06_cnn/lecture.en.md) |
| 07 | [Transfer learning i ponowne wykorzystanie reprezentacji](https://github.com/michalmaj/deep-learning/blob/main/lectures/07_transfer_learning/lecture.md) | [Lecture 07](https://github.com/michalmaj/deep-learning/blob/main/lectures/07_transfer_learning/lecture.en.md) |
| 08 | [Embeddingi i geometria przestrzeni cech](https://github.com/michalmaj/deep-learning/blob/main/lectures/08_embeddings/lecture.md) | [Lecture 08](https://github.com/michalmaj/deep-learning/blob/main/lectures/08_embeddings/lecture.en.md) |
| 09 | [Modelowanie sekwencji za pomocą RNN, LSTM i GRU](https://github.com/michalmaj/deep-learning/blob/main/lectures/09_rnn/lecture.md) | [Lecture 09](https://github.com/michalmaj/deep-learning/blob/main/lectures/09_rnn/lecture.en.md) |
| 10 | [Attention i architektura Transformer](https://github.com/michalmaj/deep-learning/blob/main/lectures/10_attention/lecture.md) | [Lecture 10](https://github.com/michalmaj/deep-learning/blob/main/lectures/10_attention/lecture.en.md) |
| 11 | [Od Transformera do systemu generowania tekstu](https://github.com/michalmaj/deep-learning/blob/main/lectures/11_llm_engineering/lecture.md) | [Lecture 11](https://github.com/michalmaj/deep-learning/blob/main/lectures/11_llm_engineering/lecture.en.md) |
| 12 | [Autoenkodery, VAE i przestrzeń latentna](https://github.com/michalmaj/deep-learning/blob/main/lectures/12_autoencoders/lecture.md) | [Lecture 12](https://github.com/michalmaj/deep-learning/blob/main/lectures/12_autoencoders/lecture.en.md) |
| 13 | [Modele dyfuzyjne: uczenie generowania przez odszumianie](https://github.com/michalmaj/deep-learning/blob/main/lectures/13_diffusion/lecture.md) | [Lecture 13](https://github.com/michalmaj/deep-learning/blob/main/lectures/13_diffusion/lecture.en.md) |
| 14 | [Jak oceniać i interpretować modele, którym chcemy zaufać?](https://github.com/michalmaj/deep-learning/blob/main/lectures/14_evaluation_interpretability/lecture.md) | [Lecture 14](https://github.com/michalmaj/deep-learning/blob/main/lectures/14_evaluation_interpretability/lecture.en.md) |
| 15 | [Od modelu w notebooku do systemu, który można obserwować i utrzymywać](https://github.com/michalmaj/deep-learning/blob/main/lectures/15_production/lecture.md) | [Lecture 15](https://github.com/michalmaj/deep-learning/blob/main/lectures/15_production/lecture.en.md) |

## Laboratoria

Każde laboratorium ma instrukcję i notebook do uzupełnienia, w obu językach. Uwaga na nazwy plików:
instrukcja po polsku to `README.pl.md`, a `README.md` jest po angielsku. Notebook to `lab.ipynb` (po
polsku) i `lab.en.ipynb` (po angielsku). Notebooki mają gotowy szkielet, a zadania są oznaczone jako
`TODO`. Repozytorium nie zawiera rozwiązań laboratoriów.

| Nr | Laboratorium (po polsku) | English |
|---|---|---|
| 01 | [Podstawy PyTorch, tensory, urządzenia i pierwszy model](https://github.com/michalmaj/deep-learning/blob/main/labs/01_intro/README.pl.md) | [Lab 01](https://github.com/michalmaj/deep-learning/blob/main/labs/01_intro/README.md) |
| 02 | [Klasyfikacja danych tabularnych za pomocą MLP](https://github.com/michalmaj/deep-learning/blob/main/labs/02_mlp/README.pl.md) | [Lab 02](https://github.com/michalmaj/deep-learning/blob/main/labs/02_mlp/README.md) |
| 03 | [Backpropagation od podstaw w NumPy](https://github.com/michalmaj/deep-learning/blob/main/labs/03_backprop/README.pl.md) | [Lab 03](https://github.com/michalmaj/deep-learning/blob/main/labs/03_backprop/README.md) |
| 04 | [Eksperymentalne porównanie strategii optymalizacji](https://github.com/michalmaj/deep-learning/blob/main/labs/04_optimization/README.pl.md) | [Lab 04](https://github.com/michalmaj/deep-learning/blob/main/labs/04_optimization/README.md) |
| 05 | [Rozpoznawanie przeuczenia i dobór regularyzacji](https://github.com/michalmaj/deep-learning/blob/main/labs/05_generalization/README.pl.md) | [Lab 05](https://github.com/michalmaj/deep-learning/blob/main/labs/05_generalization/README.md) |
| 06 | [Projektowanie, trenowanie i analiza CNN](https://github.com/michalmaj/deep-learning/blob/main/labs/06_cnn/README.pl.md) | [Lab 06](https://github.com/michalmaj/deep-learning/blob/main/labs/06_cnn/README.md) |
| 07 | [Adaptacja modelu pretrained do nowego zadania](https://github.com/michalmaj/deep-learning/blob/main/labs/07_transfer_learning/README.pl.md) | [Lab 07](https://github.com/michalmaj/deep-learning/blob/main/labs/07_transfer_learning/README.md) |
| 08 | [System wyszukiwania podobnych obrazów](https://github.com/michalmaj/deep-learning/blob/main/labs/08_embeddings/README.pl.md) | [Lab 08](https://github.com/michalmaj/deep-learning/blob/main/labs/08_embeddings/README.md) |
| 09 | [Klasyfikacja wiadomości SMS za pomocą RNN, LSTM i GRU](https://github.com/michalmaj/deep-learning/blob/main/labs/09_rnn/README.pl.md) | [Lab 09](https://github.com/michalmaj/deep-learning/blob/main/labs/09_rnn/README.md) |
| 10 | [Mały Transformer do klasyfikacji sekwencji](https://github.com/michalmaj/deep-learning/blob/main/labs/10_attention/README.pl.md) | [Lab 10](https://github.com/michalmaj/deep-learning/blob/main/labs/10_attention/README.md) |
| 11 | [Pipeline inferencji małego modelu językowego](https://github.com/michalmaj/deep-learning/blob/main/labs/11_llm_engineering/README.pl.md) | [Lab 11](https://github.com/michalmaj/deep-learning/blob/main/labs/11_llm_engineering/README.md) |
| 12 | [Detekcja anomalii za pomocą autoenkodera](https://github.com/michalmaj/deep-learning/blob/main/labs/12_autoencoders/README.pl.md) | [Lab 12](https://github.com/michalmaj/deep-learning/blob/main/labs/12_autoencoders/README.md) |
| 13 | [Samodzielna implementacja i analiza niewielkiego modelu dyfuzyjnego (DDPM)](https://github.com/michalmaj/deep-learning/blob/main/labs/13_diffusion/README.pl.md) | [Lab 13](https://github.com/michalmaj/deep-learning/blob/main/labs/13_diffusion/README.md) |
| 14 | [Audyt błędów i interpretacja decyzji klasyfikatora obrazów](https://github.com/michalmaj/deep-learning/blob/main/labs/14_evaluation_interpretability/README.pl.md) | [Lab 14](https://github.com/michalmaj/deep-learning/blob/main/labs/14_evaluation_interpretability/README.md) |
| 15 | [Lokalna usługa inferencyjna z monitoringiem (EuroSAT + ResNet18)](https://github.com/michalmaj/deep-learning/blob/main/labs/15_production/README.pl.md) | [Lab 15](https://github.com/michalmaj/deep-learning/blob/main/labs/15_production/README.md) |

## Licencje

Kod repozytorium jest na licencji MIT, a oryginalne treści wykładów i laboratoriów — na licencji
CC BY-SA 4.0. To inna licencja niż CC BY 4.0, na której są treści tej strony. Zbiory danych i
materiały zewnętrzne zachowują własne licencje, opisane w repozytorium.
