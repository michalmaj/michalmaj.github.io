---
title: "Od odległości do klastrów"
summary: "Druga prowadzona ścieżka nauki w aplikacji Interactive ML Labs (wersja alfa): pięć lekcji, od wyboru metryki odległości, przez głosowanie k-NN i centroidy K-Means, po DBSCAN i miękkie przypisania w Gaussian Mixture. W każdej lekcji wykonujesz dwa zadania w demie."
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
  distance-knn-vote:
    materials:
      - repository: interactive-ml-labs
        path: demos/level_1_fundamentals/02_knn_vote_map/THEORY.pl.md
        lang: pl
        label: "Teoria do dema k-NN Vote Map"
      - repository: interactive-ml-labs
        path: demos/level_1_fundamentals/02_knn_vote_map/CHALLENGES.pl.md
        lang: pl
        label: "Zadania do dema k-NN Vote Map (poza aplikacją)"
---
Ten zestaw prowadzi przez drugą ścieżkę nauki aplikacji Interactive ML Labs, „Od odległości do
klastrów”. Mapa kursu w aplikacji pokazuje ją jako krok 2, po ścieżce z
[zestawu 1](how-models-learn-from-error.md). Ścieżka ma pięć lekcji, a każda lekcja to jedno
zadanie tego zestawu. W lekcji uruchamiasz demo i wykonujesz dwa zadania, które aplikacja pokazuje
na liście „Zadania lekcji”. Nie piszesz kodu. Ta strona nie zastępuje lekcji: podaje, gdzie je
znaleźć, co w nich zrobić i co aplikacja sprawdza. Nazwy ekranów, zadań i przycisków są tu takie,
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

Postęp zapisany przy ścieżce z zestawu 1 zostaje. Ekran startowy liczy razem lekcje wszystkich
ścieżek.

## Gdzie znajdziesz ścieżkę

1. Na pierwszym ekranie wybierz „Polski”, a na ekranie startowym „Prowadzone ścieżki nauki”.
2. W „Mapie kursu” wybierz „Krok 2: Od odległości do klastrów”. Zobaczysz listę pięciu lekcji.
3. Wybierz lekcję. Na ekranie intro `Enter` uruchamia demo, a `T` otwiera teorię.

Po ukończeniu ścieżki z zestawu 1 ekran startowy proponuje pierwszą lekcję tej ścieżki, a klawisz
`C` od razu ją otwiera. Nawigacja, ekran „Lekcja ukończona” i pauza działają tak samo jak w
zestawie 1. Lekcje otwieraj przez „Prowadzone ścieżki nauki”. To samo demo uruchomione przez
„Przeglądaj dema według poziomu” nie zapisuje postępu lekcji. Każdą lekcję możesz otworzyć od razu,
choć aplikacja poleca kolejność z listy.

## Postęp w aplikacji a zrozumienie tematu

