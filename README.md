# Tagesteller

Ernährungstagebuch für iPhone und iPad: Lebensmittel und Speisen eintragen, Nährwerte werden automatisch berechnet, Auswertung über Zeiträume mit Diagrammen, Vergleich von Lebensmitteln. Läuft als Web-App ohne App Store, ohne Konto, Daten bleiben auf dem Gerät.

## Dateien

```
index.html      die App
foods.js        Lebensmittel-Datenbank (7.140 Einträge aus dem BLS 4.0, je 100 g)
tools/          Skript, das foods.js aus der BLS-Excel-Datei erzeugt
manifest.json   App-Name und Icon für den Home-Bildschirm
sw.js           Offline-Speicher (App funktioniert auch ohne Internet)
icons/          App-Icons
```

## 1. Online stellen mit GitHub Pages (kostenlos, einmalig ca. 10 Minuten)

1. Auf https://github.com ein kostenloses Konto anlegen (falls noch keins vorhanden).
2. Oben rechts **+ → New repository**. Name z. B. `tagesteller`, Sichtbarkeit **Public**, „Create repository“.
3. Auf der leeren Repository-Seite **uploading an existing file** anklicken und alle Dateien aus diesem Ordner
   hineinziehen (inklusive Ordner `icons`). Unten **Commit changes**.
4. Im Repository **Settings → Pages**. Bei „Branch“ `main` und `/ (root)` wählen, **Save**.
5. Nach 1–2 Minuten steht oben der Link, z. B. `https://DEIN-NAME.github.io/tagesteller/`.

Diesen Link schickst du deinen Eltern. Hinweis: Die Adresse ist öffentlich auffindbar, enthält aber keine
persönlichen Daten. Die Einträge liegen ausschließlich auf dem jeweiligen iPhone bzw. iPad.

Alternative: Jeder andere Webserver mit **HTTPS** funktioniert auch (z. B. im eigenen Homelab hinter einem
Reverse-Proxy mit Zertifikat). Ohne HTTPS funktioniert der Offline-Modus nicht.

## 2. Auf iPhone und iPad installieren

1. Link in **Safari** öffnen (nicht in Chrome oder in der WhatsApp-Vorschau).
2. Unten auf **Teilen** tippen (Quadrat mit Pfeil nach oben).
3. **Zum Home-Bildschirm** wählen, dann **Hinzufügen**.
4. Ab jetzt über das Icon „Tagesteller“ öffnen. Die App startet dann im Vollbild und funktioniert auch offline.

Wichtig: Immer über das Icon öffnen, nicht über Safari. Das Icon und Safari haben getrennte Speicher.
iPhone und iPad haben jeweils ein eigenes Tagebuch. Übertragen geht über **Mehr → Datensicherung**.

## Updates

Neue Version einfach wieder in das GitHub-Repository hochladen (Dateien ersetzen) und in `sw.js` die
Versionsnummer in `CACHE = 'tagesteller-vX'` hochzählen. Die Apps holen sich das Update beim nächsten
Öffnen mit Internetverbindung. Die Daten deiner Eltern bleiben dabei erhalten.

## Datenquellen

- Nährwerte: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0,
  Deutsche Nährstoffdatenbank. Karlsruhe. DOI: 10.25826/Data20251217-134202-0
  Die Datenbank neu erzeugen: `python3 tools/build_foods.py BLS_4_0_Daten_2025_DE.xlsx`
  (Alltagsnamen und Portionsgrößen stehen in `tools/curated.json`).
- Online-Suche und Barcode: Open Food Facts (openfoodfacts.org, ODbL), Herstellerangaben.
- Tagesziele: Referenzwerte der DGE für Frauen ab 65 Jahren, in der App änderbar.

Die App ersetzt keine ärztliche Beratung.
