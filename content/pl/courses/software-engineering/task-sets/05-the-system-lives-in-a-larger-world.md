---
title: "System żyje w większym świecie"
summary: "Kontrakt HTTP API, dane w SQLite z migracjami zachowującymi starsze wiersze, ponowienia wokół zawodnego serwisu zewnętrznego, logi z testami i wydania jako tagi Gita z dziennikiem zmian. Laboratoria 21–25."
status: published
materials:
  - repository: software-engineering-in-practice
    path: README.pl.md
    lang: pl
    label: "Opis kursu: akty, ścieżki językowe i wymagane wersje narzędzi"
  - repository: software-engineering-in-practice
    path: examples/order-api/
    lang: en
    label: "Projekt Aktu V: serwis zamówień w Pythonie, Go i Javie"
  - repository: software-engineering-in-practice
    path: docs/setup/troubleshooting.pl.md
    lang: pl
    label: "Gdy coś pójdzie nie tak przy konfiguracji"
tasks:
  lab-21:
    materials:
      - repository: software-engineering-in-practice
        path: labs/21-api-is-a-contract/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 21 — API to kontrakt"
  lab-22:
    materials:
      - repository: software-engineering-in-practice
        path: labs/22-data-outlives-code/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 22 — Kod się zmienił, stare dane zostały"
  lab-23:
    materials:
      - repository: software-engineering-in-practice
        path: labs/23-outside-world-fails/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 23 — Świat zewnętrzny zawodzi"
  lab-24:
    materials:
      - repository: software-engineering-in-practice
        path: labs/24-production-says-it-doesnt-work/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 24 — Produkcja mówi „to nie działa”"
  lab-25:
    materials:
      - repository: software-engineering-in-practice
        path: labs/25-release-and-compatibility/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 25 — Wydanie i kompatybilność"
---
## Cel

Piąta część kursu wyprowadza kod poza jeden proces. Opisujesz HTTP API serwisu zamówień jako
kontrakt, przenosisz zamówienia do bazy SQLite i zmieniasz jej schemat bez utraty starszych danych,
otaczasz zawodne wywołanie zewnętrznego serwisu ograniczoną liczbą ponowień, dodajesz logi, z
których da się odczytać przebieg żądania, a na koniec wydajesz kolejne wersje jako tagi Gita z
dziennikiem zmian.

## Wymagania wstępne

- Ukończony [zestaw 4](you-do-not-work-alone.md) w wybranej ścieżce: instrukcja laboratorium 21
  zakłada ukończone laboratoria 06–20.
- Akt V jest jednym ciągiem pracy nad tym samym serwisem, a nie zbiorem niezależnych zadań. Każde
  laboratorium zaczyna od wyniku poprzedniego: laboratorium 22 od kontraktu i walidacji z
  laboratorium 21, laboratorium 23 od bazy SQLite z migracją `notes`, laboratorium 24 od ponowień
  podłączonych do tworzenia zamówienia, a laboratorium 25 od scalonego i otagowanego wydania
  `order-api-v1.0.0` z laboratorium 24.
- Własny fork repozytorium kursu z włączonym GitHub Actions, jak w laboratorium 19. Każde
  laboratorium tego aktu kończy się pull requestem scalonym dopiero po zielonym wyniku CI.
- Te same narzędzia co w poprzednich aktach, tylko dla wybranej ścieżki. Serwer sprawdzasz ręcznie
  poleceniami `curl` z drugiego terminala; instrukcja laboratorium 21 pokazuje, jak otworzyć dwa
  terminale w VS Code.

## Ścieżka językowa

Kontynuujesz ścieżkę wybraną w laboratorium 05. Instrukcje dzielą się na warianty i czytasz tylko
swój. Kontrakt `examples/order-api/CONTRACT.md` jest wspólny dla wszystkich ścieżek, a polecenia
`curl` są w każdej ścieżce takie same, bo korzystają wyłącznie z HTTP.

- **Python:** pracujesz w `examples/order-api/python/`, serwer uruchamiasz poleceniem
  `uv run python api.py`, a testy poleceniem `uv run pytest -v`. SQLite i logowanie pochodzą z
  biblioteki standardowej (`sqlite3`, `logging`).
