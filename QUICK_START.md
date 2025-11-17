# Quick Start - Bot in 5 Minuten einrichten

## Für Käufer - Schnellste Einrichtung

### 1. Bot-Token holen (2 Minuten)

1. Telegram → @BotFather → `/newbot`
2. Token kopieren (z.B. `123456789:ABC-DEF...`)

### 2. IDs herausfinden (2 Minuten)

1. **Gruppen-ID:** Bot zur Gruppe hinzufügen → @userinfobot → Gruppen-ID kopieren
2. **Deine ID:** @userinfobot privat → `/start` → Deine ID kopieren

### 3. Deployen (1 Minute)

**Docker (einfachste Methode):**

```bash
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost
cp .env.example .env
nano .env  # Token, GROUP_ID, OWNER_ID eintragen
docker-compose up -d
docker-compose logs -f
```

**Fertig!** Bot läuft jetzt.

### 4. Testen

In deiner Gruppe: `/start` → Bot sollte antworten.

## Nächste Schritte

- Inhalte hinzufügen: `/addtext Dein Text` oder Bilder senden
- Auto-Posting aktivieren: `/schedule 1h`
- Warteschlange prüfen: `/queue`

Siehe `SETUP_GUIDE.md` für vollständige Anleitung.

