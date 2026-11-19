---
title: "Czujniki"
summary: "Pięć misji modułu 6: czujnik obecności i czujnik wagi z obsługą usterek, klasyfikacja odrzucająca niewiarygodny odczyt, pamięć decyzji sterownika między tickami i Engine, który bez wiarygodnej klasyfikacji nie kieruje paczki do wyjścia."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność modułów i sposób pracy w każdym module"
  - repository: mechatronic-systems-programming
    path: course/module_06_sensors/00_wprowadzenie.md
    lang: pl
    label: "Moduł 6 — wprowadzenie: skąd startujesz i mapa misji"
  - repository: mechatronic-systems-programming
    ref: module-06-start
    lang: pl
    label: "Kod startowy modułu 6 (tag module-06-start)"
tasks:
  misja-20:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_06_sensors/01_czujnik_obecnosci.md
        lang: pl
        label: "Instrukcja: Misja 20 — Czujnik obecności"
  misja-21:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_06_sensors/02_czujnik_wagi.md
        lang: pl
        label: "Instrukcja: Misja 21 — Czujnik wagi"
  misja-22:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_06_sensors/03_klasyfikacja_odporna_na_awarie.md
        lang: pl
        label: "Instrukcja: Misja 22 — Klasyfikacja odporna na awarie"
  misja-23:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_06_sensors/04_pamiec_decyzji_sterownika.md
        lang: pl
        label: "Instrukcja: Misja 23 — Pamięć decyzji sterownika"
  misja-24:
    materials:
      - repository: mechatronic-systems-programming
        path: course/module_06_sensors/05_silnik_z_czujnikami.md
        lang: pl
        label: "Instrukcja: Misja 24 — Engine z czujnikami"
---
W tym zestawie sterownik przestaje korzystać bezpośrednio z masy paczki. Masę mierzy czujnik wagi,
obecność potwierdza czujnik obecności, a każdy z nich może zgłosić usterkę. Czujniki działają w
różnych strefach, więc sterownik po raz pierwszy musi zapamiętać informację między tickami. Pięć
zadań to misje 20–24 modułu 6 (w instrukcjach oznaczone też jako 6.1–6.5): misja N ma test
`misja-N`.

## Przygotowanie do zestawu

**Po module 5.** Zestaw kontynuuje [zestaw 5](estop.md). Środowisko z modułu 0 już działa.

**Punkt startowy: tag `module-06-start`.** Tak jak w poprzednich modułach zaczynasz od tagu
startowego, a nie od własnej gałęzi z modułu 5. Tag zawiera kompletny kod modułu 5, w tym zatrzask
przycisku awaryjnego i niezależną ścieżkę awaryjną, oraz puste szkielety czujników i pamięci
sterownika. Plan pracy studenta podaje polecenia:

```bash
git fetch --tags
git switch -c my-work module-06-start
```

Jeśli gałąź `my-work` już istnieje, nadaj nowej gałęzi inną nazwę.

Kod startowy kompiluje się od razu. Testy modułów 1–5 (`misja-1`…`misja-4`, `misja-6`…`misja-19`)
przechodzą od początku, a testy `misja-20`…`misja-24` zgłaszają błąd, dopóki nie uzupełnisz kodu.
Program `simulator_cli` na starcie wypisuje scenariusz zatrzymania awaryjnego z modułu 5.

**Dokumentacja na `main`, kod na tagu.** Instrukcji modułu 6 nie ma w tagu `module-06-start`:
czytasz je na gałęzi `main`. Odnośniki do kodu w instrukcjach otwierają pliki z tagu na GitHubie, a
u siebie edytujesz plik pod tą samą ścieżką. Nie zmieniasz plików `CMakeLists.txt` ani testów.
`Engine::step()` i `Plant::advance()` zmieniasz dopiero w ostatniej misji.

## Materiały

