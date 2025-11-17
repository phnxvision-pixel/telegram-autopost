@echo off
chcp 65001 >nul
echo ==========================================
echo Telegram Auto-Post Bot - Setup Script
echo ==========================================
echo.

REM Prüfe ob Docker installiert ist
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker ist nicht installiert!
    echo Installiere Docker: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

where docker-compose >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker Compose ist nicht installiert!
    echo Installiere Docker Compose: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

echo ✅ Docker gefunden
echo.

REM Prüfe ob .env existiert
if not exist .env (
    echo 📝 Erstelle .env Datei...
    copy .env.example .env >nul
    echo.
    echo ⚠️  WICHTIG: Bearbeite jetzt die .env Datei mit deinen Werten:
    echo    - TOKEN: Dein Bot-Token von @BotFather
    echo    - GROUP_ID: Deine Gruppen-ID (negativ)
    echo    - OWNER_ID: Deine Telegram-ID
    echo.
    pause
)

REM Prüfe ob .env Werte gesetzt sind
findstr /C:"your-bot-token-here" .env >nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  WARNUNG: .env Datei enthält noch Platzhalter-Werte!
    echo Bitte bearbeite .env mit deinen echten Werten.
    echo.
    pause
)

echo 🐳 Starte Docker Container...
docker-compose up -d

echo.
echo ⏳ Warte 5 Sekunden...
timeout /t 5 /nobreak >nul

echo.
echo 📋 Logs anzeigen:
docker-compose logs --tail=20

echo.
echo ==========================================
echo ✅ Setup abgeschlossen!
echo ==========================================
echo.
echo Nützliche Befehle:
echo   docker-compose logs -f     # Logs live anzeigen
echo   docker-compose ps          # Container-Status
echo   docker-compose restart     # Bot neu starten
echo   docker-compose down        # Bot stoppen
echo.
echo Teste den Bot in deiner Gruppe mit: /start
echo.
pause

