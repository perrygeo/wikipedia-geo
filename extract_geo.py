import xml.sax
import re
import parse_coord

"""
Download the wikipedia xml dump, unbunzip it and
point this script at it to extract all geo info
from wikipedia articles

The SAX parser has a terrible API but is the only 
reasonable way to parse the 40GB+ XML file from 
wikipedia.
"""

class WikipediaGeoHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.titleLines = []
        self.textLines = []
        self.inPage = False
        self.inTitle = False
        self.inText = False
        self.currTitle = None
        #self.regex = re.compile("^.*({{coord\|.*}})")
        self.regex = re.compile("^.*({{coord\|[^}]*}})")

    def startElement(self, name, attrs):
        if name == "page":
            self.inPage = True
            self.textLines = []
            self.titleLines = []
            self.currTitle = None
        elif name == "title":
            self.inTitle = True
        elif name == "text":
            self.inText = True

    def endElement(self, name):
        if name == "page":
            self.inPage = False
            for coord in self.textLines:
                # TODO 
                # print self.currTitle, "\t", coord
                pass
        elif name == "title":
            self.inTitle = False
            self.currTitle = ''.join(self.titleLines)
        elif name == "text":
            self.inText = False

    def characters(self, line):
        if self.inPage and self.inText:
            match = self.regex.match(line)
            if match:
                for grp in match.groups():
                    try:
                        coords = parse_coord.parse_coord(grp)
                    except ValueError:
                        print grp
                        continue
                        
                    if coords:
                        self.textLines.append(str(coords))
                    else:
                        if "LAT|LON" not in grp:
                            print grp
        elif self.inPage and self.inTitle:
            self.titleLines.append(line)


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setContentHandler(WikipediaGeoHandler())
    parser.parse(open("real.xml","r"))



