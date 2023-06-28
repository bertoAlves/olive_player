import xmltodict, os, sys, xlrd
import xml.etree.ElementTree as ET
from lxml import etree
from openpyxl import load_workbook

sys.path.append('../../utils')
from dictionary_library import xml_navegation


#returns the new playlist name
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no playlist found
#returns -3 in case strange info encountered in db.xml file
#returns -4 in case current playlist name is wrong
#returns -5 in case unable to get schema
#returns -6 in case db.xml is wrong format
#returns -7 in case error while saving transactions
def change_playlist_name_transac(playlist, current_playlist_name, new_playlist_name):
    
    root = ''
    tree = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1
        
    playlist_result = root.findall('.//playlists/playlist[@id_playlist="'+str(playlist)+'"]')
    
    if len(playlist_result)==0:
        return -2
    elif len(playlist_result)>1:
        return -3
    
    
    if playlist_result[0].attrib['name'] != current_playlist_name:
        return -4
      
    try:
        schema_root = etree.parse('../xml_schema.xsd').getroot()
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema = schema)
    except:
        return -5
    
    playlist_result[0].attrib['name'] = new_playlist_name
    
    try:
        etree.fromstring(etree.tostring(root), parser)
    except:
        return -6
    
    try:
        tree.write(open("../database/db.xml", "wb"), encoding='UTF8')
    except:
        return -7
        
    return { "new_playlist_name" : new_playlist_name}


#returns playlist with new track added
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no playlist or no track found
#returns -3 in case strange info encountered in db.xml file
#returns -4 in case unable to get schema
#returns -5 in case db.xml is wrong format
#returns -6 in case error while saving transactions
def add_track_to_playlist_transac(playlist, track, list_of_tracks = False, aux_tree = ''):
    root = ''   
    tree = ''
    if not list_of_tracks:
        try:
            xmlp = etree.XMLParser(encoding='utf-8')
            tree = etree.parse('../database/db.xml', parser=xmlp)
        except:
            return -1
    else:
        tree = aux_tree
    
    root = tree.getroot()
    
    playlist_result = root.findall('.//playlists/playlist[@id_playlist="'+str(playlist)+'"]')
    
    track_result = root.findall('.//artists/artist/albums/album/tracks/track[@id_track="'+str(track)+'"]')
    
    if len(playlist_result)==0 or len(track_result)==0:
        return -2
    elif len(playlist_result)>1 or len(track_result)>1:
        return -3
    
    try:
        schema_root = etree.parse('../xml_schema.xsd').getroot()
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema = schema)
    except:
        return -4
    
    track_id = etree.Element('track_id')
    track_id.set('id', track_result[0].attrib.get('id_track'))
    
    playlist_result[0].append(track_id)
    
    try:
        etree.fromstring(etree.tostring(root), parser)
    except:
        return -5
    
    playlist = {}
    if list_of_tracks:
        return 1
    else:
        try:
            tree.write(open("../database/db.xml", "wb"), encoding='UTF8')
        except:
            return -6
    
        playlist['id'] = playlist_result[0].attrib.get('id_playlist')
        playlist['name'] = playlist_result[0].attrib.get('name')
        
        tracks = []
        for track_element in playlist_result[0].findall(xml_navegation['GET_TracksOfPlaylist']):
            track = {}
            track['id'] = track_element.attrib.get('id')
            
            available = False
            for track_ele in root.findall('.//track[@id_track="'+track_element.attrib.get('id')+'"]'):   
                track['track_title'] = track_ele.find('.//track_title').text         
                track['authors'] = track_ele.find('.//authors').text
                track['duration'] = track_ele.find('.//duration').text
                available = True
                
            if available:
                tracks.append(track)
            else:
                return -3
                
        playlist['tracks'] = tracks 
        
    return playlist


