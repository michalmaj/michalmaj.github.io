---
title: "Podstawy sterowania"
summary: "Sześć misji modułu 1, poprzedzonych przygotowaniem środowiska w module 0: paczka przechodzi przez strefy przenośnika i trafia do właściwego wyjścia, a symulator pokazuje działanie Twojego kodu."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: course/module_00_tooling/
    lang: pl
    label: "Moduł 0 — wszystkie kroki, z wariantami dla Windows, Linuksa i macOS"
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_01_control_basics/00_wprowadzenie.md
    lang: pl
    label: "Moduł 1 — wprowadzenie: skąd startujesz i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-01-start
    lang: pl
    label: "Kod startowy modułu 1 (tag module-01-start)"
tasks:
  misja-1:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_01_control_basics/01_paczka_i_strefy.md
        lang: pl
        label: "Instrukcja: Misja 1 — Paczka i strefy"
  misja-2:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_01_control_basics/02_ruch_paczki.md
        lang: pl
        label: "Instrukcja: Misja 2 — Ruch paczki"
  misja-3:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_01_control_basics/03_stan_przenosnika.md
        lang: pl
        label: "Instrukcja: Misja 3 — Stan przenośnika"
  misja-4:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_01_control_basics/04_decyzja_sortowania.md
        lang: pl
        label: "Instrukcja: Misja 4 — Decyzja sortowania"
  misja-5:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_01_control_basics/05_petla_sterowania.md
        lang: pl
        label: "Instrukcja: Misja 5 — Pętla sterowania"
  misja-6:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_01_control_basics/06_pierwszy_przebieg.md
        lang: pl
        label: "Instrukcja: Misja 6 — Pierwszy przebieg"
---
W tym zestawie piszesz pierwszą logikę symulatora linii sortującej. Jedna paczka przechodzi przez
kolejne strefy przenośnika i na końcu trafia do wyjścia dla paczek lekkich albo ciężkich, zależnie
od swojej masy. Sześć zadań odpowiada misjom 1–6 modułu 1 i testom `misja-1`…`misja-6`. Na koniec
program `simulator_cli` pokaże na konsoli działanie Twojego kodu.

## Przygotowanie do zestawu

Potrzebujesz komputera z Windows, Linuksem albo macOS oraz podstaw programowania w dowolnym języku.
Znajomość C++ nie jest wymagana.

**Moduł 0: środowisko.** Zaczynasz od
[modułu 0](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/course/module_00_tooling/00_orientacja.md).
Nie ma on misji ani tagu startowego: pracujesz na gałęzi `main`. Przejdź po kolei kroki 0.0–0.8:
orientacja; terminal i instalacja narzędzi (kompilator, CMake, Git, środowisko programistyczne) w
wariancie dla swojego systemu; pobranie repozytorium; pierwsze budowanie; celowa zmiana i błąd
kompilacji; pierwsze uruchomienie testów; podgląd symulatora. Kroki 0.3 (Git przez Chocolatey na
Windows) i 0.9 (Git i GitHub) są opcjonalne.

**Sprawdzenie narzędzi i testów.** Według instrukcji modułu 0 środowisko jest gotowe, gdy:

- program `toolchain_check` wypisuje komunikat o poprawnie połączonych narzędziach;
- `ctest --preset test` na gałęzi `main` kończy się wynikiem `100% tests passed`;
- `simulator_cli` wypisuje kolejne kroki symulacji.

**Dokumentacja na `main`, kod na tagu `module-01-start`.** Instrukcje misji czytasz na gałęzi
`main`, gdzie jest ich aktualna wersja. Kod piszesz na własnej gałęzi utworzonej z tagu startowego
modułu 1 (odnośnik do tagu jest w sekcji „Materiały”). Plan pracy studenta podaje polecenia:

```bash
git fetch --tags
git switch -c my-work module-01-start
```

Kod startowy kompiluje się od razu, a miejsca do uzupełnienia są oznaczone komentarzem `// TODO`.
Testy misji 1–5 zgłaszają błąd, dopóki nie uzupełnisz odpowiadającego im kodu. Test misji 6
sprawdza tylko, czy program się uruchamia. Pliki `.md` w tagu są kopią z chwili jego publikacji:
jeśli różnią się od wersji na `main`, aktualna jest wersja na `main`. Odnośniki do kodu w
instrukcjach otwierają pliki z tagu na GitHubie. U siebie edytujesz plik pod tą samą ścieżką.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 1 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#1-modelowanie-prostego-procesu).

## Zadania

### Paczka i strefy {#misja-1}

