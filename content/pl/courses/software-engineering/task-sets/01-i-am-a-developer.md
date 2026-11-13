---
title: "Jestem developerem"
summary: "Stanowisko pracy, terminal, Git lokalnie i zdalnie oraz pierwszy projekt, który da się uruchomić nie tylko na Twoim komputerze. Laboratoria 01–05."
status: published
materials:
  - repository: software-engineering-in-practice
    path: START-HERE.pl.md
    lang: pl
    label: "Zacznij tutaj: przygotowanie komputera i własnej kopii repozytorium"
  - repository: software-engineering-in-practice
    path: docs/setup/troubleshooting.pl.md
    lang: pl
    label: "Gdy coś pójdzie nie tak przy konfiguracji"
  - repository: software-engineering-in-practice
    path: README.pl.md
    lang: pl
    label: "Opis kursu i mapa laboratoriów"
tasks:
  lab-01:
    materials:
      - repository: software-engineering-in-practice
        path: labs/01-workstation/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 01 — Witaj na swoim stanowisku pracy"
  lab-02:
    materials:
      - repository: software-engineering-in-practice
        path: labs/02-terminal/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 02 — Terminal jako narzędzie pracy"
  lab-03:
    materials:
      - repository: software-engineering-in-practice
        path: labs/03-inherited-repository/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 03 — Dziedziczysz repozytorium"
  lab-04:
    materials:
      - repository: software-engineering-in-practice
        path: labs/04-local-vs-remote/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 04 — Lokalne to nie zdalne"
      - repository: software-engineering-in-practice
        path: docs/setup/github-auth.pl.md
        lang: pl
        label: "Uwierzytelnianie w GitHubie przy pierwszym wysyłaniu zmian"
      - repository: software-engineering-in-practice
        path: docs/setup/already-have-a-fork.pl.md
        lang: pl
        label: "Gdy git remote -v nie wskazuje Twojego forka"
  lab-05:
    materials:
      - repository: software-engineering-in-practice
        path: labs/05-works-on-my-machine/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 05 — „Działa na moim komputerze”"
      - repository: software-engineering-in-practice
        path: examples/works-on-my-machine/
        lang: en
        label: "Projekt startowy: Python, Go, Java"
---
## Cel

Pierwsza część kursu przygotowuje Cię do codziennej pracy developera. Poruszasz się po komputerze z
poziomu terminala, zapisujesz zmiany w Gicie, wysyłasz je do repozytorium na GitHubie i
sprawdzasz, czy projekt da się uruchomić także na innym komputerze niż Twój.

## Wymagania wstępne

- Komputer z Windows, macOS albo Linuksem lub praca w GitHub Codespaces.
- Konto na GitHubie.
- Środowisko przygotowane według przewodnika „Zacznij tutaj” (w materiałach poniżej). Nie musisz
  wcześniej znać terminala ani Gita.
- Do laboratorium 05: podstawy jednego z języków — Pythona, Go albo Javy.

## Materiały

Pełne instrukcje są w repozytorium kursu. Każda ma tę samą budowę: sytuacja, cele nauki,
przygotowanie, zadanie, kryteria akceptacji, weryfikacja, pytania do przemyślenia, podpowiedzi i
zapowiedź kolejnego kroku.

## Zadania

### Witaj na swoim stanowisku pracy {#lab-01}

Dołączasz do projektu i dostajesz świeżo skonfigurowany komputer. Zanim zmienisz kod, poznajesz
swoje środowisko.

**Cel:** poruszać się po systemie plików z terminala, tworzyć i sprawdzać pliki oraz rozumieć, do
czego służą zmienne `$HOME`, `$PATH` i `$SHELL`.

**Zakres pracy:** pracując wyłącznie w terminalu, utwórz w katalogu domowym katalog `lab01-notes` z
plikiem `findings.txt` i zapisz w nim opisane wyniki pięciu poleceń, które charakteryzują Twój
komputer. Sprawdź też, gdzie na dysku znajdują się programy `git` i `code`.

