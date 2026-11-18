---
title: "Jesteście zespołem inżynierskim"
summary: "Projekt TableTime od zera w nowym repozytorium zespołu: plan i decyzja architektoniczna, iteracja przez pull requesty z CI, zmiana wymagań, incydent produkcyjny i przekazanie projektu innym. Laboratoria 26–30."
status: published
materials:
  - repository: software-engineering-in-practice
    path: README.pl.md
    lang: pl
    label: "Opis kursu: akty, ścieżki językowe i wymagane wersje narzędzi"
  - repository: software-engineering-in-practice
    path: examples/capstone-starters/
    lang: en
    label: "Projekty startowe TableTime w Pythonie, Go i Javie"
  - repository: software-engineering-in-practice
    path: docs/setup/troubleshooting.pl.md
    lang: pl
    label: "Gdy coś pójdzie nie tak przy konfiguracji"
tasks:
  lab-26:
    materials:
      - repository: software-engineering-in-practice
        path: labs/26-project-kickoff/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 26 — Kickoff projektu"
  lab-27:
    materials:
      - repository: software-engineering-in-practice
        path: labs/27-development-iteration/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 27 — Iteracja rozwojowa"
  lab-28:
    materials:
      - repository: software-engineering-in-practice
        path: labs/28-change-request/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 28 — Zmiana wymagań"
  lab-29:
    materials:
      - repository: software-engineering-in-practice
        path: labs/29-production-incident/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 29 — Incydent produkcyjny"
  lab-30:
    materials:
      - repository: software-engineering-in-practice
        path: labs/30-handover/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 30 — Handover"
---
## Cel

Ostatnia część kursu nie daje już gotowego projektu. Restauracja prowadzi rezerwacje na papierze i
potrzebuje małego narzędzia TableTime. Zakres, model danych, język i plan ustalasz samodzielnie
albo z zespołem. Projekt powstaje w nowym repozytorium, przechodzi przez iterację z pull requestami i CI,
zmianę wymagań i zgłoszony incydent, a na koniec trafia do osób, które go wcześniej nie widziały.

## Wymagania wstępne

- Ukończony [zestaw 5](the-system-lives-in-a-larger-world.md) w wybranej ścieżce: instrukcja
  laboratorium 26 zakłada ukończone laboratoria 01–25.
- Akt VI jest jednym ciągiem pracy nad TableTime. Każde laboratorium zaczyna od wyniku
  poprzedniego: laboratorium 27 od planu, decyzji o języku i skopiowanego projektu startowego z
  laboratorium 26, laboratorium 28 od scalonego MVP, laboratorium 29 od scalonej zmiany wymagań, a
  laboratorium 30 od projektu z poprawką incydentu.
- Konto na GitHubie i te same narzędzia co wcześniej, dla języka wybranego w laboratorium 26.
  Instrukcja laboratorium 26 nie wymaga GitHub CLI, kluczy SSH, WSL ani Dockera.

## Ścieżka językowa

Język projektu wybierasz albo wybieracie w laboratorium 26 i zapisujecie w decyzji architektonicznej
`docs/adr/adr-001-language-choice.md`. Instrukcja dopuszcza każdy z trzech języków kursu.
Dotychczasowa ścieżka jest jednym z argumentów, które wymienia, ale nie obowiązkiem. Od tej decyzji
polecenia w laboratoriach 27–30 zależą od zapisanego języka:

- **Python:** projekt startowy `examples/capstone-starters/python/`; `uv sync`, testy poleceniem
  `uv run pytest`, uruchomienie poleceniem `uv run python main.py`.
- **Go:** projekt startowy `examples/capstone-starters/go/`; testy poleceniem `go test ./...`,
  uruchomienie poleceniem `go run .`. Zmiana nazwy modułu na przykład na `tabletime` jest
  opcjonalna i instrukcja podaje do niej jedno polecenie.
- **Java:** projekt startowy `examples/capstone-starters/java/` z zapisanym w repozytorium Gradle
  Wrapperem; testy poleceniem `./gradlew test`, budowanie poleceniem `./gradlew build`. Wrappera
  nie generujesz na nowo.

Każdy projekt startowy zawiera tylko program „hello world” i jeden przechodzący test.

## Repozytorium zespołu, fork i praca w zespole

- **Nowe repozytorium.** TableTime powstaje w nowym, pustym repozytorium na GitHubie, do którego
  może wysyłać zmiany cały zespół. Nie jest to fork repozytorium kursu i nie powstaje wewnątrz Twojego
  forka z laboratoriów 01–25. Zakłada je jedna osoba, a w wariancie zespołowym dodaje pozostałe jako
  współpracowników w **Settings → Collaborators**. Każda osoba klonuje ten sam adres i sprawdza
  `git remote -v`.
