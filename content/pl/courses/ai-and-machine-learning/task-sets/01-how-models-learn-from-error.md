---
title: "Jak modele uczą się z błędu"
summary: "Pierwsza prowadzona ścieżka nauki w aplikacji Interactive ML Labs (wersja alfa): cztery lekcje, od residuals dopasowanej prostej, przez gradient descent i granicę decyzyjną regresji logistycznej, po boosting. W każdej lekcji wykonujesz dwa zadania w demie."
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
  error-gradient-descent:
    materials:
      - repository: interactive-ml-labs
        path: demos/level_1_fundamentals/01_gradient_descent_playground/THEORY.pl.md
        lang: pl
        label: "Teoria do dema Gradient Descent Playground"
      - repository: interactive-ml-labs
        path: demos/level_1_fundamentals/01_gradient_descent_playground/CHALLENGES.pl.md
        lang: pl
        label: "Zadania do dema Gradient Descent Playground (poza aplikacją)"
  error-logistic-boundary:
    materials:
      - repository: interactive-ml-labs
        path: demos/level_1_fundamentals/03_logistic_regression_boundary_lab/THEORY.pl.md
        lang: pl
        label: "Teoria do dema Logistic Regression Boundary Lab"
      - repository: interactive-ml-labs
        path: demos/level_1_fundamentals/03_logistic_regression_boundary_lab/CHALLENGES.pl.md
        lang: pl
        label: "Zadania do dema Logistic Regression Boundary Lab (poza aplikacją)"
  error-boosting-mistakes:
    materials:
      - repository: interactive-ml-labs
        path: demos/level_2_practical_ml/02_boosting_mistake_lab/THEORY.pl.md
        lang: pl
        label: "Teoria do dema Boosting Mistake Lab"
      - repository: interactive-ml-labs
        path: demos/level_2_practical_ml/02_boosting_mistake_lab/CHALLENGES.pl.md
        lang: pl
        label: "Zadania do dema Boosting Mistake Lab (poza aplikacją)"
---
Ten zestaw prowadzi przez pierwszą ścieżkę nauki aplikacji Interactive ML Labs, „Jak modele uczą
się z błędu”. Mapa kursu w aplikacji pokazuje ją jako krok 1. Ścieżka ma cztery lekcje, a każda
lekcja to jedno zadanie tego zestawu. W lekcji uruchamiasz demo i wykonujesz dwa zadania, które
aplikacja pokazuje na liście „Zadania lekcji”. Nie piszesz kodu. Ta strona nie zastępuje lekcji:
podaje, gdzie je znaleźć, co w nich zrobić i co aplikacja sprawdza. Nazwy ekranów, zadań i
przycisków są tu takie, jak w polskiej wersji aplikacji. Nazwy dem i część pojęć aplikacja zostawia
po angielsku.

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

Aplikacja działa na Twoim komputerze, w osobnym oknie programu (Pygame). Nie jest stroną
internetową. Instrukcja wymaga Pythona 3.12 lub nowszego i narzędzia uv.

1. Pobierz repozytorium i przejdź do jego katalogu, na przykład tak (to pobiera bieżący kod z
   gałęzi `main`):

    ```bash
    git clone https://github.com/michalmaj/interactive-ml-labs.git
    cd interactive-ml-labs
    ```

2. W katalogu głównym repozytorium zainstaluj zależności:

    ```bash
    uv sync
    ```

3. Z tego samego katalogu uruchom aplikację:

    ```bash
    uv run --package interactive-ml-labs-app interactive-ml-labs
    ```

Domyślnie aplikacja otwiera okno 1280×720. Według instrukcji w „Ustawieniach” są tryb
pełnoekranowy, adaptacyjny rozmiar okna i opcje komfortu: większy tekst, wysoki kontrast i paleta
przyjazna daltonizmowi.

Postęp lekcji i ustawienia aplikacja zapisuje w pliku w Twoim profilu użytkownika, a nie w
katalogu repozytorium. Po zamknięciu i ponownym uruchomieniu aplikacji ukończone zadania i lekcje
są nadal oznaczone. Zapis dotyczy tylko tego komputera i tego konta.

