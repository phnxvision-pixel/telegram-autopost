# Telegram Auto-Post Bot

Bot für automatisches Posten in Telegram-Gruppen mit Admin-Rechten.

## Features

- **Admin-Only**: Nur Gruppen-Administratoren können Befehle ausführen
- **Warteschlange**: Zufällige Auswahl aus gespeicherten Texten/Bildern
- **Fester Modus**: Fester Text/Bild für wiederkehrende Posts
- **Auto-Posting**: Planbare automatische Posts (30min, 1h, 4h, daily)
- **Manuelles Posten**: Sofortiges Posten auf Befehl

## Befehle (nur Admins)

- `/start` - Bot-Info anzeigen
- `/addtext <Text>` - Text zur Warteschlange hinzufügen
- `/queue` - Warteschlange anzeigen
- `/settext <Text>` - Fester Text setzen (wird immer gepostet)
- `/setmedia` - Fester Text + Bild kombinieren
- `/randommode` - Zurück zur Zufalls-Warteschlange
- `/post` - Manuell posten
- `/schedule <30min|1h|4h|daily>` - Auto-Posting planen
- `/stop` - Auto-Posting stoppen

## Befehle (nur Owner)

- `/clear` - Warteschlange leeren

## Installation

1. Repository klonen
2. Dependencies installieren: `pip install -r requirements.txt`
3. Environment-Variablen setzen:
   - `TOKEN` - Bot-Token von @BotFather
   - `GROUP_ID` - Gruppen-ID (negativ)
   - `OWNER_ID` - Deine Telegram-ID
4. Bot starten: `python bot.py`

## Deployment-Optionen

### Option 1: Render.com (Cloud - kostenpflichtig)

1. **Neuen Web Service erstellen**
   - Repository: `https://github.com/phnxvision-pixel/telegram-autopost`
   - Environment: `Python 3`
   - Region: `Frankfurt` (oder deine Präferenz)

2. **Build Command:**
   ```
   pip install -r requirements.txt
   ```

3. **Start Command:**
   ```
   python bot.py
   ```

4. **Environment-Variablen setzen:**
   - `TOKEN` = `8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA`
   - `GROUP_ID` = Deine Gruppen-ID (negativ, z.B. `-1001234567890`)
   - `OWNER_ID` = Deine Telegram-ID (z.B. `123456789`)

5. **Deploy** → Bot läuft automatisch

### Option 2: Docker (empfohlen für eigene Server)

**Schnellstart mit Docker Compose:**

```bash
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost

# .env Datei erstellen
cp .env.example .env
nano .env  # Token, GROUP_ID, OWNER_ID eintragen

# Container starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f
```

**Siehe `DOCKER_DEPLOY.md` für vollständige Docker-Anleitung.**

### Option 3: Eigenen Server (ohne Docker)

**Schnellstart auf Linux:**

```bash
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export TOKEN="8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA"
export GROUP_ID="-1001234567890"
export OWNER_ID="123456789"
python bot.py
```

**Als Systemd Service (automatischer Start):**

Siehe `DEPLOY_LOCAL.md` für vollständige Anleitung mit systemd oder Windows Service.

**Vorteile eigener Server:**
- ✅ Kostenlos
- ✅ Volle Kontrolle
- ✅ Keine Limits

## Technologie

- Python 3.11+
- python-telegram-bot 20.7

