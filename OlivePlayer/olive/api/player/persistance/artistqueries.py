import xmltodict, os, sys
import xml.etree.ElementTree as ET
from lxml import etree

sys.path.append('../../utils')
from dictionary_library import xml_navegation


#---------------------------------------------------------------------WILL RETURN IMAGES ASWELL
#returns all artists
#returns -1 in case error while trying to access db.xml file content
def all_artists_query():
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1
        
    try:
        artists = []
        for artist_element in root.findall(xml_navegation['GET_Artists']):
            artist = {}
            artist['id'] = artist_element.attrib.get('id_artist')
            artist['artist_name'] = artist_element.attrib.get('artist_name')
            artists.append(artist)
        return artists
    except:
        return -1


#returns artist's albums
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no artist found
#returns -3 in case strange info encountered in db.xml file
def albums_of_artist_query(artist, list_of_artists = False, aux_root = ''):
    root = ''
    if not list_of_artists:
        try:
            xmlp = etree.XMLParser(encoding='utf-8')
            tree = etree.parse('../database/db.xml', parser=xmlp)
            root = tree.getroot()
        except:
            return -1
    else:
        root = aux_root
        
    artist_element = root.findall('artists/artist[@id_artist="'+str(artist)+'"]')
    if len(artist_element)==0:
        return -2
    elif len(artist_element)>1:
        return -3
        
    try:     
        artist = {}
        artist['id'] = artist_element[0].attrib.get('id_artist')
        artist['artist'] = artist_element[0].attrib.get('artist_name')
        albums = []
        for album_element in artist_element[0].findall(xml_navegation['GET_AlbumsOfArtist']):
            album = {}
            album['id'] = album_element.attrib.get('id_album')
            album['title'] = album_element.attrib.get('title')
            album['year'] = album_element.attrib.get('year')
            albums.append(album)
            
        singles_element = artist_element[0].find(xml_navegation['GET_SinglesOfArtist'])
        if singles_element is not None:
            singles = {}
            singles['singles'] = artist_element[0].attrib.get('artist_name') + ' - singles'
            albums.append(singles)   
            
        artist['albums'] = albums
    except:
        return -1
    
    return artist


#returns artists's albums
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no artist found
#returns -3 in case strange info encountered in db.xml file
def albums_of_artists_query(artists_list):
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1

    artists = []   
    for artist in artists_list:
        res = albums_of_artist_query(artist=artist, list_of_artists=True, aux_root=root)
        if res == -1 or res == -2 or res == -3:
            return res
        else:
            artists.append(res)
            
    return artists
    

#returns artist tracks
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no artist found
#returns -3 in case strange info encountered in db.xml file
def tracks_of_artist_query(artist, list_of_artists = False, aux_root = ''):
    root = ''
    if not list_of_artists:
        try:
            xmlp = etree.XMLParser(encoding='utf-8')
            tree = etree.parse('../database/db.xml', parser=xmlp)
            root = tree.getroot()
        except:
            return -1
    else:
        root = aux_root
        
    artist_element = root.findall('artists/artist[@id_artist="'+str(artist)+'"]')
    if len(artist_element)==0:
        return -2
    elif len(artist_element)>1:
        return -3
    
    artist = {}
    artist['id'] = artist_element[0].attrib.get('id_artist')
    artist['artist'] = artist_element[0].attrib.get('artist_name')    
    try:
        tracks = []
        for track_element in artist_element[0].findall('.//track'):
            track = {}
            track['id'] = track_element.attrib.get('id_track')
            track['track_number'] = track_element.find('track_number').text
            if track_element.getparent().getparent().tag == 'album':
                track['album_id'] = track_element.getparent().getparent().attrib.get('id_album')
                track['album_title'] = track_element.getparent().getparent().attrib.get('title')
            else:
                track['single'] = 'SINGLE'
            track['track_title'] = track_element.find('track_title').text         
            track['authors'] = track_element.find('authors').text
            track['duration'] = track_element.find('duration').text
            tracks.append(track)
        artist['tracks'] = tracks
    except:
        return -1

    return artist


#returns artists tracks
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no artist found
#returns -3 in case strange info encountered in db.xml file
def tracks_of_artists_query(artists_list):
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1

    artists = []   
    for artist in artists_list:
        res = tracks_of_artist_query(artist=artist, list_of_artists=True, aux_root=root)
        if res == -1 or res == -2 or res == -3:
            return res
        else:
            artists.append(res)
            
    return artists

  
#returns artist singles
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no artist found or no singles
#returns -3 in case strange info encountered in db.xml file
def singles_of_artist_query(artist):
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1

    artist_element = root.findall('artists/artist[@id_artist="'+str(artist)+'"]')
    if len(artist_element)==0:
        return -2
    elif len(artist_element)>1:
        return -3
    
    singles_element = artist_element[0].find(xml_navegation['GET_SinglesOfArtist'])
    singles = []
    if singles_element is not None:
        for single_element in singles_element.findall('.//track'):
            single = {}
            single['id'] = single_element.attrib.get('id_track')
            single['track_number'] = single_element.find('track_number').text
            single['single'] = 'SINGLE'
            single['track_title'] = single_element.find('track_title').text         
            single['authors'] = single_element.find('authors').text
            single['duration'] = single_element.find('duration').text
            singles.append(single)
    else:
        return -2
        
    return singles