## Gdzie znajdziesz ścieżkę

1. Na pierwszym ekranie wybierz „Polski”. Ekran wyboru języka pojawia się przy każdym uruchomieniu.
2. Na ekranie startowym wybierz „Prowadzone ścieżki nauki”. Otworzy się „Mapa kursu”.
3. Wybierz „Krok 1: Jak modele uczą się z błędu”. Zobaczysz listę czterech lekcji. Przy zaznaczonej
   lekcji aplikacja pokazuje jej cel, status, zadania i odznakę do zdobycia.
4. Wybierz lekcję. Ekran intro pokazuje cele dema, listę „Zadania lekcji” i sterowanie. `Enter`
   uruchamia demo, a `T` otwiera teorię.

W menu poruszasz się strzałkami albo myszą, a wybierasz klawiszem `Enter` albo kliknięciem. W demie
`Esc` otwiera pauzę z pozycjami „Wróć”, „Pomoc”, „Teoria”, „Restart”, „Ustawienia”, „Lista dem” i
„Zamknij”, `H` pokazuje pomoc dema, a `T` otwiera teorię. Stopka dem Gradient Descent Playground i Logistic
Regression Boundary Lab podaje „Esc: wyjście”, bo pochodzi z ich samodzielnej wersji. W aplikacji
`Esc` otwiera pauzę.

Aplikacja poleca lekcje w kolejności z listy i przy każdej lekcji podaje „Wymagania”, czyli
poprzednią lekcję. Niczego jednak nie blokuje: każdą lekcję możesz otworzyć od razu.

Lekcje otwieraj przez „Prowadzone ścieżki nauki”. To samo demo uruchomione przez „Przeglądaj dema
według poziomu” działa, ale aplikacja nie zapisuje wtedy postępu lekcji.

Po wykonaniu obu zadań aplikacja sama otwiera ekran „Lekcja ukończona”:

- „Następna lekcja: …” otwiera intro kolejnej lekcji;
- „Powtórz tę lekcję” uruchamia lekcję ponownie;
- „Wróć do ścieżki” wraca do listy lekcji.

Na ostatniej lekcji pierwsza pozycja też nazywa się „Wróć do ścieżki”, ale otwiera ekran „Ścieżka
ukończona” z podsumowaniem i propozycją kolejnej ścieżki. `Esc` na ekranie intro prowadzi do listy
dem poziomu, a nie do ścieżki. Do mapy kursu wrócisz z ekranu startowego. Klawisz `C` na ekranie
startowym otwiera lekcję, którą aplikacja proponuje jako następną.

## Postęp w aplikacji a zrozumienie tematu

Na tej ścieżce trzeba odróżnić trzy rzeczy:

- **Wykonanie działań.** Każde zadanie lekcji mówi, co zrobić w demie i na co patrzeć. Opisy
  zadań niżej streszczają te polecenia.
- **Oznaczenie postępu.** Aplikacja odhacza zadanie (`[x]`) po konkretnej czynności w demie. Zwykle
  wystarczy naciśnięcie klawisza albo zmiana parametru, a w jednym zadaniu spadek loss. Po obu
  zadaniach oznacza lekcję jako ukończoną, przyznaje odznakę i otwiera ekran „Lekcja ukończona”.
  Przy każdej lekcji niżej opisano, jaka czynność odhacza zadanie i czego aplikacja nie sprawdza.
- **Zrozumienie tematu.** Aplikacja nie sprawdza, czy rozumiesz wpływ parametrów na zachowanie
  modelu. Odhaczone zadanie znaczy, że wykonano czynność, a nie że osiągnięto opisany w zadaniu
  efekt. Na przykład zadanie „Zbalansuj residuals” zostaje odhaczone także wtedy, gdy diagnoza w
  demie nadal brzmi „popraw intercept”. Ukończona lekcja nie potwierdza więc opanowania tematu.

