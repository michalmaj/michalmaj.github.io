---
title: "Wiele paczek"
summary: "Cztery misje modułu 8: Plant z osobnym miejscem dla każdej strefy, przesuwanie kilku paczek w jednym ticku, wyniki pomiarów zapisywane w paczkach i Engine, który prowadzi kilka paczek naraz."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_08_multiple_items/00_wprowadzenie.md
    lang: pl
    label: "Moduł 8 — wprowadzenie: co się zmienia i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-08-start
    lang: pl
    label: "Kod startowy modułu 8 (tag module-08-start)"
tasks:
  misja-29:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_08_multiple_items/01_partie_i_paczki.md
        lang: pl
        label: "Instrukcja: Misja 29 — Model wielu paczek"
  misja-30:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_08_multiple_items/02_przesuwanie_partii.md
        lang: pl
        label: "Instrukcja: Misja 30 — Przesuwanie paczek"
  misja-31:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_08_multiple_items/03_korelacja_per_paczka.md
        lang: pl
        label: "Instrukcja: Misja 31 — Powiązanie odczytów z paczkami"
  misja-32:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_08_multiple_items/04_silnik_z_wieloma_paczkami.md
        lang: pl
        label: "Instrukcja: Misja 32 — Engine z wieloma paczkami"
---
W tym zestawie na linii może być jednocześnie kilka paczek. `Plant` dostaje osobne pole dla każdej
strefy, a każda paczka przechowuje własny stan przetwarzania, więc wyniki pomiarów nie mieszają się
między paczkami. Cztery zadania to misje 29–32 modułu 8 (w instrukcjach oznaczone też jako 8.1–8.4):
testy misji N mają etykietę `misja-N`.

## Przygotowanie do zestawu

**Po module 7.** Zestaw kontynuuje [zestaw 7](fault-mode.md). Środowisko z modułu 0 już działa.

**Punkt startowy: tag `module-08-start`.** Tak jak w poprzednich modułach zaczynasz od tagu
startowego, a nie od własnej gałęzi z modułu 7. Tym razem tag nie jest jednak prostym przedłużeniem
modułu 7: zmienia `Item`, `Plant`, `TickResult` i `Engine` tak, żeby na linii mogło być kilka paczek.
Wprowadzenie do modułu wyjaśnia, dlaczego tego modułu nie da się budować przyrostowo jak
poprzednich. Elementy zależne od starego modelu są w tagu szkieletami do uzupełnienia, a pozostałe,
na przykład `Diverter`, `BeltMotor`, `Mode` i zatrzask przycisku awaryjnego, działają bez zmian. Plan
pracy studenta podaje polecenia:

```bash
git fetch --tags
git switch -c my-work module-08-start
```

Jeśli gałąź `my-work` już istnieje, nadaj nowej gałęzi inną nazwę.

**Stan na starcie.** Kod startowy kompiluje się, ale `Engine::step()` nie przesuwa paczek;
wprowadzenie mówi, że to zamierzone. Błąd zgłaszają nie tylko testy misji 29–32. Wcześniejsze
testy, które moduł 8 przepisał na nowy model, mają dwie etykiety, np. test misji 3 ma też etykietę
`misja-29`. Na starcie zgłaszają więc błąd także `misja-3`, `misja-9`–`misja-11`, `misja-15`,
`misja-19`–`misja-21`, `misja-24`, `misja-26` i `misja-28`. Każdy z tych testów zaczyna przechodzić
razem z testami misji, której etykietę też nosi. Testów `misja-2` i `misja-23` w tym kodzie już nie
ma. Program `simulator_cli` na starcie wypisuje tylko informację, że demonstracja z misji 32 jest
jeszcze do zrobienia.

**Dokumentacja na `main`, kod na tagu.** Instrukcji modułu 8 nie ma w tagu `module-08-start`:
czytasz je na gałęzi `main`. Odnośniki do kodu w instrukcjach otwierają pliki z tagu na GitHubie, a
u siebie edytujesz plik pod tą samą ścieżką. Nie zmieniasz plików `CMakeLists.txt` ani testów. Typy
`Item`, `Plant`, `TickResult`, `SensorSnapshot` i `Engine` mają już docelowe definicje.
`Engine::step()` uzupełniasz dopiero w ostatniej misji.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 8 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#8-wiele-paczek-i-niezmienniki).

## Zadania

### Misja 29: Model wielu paczek {#misja-29}

**Cel:** poznać model, w którym każda strefa `Plant` ma własne pole, i dodawać do niego paczki o
niepowtarzalnych identyfikatorach.

**Zakres pracy:** nowe definicje `Item` i `Plant` są gotowe. W pliku `src/plant.cpp` uzupełnij
`spawnItem()` według wymagań z instrukcji: funkcja odrzuca paczkę, gdy `infeed` jest zajęty albo gdy
ten sam identyfikator ma już paczka w `presenceCheck`, `weighing` lub `diverting`, a w pozostałych
przypadkach tworzy nową paczkę w `infeed`. Funkcja `advance()` zostaje na razie pusta.