- **Go:** pracujesz w `examples/order-api/go/`, serwer uruchamiasz poleceniem `go run .`, a testy
  poleceniem `go test ./...`. W laboratorium 22 dodajesz poleceniem
  `go get modernc.org/sqlite@v1.60.1` sterownik SQLite napisany w całości w Go, bez kompilatora C i
  CGO; `go.mod` i `go.sum` zapisujesz w commicie. Logi zapisujesz przez `log/slog`.
- **Java:** pracujesz w `examples/order-api/java/`, serwer uruchamiasz poleceniem
  `./gradlew run --console=plain`, a testy poleceniem `./gradlew test`. W laboratorium 22 dodajesz
  do `build.gradle` zależność `org.xerial:sqlite-jdbc:3.53.4.0`, która zawiera biblioteki SQLite dla
  Windows, Linuksa i macOS. Logi zapisujesz przez `java.util.logging`, w którym najcięższy poziom
  nazywa się `SEVERE`, a nie `ERROR`. `./gradlew test` nie wypisuje liczby testów; pokazuje ją
  raport `build/reports/tests/test/index.html`.

Instrukcje podają liczbę testów po każdym laboratorium: 4 po laboratorium 21, 5 po 22, 9 po 23 i 11
po 24.

## Twój fork, pull requesty i tagi

- **Gałąź i pull request w każdym laboratorium.** Pracę z każdego laboratorium wykonujesz na
  osobnej gałęzi, wysyłasz ją do swojego forka i scalasz pull requestem dopiero po zielonym wyniku
  przepływu `order-api CI` z laboratorium 21. Instrukcja laboratorium 21 zaznacza, że sam zielony
  wynik `team-inventory CI` z laboratorium 19 nie wystarczy.
- **Tag dopiero po scaleniu.** Tagi `order-api-v1.0.0` (laboratorium 24) i `order-api-v1.1.0`
  (laboratorium 25) tworzysz na `main` po pobraniu scalonej zmiany poleceniem `git pull --ff-only` i
  wysyłasz do swojego forka. Instrukcje wyjaśniają, dlaczego nie taguje się gałęzi przed scaleniem:
  scalenie przez squash albo rebase może dać na `main` commit o innym hashu.
- **Jedno repozytorium.** Instrukcja laboratorium 25 przypomina, że `examples/order-api/<język>/` to
  katalog, a nie osobne repozytorium: tag wskazuje commit całego repozytorium kursu w Twoim forku.
  Przed wysłaniem tagu sprawdzasz `git remote -v`.
- **Bez poleceń siłowych.** Instrukcje nie pozwalają wychodzić z problemów z tagami przez
  `git tag -f`, `git push --force` ani `git reset --hard` i dla typowych sytuacji opisują bezpieczne
  rozwiązanie. Wydanie w tym akcie to tylko tag Gita: bez GitHub Release i bez publikowania paczek.

## Materiały

Pełne instrukcje są w repozytorium kursu, po polsku i po angielsku. Kod projektu jest po angielsku.
Każda instrukcja ma tę samą podstawową budowę: sytuacja, cele nauki, przygotowanie, zadanie,
kryteria akceptacji, weryfikacja, pytania do przemyślenia, podpowiedzi i zapowiedź kolejnego kroku.

## Zadania

### API to kontrakt {#lab-21}

Inna część systemu kuchennego, być może napisana w innym języku, ma tworzyć zamówienia i sprawdzać
ich stan przez sieć, bez importowania Twojego kodu.

**Cel:** opisać kontrakt endpointów HTTP, czyli żądania, odpowiedzi, kody statusu i format błędów,
oraz dodać regułę walidacji bez zmiany zachowania dla klientów, którzy już przestrzegają kontraktu.

**Zakres pracy:** uruchom serwer startowy w jednym terminalu i sprawdź go poleceniami `curl` z
instrukcji w drugim. Na podstawie tych obserwacji utwórz `examples/order-api/CONTRACT.md`: dla
każdego endpointu metodę i ścieżkę, ciało żądania, wszystkie odpowiedzi z kodem statusu i przyczynę
każdego błędu. Dodaj regułę, że każdy element `items` musi być niepustym napisem, test tej reguły i
nowy błąd w kontrakcie. Utwórz przepływ `.github/workflows/order-api-ci.yml` z instrukcji dla swojej
ścieżki. Całość scal pull requestem, na przykład z gałęzi `feature/api-contract`.

