---
title: "Powtórka analizy danych: dziennik walk"
summary: "Etap Data Recall Checkpoint kursu Python RPG Questbook, między poziomami 3 i 4: powtórka pracy z NumPy i pandas na dzienniku walk w formacie z poziomu 3, w jednym zadaniu Combat Log Analytics."
status: published
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu: instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: miejsce etapu między poziomami 3 i 4"
tasks:
  combat-log-analytics:
    materials:
      - repository: python-rpg-questbook
        path: data_recall_checkpoint/README.md
        lang: en
        label: "Instrukcja: Data Recall Checkpoint — Combat Log Analytics"
---
Ten zestaw obejmuje etap Data Recall Checkpoint kursu Python RPG Questbook. Mapa kursu umieszcza go
między poziomem 3 a poziomem 4. Etap nie wprowadza nowych pojęć ani bibliotek: wracasz w nim do
NumPy i pandas i analizujesz dziennik walk w formacie, który gra zapisuje od misji 06 poziomu 3.
Zestaw ma jedno zadanie, Combat Log Analytics. Instrukcja, kod, pliki danych i komunikaty skryptu
sprawdzającego są po angielsku. Ta strona streszcza je po polsku i odsyła do instrukcji.

## Miejsce etapu w Questbooku i w przedmiocie

W ścieżce Questbooka ten etap ma stałe miejsce. Mapa kursu podaje dla niego wymaganie „Level 3
complete” i wymienia go obok poziomu 3 w wymaganiach wstępnych poziomu 4. Opis poziomu 4 podaje
tylko ukończony poziom 3. Narzędzie postępu pokazuje etap między poziomami 3 i 4.

To opis ścieżki Questbooka, a nie zasad realizacji przedmiotu. Strona
[„Materiały przedmiotu”](../guides/course-materials.md) wymienia ten etap wśród materiałów
opcjonalnych z Questbooka.

## Przygotowanie do zestawu

Instalację repozytorium opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1. NumPy i
pandas instalują się razem z innymi zależnościami.

**Wiedza.** Etap zakłada znajomość NumPy i pandas z poziomu 1 Questbooka, z części „Game Data
Analysis”. Jeśli potrzebujesz przypomnienia, instrukcja zawiera krótką ściągę z potrzebnymi
operacjami i odnośniki do misji 17, 18, 20, 21 i 22 poziomu 1. Z poziomu 3 potrzebujesz tylko
znajomości formatu dziennika walk z misji 06 ([zestaw 3](world-3-integration.md)): jeden wiersz to
jedna tura, a wynik `win` albo `loss` ma tylko ostatni wiersz walki. Wcześniejsze wiersze tej samej
walki mają wynik `ongoing`.

**Pliki i dane.** Nie potrzebujesz plików z poziomu 3 ani dziennika z własnej gry: etap ma własne
dane w katalogu `data_recall_checkpoint/data/`. Plik `combat_log_fixture.csv` ma 218 wierszy z 42
walk trzech klas bohatera (`warrior`, `mage`, `rogue`) z czterema potworami (Goblin, Orc, Troll,
Dragon). Plik `combat_log_fixture_variant.csv` ma te same kolumny, ale inne liczby i inną kolejność
trudności potworów. Kolumny są takie same jak w dzienniku z misji 06.

**Polecenia.** Polecenia z instrukcji wpisujesz w katalogu głównym repozytorium. Docstring `task.py`
podaje krótszą wersję, `uv run python check.py`, którą wpisuje się w katalogu
`data_recall_checkpoint/`. Obie działają.

## Sprawdzanie własnej pracy

Skrypt `check.py` uruchamia Twoje funkcje na obu plikach danych. Wyniki porównuje z wartościami,
które sam wylicza z tych plików zwykłym Pythonem, bez Twojego kodu. Dlatego wynik wpisany na stałe
dla jednego pliku nie przechodzi sprawdzenia na drugim. Gdy wszystko się zgadza, skrypt wypisuje
komunikat o ukończeniu i zapisuje postęp w pliku `data_recall_checkpoint/.progress`. Gdy coś się
nie zgadza, wypisuje, czego oczekiwał.

Instrukcja wymienia trzy pytania, na które odpowiadają wyniki funkcji. Skrypt sprawdza liczby, a
nie ich interpretację.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcja, kod z docstringami i komentarzami `TODO`,
pliki danych i komunikaty skryptu `check.py`.

## Zadania

### Combat Log Analytics: powtórka NumPy i pandas {#combat-log-analytics}

