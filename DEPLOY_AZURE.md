# Azure Deployment - Kostenlose Optionen

## Übersicht

Azure bietet mehrere kostenlose Optionen für Telegram-Bots. Hier sind die besten:

## 🎓 Azure Student Account (BESTE OPTION!)

**Wenn du ein Azure Student Abo hast:**
- ✅ **$100 Credits pro Jahr** (12 Monate)
- ✅ **Alle Azure Services** kostenlos nutzbar (innerhalb der Credits)
- ✅ **Keine Kreditkarte nötig** (nur Studenten-Verifizierung)
- ✅ **Mehr Ressourcen** als Free Tier

**Für Telegram-Bots:** ⭐⭐⭐⭐⭐ Perfekt!

### Student Account Vorteile:

| Feature | Normal Free Tier | Student Account |
|---------|------------------|-----------------|
| Credits | $200 (30 Tage) | $100 (12 Monate) |
| VM Größe | B1S (1GB RAM) | B2s (2GB RAM) oder größer |
| Container Instances | 0.5GB RAM | Bis zu 4GB RAM |
| Storage | 64GB | Mehr verfügbar |
| Dauer | 30 Tage | 12 Monate |

## Option 1: Azure Container Instances (⭐ EMPFOHLEN)

### Kosten: Kostenlos mit Limits

**Free Tier (ohne Student Account):**
- ✅ Immer kostenlos (kein Ablauf)
- ✅ Container laufen 24/7
- ⚠️ Limit: 1 Container gleichzeitig
- ⚠️ Limit: 0.1 CPU, 0.5GB RAM pro Container
- ⚠️ Limit: 20GB Storage

**Student Account:**
- ✅ **$100 Credits pro Jahr** (12 Monate)
- ✅ **Bis zu 4GB RAM** möglich
- ✅ **Mehr CPU** verfügbar
- ✅ **Mehr Storage**
- ✅ Container laufen 24/7

**Für Telegram-Bots:** ✅ Gut geeignet (läuft 24/7)

### Setup-Anleitung:

#### Schritt 1: Azure Account erstellen

1. Gehe zu: https://azure.microsoft.com/free/
2. Klicke auf "Start free"
3. Registriere dich (E-Mail, Telefon)
4. Kreditkarte angeben (wird NICHT belastet bei Free Tier)
5. Warte auf Verifizierung

#### Schritt 2: Azure CLI installieren

**Windows:**
```powershell
# Download: https://aka.ms/installazurecliwindows
# Oder mit winget:
winget install -e --id Microsoft.AzureCLI
```

**Linux:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Mac:**
```bash
brew install azure-cli
```

#### Schritt 3: Azure einloggen

```bash
az login
```

#### Schritt 4: Resource Group erstellen

```bash
az group create --name telegram-bot-rg --location westeurope
```

#### Schritt 5: Container Registry erstellen (optional)

```bash
az acr create --resource-group telegram-bot-rg \
  --name telegrambotregistry \
  --sku Basic \
  --admin-enabled true
```

#### Schritt 6: Container deployen

**Option A: Direkt aus Docker Hub**

**Für Student Account (mehr Ressourcen):**
```bash
az container create \
  --resource-group telegram-bot-rg \
  --name telegram-autopost-bot \
  --image docker.io/yourusername/telegram-bot:latest \
  --cpu 1.0 \
  --memory 2.0 \
  --environment-variables \
    TOKEN="dein-bot-token" \
    OWNER_ID="deine-telegram-id" \
  --restart-policy Always \
  --location westeurope
```

**Für Free Tier (weniger Ressourcen):**
```bash
az container create \
  --resource-group telegram-bot-rg \
  --name telegram-autopost-bot \
  --image docker.io/yourusername/telegram-bot:latest \
  --cpu 0.1 \
  --memory 0.5 \
  --environment-variables \
    TOKEN="dein-bot-token" \
    OWNER_ID="deine-telegram-id" \
  --restart-policy Always \
  --location westeurope
```

**Option B: Mit Azure Container Registry**

```bash
# Image zu ACR pushen
az acr login --name telegrambotregistry
docker tag telegram-bot telegrambotregistry.azurecr.io/telegram-bot:latest
docker push telegrambotregistry.azurecr.io/telegram-bot:latest

# Container erstellen
az container create \
  --resource-group telegram-bot-rg \
  --name telegram-autopost-bot \
  --image telegrambotregistry.azurecr.io/telegram-bot:latest \
  --registry-login-server telegrambotregistry.azurecr.io \
  --registry-username telegrambotregistry \
  --registry-password $(az acr credential show --name telegrambotregistry --query "passwords[0].value" -o tsv) \
  --cpu 0.1 \
  --memory 0.5 \
  --environment-variables \
    TOKEN="dein-bot-token" \
    OWNER_ID="deine-telegram-id" \
  --restart-policy Always \
  --location westeurope
```

