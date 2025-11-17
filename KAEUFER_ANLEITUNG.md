# Bot-Anleitung für Käufer

## Willkommen! 🎉

Du hast Zugriff auf den **Telegram Auto-Post Bot** erhalten. Der Bot läuft bereits online und ist einsatzbereit!

## Bot finden

Der Bot ist unter dem Username **@group_help** (oder dem dir mitgeteilten Username) verfügbar.

## Erste Schritte

### 1. Bot zu deiner Gruppe hinzufügen

1. Öffne deine Telegram-Gruppe
2. Gehe zu **Gruppen-Einstellungen** → **Administratoren** → **Administrator hinzufügen**
3. Suche nach dem Bot (z.B. `@group_help`)
4. Füge den Bot als **Administrator** hinzu
5. Aktiviere die Berechtigung: **Nachrichten senden**

### 2. Bot testen

Sende in deiner Gruppe:
```
/start
```

Der Bot sollte mit einer Begrüßungsnachricht und allen verfügbaren Befehlen antworten.

## Verfügbare Befehle

### 📝 Inhalte hinzufügen

- **Text hinzufügen:**
  ```
  /addtext Dein Text hier
  ```

- **Bild hinzufügen:**
  Einfach ein Bild in die Gruppe senden (Bot muss Admin sein)

- **Nachricht speichern:**
  Eine Nachricht in die Gruppe weiterleiten → wird automatisch gespeichert

### 📋 Warteschlange verwalten

- **Warteschlange anzeigen:**
  ```
  /queue
  ```

- **Fester Text setzen:**
  ```
  /settext Dein fester Text, der immer gepostet wird
  ```

- **Fester Text + Bild:**
  ```
  /setmedia
  ```
  Dann ein Bild senden

- **Zurück zur Zufalls-Warteschlange:**
  ```
  /randommode
  ```

### 🚀 Posten

- **Manuell posten:**
  ```
  /post
  ```
  Postet sofort einen zufälligen Eintrag aus der Warteschlange

- **Auto-Posting aktivieren:**
  ```
  /schedule 30min    # Alle 30 Minuten
  /schedule 1h       # Stündlich
  /schedule 4h       # Alle 4 Stunden
  /schedule daily    # Täglich um 12:00
  ```

- **Auto-Posting stoppen:**
  ```
  /stop
  ```

### 🗑️ Warteschlange leeren (nur Owner)

- **Alle Inhalte löschen:**
  ```
  /clear
  ```
  ⚠️ **Achtung:** Löscht alle gespeicherten Texte und Bilder!

## Beispiel-Workflow

### Szenario: Tägliche Motivationsposts

1. **Inhalte sammeln:**
   ```
   /addtext 🚀 Starte deinen Tag mit Energie!
   /addtext 💪 Du schaffst das!
   /addtext ✨ Heute wird ein großartiger Tag!
   ```
   (Oder Bilder senden)

2. **Auto-Posting aktivieren:**
   ```
   /schedule daily
   ```

3. **Fertig!** Der Bot postet jetzt täglich um 12:00 einen zufälligen Eintrag.

### Szenario: Fester Werbetext

1. **Festen Text setzen:**
   ```
   /settext 🎯 Besuche unsere Website: example.com
   ```

2. **Optional: Bild hinzufügen:**
   ```
   /setmedia
   ```
   Dann Logo/Bild senden

3. **Auto-Posting aktivieren:**
   ```
   /schedule 4h
   ```

4. **Fertig!** Der Bot postet jetzt alle 4 Stunden deinen festen Text (+ Bild).

## Häufige Fragen

### ❓ Bot antwortet nicht

- **Prüfe:** Ist der Bot Admin in deiner Gruppe?
- **Prüfe:** Hat der Bot Berechtigung, Nachrichten zu senden?
- **Prüfe:** Hast du `/start` gesendet?

### ❓ Auto-Posting funktioniert nicht

- **Prüfe:** Ist die Warteschlange gefüllt? (`/queue`)
- **Prüfe:** Ist Auto-Posting aktiviert? (`/schedule`)
- **Prüfe:** Ist ein fester Text gesetzt? (`/settext`)

### ❓ Warteschlange ist leer

- Füge Inhalte hinzu mit `/addtext` oder sende Bilder
- Oder setze einen festen Text mit `/settext`

### ❓ Kann ich mehrere Gruppen verwenden?

Ja! Füge den Bot einfach zu mehreren Gruppen hinzu und mache ihn in jeder Gruppe zum Admin. Der Bot verwaltet für jede Gruppe eine separate Warteschlange.

## Wichtige Hinweise

⚠️ **Berechtigungen:**
- Nur **Gruppen-Administratoren** können Befehle ausführen
- Der Bot muss **Admin** in deiner Gruppe sein

⚠️ **Warteschlange:**
- Die Warteschlange wird pro Gruppe separat gespeichert
- Bei Bot-Neustart geht die Warteschlange verloren (Backup mit `/queue`)

⚠️ **Limits:**
- Telegram hat Rate-Limits (ca. 30 Nachrichten/Sekunde)
- Der Bot respektiert diese automatisch

## Support

Bei Problemen oder Fragen:
1. Prüfe diese Anleitung
2. Teste `/start` um zu sehen, ob der Bot antwortet
3. Kontaktiere den Bot-Verkäufer

## Nützliche Tipps

💡 **Tipp 1:** Nutze `/queue` regelmäßig, um zu sehen, was gespeichert ist

💡 **Tipp 2:** Kombiniere feste Texte mit der Warteschlange für Abwechslung

💡 **Tipp 3:** Teste neue Einstellungen mit `/post` bevor du Auto-Posting aktivierst

💡 **Tipp 4:** Nutze HTML-Formatierung in Texten:
   - `<b>fett</b>` für fett
   - `<i>kursiv</i>` für kursiv
   - `<a href="url">Link</a>` für Links

---

**Viel Erfolg mit deinem Bot! 🚀**

