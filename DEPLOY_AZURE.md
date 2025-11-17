# Azure Deployment - Kostenlose Optionen

## Übersicht

Azure bietet mehrere kostenlose Optionen für Telegram-Bots. Hier sind die besten:

## Option 1: Azure Container Instances (⭐ EMPFOHLEN)

### Kosten: Kostenlos mit Limits

**Free Tier:**
- ✅ Immer kostenlos (kein Ablauf)
- ✅ Container laufen 24/7
- ⚠️ Limit: 1 Container gleichzeitig
- ⚠️ Limit: 0.1 CPU, 0.5GB RAM pro Container
- ⚠️ Limit: 20GB Storage

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

## Option 3: Azure VM (Free Tier)

### Kosten: $200 Credits für 30 Tage, danach kostenpflichtig

**Free Tier:**
- B1S VM (1 vCPU, 1GB RAM)
- 64GB Storage
- Nur 30 Tage kostenlos

**Für Telegram-Bots:** ⚠️ Nur kurzfristig kostenlos

### Setup:

```bash
# VM erstellen
az vm create \
  --resource-group telegram-bot-rg \
  --name telegram-bot-vm \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Basic

# SSH verbinden
ssh azureuser@<PUBLIC_IP>

# Dann Docker installieren und Bot deployen (siehe DEPLOY_LOCAL.md)
```

## Option 4: Azure Functions (nicht empfohlen)

**Warum nicht:**
- Functions sind für Event-basierte Tasks
- Telegram-Bots müssen 24/7 laufen (Polling)
- Nicht ideal für kontinuierliche Verbindungen

## Vergleich: Azure Optionen

| Option | Kosten | 24/7 | Sleep-Mode | Empfehlung |
|--------|--------|------|------------|------------|
| **Container Instances** | ✅ Kostenlos | ✅ Ja | ❌ Nein | ⭐⭐⭐⭐⭐ |
| **App Service** | ✅ Kostenlos | ❌ Nein | ⚠️ Ja | ⭐⭐ |
| **VM** | ⚠️ 30 Tage | ✅ Ja | ❌ Nein | ⭐⭐⭐ |
| **Functions** | ✅ Kostenlos | ❌ Nein | ⚠️ Ja | ⭐ |

## 🎯 Empfehlung: Azure Container Instances

**Warum:**
- ✅ Immer kostenlos (kein Ablauf)
- ✅ Läuft 24/7 (kein Sleep-Mode)
- ✅ Einfaches Deployment
- ✅ Automatischer Neustart bei Fehlern

**Limits:**
- 0.1 CPU, 0.5GB RAM (ausreichend für Telegram-Bot)
- 1 Container gleichzeitig (ausreichend für Multi-Group Bot)

## Kostenvergleich (1 Jahr)

| Option | Kosten/Jahr | Bemerkung |
|--------|-------------|-----------|
| **Container Instances** | **€0** | Immer kostenlos |
| **App Service** | **€0** | Sleep-Mode Problem |
| **VM** | **€0-300** | Nach 30 Tagen kostenpflichtig |

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

**Für Azure:**
- ✅ **Container Instances** → Beste kostenlose Option
- ✅ Läuft 24/7
- ✅ Immer kostenlos
- ⚠️ Limit: 0.5GB RAM (ausreichend für Bot)

**Alternative:**
- Oracle Cloud Free Tier → Mehr Ressourcen (6GB RAM)
- Siehe `DEPLOY_ORACLE_CLOUD.md`

## Vergleich: Azure vs Oracle Cloud

| Feature | Azure Container Instances | Oracle Cloud |
|---------|--------------------------|--------------|
| Kosten | ✅ Kostenlos | ✅ Kostenlos |
| RAM | 0.5GB | 6GB |
| CPU | 0.1 vCPU | 1-4 vCPU |
| 24/7 | ✅ Ja | ✅ Ja |
| Setup | Mittel | Einfach |

**Empfehlung:** Oracle Cloud bietet mehr Ressourcen, aber Azure Container Instances ist auch eine gute Option!

