---
title: "Scenariusze zapisane w danych"
summary: "Trzy misje modułu 9: cały eksperyment opisany jedną wartością Scenario, sprawdzanie jej poprawności przed uruchomieniem, wykonywanie scenariusza tick po ticku i dwa scenariusze w programie terminalowym."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_09_scripted_scenarios/00_wprowadzenie.md
    lang: pl
    label: "Moduł 9 — wprowadzenie: co się zmienia i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-09-start
    lang: pl
    label: "Kod startowy modułu 9 (tag module-09-start)"
tasks:
  misja-33:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_09_scripted_scenarios/01_model_i_walidacja.md
        lang: pl
        label: "Instrukcja: Misja 33 — Model i sprawdzanie poprawności"
  misja-34:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_09_scripted_scenarios/02_odtwarzacz.md
        lang: pl
        label: "Instrukcja: Misja 34 — Uruchamianie scenariusza"
  misja-35:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_09_scripted_scenarios/03_integracja_w_cli.md
        lang: pl
        label: "Instrukcja: Misja 35 — Scenariusze w programie terminalowym"
---
W tym zestawie cały przebieg symulacji zapisujesz jako jedną wartość `Scenario`: polecenia
operatora, przybycia paczek, przedziały aktywności usterek i czas trwania. Scenariusz jest
sprawdzany przed uruchomieniem, a `runScenario()` wykonuje go na nowym `Engine` i zwraca wyniki
wszystkich ticków. Scenariusze są wartościami typów C++ budowanymi w kodzie; moduł nie wczytuje ich
z plików. Trzy zadania to misje 33–35 modułu 9 (w instrukcjach oznaczone też jako 9.1–9.3): testy
misji N mają etykietę `misja-N`.

## Przygotowanie do zestawu

**Po module 8.** Zestaw kontynuuje [zestaw 8](multiple-items.md). Środowisko z modułu 0 już działa.

**Punkt startowy: tag `module-09-start`.** Tak jak w poprzednich modułach zaczynasz od tagu
startowego, a nie od własnej gałęzi z modułu 8. Tag zawiera kompletny kod modułu 8, gotowe typy
scenariusza i szkielety `isValidScenario()`, `runScenario()` oraz dwóch funkcji tworzących
przykładowe scenariusze. `Engine` i pozostałe typy się nie zmieniają. Nowy jest gotowy program
`apps/simulator_cli/main.cpp`, którego nie edytujesz. Plan pracy studenta podaje polecenia:

```bash
git fetch --tags
git switch -c my-work module-09-start
```

Jeśli gałąź `my-work` już istnieje, nadaj nowej gałęzi inną nazwę.

Kod startowy kompiluje się od razu. Testy modułów 1–8 (`misja-1`, `misja-3`–`misja-4`,
`misja-6`–`misja-32`) przechodzą od początku, a testy `misja-33`…`misja-35` zgłaszają błąd, dopóki
nie uzupełnisz kodu. Program `simulator_cli` na starcie dwa razy wypisuje `scenario did not complete`
i kończy się kodem 0.

**Dokumentacja na `main`, kod na tagu.** Instrukcji modułu 9 nie ma w tagu `module-09-start`:
czytasz je na gałęzi `main`. Odnośniki do kodu w instrukcjach otwierają pliki z tagu na GitHubie, a
u siebie edytujesz plik pod tą samą ścieżką. Nie zmieniasz plików `CMakeLists.txt` ani testów.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 9 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#9-scenariusze-jako-dane).

## Zadania

### Misja 33: Model i sprawdzanie poprawności {#misja-33}

**Cel:** opisać cały eksperyment jedną wartością i odrzucić niepoprawny opis, zanim zacznie się
symulacja.

**Zakres pracy:** `Scenario` i pięć typów, z których korzysta, są gotowe w plikach nagłówkowych. W
pliku `src/scenario.cpp` uzupełnij `isValidScenario()` zgodnie z ośmioma regułami z instrukcji. Dotyczą
one przedziałów usterek i ich nakładania się (dla czujników osobno dla każdego celu), poleceń
operatora w jednym ticku, terminów względem `duration` oraz przybyć paczek i ich identyfikatorów.
Kolejność elementów w wektorach nie ma znaczenia.

**Rezultat:** funkcja przyjmuje każdy scenariusz zgodny z regułami, także pusty scenariusz o
`duration == 0`, i odrzuca każdy, który łamie którąkolwiek z nich.

**Sprawdź się:** `ctest --preset test -L misja-33`. Oczekiwany wynik:
`100% tests passed, 0 tests failed out of 1`. Test sprawdza osobno każdą z ośmiu reguł i przypadek
`duration == 0`, w tym parę `{Reset, StartRequested}`, którą trzeba odrzucić, i jednoczesne usterki
różnych czujników, które są dozwolone.

### Misja 34: Uruchamianie scenariusza {#misja-34}

**Cel:** wykonać poprawny scenariusz tick po ticku na nowym `Engine` i przy każdym uruchomieniu
otrzymać ten sam wynik.

**Zakres pracy:** w pliku `src/scenario.cpp` uzupełnij `runScenario()` i dodaj prywatne funkcje
`activeSensorFault()` i `activeDiverterFault()` w anonimowej przestrzeni nazw, a nie w
`scenario.hpp`. Zachowaj kolejność operacji w ticku z instrukcji: przybycia paczek, polecenia
operatora, ustawienie stanu usterek, `Engine::step()`, zapisanie wyniku. Stan usterek wyznaczasz od
nowa w każdym ticku. Błędy zgłaszasz przez typ zwracany, a nie przez `assert()`.

