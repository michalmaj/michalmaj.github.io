---
title: "Oprogramowanie musi przetrwać zmianę"
summary: "Od niejasnego zlecenia do wymagań z przykładami, przez koszt zmiany w dwóch wersjach kodu i refaktoryzację pod osłoną testów, po jeden kontrakt w trzech językach i wzorce nazwane po fakcie. Laboratoria 11–15."
status: published
materials:
  - repository: software-engineering-in-practice
    path: README.pl.md
    lang: pl
    label: "Opis kursu: akty, ścieżki językowe i wymagane wersje narzędzi"
  - repository: software-engineering-in-practice
    path: examples/discount-codes/
    lang: en
    label: "Projekty do laboratoriów 12, 13 i 15: kody rabatowe w wersji A i B"
  - repository: software-engineering-in-practice
    path: examples/notifier/
    lang: en
    label: "Projekty do laboratoriów 14 i 15: kontrakt Notifier w trzech językach"
tasks:
  lab-11:
    materials:
      - repository: software-engineering-in-practice
        path: labs/11-changed-requirements/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 11 — Klient zmienił zdanie"
  lab-12:
    materials:
      - repository: software-engineering-in-practice
        path: labs/12-change-surface/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 12 — Gdzie powinna trafić ta zmiana?"
  lab-13:
    materials:
      - repository: software-engineering-in-practice
        path: labs/13-refactoring-safety-net/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 13 — Refaktoryzacja z siatką bezpieczeństwa"
  lab-14:
    materials:
      - repository: software-engineering-in-practice
        path: labs/14-one-contract-three-languages/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 14 — Jeden kontrakt, trzy języki"
  lab-15:
    materials:
      - repository: software-engineering-in-practice
        path: labs/15-patterns-without-worship/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 15 — Wzorce bez bałwochwalstwa"
---
## Cel

Trzecia część kursu dotyczy zmian. Zaczynasz od niejasnego zlecenia i zamieniasz je w konkretne
wymagania. Potem dodajesz to samo wymaganie do dwóch wersji kodu i porównujesz koszt zmiany,
refaktoryzujesz słabszą wersję pod osłoną testów, poznajesz jeden kontrakt zapisany w trzech
językach, a na koniec nazywasz wzorce, które pojawiły się po drodze.

## Wymagania wstępne

- Ukończony [zestaw 2](code-is-not-yet-a-project.md) w wybranej ścieżce: instrukcja laboratorium 11
  zakłada ukończone laboratoria 06–10, a laboratorium 12 — laboratoria 06–11.
- Laboratorium 14 jest wyjątkiem: jego instrukcja wymaga tylko laboratoriów 01–05 i mówi, że
  laboratoria 06–13 nie są potrzebne do tego ćwiczenia. Laboratorium 15 wymaga laboratoriów 12–14.
- Te same narzędzia co w zestawie 2, tylko dla wybranej ścieżki. Laboratoria 11 i 15 nie wymagają
  nowych narzędzi.

## Ścieżka językowa

Laboratoria 12–15 wyglądają tak samo w każdym języku: gdy instrukcja dzieli się na warianty, czytasz
tylko ten dla ścieżki wybranej w Akcie II. W laboratorium 14 czytasz kod kontraktu we wszystkich
trzech językach, ale piszesz go tylko w swoim; uruchomienie pozostałych dwóch języków jest
opcjonalnym ćwiczeniem dla osób, które mają ich narzędzia. Laboratorium 11 nie zależy od języka.

W laboratoriach 12, 13 i 15 pracujesz na gotowych projektach z `examples/discount-codes/`, a w
laboratorium 14 na `examples/notifier/`, w podkatalogu swojego języka. Nie kontynuujesz tu kodu z
Aktu II.

## Materiały

Pełne instrukcje są w repozytorium kursu, po polsku i po angielsku. Kod projektów jest po angielsku.
Każda instrukcja ma tę samą budowę: sytuacja, cele nauki, przygotowanie, zadanie, kryteria
akceptacji, weryfikacja, pytania do przemyślenia, podpowiedzi i zapowiedź kolejnego kroku.

## Zadania

### Klient zmienił zdanie {#lab-11}

Właściciel restauracji chce, żeby kelnerzy mogli wpisać kod rabatowy. To całe zlecenie: nie wiadomo,
jakie kody istnieją, jakie dają rabaty ani co zrobić z pomyłką przy wpisywaniu.

**Cel:** zamienić niejasne zlecenie w pytania doprecyzowujące, a uzgodnione wymaganie w konkretne
przykłady danych wejściowych i oczekiwanych wyników.

