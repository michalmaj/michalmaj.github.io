---
title: "Sekwencje i język"
summary: "Laboratoria 09–11 z repozytorium Deep Learning: klasyfikacja wiadomości SMS za pomocą GRU i LSTM, mały Transformer z maską paddingu i positional encoding oraz pipeline inferencji małego modelu językowego. Laboratoria 09 i 11 pobierają zbiór danych i model przy pierwszym uruchomieniu."
status: published
materials:
  - repository: deep-learning
    path: README.pl.md
    lang: pl
    label: "Opis kursu: konfiguracja, uruchomienie JupyterLab i pamięć podręczna danych"
  - repository: deep-learning
    path: data/registry.yml
    lang: en
    label: "Rejestr danych: źródła, licencje i sposób pobierania SMS Spam Collection i SmolLM2"
tasks:
  lab-09:
    materials:
      - repository: deep-learning
        path: labs/09_rnn/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 09 — Klasyfikacja wiadomości SMS za pomocą RNN, LSTM i GRU"
      - repository: deep-learning
        path: labs/09_rnn/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/09_rnn/lab.ipynb"
      - repository: deep-learning
        path: lectures/09_rnn/lecture.md
        lang: pl
        label: "Wykład 09: Modelowanie sekwencji za pomocą RNN, LSTM i GRU"
  lab-10:
    materials:
      - repository: deep-learning
        path: labs/10_attention/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 10 — Mały Transformer do klasyfikacji sekwencji"
      - repository: deep-learning
        path: labs/10_attention/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/10_attention/lab.ipynb"
      - repository: deep-learning
        path: lectures/10_attention/lecture.md
        lang: pl
        label: "Wykład 10: Attention i architektura Transformer"
  lab-11:
    materials:
      - repository: deep-learning
        path: labs/11_llm_engineering/README.pl.md
        lang: pl
        label: "Instrukcja: Laboratorium 11 — Pipeline inferencji małego modelu językowego"
      - repository: deep-learning
        path: labs/11_llm_engineering/lab.ipynb
        lang: pl
        label: "Notebook do uzupełnienia: labs/11_llm_engineering/lab.ipynb"
      - repository: deep-learning
        path: lectures/11_llm_engineering/lecture.md
        lang: pl
        label: "Wykład 11: Od Transformera do systemu generowania tekstu"
---
Ten zestaw obejmuje trzecią grupę laboratoriów z repozytorium Deep Learning, nazwaną w opisie kursu
„Sekwencje i język”. Klasyfikujesz prawdziwe wiadomości SMS sieciami rekurencyjnymi, budujesz mały
Transformer z jawnie zapisanym blokiem attention, a na koniec składasz i mierzysz pipeline
inferencji gotowego, małego modelu językowego. We wszystkich trzech laboratoriach ważna jest
poprawna obsługa paddingu i masek. Trzy zadania odpowiadają laboratoriom 09–11, w kolejności z
repozytorium.

## Status materiałów

Repozytorium jest w rozbudowie i jego treści mogą się jeszcze zmieniać. Ta strona opisuje instrukcje
i notebooki z gałęzi `main` (commit `0ffe385`), którą pobiera polecenie `git clone`. Wydanie
`v1.0.0` z 19 października 2026 roku zawiera starsze wersje instrukcji i notebooków tych
laboratoriów. W laboratorium 09 porównanie błędów z długością wiadomości było w wydaniu częścią
rdzenia, a na `main` jest rozszerzeniem opcjonalnym. Instrukcji i notebooka korzystaj z tej samej
wersji.

## Przygotowanie do zestawu

Środowisko jest takie samo jak w [zestawie 1](fundamentals.md): uv, Python 3.12 i polecenia z sekcji
„Konfiguracja” w opisie kursu:

```bash
git clone https://github.com/michalmaj/deep-learning.git
cd deep-learning
uv sync
uv run jupyter lab
```