#returns playlist with tracks are added
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no playlist or no track found
#returns -3 in case strange info encountered in db.xml file
#returns -4 in case unable to get schema
#returns -5 in case db.xml is wrong format
#returns -6 in case error while saving transactions
def add_tracks_to_playlist_transac(playlist, tracks):
    
    tree = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
    except:
        return -1
    root = tree.getroot()
    
    for track in tracks:
        res = add_track_to_playlist_transac(playlist, track, list_of_tracks = True, aux_tree = tree)
        if res == -1 or res == -2 or res == -3 or res == -4 or res == -5 or res == -6:
            return res
    
    try:
        tree.write(open("../database/db.xml", "wb"), encoding='UTF8')
    except:
        return -6
    
    
    playlist_result = root.findall('.//playlists/playlist[@id_playlist="'+str(playlist)+'"]')
    
    
    playlist = {}
    playlist['id'] = playlist_result[0].attrib.get('id_playlist')
    playlist['name'] = playlist_result[0].attrib.get('name')
    tracks = []
    for track_element in playlist_result[0].findall(xml_navegation['GET_TracksOfPlaylist']):
        track = {}
        track['id'] = track_element.attrib.get('id')
        
        available = False
        for track_ele in root.findall('.//track[@id_track="'+track_element.attrib.get('id')+'"]'):   
            track['track_title'] = track_ele.find('.//track_title').text         
            track['authors'] = track_ele.find('.//authors').text
            track['duration'] = track_ele.find('.//duration').text
            available = True
            
        if available:
            tracks.append(track)
        else:
            return -3
                
    playlist['tracks'] = tracks
    
    return playlist
    

#returns playlist with track removed
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no playlist or no track found
#returns -3 in case strange info encountered in db.xml file
#returns -4 in case error while saving transactions
def remove_track_from_playlist_transac(playlist, track, list_of_tracks = False, aux_tree = ''):
    root = ''
    
    tree = ''
    if not list_of_tracks:
        try:
            xmlp = etree.XMLParser(encoding='utf-8')
            tree = etree.parse('../database/db.xml', parser=xmlp)
        except:
            return -1
    else:
        tree = aux_tree
    
    root = tree.getroot()
    
    playlist_result = root.findall('.//playlists/playlist[@id_playlist="'+str(playlist)+'"]')
    
    track_result = playlist_result[0].findall('.//track_id[@id="'+str(track)+'"]')
    
    if len(playlist_result)==0 or len(track_result)==0:
        return -2
    elif len(playlist_result)>1 or len(track_result)>1:
        return -3
    
    playlist_result[0].remove(track_result[0])
    
    playlist = {}
    if list_of_tracks:
        return 1
    else:
        try:
            tree.write(open("../database/db.xml", "wb"), encoding='UTF8')
        except:
            return -6
    
        playlist['id'] = playlist_result[0].attrib.get('id_playlist')
        playlist['name'] = playlist_result[0].attrib.get('name')
        
        tracks = []
        for track_element in playlist_result[0].findall(xml_navegation['GET_TracksOfPlaylist']):
            track = {}
            track['id'] = track_element.attrib.get('id')
            
            available = False
            for track_ele in root.findall('.//track[@id_track="'+track_element.attrib.get('id')+'"]'):   
                track['track_title'] = track_ele.find('.//track_title').text         
                track['authors'] = track_ele.find('.//authors').text
                track['duration'] = track_ele.find('.//duration').text
                available = True
                
            if available:
                tracks.append(track)
            else:
                return -3
                
        playlist['tracks'] = tracks 
        
    return playlist
    
    
#returns playlist with tracks removed
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no playlist or no track found
#returns -3 in case strange info encountered in db.xml file
#returns -4 in case error while saving transactions
def remove_tracks_from_playlist_transac(playlist, tracks):
    
    tree = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
    except:
        return -1
    root = tree.getroot()
    
    for track in tracks:
        res = remove_track_from_playlist_transac(playlist, track, list_of_tracks = True, aux_tree = tree)
        if res == -1 or res == -2 or res == -3 or res == -4:
            return res
    
    try:
        tree.write(open("../database/db.xml", "wb"), encoding='UTF8')
    except:
        return -6
    
    
    playlist_result = root.findall('.//playlists/playlist[@id_playlist="'+str(playlist)+'"]')
      
    playlist = {}
    playlist['id'] = playlist_result[0].attrib.get('id_playlist')
    playlist['name'] = playlist_result[0].attrib.get('name')
    tracks = []
    for track_element in playlist_result[0].findall(xml_navegation['GET_TracksOfPlaylist']):
        track = {}
        track['id'] = track_element.attrib.get('id')
        
        available = False
        for track_ele in root.findall('.//track[@id_track="'+track_element.attrib.get('id')+'"]'):   
            track['track_title'] = track_ele.find('.//track_title').text         
            track['authors'] = track_ele.find('.//authors').text
            track['duration'] = track_ele.find('.//duration').text
            available = True
            
        if available:
            tracks.append(track)
        else:
            return -3
                
    playlist['tracks'] = tracks
    
    return playlist
    

