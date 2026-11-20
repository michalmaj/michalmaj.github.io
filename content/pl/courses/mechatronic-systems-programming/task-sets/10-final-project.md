---
title: "Projekt końcowy"
summary: "Krótkie ćwiczenie z pierwszym własnym testem, a potem projekt końcowy: bufor wejściowy przed strefą Infeed, zaprojektowany samodzielnie w istniejącym symulatorze, z własnymi testami i scenariuszem odbiorczym."
status: published
materials:
  - repository: mechatronic-systems-programming
    path: docs/roadmap.md
    lang: pl
    label: "Plan pracy studenta: kolejność etapów po module 9"
  - repository: mechatronic-systems-programming
    path: final_project/README.md
    lang: pl
    label: "Projekt końcowy: od czego zacząć"
  - repository: mechatronic-systems-programming
    ref: final-project-start-v3
    lang: pl
    label: "Kod startowy ćwiczenia i projektu (tag final-project-start-v3)"
tasks:
  pierwszy-wlasny-test:
    materials:
      - repository: mechatronic-systems-programming
        path: final_project/00_project_kickoff.md
        lang: pl
        label: "Instrukcja: Przed projektem — pierwszy własny test"
  bufor-wejsciowy:
    materials:
      - repository: mechatronic-systems-programming
        path: final_project/01_final_project_brief.md
        lang: pl
        label: "Brief: Projekt końcowy — bufor wejściowy"
---
Ostatni zestaw przedmiotu ma dwa etapy. Najpierw krótkie ćwiczenie, w którym piszesz pierwszy
własny test, a potem projekt końcowy: bufor wejściowy, w którym paczka czeka na zwolnienie strefy
`Infeed`. Projekt rozwija ten sam symulator, nad którym pracujesz od modułu 1. Plan pracy studenta
umieszcza oba etapy po module 9 i rozmowie sprawdzającej, w tej kolejności. Projekt nie jest
podzielony na misje: brief opisuje wymagania, decyzje projektowe i kryteria akceptacji dla całości.

## Przygotowanie do zestawu

**Po module 9.** Zestaw kontynuuje [zestaw 9](scripted-scenarios.md). Środowisko z modułu 0 już
działa.

**Punkt startowy obu etapów: tag `final-project-start-v3`.** Plan pracy studenta podaje polecenia,
którymi tworzysz z niego własną gałąź:

```bash
git fetch --tags
git switch -c my-final-project final-project-start-v3
```

Na kodzie z tego taga wykonujesz również ćwiczenie z pierwszym własnym testem. Kod w tagu działa
tak samo jak ukończony moduł 9. Na starcie przechodzą wszystkie 30 testów, a `simulator_cli`
wypisuje oba scenariusze z modułu 9. Tag nie zawiera szkieletu projektu ani komentarzy `// TODO`:
opis projektu mówi wprost, że część architektury projektujesz samodzielnie.

**Dokumentacja na `main`, kod na tagu.** Instrukcję ćwiczenia i brief projektu czytasz na gałęzi
`main`. Tag zawiera ich wcześniejszą kopię w katalogu `final_project/`; wymagania i polecenia są w
niej te same, różni się redakcja tekstu. Kodu z gałęzi `main` nie używasz w żadnym z etapów: to
osobna wersja symulatora, w której `decideClassification` ma inną sygnaturę niż funkcja opisana w
ćwiczeniu.

## Materiały

