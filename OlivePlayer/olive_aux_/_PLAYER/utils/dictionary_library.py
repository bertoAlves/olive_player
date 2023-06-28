#general dictionaries library
from datetime import date
import random

#help navigate through db.xml
xml_navegation = {    
    'GET_Tracks' : './/artists/artist/albums/album/tracks/track',
    'GET_TracksOfArtist' : './/albums/album/tracks/track',
    'GET_TracksOfAlbum' : './/tracks/track',  
    'GET_Albums' : './/artists/artist/albums/album',
    'GET_AlbumsOfArtist' : './/albums/album', 
    'GET_Artists' : './/artists/artist',
    'GET_Playlists' : './/playlists/playlist',
    'GET_TracksOfPlaylist' : './/track_id'
}

#help navigate through folders
folder_navegation = {
    'LOG_FILE' : 'C:/Users/catar/OneDrive/Documentos/olive_aux_/_PLAYER/log/player_log_.log',
    'LOG_FOLDER' : 'C:/Users/catar/OneDrive/Documentos/olive_aux_/_PLAYER/log',
    'MUSIC_FOLDER' : 'C:/Users/catar/Music/',
    'PLAYLISTS_FOLDER' : 'C:/Users/catar/Music/Playlists',
    'PLAYLISTS_XML_FOLDER' : 'C:/Users/catar/Music/Playlists_xml/',
    'DBVERSION_FOLDER' : 'C:/Users/catar/OneDrive/Documentos/olive_aux_/_PLAYER/db_versions',
    'DB_FOLDER' : 'C:/Users/catar/OneDrive/Documentos/olive/api/player/database',
    'DB_FILE' : 'C:/Users/catar/OneDrive/Documentos/olive/api/player/database/db.xml',
    'CONFIG_FILE' : 'olive_.ini',
    'SCHEMA_FILE' : 'xml_schema.xsd',    
}

#default atributes for dm.xml
db_default = {
    'DEFAULT_year' : date.today().year,
    'DEFAULT_artist' : 'Default_artist',
    'DEFAULT_album_title' : 'Default_album_title',   
    'DEFAULT_track_number' : random.randrange(1,255),
    'DEFAULT_music_title' : 'Default_music_title',
    'DEFAULT_music_artist' : 'Default_music_artists',
    'DEFAULT_music_duration' : '0:00:01',
}

#audio file extensions permitted
audio_files_extensions = ['.mp3','.flac','.m4a']