Pracujesz tak samo jak w zestawie 1: instrukcja `README.pl.md`, notebook `lab.ipynb` z komórkami
`TODO` i komórki Markdown na odpowiedzi. Laboratorium 10 korzysta z zasady pomijania paddingu
poznanej w laboratorium 09, a instrukcja laboratorium 09 nawiązuje do normalizacji bez przecieku z
laboratoriów 05–07.

- **Sprzęt:** według opisu kursu wystarcza procesor (CPU). Notebooki laboratoriów 09–11 zawsze liczą
  na procesorze (`device = torch.device("cpu")`).
- **Pomiary czasu:** laboratorium 09 wypisuje czas treningu, a laboratorium 11 każe zmierzyć czas
  generowania i liczbę nowych tokenów na sekundę. Opis kursu zaznacza, że czas zależy od komputera.

## Dane i modele do pobrania

Laboratorium 10 generuje dane syntetyczne w notebooku. Laboratoria 09 i 11 pobierają dane albo model
przy pierwszym uruchomieniu. Potrzebujesz wtedy połączenia z internetem. Kolejne uruchomienia
korzystają z plików zapisanych w pamięci podręcznej.

- **SMS Spam Collection** (laboratorium 09): 5574 wiadomości z etykietami `ham` i `spam`. Archiwum z
  repozytorium UCI ma około 200 KB. Gotowy moduł `labs/09_rnn/sms_data.py` pobiera je, sprawdza sumę
  SHA-256 i zapisuje w katalogu `data_cache/`.
- **Model SmolLM2-135M-Instruct** (laboratorium 11): model z Hugging Face Hub w wersji przypiętej do
  konkretnego commita (`REVISION` w notebooku). Plik wag ma około 270 MB i trafia do pamięci
  podręcznej Hugging Face, domyślnie `~/.cache/huggingface`, a nie do `data_cache/`.

Rejestr danych w materiałach zestawu podaje źródła, licencje i sposób pobierania obu zasobów.

## Samodzielna praca i sprawdzanie wyników

Sprawdzanie działa tak samo jak w [zestawie 1](fundamentals.md). Testy repozytorium sprawdzają
szkielet notebooka, czyli to, że dostarczony kod działa do pierwszego `TODO`. Laboratoria 09–11 mają
też osobne testy wzorów i zachowań, które opisują instrukcje (np. obsługa paddingu, makro-F1,
różnica `max_length` i `max_new_tokens`). Te testy nie uruchamiają Twojego notebooka. Testy
szkieletu laboratoriów 09 i 11 pobierają dane, dlatego są oznaczone jako `network`. Gotowe asercje w
notebookach sprawdzają wybrane elementy, a opis każdego zadania podaje, które. Wyniki eksperymentów
pochodzą z Twojego przebiegu, a interpretacji w komórkach Markdown nic nie sprawdza automatycznie.
Repozytorium nie zawiera rozwiązań laboratoriów.

Każda instrukcja kończy się sekcją „Kryteria oceny”. Opisuje ona, po czym poznać merytorycznie
kompletny wynik laboratorium, i możesz jej używać do samodzielnego sprawdzenia pracy. Ta strona nie
przenosi tej sekcji i nie traktuje jej jako zasad zaliczenia przedmiotu.

## Materiały

Instrukcje i notebooki są po polsku i po angielsku. Instrukcja opisuje problem i dane, kolejne
sekcje notebooka, pytania do wniosków, rozszerzenia opcjonalne i kryteria oceny. Rejestr danych jest
po angielsku. Pełną listę wykładów i laboratoriów znajdziesz na stronie [„Materiały
przedmiotu”](../guides/course-materials.md).

## Zadania

### Klasyfikacja wiadomości SMS za pomocą RNN, LSTM i GRU {#lab-09}

