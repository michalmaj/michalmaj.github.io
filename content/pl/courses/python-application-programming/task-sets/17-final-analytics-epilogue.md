---
title: "Epilog analityczny: czy gra jest zbalansowana?"
summary: "Final Analytics Epilogue kursu Python RPG Questbook, po poziomie 7: trzecie spotkanie z NumPy i pandas, na danych z turniejów rozegranych przez kod gry, w jednym zadaniu Is the Game Balanced?"
status: published
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu: instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: miejsce epilogu po poziomie 7"
tasks:
  is-the-game-balanced:
    materials:
      - repository: python-rpg-questbook
        path: final_analytics_epilogue/README.md
        lang: en
        label: "Instrukcja: Final Analytics Epilogue — Is the Game Balanced?"
---
Ten zestaw obejmuje Final Analytics Epilogue kursu Python RPG Questbook. Mapa kursu umieszcza go po
poziomie 7 i opisuje jako zakończenie kursu, a nie ósmy poziom. Epilog nie wprowadza nowych pojęć
ani bibliotek. Po raz trzeci, po poziomie 1 i etapie Data Recall Checkpoint, używasz NumPy i
pandas, tym razem na danych z turniejów rozegranych przez kod gry z poziomu 7. Celem jest
odpowiedź na pytanie z poziomu 1: czy gra jest zbalansowana. Zestaw ma jedno zadanie. Instrukcja,
kod, pliki danych i komunikaty skryptu sprawdzającego są po angielsku. Ta strona streszcza je po
polsku i odsyła do instrukcji.

## Miejsce etapu w Questbooku i w przedmiocie

