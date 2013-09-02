import re

# For degrees 
# {{coord|dd|N/S|dd|E/W}}
dns = re.compile("{{coord.*?\|\s*([0-9\.]*)\s*\|([N|S])\|\s*([0-9\.]*)\s*\|([E|W])")

# For degrees/minutes:
# {{coord|dd|mm|N/S|dd|mm|E/W}}
dmns = re.compile("{{coord.*?\|\s*([0-9\.]*)\s*\|\s*([0-9\.]*)\s*\|([N|S])\|\s*([0-9\.]*)\s*\|\s*([0-9\.]*)\s*\|([E|W])")

# For degrees/minutes/seconds:
# {{coord|dd|mm|ss|N/S|dd|mm|ss|E/W}}
dmsns = re.compile("{{coord.*?\|\s*([0-9\.]*)\s*\|\s*([0-9\.]*)\s*\|\s*([0-9\.]*)\s*\|([N|S])\|\s*([0-9\.]*)\s*\|\s*([0-9\.]*)\s*\|\s*([0-9\.]*)\s*\|([E|W])")

# For decimal degrees
# {{coord|dd|dd}}
dd = re.compile("{{coord.*?\|\s*([0-9\.-]*)\s*\|\s*([0-9\.-]*)\s*[^NSEW0-9\.]")

type_re = re.compile(".*type:([^_|}]*)")
name_re = re.compile(".*name=([^|}]*)")

def adjust_ns(lat, lon, ns, ew):
    if ns == "S":
        lat *= -1
    if ew == "W":
        lon *= -1
    return (lon, lat)

def parse_coord(coord):
    lat = lon = ns = ew = None
    point = None

    # Order matters!
    dmsns_match = dmsns.match(coord)
    if dmsns_match:
        latd, latm, lats, ns, lond, lonm, lons, ew =  dmsns_match.groups() 
        if latd == "": latd = "0"
        if latm == "": latm = "0"
        if lats == "": lats = "0"
        if lond == "": lond = "0"
        if lonm == "": lonm = "0"
        if lons == "": lons = "0"
        lat = float(latd) + (float(latm)/60.0) + (float(lats)/3600.0)
        lon = float(lond) + (float(lonm)/60.0) + (float(lons)/3600.0)
        point = adjust_ns(lat, lon, ns, ew)

    if not point:
        dmns_match = dmns.match(coord)
        if dmns_match:
            latd, latm, ns, lond, lonm, ew =  dmns_match.groups()
            if latd == "": latd = "0"
            if latm == "": latm = "0"
            if lond == "": lond = "0"
            if lonm == "": lonm = "0"
            lat = float(latd) + (float(latm)/60.0)
            lon = float(lond) + (float(lonm)/60.0)
            point = adjust_ns(lat, lon, ns, ew)

    if not point:
        dns_match = dns.match(coord)
        if dns_match:
            lat, ns, lon, ew =  dns_match.groups()
            lat = float(lat)
            lon = float(lon)
            point = adjust_ns(lat, lon, ns, ew)

    if not point:
        dd_match = dd.match(coord)
        if dd_match:
            lat, lon =  dd_match.groups()
            point = (float(lon), float(lat))

    data = {'point': point }

    typematch = type_re.match(coord)
    if typematch:
        data['type'] = typematch.groups()[0].strip()

    namematch = name_re.match(coord)
    if namematch:
        data['name'] = namematch.groups()[0].strip()

    return data
    
    
if __name__ == "__main__":
    test_cases = [
        ("{{coord|51|30|N|0|5|W|region:GB_type:adm1st|display=title}}", 
            {'point': (-0.08333333333333333, 51.5), 'type': "adm1st"}),
        ("{{coord|51|N|5|W|region:GB|display=title}}", 
            {'point': (-5.0, 51.0)}),
        ("{{coord|51|N|5|E|region:GB|display=title}}", 
            {'point': (5.0, 51.0)}),
        ("{{coord|48.8814|2.3331|type:landmark_region:FR|display=title}}", 
            {'point': (2.3331, 48.8814), 'type': "landmark"}),
        ("{{coord|LAT|LONG|display=title}}", 
            {'point': None}),
        ("{{coord|24.088254|32.878722}}",  
            {'point':(32.878722, 24.088254)}),
        ("{{coord|37.33182|-122.03118|region:US-CA|display=title}}", 
            {'point': (-122.03118, 37.33182)}),
        ("{{coord|50|02|53|N|5|10|55|W|source:dewiki|display=title}}", 
            {'point': (-5.1819444444444445, 50.04805555555556)}),
        ("{{coord| 52|32|10.78|N| 13| 0|33.20|E|scale:8000|display=inline}}", 
            {'point': (13.009222222222222, 52.53632777777778)}),
        ("{{coord|42|50||N|78|5||W|region:US-NY_source:dewiki|display=title}}", 
            {'point': (-78.08333333333333, 42.833333333333336)}),
        ("{{coord|display=title|39.331156|-84.542842}}", 
            {'point': (-84.542842, 39.331156)}),
        ("{{coord|display=title|name=Digby|44|37|20|N|65|45|38|W|type:city_region:CA-NS}}", 
            {'point': (-65.76055555555556, 44.62222222222222), 'type': "city", 'name': "Digby"}),
        ("{{coord|49.621050 |N|6.140616 |E |type:landmark |display=title}}", 
            {'point': (6.140616, 49.621050), 'type': "landmark"}),
    ]

    for case in test_cases:
        try:
            assert case[1] == parse_coord(case[0])
        except:
            print
            print "*** FAILED"
            print case[0]
            print case[1], "!=", parse_coord(case[0])
            raise Exception
    print
