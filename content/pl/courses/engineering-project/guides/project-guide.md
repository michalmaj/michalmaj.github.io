---
title: "Wskazówki do pracy nad projektem"
summary: "Praktyczne wskazówki do pracy nad projektem: od określenia problemu do prezentacji rezultatów."
status: published
order: 1
---
Ta strona zbiera ogólne, praktyczne wskazówki do pracy nad projektem inżynierskim. Są to dobre
praktyki warsztatowe, a nie wymagania. Strona nie jest programem zajęć i nie zastępuje ustaleń z
prowadzącym.

**Wymagania formalne, obowiązkowe etapy i dokumenty, terminy oraz zasady zaliczenia** nie są
opisane na tej stronie. Obowiązują w tym zakresie aktualne dokumenty uczelni i ustalenia z
prowadzącym.

## Problem

- Opisz problem w dwóch, trzech zdaniach: kogo dotyczy, w jakiej sytuacji występuje i co dziś nie
  działa albo działa źle.
- Oddziel problem od rozwiązania. „Aplikacja w technologii X” to rozwiązanie, a problem to
  potrzeba, na którą ta aplikacja ma odpowiedzieć.
- Sprawdź, jak problem rozwiązują istniejące narzędzia, i nazwij, czym Twój projekt się od nich
  różni.

## Zakres

- Podziel funkcje na niezbędne, pożądane i świadomie pominięte. Lista pominiętych chroni projekt
  przed rozrastaniem się.
- Dla każdej niezbędnej funkcji zapisz, po czym poznasz, że jest gotowa.
- Zapisz założenia i ograniczenia: dane, sprzęt, dostęp do systemów, czas.
- Mniejszy projekt, który działa i jest sprawdzony, jest lepszy niż duży i niedokończony.

## Projekt rozwiązania

- Zacznij od widoku całości: główne komponenty, przepływ danych i połączenia między nimi. Prosty
  diagram wystarczy.
- Uzasadnij wybór technologii wymaganiami projektu, a nie samą popularnością.
- Wskaż największe ryzyka techniczne i sprawdź je wcześnie, małym prototypem.

## Implementacja i weryfikacja

- Pracuj małymi krokami i trzymaj kod w systemie kontroli wersji, z czytelnymi opisami zmian.
- Testami automatycznymi obejmij przede wszystkim najważniejszą logikę.
- Sprawdzaj wynik względem kryteriów z zakresu, a nie tylko tego, że „działa u mnie”.
- Napisz instrukcję uruchomienia i sprawdź ją w czystym środowisku albo poproś o to inną osobę.

## Decyzje techniczne

- Ważne decyzje zapisuj na bieżąco, krótko: kontekst, rozważane możliwości, wybór i jego
  konsekwencje. Taki zapis bywa nazywany ADR (architecture decision record).
- Zapisuj też porzucone podejścia i powód rezygnacji. Przydają się, gdy trzeba wyjaśnić, dlaczego
  rozwiązanie wygląda tak, a nie inaczej.
- Trzymaj notatki blisko kodu, np. w repozytorium projektu, żeby zmieniały się razem z nim.

## Prezentacja i demonstracja

- Ułóż prezentację w kolejności: problem, rozwiązanie, demonstracja, wyniki weryfikacji,
  ograniczenia.
- Przygotuj scenariusz demonstracji na sprawdzonych danych i plan awaryjny, np. nagranie albo
  zrzuty ekranu.
- Powiedz wprost, czego projekt nie robi i co można by rozwinąć dalej.
- Przećwicz prezentację z pomiarem czasu.