**Cel:** poznać `enum class` i `struct` jako sposób opisania stref przenośnika i jednej paczki.

**Zakres pracy:** w pliku `src/zone.cpp` uzupełnij funkcję `toString` tak, jak opisuje to
instrukcja.

**Rezultat:** każda z sześciu stref ma w programie własny, czytelny napis.

**Sprawdź się:** `ctest --preset test -L misja-1`. Oczekiwany wynik podaje instrukcja.

### Ruch paczki {#misja-2}

**Cel:** przekazać obiekt do funkcji przez referencję i zmienić jego stan.

**Zakres pracy:** w pliku `src/item_motion.cpp` uzupełnij funkcję `advanceZone`, która przesuwa
paczkę o jedną strefę do przodu, w kolejności podanej w instrukcji.

**Rezultat:** paczka przechodzi kolejne strefy aż do rozjazdu (`Diverting`) i tam się na razie
zatrzymuje.

**Sprawdź się:** `ctest --preset test -L misja-2`.

### Stan przenośnika {#misja-3}

**Cel:** wyrazić w kodzie, że przenośnik może być pusty.

**Zakres pracy:** w pliku `src/plant.cpp` uzupełnij funkcje `spawnItem` i `advance` dla
przenośnika, na którym jest najwyżej jedna paczka.

**Rezultat:** paczkę można postawić na pustym przenośniku, druga próba zostaje odrzucona, a kolejne
kroki przesuwają paczkę do rozjazdu.

**Sprawdź się:** `ctest --preset test -L misja-3`.

### Decyzja sortowania {#misja-4}

**Cel:** oddzielić decyzję sterownika od stanu fizycznego linii.

**Zakres pracy:** w pliku `src/controller.cpp` uzupełnij funkcje `classify` i
`toDiverterPosition`. W pliku `src/plant.cpp` rozszerz `advance` o wybór wyjścia i zdjęcie paczki
z linii.

**Rezultat:** paczki lekkie i ciężkie trafiają do różnych wyjść, a potem opuszczają przenośnik.

**Sprawdź się:** `ctest --preset test -L misja-4`, a potem jeszcze raz `-L misja-3`. Oba testy
mają przechodzić.

### Pętla sterowania {#misja-5}

**Cel:** połączyć stan, decyzję i działanie w powtarzany cykl sterowania.

**Zakres pracy:** w pliku `src/loop.cpp` uzupełnij funkcję `runTicks`. W każdym z kolejnych
kroków funkcja wyznacza decyzję i przesuwa paczkę.

**Rezultat:** po serii kroków paczka dociera do właściwego wyjścia, a kolejny krok usuwa ją z
systemu.

**Sprawdź się:** `ctest --preset test -L misja-5`.

### Pierwszy przebieg {#misja-6}

**Cel:** zobaczyć działanie własnego kodu na konsoli.

**Zakres pracy:** w pliku `apps/simulator_cli/main.cpp` napisz funkcję `main()`. Program stawia
jedną paczkę na przenośniku, w pętli wykonuje kroki sterowania i po każdym kroku wypisuje stan
paczki.

**Rezultat:** program wypisuje sensowną sekwencję stref zakończoną wyjściem odpowiednim do masy
paczki, a potem informację, że przenośnik jest pusty.

**Sprawdź się:** `ctest --preset test -L misja-6` sprawdza tylko, czy program uruchamia się i
kończy bez błędu. Wynik przeczytaj sam po uruchomieniu `simulator_cli`; instrukcja podaje
polecenie dla każdego systemu. Na koniec modułu uruchom cały zestaw testów: `ctest --preset test`.

## Oczekiwane rezultaty

- Środowisko z modułu 0 działa: projekt się buduje, a testy uruchamiasz z terminala.
- Testy `misja-1`…`misja-6` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy się
  wynikiem `100% tests passed`.
- `simulator_cli` pokazuje przebieg wygenerowany przez Twój kod.

## Wskazówki

- W tym module nie zmieniasz plików `CMakeLists.txt` ani testów. Testy tylko uruchamiasz.
- Po każdej misji uruchom jej test, a na koniec modułu cały zestaw testów.
- Każda misja kończy się sekcją „Częste błędy” i pytaniem do zastanowienia. Zajrzyj do nich, zanim
  poprosisz o pomoc.
- Zapisuj pracę w commitach po każdym sensownym etapie, zamiast odkładać cały moduł do jednego
  commita. Tak radzi plan pracy studenta.
- Kolejność dalszych modułów i sposób pracy w każdym z nich opisuje plan pracy studenta.