**Rezultat:** kontrakt obejmujący każdy endpoint i każdy kod statusu, w tym nowy błąd walidacji;
4 przechodzące testy; przepływ CI uruchamiany przy wysłaniu zmian i pull requestach.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia testy i sprawdza, czy istnieją pliki kontraktu i
przepływu. Nie sprawdza treści kontraktu: to, czy opisuje wszystkie odpowiedzi, porównujesz z
wynikami poleceń `curl`. Zielony wynik `order-api CI` potwierdzasz w zakładce **Checks** pull
requesta.

### Kod się zmienił, stare dane zostały {#lab-22}

Każdy restart serwera usuwa zamówienia, bo istnieją tylko w pamięci. Do tego kuchnia potrzebuje
pola `notes` na uwagi do zamówienia.

**Cel:** zastąpić stan w pamięci bazą SQLite bez zmiany kontraktu, dodać kolumnę migracją, która
nie psuje starszych wierszy, i odizolować bazę testów od prawdziwych danych.

**Zakres pracy:** w części 1 utwórz warstwę przechowywania (`db.py`, `db.go` albo `OrderDb.java`)
ze schematem z instrukcji i podłącz do niej obsługę HTTP. Testy kierujesz do tymczasowej bazy przez
`ORDER_DB_PATH`; w Javie przez właściwość systemową `order.db.path`, bo JVM nie wyczyści raz
odczytanej zmiennej środowiskowej. Utwórz zamówienie na działającym serwerze, zatrzymaj go,
uruchom ponownie i sprawdź, czy zamówienie przetrwało. Plik bazy zachowaj do końca laboratorium, ale
nie zapisuj go w Git. W części 2 napisz migrację, która sprawdza kolumny przez
`PRAGMA table_info(orders)` i dodaje `notes` tylko wtedy, gdy jej brakuje. Uruchamiaj ją przy
starcie i w testach. Dodaj `notes` do zapisu, odczytu i ciała żądania; dla starszego wiersza baza
zwraca `NULL`, a API ma zwrócić `""`. Potem dwa razy uruchamiasz serwer z tym samym plikiem bazy:
najpierw odczytujesz starsze zamówienie i tworzysz nowe z uwagami, a na koniec sprawdzasz oba.
Laboratorium kończą test nowego pola i aktualizacja kontraktu.

**Rezultat:** 5 przechodzących testów; zamówienie sprzed migracji nadal się odczytuje, z
`notes` równym `""`; nowe zamówienie zachowuje `notes` po restarcie; ponowne uruchomienie migracji
na bazie z nową kolumną nie zgłasza błędu; kontrakt z polem `notes`.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia testy. Instrukcja mówi wprost, że ręczne kontrole z
kroków 5, 6, 13, 14 i 15 są nadal wymagane, bo zestaw testów nie zastąpi prawdziwych restartów z
istniejącą bazą. Tego, że `git status` nie pokazuje pliku bazy, też nie sprawdza żadne polecenie z
weryfikacji. Instrukcja prosi, żeby nie udawać starego wiersza ręcznie napisanym plikiem: migracja
ma działać na danych utworzonych przez wcześniejszą wersję kodu.

### Świat zewnętrzny zawodzi {#lab-23}

Każde nowe zamówienie ma wysłać powiadomienie do zewnętrznego serwisu kuchni, który czasem nie
odpowiada za pierwszym razem.

**Cel:** otoczyć zawodne wywołanie ponowieniami z limitem prób i stałym odstępem, testować je bez
sieci i bez prawdziwego czekania oraz rozumieć, dlaczego zamówienie powstaje mimo nieudanego
powiadomienia.