#### Schritt 7: Logs anzeigen

```bash
az container logs --resource-group telegram-bot-rg --name telegram-autopost-bot --follow
```

#### Schritt 8: Container-Status prüfen

```bash
az container show --resource-group telegram-bot-rg --name telegram-autopost-bot --query "instanceView.state"
```

## Option 2: Azure App Service (Free Tier)

### Kosten: Kostenlos mit Limits

**Free Tier (F1):**
- ✅ Immer kostenlos
- ⚠️ **WICHTIG:** App schläft nach 20 Minuten Inaktivität ein
- ⚠️ Langsamer Start nach Sleep (~30 Sekunden)
- ⚠️ Nicht ideal für Telegram-Bots

**Für Telegram-Bots:** ❌ Nicht empfohlen (Sleep-Mode Problem)

### Setup (falls gewünscht):

```bash
# App Service Plan erstellen (Free Tier)
az appservice plan create \
  --name telegram-bot-plan \
  --resource-group telegram-bot-rg \
  --sku FREE \
  --location westeurope

# Web App erstellen
az webapp create \
  --resource-group telegram-bot-rg \
  --plan telegram-bot-plan \
  --name telegram-autopost-bot \
  --deployment-container-image-name docker.io/yourusername/telegram-bot:latest

# Environment Variables setzen
az webapp config appsettings set \
  --resource-group telegram-bot-rg \
  --name telegram-autopost-bot \
  --settings TOKEN="dein-bot-token" OWNER_ID="deine-telegram-id"
```

## Option 3: Azure VM (⭐ BESTE OPTION FÜR STUDENT ACCOUNT)

### Kosten: $100 Credits für 12 Monate (Student Account)

**Student Account:**
- ✅ **B2s VM** (2 vCPU, 4GB RAM) möglich
- ✅ **Oder B1s** (1 vCPU, 1GB RAM) für längere Laufzeit
- ✅ **64GB+ Storage**
- ✅ **12 Monate** kostenlos (innerhalb der Credits)
- ✅ **Volle Kontrolle** wie eigener Server

**Für Telegram-Bots:** ⭐⭐⭐⭐⭐ Perfekt für Student Account!

**Kostenberechnung:**
- B1s VM: ~$10/Monat → Läuft ~10 Monate kostenlos
- B2s VM: ~$20/Monat → Läuft ~5 Monate kostenlos
- Oder kleinere VM für längere Laufzeit

### Setup für Student Account:

**Option A: B1s VM (1 vCPU, 1GB RAM) - Längere Laufzeit**

```bash
# VM erstellen
az vm create \
  --resource-group telegram-bot-rg \
  --name telegram-bot-vm \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Basic \
  --location westeurope

# SSH verbinden
ssh azureuser@<PUBLIC_IP>

# Docker installieren
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker

# Bot deployen
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost
nano .env  # TOKEN, OWNER_ID eintragen
docker-compose up -d
```

**Option B: B2s VM (2 vCPU, 4GB RAM) - Mehr Power**

```bash
# VM erstellen
az vm create \
  --resource-group telegram-bot-rg \
  --name telegram-bot-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Basic \
  --location westeurope

# Dann wie oben weiter
```

**Kostenüberwachung:**
```bash
# Credits prüfen im Portal
# Gehe zu: https://portal.azure.com → Cost Management + Billing
```

## Option 4: Azure Functions (nicht empfohlen)

**Warum nicht:**
- Functions sind für Event-basierte Tasks
- Telegram-Bots müssen 24/7 laufen (Polling)
- Nicht ideal für kontinuierliche Verbindungen

## Vergleich: Azure Optionen

| Option | Kosten | 24/7 | Sleep-Mode | Empfehlung |
|--------|--------|------|------------|------------|
| **VM (Student)** | ✅ $100/Jahr | ✅ Ja | ❌ Nein | ⭐⭐⭐⭐⭐ |
| **Container Instances** | ✅ Kostenlos | ✅ Ja | ❌ Nein | ⭐⭐⭐⭐ |
| **Container Instances (Student)** | ✅ $100/Jahr | ✅ Ja | ❌ Nein | ⭐⭐⭐⭐⭐ |
| **App Service** | ✅ Kostenlos | ❌ Nein | ⚠️ Ja | ⭐⭐ |
| **VM (Free Tier)** | ⚠️ 30 Tage | ✅ Ja | ❌ Nein | ⭐⭐⭐ |
| **Functions** | ✅ Kostenlos | ❌ Nein | ⚠️ Ja | ⭐ |

## 🎯 Empfehlung für Student Account

### Option 1: Azure VM (BESTE WAHL FÜR STUDENT)

