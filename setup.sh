#!/bin/bash

echo "=========================================="
echo "Telegram Auto-Post Bot - Setup Script"
echo "=========================================="
echo ""

# Prüfe ob Docker installiert ist
if ! command -v docker &> /dev/null; then
    echo "❌ Docker ist nicht installiert!"
    echo "Installiere Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose ist nicht installiert!"
    echo "Installiere Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker gefunden"
echo ""

# Prüfe ob .env existiert
if [ ! -f .env ]; then
    echo "📝 Erstelle .env Datei..."
    cp .env.example .env
    echo ""
    echo "⚠️  WICHTIG: Bearbeite jetzt die .env Datei mit deinen Werten:"
    echo "   - TOKEN: Dein Bot-Token von @BotFather"
    echo "   - GROUP_ID: Deine Gruppen-ID (negativ)"
    echo "   - OWNER_ID: Deine Telegram-ID"
    echo ""
    read -p "Drücke Enter wenn du die .env Datei bearbeitet hast..."
fi

# Prüfe ob .env Werte gesetzt sind
if grep -q "your-bot-token-here" .env || grep -q "-1001234567890" .env || grep -q "123456789" .env; then
    echo "⚠️  WARNUNG: .env Datei enthält noch Platzhalter-Werte!"
    echo "Bitte bearbeite .env mit deinen echten Werten."
    echo ""
    read -p "Drücke Enter wenn du die .env Datei bearbeitet hast..."
fi

echo "🐳 Starte Docker Container..."
docker-compose up -d

echo ""
echo "⏳ Warte 5 Sekunden..."
sleep 5

echo ""
echo "📋 Logs anzeigen:"
docker-compose logs --tail=20

echo ""
echo "=========================================="
echo "✅ Setup abgeschlossen!"
echo "=========================================="
echo ""
echo "Nützliche Befehle:"
echo "  docker-compose logs -f     # Logs live anzeigen"
echo "  docker-compose ps          # Container-Status"
echo "  docker-compose restart     # Bot neu starten"
echo "  docker-compose down        # Bot stoppen"
echo ""
echo "Teste den Bot in deiner Gruppe mit: /start"
echo ""

