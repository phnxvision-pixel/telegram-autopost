# Azure CLI Installation - Windows

## Option 1: Mit winget (empfohlen)

```powershell
# PowerShell als Administrator öffnen
winget install -e --id Microsoft.AzureCLI
```

## Option 2: Mit MSI Installer

1. Download: https://aka.ms/installazurecliwindows
2. Installer ausführen
3. Standard-Installation durchführen

## Option 3: Mit Chocolatey

```powershell
# PowerShell als Administrator
choco install azure-cli
```

## Option 4: Mit Scoop

```powershell
scoop install azure-cli
```

## Nach Installation

**Git Bash neu starten** oder Terminal neu öffnen.

**Testen:**
```bash
az --version
```

**Einloggen:**
```bash
az login
```

## Troubleshooting

### Command not found nach Installation

1. **Terminal komplett schließen und neu öffnen**
2. Oder: PowerShell/CMD neu starten
3. Prüfe ob Azure CLI im PATH ist:
   ```bash
   echo $PATH
   # Sollte enthalten: C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin
   ```

### Manuell zum PATH hinzufügen

1. Windows-Taste → "Umgebungsvariablen"
2. "Umgebungsvariablen bearbeiten"
3. "Path" auswählen → "Bearbeiten"
4. Hinzufügen: `C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin`
5. Terminal neu starten

## Alternative: Azure Cloud Shell (Browser)

Falls Installation Probleme macht:

1. Gehe zu: https://portal.azure.com
2. Klicke auf Cloud Shell Icon (oben rechts)
3. Wähle "Bash" oder "PowerShell"
4. Azure CLI ist bereits installiert!

**Vorteil:** Keine Installation nötig
**Nachteil:** Nur im Browser verfügbar
