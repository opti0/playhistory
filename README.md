# Play History

Projekt dla szkolnego radiowęzła (LO III Wrocław). PH jest prostym narzędziem do tworzenia statystyk puszczonych utworów poprzez minimalistyczny interfejs web.

### Zależności

- python3
- flask
- sqlite

### instalacja

1. Stwórz folder z dostępem dla roota (i tylko roota)
2. `# python3 app/db.py create` aby stworzyć bazę danych
3. `# cp playhistory.service to /lib/systemd/system/playhistory.service`
4. `# systemctl enable playhistory && systemctl status playhistory`
5. Wejdź w przeglądarce _localhost__

### wyczyść bazę danych

`# python3 app/db.py create`