Zasady są te same co w zestawie 1, opisane w części
[„Postęp w aplikacji a zrozumienie tematu”](how-models-learn-from-error.md#postep-w-aplikacji-a-zrozumienie-tematu).
W skrócie:

- **Wykonanie działań.** Każde zadanie lekcji mówi, co zrobić w demie i na co patrzeć.
- **Oznaczenie postępu.** Aplikacja odhacza zadanie (`[x]`) po konkretnej czynności w demie, zwykle
  po naciśnięciu klawisza, zmianie parametru albo kliknięciu. Przy każdej lekcji niżej opisano, jaka
  czynność odhacza zadanie i czego aplikacja nie sprawdza.
- **Zrozumienie tematu.** Aplikacja nie sprawdza obserwacji ani wniosków. Na przykład zadanie
  „Przesuń query point” zostaje odhaczone po pierwszym ruchu punktu, choć polecenie mówi o
  ustawieniu go tak, żeby metryki nie zgadzały się co do nearest neighbor. Ukończona lekcja nie
  potwierdza więc opanowania tematu.

Pytania na ekranie „Lekcja ukończona” służą refleksji i nie są oceniane. Na gałęzi `main` wybór
„Rozumiem” albo „Do powtórki” jest Twoją deklaracją, której aplikacja nie sprawdza.

## Materiały

Aplikacja ma interfejs po polsku i po angielsku. Notatki dla studentów i instrukcja są po polsku i
po angielsku.

Z dem tej ścieżki tylko k-NN Vote Map ma w repozytorium własny katalog. Jest w nim opis dema
(`README.md`, po angielsku) oraz teoria (`THEORY.pl.md`) i rozszerzone zadania z pytaniami
kontrolnymi (`CHALLENGES.pl.md`), po polsku. Plik z zadaniami opisuje samodzielne uruchomienie dema
poza aplikacją. Zadania z niego nie zastępują zadań lekcji, a aplikacja ich nie odhacza. Pozostałe
cztery dema są wbudowane w aplikację. Ich sterowanie opisuje instrukcja, a teorię każdej lekcji
otwierasz klawiszem `T`.

## Zadania

### Ustal, co znaczy blisko (Distance Metrics Lab) {#distance-choose-metric}

**Cel:** według aplikacji zrozumieć, że distance jest decyzją modelarską: różne metryki mogą
wskazywać różnych nearest neighbors.

**Zakres pracy:** demo pokazuje query point i kilka punktów wraz z ich odległościami w bieżącej
metryce. Panel „Odczyt nearest” podaje dataset, metrykę, położenie query point, najbliższy punkt,
jego distance i diagnozę. Strzałki przesuwają query point, `M` zmienia metrykę, `1`–`3` dataset, a
`R` resetuje lab. Zadania lekcji:

- **Przesuń query point:** przesuń query point tak, żeby co najmniej dwie metryki nie zgadzały się
  co do nearest neighbor.
- **Porównaj metryki distance:** przełącz Euclidean, Manhattan i Chebyshev distance i nazwij, co
  każda metryka podkreśla.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 1”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-1).

**Rezultat:** „Przesuń query point” zostaje odhaczone po pierwszym ruchu punktu. Aplikacja nie
sprawdza, czy metryki wskazują różnych sąsiadów. „Porównaj metryki distance” zostaje odhaczone po
pierwszym naciśnięciu `M`, bez przejścia przez wszystkie trzy metryki.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Która metryka zmieniła nearest neighbor i co to
mówi o tym, jak model czyta distance?”. Mini-check prosi o wyjaśnienie celu lekcji własnymi słowami
i o wskazanie widocznego sygnału z dema, który go potwierdził.

### Klasyfikuj przez najbliższe przykłady (k-NN Vote Map) {#distance-knn-vote}

**Cel:** według aplikacji zrozumieć, jak k-NN zamienia distance w lokalne głosowanie i dlaczego k
zmienia gładkość decision map.

**Zakres pracy:** kolorowe tło dema to mapa głosowania: pokazuje, jaką klasę model wybrałby w danym
miejscu. Panel podaje k, liczbę próbek, szum, seed, predykcję i głosy sąsiadów. Cel dema to
accuracy co najmniej 0.90 na osobnym zbiorze testowym. Kliknięcie mapy klasyfikuje wskazany punkt,
`N` losuje punkt do klasyfikacji, `Up` / `Down` zmieniają k, `Left` / `Right` szum, `S` seed, a `R`
resetuje mapę. Według pliku z zadaniami zmiana k, szumu albo seeda resetuje demo. Stopka dema podaje
„Esc: wyjście”, bo pochodzi z jego samodzielnej wersji. W aplikacji `Esc` otwiera pauzę. Zadania
lekcji:

- **Sklasyfikuj query point:** klikaj albo losuj query points i obserwuj, którzy sąsiedzi głosują.
- **Porównaj wartości k:** zmieniaj k i porównuj szumne lokalne granice z gładszymi regionami.

