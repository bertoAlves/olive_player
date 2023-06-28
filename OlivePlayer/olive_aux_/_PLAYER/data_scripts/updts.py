import os, re, sys, datetime, xlrd
import xml.etree.ElementTree as ET
import xlwings
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

#checks if album is in database
def check_if_album_in_database(folder, folder_info, root, is_album):      
    fld = ''
    if is_album:
        fld = root.findall('.//artists/artist/albums/album[@album_path="' + folder + '"]')
    else:
        fld = root.findall('.//artists/artist/singles[@singles_path="' + folder + '"]')
    
    if len(fld) == 1:
        return True
    elif len(fld) == 0:
        artist = root.findall('.//artists/artist[@inFolderAs="' + folder_info[0] + '"]')
        if len(artist) == 1:
            return artist[0]
        elif len(artist) == 0:
            return False
        else:
            sys.exit('Error while checking if ' + folder + ' artist is in database')  
    else:
        sys.exit('Error while checking if ' + folder + ' is in database')

#checks if track is in database and if it is possible to add new track.
#Returns false if not possible. And the album_id if possible.
def check_if_album_track_is_in_database(root, album, file, is_album_folder): 
    
    folder = ''
    if is_album_folder:
        folder = root.findall('.//artists/artist/albums/album[@album_path="' + album + '"]')
    else:
        folder = root.findall('.//artists/artist/singles[@singles_path="' + album + '"]')
    
    if len(folder) == 1:
        for tracks_path in folder[0].findall('.//tracks/track/path'):
            if tracks_path.text == file:
                return True
    else:
        sys.exit('Error while getting folder')
        
    return folder

#Gets a new album_id
def get_new_album_id(root):
    new_id = 0
    for album in root.findall('.//artists/artist/albums/album'):
        if new_id < int(album.attrib.get('id_album')):
            new_id = int(album.attrib.get('id_album'))
    new_id += 1
    return new_id

#Gets a new artist_id
def get_new_artist_id(root):
    new_id = 0
    for artist in root.findall('.//artists/artist'):
        if artist.attrib.get('id_artist'):
            if new_id < int(artist.attrib.get('id_artist')):
                new_id = int(artist.attrib.get('id_artist'))
    new_id += 1
    return new_id

#Gets a new track_id    
def get_new_track_id(root):
    new_id = 0
    for track in root.findall('.//artists/artist/albums/album/tracks/track'):
        if track.attrib.get('id_track'):
            if new_id < int(track.attrib.get('id_track')):
                new_id = int(track.attrib.get('id_track'))            
    for track in root.findall('.//artists/artist/singles/tracks/track'):
        if track.attrib.get('id_track'):
            if new_id < int(track.attrib.get('id_track')):
                new_id = int(track.attrib.get('id_track'))
            
    new_id += 1
    return new_id