**Zakres pracy:** w tym laboratorium nie piszesz kodu. Zanim przeczytasz dalszą część instrukcji,
zapisz co najmniej pięć pytań do właściciela w pliku
`labs/11-changed-requirements/my-clarifying-questions.md`. Potem przeczytaj uzgodnioną specyfikację
z instrukcji i dodaj w tym samym pliku tabelę co najmniej czterech przykładów: zamówienie z
`SAVE10`, z `SAVE5`, bez kodu i z nieistniejącym kodem, każdy z oczekiwaną sumą albo błędem.

**Rezultat:** plik z pytaniami napisanymi przed lekturą specyfikacji i tabelą przykładów, w której
każdy przykład ma jeden jednoznaczny wynik.

**Sprawdź się:** sekcja „Weryfikacja” sprawdza tylko, czy plik istnieje, i liczy w nim elementy
listy. Jak mówi instrukcja, treści analizy wymagań nie da się sprawdzić automatycznie: przeczytaj
notatki jeszcze raz i upewnij się, że każdy przykład ma jeden jednoznaczny wynik. Tego, że pytania
powstały przed lekturą specyfikacji, nie sprawdza nic poza Tobą.

### Gdzie powinna trafić ta zmiana? {#lab-12}

Dwie osoby niezależnie zaimplementowały kody rabatowe. Obie wersje działają tak samo, ale ich
rozbudowa kosztuje różnie dużo pracy.

**Cel:** wskazać pliki, które trzeba zmienić przy nowym wymaganiu, i wyjaśnić sprzężenie (coupling)
i spójność (cohesion) na konkretnym przykładzie.

**Zakres pracy:** przeczytaj wersję A i wersję B w swoim języku i sprawdź, że obie przechodzą
testy. Dodaj do obu wersji kod `SAVE20`, czyli 20% od kwoty po rabacie lojalnościowym, i w każdej
test dla dużego zamówienia, który sprawdza łączny rabat `16.8` i kwotę `53.14`. W wersji A
dodajesz nową gałąź w obliczeniu rachunku, a w wersji B nowy wpis w osobnym pliku z kodami. Potem
zapisz w `examples/discount-codes/COMPARISON.md`, które pliki trzeba było zmienić w każdej wersji i w której
łatwiej wykluczyć zmianę kodu rabatowego jako przyczynę błędu w podatku.

**Rezultat:** w obu wersjach przechodzą wszystkie testy, łącznie z nowymi; `COMPARISON.md` opisuje
Twoją ścieżkę i odpowiada na pytanie z instrukcji.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia testy obu wersji w Twojej ścieżce: w każdym języku
wersja A ma mieć 5 przechodzących testów, a wersja B 8. Sprawdza też, czy `COMPARISON.md`
istnieje; jego treści nie sprawdza.

### Refaktoryzacja z siatką bezpieczeństwa {#lab-13}

Wersja A działa i ma testy, ale łańcuch warunków z kodami rabatowymi rośnie w funkcji, która liczy
cały rachunek.

**Cel:** zmienić strukturę kodu małymi krokami, bez zmiany działania, i po każdym kroku traktować
przechodzące testy jako dowód, że niczego nie zepsuto.

**Zakres pracy:** w swojej kopii wersji A po laboratorium 12 utwórz osobny komponent z kodami
rabatowymi wzorowany na wersji B, uruchom testy, skieruj obliczenie rachunku do nowego komponentu,
znowu uruchom testy, usuń starą logikę warunkową i uruchom testy po raz ostatni. W Go instrukcja
uprzedza, że po usunięciu `switch` import `"fmt"` stanie się nieużywany i kompilacja go zgłosi.

**Rezultat:** plik z kodami rabatowymi ma te same trzy kody co wersja B, a obliczenie rachunku nie
sprawdza już bezpośrednio napisów z kodami.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia testy wersji A (w Go także `go build ./...`) i
szuka w kalkulatorze śladu starej logiki: `elif discount_code`, `case "SAVE` albo
`switch (discountCode)`. Gdy go nie ma, wypisuje `decoupled`. Polecenia pokazują tylko stan
końcowy; to, że testy przechodziły po każdym kroku, widzisz sam w trakcie pracy.

### Jeden kontrakt, trzy języki {#lab-14}

Kuchnia chce powiadomienia, gdy zamówienie jest gotowe: dziś w konsoli, później może e-mailem albo
SMS-em. Trzy zespoły zapisały ten sam mały kontrakt w trzech językach.

