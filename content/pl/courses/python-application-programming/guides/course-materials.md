---
title: "Materiały przedmiotu"
summary: "Poziomy 3–7 kursu Python RPG Questbook, przewodniki uzupełniające i etapy opcjonalne. Materiały są po angielsku."
status: published
order: 1
materials:
  - repository: python-rpg-questbook
    path: README.md
    lang: en
    label: "Opis kursu, instalacja i sposób pracy z misjami"
  - repository: python-rpg-questbook
    path: level_3_validation_and_persistence/README.md
    lang: en
    label: "Poziom 3 — Validation and Persistence: od niego zaczynasz"
  - repository: python-rpg-questbook
    path: COURSE_MAP.md
    lang: en
    label: "Mapa kursu: wszystkie poziomy i misje"
  - url: https://michalmaj.github.io/modern-python-project-guide/
    lang: en
    label: "Uzupełniająco: Modern Python Project Guide — witryna przewodnika"
  - repository: modern-python-project-guide
    path: README.md
    lang: en
    label: "Uzupełniająco: Modern Python Project Guide — repozytorium z przykładowym projektem"
  - repository: python-dev-setup-for-beginners
    path: docs/00_start_here.md
    lang: en
    label: "Uzupełniająco: Python Dev Setup for Beginners — od czego zacząć (wersja alfa)"
  - repository: python-rpg-questbook
    path: data_recall_checkpoint/README.md
    lang: en
    label: "Opcjonalnie: Data Recall Checkpoint — między poziomami 3 i 4"
  - repository: python-rpg-questbook
    path: final_analytics_epilogue/README.md
    lang: en
    label: "Opcjonalnie: Final Analytics Epilogue — po poziomie 7"
---
Instrukcje, mapy i dokumentacja techniczna wszystkich materiałów na tej stronie są dostępne po
angielsku. Ta strona wskazuje punkty wejścia i nie zawiera tłumaczeń.

## Materiał główny: poziomy 3–7 Questbooka

Poziomy 3–7 rozwijają tę samą terminalową grę RPG w coraz pełniejszą aplikację: od walidacji i
zapisu danych, przez interfejs wiersza poleceń i jakość kodu, po API i zadania w tle. Każdy poziom
zaczyna się od przygotowanej wersji gry (kod startowy w katalogu `starter_…`) z problemami, którymi
zajmujesz się na tym poziomie.

- **Od czego zacząć:** zainstaluj projekt według sekcji „Setup” w opisie repozytorium i otwórz opis
  poziomu 3.
- **Jak wygląda misja:** każda ma instrukcję (`README.md`), plik do edycji (`task.py`) i skrypt
  sprawdzający (`check.py`). Każdy poziom ma też projekty, które łączą poznane elementy.
- **Mapa kursu** (`COURSE_MAP.md`) pokazuje wszystkie misje i projekty poziomów 3–7.

| Poziom | Czego dotyczy | Stan gry na początku poziomu |
|---|---|---|
| [3 — Validation and Persistence](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_3_validation_and_persistence/README.md) | walidacja danych (Pydantic), ustawienia aplikacji, wzorzec repozytorium, zapis w SQLite | [`starter_raw_rpg/`](https://github.com/michalmaj/python-rpg-questbook/tree/main/level_3_validation_and_persistence/starter_raw_rpg): gra wczytuje i zapisuje dane bez walidacji |
| [4 — Interfaces and Reports](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_4_interfaces/README.md) | interfejs wiersza poleceń (Typer), logowanie, czytelne wyjście w terminalu (Rich), raporty, polecenie `rpg` instalowane w systemie | [`starter_verbose_rpg/`](https://github.com/michalmaj/python-rpg-questbook/tree/main/level_4_interfaces/starter_verbose_rpg): działająca gra po poziomie 3 z opisanymi problemami interfejsu |
| [5 — Production Quality and Maintainability](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_5_maintainability/README.md) | Ruff, mypy, pyright, testy i pokrycie kodu, własne wyjątki, pre-commit, CI w GitHub Actions | [`starter_unqualified_rpg/`](https://github.com/michalmaj/python-rpg-questbook/tree/main/level_5_maintainability/starter_unqualified_rpg): działająca gra bez adnotacji typów, testów, własnych wyjątków, pre-commit i CI |
| [6 — API Interface with FastAPI](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_6_api/README.md) | API w FastAPI: schematy, routery, wstrzykiwanie zależności, kody błędów, testy API | [`starter_service_ready_rpg/`](https://github.com/michalmaj/python-rpg-questbook/tree/main/level_6_api/starter_service_ready_rpg): silnik walk z warstwą usług, który wywołuje Twoje API |
| [7 — Concurrency and Background Work](https://github.com/michalmaj/python-rpg-questbook/blob/main/level_7_concurrency_and_background_work/README.md) | asyncio, zadania w tle z identyfikatorem (`job_id`), pule wątków i procesów, testy pracy w tle | [`starter_blocking_rpg_api/`](https://github.com/michalmaj/python-rpg-questbook/tree/main/level_7_concurrency_and_background_work/starter_blocking_rpg_api): API turniejów, w którym żądanie czeka na koniec całej symulacji |

## Materiały uzupełniające

- **Modern Python Project Guide** — przewodnik po strukturze projektu i narzędziach: uv,
  `pyproject.toml`, pytest, Ruff, mypy, pre-commit, GitHub Actions, MkDocs i GitHub Pages.
  Najwygodniej czytać go w
  [witrynie przewodnika](https://michalmaj.github.io/modern-python-project-guide/). Repozytorium
  zawiera też mały przykładowy projekt, na którym pokazano te narzędzia.
- **Python Dev Setup for Beginners** — przygotowanie środowiska od zera: terminal, Git, GitHub, VS
  Code i uv, osobno dla
  [Windows](https://github.com/michalmaj/python-dev-setup-for-beginners/blob/main/docs/windows/00_windows_path.md),
  [Linuksa](https://github.com/michalmaj/python-dev-setup-for-beginners/blob/main/docs/linux/00_linux_path.md)
  i [macOS](https://github.com/michalmaj/python-dev-setup-for-beginners/blob/main/docs/macos/00_macos_path.md).
  Questbook korzysta z uv, więc przewodnik przydaje się przed rozpoczęciem pracy z grą. Najnowsze
  wydanie, `v1.0.0-alpha.1`, to wersja alfa. Repozytorium opisuje ten przewodnik jako wprowadzenie
  poprzedzające Modern Python Project Guide.

## Materiały opcjonalne z Questbooka

Dwa etapy Questbooka nie wprowadzają nowych pojęć, tylko utrwalają pracę z NumPy i pandas na danych
z gry. Opis i mapa Questbooka traktują je jako stałe punkty jego ścieżki. W tym przedmiocie są
materiałem opcjonalnym.

- **Data Recall Checkpoint** (`data_recall_checkpoint/`, między poziomami 3 i 4) — analiza
  dziennika walk w formacie, który gra zapisuje od poziomu 3.
- **Final Analytics Epilogue** (`final_analytics_epilogue/`, po poziomie 7) — zakończenie
  Questbooka: analiza danych z turniejów rozegranych przez gotowy system, aby odpowiedzieć na
  pytanie, czy gra jest zbalansowana.
