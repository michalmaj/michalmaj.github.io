---
title: "Klasa Diverter"
summary: "Trzy misje modułu 2: rozjazd przestaje zmieniać położenie natychmiast, polecenie sterownika oddziela się od stanu urządzenia, a przenośnik czeka, aż dywerter się ustawi. Pierwsza klasa w kursie."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_02_diverter_class/00_wprowadzenie.md
    lang: pl
    label: "Moduł 2 — wprowadzenie: skąd startujesz i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-02-start
    lang: pl
    label: "Kod startowy modułu 2 (tag module-02-start)"
tasks:
  misja-7:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_02_diverter_class/01_polecenie_a_rzeczywistosc.md
        lang: pl
        label: "Instrukcja: Misja 7 — Polecenie a rzeczywistość"
  misja-8:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_02_diverter_class/02_dywerter_jako_klasa.md
        lang: pl
        label: "Instrukcja: Misja 8 — Dywerter jako klasa"
  misja-9:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_02_diverter_class/03_przenosnik_czeka_na_dywerter.md
        lang: pl
        label: "Instrukcja: Misja 9 — Przenośnik czeka na dywerter"
---
W tym zestawie rozjazd (dywerter) przestaje zmieniać położenie natychmiast. Przechodzi między
`Straight` i `Diverted` przez stan pośredni `Moving`, a przenośnik czeka, aż rozjazd się ustawi.
Piszesz przy tym pierwszą klasę w kursie. Trzy zadania to misje 7–9 modułu 2 (w instrukcjach
oznaczone też jako 2.1–2.3): misja N ma test `misja-N`.

## Przygotowanie do zestawu

**Po module 1.** Zestaw kontynuuje [zestaw 1](control-basics.md). Środowisko z modułu 0 już
działa. Jeśli coś przestało działać, wróć do sprawdzenia narzędzi opisanego w zestawie 1.

**Punkt startowy: tag `module-02-start`.** Każdy moduł zaczynasz od jego tagu startowego, a nie od
własnej gałęzi z poprzedniego modułu. Tag zawiera kompletny kod modułu 1, więc wszyscy zaczynają od
tego samego, działającego stanu. Plan pracy studenta podaje polecenia:

```bash
git fetch --tags
git switch -c my-work module-02-start
```

Jeśli gałąź `my-work` została po module 1, nadaj nowej gałęzi inną nazwę.

Kod startowy kompiluje się od razu. Testy `misja-1`…`misja-4` i `misja-6` przechodzą od początku,
a testy `misja-7`…`misja-9` zgłaszają błąd, dopóki nie uzupełnisz odpowiadającego im kodu. Testu
`misja-5` w tym module już nie ma: jego rolę przejął test misji 9. Miejsca do uzupełnienia są
oznaczone komentarzem `// TODO (Misja N: …)`. Program `simulator_cli` w kodzie startowym nic nie
wypisuje, bo jego `main()` piszesz dopiero w misji 9.

**Dokumentacja na `main`, kod na tagu.** Instrukcji modułu 2 nie ma w tagu `module-02-start`:
czytasz je na gałęzi `main`. Tag zawiera kod, który uzupełniasz. Odnośniki do kodu w instrukcjach
otwierają pliki z tagu na GitHubie, a u siebie edytujesz plik pod tą samą ścieżką.

Tak jak w module 1 nie zmieniasz plików `CMakeLists.txt` ani testów. Testy tylko uruchamiasz.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 2 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#2-polecenie-to-nie-stan-fizyczny).

## Zadania

### Misja 7: Polecenie a rzeczywistość {#misja-7}

**Cel:** oddzielić polecenie sterownika od rzeczywistego położenia rozjazdu. Polecenie dostaje
własny typ `DiverterCommand`, a `DiverterPosition` opisuje odtąd stan fizyczny.

**Zakres pracy:** w pliku `src/controller.cpp` uzupełnij funkcję `toDiverterCommand`: paczka lekka
daje `HoldStraight`, a ciężka `Divert`. Funkcja `classify` się nie zmienia.

**Rezultat:** sterownik wydaje polecenie dla rozjazdu, a nie ustawia jego położenia.

