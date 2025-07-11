# Prüfungsergebnis Rechner

Diese kleine WebApp berechnet, welches Ergebnis in der zweiten Prüfung erreicht werden muss, um ein gewünschtes Gesamt-Ergebnis zu erhalten. Alle Berechnungen werden in einer PostgreSQL-Datenbank gespeichert.

## Lokales Starten

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```


## Deployment auf Render

1. Dieses Repository zu Render hochladen bzw. mit GitHub verbinden.
2. Als Startbefehl `python app.py` angeben.
3. Eine PostgreSQL-Datenbank in Render erstellen und die Verbindungs-URL als Umgebungsvariable `DATABASE_URL` hinterlegen.

Beim ersten Start werden die benötigten Tabellen automatisch erzeugt.