Wiadomości SMS ze zbioru SMS Spam Collection trzeba zaklasyfikować jako `ham` albo `spam`. Zbiór
jest niezbalansowany, a wiadomości mają różną długość, więc batch wymaga paddingu.

**Cel:** przygotować tekst do modelu sekwencyjnego (tokenizacja, słownik tylko z danych
treningowych, `<PAD>` i `<UNK>`), zbudować klasyfikator GRU, który nie przetwarza paddingu, porównać
go z modelem bazowym bez kolejności i ocenić wynik metrykami odpowiednimi dla niezbalansowanych
danych.

**Zakres pracy:**

- **Dane i tokenizacja (sekcje 1–2):** liczysz rozkład klas `ham` i `spam` i oceniasz, czy zbiór
  jest zbalansowany. Uzupełniasz `tokenize(text)` (małe litery, słowa, cyfry i interpunkcja jako
  osobne tokeny) i w 2–3 zdaniach opisujesz ograniczenia takiej tokenizacji. Podział 70/15/15 w
  sekcji 3 jest gotowy.
- **Słownik i kodowanie (sekcje 4–5):** słownik budujesz wyłącznie z `train_texts`, z tokenami
  `<PAD>` (identyfikator 0) i `<UNK>` (identyfikator 1) oraz progiem `MIN_FREQ`. Uzupełniasz
  `encode` i sprawdzasz w kodzie, że token spoza słownika zamienia się na `<UNK>` bez wyjątku.
  Gotowe `make_batch_tensors` tworzy dopełniony batch i tensor `lengths`. Instrukcja prosi o
  wyjaśnienie, co stało się z krótszą z dwóch wiadomości w przykładowym batchu.
- **Model bazowy (sekcja 6):** w `MeanPoolBaseline.forward` uśredniasz embeddingi tylko po
  prawdziwych tokenach, z maską `x != PAD_ID` i dzieleniem przez `lengths`. Gotowe wywołanie
  `train_eval` trenuje model.
- **Klasyfikator GRU (sekcje 7–8):** w `GRUClassifier.forward` stosujesz `pack_padded_sequence`
  przed warstwą `nn.GRU` i bierzesz stan po ostatnim prawdziwym tokenie. Gotowa komórka trenuje
  model przez `train_eval`.
- **Porównanie konfiguracji (sekcja 9):** porównujesz co najmniej dwie konfiguracje na tym samym
  podziale i tych samych metrykach i w 2–3 zdaniach uzasadniasz wybór. Instrukcja wymienia GRU i
  LSTM, wymiar stanu ukrytego, dropout albo liczbę epok, a komentarz `TODO` w notebooku prowadzi
  przez `LSTMClassifier`.
- **Ewaluacja testowa (sekcja 10):** konfigurację wybierasz na podstawie walidacji i dopiero wtedy,
  pierwszy raz w laboratorium, liczysz na zbiorze testowym accuracy, macro-F1 (uzupełniasz
  `macro_f1`) i macierz pomyłek.
- **Zadanie diagnostyczne (sekcja 11):** gotowy `BuggyClassifier` trenuje się bez wyjątku, ale źle
  obsługuje padding. Wskazujesz błędną linię, wyjaśniasz, kiedy błąd się ujawnia (porównanie
  `batch_size=1` z batchem sekwencji różnej długości), poprawiasz kod i sprawdzasz poprawkę.
- **Analiza błędów (sekcja 12):** wypisujesz 5–8 błędnie sklasyfikowanych wiadomości i ustalasz, czy
  częstsze są pomyłki `ham` na `spam`, czy odwrotnie.
- **Wnioski (sekcja 13):** trzy pytania, w odniesieniu do liczb z sekcji 6–12.
- **Rozszerzenia opcjonalne:** długość poprawnie i błędnie sklasyfikowanych wiadomości,
  dwukierunkowy GRU albo LSTM (`bidirectional=True`), osobne accuracy dla krótkich i długich
  wiadomości.