**Rezultat:** plik `~/lab01-notes/findings.txt` z pięcioma opisanymi liniami z Twojego komputera;
potrafisz podać ścieżkę katalogu domowego i nazwę swojej powłoki oraz wyjaśnić, do czego służy
`$PATH`.

**Sprawdź się:** polecenia z sekcji „Weryfikacja” instrukcji sprawdzają, czy plik istnieje i ma co
najmniej pięć linii oraz czy powłoka znajduje `git` i `code`.

### Terminal jako narzędzie pracy {#lab-02}

Pracujesz bez myszy: kopiujesz pliki, przeszukujesz ich zawartość, łączysz polecenia i panujesz nad
procesem, który działa aż do zatrzymania.

**Cel:** kopiować, przenosić i usuwać pliki, przeszukiwać ich zawartość i nazwy, przekierowywać
wyjście poleceń oraz uruchomić i zatrzymać długo działający proces.

**Zakres pracy:** na plikach z laboratorium 01 zrób kopię zapasową w nowym katalogu
`~/lab02-notes/`, wyszukaj wybraną linię i zapisz ją do osobnego pliku, policz pasujące pliki. Potem
uruchom pętlę, która co sekundę dopisuje czas do pliku, obserwuj ją z drugiego terminala i zatrzymaj
skrótem `Ctrl+C`.

**Rezultat:** pliki `~/lab02-notes/findings.bak.txt` i `~/lab02-notes/whoami-line.txt` (ten drugi z
dokładnie jedną linią ze słowem `whoami`); potrafisz wyjaśnić różnicę między `>` a `>>` i powiedzieć,
co robi `Ctrl+C`.

**Sprawdź się:** sekcja „Weryfikacja” sprawdza obecność obu plików, liczbę linii w
`whoami-line.txt` i liczbę znalezionych plików `findings.txt`.

### Dziedziczysz repozytorium {#lab-03}

Masz dostęp do repozytorium. Zanim cokolwiek zmienisz, sprawdzasz jego stan i uczysz się
bezpiecznie zapisywać swoją pracę.

**Cel:** odróżniać katalog roboczy, obszar stagingu i lokalne repozytorium; sprawdzać stan
repozytorium poleceniami `git status`, `git log` i `git diff`; utworzyć commit z jasnym komunikatem.

**Zakres pracy:** w swojej kopii repozytorium kursu zapisz obserwacje w pliku
`labs/03-inherited-repository/notes/my-observations.txt`, dodaj do stagingu tylko ten plik, porównaj
`git diff` z `git diff --staged` i utwórz commit z komunikatem po angielsku. Instrukcja wyjaśnia, co
zrobić, gdy przy pierwszym commicie Git poprosi o podanie autora.

**Rezultat:** zacommitowany plik z obserwacjami (co najmniej trzy linie), Twój commit widoczny w
`git log`; potrafisz wyjaśnić, co oznacza „staged”.

**Sprawdź się:** sekcja „Weryfikacja” sprawdza, czy Twój commit jest najnowszy, czy w repozytorium
nie ma niezapisanych zmian i czy plik z obserwacjami ma co najmniej trzy linie.

### Lokalne to nie zdalne {#lab-04}

Twój commit istnieje na razie tylko na Twoim komputerze. Ktoś z zespołu pyta, czy zmiany są już na
GitHubie — a Ty jeszcze nie wiesz, jak to sprawdzić.

**Cel:** odróżniać repozytorium lokalne od zdalnego oraz Git od GitHuba; sprawdzać skonfigurowane
repozytoria zdalne; wysyłać zmiany poleceniem `git push` i pobierać je poleceniem `git pull`.

**Zakres pracy:** sprawdź, dokąd wskazuje `origin`, i opisz to jednym zdaniem, własnymi słowami, w
pliku `labs/04-local-vs-remote/notes/my-observations.txt` — plik i katalog `notes/` tworzysz sam,
tak jak w laboratorium 03. Utwórz commit, wyślij swoje commity na GitHuba, porównaj historię
lokalną z historią widoczną na GitHubie i pobierz zmiany. Jeśli `git remote -v` nie wskazuje Twojego forka, zatrzymaj
się i skorzystaj z przewodnika w materiałach — wysłanie zmian do cudzego repozytorium skończy się
błędem uprawnień.