**Sprawdź się:** `ctest --preset test -L misja-7`. Oczekiwany wynik:
`100% tests passed, 0 tests failed out of 1`. Test sprawdza oba przyporządkowania.

### Misja 8: Dywerter jako klasa {#misja-8}

**Cel:** napisać pierwszą klasę w kursie: prywatny stan, publiczne metody i niezmiennik, którego
nic z zewnątrz nie może złamać.

**Zakres pracy:** w pliku `src/diverter.cpp` uzupełnij ciała czterech metod klasy `Diverter`:
`setCommand`, `resolve`, `actualPosition` i `isSettled`. Deklaracje są gotowe. `resolve()`
realizuje tabelę przejść z instrukcji: każde wywołanie przesuwa rozjazd najwyżej o jeden krok, przez
`Moving`. `isSettled()` liczy porównanie przy każdym wywołaniu, zamiast korzystać z zapamiętanej
odpowiedzi.

**Rezultat:** rozjazd przechodzi z `Straight` do `Diverted` i z powrotem przez `Moving`, a
`isSettled()` od razu po `setCommand()` odzwierciedla nowe polecenie.

**Sprawdź się:** `ctest --preset test -L misja-8`. Test przechodzi pełną tabelę przejść w obie
strony i sprawdza `isSettled()` zaraz po `setCommand()`, przed `resolve()`.

### Misja 9: Przenośnik czeka na dywerter {#misja-9}

**Cel:** połączyć dwie poprzednie misje: przenośnik uwzględnia czas ruchu rozjazdu i czeka, aż ten
się ustawi.

**Zakres pracy:** misja korzysta z wyników misji 7 i 8. W pliku `src/plant.cpp` uzupełnij gałąź
`Diverting`: dopóki rozjazd się nie ustawił, paczka czeka; potem trafia do wyjścia zgodnego z
położeniem rozjazdu. W pliku `src/loop.cpp` napisz `runTicks` z własnym obiektem `Diverter` i
kolejnością kroków podaną w instrukcji (decyzja sterownika, `setCommand`, `resolve`, `advance`). W
pliku `apps/simulator_cli/main.cpp` napisz `main()`, który w pętli wykonuje te same kroki i po
każdym ticku wypisuje jego numer, strefę paczki i położenie rozjazdu.

**Rezultat:** przenośnik czeka na rozjazd, a program konsolowy pokazuje kolejne ticki z położeniem
rozjazdu.

**Sprawdź się:** `ctest --preset test -L misja-9`. Test sprawdza `runTicks` oraz scenariusz, w
którym polecenie `Divert` pada dopiero wtedy, gdy paczka już czeka w `Diverting`. Funkcji `main()`
nie sprawdza żaden test. Test `misja-6` sprawdza tylko, czy program uruchamia się i kończy bez
błędu, więc przechodzi także przy pustym `main()` z kodu startowego. Zbuduj i uruchom program
poleceniami z instrukcji (`cmake --build --preset dev`, a potem
`./build/dev/apps/simulator_cli/simulator_cli`; wariant dla Windows podaje instrukcja misji 6) i
przeczytaj wynik. Na koniec modułu uruchom `ctest --preset test`: według instrukcji przechodzą
wszystkie testy od `misja-1` do `misja-4` oraz od `misja-6` do `misja-9`.

## Oczekiwane rezultaty

- Testy `misja-7`…`misja-9` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy się
  wynikiem `100% tests passed`.
- `simulator_cli` wypisuje przebieg, w którym widać strefy paczki i położenie rozjazdu.
- Twoja praca jest zapisana w commitach na własnej gałęzi utworzonej z `module-02-start`.

## Wskazówki

- Kolejność `resolve()` i `advance()` w jednym ticku ma znaczenie: po zamianie wyniki przesuwają się
  o jeden tick. Instrukcja misji 9 wyjaśnia dlaczego.
- Kod startowy ma funkcję zamieniającą na tekst tylko strefę (`psm::toString`). Do wypisania
  położenia rozjazdu w misji 9 potrzebujesz własnego przekształcenia.
- Każda misja kończy się sekcją „Częste błędy” i pytaniem do zastanowienia. Zajrzyj do nich, zanim
  poprosisz o pomoc.
- Zapisuj pracę w commitach po każdym sensownym etapie. Tak radzi plan pracy studenta.