Ekran „Lekcja ukończona” zadaje pytanie do przemyślenia („Zatrzymaj się na chwilę”), podpowiada, na
co zwrócić uwagę, i pokazuje „Mini-check”. Notatki dla studentów zaznaczają, że pytania sprawdzające
to „prompty do refleksji, a nie oceniane quizy”. Aplikacja nie zbiera odpowiedzi. Odpowiedz na nie
samodzielnie, a wyjaśnienie porównaj z celem lekcji i z teorią.

Na gałęzi `main` ten ekran ma też „Samoocenę” z przyciskami „Rozumiem” i „Do powtórki”. Ten wybór to
Twoja deklaracja. Aplikacja zapisuje go bez sprawdzania odpowiedzi, a później można go zmienić.
„Raport postępu” na ekranie startowym pokazuje między innymi lekcje oznaczone do powtórki. W wydaniu
v0.0.9a nie ma samooceny ani raportu.

Teorię lekcji aplikacja oznacza jako przeczytaną po otwarciu ekranu teorii. Do ukończenia lekcji
teoria nie jest potrzebna.

## Materiały

Aplikacja ma interfejs po polsku i po angielsku. Notatki dla studentów i instrukcja są po polsku i
po angielsku.

Trzy dema tej ścieżki mają w repozytorium własny katalog: Gradient Descent Playground, Logistic
Regression Boundary Lab i Boosting Mistake Lab. W każdym jest opis dema (`README.md`, po angielsku)
oraz teoria (`THEORY.pl.md`) i rozszerzone zadania z pytaniami kontrolnymi (`CHALLENGES.pl.md`), po
polsku. Linki do teorii i zadań są przy lekcjach.

Pliki z zadaniami opisują samodzielne uruchomienie dema poza aplikacją, poleceniami podanymi w
pliku. W tej wersji demo w aplikacji i poza nią ma to samo sterowanie. Wyjątkiem są `Esc`, `H` i
`T`, które w aplikacji obsługuje sama aplikacja. Zadania z tych plików nie zastępują zadań lekcji, a
aplikacja ich nie odhacza. Lekcja z regresją liniową korzysta z dema wbudowanego w aplikację. Jej
sterowanie opisuje instrukcja.

## Zadania

### Zobacz błąd dopasowanej prostej (Linear Regression Line Fit Lab) {#error-linear-regression-line-fit}

**Cel:** według aplikacji zrozumieć, że model regresji ocenia się po residuals, które zostawia, a
nie po tym, czy prosta wygląda ładnie.

**Zakres pracy:** w demie zmieniasz slope prostej (`Left` / `Right`) i intercept (`Up` / `Down`).
Panel „Odczyt dopasowania” pokazuje MSE loss, najlepszy slope, najlepszy intercept i diagnozę.
Klawisze `1`–`3` zmieniają dataset, a `R` resetuje lab. Zadania lekcji:

- **Zbalansuj residuals:** zmieniaj slope i intercept, aż residuals przestaną wyraźnie uciekać w
  jedną stronę. Wskazówka w aplikacji: patrz, czy błędy są systematycznie nad albo pod prostą.
- **Porównaj z least squares:** klawisz `F` ustawia prostą least squares. Wskaż, który ręcznie
  ustawiony parametr był dalej od optimum. `F` zastępuje ręczne ustawienia, więc porównaj je
  wcześniej albo skorzystaj z wartości najlepszego slope i intercept, które panel pokazuje cały
  czas.

