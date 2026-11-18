---
title: "Nie pracujesz w pojedynkę"
summary: "Gałęzie dla pracy równoległej, konflikt scalania rozwiązany z zachowaniem obu zmian, pull request z przeglądem kodu w Twoim forku, CI w GitHub Actions i definicja ukończenia. Laboratoria 16–20."
status: published
materials:
  - repository: software-engineering-in-practice
    path: README.pl.md
    lang: pl
    label: "Opis kursu: akty, ścieżki językowe i wymagane wersje narzędzi"
  - repository: software-engineering-in-practice
    path: examples/team-inventory/
    lang: en
    label: "Projekt Aktu IV: magazyn kuchenny w Pythonie, Go i Javie"
  - repository: software-engineering-in-practice
    path: docs/setup/troubleshooting.pl.md
    lang: pl
    label: "Gdy coś pójdzie nie tak przy konfiguracji"
tasks:
  lab-16:
    materials:
      - repository: software-engineering-in-practice
        path: labs/16-parallel-branches/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 16 — Gałęzie istnieją, bo praca toczy się równolegle"
  lab-17:
    materials:
      - repository: software-engineering-in-practice
        path: labs/17-merge-conflict/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 17 — Konflikt scalania"
  lab-18:
    materials:
      - repository: software-engineering-in-practice
        path: labs/18-pull-requests-and-review/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 18 — Pull request i przegląd kodu"
  lab-19:
    materials:
      - repository: software-engineering-in-practice
        path: labs/19-repository-checks-itself/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 19 — Repozytorium powinno sprawdzać samo siebie"
  lab-20:
    materials:
      - repository: software-engineering-in-practice
        path: labs/20-definition-of-done/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 20 — Co oznacza „zrobione”?"
---
## Cel

Czwarta część kursu przenosi pracę z jednego komputera do zespołu. Pracujesz na gałęziach,
scalasz je i rozwiązujesz konflikt, otwierasz pull request i przeglądasz zmianę według listy
kontrolnej, uruchamiasz CI w GitHub Actions, a na koniec zapisujesz, co w projekcie znaczy
„zrobione”.

## Wymagania wstępne

- Ukończony [zestaw 3](software-must-survive-change.md) w wybranej ścieżce: instrukcja
  laboratorium 16 zakłada ukończone laboratoria 06–15. Kolejne laboratoria tego aktu wymagają
  poprzednich, a laboratorium 20 — laboratoriów 06–19.
- Czysta gałąź `main` w Twoim repozytorium: laboratorium 16 zaczyna się od sprawdzenia
  `git status --short`, a instrukcja laboratorium 15 kończyła Akt III właśnie tym sprawdzeniem.
- Własny fork repozytorium kursu na GitHubie, utworzony w Akcie I. Laboratoria 18 i 19 wysyłają do
  niego gałęzie i otwierają w nim pull requesty.
- Te same narzędzia co w poprzednich aktach, tylko dla wybranej ścieżki. GitHub CLI (`gh`) nie jest
  wymagany; instrukcja laboratorium 18 opisuje go jako opcję dla osób, które już go mają.

## Ścieżka językowa

Kontynuujesz ścieżkę wybraną w laboratorium 05. Instrukcje laboratoriów 16–19 dzielą się na
warianty i czytasz tylko swój. Laboratorium 20 nie zależy od języka i nie wymaga pisania kodu.

- **Python:** pracujesz w `examples/team-inventory/python/`, testy uruchamiasz poleceniem
  `uv run pytest`.
- **Go:** pracujesz w `examples/team-inventory/go/`, testy uruchamiasz poleceniem `go test ./...`.
- **Java:** pracujesz w `examples/team-inventory/java/`, testy uruchamiasz poleceniem
  `./gradlew test`.

Polecenia Gita w tym akcie działają na całym repozytorium kursu, nie na katalogu jednego języka:
gałąź utworzona w laboratorium 16 należy do całego repozytorium, nawet jeśli zmieniasz pliki tylko
jednej ścieżki.