**Rezultat:** „Sklasyfikuj query point” zostaje odhaczone po pierwszym kliknięciu albo po `N`.
Kliknięcie w dowolnym miejscu dema też się liczy, także w panelu obok mapy, gdzie nic nie zostaje
sklasyfikowane. „Porównaj wartości k” zostaje odhaczone po pierwszej zmianie k.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Jak zmiana k wpłynęła na decision map i kiedy
głosowanie było zbyt lokalne albo zbyt wygładzone?”. Mini-check prosi o wyjaśnienie celu lekcji
własnymi słowami i o wskazanie sygnału z dema. Plik z zadaniami do dema ma ćwiczenia z
klasyfikacją punktów, wartością k, szumem, seedem i mapą decyzji, wyzwanie z accuracy na ukrytym
zbiorze testowym i pytania kontrolne.

### Grupuj punkty przez centroidy (K-Means Intro Lab) {#distance-kmeans-centroids}

**Cel:** według aplikacji zrozumieć K-Means jako powtarzane przypisanie do najbliższych centroidów
i przesuwanie centroidów do przypisanych punktów.

**Zakres pracy:** demo pokazuje punkty i centroidy. Panel „Odczyt K-Means” podaje dataset, k,
następny krok, numer iteracji, inertia i rozmiary klastrów. `Space` wykonuje jeden krok (przypisanie
albo aktualizację centroidów), `A` włącza i wyłącza auto-run, `-` / `=` zmieniają k, `1`–`3`
dataset, `C` pokazuje linie punkt–centroid, `N` losuje nową próbkę, a `R` resetuje lab. Zadania
lekcji:

- **Przejdź iteracje K-Means:** przejdź przez fazy assignment i aktualizacji centroidów.
- **Porównaj liczbę klastrów:** zmień k i zauważ, kiedy inertia się poprawia, ale interpretacja
  słabnie.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 1”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-1).

**Rezultat:** „Przejdź iteracje K-Means” zostaje odhaczone po pierwszym kroku wykonanym klawiszem
`Space`. Kroki wykonane przez auto-run (`A`) tego zadania nie odhaczają. „Porównaj liczbę klastrów”
zostaje odhaczone po pierwszym naciśnięciu `-` albo `=`. Aplikacja nie sprawdza, czy porównano
inertia z interpretacją.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Co zmieniało się najpierw: przypisania punktów czy
centroidy, i jak każdy krok zmniejszał błąd klastrowania?”. Mini-check prosi o wyjaśnienie celu
lekcji własnymi słowami i o wskazanie sygnału z dema.

### Dopasuj clustering do kształtu (Clustering Lab) {#distance-clustering-shape}

**Cel:** według aplikacji zrozumieć, dlaczego clustering oparty na centroidach i clustering oparty na
gęstości mogą się różnić, gdy zmienia się kształt danych.

**Zakres pracy:** demo ma dwa tryby, K-Means i DBSCAN, przełączane klawiszem `M`. W trybie K-Means
panel podaje k, iterację i inertia, a w trybie DBSCAN eps, min points, liczbę klastrów i liczbę
punktów noise. `1`–`4` zmieniają preset danych, a `-` / `=` zmieniają k w trybie K-Means albo eps w
trybie DBSCAN. `Space` wykonuje kolejną fazę K-Means albo ponownie uruchamia DBSCAN, `A` włącza
auto-run (K-Means), `C` pokazuje linie punkt–centroid, `N` losuje nową próbkę, a `R` resetuje aktywny
algorytm. Punkt danych można przesunąć myszą. Zadania lekcji:

- **Porównaj K-Means i DBSCAN:** przełącz algorytmy i znajdź dataset, gdzie ich założenia się
  rozmijają.
- **Dostosuj parametry gęstości:** zmień eps albo minimum samples i obserwuj, co staje się noise.
  W tej wersji demo pozwala zmieniać tylko eps. Wartość min points (5) jest wyświetlana, ale nie
  ma do niej sterowania.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 3”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-3).