**Cel:** wyjaśnić, co sprawia, że coś jest kontraktem, i jak Twój język rozpoznaje jego spełnienie
na tle pozostałych dwóch.

**Zakres pracy:** przeczytaj kontrakt `Notifier` we wszystkich trzech językach i uruchom test swojej
ścieżki w `examples/notifier/`. Dodaj `SilentNotifier`, którego metoda wysyłania nic nie robi, i
sprawdzenie, że wysłanie powiadomienia przez niego nie zgłasza błędu. W ścieżce Java kompilujesz i
uruchamiasz pliki bez Gradle: `javac *.java -d out && java -cp out NotifierCheck`. Potem porównaj
przykłady z instrukcji, które pokazują, jak każdy język reaguje na typ niespełniający kontraktu, i
odpowiedz na trzy pytania w `labs/14-one-contract-three-languages/my-notes.md`.

**Rezultat:** `SilentNotifier` działa w Twoim języku, a nowe sprawdzenie przechodzi razem z
istniejącym; notatki odpowiadają własnymi słowami na trzy pytania z instrukcji.

**Sprawdź się:** sekcja „Weryfikacja” uruchamia testy albo `NotifierCheck` Twojej ścieżki i
sprawdza, czy plik z notatkami istnieje. Treści odpowiedzi nie sprawdza. Startery mają jedno
istniejące sprawdzenie, dla `InMemoryNotifier`; kryteria akceptacji wymieniają także
`ConsoleNotifier`, ale takiego sprawdzenia w projekcie nie ma.

### Wzorce bez bałwochwalstwa {#lab-15}

Kody rabatowe z wersji B i powiadomienia z laboratorium 14 powstały, zanim padła nazwa ich
rozwiązania. Teraz czas ją poznać.

**Cel:** rozpoznać wzorzec Strategy w istniejącym kodzie, wyjaśnić Dependency Injection na
przykładzie funkcji wysyłającej powiadomienie i opisać jednym zdaniem Factory i Adapter.

**Zakres pracy:** wróć do pliku z kodami rabatowymi wersji B i do kontraktu `Notifier` w swojej
ścieżce. W `labs/15-patterns-without-worship/my-notes.md` opisz własnymi słowami, co łączy te dwa
fragmenty, czego funkcja nie mogłaby zrobić, gdyby sama tworzyła `ConsoleNotifier`, oraz po jednym
zdaniu o Factory i Adapterze. Na koniec dodaj do wersji B kod `SAVE_FLAT2` (stałe 2 dolary) z
własnym testem i zapisz, ile linii i plików trzeba było zmienić. W Go po zmianie uruchamiasz
`gofmt -w .`, który zmieni wyrównanie wpisów; instrukcja zaznacza, że to oczekiwany efekt.

**Rezultat:** notatki z własnymi odpowiedziami, nie skopiowanym tekstem instrukcji; wersja B ma nowy
kod rabatowy z przechodzącym testem.

**Sprawdź się:** sekcja „Weryfikacja” sprawdza, czy plik z notatkami istnieje, i uruchamia testy
wersji B: we wszystkich ścieżkach ma ich przejść 9. Treści notatek nie sprawdza. Instrukcja kończy
się poleceniem `git status` przed Aktem IV, który zakłada czyste drzewo robocze.

## Oczekiwane rezultaty

Każde laboratorium kończy się wynikiem opisanym w sekcji „Kryteria akceptacji” jego instrukcji. Po
całym zestawie:

- masz notatki z analizą wymagań, porównaniem wersji A i B oraz odpowiedziami z laboratoriów 14 i
  15;
- obie wersje `examples/discount-codes/` w Twojej ścieżce obsługują `SAVE20`, wersja A ma
  wydzielony komponent kodów rabatowych, a wersja B dodatkowo `SAVE_FLAT2`;
- `examples/notifier/` w Twojej ścieżce ma `SilentNotifier` z przechodzącym sprawdzeniem;
- wszystko jest zapisane w commitach i wysłane na GitHuba, a drzewo robocze jest czyste przed
  Aktem IV.

## Wskazówki

- Każda instrukcja ma sekcję „Jeśli utkniesz” z podpowiedziami, osobno dla każdej ścieżki tam, gdzie
  zadanie zależy od języka.
- Pytania z sekcji „Zastanów się” pomagają ocenić to, czego nie sprawdzają polecenia weryfikacji:
  jakość pytań, porównania i wyjaśnień.
- Laboratorium 15 dodaje `SAVE_FLAT2` tylko do Twojej kopii wersji B. Instrukcja prosi, żeby nie
  dodawać tego kodu do wersji A.