**Zakres pracy:** zdefiniuj rozpoznawalny błąd powiadomienia (`NotifierError`, `ErrNotification`
albo `NotificationException`) i funkcję ponowień według polityki z instrukcji: domyślnie 3 próby,
odstęp 0,2 s między próbami i nigdy po ostatniej, a ponawiany jest wyłącznie rozpoznany błąd
powiadomienia. Odstęp jest stały, a nie wykładniczy. Napisz trzy testy samej polityki z
testowym zamiennikiem klienta (fake), który zawodzi na żądanie: natychmiastowy sukces, sukces po
dwóch awariach i wyczerpanie prób; każdy test sprawdza dokładną liczbę wywołań. Wywołaj
powiadomienie po zapisaniu zamówienia tak, żeby jego awaria nie przerwała żądania; samo
powiadomienie kuchni na razie nic nie wysyła. Czwarty test przechodzi przez prawdziwe HTTP z
zamiennikiem, który zawsze zawodzi, i z zerowym odstępem.

**Rezultat:** 9 przechodzących testów; mimo trzech nieudanych prób powiadomienia `POST` zwraca
`201`, a zamówienie da się potem pobrać.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia testy. To, że żaden test nie czeka naprawdę, widać
tylko po czasie ich działania, a ten obejmuje też obsługę serwera testowego. W Pythonie fixture z
projektu startowego zatrzymuje serwer po każdym teście HTTP przez około 0,5 s. W Javie czas
pierwszego testu w raporcie Gradle obejmuje jednorazowe przygotowanie, na przykład klienta HTTP i
sterownika SQLite. Sam czas nie świadczy więc o prawdziwym odstępie. Działania z prawdziwym odstępem
0,2 s nie sprawdza żaden test: testy celowo go pomijają.

### Produkcja mówi „to nie działa” {#lab-24}

Ktoś zgłasza, że sprawdzał zamówienie i nic nie dostał. Proces działa, na ekranie nie ma błędu i nic
nie zostało zapisane.

**Cel:** dodać logi z poziomami w ważnych momentach obsługi żądania, z kontekstem takim jak
identyfikator zamówienia i numer próby, oraz sprawdzić testem, że rekord logu powstał.

**Zakres pracy:** skonfiguruj logowanie raz, przy starcie, a nie w obsłudze żądania. Instrukcja
podaje tabelę zdarzeń: utworzenie zamówienia na poziomie INFO, brakujące zamówienie i każda nieudana
próba powiadomienia na poziomie WARNING, wyczerpanie wszystkich prób na poziomie ERROR (`SEVERE` w
Javie). Nie loguj zawartości `items` ani `notes`; wystarczy liczba pozycji. Komunikat o starcie
serwera też wypisz przez logger. Napisz dwa testy przechwytujące rekordy logów: INFO przy `POST` i
WARNING z żądanym identyfikatorem przy pobraniu brakującego zamówienia. Uruchom serwer, wyślij kilka
żądań, w tym o brakujące zamówienie, i odczytaj logi. W tym samym pull requeście dodaj
`examples/order-api/<język>/CHANGELOG.md` z wpisem `## [1.0.0]` opisującym API z punktu widzenia
wywołującego. Po scaleniu utwórz na `main` opisany tag `order-api-v1.0.0` i wyślij go do forka.

**Rezultat:** 11 przechodzących testów; dziennik zmian z wpisem `[1.0.0]`; tag
`order-api-v1.0.0` na commicie z `main`, także w Twoim forku.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia testy, wyświetla dziennik zmian, wypisuje tagi
lokalne i tagi w forku oraz sprawdza, czy commit tagu należy do `main`. To, że tag jest opisany
(annotated), widać w wyniku `git ls-remote --tags origin`: tylko tag opisany ma dodatkowy wiersz
z `^{}`. Polecenia nie sprawdzają, czy w logach nie ma zawartości zamówień i czy żaden `print` nie
zastępuje logu; to odczytujesz z kodu i z logów. Logów ponowień nie obejmuje żaden wymagany test,
a przy ręcznym uruchomieniu się nie pojawią, bo powiadomienie kuchni nadal nic nie wysyła i nie
zawodzi.

### Wydanie i kompatybilność {#lab-25}

Inny zespół chce wywoływać `order-api` ze swojego serwisu i musi wiedzieć, z którą wersją się
integruje, co ma nadal działać i skąd dowie się o zmianach.

**Cel:** napisać wpis w dzienniku zmian ważny dla wywołującego, oznaczyć wydanie tagiem i odróżnić
zmianę addytywną od łamiącej, wraz z pozycją SemVer, którą podnosi każda z nich.

