---
title: "Tryb awarii"
summary: "Cztery misje modułu 7: zablokowany dywerter, limit czasu na jego ustawienie, tryb Fault wyznaczany w dwóch krokach i Engine z wykrywaniem awarii oraz scenariuszem jej usunięcia."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_07_fault_mode/00_wprowadzenie.md
    lang: pl
    label: "Moduł 7 — wprowadzenie: skąd startujesz i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-07-start
    lang: pl
    label: "Kod startowy modułu 7 (tag module-07-start)"
tasks:
  misja-25:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_07_fault_mode/01_zablokowany_dywerter.md
        lang: pl
        label: "Instrukcja: Misja 25 — Zablokowany dywerter"
  misja-26:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_07_fault_mode/02_termin_rutowania.md
        lang: pl
        label: "Instrukcja: Misja 26 — Limit czasu na ustawienie dywertera"
  misja-27:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_07_fault_mode/03_tryb_awarii.md
        lang: pl
        label: "Instrukcja: Misja 27 — Tryb awarii"
  misja-28:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_07_fault_mode/04_silnik_z_wykrywaniem_awarii.md
        lang: pl
        label: "Instrukcja: Misja 28 — Engine z wykrywaniem awarii"
---
W tym zestawie system rozpoznaje usterkę elementu wykonawczego. Zablokowany dywerter nie ustawia
się w wyznaczonym czasie, `Plant` zgłasza zdarzenie, a system przechodzi do trybu `Mode::Fault`, z
którego wychodzi się tylko przez jawny reset. Cztery zadania to misje 25–28 modułu 7 (w
instrukcjach oznaczone też jako 7.1–7.4): misja N ma test `misja-N`.

## Przygotowanie do zestawu

**Po module 6.** Zestaw kontynuuje [zestaw 6](sensors.md). Środowisko z modułu 0 już działa.

**Punkt startowy: tag `module-07-start`.** Tak jak w poprzednich modułach zaczynasz od tagu
startowego, a nie od własnej gałęzi z modułu 6. Tag zawiera kompletny kod modułu 6 oraz szkielety
nowych elementów. Plan pracy studenta podaje polecenia:

```bash
git fetch --tags
git switch -c my-work module-07-start
```

Jeśli gałąź `my-work` już istnieje, nadaj nowej gałęzi inną nazwę.

Kod startowy kompiluje się od razu. Testy modułów 1–6 (`misja-1`…`misja-4`, `misja-6`…`misja-24`)
przechodzą od początku, a testy `misja-25`…`misja-28` zgłaszają błąd, dopóki nie uzupełnisz kodu.
Program `simulator_cli` na starcie wypisuje scenariusze z modułu 6.

**Zmienione nazwy usterek czujników.** W kodzie startowym usterki czujników mają nowe nazwy:
`SensorFaultKind` i `SensorTarget` oraz metody `injectSensorFault` i `clearSensorFault`, a testy
modułu 6 zostały dostosowane do tych nazw. Instrukcja misji 28 mówi, że ta zmiana jest już
wprowadzona i nie wymaga Twojej pracy.

**Dokumentacja na `main`, kod na tagu.** Instrukcji modułu 7 nie ma w tagu `module-07-start`:
czytasz je na gałęzi `main`. Odnośniki do kodu w instrukcjach otwierają pliki z tagu na GitHubie, a
u siebie edytujesz plik pod tą samą ścieżką. Nie zmieniasz plików `CMakeLists.txt` ani testów.
`Engine::step()` zmieniasz dopiero w ostatniej misji.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 7 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#7-usterki-i-zdarzenia-systemowe).

## Zadania

### Misja 25: Zablokowany dywerter {#misja-25}

**Cel:** zasymulować usterkę elementu wykonawczego osobnym typem `DiverterFaultKind`, którego nie
da się pomylić z usterką czujnika.

**Zakres pracy:** sygnatura `resolve()` z parametrem usterki jest gotowa. W pliku
`src/diverter.cpp` dopisz na początku `Diverter::resolve()` sprawdzenie usterki `Blocked`, przed
dotychczasową logiką. Metody `isSettled()` nie zmieniasz.

**Rezultat:** zablokowany dywerter nie zmienia położenia, także gdy zatrzymał się w `Moving`, a bez
usterki działa jak w module 2.

**Sprawdź się:** `ctest --preset test -L misja-25`. Oczekiwany wynik:
`100% tests passed, 0 tests failed out of 1`.

### Misja 26: Limit czasu na ustawienie dywertera {#misja-26}

**Cel:** wykryć, że dywerter nie ustawia się w wyznaczonym czasie, licząc tylko kolejne aktywne
próby skierowania paczki.

**Zakres pracy:** typ zdarzenia, licznik `divertingWaitTicks` i nowa sygnatura `advance()` są
gotowe. W pliku `src/plant.cpp` uzupełnij gałąź `Diverting` według reguły z instrukcji. Przy
`routingReady` równym `false` licznik się zeruje. Przy nieustawionym dywerterze licznik rośnie, a
funkcja zgłasza `DiverterNotReady` albo, po przekroczeniu limitu, `RoutingDeadlineMissed`. Po
skierowaniu paczki do wyjścia licznik się zeruje.

