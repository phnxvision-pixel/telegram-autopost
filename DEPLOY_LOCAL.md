# Lokales Deployment - Kostenlos auf eigenem Server

## Option 1: Direkt auf Linux-Server (systemd)

### Installation

```bash
# Repository klonen
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost

# Python 3.11+ installieren (falls nicht vorhanden)
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# Environment-Variablen setzen
export TOKEN="8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA"
export GROUP_ID="-1001234567890"
export OWNER_ID="123456789"
```

### Systemd Service erstellen

```bash
sudo nano /etc/systemd/system/telegram-autopost.service
```

Füge folgendes ein:

```ini
[Unit]
Description=Telegram Auto-Post Bot
After=network.target

[Service]
Type=simple
User=dein-user
WorkingDirectory=/pfad/zum/telegram-autopost
Environment="TOKEN=8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA"
Environment="GROUP_ID=-1001234567890"
Environment="OWNER_ID=123456789"
ExecStart=/pfad/zum/telegram-autopost/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Service aktivieren

```bash
# Service-Datei neu laden
sudo systemctl daemon-reload

# Service starten
sudo systemctl start telegram-autopost

# Automatischer Start beim Booten
sudo systemctl enable telegram-autopost

# Status prüfen
sudo systemctl status telegram-autopost

# Logs anzeigen
sudo journalctl -u telegram-autopost -f
```

## Option 2: Docker Deployment

### Dockerfile erstellen

Siehe `Dockerfile` in diesem Repository.

### Docker Compose (empfohlen)

```bash
docker-compose up -d
```

## Option 3: Windows Server

### Als Windows Service

Siehe `install_windows_service.bat` für automatische Installation.

### Manuell starten

```cmd
set TOKEN=8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA
set GROUP_ID=-1001234567890
set OWNER_ID=123456789
python bot.py
```

### Mit NSSM (Non-Sucking Service Manager)

```cmd
nssm install TelegramAutopostBot "C:\Python311\python.exe" "C:\pfad\zum\bot.py"
nssm set TelegramAutopostBot AppEnvironmentExtra TOKEN=8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA GROUP_ID=-1001234567890 OWNER_ID=123456789
nssm start TelegramAutopostBot
```

## Option 4: Screen/Tmux (einfach, aber nicht ideal)

```bash
# Screen installieren
sudo apt install screen -y

# Screen-Session starten
screen -S telegram-bot

# Bot starten
export TOKEN="8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA"
export GROUP_ID="-1001234567890"
export OWNER_ID="123456789"
python3 bot.py

# Detachen: Ctrl+A dann D
# Wieder verbinden: screen -r telegram-bot
```

## Vorteile eigener Server

✅ **Kostenlos** - Keine monatlichen Gebühren
✅ **Volle Kontrolle** - Eigene Ressourcen
✅ **Keine Limits** - Keine Render.com Limits
✅ **Schneller** - Direkte Verbindung

## Nachteile

❌ **Wartung** - Du musst Server selbst warten
❌ **Uptime** - Abhängig von deinem Server
❌ **Backup** - Du bist für Backups verantwortlich