Materiały są po polsku; wersje angielskie mają w nazwie pliku `.en`. Sposób pisania testu wyjaśnia
[rozdział 10 podręcznika kursu](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#10-jak-czytać-i-pisać-test),
a pracę nad nowym wymaganiem w istniejącym systemie porządkuje
[rozdział 11](https://github.com/michalmaj/mechatronic-systems-programming/blob/main/docs/handbook.md#11-projekt-końcowy-jak-podejść-do-nowego-wymagania).

## Zadania

### Pierwszy własny test {#pierwszy-wlasny-test}

**Cel:** napisać od zera test znanej funkcji `decideClassification` i sprawdzić, że wykrywa błąd, a
nie tylko przechodzi. Instrukcja nazywa to krótkim ćwiczeniem przed projektem, a nie modułem 10.

**Zakres pracy:** w nowym pliku testu (instrukcja proponuje `tests/support_your_first_test.cpp`,
nazwa jest dowolna) sprawdź przypadki wymienione w instrukcji: poprawny odczyt w zakresie Light,
poprawny odczyt w zakresie Heavy razem z progiem oraz odczyty `Missing` i `Stale` z masą, która
dałaby Heavy. Strukturę pliku wzorujesz na `tests/controller_test.cpp`, a test rejestrujesz trzema
poleceniami CMake podanymi w instrukcji, dopisanymi na końcu `tests/CMakeLists.txt`. Funkcja i pliki
opisane w instrukcji odpowiadają kodowi z taga `final-project-start-v3`. Wzmianka o teście
`engine_routing_deadline_test` dotyczy kodu na `main`; w tagu takiego testu nie ma, a zasada
rejestracji jest ta sama.

**Rezultat:** test przechodzi na poprawnym kodzie i nie przechodzi, gdy celowo usuniesz z
`decideClassification` sprawdzenie statusu. Według instrukcji plik ma co najmniej dwa różne
przypadki testowe (`psmCheck`), a co najmniej jeden z nich wykrywa ten błąd.

**Sprawdź się:** polecenia z instrukcji:

```bash
cmake --preset dev
cmake --build --preset dev
ctest --test-dir build/dev -R support_your_first_test --output-on-failure
```

Potem wykonaj krok 6 instrukcji: wprowadź błąd, przebuduj i uruchom test ponownie, a na koniec cofnij
zmianę (`git restore src/controller.cpp` albo ręcznie) i sprawdź, że test znowu przechodzi.

### Projekt: bufor wejściowy {#bufor-wejsciowy}

**Cel:** dodać przed strefą `Infeed` bufor, w którym paczka czeka na zwolnienie wejścia, zamiast
przerywać scenariusz. Rozszerzasz istniejący kod; brief wyklucza drugą, niezależną implementację.

**Co jest ustalone:** brief wymienia wymagania obowiązkowe i dziewięć niezmienników. W skrócie:

- bufor jest trwałą częścią stanu systemu i działa tak samo przy sterowaniu bezpośrednim i przez
  `Scenario`;
- kolejność FIFO i pojemność chroni typ z prywatnym kontenerem;
- `Engine::spawnItem()` działa jak dotąd, a osobny interfejs przyjmowania paczek (brief sugeruje
  nazwę `acceptArrival`) korzysta z bufora i zastępuje `spawnItem()` w `runScenario()`;
- pojemność jest ograniczona, co najmniej 2, a przepełnienie jest zgłaszane jawnie; brief określa
  też, w którym momencie ticku ocenia się wolne miejsce;
- przejście z bufora do `Infeed` następuje po przejściu `Infeed` → `PresenceCheck` i tylko przy
  pracującej taśmie;
- aktywny `ItemId` jest unikalny w buforze i we wszystkich strefach, a `TickResult` dostaje pola
  `bufferedCount` i `bufferHeadItemId`;
- reguła jednej nowej paczki na tick w `isValidScenario()`, powtarzalność oraz działanie `EStopped`
  i `Fault` się nie zmieniają.

Dokładne brzmienie wymagań i niezmienników jest w briefie; tam też sprawdzaj szczegóły.

**Co projektujesz samodzielnie:** właściciela bufora (`Plant` albo `Engine`), pojemność powyżej
minimum i sposób jej ustawienia, nazwę nowej funkcji, wewnętrzną reprezentację bufora oraz podział
nowych funkcji pomocniczych. Przed implementacją zapisz krótkie uzasadnienie dwóch decyzji: gdzie
jest bufor i jak dobierasz pojemność. Brief podaje pytania, które warto przy tym rozważyć.

**Rezultat:** paczki, które docierają przy zajętym `Infeed`, czekają w buforze i wchodzą na linię w
kolejności przybycia. Przepełnienie jest widoczne, a ślad pokazuje liczbę paczek w buforze i
pierwszą z nich. Scenariusz odbiorczy z briefu przechodzi przy pojemności 2, a projekt ma
uruchamialny scenariusz demonstracyjny.

**Własne testy:** brief wymaga co najmniej 3 małych testów z co najmniej 3 różnych kategorii z jego
listy: FIFO, dodanie paczki przy zajętym, ale niepełnym buforze, przepełnienie z uwzględnieniem
momentu oceny, unikalność aktywnego `ItemId`, zachowanie podczas zatrzymania, E-Stop i `Fault` oraz
powtarzalność. Trzy warianty tego samego przypadku nie wystarczą. Każdy test sprawdź metodą z
pierwszego ćwiczenia: celowo zepsuj odpowiedni fragment kodu i upewnij się, że test go wykrywa.

**Scenariusz odbiorczy:** zapisujesz go samodzielnie jako `Scenario`, według sześciu kroków z
briefu: start linii i niemal natychmiast E-Stop, dwie paczki w trakcie zatrzymania, zwolnienie,
reset i ponowny start, trzecia paczka po wznowieniu, wszystkie trzy we właściwych wyjściach i w
kolejności przybycia. Scenariusz ma działać przy pojemności 2 i dawać ten sam ślad przy dwóch
uruchomieniach.

**Sprawdź się:** dostarczone testy nie sprawdzają bufora. Na kodzie startowym, czyli bez żadnego
bufora, pełny `ctest --preset test` przechodzi w całości, a bufor, który narusza FIFO, wygląda dla
dostarczonych testów tak samo jak poprawny. Jeden z dostarczonych testów sprawdza zachowanie, które
projekt celowo zmienia; postępowanie z nim opisuje sekcja
[Zmiana wymagań a istniejące testy](#zmiana-wymagan-a-istniejace-testy). Wymagania projektu
sprawdzasz więc przede wszystkim:

- własnymi testami z co najmniej trzech kategorii, z których każdy wykrywa celowo wprowadzony błąd;
- scenariuszem odbiorczym: w śladzie sprawdź kolejność wejścia paczek do `Infeed`, wyjścia zgodne z
  masą, `bufferedCount` i `bufferHeadItemId` oraz to, że żadna paczka nie znika;
- dwoma uruchomieniami tego samego scenariusza;
- pełnym `ctest --preset test` po zakończeniu pracy;
- przeglądem własnego kodu względem wymagań i niezmienników z briefu, zwłaszcza tych, których nie
  obejmą Twoje testy.

## Zmiana wymagań a istniejące testy

Projekt końcowy zmienia część zachowania symulatora z modułu 9. Dostarczony test
`run_scenario_test` (etykieta `misja-34`) nadal zawiera oczekiwania odpowiadające poprzedniej wersji
systemu.

Dlatego poprawna implementacja bufora wejściowego zgodna z briefem może spowodować niepowodzenie
tego testu.

W ramach projektu możesz dostosować te sprawdzenia, które dotyczą zachowania świadomie zmienionego
przez nowe wymagania. Uzasadnij każdą taką zmianę w opisie decyzji projektowych, wskazując jej
związek z briefem.

Nie usuwaj ani nie osłabiaj testów tylko po to, aby uzyskać pozytywny wynik. Zachowaj sprawdzenia
zachowań, które nie zostały zmienione przez wymagania projektu.

Uzupełnij zestaw testów o własne sprawdzenia wymagane w briefie. Po zakończeniu pracy uruchom pełny
`ctest` oraz wykonaj scenariusz odbiorczy. Sam pozytywny wynik dostarczonych testów nie potwierdza
poprawności nowego bufora.

## Oczekiwane rezultaty

- Ćwiczenie: test `support_your_first_test` (albo pod inną nazwą) przechodzi i wykrywa celowo
  wprowadzony błąd.
- Projekt: bufor spełniający wymagania i niezmienniki z briefu, co najmniej 3 własne testy z 3
  kategorii, scenariusz odbiorczy przy pojemności 2, scenariusz demonstracyjny i krótkie uzasadnienie
  decyzji projektowych, obejmujące także ewentualne zmiany w dostarczonych testach.
- Praca zapisana w commitach na własnej gałęzi utworzonej z `final-project-start-v3`.

## Pozostała część briefu

Brief opisuje także pracę w Git i oddanie projektu, rozmowę podsumowującą oraz rozszerzenia
opcjonalne; te części czytasz bezpośrednio w briefie.

## Wskazówki

- Zacznij od zapisania zasad, a nie od kodu. Rozdział 11 podręcznika prowadzi przez to w ośmiu
  krokach.
- Para `{EmergencyStopReleased, Reset}` w jednym ticku nie skraca dwuetapowego powrotu po
  zatrzymaniu awaryjnym (misja 34). Uwzględnij to, układając polecenia operatora w scenariuszu
  odbiorczym.
- Przyjmowanie paczek do bufora podczas `EStopped` i `Fault` to uproszczenie przyjęte w zadaniu.
  Symulator pozostaje uproszczonym modelem dydaktycznym, a nie układem bezpieczeństwa rzeczywistej
  maszyny.
- Zapisuj pracę w commitach po kolejnych etapach; brief podaje przykładowy podział.