**Rezultat:** notebook wykonany do końca, z rozkładem klas, słownikiem i obsługą `<UNK>`, modelem
bazowym i klasyfikatorem GRU, porównaniem konfiguracji, wynikami testowymi z macierzą pomyłek,
diagnozą paddingu, analizą błędów i wnioskami.

**Sprawdź się:**

- Gotowa asercja w sekcji 7 porównuje ten sam tekst zakodowany osobno i w batchu z dłuższą
  wiadomością. Wykrywa klasyfikator, który bierze stan z ostatniej kolumny tensora. Nie sprawdza
  modelu bazowego: uśrednianie z paddingiem przechodzi bez błędu.
- Nic nie sprawdza, czy słownik powstał tylko z `train_texts`. Słownik zbudowany na wszystkich
  danych też działa bez błędu.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

### Mały Transformer do klasyfikacji sekwencji {#lab-10}

Sekwencje syntetyczne mają losową długość od 10 do 40 tokenów i zawierają tokeny `A` i `B` wśród
dystraktorów. Etykieta mówi, czy `A` występuje przed `B`. Długość jest losowana niezależnie od
etykiety, więc model musi korzystać z kolejności. Dane generuje gotowa funkcja `make_dataset`.

**Cel:** zbudować jawny blok Transformer z maską paddingu, sprawdzić znaczenie positional encoding i
zdiagnozować błąd odwróconej konwencji maski.

**Zakres pracy:**

- **Dane (sekcja 1):** sprawdzasz liczbowo balans klas i to, że średnia długość sekwencji nie różni
  się istotnie między klasami.
- **Model bazowy (sekcja 2):** w `MeanPoolBaseline.forward` używasz gotowego `masked_mean_pool`,
  żeby uśredniać bez paddingu.
- **Maska i blok (sekcje 3–5):** decydujesz, gdzie dodać gotowe `sinusoidal_positional_encoding`.
  `make_key_padding_mask` ma zwracać `True` tam, gdzie jest padding (konwencja
  `nn.MultiheadAttention`). `TinyTransformerBlock.forward` składa attention, połączenie rezydualne i
  LayerNorm, FFN oraz drugie połączenie rezydualne i LayerNorm (wariant Post-LN), bez zastępowania
  go `nn.TransformerEncoderLayer`.
- **Klasyfikator (sekcja 6):** `Classifier.forward` łączy embedding, opcjonalne positional encoding,
  blok, maskowaną agregację z mianownikiem z `lengths` i warstwę klasyfikacyjną.
- **Trening (sekcja 7):** trenujesz `Classifier` z `use_pos_enc=True` i `use_pos_enc=False` przy tym
  samym budżecie i zapisujesz modele jako `model_with_pe` i `model_without_pe`. Gotowa pętla
  powtarza obie konfiguracje dla ziaren 0, 1 i 2.
- **Ewaluacja testowa (sekcja 8):** dla `model_with_pe`, bez ponownego treningu, liczysz accuracy
  testową i rozkład długości błędnie sklasyfikowanych przykładów.
- **Zadanie diagnostyczne (sekcja 9):** gotowy `BuggyClassifier` stosuje odwróconą konwencję maski.
  Wskazujesz błędną linię, obserwujesz stratę (także dla sekwencji o długości `MAX_LEN`, bez
  paddingu), wyjaśniasz zachowanie softmaxu bez dozwolonych kluczy, poprawiasz maskę i potwierdzasz
  `torch.isfinite`, że strata jest skończona, porównując accuracy z poprawnym modelem.
- **Wnioski (sekcja 10):** sześć pytań, w odniesieniu do wyników z sekcji 2 i 7–9, w tym o tym,
  czego eksperyment nie dowodzi.
- **Rozszerzenia opcjonalne R1–R4:** accuracy w przedziałach długości, wagi attention dla jednego
  przykładu, stos dwóch bloków, Pre-LN zamiast Post-LN.

