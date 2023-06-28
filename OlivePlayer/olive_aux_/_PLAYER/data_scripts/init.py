import os, re, sys, datetime, xlsxwriter, subprocess
import xml.etree.ElementTree as ET
import logging

from xml.dom import minidom
from tinytag import TinyTag
from pathlib import Path

sys.path.append('utils')
from dictionary_library import db_default, folder_navegation
from validations import *
from normalizations import removeLeading0s
from conversions import *
from tools import *

#starts database, tracks, albums and artists
def start_database():

    if not os.path.exists(folder_navegation['LOG_FOLDER']):
        Path(folder_navegation['LOG_FOLDER']).mkdir(parents=True, exist_ok=True)
        
    logging.basicConfig(filename=folder_navegation['LOG_FILE'], format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger('_INIT_')

    #Validate if db file exists. if so update with target folder changes. if not create new database
    if os.path.exists(folder_navegation['DB_FILE']):
        print('Database already available.')
        sys.exit("Run updts.py to update database")

    # root tag olive
    olive = ET.Element('olive')
    tree = ET.ElementTree(olive)

    # artists tag
    artists = ET.SubElement(olive, 'artists')
    playlists = ET.SubElement(olive, 'playlists')

    #music, album, artist ids
    music_identifier = 0
    album_identifier = 0
    artist_identifier = 0

    #auxiliaries
    last_album = ''
    last_artist = ''

    #defaults
    default_artist = 1
    default_album_title = 1
    default_music_title = 1
    
    file_error = ''
    last_artist_id = False
    i = 0
    try:
#-------for all directories (albums) in MUSIC_FOLDER, search for audio files
        for root, dirs, files in os.walk(folder_navegation['MUSIC_FOLDER']):
            printProgressBar(i, len(os.listdir(folder_navegation['MUSIC_FOLDER'])), prefix = 'Progress:', suffix = 'Complete', length = 50)
            i += 1 
       
            if len(files) == 0:
                continue
            
            dirname = os.path.basename(os.path.dirname(os.path.join(root, files[0])))
            
            is_album_folder = validateAlbumFolder(dirname)
            is_singles_folder = validateSinglesFolder(dirname)
            
            if not is_album_folder and not is_singles_folder:
                continue
            
            new_album = False
            last_album_id = False
#-----------for each file
            for file in files:
                
                #validate if file is audio file
                if validateAudioFileExtension(file):
                            
                    tag = TinyTag.get(os.path.join(root, file))                                 
                    album_folder_info = os.path.basename(os.path.dirname(os.path.join(root, file)))
                   
                    folder_info = None
                    if is_album_folder:
                        folder_info = segment_album_folder(album_folder_info)
                    else:
                        folder_info = segment_singles_folder(album_folder_info)
                             
                    filename_ext = separate_file_from_extension(file)                   
                    if not folder_info:
                        logger.info('Failed to segment folder info -' + album_folder_info)
                        logger.exception('Failed to segment folder info')
                        continue
                        
                    if not filename_ext:
                        logger.info('Failed to segment file info' + file)
                        logger.exception('Failed to segment file info' + file)
                        continue
                    
                    artist_element = None
                    try:
                        artist_element = artists.findall('.//artist[@artist_name="' + tag.albumartist + '"]')
                    except Exception as message:
                        logger.info('FILE-'+ file + ' has no albumartist tag')
                        logger.exception(message)
                        continue
                    
#-------------------if artist exists                    
                    if len(artist_element) == 1:
                        artist_element = artist_element[0]
                        
    #-------------------if album
                        if is_album_folder:                       
                            albums_element = artist_element.findall('.//albums')
                            album_element = albums_element[0].findall('.//album[@title="' + tag.album + '"]')
                            
        #-------------------if album does not exist                    
                            if len(album_element) == 0:
                                album_identifier += 1
                                album = ET.SubElement(albums_element[0], 'album')
                                album.set('id_album',str(album_identifier))

                                tracks = ET.SubElement(album, 'tracks')
                                if tag.album != None and tag.album.strip():
                                    album.set('title', tag.album)
                                elif folder_info[1] != None and folder_info[1].strip():
                                    album.set('title',folder_info[1])
                                else:
                                    logger.info('FILE-'+ file + ' has no album tag')
                                    logger.exception('File has no album tag')
                                    continue
                                    
                                if tag.year != None and tag.year.strip():
                                    if len(tag.year)>4:
                                        album.set('year', tag.year[:4])
                                    else:
                                        album.set('year', tag.year)
                                elif folder_info[2] != None and folder_info[2].strip():
                                    album.set('year',folder_info[2]) 
                                else:
                                    logger.info('FILE-'+ file + ' has no year tag')
                                    logger.exception('File has no year tag')
                                    continue
                                    
                                album.set('album_path', dirname)
                                
    #-------------------if singles                           
                        else:
                            singles_element = artist_element.findall('.//singles')
                            if len(singles_element) == 1:
                                tracks = singles_element[0].find('tracks')
                            elif len(singles_element) == 0:
                                singles = ET.SubElement(artist_element, 'singles')
                                singles.set('singles_path', dirname)
                                tracks = ET.SubElement(singles, 'tracks')
                            else:
                                logger.error('DB.XML has more than one "singles" element')
                                sys.exit('DB.XML has more than one "singles" element')

#-------------------if artist does not exist                          
                    elif len(artist_element) == 0:
                        artist_identifier += 1                        
                        artist = ET.SubElement(artists, 'artist')
                        
                        albums = ''
                        album = ''
                        tracks = ''
                        
    #-------------------if album, create album element
                        if is_album_folder:
                            album_identifier += 1
                            albums = ET.SubElement(artist, 'albums')
                            album = ET.SubElement(albums, 'album')
                            album.set('id_album',str(album_identifier))                        
                            tracks = ET.SubElement(album, 'tracks')
    #-------------------if singles, create singles element
                        else:
                            singles = ET.SubElement(artist, 'singles')
                            singles.set('singles_path', dirname) 
                            tracks = ET.SubElement(singles, 'tracks')
                           
                        artist.set('id_artist',str(artist_identifier))
                        artist.set('inFolderAs', folder_info[0])

                        if tag.albumartist != None and tag.albumartist.strip():
                            artist.set('artist_name', tag.albumartist)
                        else:
                            logger.info('FILE-' + file + ' has no albumartist tag')
                            logger.exception('File has no albumartist tag')
                            continue
                            
    #-------------------if album, specify album atributes           
                        if is_album_folder:
                            if tag.album != None and tag.album.strip():
                                album.set('title', tag.album)
                            elif folder_info[1] != None and folder_info[1].strip():
                                album.set('title',folder_info[1])
                            else:
                                logger.info('FILE-'+ file + ' has no album tag')
                                logger.exception('File has no album tag')
                                continue
                            
                            if tag.year != None and tag.year.strip():
                                if len(tag.year)>4:
                                    album.set('year', tag.year[:4])
                                else:
                                    album.set('year', tag.year)
                            elif folder_info[2] != None and folder_info[2].strip():
                                album.set('year',folder_info[2]) 
                            else:
                                logger.info('FILE-' + file + ' has no year tag')
                                logger.exception('File has no year attribute')
                                continue
                        
                            album.set('album_path', dirname)
                        
                    else:
                        logger.info('DB.XML has more than one artist' + tag.albumartist + ' element')
                        sys.exit('DB.XML has more than one artist' + tag.albumartist + ' element')
                        
    #---------------Add new track to tracks element                    
                    already_exists = False
                    tracks_path = tracks.findall('.//path')
                    for t_path in tracks_path:
                        if t_path.text == file:
                            logger.info('FILE- '+ file + 'already exists')                                
                            logger.exception('File already exists')
                            already_exists = True
                            break   
                    
                    if already_exists:
                        continue
                        
                    music = ET.SubElement(tracks, 'track')
                    music_identifier += 1
                    music.set('id_track',str(music_identifier))
                    
                    track = ET.SubElement(music, 'track_number')
                    title = ET.SubElement(music, 'track_title')
                    trackartists = ET.SubElement(music, 'authors')
                    duration = ET.SubElement(music, 'duration')
                    path = ET.SubElement(music, 'path')
                                       
                    music.set('used','0')
                    if tag.track != None and tag.track.split():
                        track.text = str(removeLeading0s(tag.track))
                    else:
                        logger.info('FILE-' + file + ' has no track number tag')
                        logger.exception('File has no track number tag')
                        continue
                    
                    if tag.title != None and tag.title.strip():
                        title.text = tag.title
                    elif music_file_name != None and music_file_name.strip():
                        title.text = music_file_name
                    else:
                        logger.info('FILE-' + file + ' has no track title tag')
                        logger.exception('File has no track title tag')
                        continue
                    
                    if tag.artist != None and tag.artist.strip():
                        trackartists.text = tag.artist
                    elif tag.albumartist != None and tag.albumartist.strip():
                        trackartists.text = tag.albumartist
                    else:
                        logger.info('FILE-' + file + ' has no track artists tag')
                        logger.exception('File has no track artists tag')
                        continue
                    
                    if tag.duration != None and tag.duration>0:
                        duration_mm_ss = datetime.timedelta(seconds=tag.duration)               
                        duration.text = str(duration_mm_ss)[:-7]                
                    else:
                        logger.info('FILE-' + file + ' has no duration tag')
                        logger.exception('File has no duration tag')
                        continue                      
                    path.text = file
            
    except Exception as message:
        logger.exception(message)
        sys.exit(str(message))
        
    try:
        tree.write(open(folder_navegation['DB_FILE'], 'wb'), encoding='UTF8')
        print('')
        print('Inserted ' + str(artist_identifier) + ' artists')
        print('Inserted ' + str(album_identifier) + ' albums')
        print('Inserted ' + str(music_identifier) + ' tracks')
        print('')
    except Exception as message:
        logger.exception(message)
        sys.exit(str(message))
    

if __name__ == '__main__':
    start_database()
    

