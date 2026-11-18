---
title: "Kod to jeszcze nie projekt"
summary: "Od jednoplikowego programu do małego projektu: moduły i manifest, testy jednostkowe, błąd naprawiony od testu, formatowanie i analiza statyczna oraz jedno polecenie sprawdzające całość. Laboratoria 06–10."
status: published
materials:
  - repository: software-engineering-in-practice
    path: README.pl.md
    lang: pl
    label: "Opis kursu: akty, ścieżki językowe i wymagane wersje narzędzi"
  - repository: software-engineering-in-practice
    path: examples/restaurant-bill/
    lang: en
    label: "Projekt startowy Aktu II: Python, Go, Java"
  - repository: software-engineering-in-practice
    path: docs/setup/troubleshooting.pl.md
    lang: pl
    label: "Gdy coś pójdzie nie tak przy konfiguracji"
tasks:
  lab-06:
    materials:
      - repository: software-engineering-in-practice
        path: labs/06-from-script-to-project/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 06 — Od skryptu do projektu"
  lab-07:
    materials:
      - repository: software-engineering-in-practice
        path: labs/07-automated-tests/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 07 — Skąd wiemy, że to działa?"
  lab-08:
    materials:
      - repository: software-engineering-in-practice
        path: labs/08-bug-report/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 08 — Nadchodzi zgłoszenie błędu"
  lab-09:
    materials:
      - repository: software-engineering-in-practice
        path: labs/09-automated-checks/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 09 — Maszyny mogą sprawdzać nudne rzeczy"
  lab-10:
    materials:
      - repository: software-engineering-in-practice
        path: labs/10-one-way-to-check/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 10 — Jeden oczywisty sposób sprawdzania projektu"
---
## Cel

Druga część kursu zamienia działający program w projekt, który da się bezpiecznie zmieniać. Przez
pięć laboratoriów rozwijasz jeden program liczący rachunek w restauracji: dzielisz go na moduły,
opisujesz manifestem, sprawdzasz testami, naprawiasz zgłoszony błąd, dodajesz formatowanie i analizę
statyczną, a na koniec łączysz wszystkie kontrole w jedno polecenie.

## Wymagania wstępne

- Ukończony [zestaw 1](i-am-a-developer.md): instrukcja laboratorium 06 zakłada ukończone
  laboratoria 01–04 i ścieżkę językową wybraną w laboratorium 05.
- Narzędzia tylko dla wybranej ścieżki, w wersjach z opisu kursu: Python 3.13 i `uv` 0.11.21; Go
  1.27; JDK 21. W ścieżce Java nie instalujesz osobno Gradle, bo projekty mają Gradle Wrapper
  (`./gradlew`). Wersje sprawdzisz poleceniem `./scripts/check-environment.sh` z katalogu głównego
  repozytorium.
- Pierwsze uruchomienie Gradle pobiera jego dystrybucję i zależności, a laboratorium 09 w ścieżce
  Java pobiera dwie wtyczki z Maven Central. Potrzebujesz wtedy połączenia z internetem.

## Ścieżka językowa

Kontynuujesz ścieżkę wybraną w laboratorium 05: Python, Go albo Java. Instrukcje dzielą się na
warianty dla każdego języka i czytasz tylko swój. Każda ścieżka jest kompletną drogą przez
laboratoria 06–10: rozwiązuje ten sam problem na tych samych danych i prowadzi do równoważnej
struktury projektu. Nie realizujesz zadań w trzech językach.

- **Python:** pracujesz w `examples/restaurant-bill/python/`, testy uruchamiasz poleceniem
  `uv run pytest`.
- **Go:** pracujesz w `examples/restaurant-bill/go/`, testy uruchamiasz poleceniem `go test ./...`.
- **Java:** pracujesz w `examples/restaurant-bill/java/`, testy uruchamiasz poleceniem
  `./gradlew test`.

## Materiały

Pełne instrukcje są w repozytorium kursu, po polsku i po angielsku. Kod projektów startowych jest po
angielsku. Każda instrukcja ma tę samą budowę: sytuacja, cele nauki, przygotowanie, zadanie,
kryteria akceptacji, weryfikacja, pytania do przemyślenia, podpowiedzi i zapowiedź kolejnego kroku.

## Zadania

### Od skryptu do projektu {#lab-06}

Program w `examples/restaurant-bill/` liczy rachunek, ale jedna funkcja albo jedno `main` robi pięć
różnych rzeczy. Zmiana jednej części wymaga przejrzenia całego programu.

**Cel:** rozdzielić odpowiedzialności programu na moduły (Python), pakiety (Go) albo klasy (Java),
oddzielić czyste funkcje obliczające od wyświetlania i opisać projekt manifestem: `pyproject.toml`,
`go.mod` albo `build.gradle`.

