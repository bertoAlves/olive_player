import xmltodict, os, sys, base64
import xml.etree.ElementTree as ET
from lxml import etree

sys.path.append('../../utils')
from dictionary_library import xml_navegation


#returns all albums
#returns -1 in case error while trying to access db.xml file content
def all_albums_query():
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1
        
    albums = []
    for album_element in root.findall(xml_navegation['GET_Albums']):
        album = {}
        album['id'] = album_element.attrib.get('id_album')
        album['artist_id'] = album_element.getparent().getparent().attrib.get('id_artist')
        album['artist_name'] = album_element.getparent().getparent().attrib.get('artist_name')
        album['name'] = album_element.attrib.get('title')
        album['year'] = album_element.attrib.get('year')
        #file = open('C:/Users/catar/OneDrive/Imagens/transferir.png', mode='rb')
        #img = file.read()
        #album['image'] = base64.encodebytes(img).decode("utf-8")
        albums.append(album)
    return albums
        
        
#returns albums's tracks
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no album found
#returns -3 in case strange info encountered in db.xml file
def tracks_of_album_query(album, list_of_albums = False, aux_root = ''):
    root = ''
    
    if not list_of_albums:
        try:
            xmlp = etree.XMLParser(encoding='utf-8')
            tree = etree.parse('../database/db.xml', parser=xmlp)
            root = tree.getroot()
        except:
            return -1
    else:
        root = aux_root
        
    album_element = root.findall('artists/artist/albums/album[@id_album="'+str(album)+'"]')
    if len(album_element)==0:
        return -2
    elif len(album_element)>1:
        return -3
        
    try:   
        album = {}
        album['id'] = album_element[0].attrib.get('id_album')
        album['title'] = album_element[0].attrib.get('title')
        album['year'] = album_element[0].attrib.get('year')
        tracks = []
        for track_element in album_element[0].findall(xml_navegation['GET_TracksOfAlbum']):
            track = {}
            track['id'] = track_element.attrib.get('id_track')
            track['track_number'] = track_element.find('track_number').text
            track['track_title'] = track_element.find('track_title').text         
            track['authors'] = track_element.find('authors').text
            track['duration'] = track_element.find('duration').text
            tracks.append(track)        
        album['tracks'] = tracks
    except:
        return -1

    return album


#returns albums's tracks
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no album found
#returns -3 in case strange info encountered in db.xml file
def tracks_of_albums_query(albums_list):
    global root
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1

    albums = []   
    for album in albums_list:
        res = tracks_of_album_query(album=album, list_of_albums=True, aux_root=root)
        if res == -1 or res == -2 or res == -3:
            return res
        else:
            albums.append(res)
            
    return albums
    