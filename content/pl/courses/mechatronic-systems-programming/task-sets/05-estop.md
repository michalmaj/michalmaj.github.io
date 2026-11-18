---
title: "Awaryjny stop"
summary: "Cztery misje modułu 5: przycisk awaryjny z zatrzaskiem, tryb zatrzymania awaryjnego z bezwzględnym priorytetem, dwie niezależne ścieżki decyzji i ich połączenie w Engine. Uproszczony model dydaktyczny."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_05_estop/00_wprowadzenie.md
    lang: pl
    label: "Moduł 5 — wprowadzenie: skąd startujesz i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-05-start
    lang: pl
    label: "Kod startowy modułu 5 (tag module-05-start)"
tasks:
  misja-16:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_05_estop/01_przycisk_awaryjny.md
        lang: pl
        label: "Instrukcja: Misja 16 — Przycisk awaryjny"
  misja-17:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_05_estop/02_tryb_zatrzymania_awaryjnego.md
        lang: pl
        label: "Instrukcja: Misja 17 — Tryb zatrzymania awaryjnego"
  misja-18:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_05_estop/03_dwie_niezalezne_sciezki.md
        lang: pl
        label: "Instrukcja: Misja 18 — Dwie niezależne ścieżki"
  misja-19:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_05_estop/04_silnik_pod_ochrona.md
        lang: pl
        label: "Instrukcja: Misja 19 — Obsługa zatrzymania awaryjnego w Engine"
---
W tym zestawie system dostaje drugą, niezależną ścieżkę reakcji na zatrzymanie awaryjne. Nie
zależy ona od decyzji sterownika ani od wyboru trasy paczki. Ma bezwzględny priorytet i nie pozwala
na automatyczne wznowienie pracy. Cztery zadania to misje 16–19 modułu 5 (w instrukcjach oznaczone
też jako 5.1–5.4): misja N ma test `misja-N`.

Jak zastrzegają wprowadzenie do modułu i plan pracy studenta, to uproszczony model dydaktyczny, a
nie projekt układu bezpieczeństwa spełniającego normy dla prawdziwej maszyny.

## Przygotowanie do zestawu

**Po module 4.** Zestaw kontynuuje [zestaw 4](belt-and-mode.md). Środowisko z modułu 0 już działa.

**Punkt startowy: tag `module-05-start`.** Tak jak w poprzednich modułach zaczynasz od tagu
startowego, a nie od własnej gałęzi z modułu 4. Tag zawiera kompletny kod modułu 4, w tym
`BeltMotor`, `Mode` i `Engine` sterowany trybem, oraz puste szkielety nowych elementów. Plan pracy
studenta podaje polecenia:

```bash
git fetch --tags
git switch -c my-work module-05-start
```

Jeśli gałąź `my-work` już istnieje, nadaj nowej gałęzi inną nazwę.

Kod startowy kompiluje się od razu. Testy modułów 1–4 (`misja-1`…`misja-4`, `misja-6`…`misja-15`)
przechodzą od początku, a testy `misja-16`…`misja-19` zgłaszają błąd, dopóki nie uzupełnisz kodu.
Program `simulator_cli` na starcie wypisuje przebieg z modułu 4: rozruch taśmy, ruch paczki, tryb i
stan silnika.

**Dokumentacja na `main`, kod na tagu.** Instrukcji modułu 5 nie ma w tagu `module-05-start`:
czytasz je na gałęzi `main`. Odnośniki do kodu w instrukcjach otwierają pliki z tagu na GitHubie, a
u siebie edytujesz plik pod tą samą ścieżką. Nie zmieniasz plików `CMakeLists.txt` ani testów.
`Engine::step()` zmieniasz dopiero w ostatniej misji.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 5 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#5-niezależna-ścieżka-awaryjnego-stopu).

## Zadania

### Misja 16: Przycisk awaryjny {#misja-16}

**Cel:** zbudować zatrzask przycisku awaryjnego, którego zwolnienie nie wznawia pracy
automatycznie.

**Zakres pracy:** w pliku `src/estop_latch.cpp` uzupełnij funkcję `nextEStopLatchState`. Wciśnięcie
ma najwyższy priorytet i zawsze daje `Engaged`. Z `Engaged` zwolnienie przycisku prowadzi do
`Armed`, a dopiero osobne potwierdzenie (`resetRequested`) w stanie `Armed` przywraca `Released`.
Instrukcja opisuje też przypadek jednoczesnego zwolnienia i potwierdzenia.

**Rezultat:** zatrzask przechodzi pełny cykl `Released` → `Engaged` → `Armed` → `Released` i
ignoruje potwierdzenie, dopóki przycisk jest wciśnięty.

**Sprawdź się:** `ctest --preset test -L misja-16`. Oczekiwany wynik:
`100% tests passed, 0 tests failed out of 1`. Test sprawdza pełny cykl, ignorowanie potwierdzenia w
`Engaged`, jednoczesne zwolnienie i potwierdzenie oraz priorytet wciśnięcia.

### Misja 17: Tryb zatrzymania awaryjnego {#misja-17}

**Cel:** dodać do `Mode` stan `EStopped`, który ma pierwszeństwo przed wszystkimi innymi
żądaniami.

