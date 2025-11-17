# Bot Setup-Anleitung für Käufer

## Übersicht

Diese Anleitung zeigt dir, wie du den Telegram Auto-Post Bot nach dem Kauf einrichtest und verwendest.

## Schritt 1: Bot-Token erhalten

1. Öffne Telegram und suche nach **@BotFather**
2. Sende `/newbot` und folge den Anweisungen
3. Gib deinem Bot einen Namen (z.B. "Mein Auto-Post Bot")
4. BotFather sendet dir einen **Token** (z.B. `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
5. **WICHTIG:** Speichere diesen Token sicher!

## Schritt 2: Gruppen-ID herausfinden

1. Füge den Bot zu deiner Telegram-Gruppe hinzu
2. Mache den Bot zum **Administrator** der Gruppe
3. Füge **@userinfobot** zu deiner Gruppe hinzu
4. Sende eine Nachricht in die Gruppe
5. @userinfobot zeigt dir die **Gruppen-ID** (negativ, z.B. `-1001234567890`)
6. **WICHTIG:** Speichere diese ID

## Schritt 3: Deine Telegram-ID herausfinden

1. Öffne Telegram und suche nach **@userinfobot**
2. Starte eine private Unterhaltung mit @userinfobot
3. Sende `/start`
4. @userinfobot zeigt dir deine **Telegram-ID** (z.B. `123456789`)
5. **WICHTIG:** Speichere diese ID

## Schritt 4: Bot deployen

### Option A: Docker (empfohlen)

```bash
# 1. Repository klonen
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost

# 2. .env Datei erstellen
cp .env.example .env
nano .env
```

Füge folgendes in `.env` ein (ersetze mit deinen Werten):

```env
TOKEN=dein-bot-token-von-botfather
GROUP_ID=-1001234567890
OWNER_ID=123456789
```

```bash
# 3. Container starten
docker-compose up -d

# 4. Logs prüfen
docker-compose logs -f
```

### Option B: Render.com (Cloud)

1. Gehe zu https://render.com
2. Erstelle einen Account (kostenlos)
3. Klicke auf "New +" → "Web Service"
4. Verbinde dein GitHub Repository: `phnxvision-pixel/telegram-autopost`
5. Konfiguriere:
   - **Name:** `telegram-autopost-bot`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
6. **Environment Variables hinzufügen:**
   - `TOKEN` = dein Bot-Token
   - `GROUP_ID` = deine Gruppen-ID (negativ)
   - `OWNER_ID` = deine Telegram-ID
7. Klicke auf "Create Web Service"
8. Warte bis der Bot deployed ist (ca. 2-3 Minuten)

### Option C: Eigenen Server (Linux)

```bash
# 1. Repository klonen
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost

# 2. Python Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. Environment-Variablen setzen
export TOKEN="dein-bot-token"
export GROUP_ID="-1001234567890"
export OWNER_ID="123456789"

# 5. Bot starten
python bot.py
```

**Als Systemd Service (automatischer Start):**
Siehe `DEPLOY_LOCAL.md` für vollständige Anleitung.

## Schritt 5: Bot testen

1. Gehe zu deiner Telegram-Gruppe
2. Sende `/start` an den Bot
3. Du solltest eine Nachricht mit allen verfügbaren Befehlen erhalten
4. Teste `/addtext Test` um einen Text zur Warteschlange hinzuzufügen
5. Teste `/queue` um die Warteschlange anzuzeigen

## Schritt 6: Bot verwenden

### Grundlegende Befehle (nur Gruppen-Admins)

- `/start` - Bot-Info anzeigen
- `/addtext <Text>` - Text zur Warteschlange hinzufügen
- `/queue` - Warteschlange anzeigen
- `/post` - Manuell posten
- `/schedule <30min|1h|4h|daily>` - Auto-Posting planen
- `/stop` - Auto-Posting stoppen

### Erweiterte Funktionen

- **Bild hinzufügen:** Einfach ein Bild in die Gruppe senden (Bot muss Admin sein)
- **Nachricht weiterleiten:** Nachricht in die Gruppe weiterleiten → wird gespeichert
- **Fester Text:** `/settext Dein Text` → Bot postet immer diesen Text
- **Fester Text + Bild:** `/setmedia` → dann Bild senden
- **Zurück zur Warteschlange:** `/randommode`

### Owner-Befehle (nur du)

- `/clear` - Warteschlange komplett leeren

## Troubleshooting

### Bot antwortet nicht

1. **Prüfe ob Bot läuft:**
   ```bash
   # Docker
   docker ps
   docker logs telegram-autopost-bot
   
   # Render.com
   Prüfe Logs im Render Dashboard
   ```

2. **Prüfe Environment-Variablen:**
   - Sind TOKEN, GROUP_ID, OWNER_ID korrekt gesetzt?
   - Ist der Bot-Token gültig?

3. **Prüfe Bot-Rechte:**
   - Ist der Bot Admin in der Gruppe?
   - Hat der Bot Berechtigung, Nachrichten zu senden?

### Bot postet nicht automatisch

1. Prüfe ob Auto-Posting aktiviert ist: `/schedule 1h`
2. Prüfe ob Warteschlange gefüllt ist: `/queue`
3. Prüfe Logs auf Fehler

### Bot startet nicht

1. **Python-Version prüfen:**
   ```bash
   python3 --version  # Sollte 3.11+ sein
   ```

2. **Dependencies prüfen:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Logs prüfen:**
   ```bash
   # Docker
   docker logs telegram-autopost-bot
   
   # Direkt
   python bot.py
   ```

## Support

Bei Problemen:
1. Prüfe die Logs
2. Prüfe ob alle Environment-Variablen korrekt sind
3. Prüfe ob der Bot Admin-Rechte in der Gruppe hat
4. Prüfe die Dokumentation in `README.md`

## Wichtige Hinweise

⚠️ **Sicherheit:**
- Teile deinen Bot-Token **NIEMALS** öffentlich
- Speichere `.env` Dateien nicht in Git
- Verwende starke Passwörter für deinen Server

⚠️ **Backup:**
- Die Warteschlange wird im RAM gespeichert
- Bei Neustart geht die Warteschlange verloren
- Verwende `/queue` regelmäßig um Inhalte zu dokumentieren

⚠️ **Limits:**
- Telegram hat Rate-Limits (ca. 30 Nachrichten/Sekunde)
- Der Bot respektiert diese Limits automatisch

