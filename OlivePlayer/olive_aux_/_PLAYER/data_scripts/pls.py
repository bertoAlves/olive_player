import os, re, sys, datetime, xlrd
import xml.etree.ElementTree as ET
import shutil
from pathlib import Path
import xlwings
import logging

sys.path.append('utils')
from dictionary_library import db_default, folder_navegation
from conversions import *
from tools import *
from validations import validateGroovePlaylistFileExtension

#get new playlist id
def get_new_playlist_id(root):
    new_id = 0
    for playlist in root.findall('.//playlists/playlist'):
        if playlist.attrib.get('id_playlist'):
            if new_id < int(playlist.attrib.get('id_playlist')):
                new_id = int(playlist.attrib.get('id_playlist'))
    new_id += 1
    return new_id


#get startup playlists from groove
def read_playlist_from_groove():
    
#---create folder if it doesn't exist
    if not os.path.exists(folder_navegation['PLAYLISTS_XML_FOLDER']):
        Path(folder_navegation['PLAYLISTS_XML_FOLDER']).mkdir(parents=True, exist_ok=True)
        
    if not os.path.exists(folder_navegation['LOG_FOLDER']):
        Path(folder_navegation['LOG_FOLDER']).mkdir(parents=True, exist_ok=True)
        
    logging.basicConfig(filename=folder_navegation['LOG_FILE'], format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger('_PLS_')
       
#---for each .zpl playlist convert it to .xml
    for root, dirs, files in os.walk(folder_navegation['PLAYLISTS_FOLDER']):        
        for file in files:
            if validateGroovePlaylistFileExtension(file):
                modifiedDate = datetime.datetime.fromtimestamp(os.path.getmtime(root + '/' + file))   
                todaysDate = datetime.datetime.today()
                modifyDateLimit = modifiedDate + datetime.timedelta(days=1)
                if modifyDateLimit > todaysDate:      
                    segmented_file = separate_file_from_extension(file)
                    shutil.copy2(root + '/' + file, folder_navegation['PLAYLISTS_XML_FOLDER'] + segmented_file[0] + '.xml')
                   
    tree = ''    
    try:
        xmlp = ET.XMLParser(encoding='utf-8')
        tree = ET.parse(folder_navegation['DB_FILE'], parser=xmlp)
    except:
        sys.exit('Error while reading db.xml')
    
    olive_root = tree.getroot()
    playlists_node = olive_root.findall('./playlists')
    
    playlists = ''
    playlists_exists = False
    if len(playlists_node) == 1:
        playlists = playlists_node[0]
        playlists_exists = True
    elif len(playlists_node) == 0:
        playlists = ET.Element('playlists')
    else:
        sys.exit('Error, db.xml in wrong format')
    
    new_playlists_count = 0
       
    check_playlist_for_updates = []
    
#---navigate playlists_xml folder
    try:      
        for root, dirs, files in os.walk(folder_navegation['PLAYLISTS_XML_FOLDER']):  
            for file in files:    
                in_database = False
                
            #---check if playlist exists
                if playlists_exists:
                    for pl in playlists_node[0].findall('./playlist'):
                        if separate_file_from_extension(file)[0] == pl.attrib.get('groove_name'):
                            in_database = True
                            break
                            
                modifiedDate = datetime.datetime.fromtimestamp(os.path.getmtime(root + '/' + file))   
                todaysDate = datetime.datetime.today()
                modifyDateLimit = modifiedDate + datetime.timedelta(days=1)
            
            #---if playlist exists and was recently modified, then add to check for updates
                if in_database and (todaysDate < modifyDateLimit):
                    check_playlist_for_updates.append(file)
                    continue
            
            #---if playlist exists and wasnt recently modified, then continue to next iteration
                elif in_database:
                    continue
                    
                playlist = ET.Element('playlist')
                playlist_tree = ET.parse(folder_navegation['PLAYLISTS_XML_FOLDER'] + file).getroot()
                
                playlist_identifier = get_new_playlist_id(olive_root)
                playlist.set('id_playlist', str(playlist_identifier))
                
                playlist.set('groove_name', separate_file_from_extension(file)[0])
                playlist.set('name', separate_file_from_extension(file)[0])
            
            #---for each media element
                for media_element in playlist_tree.findall('./body/seq/media'): 
                    src = media_element.attrib.get('src')

                    filename_ext = ''
                    title = ''
                    if src:
                        path = os.path.basename(src)
                        filename_ext = os.path.basename(path)
                    else:
                        title = media_element.attrib.get('trackTitle')
                    
                #---find track in all albums
                    track = ET.Element('track_id')
                    for track_ele in olive_root.findall('.//artists/artist/albums/album/tracks/track'):                    
                        if track_ele.find('path').text == filename_ext:
                            track.set('id', track_ele.attrib.get('id_track'))
                            playlist.append(track)
                            break
                            
                #---find track in all singles   
                    for track_ele in olive_root.findall('.//artists/artist/singles/tracks/track'):                    
                        if track_ele.find('path').text == filename_ext:
                            track.set('id', track_ele.attrib.get('id_track'))
                            playlist.append(track)
                            break
                                  
                playlists.append(playlist)
                new_playlists_count += 1
        
        messages = []
        playlists_element = olive_root.find('playlists')
    except Exception as message:
        logger.exception(message)
        sys.exit(str(message))  
    
    try:
    
    #---check if playlists were updated
        if len(check_playlist_for_updates) != 0:
            for playlist in check_playlist_for_updates:
                playlist_tree = ET.parse(folder_navegation['PLAYLISTS_XML_FOLDER'] + playlist).getroot()    
                    
                for media_element in playlist_tree.findall('./body/seq/media'):
                    next = False
                    playlist_title = separate_file_from_extension(playlist)
                    
                    src = media_element.attrib.get('src')
                    
                    filename_ext = ''
                    title = ''
                    if src:
                        path = os.path.basename(src)
                        filename_ext = os.path.basename(path)
                    else:
                        title = media_element.attrib.get('trackTitle')
                    
                    playlist_element = playlists_element.findall('.//playlist[@groove_name="' + playlist_title[0] + '"]')
                    if len(playlist_element) != 1:
                        logger.exception('Playlist ' + playlist_title[0] + ' not found')
                        continue
                    
                    tracks_of_playlist = playlist_element[0].findall('track_id')

                    track_id = ''
                    if len(tracks_of_playlist) != 0:
                        track = ET.Element('track_id')                 
                                              
                        for track_ele in olive_root.findall('.//artists/artist/albums/album/tracks/track'):                    
                            if track_ele.find('path').text == filename_ext:
                                track_id = track_ele.attrib.get('id_track')
                                break
                        
                        if not track_id:
                            for track_ele in olive_root.findall('.//artists/artist/singles/tracks/track'):                    
                                if track_ele.find('path').text == filename_ext:
                                    track_id = track_ele.attrib.get('id_track')
                                    break
                        
                        if track_id:
                            for track_element in tracks_of_playlist:
                                if track_element.attrib.get('id') == track_id:
                                    next = True
                                    break
                        
                            if next == False:
                                track.set('id',track_id)
                                playlist_element[0].append(track)
                                messages.append('track ' + track_id + ' added to playlist ' + playlist_title[0])
                                
    except Exception as message:
        logger.exception(message)
        sys.exit(str(message))
    
    if not playlists_exists:
        olive_root.append(playlists)
    
    try:
        tree.write(open(folder_navegation['DB_FILE'], 'wb'), encoding='UTF8')
    except:
        print('Error while saving db.xml')
    
    print('')
    if new_playlists_count:
        print('Added ' + str(new_playlists_count) + ' new playlists')
        
    if len(messages) != 0:
        for message in messages:
            print(message)
            
    if len(messages) == 0 and new_playlists_count == 0:
        print('No new playlists added')
        
if __name__ == '__main__':
    read_playlist_from_groove()
    