- **Repozytorium kursu.** Z repozytorium kursu czytasz instrukcje i kopiujesz projekt startowy. Nie
  wysyłasz do niego zmian ani pull requestów.
- **Zespół albo praca samodzielna.** Instrukcje przewidują dwa warianty. Jeśli prowadzący przydzielił
  Cię do zespołu 3–4 osób, plan, pull requesty i przeglądy wykonujecie razem. Jeśli pracujesz
  samodzielnie, jesteś całym zespołem: podejmujesz decyzje samodzielnie i przeglądasz własne zmiany według
  listy kontrolnej z laboratorium 18. Ta strona nie zakłada, że zespoły zostały już przydzielone.
- **Przekazanie w laboratorium 30.** W wariancie zespołowym prowadzący łączy Wasz zespół z innym.
  Strona odbierająca pracuje we własnym forku repozytorium zespołu oryginalnego i otwiera z niego
  pull request do tego repozytorium. W wariancie samodzielnym oceniasz własny projekt tak, jakby był
  Ci obcy.

## Materiały

Pełne instrukcje są w repozytorium kursu, po polsku i po angielsku. Kod projektów startowych jest po
angielsku. Każda instrukcja ma tę samą podstawową budowę: sytuacja, cele nauki, przygotowanie,
zadanie, kryteria akceptacji, weryfikacja, pytania do przemyślenia, podpowiedzi i zapowiedź
kolejnego kroku.

## Zadania

### Kickoff projektu {#lab-26}

Właściciel restauracji opisuje problem jednym zdaniem, a reszta należy do zespołu. Minimalne
możliwości to utworzenie rezerwacji, lista rezerwacji na dany dzień i anulowanie. Brief celowo nie
mówi, co ma się dziać, gdy dwie rezerwacje trafią na ten sam stolik w tym samym czasie.

**Cel:** zamienić otwarty problem na spisany zakres, założenia i sprawdzalne kryteria akceptacji
MVP, uzasadnić wybór języka w lekkim zapisie decyzji architektonicznej (ADR) i założyć repozytorium
projektu.

**Zakres pracy:** to laboratorium to prawie wyłącznie planowanie. Załóż nowe repozytorium zespołu
według kroku 1 instrukcji, bez automatycznego README, `.gitignore` i licencji, sklonuj je poza
klonem repozytorium kursu i wyślij ręcznie napisany `README.md` jako pierwszy commit. Napisz
`PROJECT_PLAN.md` z sześcioma punktami z instrukcji: zakres, założenia (w tym model czasu
rezerwacji, opisany tak dokładnie, żeby dało się rozstrzygnąć, czy dwie rezerwacje się nakładają),
kryteria akceptacji, odpowiedzialności, plan kamieni milowych dla laboratoriów 27–30 i największe
ryzyka. Napisz `docs/adr/adr-001-language-choice.md` według szablonu z instrukcji. Skopiuj do
katalogu głównego cały projekt startowy wybranego języka, razem z plikami zaczynającymi się od
kropki, przeczytaj i usuń `STARTER.md`, uruchom testy, zapisz commit i go wyślij. Konfiguracja CI
jest tu opcjonalna; laboratorium 27 zaczyna się od niej.

**Rezultat:** repozytorium zespołu z `README.md`, `PROJECT_PLAN.md`, ADR-001 i projektem startowym,
który każda osoba z zespołu klonuje i testuje na zielono.

**Sprawdź się:** instrukcja mówi wprost, że planu nie sprawdza żadne automatyczne polecenie. Czytasz
`PROJECT_PLAN.md` tak, jak zrobiłby to recenzent, który nie był na spotkaniu, i sprawdzasz, czy
według opisanego modelu czasu da się rozstrzygnąć, czy dwie podane rezerwacje się nakładają.
Lokalnie sprawdzasz tylko `git remote -v`, obecność plików startera (`ls -a`) i zielone testy.
To, że każda osoba z zespołu może sklonować repozytorium i uruchomić testy, potwierdza w praktyce
każda z tych osób.

### Iteracja rozwojowa {#lab-27}

Plan jest gotowy, decyzja zapisana. Teraz budujesz MVP, a nawyki z Aktu IV muszą przetrwać
codzienną pracę i presję czasu.

**Cel:** wielokrotnie przejść pełną pętlę zgłoszenie → gałąź → commity → testy → pull request →
przegląd → CI → scalenie, bez instrukcji prowadzącej krok po kroku.