#returns new playlist
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case invalid database behaviour
#returns -3 in playlist already exists
#returns -4 in case unable to get schema
#returns -5 in case db.xml is wrong format
#returns -6 in case error while saving transactions
def create_playlist_transac(name, tracks=''):
    tree = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
    except:
        return -1
    
    root = tree.getroot()
    
    playlists_element = root.findall('.//playlists')
    if len(playlists_element) != 1:
        return -2
    
    playlist_must_be_empty = playlists_element[0].findall('.//playlist[@name="' + name + '"]')
    
    if len(playlist_must_be_empty) > 1:
        return -2
    elif len(playlist_must_be_empty) == 1:
        return -6
    
    playlist = etree.Element('playlist')
    playlist_ret = {}
    
    new_playlist_id = get_new_playlist_id(root)
    #new playlist id
    playlist.set('id_playlist', str(new_playlist_id))
    playlist.set('name', name)
    
    playlist_ret['id'] = str(new_playlist_id)
    playlist_ret['name'] = name
    
    tracks_list = []
    if tracks:
        for track in tracks:
            track_id_ret = {}
            track_id = etree.SubElement(playlist, 'track_id')

            track_element = root.findall('.//track[@id_track="' + str(track) + '"]')
            
            if len(track_element) == 0:
                return -2
            elif len(track_element) > 1:
                return -3
            
            track_id.set('id', str(track))       
            track_id_ret['id'] = track_element[0].attrib.get('id_track')
            track_id_ret['track_title'] = track_element[0].find('.//track_title').text
            track_id_ret['album'] = track_element[0].getparent().getparent().attrib.get('title')
            track_id_ret['authors'] = track_element[0].find('.//authors').text
            track_id_ret['duration'] = track_element[0].find('.//duration').text
            
            tracks_list.append(track_id_ret)
        playlist_ret['tracks'] = tracks_list
    
    
    playlists_element[0].append(playlist)
    
    try:
        schema_root = etree.parse('../xml_schema.xsd').getroot()
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema = schema)
    except:
        return -4
    
    try:
        etree.fromstring(etree.tostring(root), parser)
    except:
        return -5
     
    try:
        tree.write(open("../database/db.xml", "wb"), encoding='UTF8')
    except:
        return -7
    
    return playlist_ret


#auxiliary method to get new playlist id
def get_new_playlist_id(root):
    new_id = 0
    for playlist in root.findall('.//playlists/playlist'):
        if playlist.attrib.get('id_playlist'):
            if new_id < int(playlist.attrib.get('id_playlist')):
                new_id = int(playlist.attrib.get('id_playlist'))
    new_id += 1
    return new_id

#returns delete playlist
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case invalid database behaviour
#returns -3 in playlist not found
#returns -4 in case error while saving transactions 
def delete_playlist_transac(playlist):
    tree = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
    except:
        return -1
    
    root = tree.getroot()
    
    playlists_element = root.findall('.//playlists')
    
    if len(playlists_element) != 1:
        return -3
        
    
    playlist_El = playlists_element[0].findall('.//playlist[@id_playlist="' + str(playlist) + '"]') 
    
    if len(playlist_El) == 0:
        return -2
    elif len(playlist_El) > 1:
        return -3
              
    playlists_element[0].remove(playlist_El[0])         
      
    try:
        tree.write(open("../database/db.xml", "wb"), encoding='UTF8')
    except:
        return -4
    
    return 1
    
    
    