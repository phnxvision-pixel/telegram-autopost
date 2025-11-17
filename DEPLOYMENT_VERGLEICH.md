# Deployment-Optionen Vergleich - Kostenlos

## 🏆 Empfehlung: Eigenen Server (VPS)

**Warum?**
- ✅ Komplett kostenlos (wenn du einen Server hast)
- ✅ Volle Kontrolle
- ✅ Keine Limits
- ✅ Beste Performance
- ✅ Multi-Group Support ohne Probleme

## Option 1: Eigenen Server/VPS (BESTE WAHL)

### Kostenlose VPS-Anbieter:

#### 1. **Oracle Cloud Free Tier** ⭐ EMPFOHLEN
- **Kosten:** Komplett kostenlos (für immer)
- **Ressourcen:** 
  - 2 AMD VMs (1/8 OCPU, 1GB RAM)
  - Oder 4 ARM VMs (24GB RAM gesamt)
- **Storage:** 200GB Block Storage
- **Bandbreite:** 10TB/Monat
- **Link:** https://www.oracle.com/cloud/free/

**Setup:**
```bash
# Ubuntu 22.04 installieren
# Dann:
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost
docker-compose up -d
```

#### 2. **Google Cloud Free Tier**
- **Kosten:** $300 Credits für 90 Tage, danach kostenlos (mit Limits)
- **Ressourcen:** f1-micro Instanz (1 vCPU, 0.6GB RAM)
- **Storage:** 30GB
- **Link:** https://cloud.google.com/free

#### 3. **AWS Free Tier**
- **Kosten:** 12 Monate kostenlos, danach kostenpflichtig
- **Ressourcen:** t2.micro (1 vCPU, 1GB RAM)
- **Storage:** 30GB
- **Link:** https://aws.amazon.com/free/

#### 4. **Azure Free Tier**
- **Kosten:** $200 Credits für 30 Tage, danach kostenlos (mit Limits)
- **Ressourcen:** B1S VM (1 vCPU, 1GB RAM)
- **Storage:** 64GB
- **Link:** https://azure.microsoft.com/free/

### Eigenen Server zu Hause

**Vorteile:**
- ✅ Komplett kostenlos
- ✅ Volle Kontrolle
- ✅ Keine Cloud-Abhängigkeit

**Nachteile:**
- ❌ Stromkosten (~5-10€/Monat)
- ❌ Internet-Abhängigkeit
- ❌ Wartung nötig

**Hardware-Anforderungen:**
- Raspberry Pi 4 (4GB RAM) → ~50€ einmalig
- Oder alter PC/Laptop
- 24/7 Internet-Verbindung

## Option 2: Render.com Free Tier

**Kosten:** Kostenlos mit Limits

**Limits:**
- ❌ Service schläft nach 15 Minuten Inaktivität ein
- ❌ Langsamer Start nach Sleep (~30 Sekunden)
- ❌ Nicht ideal für Telegram-Bots (müssen immer online sein)

**Für Telegram-Bots:** ❌ Nicht empfohlen (Bot muss 24/7 laufen)

## Option 3: Railway.app

**Kosten:** $5/Monat nach Free Tier

**Free Tier:**
- $5 Credits/Monat
- Läuft ca. 1 Monat kostenlos
- Danach kostenpflichtig

**Für Telegram-Bots:** ⚠️ Nur kurzfristig kostenlos

## Option 4: Fly.io

**Kosten:** Kostenlos mit Limits

**Limits:**
- 3 VMs kostenlos
- Shared CPU
- 3GB RAM gesamt

**Für Telegram-Bots:** ✅ Gut geeignet, aber Limits beachten

## Option 5: Heroku (nicht mehr kostenlos)

**Status:** ❌ Free Tier wurde eingestellt (2022)
- Ab $7/Monat

## Vergleichstabelle

| Anbieter | Kosten | RAM | CPU | 24/7 | Empfehlung |
|----------|--------|-----|-----|------|------------|
| **Oracle Cloud** | ✅ Kostenlos | 1-24GB | 1-4 vCPU | ✅ Ja | ⭐⭐⭐⭐⭐ |
| **Eigener Server** | ✅ Kostenlos* | Beliebig | Beliebig | ✅ Ja | ⭐⭐⭐⭐⭐ |
| **Fly.io** | ✅ Kostenlos | 3GB | Shared | ✅ Ja | ⭐⭐⭐⭐ |
| **Google Cloud** | ✅ 90 Tage | 0.6GB | 1 vCPU | ✅ Ja | ⭐⭐⭐ |
| **AWS** | ✅ 12 Monate | 1GB | 1 vCPU | ✅ Ja | ⭐⭐⭐ |
| **Azure Container Instances** | ✅ Kostenlos | 0.5GB | 0.1 vCPU | ✅ Ja | ⭐⭐⭐⭐ |
| **Render.com** | ✅ Kostenlos | 512MB | Shared | ❌ Sleep | ⭐⭐ |
| **Railway** | ⚠️ $5/Monat | 512MB | Shared | ✅ Ja | ⭐⭐ |

*Stromkosten nicht eingerechnet

## 🎯 Finale Empfehlung

### Für Verkäufer (mehrere Käufer):

**1. Oracle Cloud Free Tier** ⭐ BESTE WAHL
- Komplett kostenlos
- Genug Ressourcen für 100+ Gruppen
- 24/7 Online
- Keine Limits

**Setup-Anleitung:**
```bash
# 1. Oracle Cloud Account erstellen
# 2. Ubuntu 22.04 VM erstellen
# 3. SSH verbinden
# 4. Docker installieren:
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker

# 5. Bot deployen:
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost
nano .env  # TOKEN, OWNER_ID eintragen
docker-compose up -d

# 6. Logs prüfen:
docker-compose logs -f
```

### Alternative Optionen:

**Azure Container Instances**
- ✅ Kostenlos (immer)
- ✅ 24/7 Online
- ⚠️ Limit: 0.5GB RAM
- Siehe `DEPLOY_AZURE.md`

**Fly.io** oder **Eigener Server**
- Schnell eingerichtet
- Kostenlos
- Gute Performance

### Für Produktion (wenn du keinen Server hast):

**Oracle Cloud Free Tier** → Beste kostenlose Option
**Oder:** Eigenen VPS mieten (~3-5€/Monat bei Hetzner, Contabo, etc.)

## Kostenvergleich (1 Jahr)

| Option | Kosten/Jahr | Bemerkung |
|--------|-------------|-----------|
| Oracle Cloud | **€0** | Komplett kostenlos |
| Fly.io | **€0** | Mit Limits |
| Eigener Server | **€0-120** | Stromkosten |
| Render.com | **€0** | Sleep-Mode Problem |
| Railway | **€60** | Nach Free Tier |
| VPS mieten | **€36-60** | Hetzner/Contabo |

## Setup-Anleitung: Oracle Cloud (Empfohlen)

Siehe `DEPLOY_ORACLE_CLOUD.md` für detaillierte Schritt-für-Schritt-Anleitung.

## Fazit

**Für kostenloses Deployment:**
1. **Oracle Cloud Free Tier** → Beste Option
2. **Eigener Server** → Wenn du Hardware hast
3. **Fly.io** → Alternative mit Limits

**Für Produktion:**
- Oracle Cloud Free Tier (kostenlos)
- Oder VPS mieten (~3-5€/Monat) für mehr Ressourcen

