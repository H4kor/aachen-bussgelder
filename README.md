# Aachen Bussgelder

## Daten Quellen

Die Daten stammen aus dem [Open Data Portal der Stadt Aachen](https://offenedaten.aachen.de/).

Beinhaltete Datensätze:
* https://offenedaten.aachen.de/dataset/bussgelder-fliessender-verkehr-2019
* https://offenedaten.aachen.de/dataset/verwarn-und-bussgelder-ruhender-verkehr-2019

## Preprocessing

Das Preprocessing Skript bringt die CSVs in ein einheitliches Format und fügt Geo Koordinaten hinzu.
Es wird ein [Nominatim](https://nominatim.openstreetmap.org/ui/search.html) Server benötigt.

```
usage: bussgelder.py [-h] [--nominatim NOMINATIM] i o t

Skript um Aachen Bussgeld Daten um GPS Koordinaten zu erweitern und zu vereinheitlichen

positional arguments:
  i                     Pfad zur Original CSV
  o                     Ausgabe Pfad
  t                     Verkehrstyp (z.B. stehend oder fliessend)

optional arguments:
  -h, --help            show this help message and exit
  --nominatim NOMINATIM
                        URL des Nominatim Servers
```

## Lokale Entwicklung

```
datasette database.db -m metadata.json
```

## Deployment 

```
datasette publish cloudrun database.db -m metadata.json --service=aachen-bussgelder --install=datasette-cluster-map
```
