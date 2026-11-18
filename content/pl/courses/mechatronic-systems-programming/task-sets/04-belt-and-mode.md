---
title: "Pas i tryb pracy"
summary: "Trzy misje modułu 4: silnik przenośnika, który rozpędza się i zatrzymuje z opóźnieniem, tryb pracy całego systemu i Engine, w którym paczka rusza dopiero przy pracującej taśmie."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_04_belt_and_mode/00_wprowadzenie.md
    lang: pl
    label: "Moduł 4 — wprowadzenie: skąd startujesz i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-04-start
    lang: pl
    label: "Kod startowy modułu 4 (tag module-04-start)"
tasks:
  misja-13:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_04_belt_and_mode/01_silnik_przenosnika.md
        lang: pl
        label: "Instrukcja: Misja 13 — Silnik przenośnika"
  misja-14:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_04_belt_and_mode/02_tryb_pracy.md
        lang: pl
        label: "Instrukcja: Misja 14 — Tryb pracy"
  misja-15:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_04_belt_and_mode/03_przenosnik_pod_kontrola_trybu.md
        lang: pl
        label: "Instrukcja: Misja 15 — Przenośnik pod kontrolą trybu"
---
W tym zestawie `Engine` dostaje silnik przenośnika (`BeltMotor`), który potrzebuje czasu na
rozpędzenie i zatrzymanie, oraz tryb pracy (`Mode`) opisujący stan całego systemu. Paczka rusza
dopiero wtedy, gdy taśma naprawdę pracuje. Trzy zadania to misje 13–15 modułu 4 (w instrukcjach
oznaczone też jako 4.1–4.3): misja N ma test `misja-N`.

## Przygotowanie do zestawu

**Po module 3.** Zestaw kontynuuje [zestaw 3](engine.md). Środowisko z modułu 0 już działa.

**Punkt startowy: tag `module-04-start`.** Tak jak w poprzednich modułach zaczynasz od tagu
startowego, a nie od własnej gałęzi z modułu 3. Tag zawiera kompletny kod modułu 3, w tym `Engine`
i `main()` korzystający z `describe`, oraz puste szkielety `BeltMotor` i `Mode`. Plan pracy studenta
podaje polecenia:

```bash
git fetch --tags
git switch -c my-work module-04-start
```

Jeśli gałąź `my-work` już istnieje, nadaj nowej gałęzi inną nazwę.

Kod startowy kompiluje się od razu. Testy modułów 1–3 (`misja-1`…`misja-4`, `misja-6`…`misja-11`)
przechodzą od początku, a testy `misja-13`…`misja-15` zgłaszają błąd, dopóki nie uzupełnisz kodu.
Test `misja-11` jest w tym module zawężony: sprawdza już tylko licznik ticków pustego `Engine`, bo po
dodaniu napędu paczka nie porusza się natychmiast. Wprowadzenie do modułu wyjaśnia tę zmianę.
Program `simulator_cli` na starcie wypisuje przebieg z modułu 3, w formacie z `describe`.

**Dokumentacja na `main`, kod na tagu.** Instrukcji modułu 4 nie ma w tagu `module-04-start`:
czytasz je na gałęzi `main`. Odnośniki do kodu w instrukcjach otwierają pliki z tagu na GitHubie, a
u siebie edytujesz plik pod tą samą ścieżką. Nie zmieniasz plików `CMakeLists.txt` ani testów.
`Engine::step()` zmieniasz dopiero w ostatniej misji.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 4 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#4-element-wykonawczy-i-tryb-pracy).

## Zadania

### Misja 13: Silnik przenośnika {#misja-13}

**Cel:** napisać kolejną klasę, która oddziela polecenie od rzeczywistego stanu urządzenia. Silnik
ma cztery stany: `Stopped`, `RampingUp`, `Running` i `RampingDown`.

**Zakres pracy:** deklaracje są gotowe. W pliku `src/belt_motor.cpp` uzupełnij `setCommand`,
`resolve` i `actualState`. Tym razem instrukcja nie podaje tabeli przejść, tylko zasady, które
zamieniasz na instrukcję `switch`. Każde wywołanie `resolve()` wykonuje najwyżej jedno przejście.

**Rezultat:** silnik rozpędza się i zatrzymuje przez stany pośrednie i reaguje na zmianę polecenia
w trakcie rozruchu albo zatrzymywania.