**Zakres pracy:** deklaracja w `include/psm/mode.hpp` jest gotowa: `modeStep` ma nowy, ostatni
parametr `latch` z wartością domyślną. W pliku `src/mode.cpp` dopisz dwa sprawdzenia przed
istniejącą logiką: zatrzask inny niż `Released` daje `EStopped`, a wyjście z `EStopped` zawsze
prowadzi do `Idle`, nigdy od razu do `Running`.

**Rezultat:** zatrzymanie awaryjne wygrywa z każdym innym żądaniem, a po potwierdzeniu system czeka
w `Idle` na osobne uruchomienie.

**Sprawdź się:** `ctest --preset test -L misja-17`. Test sprawdza priorytet zatrzymania w różnych
stanach, powrót do `Idle` oraz jednoczesne potwierdzenie i żądanie uruchomienia. Instrukcja radzi
też ponownie uruchomić `ctest --preset test -L misja-14`: test z modułu 4 nadal przechodzi.

### Misja 18: Dwie niezależne ścieżki {#misja-18}

**Cel:** przygotować osobne funkcje decyzyjne ścieżki awaryjnej oraz operację, która natychmiast
zatrzymuje silnik.

**Zakres pracy:** w pliku `src/safety_supervisor.cpp` uzupełnij `checkEmergencyOverride` i
`diverterMayMove`. W pliku `src/belt_motor.cpp` uzupełnij `BeltMotor::forceStop()`, która ustawia
jednocześnie polecenie `Stop` i stan `Stopped`, z pominięciem `RampingDown`. W tej misji nie
zmieniasz jeszcze `Engine`.

**Rezultat:** obie funkcje zwracają decyzje zgodne z instrukcją, a po `forceStop()` kolejne
`resolve()` nie rozpoczyna ponownego rozruchu.

**Sprawdź się:** `ctest --preset test -L misja-18`. Test sprawdza obie funkcje decyzyjne i
zachowanie `forceStop()`.

### Misja 19: Obsługa zatrzymania awaryjnego w `Engine` {#misja-19}

**Cel:** połączyć zatrzask, rozszerzony tryb i funkcje bezpieczeństwa w `Engine::step()` tak, żeby
ścieżka awaryjna nie zależała wyłącznie od wartości `Mode`.

**Zakres pracy:** misja korzysta z wyników misji 16–18. W pliku `src/engine.cpp` uzupełnij
`requestEStop()`, `releaseEStop()` i `requestReset()` oraz rozszerz `Engine::step()` o siedem
kroków podanych w instrukcji. Decyzja awaryjna pochodzi bezpośrednio z zatrzasku, a zwykła logika
silnika i dywertera nie wykonuje się, gdy ta decyzja jest aktywna. W pliku
`apps/simulator_cli/main.cpp` pokaż zatrzymanie awaryjne, zwolnienie przycisku, potwierdzenie i
ponowne uruchomienie, a oprócz dotychczasowego wyniku wypisuj tryb i stan zatrzasku.

**Rezultat:** program pokazuje przebieg z instrukcji. Po zatrzymaniu awaryjnym w tym samym ticku tryb
to `EStopped`, zatrzask `Engaged`, silnik `Stopped`, a paczka stoi. Po zwolnieniu przycisku zatrzask
przechodzi w `Armed`, a tryb zostaje `EStopped`. Po potwierdzeniu tryb to `Idle`, a praca rusza
dopiero po osobnym `requestStart()`.

**Sprawdź się:** `ctest --preset test -L misja-19` sprawdza `Engine`. Scenariusza w `main()` nie
sprawdza żaden test. Pełny `ctest --preset test` przechodzi w całości, zanim zmienisz `main()`.
Zbuduj i uruchom program poleceniami z instrukcji (`cmake --build --preset dev`, a potem
`./build/dev/apps/simulator_cli/simulator_cli`; wariant dla Windows podaje instrukcja misji 6) i
porównaj wynik z przykładowym przebiegiem z instrukcji. Na koniec modułu uruchom
`ctest --preset test`: według instrukcji przechodzą wszystkie testy od `misja-1` do `misja-4` oraz
od `misja-6` do `misja-19`.

## Oczekiwane rezultaty

- Testy `misja-16`…`misja-19` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy się
  wynikiem `100% tests passed`.
- `simulator_cli` pokazuje zatrzymanie awaryjne, zwolnienie przycisku, potwierdzenie i ponowne
  uruchomienie, z trybem i stanem zatrzasku w każdym ticku.
- Twoja praca jest zapisana w commitach na własnej gałęzi utworzonej z `module-05-start`.

## Wskazówki

- Kolejność sprawdzeń ma w tym module duże znaczenie: wciśnięcie przycisku przed innymi sygnałami,
  zatrzask przed żądaniami uruchomienia i zatrzymania. Sekcje „Częste błędy” wskazują typowe pomyłki.
- Po wyjściu z `EStopped` system jest w `Idle`. Do ponownego ruchu taśmy potrzebne jest osobne
  `requestStart()`.
- Kod startowy nie ma funkcji zamieniającej stan zatrzasku na tekst. Do jego wypisania w misji 19
  potrzebujesz własnego przekształcenia.
- Zapisuj pracę w commitach po każdym sensownym etapie. Tak radzi plan pracy studenta.
