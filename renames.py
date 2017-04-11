import os
import pycountry
import BeautifulSoup
import shutil
import sys
from svgpathtools import *

files = os.listdir('svg')
for file in files:
    country = file.split('Low.svg')[0].capitalize()
    print file
    try:
        paths, attributes = svg2paths('svg/' + file)
        xmin, xmax, ymin, ymax = paths2svg.big_bounding_box(paths)
    except:
        print "Exception processing", file
        xmin, xmax, ymin, ymax = (0, 0, 500, 500)

    soup = BeautifulSoup.BeautifulSoup(open('svg/' + file))
    twoletter = soup.find("path")['id'].split('-')[0].split('_')[0]
    svg = soup.find('svg')
    svg['class'] = "country-map"
    svg['viewbox'] = str(xmin) + ' ' + str(ymin) + ' ' + \
        str(xmax - xmin) + ' ' + str(ymax - ymin)
    soup.find(
        'style').string = "path.land {stroke: #d8382c; fill: #d8382c;}"
    withoutstyle = soup.prettify()
    # withoutstyle = '\n'.join([str(child)
    #                           for child in svg.contents])  # soup.prettify()

    try:
        blob = pycountry.countries.get(alpha_2=twoletter)
        threeletter = blob.alpha_3.lower()
        fullname = blob.name
        if threeletter == "vat":
            fullname = "Italy"
        print blob.alpha_3.lower(), country, withoutstyle[:20]
        open('threeletter/' +
             threeletter + '.svg', 'w').write(withoutstyle)
        open('fullname/' +
             fullname + '.svg', 'w').write(withoutstyle)
    except Exception, e:
        print e
        print '***', country