#Add new tracks to database. Including new albums and new artists
def add_new_tracks_to_db():
    olive_root = ''
       
    if not os.path.exists(folder_navegation['DB_FILE']):
        print('Database does not exist')
        sys.exit('Run init.py to start database')
    
    if not os.path.exists(folder_navegation['LOG_FOLDER']):
        Path(folder_navegation['LOG_FOLDER']).mkdir(parents=True, exist_ok=True)
        
    logging.basicConfig(filename=folder_navegation['LOG_FILE'], format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger('_UPDTS_')
    
    tree = ''   
    try:
        xmlp = ET.XMLParser(encoding='utf-8')
        tree = ET.parse(folder_navegation['DB_FILE'], parser=xmlp)
    except:
        sys.exit('Error while reading db.xml')
        
    olive_root = tree.getroot()
    
    new_artists_count = 0
    new_albums_count = 0
    new_tracks_count = 0
    
    default_artist = 1
    default_album_title = 1
    default_music_title = 1
    
    albums_to_check_for_new_songs = []
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
          
            #validate if album is in correct format     
            if not is_album_folder and not is_singles_folder:
                continue
                            
            folder_info = ''
            in_database = ''
            if is_album_folder:
                folder_info = segment_album_folder(dirname)
                in_database = check_if_album_in_database(dirname, folder_info, olive_root, True) 
            else:
                folder_info = segment_singles_folder(dirname)
                in_database = check_if_album_in_database(dirname, folder_info, olive_root, False)  
            
    #-------if not new folder check and was updated recently check for new songs
            modifiedDate = datetime.datetime.fromtimestamp(os.path.getmtime(folder_navegation['MUSIC_FOLDER']+dirname))   
            todaysDate = datetime.datetime.today()
            modifyDateLimit = modifiedDate + datetime.timedelta(days=1)         
            if in_database == True and (todaysDate < modifyDateLimit):
                albums_to_check_for_new_songs.append(dirname)
                continue
    #-------if not new folder check and wasnt updated recently continue
            elif in_database == True:
                continue
    #-------if new folder add to database
            else:
                new_album = True
                artist = ''
                albums = ''
                album = ''
                tracks = ''
                artists_element = olive_root.find('artists')
                last_artist_id = False
                last_album_id = False
                            
        #-------navigate files    
                for file in files:
                        
                    new_artist_id = False
                    new_album_id = False
                
            #-------check if artist exists or not
                    in_database = ''
                    if is_album_folder:
                        in_database = check_if_album_in_database(dirname, folder_info, olive_root, True) 
                    else:
                        in_database = check_if_album_in_database(dirname, folder_info, olive_root, False)  
                    
                #---validate if file is audio file
                    if validateAudioFileExtension(file):
                        tag = TinyTag.get(os.path.join(root, file))
                                               
                        filename_ext = separate_file_from_extension(file)                    
                        if not folder_info:
                            logger.info('Failed to segment folder info-'+album_folder_info)
                            logger.exception('Failed to segment folder info')
                            continue
                            
                        if not filename_ext:
                            logger.info('Failed to segment file info' + file)
                            logger.exception('Failed to segment file info' + file)
                            continue
                        
                    #---if artist is not in database and is folder is not in database, create artist and folder(album or singles) element
                        if in_database == False and new_album:
                            new_artists_count += 1
                            new_albums_count += 1
                            artist = ET.SubElement(artists_element, 'artist')
                            
                            artist_identifier = get_new_artist_id(olive_root)
                            album_identifier = get_new_album_id(olive_root)
                            new_album = False
                            
                            albums = ''
                            album = ''
                            tracks = ''
                            
                        #---if is folder is album
                            if is_album_folder:
                                albums = ET.SubElement(artist, 'albums')
                                album = ET.SubElement(albums, 'album')
                                album.set('id_album',str(album_identifier))
                                album_identifier += 1
                                tracks = ET.SubElement(album, 'tracks')
                        
                        #---if is folder is singles
                            else:
                                singles = ET.SubElement(artist, 'singles')
                                singles.set('singles_path', dirname) 
                                tracks = ET.SubElement(singles, 'tracks')
                                                        
                            new_artist_id = artist_identifier
                            new_album_id = album_identifier
                            
                            last_artist_id = new_artist_id
                            last_album_id = new_album_id
                            
                            artist.set('id_artist',str((int(artist_identifier))))
                            artist.set('inFolderAs', folder_info[0])                           
                            if tag.albumartist != None and tag.albumartist.strip():
                                artist.set('artist_name', tag.albumartist)
                            else:
                                logger.info('FILE-' + file + ' has no albumartist tag')
                                logger.exception('File has no albumartist tag')
                                continue

                        #---if is folder is album, add album attributes                            
                            if is_album_folder:
                                if tag.albumartist != None and tag.albumartist.strip():
                                    artist.set('artist_name', tag.albumartist)
                                else:
                                    logger.info('FILE-' + file + ' has no albumartist tag')
                                    logger.exception('File has no albumartist tag')
                                    continue
                                    
                                if tag.album != None and tag.album.strip():
                                    album.set('title', tag.album)
                                elif folder_info[1] != None and folder_info[1].strip():
                                    album.set('title',folder_info[1])
                                else:
                                    logger.info('FILE-' + file + ' has no album tag')
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
                                    logger.exception('File has no year tag')
                                    continue
                                
                                album.set('album_path',dirname)

                    #---if artist is in the database and the folder is not, create folder(album or singles) element                                                  
                        elif new_album:
                            new_albums_count += 1
                            new_album = False
                            
                        #---if is folder is album
                            if is_album_folder:
                                album_identifier = get_new_album_id(olive_root)
                                new_album_id = album_identifier
                                last_album_id = new_album_id
                                
                                album = ET.SubElement(in_database.find('albums'),'album')
                                tracks = ET.SubElement(album, 'tracks')
                                album.set('id_album',str((int(album_identifier))))                                                     
                                if tag.album != None and tag.album.strip():
                                    album.set('title', tag.album)
                                elif folder_info[1] != None and folder_info[1].strip():
                                    album.set('title',folder_info[1])
                                else:
                                    logger.info('FILE-' + file + ' has no album tag')
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
                                    logger.exception('File has no year tag')
                                    continue
                                    
                                album.set('album_path',dirname)
                                
                        #---if is folder is singles
                            else:
                                singles = ET.SubElement(in_database, 'singles')
                                singles.set('singles_path', dirname) 
                                tracks = ET.SubElement(singles, 'tracks')

                        
                        music = ET.SubElement(tracks, 'track')
                    
                        track = ET.SubElement(music, 'track_number')
                        title = ET.SubElement(music, 'track_title')
                        trackartists = ET.SubElement(music, 'authors')
                        duration = ET.SubElement(music, 'duration')
                        path = ET.SubElement(music, 'path')
                    
                        album_identifier = get_new_track_id(olive_root)
                        music.set('id_track',str(album_identifier))
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
                        
                        new_tracks_count += 1
                        path.text = file
    except Exception as message:
        logger.exception(message)
        sys.exit(str(message))           
    
    messages = []
    artists_element = olive_root.find('artists')

#---if there are albums to check
    if len(albums_to_check_for_new_songs)!=0:
    
    #---for each album to check, navigate files
        for album in albums_to_check_for_new_songs:
        
            is_album_folder = validateAlbumFolder(album)
            is_singles_folder = validateSinglesFolder(album)
        
            for root, dirs, files in os.walk(folder_navegation['MUSIC_FOLDER']+album):
                for file in files:
                    if validateAudioFileExtension(file):
                    
                        track_in_database = check_if_album_track_is_in_database(olive_root,album, file, is_album_folder)
                        filename_ext = separate_file_from_extension(file)
                        
                    #---if file is in database, continue to next iteration
                        if track_in_database == True:
                            continue
                        
                        tag = TinyTag.get(os.path.join(root, file))
                    
                        if is_album_folder:
                            segmented_folder = segment_album_folder(dirname)
                        else:
                            segmented_folder = segment_singles_folder(dirname)
                        
                        music = ET.SubElement(track_in_database[0].find('tracks'),'track')
                    
                        track = ET.SubElement(music, 'track_number')
                        title = ET.SubElement(music, 'track_title')
                        trackartists = ET.SubElement(music, 'authors')
                        duration = ET.SubElement(music, 'duration')
                        path = ET.SubElement(music, 'path')
                        
                        album_identifier = get_new_track_id(olive_root)
                        music.set('id_track',str(album_identifier))
                        music.set('used','0')
                        
                        if tag.track != None and tag.track.split():
                            track.text = str(removeLeading0s(tag.track))
                        else:
                            logger.info('FILE-' + file + ' has no duration tag')
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
                        new_tracks_count += 1
                        messages.append('File ' + file + ' added to ' + album)

    try:
        tree.write(open(folder_navegation['DB_FILE'], "wb"), encoding='UTF8')
        print('')
        if new_tracks_count != 0:
            print('Inserted ' + str(new_artists_count) + ' new artists')
            print('Inserted ' + str(new_albums_count) + ' new albums')
            print('Inserted ' + str(new_tracks_count) + ' new tracks')
            print('')
        
        if len(messages) != 0:
            for message in messages:
                print(message)
                
        if len(messages) == 0 and new_tracks_count == 0:
            print('No updates')
            
    except Exception as message:
        logger.exception(message)
        sys.exit(str(message))
    
    
if __name__ == '__main__':
    add_new_tracks_to_db()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    