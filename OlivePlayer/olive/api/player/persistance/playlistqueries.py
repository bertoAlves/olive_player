import xmltodict, os, sys
import xml.etree.ElementTree as ET
from lxml import etree

sys.path.append('../../utils')
from dictionary_library import xml_navegation


#returns all playlists
#returns -1 in case error while trying to access db.xml file content
def all_playlists_query():
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1
        
    try:
        playlists = []
        
        for playlist_element in root.findall(xml_navegation['GET_Playlists']):
            playlist = {}        
            playlist['id'] = playlist_element.attrib.get('id_playlist')
            playlist['name'] = playlist_element.attrib.get('name')
            playlists.append(playlist)
        return playlists
    except:
        return -1


#returns playlist's tracks
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no playlist found
#returns -3 in case strange info encountered in db.xml file
def tracks_of_playlist_query(playlist, list_of_playlists = False, aux_root = ''):
    root = ''
    
    if not list_of_playlists:
        try:
            xmlp = etree.XMLParser(encoding='utf-8')
            tree = etree.parse('../database/db.xml', parser=xmlp)
            root = tree.getroot()
        except:
            return -1
    else:
        root = aux_root
        
    playlist_result = root.findall('playlists/playlist[@id_playlist="'+str(playlist)+'"]')
    if len(playlist_result)==0:
        return -2
    elif len(playlist_result)>1:
        return -3
        
    try:
        playlist_element = playlist_result[0]        
        playlist = {}
        playlist['id'] = playlist_element.attrib.get('id_playlist')
        playlist['name'] = playlist_element.attrib.get('name')
        tracks = []
        for track_element in playlist_element.findall(xml_navegation['GET_TracksOfPlaylist']):
            track = {}
            track['id'] = track_element.attrib.get('id')
            
            available = False
            
            track_ele = root.findall('.//track[@id_track="'+track_element.attrib.get('id')+'"]')
            
            if len(track_ele)==0:
                return -2
            elif len(track_ele)>1:
                return -3
            
            track_ele = track_ele[0]
            if track_ele.getparent().getparent().tag == 'album':
                track['artist_id'] = track_ele.getparent().getparent().getparent().getparent().attrib.get('id_artist')
                track['artist_name'] = track_ele.getparent().getparent().getparent().getparent().attrib.get('artist_name')
                track['album_id'] = track_ele.getparent().getparent().attrib.get('id_album')
                track['album_title'] = track_ele.getparent().getparent().attrib.get('title')
            else:       
                track['artist_id'] = track_ele.getparent().getparent().getparent().attrib.get('id_artist')
                track['artist_name'] = track_ele.getparent().getparent().getparent().attrib.get('artist_name')
                track['single'] = 'SINGLE'
                
            track['track_title'] = track_ele.find('track_title').text         
            track['authors'] = track_ele.find('authors').text
            track['duration'] = track_ele.find('duration').text
            available = True
                
            if available:
                tracks.append(track)
            else:
                return -3
                
        playlist['tracks'] = tracks
    except:
        return -1
    
    return playlist


#returns playlists's tracks
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no playlist found
#returns -3 in case strange info encountered in db.xml file
def tracks_of_playlists_query(playlist_list):
    global root
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1

    playlists = []   
    for playlist in playlist_list:
        res = tracks_of_playlist_query(playlist=playlist, list_of_playlists=True, aux_root=root)
        if res == -1 or res == -2 or res == -3:
            return res
        else:
            playlists.append(res)
            
    return playlists
    