**Zakres pracy:** zaczynasz od repozytorium z laboratorium 26. Jeśli CI nie powstało wcześniej,
skonfiguruj je według wzorca z laboratorium 19, zanim powstanie kod funkcji; instrukcja podaje
akcje i wersje dla każdego języka. Instrukcja nie ma stałej listy funkcji: dla każdej możliwości MVP
z `PROJECT_PLAN.md` przejdź pełną pętlę, z testem napisanym przed implementacją, małymi pull
requestami i przeglądem wykonanym przez osobę z zespołu albo samodzielnie według listy z
laboratorium 18. Scalaj dopiero po zielonym CI. Instrukcja pokazuje przykładowy podział pracy w
zespole 3–4 osób. W wariancie samodzielnym pozwala rozłożyć pracę na kilka sesji albo zawęzić zakres
MVP w planie.

**Rezultat:** wszystkie kryteria akceptacji MVP z `PROJECT_PLAN.md` spełnione i scalone, zielone CI
na głównej gałęzi, a historia commitów i lista pull requestów jako dowód pętli.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia zestaw testów w języku z ADR (`uv run pytest -v`,
`go test ./...` albo `./gradlew test`). Zielone CI na ostatnim commicie głównej gałęzi
sprawdzasz na GitHubie. Tego, czy testy powstawały przed kodem, czy przeglądy były prawdziwe i czy
pull requesty były małe, nie sprawdza żadne polecenie. Widać to w historii repozytorium i w pull
requestach.

### Zmiana wymagań {#lab-28}

Restauracja odmawia dużym grupom i pyta, czy system może łączyć dwa stoliki, a MVP zakładało jeden
stolik na rezerwację.

**Cel:** wprowadzić prawdziwą zmianę wymagań we własnym projekcie, wskazać, które pliki i kształty
danych zmiana naprawdę dotyka, i uczciwie ocenić, czy projekt z laboratoriów 26–27 obniżył jej
koszt.

**Zakres pracy:** zaczynasz od scalonego MVP. Na nowej gałęzi, zanim napiszesz kod, zapisz w
`docs/change-request-impact.md` przewidywanie: które pliki zmienisz i czy model danych ma miejsce na
rezerwację z więcej niż jednym stolikiem. Zapisz to przewidywanie w osobnym commicie. Zaimplementuj
łączenie stałych, ustalonych przez zespół par sąsiednich stolików i zaktualizuj testy. Test zmieniony
tylko z powodu zmiany nazwy pola opisz w tym samym pliku. Przed otwarciem pull requesta dopisz, co
faktycznie się zmieniło w porównaniu z przewidywaniem, i scal całość jednym pull requestem po
zielonym CI.

**Rezultat:** łączenie stolików zaimplementowane, przetestowane i scalone; `docs/change-request-impact.md`
z przewidywaniem i rzeczywistością w tym samym pull requeście co implementacja.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia pełny zestaw testów. Instrukcja oczekuje w nim
testów łączenia stolików i odrzucenia grupy, która nie mieści się w żadnej kombinacji. Polecenia nie
sprawdzają kolejności commitów: to, że przewidywanie jest w historii przed kodem, odczytujesz z
`git log`, a czysty stan po scaleniu z `git status --short`. Uczciwość porównania przewidywania z
rzeczywistością oceniasz samodzielnie albo w przeglądzie.

### Incydent produkcyjny {#lab-29}

Menedżer zgłasza, że dwie grupy przyszły na 19:00 z potwierdzeniem na ten sam stolik.

**Cel:** odtworzyć zgłoszenie jako test, zanim zmienisz kod, naprawić defekt bez psucia
wcześniejszego zachowania i napisać postmortem bez obwiniania osób (blameless).

**Zakres pracy:** zaczynasz od projektu ze scaloną zmianą wymagań. Pracujesz na gałęzi, bo
instrukcja mówi wprost, że incydent nie zawiesza pull requestów ani przeglądu. Najpierw sprawdzasz,
jak zachowuje się Twój system według modelu czasu z laboratorium 26, i wybierasz jedną z trzech
ścieżek. Ścieżka A: błąd jest prawdziwy, więc piszesz test, który nie przechodzi, i naprawiasz
defekt. Ścieżka B: prosty przypadek jest już chroniony, więc dowodzisz tego testem i szukasz
głębszego przypadku wynikającego z Twoich założeń. Ścieżka C: żadnej wersji nie da się odtworzyć,
więc dokumentujesz próby i dodajesz test potwierdzający ochronę. Instrukcja zabrania tworzenia
sztucznej awarii i zbędnej poprawki. Na koniec piszesz `POSTMORTEM.md` z elementami wymienionymi w
instrukcji i scalasz całość pull requestem po zielonym CI.

