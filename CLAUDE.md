# Zadania — lista zadań na iPhone'a

Osobista aplikacja to-do, używana na iPhonie jako aplikacja na ekranie początkowym (PWA).

## O użytkowniku
- Właściciel uczy się Claude Code od podstaw i nie jest programistą. Wyjaśniaj po polsku, prostym językiem, krótko mówiąc, co robisz i dlaczego.
- Rozmawiamy po polsku; teksty w aplikacji też są po polsku.

## Pliki
- `index.html` — cała aplikacja: wygląd (CSS), logika (JavaScript) i treść w jednym pliku.
- `manifest.webmanifest` — nazwa, kolory i ikony appki na ekranie początkowym.
- `sw.js` — service worker: dzięki niemu appka działa offline. **Po każdej zmianie w plikach podnieś `VERSION` w `sw.js`**, inaczej iPhone pokaże starą wersję.
- `icons/` — ikony PNG (180 px dla iPhone'a, 192 i 512 px dla manifestu), generowane skryptem `icons/make_icons.py`.

## Jak działa
- Zadania są zapisywane w pamięci telefonu (`localStorage`, klucz `zadania-v1`). Nie ma serwera ani konta.
- Każde zadanie ma pole `order` (mniejsza liczba = wyżej). Niezrobione są zawsze nad zrobionymi; zadanie nowe lub właśnie odhaczone trafia na górę swojej grupy.
- Dwie zakładki: „Do zrobienia” (domyślna) i „Zrobione”. Nie ma widoku „Wszystkie” ani przycisku × do usuwania.
- Zrobione zadania wyglądają jak niezrobione (bez przekreślenia), tylko z zielonym ptaszkiem w kółku.
- Dodawanie: pod nagłówkiem jest tylko szeroki niebieski przycisk +; po dotknięciu otwiera się okienko „Nowe zadanie” (u góry ekranu, nad klawiaturą) z polem tekstowym oraz „Anuluj” / „Dodaj”.
- Gesty (Pointer Events, działają też myszką), próg 35% szerokości wiersza, zawsze z „Cofnij”:
  - w prawo = odhacz (zielone tło); na zrobionym = przywróć (niebieskie tło),
  - w lewo = usuń (czerwone tło),
  - przeciąganie za uchwyt ≡ zmienia kolejność, z auto-przewijaniem przy krawędzi ekranu.
- Kopia zapasowa (eksport/import) została usunięta na życzenie właściciela — zadania są tylko w pamięci telefonu.
- Wygląd w stylu iOS: systemowa czcionka, kolory jako zmienne CSS w `:root`, automatyczny tryb ciemny.
- Tekst w polach ma co najmniej 16 px, żeby Safari nie powiększało strony; elementy do dotykania mają co najmniej 44 px.

## Testowanie lokalnie
```bash
py -m http.server 8765
```
Potem otwórz http://localhost:8765 w widoku telefonu.

## Publikacja
- Repozytorium: https://github.com/Izokrat500/maxtodoo (gałąź `main`, publiczne).
- Netlify (projekt `maxtodoo`, adres https://maxtodoo.netlify.app) jest połączony z GitHubem: każdy `git push` na `main` publikuje appkę automatycznie w kilkanaście sekund. Nie przeciągamy już folderu.
- Gdy właściciel napisze „opublikuj”: podnieś `VERSION` w `sw.js` (jeśli zmieniły się pliki appki), zrób commit z opisem po polsku i `git push`.
- Na iPhonie appka aktualizuje się sama przy następnym otwarciu (czasem trzeba ją zamknąć i otworzyć dwa razy). Instalacja: Safari → Udostępnij → Do ekranu początkowego.