**Zakres pracy:** zanim napiszesz kod, sprawdź stan wydania `order-api-v1.0.0`; instrukcja opisuje
typowe rozbieżności i bezpieczne rozwiązanie każdej z nich. Na gałęzi `feature/priority-field`
dodaj opcjonalne pole `priority` z domyślną wartością `"normal"`. Ma być zapisane w bazie przez
drugą migrację, zwracane przez `GET` i zachowane po restarcie, a nie tylko odesłane w odpowiedzi na
`POST`. Napisz trzy testy: jawna wartość, wartość domyślna oraz zapis przez `POST` i odczyt przez
`GET`. Czwarty test
wstawia wiersz surowym `INSERT` bez `priority` przed migracją i sprawdza, że po migracji odczytuje
się z wartością `"normal"`, a nie `null`. Wcześniejsze testy mają przechodzić bez zmian. W
`CONTRACT.md` opisz nowe pole i dodaj sekcję `## Compatibility assumption`. W `CHANGELOG.md` dodaj
wpis `## [1.1.0]` i sekcję `## Compatibility notes`. Po scaleniu utwórz tag `order-api-v1.1.0` i
wyślij go do forka.

**Rezultat:** pole `priority` zapisane w bazie i objęte czterema testami; kontrakt z założeniem
kompatybilności, przedstawionym jako oczekiwanie wobec wywołujących, a nie gwarancja; dziennik
zmian z wpisami `[1.1.0]` i `[1.0.0]`; oba opisane tagi na `main` i w forku.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia testy, wyświetla dziennik zmian, wypisuje tagi
lokalne i tagi w forku oraz sprawdza dla obu tagów, czy ich commit należy do `main`. Instrukcja nie
podaje łącznej liczby testów; po 11 testach z laboratorium 24 i czterech nowych jest ich 15.
Kryterium, że `priority` przetrwa restart serwera, nie sprawdza żadne polecenie z weryfikacji;
można je sprawdzić tak jak restarty w laboratorium 22. Uzasadnienie kompatybilności i wybór pozycji
SemVer sprawdzasz samodzielnie, z pomocą pytań z sekcji „Zastanów się”.

## Oczekiwane rezultaty

Każde laboratorium kończy się wynikiem opisanym w sekcji „Kryteria akceptacji” jego instrukcji. Po
całym zestawie:

- w `examples/order-api/<język>/` Twojej ścieżki działa API z walidacją, zamówieniami w SQLite,
  migracjami `notes` i `priority`, ponowieniami powiadomienia, logami i dziennikiem zmian;
- `examples/order-api/CONTRACT.md` opisuje oba endpointy, ich błędy, pola `notes` i `priority` oraz
  założenie kompatybilności;
- Twój fork ma przepływ `order-api CI`, a każda zmiana z tego aktu została scalona pull requestem po
  zielonym wyniku;
- tagi `order-api-v1.0.0` i `order-api-v1.1.0` wskazują commity z `main` i są w Twoim forku.

## Wskazówki

- Każda instrukcja ma sekcję „Jeśli utkniesz” z podpowiedziami, osobno dla każdej ścieżki.
- Jeśli serwer nie startuje, bo port 8000 jest zajęty, zwykle działa jeszcze poprzednio uruchomiony
  serwer. Instrukcja laboratorium 21 opisuje, jak go znaleźć i jak w ostateczności użyć zmiennej
  `PORT`. Każdy serwer zatrzymujesz w jego terminalu przez `Ctrl+C`.
- Plik bazy utworzony w kroku 5 laboratorium 22 jest potrzebny do końca tego laboratorium: na nim
  sprawdzasz migrację wiersza starszego niż nowa kolumna. Główny `.gitignore` powinien już ignorować
  pliki `*.db` i pliki pomocnicze SQLite; instrukcja mówi, co zrobić, jeśli w starszym forku tych
  wzorców brakuje.
- Identyfikator zamówienia zależy od tego, ile zamówień jest już w bazie. Jeśli przykład z
  instrukcji używa `1` albo `2`, wstaw identyfikator zwrócony przez serwer.
- Jeśli sprawdzenie `git merge-base --is-ancestor` nic nie wypisuje, commit tagu nie należy do
  `main`. Instrukcje laboratoriów 24 i 25 opisują, jak ustalić przyczynę, zanim cokolwiek zmienisz.