## Twój fork i praca w parze

- **Gdzie trafia praca.** Gałęzie, pull requesty i przepływy CI z tego aktu tworzysz w swoim
  forku. Instrukcja laboratorium 18 mówi wprost, żeby nigdy nie kierować pull requesta do
  wspólnego repozytorium kursu: celem jest zawsze `main` Twojego forka. Przed utworzeniem pull
  requesta sprawdzasz repozytorium i gałąź bazową, bo GitHub może zaproponować repozytorium kursu.
- **Dwie osoby w laboratoriach 16–17.** Wykonujesz pracę obu osób samodzielnie, po jednej gałęzi naraz.
- **Przegląd w laboratorium 18.** Instrukcja przewiduje dwa warianty. Jeśli prowadzący przydzielił
  Ci osobę do pracy w parze, wymieniacie się pull requestami i przeglądacie je nawzajem. Bez takiego
  przydziału przeglądasz własną zmianę tak, jakby autor był Ci obcy, i wynik zapisujesz w notatce;
  instrukcja wyjaśnia, że GitHub nie pozwala zatwierdzić własnego pull requesta.

## Materiały

Pełne instrukcje są w repozytorium kursu, po polsku i po angielsku. Kod projektu jest po angielsku.
Każda instrukcja ma tę samą budowę: sytuacja, cele nauki, przygotowanie, zadanie, kryteria
akceptacji, weryfikacja, pytania do przemyślenia, podpowiedzi i zapowiedź kolejnego kroku.

## Zadania

### Gałęzie istnieją, bo praca toczy się równolegle {#lab-16}

Dwie osoby mają dziś dodać ostrzeżenia do skryptu magazynu kuchennego, bez czekania na siebie.

**Cel:** tworzyć gałęzie w konkretnym punkcie historii, przełączać się między nimi i odczytać
rozbieżną historię w `git log --all --graph`.

**Zakres pracy:** z czystego `main` utwórz gałąź `feature/low-stock-warning` i dodaj na niej
funkcję ostrzeżenia o niskim stanie, jej wywołanie w funkcji podsumowania i test. Potem wróć na
`main`, bez scalania, utwórz gałąź `feature/expiry-warning` i dodaj w tych samych miejscach
ostrzeżenie o terminie ważności z testem. Instrukcja podaje dokładny kod i miejsca wstawienia dla
każdej ścieżki; ich zachowanie jest potrzebne, żeby laboratorium 17 zadziałało zgodnie z opisem.

**Rezultat:** dwie gałęzie, każda z jednym commitem utworzonym na tym samym commicie z `main`;
na każdej przechodzą testy, a żadna nie zawiera funkcji z drugiej.

**Sprawdź się:** sekcja „Weryfikacja” wyświetla gałęzie i historię, a potem uruchamia testy na
obu gałęziach. Testy pokazują, że kod na każdej gałęzi działa. To, że obie gałęzie wychodzą z
tego samego commitu i nie zawierają swojej pracy nawzajem, odczytujesz samodzielnie z wyniku `git log`.

### Konflikt scalania {#lab-17}

Obie funkcje są gotowe i mają trafić do `main`, jedna po drugiej.

**Cel:** scalić gałąź bez konfliktu, przeczytać markery konfliktu i rozwiązać go, łącząc obie
zmiany zamiast wybierać na oślep jedną stronę.

**Zakres pracy:** na `main` scal najpierw `feature/low-stock-warning`, co powinno skończyć się bez
konfliktu, i uruchom testy. Potem scal `feature/expiry-warning`, co wywoła konflikt w pliku
źródłowym i w pliku testów. Instrukcja opisuje kształt konfliktu osobno dla każdej ścieżki:
w Pythonie po dwa bloki w obu plikach, w Go i Javie dwa bloki w pliku źródłowym i jeden w pliku
testów. Rozwiąż konflikt, zachowując obie zmiany i usuwając wszystkie markery, uruchom testy i
dokończ scalanie.

