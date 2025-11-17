# Verkäufer-Setup - Bot für mehrere Käufer einrichten

## Übersicht

Diese Anleitung zeigt dir, wie du den Bot so einrichtest, dass mehrere Käufer ihn gleichzeitig verwenden können.

## Konzept

- **Ein Bot** läuft auf deinem Server
- **Mehrere Gruppen** können den Bot verwenden
- Jede Gruppe hat eine **separate Warteschlange**
- Jeder Käufer bekommt Zugriff auf **seine eigene Gruppe**

## Setup für Verkäufer

### Schritt 1: Bot erstellen und deployen

1. **Bot bei @BotFather erstellen:**
   ```
   /newbot
   ```
   - Name: z.B. "Group Help Bot"
   - Username: z.B. `@group_help`

2. **Bot deployen:**
   - **WICHTIG:** Verwende `bot_multi_group.py` für Multi-Group Support!
   - In `docker-compose.yml` oder `bot.py` durch `bot_multi_group.py` ersetzen
   - Siehe `DOCKER_DEPLOY.md` oder `DEPLOY_LOCAL.md`
   - Bot läuft auf deinem Server
   
   **Für Docker:** Ändere `CMD ["python", "bot.py"]` zu `CMD ["python", "bot_multi_group.py"]` im Dockerfile

### Schritt 2: Bot für Käufer freigeben

**Option A: Jeder Käufer bekommt eine eigene Gruppe**

1. Käufer erstellt eine Telegram-Gruppe
2. Käufer fügt Bot hinzu: `@group_help`
3. Käufer macht Bot zum Admin
4. Bot funktioniert automatisch in dieser Gruppe

**Option B: Käufer nutzen den Bot in bestehenden Gruppen**

1. Käufer fügt Bot zu seiner Gruppe hinzu
2. Käufer macht Bot zum Admin
3. Bot funktioniert automatisch

### Schritt 3: Bot-Konfiguration

Der Bot unterstützt **automatisch mehrere Gruppen**. Jede Gruppe hat:
- Eigene Warteschlange
- Eigene Einstellungen (fester Text, Auto-Posting)
- Eigene Admin-Rechte

**Keine zusätzliche Konfiguration nötig!**

## Bot-Verwaltung

### Bot-Status prüfen

```bash
# Docker
docker ps
docker logs telegram-autopost-bot -f

# Systemd
systemctl status telegram-autopost
journalctl -u telegram-autopost -f
```

### Bot neu starten

```bash
# Docker
docker-compose restart

# Systemd
systemctl restart telegram-autopost
```

### Updates einspielen

```bash
git pull
docker-compose up -d --build
# oder
systemctl restart telegram-autopost
```

## Käufer-Onboarding

### Was Käufer brauchen:

1. **Bot-Username:** z.B. `@group_help`
2. **Anleitung:** `KAEUFER_ANLEITUNG.md`
3. **Zugriff:** Bot zu ihrer Gruppe hinzufügen

### Onboarding-Prozess:

1. Käufer erhält Bot-Username und Anleitung
2. Käufer fügt Bot zu seiner Gruppe hinzu
3. Käufer macht Bot zum Admin
4. Käufer testet mit `/start`
5. **Fertig!** Bot ist einsatzbereit

## Skalierung

### Wie viele Gruppen kann der Bot gleichzeitig bedienen?

- **Theoretisch:** Unbegrenzt (Telegram-Limits beachten)
- **Praktisch:** Abhängig von Server-Ressourcen
- **Empfohlen:** Bis zu 1000 Gruppen pro Bot-Instanz

### Server-Ressourcen

**Minimal:**
- 1 CPU Core
- 512 MB RAM
- 10 GB Storage

**Empfohlen (100+ Gruppen):**
- 2 CPU Cores
- 2 GB RAM
- 50 GB Storage

## Monitoring

### Logs prüfen

```bash
# Alle Gruppen
docker logs telegram-autopost-bot -f

# Nach Gruppen-ID filtern
docker logs telegram-autopost-bot 2>&1 | grep "-1001234567890"
```

### Bot-Status

Der Bot loggt:
- Befehle von Admins
- Postings
- Fehler
- Gruppen-Wechsel

## Troubleshooting

### Bot antwortet nicht in einer Gruppe

1. Prüfe ob Bot Admin ist
2. Prüfe Bot-Logs
3. Prüfe ob Gruppe-ID korrekt ist

### Bot stürzt ab

1. Prüfe Server-Ressourcen
2. Prüfe Logs auf Fehler
3. Prüfe ob TOKEN gültig ist

### Käufer hat Probleme

1. Prüfe ob Bot in Gruppe ist
2. Prüfe ob Bot Admin ist
3. Verweise auf `KAEUFER_ANLEITUNG.md`

## Sicherheit

### Bot-Token schützen

- **NIEMALS** Token öffentlich teilen
- Token nur in `.env` speichern
- `.env` nicht in Git committen

### Admin-Rechte

- Bot sollte nur **notwendige** Admin-Rechte haben
- Empfohlen: Nur "Nachrichten senden"

### Rate-Limits

- Bot respektiert Telegram-Limits automatisch
- Bei vielen Gruppen: Monitoring aktivieren

## Support für Käufer

### Häufige Fragen

1. **"Bot antwortet nicht"**
   - Bot muss Admin sein
   - `/start` senden

2. **"Auto-Posting funktioniert nicht"**
   - Warteschlange prüfen (`/queue`)
   - Auto-Posting aktivieren (`/schedule`)

3. **"Wie füge ich Inhalte hinzu?"**
   - `/addtext` für Text
   - Bilder senden für Bilder

### Support-Kanal

- Erstelle eine Support-Gruppe
- Oder nutze E-Mail/Telegram für Support
- Verweise auf `KAEUFER_ANLEITUNG.md`

## Preismodell

### Mögliche Modelle:

1. **Einmalzahlung:** Käufer kauft Zugriff auf Bot
2. **Monatlich:** Abo-Modell
3. **Pro Gruppe:** Preis pro Gruppe/Monat

### Technische Umsetzung:

- Bot läuft auf deinem Server
- Käufer erhalten Bot-Username
- Keine technische Konfiguration nötig
- Bot funktioniert automatisch in jeder Gruppe

## Checkliste für Verkäufer

- [ ] Bot bei @BotFather erstellt
- [ ] Bot auf Server deployed
- [ ] Bot läuft stabil
- [ ] Käufer-Anleitung bereit (`KAEUFER_ANLEITUNG.md`)
- [ ] Support-Kanal eingerichtet
- [ ] Monitoring aktiviert
- [ ] Backup-Strategie definiert

---

**Viel Erfolg mit deinem Bot-Geschäft! 💰**

