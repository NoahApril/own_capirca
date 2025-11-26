# Confluence Dependency Analysis - Setup Guide

## Voraussetzungen

Du brauchst:
1. ✅ `python-dotenv` (bereits installiert)
2. ✅ `requests` (bereits installiert)
3. ✅ Confluence API Token

## Setup

### 1. Erstelle `.env` Datei

Kopiere `.env.example` zu `.env`:

```bash
cp .env.example .env
```

Fülle die `.env` aus:

```bash
CONFLUENCE_BASE_URL=https://deine-confluence-instance.com
CONFLUENCE_API_TOKEN=dein_api_token
CONFLUENCE_USERNAME=deine.email@example.com
```

### 2. API Token erstellen

1. Gehe zu: https://id.atlassian.com/manage-profile/security/api-tokens
2. Klicke "Create API token"
3. Kopiere den Token in `.env`

### 3. Script ausführen

**Option A: Mit Page ID als Argument**
```bash
cd /home/ygao/Workspace/Python/own_capirca
export PYTHONPATH=$PYTHONPATH:.
python3 examples/dependency_analysis_demo.py 123456789
```

**Option B: Interaktiv**
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 examples/dependency_analysis_demo.py
# Dann Page ID eingeben wenn gefragt
```

## Was passiert?

Das Script:
1. ✅ Lädt Credentials aus `.env`
2. ✅ Fetcht Confluence Page via API
3. ✅ Parst Tabellen (Hosts, Networks, Groups, Rules)
4. ✅ Analysiert Abhängigkeiten
5. ✅ Generiert Report
6. ✅ Speichert Report als `dependency_report_<page_id>.txt`

## Output Beispiel

```
==================================================================
Confluence Dependency Analysis
==================================================================
Base URL: https://confluence.example.com
Page ID:  123456789
------------------------------------------------------------------

Fetching page from Confluence...
✓ Fetched: Firewall Configuration

Parsing tables...
✓ Parsed 5 firewall rules
✓ Found 3 hosts
✓ Found 2 networks
✓ Found 4 groups

Analyzing dependencies...
✓ Analysis complete

==================================================================
Dependency Analysis Report
==================================================

Definitions (9):
  - DMZ (network)
  - Staff-Network (network)
  - WS-Clients (group)
  ...

Unresolved (1):
  - Well-Known-Names

Dependency Chains:
  - WS-Clients: WS-Clients → Staff-Network → Well-Known-Names

Cycles: None

Max Dependency Depth: 2
==================================================================

⚠️  WARNINGS:
   - 1 unresolved reference(s)
   - You need to fetch additional pages:
      • Well-Known-Names

📄 Report saved to: dependency_report_123456789.txt
```

## Nächste Schritte

Wenn du **unresolved references** hast:
1. Finde die Page mit der fehlenden Definition
2. Führe das Script nochmal mit der Page ID aus
3. Merge die Daten (wird später implementiert)

Wenn du **cycles** hast:
1. Fixe die Zirkularität in Confluence
2. Führe das Script erneut aus
