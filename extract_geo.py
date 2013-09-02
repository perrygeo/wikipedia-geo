import xml.sax
import re
import parse_coord

out_fields = ['title', 'point', 'name', 'type']

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
                coord['title'] = self.currTitle
                data = []
                if not coord['point']:
                    continue
                for field in out_fields:
                    if field == 'point':
                        data.append(coord['point'][0])
                        data.append(coord['point'][1])
                    else:
                        try:
                            data.append(coord[field])
                        except KeyError:
                            data.append('')
                tabdelim = u'\t'.join([unicode(x) for x in data])
                print tabdelim.encode('utf-8')

        elif name == "title":
            self.inTitle = False
            self.currTitle = u''.join(self.titleLines)
        elif name == "text":
            self.inText = False

    def characters(self, line):
        if self.inPage and self.inText:
            match = self.regex.match(line)
            if match:
                for grp in match.groups():
                    coords = parse_coord.parse_coord(grp)
                    try:
                        coords = parse_coord.parse_coord(grp)
                    except:
                        continue

                    if coords:
                        self.textLines.append(coords)
        elif self.inPage and self.inTitle:
            self.titleLines.append(line)


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setContentHandler(WikipediaGeoHandler())
    parser.parse(open("enwiki-latest-pages-articles.xml","r"))
