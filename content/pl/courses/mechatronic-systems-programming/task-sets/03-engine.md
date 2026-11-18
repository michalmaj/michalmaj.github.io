---
title: "Engine"
summary: "Trzy misje modułu 3: wynik jednego ticku, klasa Engine jako jedyne miejsce, które zna kolejność operacji, i program konsolowy przepięty na silnik. Misję 12 sprawdzasz, uruchamiając symulator."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_03_engine/00_wprowadzenie.md
    lang: pl
    label: "Moduł 3 — wprowadzenie: skąd startujesz i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-03-start
    lang: pl
    label: "Kod startowy modułu 3 (tag module-03-start)"
tasks:
  misja-10:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_03_engine/01_tick_i_wynik.md
        lang: pl
        label: "Instrukcja: Misja 10 — Tick i wynik"
  misja-11:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_03_engine/02_silnik_formalizuje_kolejnosc.md
        lang: pl
        label: "Instrukcja: Misja 11 — Silnik porządkuje kolejność"
  misja-12:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_03_engine/03_przepiecie_na_silnik.md
        lang: pl
        label: "Instrukcja: Misja 12 — Przejście na silnik"
---
Po module 2 kolejność operacji w jednym ticku jest zapisana dwa razy: w `runTicks` i w `main()`.
W tym zestawie przenosisz ją do jednej klasy `Engine`, a program konsolowy zaczyna z niej
korzystać. Trzy zadania to misje 10–12 modułu 3 (w instrukcjach oznaczone też jako 3.1–3.3).
Misje 10 i 11 mają testy `misja-10` i `misja-11`. Misja 12 nie ma własnego testu: sprawdzasz ją,
uruchamiając `simulator_cli`.

## Przygotowanie do zestawu

**Po module 2.** Zestaw kontynuuje [zestaw 2](diverter-class.md). Środowisko z modułu 0 już działa.

**Punkt startowy: tag `module-03-start`.** Tak jak w poprzednim module zaczynasz od tagu startowego,
a nie od własnej gałęzi z modułu 2. Tag zawiera kompletny kod modułu 2, w tym `runTicks` i `main()`
działające tak jak po misji 9, oraz pusty szkielet klasy `Engine`. Plan pracy studenta podaje
polecenia:

```bash
git fetch --tags
git switch -c my-work module-03-start
```

Jeśli gałąź `my-work` już istnieje, nadaj nowej gałęzi inną nazwę.

Kod startowy kompiluje się od razu. Testy modułów 1 i 2 (`misja-1`…`misja-4`, `misja-6`…`misja-9`)
przechodzą od początku, a testy `misja-10` i `misja-11` zgłaszają błąd, dopóki nie uzupełnisz kodu.
Program `simulator_cli` już na starcie wypisuje poprawny przebieg, w formacie z modułu 2, na przykład
`tick 0: zone=PresenceCheck, diverter=Moving`.

**Dokumentacja na `main`, kod na tagu.** Instrukcji modułu 3 nie ma w tagu `module-03-start`:
czytasz je na gałęzi `main`. Odnośniki do kodu w instrukcjach otwierają pliki z tagu na GitHubie, a
u siebie edytujesz plik pod tą samą ścieżką. Nie zmieniasz plików `CMakeLists.txt` ani testów.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 3 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#3-koordynacja-systemu).

## Zadania

### Misja 10: Tick i wynik {#misja-10}

**Cel:** opisać wynik jednego ticku jednym typem i zamienić go na czytelny tekst.

**Zakres pracy:** typy `Tick` i `TickResult` są gotowe. W pliku `src/tick_result.cpp` uzupełnij
funkcję `describe`, która zwraca `"tick T: item ID in zone Z"`, gdy na przenośniku jest paczka, albo
`"tick T: empty"`, gdy go nie ma. Dokładny format i potrzebne nagłówki podaje instrukcja.

**Rezultat:** każdy wynik ticku ma jednoznaczny opis tekstowy. Do programu podłączysz go dopiero w
misji 12.

**Sprawdź się:** `ctest --preset test -L misja-10`. Oczekiwany wynik:
`100% tests passed, 0 tests failed out of 1`. Test porównuje napis znak w znak, dla paczki i dla
pustego przenośnika.

### Misja 11: Silnik porządkuje kolejność {#misja-11}