**Rezultat:** pierwsza nieudana próba daje `DiverterNotReady`, druga z rzędu
`RoutingDeadlineMissed`, a przerwa w możliwości skierowania paczki zaczyna liczenie od nowa.

**Sprawdź się:** `ctest --preset test -L misja-26`.

### Misja 27: Tryb awarii {#misja-27}

**Cel:** rozdzielić wyznaczanie trybu na dwie decyzje podejmowane w różnych momentach ticku.

**Zakres pracy:** `Mode::Fault` i deklaracje obu funkcji są gotowe. W pliku `src/mode.cpp` dodaj w
`modeStep()` regułę dla `Fault`: po obsłudze zatrzymania awaryjnego, a przed żądaniami zatrzymania i
uruchomienia. Bez resetu tryb zostaje `Fault`, a reset prowadzi do `Idle`. Uzupełnij też
`reactToSystemEvent()`, która zwraca `Fault` tylko dla trybu `Running` i zdarzenia
`RoutingDeadlineMissed`.

**Rezultat:** tryb `Fault` trwa aż do resetu, powrót prowadzi przez `Idle`, a zatrzymanie awaryjne ma
pierwszeństwo przed `Fault`.

**Sprawdź się:** `ctest --preset test -L misja-27`.

### Misja 28: `Engine` z wykrywaniem awarii {#misja-28}

**Cel:** połączyć zablokowany dywerter, licznik i dwuetapowe wyznaczanie trybu w `Engine`.

**Zakres pracy:** misja korzysta z wyników misji 25–27. W pliku `src/engine.cpp` uzupełnij
`injectDiverterFault` i `clearDiverterFault` oraz wprowadź w `Engine::step()` cztery zmiany z
instrukcji:

- wynik `modeStep(...)` zapisz w lokalnej zmiennej `modeForTick`;
- użyj `modeForTick` do sterowania taśmą i dywerterem i przekaż usterkę do `diverter_.resolve()`;
- zapisz zdarzenie zwrócone przez `advance()`;
- na końcu ustaw `mode_` przez `reactToSystemEvent()`.

Dodaj też zdarzenie do `TickResult`. W wywołaniu `modeStep(...)` przekaż również żądanie resetu,
czyli nowy parametr z misji 27. Bez tego tryb `Fault` nie kończy się po `requestReset()` i test
`misja-28` nie przechodzi. W pliku `apps/simulator_cli/main.cpp` przygotuj scenariusz usunięcia
awarii z instrukcji.

**Rezultat:** przebieg jak w przykładowym scenariuszu z instrukcji:

- przy zablokowanym dywerterze najpierw pojawia się `DiverterNotReady`, potem
  `RoutingDeadlineMissed` i tryb `Fault`;
- taśma zaczyna zwalniać dopiero w następnym ticku;
- `clearDiverterFault()` nie zmienia trybu, a `requestReset()` przywraca `Idle`;
- po osobnym `requestStart()` paczka trafia do wyjścia.

**Sprawdź się:** `ctest --preset test -L misja-28` przechodzi krok po kroku przez scenariusz w
`Engine`. Scenariusza w `main()` nie sprawdza żaden test. Pełny `ctest --preset test` przechodzi w
całości, zanim zmienisz `main()`. Zbuduj i uruchom program poleceniami z instrukcji
(`cmake --build --preset dev`, a potem `./build/dev/apps/simulator_cli/simulator_cli`; wariant dla
Windows podaje instrukcja misji 6) i porównaj wynik z przykładowym scenariuszem z instrukcji. Na
koniec modułu uruchom `ctest --preset test`: według instrukcji przechodzą wszystkie testy od
`misja-1` do `misja-4` oraz od `misja-6` do `misja-28`.

## Oczekiwane rezultaty

- Testy `misja-25`…`misja-28` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy się
  wynikiem `100% tests passed`.
- `simulator_cli` pokazuje wykrycie awarii, zatrzymanie taśmy, usunięcie blokady, reset i ponowne
  uruchomienie.
- Twoja praca jest zapisana w commitach na własnej gałęzi utworzonej z `module-07-start`.

## Po module 7

Źródłowy plan pracy studenta przewiduje po module 7 rozmowę sprawdzającą z prowadzącym (sekcja
[„Rozmowy sprawdzające”](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/roadmap.md#rozmowy-sprawdzające)).

## Wskazówki

- Opóźnienie zatrzymania taśmy o jeden tick po przejściu do `Fault` jest zamierzonym zachowaniem
  modelu. Przycisk awaryjny z modułu 5 działa inaczej: zatrzymuje taśmę natychmiast i ma
  pierwszeństwo przed `Fault`. To nadal ten sam uproszczony model dydaktyczny, a nie układ
  bezpieczeństwa rzeczywistej maszyny.
- `requestReset()` kończy tryb awarii, ale nie usuwa jej przyczyny. Bez `clearDiverterFault()`
  scenariusz wraca do `Fault`.
- Każda misja kończy się sekcją „Częste błędy” i pytaniem do zastanowienia. Zajrzyj do nich, zanim
  poprosisz o pomoc.
- Zapisuj pracę w commitach po każdym sensownym etapie. Tak radzi plan pracy studenta.