**Zakres pracy:** zapisz wynik oryginalnego programu jako punkt odniesienia. Utwórz pakiet
`billing` z pięcioma funkcjami albo metodami o nazwach i sygnaturach podanych w instrukcji oraz
moduł, który wyświetla rachunek, wywołując obliczenie tylko raz. Refaktoryzacja ma zachować obecne
działanie programu, także jego błąd w liczeniu podatku, który naprawisz w laboratorium 08. Na
koniec porównaj nowy wynik z punktem odniesienia. W ścieżce Python usuwasz potem `bill.py`, w Go
tworzysz `go.mod`, a w Javie dodajesz do `build.gradle` zależności JUnit 5 na potrzeby laboratorium 07.

**Rezultat:** program po refaktoryzacji wyświetla rachunek identyczny z oryginałem; struktura i
manifest projektu odpowiadają kryteriom akceptacji dla Twojej ścieżki.

**Sprawdź się:** sekcja „Weryfikacja” ma wariant dla każdej ścieżki. Porównuje nowy wynik z punktem
odniesienia poleceniem `diff` i sprawdza ślad zmiany w projekcie: brak `bill.py`, obecność `go.mod`
albo przechodzące `./gradlew test`, które przy braku testów kończy się sukcesem. W ścieżce Java
punkt odniesienia zapisany w kroku 1 bez opcji `--quiet` zawiera komunikaty Gradle, a weryfikacja
porównuje go z wynikiem uruchomionym z `--quiet`. Dlatego `diff` z sekcji „Weryfikacja” może pokazać
różnicę i nie wypisać `IDENTICAL` nawet przy poprawnej refaktoryzacji, bo porównywane wyniki różnią
się komunikatami Gradle. Jak mówi krok 7 instrukcji, komunikaty Gradle nie
są częścią wyniku programu: porównuj sam rachunek, od wiersza `Receipt`, albo od początku zapisuj
oba wyniki z `--quiet`.

### Skąd wiemy, że to działa? {#lab-07}

Refaktoryzacja została sprawdzona ręcznie poleceniem `diff`. Powtarzanie tego po każdej zmianie
byłoby uciążliwe, więc czas zautomatyzować kontrolę.

**Cel:** napisać testy jednostkowe według schematu Arrange-Act-Assert, dobierać przypadki obejmujące
różne zachowania funkcji i odczytać wynik zestawu testów narzędziami swojego języka.

**Zakres pracy:** napisz co najmniej sześć testów dla przypadków wymienionych w instrukcji: suma
częściowa, rabat poniżej i od progu 50, podatek, napiwek oraz pełny rachunek małego zamówienia o
kwocie `46.74`. Plik testów tworzysz w miejscu wskazanym dla swojej ścieżki, a instrukcja podaje
przykład pierwszego testu w każdym języku. W Go możesz połączyć przypadki rabatu w test tabelaryczny.

**Rezultat:** zestaw co najmniej sześciu przechodzących testów, bez dodatkowych bibliotek ponad
standardowe narzędzie Twojego języka.

**Sprawdź się:** `uv run pytest -v`, `go test ./... -v` albo `./gradlew test` w katalogu swojej
ścieżki; wszystkie testy przechodzą. Polecenia sprawdzają, czy testy przechodzą, ale nie oceniają,
czy przypadki naprawdę obejmują różne zachowania funkcji. Do tego służą pytania z sekcji „Zastanów
się”.

### Nadchodzi zgłoszenie błędu {#lab-08}

Klient zgłasza, że przy zamówieniu za $60 podatek jest liczony od kwoty sprzed rabatu. Wszystkie
testy przechodzą, a klient ma rację.

**Cel:** zamienić zgłoszenie błędu w test, który najpierw nie przechodzi, i naprawić błąd najmniejszą
możliwą zmianą.

**Zakres pracy:** policz, jaki podatek powinien być dla zamówienia za $60 z napiwkiem 15%. Dodaj
test o nazwie podanej w instrukcji dla swojej ścieżki, który sprawdza `tax == 4.32` i
`total == 66.42`, i potwierdź, że nie przechodzi. Potem przekaż do obliczenia podatku kwotę po
rabacie zamiast sumy częściowej i uruchom cały zestaw ponownie.

**Rezultat:** nowy test przechodzi razem z testami z laboratorium 07; poprawka zmienia tylko sposób
liczenia podatku wewnątrz obliczenia całego rachunku.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia zestaw testów w Twojej ścieżce, a w ścieżce Python
wyświetla też rachunek dla zamówienia za $60 z wartościami `'tax': 4.32` i `'total': 66.42`. To, że
nowy test najpierw nie przechodził, widzisz sam przy kroku 3; końcowe polecenia pokazują już tylko
stan po poprawce.