**Rezultat:** w obu plikach nie ma markerów konfliktu, obie funkcje są zdefiniowane i używane w
funkcji podsumowania, przechodzą wszystkie 3 testy, a na `main` jest commit scalający.

**Sprawdź się:** sekcja „Weryfikacja” szuka markerów konfliktu w obu plikach, uruchamia testy i
wyświetla historię. Blok weryfikacji zawiera `exit 1`, który przy znalezionych markerach przerywa
działanie z błędem; wklejony bezpośrednio do terminala zamknie wtedy samą sesję terminala. Przy
rozwiązywaniu konfliktu w Go i Javie zwróć uwagę na wiersze zamykające, które Git scalił poza
markerami: samo sklejenie obu stron bloku nie da poprawnego kodu, a błąd pokażą testy.

### Pull request i przegląd kodu {#lab-18}

Dotąd każda zmiana trafiała na `main` po samodzielnym scaleniu. Przed scaleniem kod powinien
zobaczyć ktoś jeszcze, choćby Ty po pewnym czasie.

**Cel:** otworzyć pull request z opisem wyjaśniającym, dlaczego zmiana powstała, przejrzeć
różnice według listy kontrolnej i zakończyć przegląd konkretnym wynikiem.

**Zakres pracy:** na gałęzi `feature/reorder-report` dodaj funkcję raportu zamówień, która
korzysta z funkcji niskiego stanu z laboratorium 16, z testem. Wyślij gałąź i otwórz pull request
w swoim forku, sprawdzając wcześniej repozytorium i gałąź bazową. Przejrzyj zmianę według listy z
instrukcji: w parze, jeśli prowadzący Ci ją przydzielił, albo samodzielnie. Zostaw merytoryczny
komentarz i odnieś się do niego albo, gdy nie ma czego poprawiać, zatwierdź zmianę: w parze na
GitHubie, samodzielnie jednym konkretnym zdaniem w
`labs/18-pull-requests-and-review/my-review-notes.md`. Instrukcja prosi, żeby nie wymyślać
komentarza tylko po to, by spełnić wymaganie. Scal pull request przyciskiem GitHuba i pobierz
zmianę do lokalnego `main`.

**Rezultat:** pull request skierowany do `main` Twojego forka, z opisem zmiany, powodu i sposobu
sprawdzenia; przegląd zakończony jednym z dwóch wyników z instrukcji; lokalny `main` z nową
funkcją, jej testem i przechodzącymi testami.

**Sprawdź się:** sekcja „Weryfikacja” wyświetla trzy ostatnie commity i uruchamia testy na
lokalnym `main`. Pokazuje w ten sposób kod po scaleniu. Pull requesta, jego opisu ani przeglądu nie
sprawdza żadne polecenie: to, że pull request trafił do Twojego forka i że przegląd ma konkretny
wynik, potwierdzasz na GitHubie i w notatce.

### Repozytorium powinno sprawdzać samo siebie {#lab-19}

Zmiana scalona tydzień temu zepsuła testy na `main`: autor ich nie uruchomił, a osoba
przeglądająca zaufała opisowi.

**Cel:** napisać prosty przepływ GitHub Actions uruchamiany przy każdym wysłaniu zmian i pull
requeście, rozumieć każdy jego krok i traktować wynik CI jako dowód.

**Zakres pracy:** na gałęzi `feature/ci-pipeline` utwórz w katalogu głównym repozytorium plik
`.github/workflows/team-inventory-ci.yml` z kompletnym przepływem dla swojej ścieżki, skopiowanym z
instrukcji bez zmian. Jeśli pracujesz na forku, najpierw włącz w nim GitHub Actions w zakładce
**Actions**; instrukcja wyjaśnia też, dlaczego przepływ kursu `course-health.yml` jest na forku
oznaczony jako pominięty. Otwórz pull request w swoim forku i obserwuj wynik w zakładce **Checks**.
Potem celowo zepsuj jeden test, zobacz czerwony wynik, cofnij zmianę, poczekaj na zielony i scal.