W ścieżce Questbooka epilog ma stałe miejsce. Mapa kursu podaje dla niego wymaganie „Level 7
complete”, a opis kursu nazywa go obowiązkowym zakończeniem kursu. Instrukcja projektu Concurrent
Tournament Runner z [zestawu 16](world-3-parallel-execution.md#concurrent-tournament-runner) kieruje
do niego jako ostatniego kroku. Narzędzie postępu pokazuje go po poziomie 7.

To opis ścieżki Questbooka, a nie zasad realizacji przedmiotu. Strona
[„Materiały przedmiotu”](../guides/course-materials.md) wymienia epilog wśród materiałów
opcjonalnych z Questbooka.

## Przygotowanie do zestawu

Instalację repozytorium opisuje część
[„Przygotowanie do zestawu”](world-1-trusted-data.md#przygotowanie-do-zestawu) zestawu 1. NumPy i
pandas instalują się razem z innymi zależnościami, podobnie jak Matplotlib do nieobowiązkowej części
„Side quest”.

**Wiedza.** Epilog zakłada znajomość NumPy i pandas z poziomu 1 Questbooka i z etapu Data Recall
Checkpoint, opisanego w [zestawie 4](data-recall-checkpoint.md). Instrukcja zawiera krótką ściągę z
potrzebnymi operacjami i odnośniki do misji 17–20 i 22 poziomu 1 oraz do Data Recall Checkpoint.
Pojęć z poziomu 7 nie potrzebujesz.

**Pliki i dane.** Nie potrzebujesz własnych danych z poziomu 7: epilog ma własne pliki w katalogu
`final_analytics_epilogue/data/`. Według instrukcji powstały przez uruchomienie kodu gry z projektu
Concurrent Tournament Runner. Skrypt `scripts/generate_fixtures.py` jest narzędziem autora kursu i
nie musisz go uruchamiać.

- `deep_dive_battles.json` zawiera 500 walk jednego, stałego starcia klasy bohatera z potworem.
- `tournament_history.csv` zawiera 45 turniejów dla wszystkich par klasy bohatera i potwora, po
  jednym wierszu na turniej. Kolumny wymienia instrukcja.
- `deep_dive_battles_variant.json` to starcie o przeciwnym wyniku.
- `tournament_history_variant.csv` ma te same dziewięć par z innym podziałem turniejów.

Dwa ostatnie pliki służą skryptowi do sprawdzenia, czy wyniki nie są wpisane na stałe.

**Polecenia.** Instrukcja podaje polecenie sprawdzenia z katalogu głównego repozytorium. Docstring
`task.py` podaje krótszą wersję, `uv run python check.py`, którą wpisuje się w katalogu
`final_analytics_epilogue/`. Obie działają.

## Sprawdzanie własnej pracy

Skrypt `check.py` uruchamia Twoje funkcje na obu parach plików danych i na kilku wycinkach
prawdziwej historii turniejów, na przykład tylko na wierszach z potworami Orc i Dragon. Wyniki
porównuje z wartościami, które sam liczy z tych plików bibliotekami standardowymi Pythona, bez
NumPy, pandas i Twojego kodu. Dlatego wynik wpisany na stałe nie przechodzi. Dodatkowo sprawdza w
kodzie techniki, które epilog ma przypomnieć: redukcje i percentyl NumPy, maski logiczne, macierz
dwuwymiarową z argumentem `axis` i `groupby` w pandas. Gdy wszystko się zgadza, skrypt wypisuje
komunikat o ukończeniu i zapisuje postęp w pliku `final_analytics_epilogue/.progress`, który jest w
`.gitignore` repozytorium. Gdy coś się nie zgadza, wypisuje, czego oczekiwał.

**Obliczenia a wnioski.** Skrypt sprawdza liczby, a nie odpowiedź na pytanie z tytułu. Instrukcja
każe po przejściu skryptu przyjrzeć się zwróconym wartościom i samodzielnie sformułować odpowiedź.
Zaznacza, że nie ma jednego poprawnego tekstu. Przejście skryptu potwierdza więc poprawność
obliczeń, ale nie poprawność wniosków. Instrukcja i docstringi przypominają też, że średnie z
historii turniejów opisują zapisaną historię, a nie stałą cechę klasy bohatera, bo próba jest mała.

## Materiały

Wszystkie materiały zestawu są po angielsku: instrukcja, kod z docstringami i komentarzami `TODO`,
pliki danych i komunikaty skryptu `check.py`.

## Zadania

### Is the Game Balanced?: NumPy i pandas na danych z turniejów {#is-the-game-balanced}

**Cel:** policzyć NumPy i pandas statystyki walk i turniejów, a potem na ich podstawie samodzielnie
odpowiedzieć na pytanie, czy gra jest zbalansowana.

**Zakres pracy:** w `final_analytics_epilogue/task.py` są funkcje, które zgłaszają
`NotImplementedError`. Instrukcja pisze o ośmiu funkcjach, ale wymienia dziewięć, i dziewięć jest w
pliku. Dokładny kontrakt każdej funkcji podaje jej docstring.

- **NumPy, jedno starcie:** `load_battle_arrays()` wczytuje walki do trzech tablic: wygranych,
  rund i złota. `deep_dive_stats()` liczy odsetek wygranych bohatera, medianę, odchylenie
  standardowe i 90. percentyl liczby rund oraz liczbę szybkich wygranych, czyli wygranych w co
  najwyżej dwóch rundach, z połączonych masek logicznych. `battle_matrix_summary()` składa wygrane i
  rundy w macierz o dwóch kolumnach i liczy średnie z `axis=0`.
- **pandas, historia turniejów:** `load_tournament_history()` wczytuje plik CSV.
  `win_rate_by_class()`, `rank_monsters()` i `unfavorable_matchups()` grupują dane przez `groupby`.
  `balance_conclusions()` zwraca najtrudniejszego potwora, najdłuższe starcie i liczbę starć
  całkowicie jednostronnych. Ta funkcja ma działać dla dowolnego fragmentu historii, nie tylko dla
  całego pliku.
- **Podsumowanie:** `build_final_report()` wywołuje funkcje powyżej i składa ich wyniki w jeden
  słownik, bez liczenia czegokolwiek od nowa.

Instrukcja wymienia cztery pytania, na które odpowiadają te wyniki. Część „Side quest” proponuje
wykres w Matplotlib, z zaznaczeniem, że nie jest wymagany ani sprawdzany.

Polecenie `uv run python final_analytics_epilogue/task.py` wypisuje wynik `build_final_report()`
dla podstawowych plików danych. Z tych wartości formułujesz odpowiedź na pytanie z tytułu.

**Rezultat:** na starcie skrypt zgłasza, że `load_battle_arrays` nie jest zaimplementowana. Po
uzupełnieniu wypisuje wyniki każdej funkcji dla obu par plików i dla wycinków historii, a na
końcu komunikat o ukończeniu.

**Sprawdź się:** `uv run python final_analytics_epilogue/check.py`. Skrypt sprawdza:

- że `load_battle_arrays()` zwraca trzy tablice NumPy o długości równej liczbie walk, z wartościami
  zgodnymi z plikiem;
- wyniki `deep_dive_stats()` i `battle_matrix_summary()` dla obu plików walk, z tolerancją 0,001;
- wyniki funkcji pandas dla obu plików historii i dla wycinków historii podstawowej;
- że `build_final_report()` dla obu par plików zwraca wartości zgodne z danymi;
- że `deep_dive_stats()` używa średniej, mediany i odchylenia standardowego NumPy, wywołuje
  `np.percentile` albo `np.quantile` i liczy szybkie wygrane z dwóch porównań połączonych przez `&`
  albo `np.logical_and`;
- że `battle_matrix_summary()` tworzy macierz dwuwymiarową i liczy średnie z argumentem `axis`;
- że `win_rate_by_class()`, `rank_monsters()` i `unfavorable_matchups()` używają `groupby`.

W kontroli nie przechodziła wersja z poprawnymi liczbami, która importowała funkcję przez
`from numpy import percentile`, bo skrypt obserwuje tylko wywołania `np.percentile` i
`np.quantile`. Instrukcja wymienia te dwie formy. Nie przechodziły też wersje z pętlą po
`.unique()` i z `pivot_table` zamiast `groupby`, bo instrukcja wymaga `groupby`. Skrypt nie ocenia
odpowiedzi na pytanie z tytułu ani części „Side quest”.

## Oczekiwane rezultaty

- `check.py` epilogu kończy się komunikatem o ukończeniu.
- Funkcje zwracają wyniki zgodne z danymi dla obu par plików i dla wycinków historii turniejów.
- Odpowiedź na pytanie, czy gra jest zbalansowana, formułujesz samodzielnie z wyników funkcji.
  Skrypt jej nie ocenia.

## Wskazówki

- Wyniki dla plików wariantowych różnią się od podstawowych. Instrukcja wyjaśnia, które
  odpowiedzi zmieniają się między plikami historii, a które nie, i dlaczego skrypt sprawdza część
  funkcji na wycinkach danych.
- Postęp zapisany przez `check.py` pokazuje polecenie `uv run python tools/course_status.py`, w
  części „Final Analytics Epilogue” po poziomie 7.