**Rezultat:** notebook wykonany do końca, z potwierdzonym balansem i niezależnością długości,
modelem bazowym, klasyfikatorem z przechodzącą asercją, porównaniem z PE i bez PE dla trzech ziaren,
ewaluacją testową, diagnozą maski i wnioskami.

**Sprawdź się:**

- Gotowa asercja w sekcji 4 sprawdza liczbę pozycji oznaczonych jako padding w masce jednej
  sekwencji, więc wykrywa odwróconą konwencję w Twojej masce. Gotowa asercja w sekcji 6 porównuje tę
  samą sekwencję osobno i w batchu z dłuższą sekwencją. To, co ta asercja naprawdę potwierdza, jest
  tematem pytania 4 we wnioskach.
- Nic nie sprawdza, czy positional encoding rzeczywiście jest dodawany w modelu z PE. Pokaże to
  dopiero porównanie accuracy z PE i bez PE.
- Gotowa funkcja `train_eval` zwraca też dokładność testową, gotowa pętla dla trzech ziaren wypisuje
  ją dla obu konfiguracji, a komentarz `TODO` w sekcji 7 każe wypisać `test_acc`. Instrukcja i
  kryteria mówią, że zbiór testowy jest używany dopiero w sekcji 8.
- Komórki rozszerzeń R1 i R2 zgłaszają `NotImplementedError`, dopóki ich nie uzupełnisz, więc
  zatrzymują wykonywanie wszystkich komórek po kolei.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

### Pipeline inferencji małego modelu językowego {#lab-11}

Laboratorium składa pipeline inferencji gotowego modelu SmolLM2-135M-Instruct: prompt, chat
template, tokenizacja, generowanie, dekodowanie, pomiar i ocena. Modelu nie trenujesz. Prompty są po
angielsku, a odpowiedzi w komórkach Markdown po polsku. Model ma 135 milionów parametrów i według
instrukcji nie gwarantuje rozumowania wieloetapowego ani poprawności faktograficznej.

**Cel:** poprawnie przygotować wejście z chat template, wydzielić z wyjścia tylko nowe tokeny,
porównać strategie dekodowania, zmierzyć koszt generowania i oddzielić automatyczną ocenę od
jakościowego uzasadnienia.

**Zakres pracy:**

- **Model (sekcja 1):** gotowa komórka wczytuje model i tokenizer z przypiętym `revision`.
  Wypisujesz `num_attention_heads` i `num_key_value_heads`, porównujesz je i wyjaśniasz wpływ na
  pamięć KV cache.
- **Prompty (sekcja 2):** dokładnie trzy prompty w liście słowników
  `{"id", "typ", "prompt", "expected"}`: dwa jednoznaczne (np. ekstrakcja informacji i zmiana
  formatu daty) z oczekiwaną odpowiedzią zapisaną przed uruchomieniem modelu oraz jeden jakościowy z
  `expected=None`.
- **Chat template i generowanie (sekcje 3–4):** `format_prompt` korzysta z
  `tokenizer.apply_chat_template()` z `add_generation_prompt=True` i `return_dict=True`, bez
  ręcznego dodawania tokenów specjalnych. `generate_response` formatuje prompt, wywołuje
  `model.generate`, wybiera tylko nowo wygenerowane tokeny, dekoduje je z `skip_special_tokens=True`
  i zwraca tekst oraz liczbę nowych tokenów.
- **Strategie dekodowania (sekcja 5):** greedy (`do_sample=False`) dla wszystkich trzech promptów
  oraz sampling z temperaturą 0,7 i 1,3 dla jednego promptu jednoznacznego i promptu jakościowego, z
  ustawionym ziarnem przed każdym samplingiem.
- **Pomiary (sekcje 6–8):** tabela czasu i liczby nowych tokenów na sekundę dla każdej uruchomionej
  pary prompt i strategia; krótka i długa wersja jednego promptu z
  `min_new_tokens == max_new_tokens`; porównanie `use_cache=True` i `use_cache=False` przy tej samej
  długości generowania.