Sterowanie opisuje
[instrukcja, sekcja „Natywne laby Level 1”](https://github.com/michalmaj/interactive-ml-labs/blob/main/USAGE.pl.md#natywne-laby-level-1).
Teoria lekcji (`T`) proponuje też mini-zadania, na przykład wyjaśnienie, dlaczego na zaszumionym
datasecie najlepsza prosta nadal zostawia widoczne residuals. Aplikacja ich nie odhacza.

**Rezultat:** „Zbalansuj residuals” zostaje odhaczone po co najmniej jednej zmianie slope i jednej
zmianie intercept. Aplikacja nie sprawdza wtedy residuals ani diagnozy. „Porównaj z least squares”
zostaje odhaczone po naciśnięciu `F`.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Jaki wzór residuals pokazał Ci, że prosta nadal
jest przesunięta, i który parametr pomógł to zmniejszyć?”. Mini-check: „Czy umiesz wskazać
residuals, które pokazują, że prosta nadal ma bias?”.

### Pozwól algorytmowi zmniejszać loss (Gradient Descent Playground) {#error-gradient-descent}

**Cel:** według aplikacji zrozumieć, jak gradient descent przez małe, powtarzane zmiany parametrów
zmniejsza loss.

**Zakres pracy:** demo uczy prostą regresji metodą gradient descent. Panel pokazuje krok, loss,
weight, bias, learning rate, szum i seed, a obok jest wykres „Historia loss”. Cel dema to loss
najwyżej 1.0 w 80 krokach. `N` wykonuje jeden krok, a `Space` uruchamia i zatrzymuje kroki
automatyczne. `Up` / `Down` zmieniają learning rate, `Left` / `Right` szum, `S` seed, a `R`
resetuje przebieg. Według pliku z zadaniami zmiana learning rate, szumu albo seeda resetuje demo.
Zadania lekcji:

- **Znajdź stabilny learning rate:** zmieniaj learning rate, aż ścieżka będzie iść do minimum bez
  chaotycznego odbijania. Wskazówka w aplikacji: za mały jest wolny, za duży przeskakuje optimum.
- **Zaobserwuj spadek loss:** uruchom kilka kroków i patrz na trend loss, nie tylko na poruszający
  się punkt.

**Rezultat:** „Znajdź stabilny learning rate” zostaje odhaczone po pierwszej zmianie learning
rate, także na wartość, przy której uczenie jest niestabilne. W kontroli zadanie zostało odhaczone
przy learning rate 0.15, przy którym loss po sześciu krokach wzrósł z około 31.8 do 244. „Zaobserwuj
spadek loss” aplikacja sprawdza na historii loss. Zadanie zostaje odhaczone, gdy po co najmniej
dwóch krokach loss jest niższy niż na początku przebiegu. Gdy loss rośnie, zadanie nie zostaje
odhaczone.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Co działo się z loss, gdy learning rate był za
mały albo za duży, i czym różnił się stabilny przebieg?”. Mini-check prosi o wyjaśnienie celu lekcji
własnymi słowami i o wskazanie widocznego sygnału z dema, który go potwierdził. Plik z zadaniami do
dema ma ćwiczenia z learning rate, szumem i seedem, wyzwanie „loss <= 1.0 przed upływem 80 kroków” i
pytania kontrolne.

### Zamień score na decyzję (Logistic Regression Boundary Lab) {#error-logistic-boundary}

**Cel:** według aplikacji zrozumieć, że klasyfikacja używa score, threshold i decision boundary, a
nie tylko jednej etykiety.

**Zakres pracy:** tło dema pokazuje probability dla `class_1`. Panel pokazuje accuracy, precision,
recall, learning rate, threshold i szum oraz confusion matrix (TP, TN, FP, FN). Cel dema to
precision co najmniej 0.80 i recall co najmniej 0.90. `Space` uruchamia i zatrzymuje trening, a `N`
wykonuje jeden krok. `Up` / `Down` zmieniają learning rate, `Q` / `E` threshold, `Left` / `Right`
szum, `S` seed, a `R` resetuje przebieg. Podpowiedź w demie brzmi: „Trenuj model, a potem zmieniaj
threshold, żeby zbalansować FP i FN”. Zadania lekcji:

- **Przesuń decision boundary:** zmień parametry i zobacz, które punkty jako pierwsze zmieniają
  klasę.
- **Porównaj punkty pewne i graniczne:** znajdź punkty daleko od granicy i blisko niej. Wyjaśnij,
  czemu model traktuje je inaczej.

**Rezultat:** „Przesuń decision boundary” zostaje odhaczone po pierwszej zmianie learning rate,
threshold albo szumu. „Porównaj punkty pewne i graniczne” zostaje odhaczone po uruchomieniu
treningu (`Space`) albo po jednym kroku (`N`). Aplikacja nie sprawdza, czy porównano punkty.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Które punkty zmieniły klasę po przesunięciu
decision boundary i dlaczego punkty graniczne były mniej pewne?”. Mini-check prosi o wyjaśnienie
celu lekcji własnymi słowami i o wskazanie sygnału z dema. Plik z zadaniami do dema prowadzi przez
probability i klasę, threshold, confusion matrix, learning rate i szum. Ma też wyzwanie z precision
i recall oraz pytania kontrolne.

### Ucz się z poprzednich błędów (Boosting Mistake Lab) {#error-boosting-mistakes}

**Cel:** według aplikacji zrozumieć, dlaczego boosting kieruje kolejny weak learner na przykłady, z
którymi poprzednie modele radziły sobie słabo.

**Zakres pracy:** demo pokazuje obok siebie weak learner wybranego etapu i cały boosted ensemble.
Panel pokazuje między innymi dataset i preset, etap, szum, train i test accuracy, gap, confidence,
alpha i najlepszą rundę, a pod spodem jest wykres staged accuracy. `Up` / `Down` zmieniają wybrany
etap, a `[` / `]` liczbę rund (lista sterowania w intro podaje do tego `+` / `-`; działają obie
pary). `1`–`4` i `P` przełączają presety, `C` włącza i wyłącza widok confidence, `N` zmienia seed, a
`R` resetuje demo. Zadania lekcji:

- **Przejdź kolejne rundy boosting:** przejdź przez kilka weak learners i obserwuj, które błędy
  dostają więcej uwagi.
- **Połącz wagę z błędem:** znajdź przykład, którego waga zmienia się po błędzie, i wyjaśnij, co
  kolejny learner powinien z nim zrobić.

**Rezultat:** „Przejdź kolejne rundy boosting” zostaje odhaczone po pierwszej zmianie etapu albo
liczby rund. „Połącz wagę z błędem” zostaje odhaczone po naciśnięciu `C`, czyli po włączeniu albo
wyłączeniu widoku confidence. Aplikacja nie sprawdza, czy znaleziono przykład ze zmienioną wagą.

**Sprawdź się:** ekran „Lekcja ukończona” pyta: „Które błędy dostały więcej uwagi w kolejnej
rundzie boosting i jak zmieniło to ensemble?”. Mini-check prosi o wyjaśnienie celu lekcji własnymi
słowami i o wskazanie sygnału z dema. Plik z zadaniami do dema zaczyna od części, w których
uruchamiasz wersję tekstową i liczysz weighted error. Dalsze części dotyczą wizualizacji: etapów,
widoku confidence, presetów, wyzwania i eksportu wyniku. Eksport (`E`) zapisuje plik JSON w katalogu
`exports/` repozytorium, który Git ignoruje. Zadanie końcowe w tym pliku wymienia elementy „Do
oddania”. To część materiału dema, a ta strona nie robi z niej wymagania.

## Oczekiwane rezultaty

- Na liście lekcji wszystkie cztery lekcje mają `[x]`, a mapa kursu pokazuje krok 1 jako
  ukończony. Ekran „Ścieżka ukończona” pokazuje 4/4 lekcje, 8/8 zadań i 4/4 odznaki.
- Na pytania z ekranów „Lekcja ukończona” odpowiadasz własnymi słowami. Aplikacja tych odpowiedzi
  nie sprawdza.

## Wskazówki

- Notatki dla studentów radzą otwierać teorię, kiedy potrzebujesz kontekstu: `T` w demie albo na
  ekranie intro. Teoria lekcji opisuje demo, typowe pułapki, mini-zadania i słowniczek, a `Esc`
  wraca do poprzedniego ekranu.
- Ekran startowy pokazuje „Postęp nauki”: liczbę ukończonych lekcji, zadań i odznak oraz następną
  proponowaną lekcję.
- Kolejna ścieżka w mapie kursu to „Od odległości do klastrów”, opisana w
  [zestawie 2](from-distance-to-clusters.md).