**Warum:**
- ✅ **$100 Credits für 12 Monate**
- ✅ **B2s VM möglich** (2 vCPU, 4GB RAM)
- ✅ **Volle Kontrolle** wie eigener Server
- ✅ **Läuft 24/7** (kein Sleep-Mode)
- ✅ **Genug für 100+ Gruppen**

**Setup:** Siehe Option 3 oben

### Option 2: Azure Container Instances (Student)

**Warum:**
- ✅ **$100 Credits für 12 Monate**
- ✅ **Bis zu 4GB RAM** möglich
- ✅ **Einfaches Deployment**
- ✅ **Automatischer Neustart**

**Limits (mit Student Credits):**
- Bis zu 1 CPU, 4GB RAM
- Mehr als Free Tier (0.1 CPU, 0.5GB RAM)

### Option 3: Azure Container Instances (Free Tier)

**Warum:**
- ✅ Immer kostenlos (kein Ablauf)
- ✅ Läuft 24/7 (kein Sleep-Mode)
- ✅ Einfaches Deployment

**Limits:**
- 0.1 CPU, 0.5GB RAM (ausreichend für Telegram-Bot)
- 1 Container gleichzeitig

## Kostenvergleich (1 Jahr)

| Option | Kosten/Jahr | Bemerkung |
|--------|-------------|-----------|
| **VM (Student)** | **€0** | $100 Credits für 12 Monate |
| **Container Instances (Student)** | **€0** | $100 Credits für 12 Monate |
| **Container Instances (Free)** | **€0** | Immer kostenlos |
| **App Service** | **€0** | Sleep-Mode Problem |
| **VM (Free Tier)** | **€0-300** | Nach 30 Tagen kostenpflichtig |

## Nützliche Azure CLI Befehle

```bash
# Container neu starten
az container restart --resource-group telegram-bot-rg --name telegram-autopost-bot

# Container stoppen
az container stop --resource-group telegram-bot-rg --name telegram-autopost-bot

# Container löschen
az container delete --resource-group telegram-bot-rg --name telegram-autopost-bot

# Logs anzeigen
az container logs --resource-group telegram-bot-rg --name telegram-autopost-bot --follow

# Status prüfen
az container show --resource-group telegram-bot-rg --name telegram-autopost-bot
```

## Troubleshooting

### Container startet nicht

```bash
# Logs prüfen
az container logs --resource-group telegram-bot-rg --name telegram-autopost-bot

# Events prüfen
az container show --resource-group telegram-bot-rg --name telegram-autopost-bot --query "instanceView.events"
```

### Environment Variables ändern

```bash
az container create \
  --resource-group telegram-bot-rg \
  --name telegram-autopost-bot \
  --image telegrambotregistry.azurecr.io/telegram-bot:latest \
  --cpu 0.1 \
  --memory 0.5 \
  --environment-variables \
    TOKEN="neuer-token" \
    OWNER_ID="neue-id" \
  --restart-policy Always \
  --location westeurope \
  --overwrite
```

### Kosten prüfen

```bash
# Kostenübersicht im Portal
# Gehe zu: https://portal.azure.com → Cost Management
```

## Fazit

### Für Student Account:

**🏆 BESTE WAHL: Azure VM (B2s)**
- ✅ $100 Credits für 12 Monate
- ✅ 2 vCPU, 4GB RAM
- ✅ Volle Kontrolle
- ✅ Genug für 100+ Gruppen

**Alternative: Azure Container Instances**
- ✅ $100 Credits für 12 Monate
- ✅ Bis zu 4GB RAM möglich
- ✅ Einfaches Deployment

### Für normale Free Tier:

**Azure Container Instances**
- ✅ Immer kostenlos
- ✅ Läuft 24/7
- ⚠️ Limit: 0.5GB RAM (ausreichend für Bot)

### Vergleich: Azure Student vs Oracle Cloud

| Feature | Azure VM (Student) | Azure Container Instances (Student) | Oracle Cloud |
|---------|-------------------|-------------------------------------|--------------|
| Kosten | ✅ $100/Jahr | ✅ $100/Jahr | ✅ Kostenlos |
| RAM | 4GB (B2s) | Bis zu 4GB | 6GB |
| CPU | 2 vCPU (B2s) | Bis zu 1 vCPU | 1-4 vCPU |
| 24/7 | ✅ Ja | ✅ Ja | ✅ Ja |
| Setup | Mittel | Einfach | Einfach |
| Dauer | 12 Monate | 12 Monate | Für immer |

**Empfehlung für Student:**
- **Azure VM (B2s)** → Beste Option mit Student Credits
- **Oder Oracle Cloud** → Mehr Ressourcen, für immer kostenlos

**Empfehlung ohne Student:**
- **Oracle Cloud Free Tier** → Mehr Ressourcen (6GB RAM)
- **Oder Azure Container Instances** → Immer kostenlos