**Rezultat:** `spawnItem()` zwraca `true` albo `false` i przy odrzuceniu nie zmienia `Plant`.
Ponowienie nieudanej próby należy do wywołującego, nie do `Plant`.

**Sprawdź się:** `ctest --preset test -L misja-29`. Oczekiwany wynik:
`100% tests passed, 0 tests failed out of 1`. Powtórzony identyfikator test sprawdza tylko dla
paczki w `presenceCheck`. Wymaganie dla `weighing` i `diverting` porównaj z instrukcją, czytając
własny kod.

### Misja 30: Przesuwanie paczek {#misja-30}

**Cel:** przesunąć w jednym wywołaniu `advance()` każdą paczkę najwyżej o jedną strefę, tak żeby
następna paczka mogła od razu wejść do strefy zwolnionej w tym samym ticku.

**Zakres pracy:** typy `ItemDeparture` i `AdvanceResult` są gotowe. W pliku `src/plant.cpp`
zaimplementuj `advance()`: cztery przejścia w kolejności od wyjścia do wejścia, każde dokładnie raz.
W strefie `diverting` obowiązuje reguła limitu czasu z misji 26, ale licznik `divertingWaitTicks`
jest teraz polem paczki, a odjazd paczki opisuje `departure`. Pozostałe przejścia uwzględniają
bieżącą zajętość stref. Szczegółowe reguły i przykładowy przebieg trzech paczek podaje instrukcja.

**Rezultat:** w jednym ticku może przesunąć się kilka paczek, każda o jedną strefę. Paczka, która
opuszcza linię, znika z `Plant`, a `advance()` zwraca jej odjazd albo zdarzenie, nigdy oba naraz.

**Sprawdź się:** `ctest --preset test -L misja-30` uruchamia dwa testy, które mają też etykiety
`misja-9` i `misja-26`: przejście paczki przez cztery strefy przy spóźnionym poleceniu dywertera oraz
licznik `divertingWaitTicks`. Oba prowadzą pojedynczą paczkę. Tego, że kilka paczek przesuwa się w
jednym ticku, nie sprawdza żaden test: implementacja, w której paczka nie wchodzi do strefy
zwolnionej w tym samym ticku, przechodzi także testy misji 32. Sprawdzisz to w misji 32 w przebiegu
programu, a wcześniej porównaj swój kod z regułą i przykładowym przebiegiem z instrukcji.

### Misja 31: Powiązanie odczytów z paczkami {#misja-31}

**Cel:** zapisywać wyniki pomiarów w paczce, której dotyczą, zamiast we wspólnym `ControllerState`.

**Zakres pracy:** deklaracje są gotowe. W pliku `src/controller.cpp` uzupełnij
`updatePresenceConfirmation()` i `updateClassification()` według reguł z instrukcji. W plikach
`src/presence_sensor.cpp` i `src/weight_sensor.cpp` czujnik ustala stan rzeczywisty z pola strefy,
które dostaje (`item.has_value()`, a dla masy także `item->mass`). Instrukcja każe pozostawić resztę
logiki z modułu 6 bez zmian, ale w kodzie startowym obie metody `read()` są szkieletami, które zawsze
zwracają `Missing`. Regułę z modułu 6 trzeba więc wpisać ponownie, na przykład przenosząc ją z
własnej gałęzi z poprzedniego modułu. Komentarz `// TODO` w każdym z tych plików ją streszcza.

**Rezultat:** każda paczka ma własne potwierdzenie obecności i własną klasyfikację. Klasyfikacja
powstaje tylko z wiarygodnego pomiaru i po potwierdzeniu obecności tej samej paczki, a odczyt pustej
strefy bez usterki nie zmienia wartości zapamiętanej przez czujnik.

**Sprawdź się:** `ctest --preset test -L misja-31` uruchamia trzy testy: obie nowe funkcje na
osobnych paczkach, w tym dwie paczki sklasyfikowane niezależnie w tym samym ticku, oraz oba czujniki.
Testy czujników mają też etykiety `misja-20` i `misja-21` i sprawdzają, że odczyt pustej strefy nie
nadpisuje zapamiętanej wartości.

### Misja 32: `Engine` z wieloma paczkami {#misja-32}

**Cel:** połączyć nowy `Plant`, `advance()` i funkcje z misji 31 w `Engine::step()` tak, żeby kilka
paczek przechodziło przez linię jednocześnie, każda z własną klasyfikacją.

**Zakres pracy:** misja korzysta z wyników misji 29–31 oraz z modułów 6 i 7. W kodzie startowym
`Engine::step()` jest tymczasowym szkieletem: zachowuje flagi wejściowe, `latch_`, `decision`,
`modeForTick` i sterowanie taśmą, ale nie odczytuje czujników, nie steruje dywerterem i nie wywołuje
`advance()`. W pliku `src/engine.cpp` uzupełnij `step()` w kolejności z instrukcji:

