**Extract and filter geographic information from wikipedia**

Download the wikipedia xml dump, unbunzip it and
point this script at it to extract all geo info
from wikipedia articles

The SAX parser has a terrible API but it's a
reasonable way to parse the 40GB+ XML file from 
wikipedia without loading into memory.

Tab-delimited output to stdout with columns:

```
article_title	longitude	latitude	name 	type
```

example:

```
...
Wangford Warren	0.583	52.427		landmark
Raffles Bay	132.383333333	-11.2666666667		waterbody
Friedrichsdorf station	8.64444444444	50.2522222222		railwaystation
Mount Ovit Tunnel	40.82382	40.62438		
Ambulapcha Glacier	86.9130555556	27.8930555556		
Spårvägsmuseet	18.0986111111	59.3116666667		landmark
Dughla	86.805	27.9241666667		
Glen Pean powerline span	-5.48005555556	56.9486944444	Glen Pean Powerline Span	landmark
...
```