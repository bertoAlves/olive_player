import xmltodict, os, sys
import xml.etree.ElementTree as ET
from lxml import etree

sys.path.append('../../utils')
from dictionary_library import xml_navegation


#---------------------------------------------------------------------WILL RETURN IMAGES ASWELL
#returns searches matching the criteria
#returns -1 in case error while trying to access db.xml file content
#returns -2 in case nothing is found
def search_query(search, artists_arg=True, albums_arg=True, tracks_arg=True, playlists_arg=True):
    root = ''
    try:
        xmlp = etree.XMLParser(encoding='utf-8')
        tree = etree.parse('../database/db.xml', parser=xmlp)
        root = tree.getroot()
    except:
        return -1
    
    playlists = []
    if playlists_arg:
        for it in search:
            try:
                for playlist_element in root.findall('.//playlist'):
                    if it.lower() in playlist_element.attrib.get('name').lower():
                        playlist = {}        
                        playlist['id'] = playlist_element.attrib.get('id_playlist')
                        playlist['name'] = playlist_element.attrib.get('name')
                        playlists.append(playlist)
                        playlist_element.getparent().remove(playlist_element)
            except:
                return -1
                
    tracks = []
    if tracks_arg:
        for it in search:
            try:
                for track_title in root.findall('.//track_title'):
                    track_element = track_title.getparent()
                    if it.lower() in track_title.text.lower():
                        track = {}
                        track['id'] = track_element.attrib.get('id_track')
                        track['track_number'] = track_element.find('.//track_number').text
                        if track_element.getparent().getparent().tag == 'album':
                            track['artist_id'] = track_element.getparent().getparent().getparent().getparent().attrib.get('id_artist')
                            track['artist_name'] = track_element.getparent().getparent().getparent().getparent().attrib.get('artist_name')
                            track['album_id'] = track_element.getparent().getparent().attrib.get('id_album')
                            track['album_title'] = track_element.getparent().getparent().attrib.get('title')
                        else:
                            track['artist_id'] = track_element.getparent().getparent().getparent().attrib.get('id_artist')
                            track['artist_name'] = track_element.getparent().getparent().getparent().attrib.get('artist_name')
                            track['single'] = 'SINGLE'                           
                        track['track_title'] = track_element.find('.//track_title').text
                        track['authors'] = track_element.find('.//authors').text
                        track['duration'] = track_element.find('.//duration').text
                        tracks.append(track) 
                        track_element.getparent().remove(track_element)
            except:
                return -1
                
    albums = []
    if albums_arg:
        for it in search:
            try:
                for album_element in root.findall('.//album'):
                    if it.lower() in album_element.attrib.get('title').lower() or it.lower() in album_element.attrib.get('year').lower():
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
                        album_element.getparent().remove(album_element)
            except:
                return -1
    
    artists = []
    if artists_arg:
        for it in search:
            try:
                for artist_element in root.findall('.//artist'):
                    if it.lower() in artist_element.attrib.get('artist_name').lower():
                        artist = {}
                        artist['id'] = artist_element.attrib.get('id_artist')
                        artist['artist_name'] = artist_element.attrib.get('artist_name')
                        artists.append(artist)
                        artist_element.getparent().remove(artist_element)
            except:
                return -1     
    
    if not artists and not albums and not tracks and not playlists:
        return -2
        
    search = {}
    if artists:
        search['artists'] = artists
        
    if albums:    
        search['albums'] = albums

    if tracks:
        search['tracks'] = tracks
    
    if playlists:
        search['playlists'] = playlists
        
    return search
