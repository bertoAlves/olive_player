import xmltodict, json, os, sys, xlrd
from lxml import etree

sys.path.append('../../utils')
from dictionary_library import xml_navegation, folder_path

#returns all tracks
#returns -1 in case error while trying to access db.xml file content
def all_tracks_query():
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1
    
    try:
        tracks = []
        for track_element in root.findall(xml_navegation['GET_Tracks']):
            track = {}
            track['id'] = track_element.attrib.get('id_track')
            track['track_number'] = track_element.find('.//track_number').text
            if track_element.getparent().getparent().tag == 'album':
                track_return['artist_id'] = track_element.getparent().getparent().getparent().getparent().attrib.get('id_artist')
                track_return['artist_name'] = track_element.getparent().getparent().getparent().getparent().attrib.get('artist_name')
                track_return['album_id'] = track_element.getparent().getparent().attrib.get('id_album')
                track_return['album_title'] = track_element.getparent().getparent().attrib.get('title')
            else:
                track_return['artist_id'] = track_element.getparent().getparent().getparent().attrib.get('id_artist')
                track_return['artist_name'] = track_element.getparent().getparent().getparent().attrib.get('artist_name')
                track_return['single'] = 'SINGLE'
                
            track['track_title'] = track_element.find('.//track_title').text
            track['authors'] = track_element.find('.//authors').text
            track['duration'] = track_element.find('.//duration').text
            tracks.append(track)   
        return tracks
    except:
        return -1


#returns track by id
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no track found
#returns -3 in case strange info encountered in db.xml file
def track_by_id(track, list_of_tracks = False, aux_root = ''):
    global root
    
    if not list_of_tracks:
        try:
            xmlp = etree.XMLParser(encoding='utf-8')
            tree = etree.parse('../database/db.xml', parser=xmlp)
            root = tree.getroot()
        except:
            return -1
    else:
        root = aux_root
        
    track_return = {} 
    track_element = root.findall('.//track[@id_track="'+str(track)+'"]')
    if len(track_element)==0:
        return -2
    elif len(track_element)>1:
        return -3
        
    else:    
        track_return['id'] = track_element[0].attrib.get('id_track')
        track_return['track_number'] = track_element[0].find('.//track_number').text
        if track_element[0].getparent().getparent().tag == 'album':
            track_return['artist_id'] = track_element[0].getparent().getparent().getparent().getparent().attrib.get('id_artist')
            track_return['artist_name'] = track_element[0].getparent().getparent().getparent().getparent().attrib.get('artist_name')
            track_return['album_id'] = track_element[0].getparent().getparent().attrib.get('id_album')
            track_return['album_title'] = track_element[0].getparent().getparent().attrib.get('title')
        else:
            track_return['artist_id'] = track_element[0].getparent().getparent().getparent().attrib.get('id_artist')
            track_return['artist_name'] = track_element[0].getparent().getparent().getparent().attrib.get('artist_name')
            track_return['single'] = 'SINGLE'
            
        track_return['track_title'] = track_element[0].find('.//track_title').text
        track_return['authors'] = track_element[0].find('.//authors').text
        track_return['duration'] = track_element[0].find('.//duration').text
        return track_return
            
    return -2


#returns tracks by ids
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no track found
#returns -3 in case strange info encountered in db.xml file
def tracks_by_listids(tracks_list):
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1

    tracks = []   
    for track in tracks_list:
        res = track_by_id(track=track, list_of_tracks=True, aux_root=root)
        if res == -1 or res == -2 or res == -3:
            return res
        else:
            tracks.append(res)
            
    return tracks
 
 
#returns path of track
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case no track found
def track_path_by_id(id):
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1
    
    track_element = root.findall('.//track[@id_track="'+str(id)+'"]')
    if len(track_element)==0:
        return -2
    elif len(track_element)>1:
        return -3
    
    parent_p = track_element[0].getparent().getparent()
    if parent_p.tag == 'album':
        return folder_path['music_folder'] + parent_p.attrib.get('album_path') + '/' + track_element[0].find('path').text
    else:
        return folder_path['music_folder'] + parent_p.attrib.get('singles_path') + '/' + track_element[0].find('path').text
                           
    return -2