import os, re, sys
import logging

from lxml import etree

sys.path.append('utils')
from dictionary_library import db_default, folder_navegation

#check if missing files    
def check_for_deletions():
    olive_root = ''
    eliminated_tracks_ids = []
    
    if not os.path.exists(folder_navegation['DB_FILE']):
        print('Database does not exist')
        sys.exit('Run init.py to start database')
    
    if not os.path.exists(folder_navegation['LOG_FOLDER']):
        Path(folder_navegation['LOG_FOLDER']).mkdir(parents=True, exist_ok=True)
        
    logging.basicConfig(filename=folder_navegation['LOG_FILE'], format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger('_DELETS_')
    
    tree = ''   
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse(folder_navegation['DB_FILE'], parser=xmlp)
    except:
        sys.exit('Error while reading db.xml')
        
    olive_root = tree.getroot()
    
    try:
#---navigate albums in db.xml
        for album_element in olive_root.findall('.//album'):
        
    #-------if album's path does not exist, remove album
            if not os.path.exists(folder_navegation['MUSIC_FOLDER']+'/'+album_element.attrib.get('album_path')):
                path = album_element.attrib.get('album_path')           
                albums_element = album_element.getparent()
                artist_element = albums_element.getparent()
                
                #save removed tracks ids
                for track in album_element.findall('.//track'):
                    eliminated_tracks_ids.append(track.attrib.get('id_track'))
                
        #-------if artist only has an album and no singles element, eliminate artist element
                if len(artist_element.findall('.//album')) == 1 and len(artist_element.findall('.//singles')) == 0:
                    artists = artist_element.getparent()
                    artists.remove(artist_element)
                    
        #-------if artist only has an album and has singles element, eliminate the albums element              
                elif len(artist_element.findall('.//album')) == 1:
                    artist_element.remove(albums_element)
                    
        #-------if artist has many albums, eliminate only the specific album element
                else:
                    albums_element.remove(album_element)
                print('ALBUM ' + folder_navegation['MUSIC_FOLDER']+'/'+ path + ' Removed')

               
    #---navigate singles in db.xml
        for singles_element in olive_root.findall('.//singles'):
        
        #-------if singles's path does not exist, remove singles
            if not os.path.exists(folder_navegation['MUSIC_FOLDER']+'/'+singles_element.attrib.get('singles_path')):
                path = singles_element.attrib.get('singles_path')           
                
                #save removed tracks ids
                for track in singles_element.findall('.//track'):
                    eliminated_tracks_ids.append(track.attrib.get('id_track'))
            
                artist_element = singles_element.getparent()
        #-------if artist has no albums, eliminate artist element
                if len(artist_element.findall('.//album')) == 0:
                    artists = artist_element.getparent()
                    artists.remove(artist_element)
                    
        #-------if artist has albums, eliminate only the singles element
                else:
                    artist_element.remove(singles_element)
                print('SINGLES_FOLDER ' + folder_navegation['MUSIC_FOLDER']+'/'+ path + ' Removed')


    #---navigate tranks in db.xml
        for track_element in olive_root.findall('.//track'):
            folderpath = ''
            if track_element.getparent().getparent().tag == 'album':
                folderpath = track_element.getparent().getparent().attrib.get('album_path')
            else:
                folderpath = track_element.getparent().getparent().attrib.get('singles_path')
            
        #-------if track's path does not exist, remove track        
            if not os.path.exists(folder_navegation['MUSIC_FOLDER']+'/'+ folderpath +'/'+track_element.find('path').text):
                path = track_element.find('path').text                       
                #save removed track id
                eliminated_tracks_ids.append(track_element.attrib.get('id_track'))
                
                tracks = track_element.getparent()
            #-------if the track is the only one...       
                if len(tracks.findall('.//track')) == 1:
                    parent_ = tracks.getparent()
                #-------... if track is from album...      
                    if parent_.tag == 'album':
                        albums_element = parent_.getparent()
                        artist_element = albums_element.getparent()
                        #-------... if artist only has one album and no singles, eliminate artist element   
                        if len(artist_element.findall('.//album')) == 1 and len(artist_element.findall('.//singles')) == 0:
                            artists = artist_element.getparent()
                            artists.remove(artist_element)
                        #-------... if artist only has one album and has singles, eliminate albums element   
                        elif len(artist_element.findall('.//album')) == 1:
                            artist_element.remove(albums_element)
                        #-------... if artist only has more than one album, eliminate album element
                        else:
                            albums_element.remove(parent_)
                            
                #-------... if track is from singles...                             
                    else:
                        artist_element = parent_.getparent()
                        
                    #-------... if artist only has singles and no albums, eliminate artist element 
                        if len(artist_element.findall('.//album')) == 0:
                            artists = artist_element.getparent()
                            artists.remove(artist_element)
                    #-------... if artist only has singles and albums, only eliminate singles element
                        else:
                            artist_element.remove(parent_)
                            
            #-------if more than one track, eliminate track 
                else:
                    tracks.remove(track_element)
                print('TRACK ' + folder_navegation['MUSIC_FOLDER']+'/'+ folderpath +'/'+ path + ' Removed')
                
    except Exception as message:
        logger.exception(message)
        sys.exit(str(message)) 
    
#-------for each track_id in playslist, remove references to eliminated ids... 
    for track_id_element in olive_root.findall('.//track_id'):
        if track_id_element.attrib.get('id') in eliminated_tracks_ids:
            track_id_element.getparent().remove(track_id_element)
    
    try:
        tree.write(open(folder_navegation['DB_FILE'], "wb"), encoding='UTF8')
    except:
        print('')
        sys.exit('Error while saving updates to files')
        

if __name__ == '__main__':
    check_for_deletions()