**Sprawdź się:** `ctest --preset test -L misja-13`. Oczekiwany wynik:
`100% tests passed, 0 tests failed out of 1`. Test przechodzi pełny cykl rozpędzenia i zatrzymania
oraz zmianę polecenia w trakcie każdego z nich.

### Misja 14: Tryb pracy {#misja-14}

**Cel:** opisać stan całego systemu typem wyliczeniowym `Mode` i wolną funkcją, bez osobnej klasy.

**Zakres pracy:** w pliku `src/mode.cpp` uzupełnij funkcję `modeStep`. Żądanie zatrzymania ma
pierwszeństwo przed żądaniem uruchomienia, a bez żadnego żądania tryb się nie zmienia. Kolejność
sprawdzeń podaje instrukcja.

**Rezultat:** `modeStep` zwraca poprawny tryb dla każdej kombinacji żądań, także gdy oba są
zgłoszone jednocześnie.

**Sprawdź się:** `ctest --preset test -L misja-14`. Test sprawdza wszystkie cztery kombinacje żądań.

### Misja 15: Przenośnik pod kontrolą trybu {#misja-15}

**Cel:** połączyć `BeltMotor` i `Mode` z `Engine`, tak żeby paczka poruszała się tylko przy
pracującej taśmie.

**Zakres pracy:** misja korzysta z wyników misji 13 i 14. W pliku `src/engine.cpp` uzupełnij
`requestStart()` i `requestStop()` oraz rozszerz `Engine::step()` o kroki podane w instrukcji:
obliczenie trybu, sterowanie silnikiem i przesunięcie paczki tylko wtedy, gdy silnik jest w stanie
`Running`. Pola w `engine.hpp` i `tick_result.hpp` są gotowe. W pliku `apps/simulator_cli/main.cpp`
wywołaj `engine.requestStart()` przed pętlą i oprócz wyniku `describe()` wypisuj tryb oraz stan
silnika. Samej funkcji `describe()` nie zmieniasz.

**Rezultat:** po `requestStart()` silnik najpierw się rozpędza, a paczka rusza dopiero w ticku, w
którym taśma osiąga `Running`. Program pokazuje ten przebieg razem z trybem i stanem silnika.

**Sprawdź się:** `ctest --preset test -L misja-15` sprawdza `Engine`: przebieg z instrukcji, w
którym pierwszy krok po `requestStart()` nie rusza paczki, a drugi przesuwa ją o jedną strefę, oraz
zatrzymanie. Zmian w `main()` nie sprawdza żaden test. Pełny `ctest --preset test` przechodzi
w całości, zanim zmienisz `main()`. Zbuduj i uruchom program poleceniami z instrukcji
(`cmake --build --preset dev`, a potem `./build/dev/apps/simulator_cli/simulator_cli`; wariant dla
Windows podaje instrukcja misji 6) i przeczytaj wynik. Jeśli paczka przez cały czas stoi w `Infeed`,
w `main()` brakuje `requestStart()`. Na koniec modułu uruchom `ctest --preset test`: według
instrukcji przechodzą wszystkie testy od `misja-1` do `misja-4` oraz od `misja-6` do `misja-15`.

## Oczekiwane rezultaty

- Testy `misja-13`…`misja-15` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy się
  wynikiem `100% tests passed`.
- `simulator_cli` pokazuje rozruch taśmy, ruch paczki dopiero przy `Running` oraz tryb i stan
  silnika w każdym ticku.
- Twoja praca jest zapisana w commitach na własnej gałęzi utworzonej z `module-04-start`.

## Wskazówki

- `Mode::Running` razem z `RampingUp` oraz `Mode::Idle` razem z `RampingDown` to poprawne stany
  przejściowe, a nie błędy. Instrukcja misji 15 wyjaśnia dlaczego.
- Warunek ruchu paczki sprawdzasz po `beltMotor_.resolve()` w tym samym ticku, nie przed nim.
- Kod startowy ma funkcję zamieniającą na tekst tylko strefę (`psm::toString`). Do wypisania trybu
  i stanu silnika w misji 15 potrzebujesz własnego przekształcenia, tak jak dla położenia rozjazdu w
  module 2.
- Każda misja kończy się sekcją „Częste błędy” i pytaniem do zastanowienia. Zajrzyj do nich, zanim
  poprosisz o pomoc.
- Zapisuj pracę w commitach po każdym sensownym etapie. Tak radzi plan pracy studenta.