**Rezultat:** commity z laboratoriów 03 i 04 widoczne zarówno lokalnie, jak i na GitHubie; notatka
o `origin`; potrafisz jednym zdaniem odróżnić repozytorium lokalne od zdalnego oraz Git od GitHuba.

**Sprawdź się:** po poleceniach z sekcji „Weryfikacja” `git status` zgłasza brak zmian i zgodność z
gałęzią zdalną, a Twój ostatni commit widać w repozytorium na GitHubie.

### „Działa na moim komputerze” {#lab-05}

Ktoś przesyła Ci mały projekt i mówi: „Po prostu go uruchom”. U niego działa, u Ciebie brakuje
zależności albo wersji narzędzia — a projekt nie określa swoich wymagań.

W tym laboratorium wybierasz ścieżkę językową: Python, Go albo Java, i wykonujesz część instrukcji
dla wybranego języka. Od tej pory projekty startowe znajdziesz w katalogu `examples/` repozytorium.

**Cel:** wyjaśnić, dlaczego „u mnie działa” nie dowodzi, że projekt jest odtwarzalny; jawnie określić
zależności lub wymaganą wersję narzędzia za pomocą narzędzi swojej ścieżki; rozumieć rolę manifestu
projektu i konfiguracji devcontainera.

**Zakres pracy:** w projekcie startowym dla swojego języka doprowadź do sytuacji, w której brakuje
wymagania (w Pythonie: uruchomienie bez zainstalowanych zależności; w Go i Javie: celowe podniesienie
wymaganej wersji narzędzia), przeczytaj komunikaty błędów i przywróć działający stan. Wnioski oraz
obserwację z pliku `.devcontainer/devcontainer.json` zapisz w
`labs/05-works-on-my-machine/notes/my-observations.txt`. Na koniec zacommituj i wyślij zmiany na
GitHuba.

**Rezultat:** testy projektu startowego przechodzą; w ścieżce Python plik `uv.lock` jest
zacommitowany, a w ścieżkach Go i Java manifest projektu nie różni się od startera; notatki
odpowiadają na pytania z instrukcji.

**Sprawdź się:** sekcja „Weryfikacja” ma wariant dla każdej ścieżki: uruchamia testy projektu
startowego, sprawdza zapisane wymagania (`uv.lock` w Pythonie, wersję w `go.mod` albo
`build.gradle`) i obecność notatek.

## Oczekiwane rezultaty

Każde laboratorium kończy się wynikiem opisanym w sekcji „Kryteria akceptacji” jego instrukcji. Po
całym zestawie:

- masz działające stanowisko pracy: terminal, Git, VS Code i własną kopię repozytorium kursu
  połączoną z GitHubem;
- w katalogu domowym masz notatki z laboratoriów 01 i 02 (`~/lab01-notes/`, `~/lab02-notes/`);
- w Twoim repozytorium na GitHubie są commity z notatkami z laboratoriów 03–05;
- projekt startowy z laboratorium 05 działa w wybranym języku, a jego wymagania są zapisane w
  repozytorium.

## Wskazówki

- Każda instrukcja ma sekcję „Jeśli utkniesz” z podpowiedziami: od ogólnych do coraz bardziej
  szczegółowych. Zajrzyj do niej, zanim poprosisz o pomoc.
- Pytania z sekcji „Zastanów się” pomagają sprawdzić, czy rozumiesz, dlaczego coś działa.
- Notatki z laboratoriów 01 i 02 powstają w katalogu domowym, poza repozytorium; laboratorium 02
  korzysta z plików z laboratorium 01.
- Problemy z instalacją, forkiem albo stanem repozytorium opisuje przewodnik „Gdy coś pójdzie nie tak
  przy konfiguracji” w materiałach zestawu.