- odczyty obu czujników i zapisanie wyników w paczkach, ale tylko w zajętych strefach;
- polecenie dywertera i `routingReady` wyznaczone jednym warunkiem, wyłącznie z paczki w
  `plant_.diverting`;
- `advance()` przed wyznaczeniem końcowego trybu;
- `TickResult` ze wszystkimi czterema strefami, `event`, `departure` i identyfikatorami paczek w
  `SensorSnapshot`.

Sterowanie dywerterem z modułu 7, w tym przekazanie usterki do `diverter_.resolve()`, trzeba przy tym
przywrócić: w szkielecie go nie ma. Komentarz `// TODO` w `src/engine.cpp` wymienia też pole
`diverterCommandItemId`, które `describe()` wypisuje po `@`. W pliku `src/tick_result.cpp`
zaimplementuj `describe()` w formacie z instrukcji; dokładne przykłady są w
`tests/tick_result_test.cpp`. W pliku `apps/simulator_cli/main.cpp` przygotuj demonstrację co
najmniej trzech paczek o różnych klasyfikacjach, z tickiem, w którym jedna paczka odjeżdża, a
następna wchodzi do zwolnionej strefy.

**Rezultat:** trzy paczki o masach 100 g, 800 g i 150 g odjeżdżają w kolejności dodania do wyjść
Light, Heavy i Light. Program wypisuje każdy tick przez `describe()`.

**Sprawdź się:** `ctest --preset test -L misja-32` uruchamia siedem testów: `describe()`, testy
`Engine` z modułów 3–7 przepisane na nowy model (mają też etykiety `misja-10`, `misja-11`,
`misja-15`, `misja-19`, `misja-24` i `misja-28`) oraz nowy test trzech paczek. Testy nie sprawdzają
identyfikatorów paczek, które `Engine` zapisuje w wyniku ticku (`presenceObservedItemId`,
`weightObservedItemId` i `diverterCommandItemId`). Implementacja bez nich, a także taka, która
przypisuje paczce odczyt `Stale`, przechodzi wszystkie testy. `describe()` wypisuje tylko ostatni z
tych identyfikatorów, więc dwa pierwsze porównaj z regułą z instrukcji, czytając własny kod.

Przebiegu w `main()` nie sprawdza żaden test: pełny `ctest --preset test` przechodzi w całości, zanim
zmienisz `main()`. Zbuduj i uruchom program poleceniami z instrukcji (`cmake --build --preset dev`, a
potem `./build/dev/apps/simulator_cli/simulator_cli`; wariant dla Windows podaje instrukcja misji 6).
W wypisanych tickach sprawdź odjazdy do wyjść Light, Heavy i Light oraz tick, w którym jedna paczka
odjeżdża, a następna wchodzi do zwolnionej strefy. Instrukcja misji 30 zaznacza, że w pełnej
symulacji numery ticków są inne niż w jej przykładzie, bo taśma najpierw się rozpędza, ale kolejność
zdarzeń jest taka sama. Na koniec modułu uruchom `ctest --preset test`: według instrukcji przechodzą
testy `misja-1`, `misja-3`–`misja-4`, `misja-6`–`misja-22` oraz `misja-24`–`misja-32`.

## Oczekiwane rezultaty

- Testy `misja-29`…`misja-32` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy się
  wynikiem `100% tests passed`.
- `simulator_cli` pokazuje kilka paczek w różnych strefach naraz, ich odjazdy do właściwych wyjść i
  tick, w którym kilka paczek przesuwa się jednocześnie.
- Twoja praca jest zapisana w commitach na własnej gałęzi utworzonej z `module-08-start`.

## Wskazówki

- Polecenie dywertera zawsze dotyczy paczki, która już jest w `diverting`, a nie paczki właśnie
  sklasyfikowanej w `weighing`. Instrukcje misji 30 i 32 wyjaśniają dlaczego.
- `spawnItem()` nie ma własnej kolejki. Po nieudanej próbie to wywołujący, na przykład program w
  `main()`, ponawia dodanie paczki w kolejnym ticku.
- Kod startowy zamienia na tekst tylko strefę (`psm::toString`). Pozostałe wartości wyliczeniowe dla
  `describe()` trzeba zamienić na tekst we własnym kodzie; komentarz `// TODO` w
  `src/tick_result.cpp` podaje wymagane napisy. Miejsce docelowe zapisujesz jako `Light` albo
  `Heavy`, a nie pełną nazwą wartości `Zone`.
- Na linii jest kilka paczek, ale program nadal działa w jednym wątku. Plan pracy studenta podkreśla,
  że symulator pozostaje sekwencyjny i powtarzalny.
- Każda misja kończy się sekcją „Częste błędy” i pytaniem do zastanowienia. Zajrzyj do nich, zanim
  poprosisz o pomoc.
- Zapisuj pracę w commitach po każdym sensownym etapie. Tak radzi plan pracy studenta.