**Rezultat:** `runScenario()` zwraca pełną sekwencję `TickResult` albo `std::nullopt`, gdy scenariusz
jest niepoprawny albo zaplanowana paczka trafia na zajęty `infeed`. Nieudanego przybycia funkcja nie
ponawia.

**Sprawdź się:** `ctest --preset test -L misja-34`. Test porównuje pole po polu przebieg zapisany w
`Scenario` z tym samym przebiegiem wykonanym bezpośrednio na `Engine` i sprawdza przypadki wymienione
w instrukcji. Żaden z jego scenariuszy nie wykonuje jednak aktywnej usterki: implementacja bez obsługi
usterek albo z usterkami ustawianymi dopiero po `step()` przechodzi ten test. Obsługę usterki
dywertera sprawdza pośrednio test misji 35, bo scenariusz awarii musi dojść do `Mode::Fault`. Usterek
czujników w scenariuszu nie sprawdza żaden test, więc tę część porównaj z regułami z instrukcji,
czytając własny kod.

### Misja 35: Scenariusze w programie terminalowym {#misja-35}

**Cel:** zastąpić ręcznie zapisane sekwencje wywołań dwoma scenariuszami zapisanymi jako dane.

**Zakres pracy:** w pliku `apps/simulator_cli/scenario_demos.cpp` uzupełnij
`recoveryDemoScenario()` i `multiParcelDemoScenario()`. Pliku `main.cpp` nie zmieniasz. Pierwszy
scenariusz odtwarza awarię zablokowanego dywertera z [misji 28](fault-mode.md#misja-28); instrukcja
podaje wszystkie jego dane: przybycie paczki, polecenia operatora, przedział usterki i `duration`.
Drugi planuje przybycie trzech paczek różnych klas z odstępem co najmniej dwóch ticków.

**Rezultat:** program wypisuje oba przebiegi przez `describe()`. W pierwszym widać wykrycie awarii,
tryb `Fault`, reset i odjazd paczki, a w drugim trzy odjazdy do wyjść Light, Heavy i Light.

**Sprawdź się:** `ctest --preset test -L misja-35`. Instrukcja na `main` opisuje wcześniejszy układ
sprawdzania: test `simulator_cli_scenario_smoke` i kod zakończenia programu zależny od sprawdzeń w
`main.cpp`. W kodzie tagu `module-09-start` jest inaczej. Etykietę `misja-35` ma osobny test
`simulator_cli_scenario_test`, który wywołuje obie funkcje bezpośrednio, a `main.cpp` zawsze kończy
się kodem 0 i przy niewykonanym scenariuszu wypisuje `scenario did not complete`. Test `misja-6`
przechodzi więc przez cały moduł.

Test misji 35 sprawdza tylko minimalne warunki, o które pyta pytanie do zastanowienia w instrukcji:
oba scenariusze wykonują się do końca, w scenariuszu awarii pojawia się `Mode::Fault`, a w drugim są
co najmniej trzy odjazdy. Scenariusz awarii bez resetu i ponownego uruchomienia też go przechodzi,
choć paczka nigdy nie opuszcza linii. Dlatego zbuduj i uruchom program poleceniami z instrukcji
(`cmake --build --preset dev`, a potem `./build/dev/apps/simulator_cli/simulator_cli`; wariant dla
Windows podaje instrukcja misji 6) i porównaj pierwszy przebieg z przykładem z misji 28. Format
wyniku zmienił się w module 8, więc porównujesz kolejność zdarzeń, a nie tekst. Przykład z misji 28
numeruje kroki od 1, a `describe()` wypisuje numery ticków od 0: krok N odpowiada tickowi N−1. W
drugim przebiegu sprawdź odjazdy do wyjść Light, Heavy i Light. Na koniec modułu uruchom
`ctest --preset test`: według instrukcji przechodzą testy `misja-1`, `misja-3`–`misja-4` oraz
`misja-6`–`misja-35`.

## Oczekiwane rezultaty

- Testy `misja-33`…`misja-35` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy się
  wynikiem `100% tests passed`.
- `simulator_cli` wypisuje oba scenariusze do końca: awarię z resetem i powrotem do pracy oraz trzy
  paczki, które trafiają do wyjść Light, Heavy i Light.
- Twoja praca jest zapisana w commitach na własnej gałęzi utworzonej z `module-09-start`.

## Po module 9

Źródłowy plan pracy studenta przewiduje po module 9 rozmowę sprawdzającą z prowadzącym (sekcja
[„Rozmowy sprawdzające”](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/roadmap.md#rozmowy-sprawdzające)).
Następne etapy w tym planie to
[„Pierwszy własny test”](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/roadmap.md#pierwszy-własny-test)
i [„Projekt końcowy”](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/roadmap.md#projekt-końcowy).

## Wskazówki

- `Engine` nie dostaje w tym module nowego konstruktora ani pól. `runScenario()` korzysta z tych
  samych publicznych metod co testy i program z poprzednich modułów.
- Para `{EmergencyStopReleased, Reset}` w jednym ticku jest dozwolona. Instrukcja misji 34 wyjaśnia,
  dlaczego nie skraca dwuetapowego powrotu po zatrzymaniu awaryjnym. To nadal uproszczony model
  dydaktyczny z modułu 5, a nie układ bezpieczeństwa rzeczywistej maszyny.
- Jeśli program wypisuje `scenario did not complete`, `runScenario()` zwróciło `std::nullopt`:
  scenariusz jest niepoprawny albo paczka trafiła na zajęty `infeed`.
- Każda misja kończy się sekcją „Częste błędy” i pytaniem do zastanowienia. Zajrzyj do nich, zanim
  poprosisz o pomoc.
- Zapisuj pracę w commitach po każdym sensownym etapie. Tak radzi plan pracy studenta.
