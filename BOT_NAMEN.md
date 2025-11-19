# Bot-Namen Übersicht

## Aktuelle Bot-Namen im Code

Im Code wird aktuell **`@group_help`** als Beispiel verwendet. Du kannst jeden beliebigen Bot-Namen wählen.

## Bot-Namen Beispiele

### Für Verkäufer (Multi-Group Bot)

**Empfohlene Namen:**
- `@group_help` - Standard-Name
- `@autopost_bot` - Beschreibend
- `@group_poster` - Klar
- `@smart_poster` - Modern
- `@content_bot` - Einfach

**Beispiele für verschiedene Märkte:**
- `@motivation_bot` - Für Motivations-Content
- `@news_bot` - Für News-Updates
- `@promo_bot` - Für Werbung
- `@daily_post` - Für tägliche Posts

## Bot-Namen bei @BotFather setzen

### Schritt 1: Bot erstellen

1. Öffne Telegram → @BotFather
2. Sende `/newbot`
3. **Name eingeben:** z.B. "Group Help Bot"
4. **Username eingeben:** z.B. `group_help` (ohne @)
5. BotFather sendet dir den Token

### Schritt 2: Bot-Namen ändern (falls nötig)

**Name ändern:**
```
/setname
```
Dann neuen Namen eingeben

**Username ändern:**
```
/setusername
```
Dann neuen Username eingeben (muss mit `_bot` enden)

**Beschreibung ändern:**
```
/setdescription
```
Dann Beschreibung eingeben

## Bot-Namen in Dokumentation

Aktuell verwendet:
- `@group_help` in `KAEUFER_ANLEITUNG.md`
- `@group_help` in `VERKAEUFER_SETUP.md`
- `@group_help` in `README.md`

**Diese sind nur Beispiele** - jeder Verkäufer kann seinen eigenen Bot-Namen wählen.

## Empfehlungen für Bot-Namen

### ✅ Gute Bot-Namen:
- Kurz und prägnant
- Beschreibend
- Einfach zu merken
- Endet mit `_bot` (Telegram-Anforderung)

**Beispiele:**
- `@autopost_bot`
- `@group_poster`
- `@smart_post`
- `@content_helper`

### ❌ Schlechte Bot-Namen:
- Zu lang
- Schwer auszusprechen
- Nicht beschreibend

## Für mehrere Bots (verschiedene Märkte)

Wenn du mehrere Bots für verschiedene Märkte verkaufst:

1. **Motivations-Bot:** `@motivation_helper`
2. **News-Bot:** `@daily_news_bot`
3. **Promo-Bot:** `@promo_poster`
4. **Content-Bot:** `@content_manager`

Jeder Bot hat:
- Eigenen Token
- Eigene Deployment-Instanz
- Eigene Käufer-Gruppen

## Bot-Namen in Code ändern

**Nicht nötig!** Der Bot-Name wird nur bei @BotFather gesetzt, nicht im Code.

Der Code funktioniert mit jedem Bot-Namen, solange der Token korrekt ist.

## Zusammenfassung

- **Aktueller Beispiel-Name:** `@group_help`
- **Kann geändert werden:** Ja, bei @BotFather
- **Code muss nicht angepasst werden:** Nein
- **Empfehlung:** Kurz, beschreibend, mit `_bot` Endung

