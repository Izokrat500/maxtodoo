# Dodo — lista zadań na iPhone'a

Osobista aplikacja to-do, używana na iPhonie jako aplikacja na ekranie początkowym (PWA).

## O użytkowniku
- Właściciel uczy się Claude Code od podstaw i nie jest programistą. Wyjaśniaj po polsku, prostym językiem, krótko mówiąc, co robisz i dlaczego.
- Rozmawiamy po polsku; teksty w aplikacji też są po polsku.

## Pliki
- `index.html` — cała aplikacja: wygląd (CSS), logika (JavaScript) i treść w jednym pliku.
- `manifest.webmanifest` — nazwa, kolory i ikony appki na ekranie początkowym.
- `sw.js` — service worker: dzięki niemu appka działa offline. **Po każdej zmianie w plikach podnieś `VERSION` w `sw.js`**, inaczej iPhone pokaże starą wersję.
- `icons/` — logo appki: źródło `dodo.svg` (maskotka dodo z zielonym ptaszkiem na niebieskim tle) i ikony PNG (180 px dla iPhone'a, 192 i 512 px dla manifestu), generowane przez `icons/render_icons.ps1` (Edge w trybie headless). Po zmianie SVG uruchom skrypt ponownie.

## Jak działa
- Zadania są zapisywane w pamięci telefonu (`localStorage`, klucz `zadania-v1`). Nie ma serwera ani konta.
- Każde zadanie ma pole `order` (mniejsza liczba = wyżej). Niezrobione są zawsze nad zrobionymi; zadanie nowe lub właśnie odhaczone trafia na górę swojej grupy.
- Cztery zakładki: „Do zrobienia” (domyślna), „Zrobione”, „Codzienne” i „Sklep”. Nie ma widoku „Wszystkie” ani przycisku × do usuwania.
- Przy zadaniach nie ma klikalnego kółka — zadania odhacza się i usuwa wyłącznie gestami. Zrobione (zakładka „Zrobione” i „Zrobione dziś”) wyglądają jak niezrobione (bez przekreślenia), tylko z nieklikalnym zielonym ptaszkiem po lewej.
- Dodawanie: pod nagłówkiem jest szeroki złoty przycisk „Nowe zadanie”; po dotknięciu otwiera się okienko „Nowe zadanie” (u góry ekranu, nad klawiaturą) z polem tekstowym, wyborem kategorii (chipy) oraz „Anuluj” / „Dodaj”.
- Kategorie (localStorage `dodo-kategorie`: `{id, name, collapsed}`, zadanie ma pole `cat`):
  - przycisk „+ Nowa kategoria” pod niebieskim przyciskiem,
  - w „Do zrobienia”: najpierw zadania bez kategorii, potem zwijane sekcje (▾/▸ zapamiętane) z licznikiem, własnym „+” i menu „⋯” (zmień nazwę / usuń),
  - usunięcie kategorii usuwa też jej zadania (z „Cofnij”),
  - dotknięcie tekstu zadania otwiera okienko „Zadanie”: zmiana treści i przeniesienie do innej kategorii,
  - przeciąganie zadania za ≡ działa w obrębie jednej kategorii,
  - kategorie przesuwa się za ≡ w ich nagłówku (widoczny, gdy są co najmniej dwie); na czas przeciągania wszystkie zwijają się do nagłówków, a po puszczeniu wracają do swojego stanu; kolejność to kolejność w tablicy `dodo-kategorie`; zadania bez kategorii zostają zawsze na górze,
  - „Zrobione” to jedna lista z szarym podpisem kategorii pod zadaniem.
- Zakładka „Codzienne” (localStorage `dodo-codzienne`: `{id, text, order, doneDate}`):
  - zadanie jest „zrobione”, gdy `doneDate` to dzisiejsza data lokalna (`RRRR-MM-DD`) — nowego dnia wraca samo, bez żadnego resetu,
  - w prawo = zrobione na dziś (znika do zwijanej sekcji „Zrobione dziś”, stan zwinięcia w `dodo-codzienne-zwiniete`), w lewo = usuń na stałe, dotknięcie = zmiana treści,
  - kolejność stała (nie zmienia się po odhaczeniu), przeciąganie za ≡; nowe na koniec; bez kategorii,
  - zmiana dnia sprawdzana co 30 s oraz przy powrocie do appki (`visibilitychange`, `focus`),
  - w tej zakładce złoty przycisk dodaje codzienne, przycisk „Nowa kategoria” jest ukryty, nad listą jest pasek „X z Y”.
- Grywalizacja (localStorage `dodo-gra`: `{hp, coins, settled}`):
  - u góry ekranu: duży okrągły awatar dodo, pasek życia (max 50 HP; pomarańczowy ≤ 50%, czerwony pulsujący ≤ 20%) i monety; ikony serca i monety to własne SVG w kodzie,
  - nagrody od razu przy odhaczeniu gestem (`applyReward` w `setDone` / `setDailyDone`): codzienne +1 moneta i +1 HP, z „Do zrobienia” +2 monety i +2 HP; przywrócenie / „Cofnij” zabiera je z powrotem (bez nabijania); usunięcie zrobionego zadania ich nie zabiera,
  - HP nie przekracza 50, dlatego zadanie pamięta w `hpGain`, ile serduszek faktycznie dało, i przy cofnięciu odejmowane jest dokładnie tyle,
  - życie: po zakończeniu dnia każde codzienne niezrobione tego dnia (`doneDate !== dzień`) = −1 HP; zadania z „Do zrobienia” nie odbierają życia; HP nie spada poniżej 0,
  - `settleDays()` rozlicza HP za wszystkie dni od `settled` + 1 do wczoraj (także kilka dni przerwy); zadanie liczy się dopiero od swojego `createdDate`,
  - po rozliczeniu okienko „Nowy dzień!” z podsumowaniem i stratą życia; rozliczenie przy starcie appki i przy zmianie dnia (`checkNewDay`).
- Sklep (czwarta zakładka; `game.owned` = kupione, `game.hat` = noszony, w `dodo-gra`):
  - 10 kapeluszy w tablicy `HATS` (ceny 100–1000 monet), rysowane w kodzie jako SVG z kształtów `tricorn` / `bicorn` / `cavalier` / `capotain` i ozdób (`plume`, `tallPlume`, `skull`, `bones`, `gem`, `cockade`, `pearls`),
  - dotknięcie grafiki = darmowa przymiarka w podglądzie, przycisk = Kup / Załóż / Zdejmij; po zakupie „Cofnij” zwraca monety,
  - awatar to jeden rysunek SVG z `avatarSvg(hat)`: dodo i kapelusz razem, wszystko mieści się w kole (w kapeluszu dodo jest mniejszy i niżej); koło ma 128 px u góry ekranu i 240 px w sklepie.
- Gesty (Pointer Events, działają też myszką), próg 35% szerokości wiersza, zawsze z „Cofnij”:
  - w prawo = odhacz (zielone tło); na zrobionym = przywróć (niebieskie tło),
  - w lewo = usuń (czerwone tło),
  - przeciąganie za uchwyt ≡ zmienia kolejność, z auto-przewijaniem przy krawędzi ekranu.
- Kopia zapasowa (eksport/import) została usunięta na życzenie właściciela — zadania są tylko w pamięci telefonu.
- Wygląd „Nocny rejs”: granat i złoto, jeden ciemny motyw (bez trybu jasnego), systemowa czcionka, kolory jako zmienne CSS w `:root`.
- Układ: u góry na środku dodo (ukryty w Sklepie, gdzie jest duży podgląd), tytuł zależny od zakładki, życie i monety; złoty przycisk „Nowe zadanie”; zakładki w dolnym pasku z ikonami (`.seg`); w „Codziennych” pasek postępu dnia; po odhaczeniu monety i serduszka lecą do paska na górze (`flyRewards`).
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