W aplikacji to demo należy do poziomu 3.

**Rezultat:** „Porównaj K-Means i DBSCAN” zostaje odhaczone po pierwszym przełączeniu trybu (`M`).
„Dostosuj parametry gęstości” zostaje odhaczone po zmianie eps (`-` albo `=` w trybie DBSCAN). Te
same klawisze w trybie K-Means zmieniają k i tego zadania nie odhaczają. Aplikacja nie sprawdza,
czy znaleziono dataset, na którym algorytmy dają różne wyniki.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Gdzie K-Means i DBSCAN dały różne wyniki i które
założenie o kształcie klastrów wywołało tę różnicę?”. Mini-check prosi o wyjaśnienie celu lekcji
własnymi słowami i o wskazanie sygnału z dema.

### Czytaj soft cluster membership (Gaussian Mixture Intro Lab) {#distance-soft-clusters}

**Cel:** według aplikacji zrozumieć, że Gaussian Mixture Models przypisują prawdopodobieństwa, więc
punkt może częściowo należeć do więcej niż jednego klastra.

**Zakres pracy:** panel „Odczyt GMM” podaje dataset, liczbę komponentów, główny komponent, top
responsibility, mixture weight, tryb i diagnozę. Strzałki przesuwają query point, `-` / `=`
zmieniają liczbę komponentów (od 2 do 4), `D` pokazuje i ukrywa density ellipses, `1`–`3`
zmieniają dataset, a `R` resetuje lab. Zadania lekcji:

- **Porównaj soft assignments:** sprawdź punkty przy nakładających się komponentach i porównaj
  probability.
- **Dostosuj liczbę komponentów:** zmień liczbę komponentów i obserwuj, kiedy mixture zaczyna
  overfitować.

Lista sterowania, pomoc i stopka dema podają `H` jako przełącznik hard assignment, a cele dema mówią
o porównaniu soft responsibilities z wymuszoną hard cluster label. W aplikacji, w wydaniu v0.0.9a i
na `main`, klawisz `H` otwiera jednak pomoc aplikacji, a demo zostaje w trybie „soft
responsibilities”. Oba zadania lekcji da się wykonać bez tego przełącznika.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 2”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-2).

**Rezultat:** „Porównaj soft assignments” zostaje odhaczone po pierwszym ruchu query point.
„Dostosuj liczbę komponentów” zostaje odhaczone po pierwszej rzeczywistej zmianie liczby
komponentów. Naciśnięcie `-` przy dwóch albo `=` przy czterech komponentach się nie liczy.
Aplikacja nie sprawdza, czy porównano prawdopodobieństwa ani czy zauważono overfitting.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Który punkt miał mieszaną przynależność i czemu
probability jest tam bardziej użyteczne niż twarda etykieta klastra?”. Mini-check prosi o
wyjaśnienie celu lekcji własnymi słowami i o wskazanie sygnału z dema.

## Oczekiwane rezultaty

- Na liście lekcji wszystkie pięć lekcji ma `[x]`, a mapa kursu pokazuje krok 2 jako ukończony.
  Ekran „Ścieżka ukończona” pokazuje 5/5 lekcji, 10/10 zadań i 5/5 odznak.
- Na pytania z ekranów „Lekcja ukończona” odpowiadasz własnymi słowami. Aplikacja tych odpowiedzi
  nie sprawdza.

## Wskazówki

- Notatki dla studentów radzą otwierać teorię, kiedy potrzebujesz kontekstu: `T` w demie albo na
  ekranie intro. Teoria lekcji ma mini-zadania, których aplikacja nie odhacza. W Clustering Lab
  proponuje na przykład porównanie obu algorytmów na danych w kształcie moons.
- Ekran „Ścieżka ukończona” proponuje jako kolejną ścieżkę „Od dobrych wyników do zaufanych
  modeli”.