- **Ocena jakości (sekcja 9):** dla obu promptów jednoznacznych automatyczne sprawdzenie odpowiedzi
  greedy (`p["expected"].lower() in response.lower()`), a dla promptu jakościowego ocena każdej
  uruchomionej strategii według kryteriów z instrukcji, z uzasadnieniem opartym na konkretnym
  fragmencie odpowiedzi.
- **Zadanie diagnostyczne (sekcja 10):** gotowy kod myli `max_length` z `max_new_tokens`.
  Porównujesz liczbę nowych tokenów z `DESIRED_NEW_TOKENS`, wyjaśniasz różnicę obu parametrów,
  powtarzasz test z promptem, dla którego `prompt_len >= max_length` (instrukcja zapowiada
  `ValueError`), poprawiasz kod i potwierdzasz liczbę nowych tokenów dla obu długości promptu.
- **Wnioski (sekcja 11):** pięć pytań, w odniesieniu do wyników z sekcji 5–10.
- **Rozszerzenia opcjonalne:** R1 (dwa dodatkowe prompty z pełnym pomiarem i oceną), R2 (sampling
  dla drugiego promptu jednoznacznego i promptów z R1), szósty prompt w innym stylu, wpływ
  `repetition_penalty`.

**Rezultat:** notebook wykonany do końca, z trzema promptami i oczekiwanymi odpowiedziami,
działającymi `format_prompt` i `generate_response`, wynikami strategii dekodowania, tabelami
pomiarów, oceną automatyczną i jakościową, diagnozą `max_length` i wnioskami.

**Sprawdź się:**

- Gotowe asercje sprawdzają, że sformatowany prompt zaczyna się od tokenu specjalnego (sekcja 3) i
  że dwa wywołania greedy z tym samym promptem dają identyczny tekst (sekcja 4). Pierwsza sprawdza
  tylko pierwszy token, więc nie wykrywa braku `add_generation_prompt=True`. Druga przechodzi także
  wtedy, gdy `generate_response` dekoduje cały wynik razem z promptem. Wydzielenie nowych tokenów
  sprawdzisz po zwróconym tekście i liczbie nowych tokenów.
- Gotowa komórka sekcji 5 wybiera prompty do samplingu po identyfikatorach `extract` i `paraphrase`
  (`SAMPLING_SUBSET`), więc te identyfikatory muszą wystąpić w Twojej liście promptów.
- Automatyczne sprawdzenie z sekcji 9 dotyczy tylko podciągu oczekiwanej odpowiedzi. Oceny promptu
  jakościowego nic nie sprawdza automatycznie.
- Pozostałe elementy porównaj z sekcją „Kryteria oceny” w instrukcji.

## Oczekiwane rezultaty

- Trzy notebooki laboratoriów 09–11 wykonane od początku do końca bez błędu, z Twoim kodem w
  miejscach oznaczonych `TODO`.
- W każdym notebooku wyniki i zestawienia z Twojego przebiegu oraz odpowiedzi w komórkach Markdown,
  które odwołują się do otrzymanych liczb i przykładów.

## Wskazówki

- Pierwsze uruchomienie laboratoriów 09 i 11 pobiera dane albo model. Zrób je wtedy, gdy masz
  połączenie z internetem i wolne miejsce na dysku.
- Jeśli zmienisz funkcję zdefiniowaną wcześniej, uruchom ponownie jej komórkę i komórki, które z
  niej korzystają. Notebook pamięta stan z poprzednich uruchomień.
- Notebooki i instrukcje po angielsku (`lab.en.ipynb`, `README.md`) mają tę samą strukturę.
- Kolejny [zestaw 4, „Modelowanie generatywne”](generative-modeling.md), obejmuje laboratoria 12–13.
