# Obsidian MCP Server — Setup für Claude Code (Windows)

## Empfehlung

**`obsidian-mcp` von StevenStavrakis** — direkter Filesystem-Zugriff auf den Vault, kein Obsidian-Plugin nötig, Zero-Config via `npx`.

Repository: `https://github.com/StevenStavrakis/obsidian-mcp`

---

## Voraussetzungen

- Node.js ≥ 18 (prüfen: `node --version`)
- Claude Code installiert
- Obsidian Vault-Pfad bekannt (z.B. `C:\Users\Falko\Documents\ObsidianVault`)

---

## Installation (3 Schritte)

### 1. MCP Server zu Claude Code hinzufügen

Im Terminal (PowerShell):

```powershell
claude mcp add obsidian -s user -- npx -y obsidian-mcp "C:\Users\Falko\Documents\ObsidianVault"
```

> **Vault-Pfad anpassen!** Ersetze den Pfad durch deinen tatsächlichen Obsidian-Vault-Ordner.
> Mehrere Vaults möglich: einfach weitere Pfade anhängen.

### 2. Verifizieren

```powershell
claude mcp list
```

`obsidian` sollte in der Liste erscheinen.

### 3. Testen

In Claude Code:

```
"Liste alle Dateien in meinem Obsidian Vault"
```

---

## Verfügbare Tools nach Setup

| Tool | Funktion |
|---|---|
| `search` | Volltextsuche über alle Notes |
| `read-note` | Einzelne Note lesen |
| `create-note` | Neue Note anlegen |
| `edit-note` | Bestehende Note bearbeiten |
| `list-notes` | Notes in Ordner auflisten |
| `list-tags` | Alle Tags im Vault anzeigen |
| `list-folders` | Ordnerstruktur anzeigen |
| `delete-note` | Note löschen |
| `manage-tags` | Tags hinzufügen/entfernen |

---

## Alternative: REST-API-basiert (mehr Features, mehr Setup)

Falls du erweiterte Features brauchst (Patch-Operationen auf Heading-Ebene, Frontmatter-Manipulation):

### Obsidian-seitig
1. Community Plugin **"Local REST API"** installieren und aktivieren
2. API-Key aus den Plugin-Settings kopieren

### Claude Code Config

```powershell
claude mcp add obsidian-rest -s user -- npx -y @huangyihe/obsidian-mcp
```

Dann `.env` oder Umgebungsvariablen setzen:

```
OBSIDIAN_VAULT_PATH=C:\Users\Falko\Documents\ObsidianVault
OBSIDIAN_API_TOKEN=dein_api_key
OBSIDIAN_API_PORT=27123
```

> **Nachteil:** Obsidian Desktop muss laufen, damit die REST API erreichbar ist.

---

## Empfehlung für deinen Workflow

| Kriterium | Filesystem (Option A) | REST API (Option B) |
|---|---|---|
| Obsidian muss laufen | Nein | Ja |
| Setup-Aufwand | Minimal | Mittel |
| Heading-Level Patches | Nein | Ja |
| Frontmatter-Ops | Begrenzt | Voll |
| Vault-Backup vorher | **Ja, zwingend** | **Ja, zwingend** |

**Für deinen Use Case (VERITAS-Docs, Diamond Lessons Research, Blackbirds-Content):**
Option A reicht. Wenn du später chirurgische Edits auf Heading-Ebene brauchst, auf B upgraden.

---

## Sicherheitshinweis

⚠️ **Vault vorher sichern** — Git-Init im Vault-Ordner oder manuelles Backup.
Der MCP Server hat Schreibzugriff. Ungetestete Bulk-Operationen können Daten zerstören.

```powershell
cd "C:\Users\Falko\Documents\ObsidianVault"
git init
git add .
git commit -m "Backup vor MCP-Setup"
```
