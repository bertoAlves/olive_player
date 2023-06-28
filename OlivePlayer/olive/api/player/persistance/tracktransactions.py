import xmltodict, json, os, sys, xlrd
from lxml import etree


#returns 1 if used is incremented on track
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no track found
#returns -3 in case strange info encountered in db.xml file
#returns -3 in case failure trying to save db.xml file
def used_transac(track):
    tree = ''
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1

    track = root.findall('.//track[@id_track="' + str(track) + '"]')
    
    if len(track) == 0:
        return -2
    elif len(track) > 1:
        return -3
        
    track[0].attrib['used'] = str(int(track[0].attrib.get('used')) + 1)
        
        
    try:
        tree.write(open("../database/db.xml", "wb"), encoding='UTF8')
    except:
        return -4
        
    return 1