**Cel:** zbudować klasę `Engine`, która zawiera `Plant` i `Diverter` (kompozycja) i jako jedyna
wykonuje kroki symulacji w ustalonej kolejności.

**Zakres pracy:** deklaracje w `include/psm/engine.hpp` są gotowe. W pliku `src/engine.cpp`
uzupełnij `Engine::spawnItem`, która wywołuje wolną funkcję `psm::spawnItem`, oraz `Engine::step()`
z pięcioma krokami podanymi w instrukcji: decyzja sterownika, `setCommand`, `resolve`, `advance` i
zapisanie wyniku. Pierwsze wywołanie `step()` zwraca tick numer 0.

**Rezultat:** jedno wywołanie `step()` wykonuje cały cykl i zwraca kompletny `TickResult`.

**Sprawdź się:** `ctest --preset test -L misja-11`. Test wykonuje sześć kroków dla paczki 750 g i
sprawdza numery ticków, strefę paczki oraz polecenie i położenie rozjazdu.

### Misja 12: Przejście na silnik {#misja-12}

**Cel:** przepiąć program konsolowy na `Engine`, tak żeby kolejność operacji była zapisana tylko w
jednym miejscu.

**Zakres pracy:** misja korzysta z wyników misji 10 i 11. W pliku `apps/simulator_cli/main.cpp`
przepisz `main()`: utwórz `psm::Engine`, dodaj jedną paczkę przez `engine.spawnItem(...)`, a potem w
pętli wywołuj `engine.step()` i wypisuj wynik przez `psm::describe`. Plik `src/loop.cpp` z funkcją
`runTicks` zostaje w repozytorium, choć program już jej nie używa.

**Rezultat:** program wypisuje wiersze w formacie z `describe`: paczka przechodzi przez strefy,
trafia do `OutputHeavy` albo `OutputLight`, a potem pojawia się `empty`. Funkcja `main()` nie
odwołuje się już bezpośrednio do `Plant`, `Diverter`, `classify` ani `toDiverterCommand`.

**Sprawdź się:** ta misja nie ma etykiety `ctest`. Zbuduj i uruchom program poleceniami z
instrukcji (`cmake --build --preset dev`, a potem `./build/dev/apps/simulator_cli/simulator_cli`;
wariant dla Windows podaje instrukcja misji 6) i przeczytaj wynik. Testy nie potwierdzają
ukończenia tej misji:

- pełny `ctest --preset test` przechodzi w całości już po misjach 10 i 11, zanim zmienisz `main()`;
- test `misja-6` sprawdza tylko, czy program uruchamia się i kończy bez błędu;
- program z kodu startowego też wypisuje sensowny przebieg, tylko w innym formacie.

O ukończeniu misji świadczą więc wiersze w formacie `tick T: item ID in zone Z` i `tick T: empty`
oraz `main()` bez starej logiki. Na koniec modułu uruchom `ctest --preset test`: według instrukcji
przechodzą wszystkie testy od `misja-1` do `misja-4` oraz od `misja-6` do `misja-11`.

## Oczekiwane rezultaty

- Testy `misja-10` i `misja-11` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy
  się wynikiem `100% tests passed`.
- `simulator_cli` korzysta z `Engine` i wypisuje przebieg w formacie z `describe`.
- Twoja praca jest zapisana w commitach na własnej gałęzi utworzonej z `module-03-start`.

## Po module 3

Źródłowy plan pracy studenta przewiduje po module 3 rozmowę sprawdzającą z prowadzącym (sekcja
[„Rozmowy sprawdzające”](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/roadmap.md#rozmowy-sprawdzające)).

## Wskazówki

- W `Engine::step()` numer ticku zapisujesz w wyniku przed zwiększeniem licznika, a `resolve()`
  wykonujesz przed `advance()`. Instrukcja misji 11 opisuje skutki obu pomyłek.
- `Plant` pozostaje strukturą bez metod: w `Engine` wywołujesz wolne funkcje `psm::spawnItem` i
  `psm::advance`, a nie metody `plant_`.
- Każda misja kończy się sekcją „Częste błędy” i pytaniem do zastanowienia. Zajrzyj do nich, zanim
  poprosisz o pomoc.
- Zapisuj pracę w commitach po każdym sensownym etapie. Tak radzi plan pracy studenta.