**Rezultat:** test regresyjny albo potwierdzający, poprawka, jeśli była potrzebna, oraz
`POSTMORTEM.md`, który zgodnie z prawdą opisuje wybraną ścieżkę i kończy się konkretną rekomendacją
dla systemu albo procesu.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia pełny zestaw testów. Pokazuje stan po poprawce: to,
że test regresyjny nie przechodził przed nią, widać tylko wtedy, gdy uruchomisz go przed zmianą
kodu. Wybór ścieżki, bezstronność postmortemu i trafność rekomendacji wymagają przeglądu przez
człowieka.

### Handover {#lab-30}

Zespół kończy pracę nad TableTime, a projekt przejmują osoby, które nie znają powodów wcześniejszych
decyzji. Wszystko, czego potrzebują, musi być w repozytorium.

**Cel:** przygotować projekt tak, żeby obca osoba mogła go skonfigurować i sprawdzić wyłącznie na
podstawie dokumentacji, oraz ocenić przekazanie ze strony odbierającej.

**Zakres pracy:** zaczynasz od projektu po laboratorium 29. Strona przekazująca uzupełnia
`README.md` tak, żeby wystarczał do sklonowania, instalacji, uruchomienia testów i jednorazowego
uruchomienia aplikacji. Dodaje krótki `ARCHITECTURE.md` z odnośnikiem do ADR-001 i potwierdza
zielone CI. Poza krótkim ustnym wprowadzeniem resztę musi wyjaśniać repozytorium. Strona odbierająca forkuje repozytorium
zespołu oryginalnego i klonuje swój fork w nowym miejscu. Konfiguruje projekt wyłącznie według
`README.md`, zapisując każde miejsce, w którym musiała zgadywać. W ograniczonym, z góry ustalonym
czasie dodaje na gałęzi w swoim forku jedną małą funkcję tylko do odczytu z testem, na przykład
wyszukanie rezerwacji po identyfikatorze. Potem otwiera pull request do repozytorium zespołu
oryginalnego i dołącza `HANDOVER_NOTES.md` z konkretną informacją zwrotną. Czy ten pull request
zostanie scalony, decyduje zespół oryginalny. Instrukcja opisuje stronę odbierającą przez fork i pull
request; nie mówi, jak wykonać te dwa kroki, gdy w wariancie samodzielnym oceniasz własne
repozytorium.

**Rezultat:** `README.md` i `ARCHITECTURE.md`, które wystarczyły stronie odbierającej; pull request
z forka strony odbierającej z jedną małą, przetestowaną zmianą; `HANDOVER_NOTES.md`, który dociera
do zespołu oryginalnego.

**Sprawdź się:** instrukcja mówi wprost, że nie ma tu jednego polecenia. Strona odbierająca na
świeżym klonie wykonuje dokładnie kroki z `README.md` zespołu oryginalnego i uruchamia polecenie
testów, które ten plik podaje. Jakość dokumentacji, uczciwość informacji zwrotnej i to, czy
przekazanie się udało, ocenia człowiek, a pull request i jego przegląd są widoczne tylko na GitHubie.

## Oczekiwane rezultaty

Każde laboratorium kończy się wynikiem opisanym w sekcji „Kryteria akceptacji” jego instrukcji. Po
całym zestawie:

- repozytorium zespołu zawiera `README.md`, `ARCHITECTURE.md`, `PROJECT_PLAN.md`, ADR-001, MVP z
  łączeniem stolików, `docs/change-request-impact.md` i `POSTMORTEM.md`;
- każda zmiana trafiła do głównej gałęzi przez pull request z przeglądem i zielonym CI;
- strona odbierająca otworzyła pull request z małą zmianą i informacją zwrotną w
  `HANDOVER_NOTES.md`.

## Wskazówki

- Każda instrukcja ma sekcję „Jeśli utkniesz” z podpowiedziami.
- Jeśli `git remote -v` w laboratorium 26 pokazuje Twój fork kursu zamiast repozytorium zespołu,
  instrukcja radzi sklonować repozytorium zespołu od nowa, a nie przestawiać `origin`.
- Przy kopiowaniu projektu startowego sprawdź `ls -a` w katalogu docelowym: zwykłe kopiowanie może
  pominąć `.gitignore`, a w Pythonie także `.python-version`.
- W Go po zmianie nazwy modułu na `tabletime` polecenie `go build ./...` zostawia w katalogu głównym
  plik wykonywalny `tabletime`. `.gitignore` z projektu startowego ignoruje tylko `/capstonestarter`,
  więc przed pierwszym commitem sprawdź `git status` i nie dodawaj tego pliku.
- Jeśli w laboratorium 29 nie wiesz, którą ścieżką iść, instrukcja radzi zacząć od próby odtworzenia
  ze ścieżki A: jej wynik wskaże właściwą ścieżkę.
