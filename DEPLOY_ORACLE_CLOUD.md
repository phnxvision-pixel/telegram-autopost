# Oracle Cloud Free Tier - Deployment-Anleitung

## Übersicht

Oracle Cloud bietet einen **komplett kostenlosen** VPS für immer. Perfekt für Telegram-Bots!

## Schritt 1: Account erstellen

1. Gehe zu: https://www.oracle.com/cloud/free/
2. Klicke auf "Start for Free"
3. Registriere dich mit E-Mail
4. Kreditkarte angeben (wird NICHT belastet, nur Verifizierung)
5. Warte auf Account-Aktivierung (ca. 10 Minuten)

## Schritt 2: VM erstellen

1. Logge dich ein: https://cloud.oracle.com/
2. Gehe zu **"Compute"** → **"Instances"**
3. Klicke auf **"Create Instance"**

### Konfiguration:

**Name:** `telegram-bot` (oder beliebig)

**Image:**
- **Canonical Ubuntu** → Version **22.04**

**Shape:**
- **VM.Standard.A1.Flex** (ARM, kostenlos)
- OCPU: **1**
- Memory: **6GB** (kostenlos)

**Networking:**
- VCN: Neue erstellen (automatisch)
- Subnet: Neue erstellen (automatisch)
- Public IP: ✅ Aktivieren

**SSH Keys:**
- **Generate a key pair for me** → Download Private Key
- Oder: Deinen eigenen SSH-Key hochladen

4. Klicke auf **"Create"**
5. Warte 2-3 Minuten bis VM läuft

## Schritt 3: Firewall-Regeln setzen

1. Gehe zu **"Networking"** → **"Security Lists"**
2. Wähle deine Security List
3. Klicke auf **"Add Ingress Rules"**
4. Regel hinzufügen:
   - **Source:** `0.0.0.0/0`
   - **IP Protocol:** TCP
   - **Destination Port Range:** `22`
   - Klicke auf **"Add Ingress Rules"**

## Schritt 4: SSH-Verbindung

**Windows:**
```powershell
# PuTTY verwenden oder WSL
ssh -i dein-private-key.key ubuntu@<PUBLIC_IP>
```

**Linux/Mac:**
```bash
chmod 400 dein-private-key.key
ssh -i dein-private-key.key ubuntu@<PUBLIC_IP>
```

**Public IP** findest du in der Instance-Übersicht.

## Schritt 5: Docker installieren

```bash
# System aktualisieren
sudo apt update
sudo apt upgrade -y

# Docker installieren
sudo apt install docker.io docker-compose -y

# Docker starten
sudo systemctl start docker
sudo systemctl enable docker

# Docker ohne sudo nutzen (optional)
sudo usermod -aG docker ubuntu
# Dann neu einloggen: exit und wieder ssh
```

## Schritt 6: Bot deployen

```bash
# Repository klonen
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost

# .env Datei erstellen
nano .env
```

Füge folgendes ein:
```env
TOKEN=dein-bot-token
OWNER_ID=deine-telegram-id
```

Speichern: `Ctrl+X`, dann `Y`, dann `Enter`

```bash
# Container starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f
```

## Schritt 7: Bot testen

1. Gehe zu deiner Telegram-Gruppe
2. Sende `/start`
3. Bot sollte antworten

## Schritt 8: Auto-Start einrichten (optional)

```bash
# Systemd Service erstellen
sudo nano /etc/systemd/system/telegram-bot.service
```

Füge ein:
```ini
[Unit]
Description=Telegram Auto-Post Bot
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/telegram-autopost
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
# Service aktivieren
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

## Nützliche Befehle

```bash
# Bot-Status prüfen
docker ps

# Logs anzeigen
docker-compose logs -f

# Bot neu starten
docker-compose restart

# Bot stoppen
docker-compose down

# Bot aktualisieren
git pull
docker-compose up -d --build
```

## Troubleshooting

### SSH-Verbindung funktioniert nicht

1. Prüfe Firewall-Regeln (Port 22 muss offen sein)
2. Prüfe Public IP in Instance-Übersicht
3. Warte 2-3 Minuten nach VM-Erstellung

### Docker-Befehl nicht gefunden

```bash
# Docker-Pfad prüfen
which docker
# Falls nicht gefunden:
sudo apt install docker.io -y
```

### Bot startet nicht

```bash
# Logs prüfen
docker-compose logs

# .env Datei prüfen
cat .env

# Container neu bauen
docker-compose up -d --build
```

## Kosten

**✅ Komplett kostenlos!**

Oracle Cloud Free Tier bietet:
- 2 AMD VMs ODER 4 ARM VMs
- 200GB Storage
- 10TB Bandbreite/Monat
- **Für immer kostenlos** (kein Ablaufdatum)

## Vorteile

- ✅ Komplett kostenlos
- ✅ 24/7 Online
- ✅ Keine Sleep-Mode
- ✅ Genug Ressourcen für 100+ Gruppen
- ✅ Volle Kontrolle
- ✅ Keine Limits

## Nachteile

- ⚠️ Kreditkarte nötig (wird nicht belastet)
- ⚠️ Account-Verifizierung kann 10-30 Minuten dauern

## Alternative: AMD VM (weniger RAM, aber mehr CPU)

Falls ARM nicht verfügbar:
- **VM.Standard.E2.1.Micro** (AMD)
- 1 OCPU, 1GB RAM
- Auch kostenlos

## Fazit

Oracle Cloud Free Tier ist die **beste kostenlose Option** für Telegram-Bots:
- Komplett kostenlos
- 24/7 Online
- Genug Ressourcen
- Keine Limits

**Perfekt für Verkäufer mit mehreren Käufern!**

