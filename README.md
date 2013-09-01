**Extract and filter geographic information from wikipedia**

Download the wikipedia xml dump, unbunzip it and
point this script at it to extract all geo info
from wikipedia articles

The SAX parser has a terrible API but it's a
reasonable way to parse the 40GB+ XML file from 
wikipedia without loading into memory.

```
...
Banca d'Italia 	(12.488888888888889, 41.89722222222222)
Battle of Blenheim 	(10.633333333333333, 48.63333333333333)
Battle of Ramillies 	(4.912777777777778, 50.63861111111111)
Bohemia 	(15.0, 50.0)
Barcelona 	(2.1521944444444445, 41.416555555555554)
...
```