**Rezultat:** przepływ, który przy wysłaniu zmian i pull requestach uruchamia testy Twojej ścieżki;
zaobserwowany czerwony wynik dla zepsutego testu i zielony po naprawie; zielone kontrole na `main`
po scaleniu.

**Sprawdź się:** instrukcja mówi wprost, że żadne lokalne polecenie nie zastąpi obserwowania
kontroli na GitHubie, bo to jest sens tego laboratorium. Sekcja „Weryfikacja” pozwala tylko
odtworzyć lokalnie polecenia przepływu: instalację zależności i testy w katalogu Twojej ścieżki.

### Co oznacza „zrobione”? {#lab-20}

Dwie osoby z zespołu spierają się, kiedy zadanie jest ukończone. Każda definicja obejmuje tylko
część pracy.

**Cel:** ułożyć konkretną i sprawdzalną definicję ukończenia (Definition of Done) i ocenić według
niej wykonaną pracę.

**Zakres pracy:** w tym laboratorium nie piszesz kodu. Przejrzyj kryteria akceptacji laboratoriów
11–19 i utwórz `labs/20-definition-of-done/definition-of-done.md` z listą 5–8 kryteriów w postaci
pól wyboru Markdown, pasującą do każdej przyszłej zmiany w `examples/team-inventory/` Twojej
ścieżki. Każde kryterium ma dać się rozstrzygnąć na „tak” albo „nie” na podstawie kodu wyjścia
polecenia, obecności pliku albo stanu pull requesta. W tym samym pliku oceń według listy, punkt po
punkcie, faktyczny wynik jednego laboratorium z zakresu 11–19.

**Rezultat:** lista 5–8 niezależnie sprawdzalnych kryteriów i ocena jednego laboratorium, która
odzwierciedla rzeczywisty stan, a nie domyślne „tak”.

**Sprawdź się:** sekcja „Weryfikacja” sprawdza, czy plik istnieje, i liczy w nim pola wyboru;
wynik ma mieścić się w zakresie 5–8. Tego, czy kryteria są naprawdę sprawdzalne i czy ocena
odpowiada rzeczywistości, nie sprawdza żadne polecenie. Pomagają w tym pytania z sekcji
„Zastanów się”.

## Oczekiwane rezultaty

Każde laboratorium kończy się wynikiem opisanym w sekcji „Kryteria akceptacji” jego instrukcji. Po
całym zestawie:

- `main` Twojego repozytorium zawiera oba ostrzeżenia z laboratoriów 16–17, scalone z rozwiązanym
  konfliktem, oraz raport zamówień z laboratorium 18, scalony przez pull request w Twoim forku;
- Twój fork ma przepływ `team-inventory CI`, który przy wysłaniu zmian i pull requestach uruchamia
  testy Twojej ścieżki;
- masz notatkę z przeglądu kodu, jeśli przegląd był samodzielny, oraz definicję ukończenia z oceną
  jednego laboratorium.

## Wskazówki

- Każda instrukcja ma sekcję „Jeśli utkniesz” z podpowiedziami, osobno dla każdej ścieżki tam, gdzie
  zadanie zależy od języka.
- Przy każdym pull requeście sprawdź przed utworzeniem repozytorium i gałąź bazową. Instrukcja
  laboratorium 18 radzi zacząć od interfejsu WWW GitHuba i opisuje, co zrobić, jeśli GitHub CLI
  kieruje pull request do repozytorium kursu.
- W laboratoriach 16 i 17 dokładne miejsca wstawienia kodu mają znaczenie: od nich zależy, czy
  konflikt w laboratorium 17 będzie wyglądał tak, jak opisuje instrukcja.
