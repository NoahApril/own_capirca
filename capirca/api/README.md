# Backend API Server

## Überblick
Diese API ist mit FastAPI erstellt und bietet Endpoints für die Verwaltung von Firewall-Policies, Netzwerkobjekten, Service-Objekten und Deployments.

## Voraussetzungen
- Python 3.8+
- Poetry (empfohlen) oder pip

## Server starten

### Mit uvicorn (empfohlen)
```bash
# Im Hauptverzeichnis des Projekts
uvicorn capirca.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Optionen
- `--reload`: Automatisches Neuladen bei Codeänderungen (nur für Entwicklung)
- `--host 0.0.0.0`: Server ist von außen erreichbar
- `--port 8000`: Port (Standard: 8000)

### Produktionsmodus
```bash
uvicorn capirca.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Dokumentation
Nach dem Start ist die API-Dokumentation verfügbar unter:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints
- `GET /`: Health Check
- `/policies/*`: Policy-Management
- `/network-objects/*`: Netzwerkobjekte (Hosts, Networks, Groups)
- `/service-objects/*`: Service-Objekte
- `/deployments/*`: Deployment-Management

## Troubleshooting

### Port bereits belegt
```bash
# Anderen Port verwenden
uvicorn capirca.api.main:app --port 8001
```

### Import-Fehler
Stellen Sie sicher, dass Sie im Hauptverzeichnis sind und die Dependencies installiert sind:
```bash
pip install -e .
```