**Cel:** policzyć z dziennika walk to, o co pytają trzy pytania z instrukcji: która klasa bohatera
wygrywa najczęściej i z jaką przewagą, jak wygląda mocny atak (75. percentyl obrażeń) i jak często
się zdarza oraz który potwór jest najtrudniejszy według samych współczynników zwycięstw.

**Zakres pracy:** w `data_recall_checkpoint/task.py` zaimplementuj cztery funkcje. Dokładny
kontrakt każdej z nich podaje jej docstring.

- `load_combat_log(path)`: wczytanie pliku CSV biblioteką pandas, bez filtrowania wierszy.
- `win_rate_by_class(df)`: odsetek zwycięstw każdej klasy bohatera, liczony tylko na wierszach
  kończących walkę (wynik inny niż `ongoing`) i z użyciem `groupby`; wynik jako słownik.
- `damage_stats(df)`: dla wierszy z akcją `attack` średnia, odchylenie standardowe populacji
  (`std()` bez poprawki), 75. percentyl i liczba ataków silniejszych niż ten percentyl, wszystko
  obliczone w NumPy; wynik jako słownik z kluczami `mean`, `std`, `p75` i `high_damage_count`.
- `rank_monsters_by_difficulty(df)`: nazwy potworów od najtrudniejszego do najłatwiejszego, czyli od
  najniższego do najwyższego odsetka zwycięstw bohatera w zakończonych walkach.

Instrukcja wyjaśnia, dlaczego tury z miksturą (`potion`) nie należą do statystyk obrażeń: mają
`damage_dealt` równe 0, bo bohater się leczył, a nie zaatakował słabo. Docstring ostatniej funkcji
zaznacza, że „trudność” oznacza tu tylko tę jedną miarę.

**Rezultat:** uruchomiony `task.py` wczytuje podstawowy plik danych, wypisuje liczbę wierszy (218)
i wyniki trzech pozostałych funkcji. Przykład w docstringu `win_rate_by_class` podaje dla tego
pliku wartości w przybliżeniu: `{"warrior": 0.59, "mage": 0.56, "rogue": 0.78}`. Zanim uzupełnisz
funkcje, `task.py` kończy się błędem `NotImplementedError`.

**Sprawdź się:** `uv run python data_recall_checkpoint/check.py`. Skrypt na każdym z dwóch plików
danych sprawdza:

- że `load_combat_log` zwraca `DataFrame` ze wszystkimi wierszami i kolumnami pliku, a kolumna
  `damage_dealt` ma typ liczb całkowitych;
- wyniki `win_rate_by_class` i `damage_stats`, te drugie z tolerancją 0,001, oraz dokładną kolejność
  z `rank_monsters_by_difficulty`;
- że `damage_stats` wywołuje `np.percentile` albo `np.quantile`.

Na końcu sprawdza w kodzie `task.py`, że `win_rate_by_class` wywołuje `groupby`, a `damage_stats`
liczy średnią i odchylenie metodami NumPy i zlicza silne ataki maską logiczną.

Nie sprawdza, czy wynik `groupby` jest naprawdę użyty: wystarczy samo wywołanie obok obliczeń w
zwykłej pętli. Nie sprawdza też sposobu obliczeń w `rank_monsters_by_difficulty`, więc zwykła pętla
Pythona przechodzi, choć docstring opisuje grupowanie jak w `win_rate_by_class`. Nie sprawdza
wypisanego wyniku `task.py`. Te elementy porównaj samodzielnie z instrukcją i docstringami.

## Oczekiwane rezultaty

- `check.py` kończy się komunikatem o ukończeniu po sprawdzeniu obu plików danych.
- `task.py` uruchamia się bez błędów i wypisuje dla podstawowego pliku liczbę wierszy i wyniki
  trzech pozostałych funkcji.

## Wskazówki

- Ściąga w instrukcji pokazuje operacje z poziomu 1, które wystarczą w tym zadaniu: wczytanie
  pliku, filtrowanie, grupowanie, sortowanie, zamianę kolumny na tablicę NumPy, statystyki i maskę
  logiczną.
- Odsetek zwycięstw liczysz tylko na wierszach kończących walkę. W każdym z dwóch plików każda walka
  ma dokładnie jeden taki wiersz.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py` w
  części „Data Recall Checkpoint”, między poziomami 3 i 4. Jeśli nie przechodzisz poziomów 1 i 2,
  jego wiersz „Next up” wskaże misję poziomu 1.
- Następny w mapie kursu jest poziom 4, „Interfaces and Reports”.