### Maszyny mogą sprawdzać nudne rzeczy {#lab-09}

Code review poświęciło dziesięć minut na wcięcia i nieużywany import. Takie spory może rozstrzygnąć
narzędzie.

**Cel:** odróżnić narzędzie formatujące, analizator statyczny i testy oraz skonfigurować narzędzia
swojej ścieżki w manifeście projektu.

**Zakres pracy:** w ścieżce Python dodajesz `ruff` jako zależność deweloperską i sekcję
`[tool.ruff]`, a potem uruchamiasz `ruff format --check` i `ruff check`. W ścieżce Go używasz
`gofmt` i `go vet`, które są częścią toolchaina. W ścieżce Java dodajesz wtyczki Spotless z Google
Java Format i PMD z własnym zestawem trzech reguł opisanym w instrukcji. W każdej ścieżce celowo
wprowadzasz problem, który narzędzie ma wykryć, czytasz komunikat i cofasz zmianę, a na koniec
naprawiasz zgłoszone problemy.

**Rezultat:** narzędzia Twojej ścieżki nie zgłaszają problemów, a testy z laboratoriów 07–08 nadal
przechodzą.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia kolejno formatowanie, analizę i testy:
`ruff format --check .`, `ruff check .` i `pytest`; `gofmt -l .`, `go vet ./...` i `go test ./...`;
`./gradlew spotlessCheck`, `./gradlew pmdMain` i `./gradlew test`. W ścieżce Go `gofmt -l .` tylko
wyświetla nazwy niesformatowanych plików i zawsze kończy się kodem `0`, więc sukces oznacza tu
pusty wynik. Instrukcja wraca do tego w laboratorium 10.

### Jeden oczywisty sposób sprawdzania projektu {#lab-10}

Nowa osoba w projekcie pyta, w jakiej kolejności uruchamiać kontrole. Nie powinna musieć tego
zapamiętywać.

**Cel:** opakować sekwencję poleceń w krótkie, czytelne skrypty, które działają z dowolnego
katalogu.

**Zakres pracy:** w katalogu `scripts/` projektu utwórz cztery skrypty: `test.sh`, `check.sh`
(formatowanie, analiza i testy w tej kolejności), `format.sh` i `run.sh`. Instrukcja podaje
gotowy `test.sh` i opisuje pozostałe dla każdej ścieżki. W Go `check.sh` sam sprawdza, czy wynik
`gofmt -l .` jest pusty. Skrypty oznaczasz jako wykonywalne, a instrukcja wyjaśnia, dlaczego na
Windowsie w Git Bash uruchamiasz je przez `bash scripts/<nazwa>.sh`.

**Rezultat:** cztery skrypty, które kończą się sukcesem wywołane z innego katalogu; `check.sh`
kończy się błędem, gdy formatowanie, analiza albo testy nie przechodzą.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia `test.sh`, `check.sh` i `run.sh` z katalogu
domowego. To, że `check.sh` przerywa działanie przy problemie, sprawdzisz, wprowadzając celowo
błąd formatowania; polecenia weryfikacji pokazują tylko przypadek, w którym wszystko przechodzi.
Kryterium, że każdy skrypt da się przeczytać w mniej niż trzydzieści sekund, oceniasz sam.

## Oczekiwane rezultaty

Każde laboratorium kończy się wynikiem opisanym w sekcji „Kryteria akceptacji” jego instrukcji. Po
całym zestawie projekt `examples/restaurant-bill/` w Twojej ścieżce:

- jest podzielony na pakiet `billing` i punkt wejścia oraz opisany manifestem;
- ma zestaw testów z przypadkiem zgłoszonego błędu i poprawkę liczenia podatku;
- przechodzi formatowanie i analizę statyczną swojej ścieżki;
- ma skrypty `scripts/test.sh`, `check.sh`, `format.sh` i `run.sh`.

## Wskazówki

- Każda instrukcja ma sekcję „Jeśli utkniesz” z podpowiedziami: od ogólnych do coraz bardziej
  szczegółowych, osobno dla każdej ścieżki.
- Laboratoria tworzą łańcuch: każde zaczyna się od stanu projektu po poprzednim. Instrukcje
  przypominają, żeby po każdym laboratorium zapisać zmiany w commicie i wysłać je na GitHuba; od
  laboratorium 16 kurs zakłada czyste drzewo robocze.
- Instrukcja laboratorium 06 opisuje, co zrobić, jeśli projekt w Pythonie był już rozpoczęty w
  starszej lokalizacji, bez podkatalogu `python/`. Ostrzega też przed `git reset --hard` i
  `git clean`, które mogą usunąć pracę jeszcze niewysłaną na GitHuba.