Instrukcje są po polsku; wersje angielskie mają w nazwie pliku `.en`. Każda misja ma tę samą
budowę: problem, nowe elementy C++, co jest już gotowe, co masz napisać, „Sprawdź się”, częste
błędy i pytanie do zastanowienia. Pojęcia z tego zestawu wyjaśnia
[rozdział 6 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#6-czujniki-i-jakość-danych).

## Zadania

### Misja 20: Czujnik obecności {#misja-20}

**Cel:** napisać klasę czujnika, która zapamiętuje wyłącznie wartości odczytane naprawdę w jej
strefie i odróżnia brak odczytu od odczytu „brak paczki”.

**Zakres pracy:** deklaracje i typy odczytu są gotowe. W pliku `src/presence_sensor.cpp` uzupełnij
`PresenceSensor::read` według reguły z instrukcji: osobno dla odczytu bez usterki w strefie
`PresenceCheck`, bez usterki poza nią, z usterką `Missing` i z usterką `Stale`. Odczyt bez usterki
poza strefą czujnika nie zmienia zapamiętanej wartości. Komentarz `// TODO` w tym pliku opisuje
starszą wersję reguły, w której zapamiętuje się każdy odczyt bez usterki. Test sprawdza regułę z
instrukcji na `main` i z regułą z komentarza nie przechodzi.

**Rezultat:** czujnik zwraca odczyt ze statusem, a przy usterce `Stale` powtarza ostatnią
wiarygodną wartość albo zgłasza `Missing`, jeśli takiej nie ma.

**Sprawdź się:** `ctest --preset test -L misja-20`. Oczekiwany wynik:
`100% tests passed, 0 tests failed out of 1`. Test sprawdza też, że odczyt dla paczki poza strefą
czujnika nie nadpisuje zapamiętanej wartości.

### Misja 21: Czujnik wagi {#misja-21}

**Cel:** zastosować ten sam wzorzec do pomiaru masy w strefie `Weighing`.

**Zakres pracy:** w pliku `src/weight_sensor.cpp` uzupełnij `WeightSensor::read`. Reguła jest
taka sama jak w misji 20, ale pamięć przechowuje masę, a zero oznacza brak pomiaru, a nie masę
paczki.

**Rezultat:** czujnik wagi zwraca masę tylko dla paczki na wadze i zapamiętuje wyłącznie
rzeczywiste pomiary.

**Sprawdź się:** `ctest --preset test -L misja-21`.

### Misja 22: Klasyfikacja odporna na awarie {#misja-22}

**Cel:** nie klasyfikować paczki na podstawie niewiarygodnego odczytu.

**Zakres pracy:** w pliku `src/controller.cpp` uzupełnij funkcję `decideClassification`. Odczyt ze
statusem innym niż `Ok` daje brak klasyfikacji, niezależnie od wartości; w przeciwnym razie
klasyfikacja pochodzi z `classify`.

**Rezultat:** klasyfikacja powstaje tylko z wiarygodnego pomiaru.

**Sprawdź się:** `ctest --preset test -L misja-22`. Test obejmuje odczyt `Stale` z wiarygodnie
wyglądającą masą, którego nie wolno użyć.

### Misja 23: Pamięć decyzji sterownika {#misja-23}

**Cel:** połączyć informacje z dwóch czujników, które nie są dostępne w tym samym ticku.

**Zakres pracy:** w pliku `src/controller_state.cpp` uzupełnij funkcję `updateControllerState`
według czterech kroków z instrukcji, w podanej kolejności: zerowanie stanu dla nowej paczki,
potwierdzenie obecności w `PresenceCheck` i zapis klasyfikacji w `Weighing` tylko po wcześniejszym
potwierdzeniu obecności.

**Rezultat:** stan sterownika zawiera potwierdzenie obecności i klasyfikację tylko wtedy, gdy oba
czujniki zadziałały poprawnie we właściwych strefach.

**Sprawdź się:** `ctest --preset test -L misja-23`. Test przeprowadza paczkę przez kolejne strefy i
obejmuje dwa przypadki usterek, w których klasyfikacja nie może powstać.

### Misja 24: `Engine` z czujnikami {#misja-24}

**Cel:** połączyć czujniki, klasyfikację i pamięć sterownika z `Engine` tak, żeby paczka bez
wiarygodnej klasyfikacji nie trafiła do żadnego wyjścia.

**Zakres pracy:** misja korzysta z wyników misji 20–23. W pliku `src/engine.cpp` uzupełnij
`injectFault` i `clearFault` oraz rozszerz `Engine::step()` o kroki 5–10 z instrukcji: odczyt obu
czujników w każdym ticku, aktualizację pamięci sterownika, warunek `routingReady` i polecenie
dywertera z zapamiętanej klasyfikacji. Instrukcja wyjaśnia też, że `Plant::advance` przyjmuje
trzeci parametr i że przy `routingReady` równym `false` paczka czeka w `Diverting`. W kodzie
startowym `src/plant.cpp` ten parametr jest jeszcze pomijany, więc gałąź `Diverting` w
`Plant::advance()` też trzeba uzupełnić. Lista „Co masz napisać” tego pliku nie wymienia, ale bez tej
zmiany test `misja-24` nie przechodzi. W pliku `apps/simulator_cli/main.cpp` przygotuj przebieg
z instrukcji: dwie paczki i usterkę `Stale` czujnika wagi między nimi, z wypisaniem odczytów
czujników.

**Rezultat:** paczka bez wiarygodnej klasyfikacji zatrzymuje się w `Diverting`. W przebiegu z
instrukcji czujnik wagi powtarza masę pierwszej paczki ze statusem `Stale`, a druga paczka czeka w
`Diverting`.

**Sprawdź się:** `ctest --preset test -L misja-24` sprawdza `Engine`. Przebiegu w `main()` nie
sprawdza żaden test. Pełny `ctest --preset test` przechodzi w całości, zanim zmienisz `main()`.
Zbuduj i uruchom program poleceniami z instrukcji (`cmake --build --preset dev`, a potem
`./build/dev/apps/simulator_cli/simulator_cli`; wariant dla Windows podaje instrukcja misji 6) i
porównaj wynik z przykładowym przebiegiem z instrukcji. Na koniec modułu uruchom
`ctest --preset test`: według instrukcji przechodzą wszystkie testy od `misja-1` do `misja-4` oraz
od `misja-6` do `misja-24`.

## Oczekiwane rezultaty

- Testy `misja-20`…`misja-24` przechodzą, a pełny `ctest --preset test` na Twojej gałęzi kończy się
  wynikiem `100% tests passed`.
- `simulator_cli` pokazuje odczyty czujników i paczkę zatrzymaną w `Diverting`, gdy odczyt wagi nie
  jest wiarygodny.
- Twoja praca jest zapisana w commitach na własnej gałęzi utworzonej z `module-06-start`.

## Wskazówki

- Brak klasyfikacji nie może oznaczać polecenia `HoldStraight`: instrukcja misji 24 wyjaśnia, dlaczego
  paczka pojechałaby wtedy dalej.
- Usterka wprowadzona przez `injectFault` jest trwała i trwa do wywołania `clearFault`.
- Plan pracy studenta uznaje dokumentację na `main` za wersję aktualną. W misji 20 komentarz
  `// TODO` w kodzie tagu się z nią nie zgadza, a test sprawdza regułę z instrukcji.
- Każda misja kończy się sekcją „Częste błędy” i pytaniem do zastanowienia. Zajrzyj do nich, zanim
  poprosisz o pomoc.
- Zapisuj pracę w commitach po każdym sensownym etapie. Tak radzi plan pracy studenta.
