# Play History

Projekt dla szkolnego radiowęzła (LO III Wrocław). PH jest prostym narzędziem do tworzenia statystyk puszczonych utworów poprzez minimalistyczny interfejs web.

### instalacja

1. Stwórz folder z dostępem dla roota (i tylko roota)
2. `# python3 app/db.py create` aby stworzyć bazę danych
3. Uzupełnij w pliku `config.py` dane serwera pocztowego dla zamówień,
4. `# cp playhistory.service to /lib/systemd/system/playhistory.service`
5. `# systemctl enable playhistory && systemctl status playhistory`
6. Wejdź w przeglądarce _localhost_

### wyczyść bazę danych

`# python3 app/db.py create`
