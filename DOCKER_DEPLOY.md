# Docker Deployment - Schnellstart

## Voraussetzungen

- Docker installiert: https://docs.docker.com/get-docker/
- Docker Compose installiert (optional, aber empfohlen)

## Option 1: Docker Compose (empfohlen)

### 1. Repository klonen

```bash
git clone https://github.com/phnxvision-pixel/telegram-autopost.git
cd telegram-autopost
```

### 2. .env Datei erstellen

```bash
nano .env
```

Füge folgendes ein:

```env
TOKEN=8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA
GROUP_ID=-1001234567890
OWNER_ID=123456789
```

### 3. Container starten

```bash
docker-compose up -d
```

### 4. Logs anzeigen

```bash
docker-compose logs -f
```

### 5. Container stoppen

```bash
docker-compose down
```

### 6. Container neu starten (nach Updates)

```bash
git pull
docker-compose up -d --build
```

## Option 2: Docker direkt (ohne Compose)

### 1. Image bauen

```bash
docker build -t telegram-autopost-bot .
```

### 2. Container starten

```bash
docker run -d \
  --name telegram-autopost-bot \
  --restart unless-stopped \
  -e TOKEN="8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA" \
  -e GROUP_ID="-1001234567890" \
  -e OWNER_ID="123456789" \
  telegram-autopost-bot
```

### 3. Logs anzeigen

```bash
docker logs -f telegram-autopost-bot
```

### 4. Container stoppen

```bash
docker stop telegram-autopost-bot
docker rm telegram-autopost-bot
```

### 5. Container neu starten (nach Updates)

```bash
docker stop telegram-autopost-bot
docker rm telegram-autopost-bot
docker build -t telegram-autopost-bot .
docker run -d \
  --name telegram-autopost-bot \
  --restart unless-stopped \
  -e TOKEN="8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA" \
  -e GROUP_ID="-1001234567890" \
  -e OWNER_ID="123456789" \
  telegram-autopost-bot
```

## Nützliche Docker-Befehle

```bash
# Container-Status prüfen
docker ps

# Alle Container (auch gestoppte)
docker ps -a

# Logs der letzten 100 Zeilen
docker logs --tail 100 telegram-autopost-bot

# In Container einsteigen (Debugging)
docker exec -it telegram-autopost-bot /bin/bash

# Container neu starten
docker restart telegram-autopost-bot

# Ressourcen-Verbrauch anzeigen
docker stats telegram-autopost-bot
```

## Automatischer Start nach Server-Neustart

Der Container startet automatisch nach einem Neustart dank `--restart unless-stopped`.

## Updates einspielen

```bash
# Mit Docker Compose
git pull
docker-compose up -d --build

# Mit Docker direkt
git pull
docker stop telegram-autopost-bot
docker rm telegram-autopost-bot
docker build -t telegram-autopost-bot .
docker run -d \
  --name telegram-autopost-bot \
  --restart unless-stopped \
  -e TOKEN="8585985138:AAFDVzaQXjiyHGueoXMuH5IziC8e1X-mcLA" \
  -e GROUP_ID="-1001234567890" \
  -e OWNER_ID="123456789" \
  telegram-autopost-bot
```

## Troubleshooting

### Container startet nicht

```bash
# Logs prüfen
docker logs telegram-autopost-bot

# Environment-Variablen prüfen
docker exec telegram-autopost-bot env
```

### Bot antwortet nicht

```bash
# Container läuft?
docker ps

# Logs prüfen
docker logs -f telegram-autopost-bot

# Token korrekt?
docker exec telegram-autopost-bot env | grep TOKEN
```

