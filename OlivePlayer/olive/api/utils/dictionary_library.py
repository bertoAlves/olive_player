#general dictionaries library for servers
from datetime import date
import random

#http responses with code and personalized message
#headers
http_responses = {

#-------------------Responses----------------------------
    
    'OK' : {
        'code' : 200,
        #-------------------------PLAYER-----------------------------------
        'playlist_deleted' : 'Playlist deleted successfully',
        'tracks_added_to_queue' : 'Tracks successfully added to queue',
        'tracks_removed_from_queue' : 'Tracks successfully removed from queue',
        'queue_cleared' : 'Queue successfully cleared',
        #----------------------LINK_LIBRARY--------------------------------
        'link_deleted' : 'Link deleted successfully',
        'tag_deleted' : 'Tag deleted successfully',
        'list_deleted' : 'List deleted successfully',
        #--------------------------AUTH------------------------------------
        'successful_login' : 'Login was sucessful',
        'valid_session' : 'Session is valid',
        'logged_out' : 'Succesfully logged out',
    },
      
    'BadRequest' : {       
        'code' : 400,
        #-------------------------PLAYER-----------------------------------
        'wrong_artists_array_parameter' : 'Artist parameter is invalid',
        'wrong_albums_array_parameter' : 'Album parameter is invalid',
        'wrong_tracks_array_parameter' : 'Track parameter is invalid',
        'wrong_playlists_array_parameter' : 'Playlist parameter is invalid',
        'wrong_shuffle_parameter' : 'Shuffle parameter is invalid or missing',
        'wrong_play_session_given' : 'Invalid track selection',
        'wrong_queue_tracks_given' : 'Invalid tracks given to add to queue',
        'wrong_queue_tracks_to_remove_given' : 'Invalid tracks given to remove from queue',
        'wrong_playlist_name' : 'Playlist name must have a maximum of 44 caracters',
        'no_queue_tracks_given' : 'No tracks to add to queue given',
        'no_queue_tracks_to_remove_given' : 'No tracks to remove from queue given',
        'no_play_session_given' : 'No track selection made',
        'no_new_playlist_name' : 'No new playlist name given',
        'no_new_playlist_tracks' : 'No new playlist tracks given',
        'no_playlist_tracks_to_remove' : 'No playlist tracks to remove',
        'no_new_playlist' : 'No new playlist given',
        'no_search_argm' : 'No search argument given',
        #----------------------LINK_LIBRARY--------------------------------
        'no_new_link' : 'No link given',
        'no_new_tag' : 'No tag given',
        'no_new_list' : 'No list given',
        'no_search_arg' : 'No search argument',
        'no_new_attributes_for_link' : 'No new changes defined for link',
        'link_name_and_given_link_are_equal' : 'The given link name must be different',
        'no_new_attributes_for_tag' : 'No new changes defined for tag',
        'no_new_attributes_for_list' : 'No new changes defined for list',
        'list_title_and_given_list_are_equal' : 'The given list title must be different',
        'no_link_name' : 'No link name given',
        'no_tag_title' : 'No tag title given',
        'no_list_title' : 'No list title given',
        'no_link_url' : 'No url description given',
        'no_tags' : 'No tags given',
        'no_time_given' : 'No time given',
        'wrong_link_given' : 'Link is in wrong format',
        'wrong_tag_given' : 'Tag is in wrong format',
        'wrong_list_given' : 'List is in wrong format',
        'wrong_allparameter_given' : '"All" parameter must be true or false',
        'wrong_link_name_given' : 'Link name must be a string and have a maximum of 44 caracters',
        'wrong_tag_ids_given' : 'Tag ids must be a string separated by ;',
        'wrong_link_ids_given' : 'Link ids must be a string separated by ;',
        'wrong_date_given' : 'Date must be in yyyy-mm-dd format',
        'array_or_string' : 'Only one of id & ids must be given',
        'wrong_tag_title_given' : 'Tag title must be a string and have a maximum of 20 caracters',
        'wrong_list_title_given' : 'List title must be a string and have a maximum of 20 caracters',
        'wrong_link_description_given' : 'Link description must be a string and have a maximum of 255 caracters',
        'wrong_list_description_given' : 'List description must be a string and have a maximum of 255 caracters',
        'wrong_link_url_given' : 'Link url is invalid',
        'wrong_tag_color_given' : 'Color must be in hexodecimal format',
        'wrong_tags_parameter' : 'Invalid tags parameter',
        'link_has_no_tags' : 'Link has no tags',
        'list_has_no_links' : 'List has no links',
        'tag_has_no_img' : 'Tag has no image',
        #--------------------------AUTH------------------------------------
        'failed_login' : 'Authentication failed',
        'no_auth' : 'No auth information given',
        'no_session_info' : 'No session info given',
        'no_session' : 'No current session',
        'invalid_session' : 'Session is not valid',
        'session_already_running' : 'A Session is already running',
    },
    
    'NotFound' : {
        'code' : 404,
        'resource_does_not_exist' : 'Requested resource does not exist',
        #-------------------------PLAYER-----------------------------------
        'nothing_found' : 'Nothing found matching the criteria',
        #----------------------LINK_LIBRARY--------------------------------
        'tag_not_found_in_link' : 'Tag was not found in link',
        'no_links_found' : 'No links found matching the criteria',
        'no_tags_found' : 'No tags found matching the criteria',
        'no_tags' : 'No tags found',
        'resource_img_not_found' : 'Resource not found',
        'no_lists_found' : 'No lists found matching the criteria',
        'no_lists' : 'No lists found',
    },
     
    'NotAcceptable' : {
        'code' : 406,
        #-------------------------PLAYER-----------------------------------
        'invalid_playlist_name' : 'Playlist name is wrong',
        'incomprehensible_request_for_play_session' : 'Request is incomprehensible'
    },
    
    'Conflict' : {
        'code' : 409,
        #-------------------------PLAYER-----------------------------------
        'playlist_name_must_be_unique' : 'Playlist name is already in use',
        'no_repetitions' : 'Playlist must not have any repetitions',
        #----------------------LINK_LIBRARY--------------------------------
        'link_name_must_be_unique' : 'Link name must be unique',
        'link_url_must_be_unique' : 'Link url must be unique',
        'tag_must_not_be_repited_in_link' : 'Link already has the given tag',
        'link_must_not_be_repited_in_list' : 'List already has the given link',
        'tag_title_must_be_unique' : 'Tag title must be unique',
        'list_title_must_be_unique' : 'List title must be unique',
    },
    
    'InternalServerError' : {
        'code' : 500,
        'database_conflict' : 'The server encontered a problem while accessing database',
        'request_error' : 'The server encontered a problem while executing the request',
        'couldt_save_changes' : 'The server encontered a problem while trying to save changes' 
    },
    
    'ServiceUnavailable' : {
        'code' : 503,
        'database_access_error' : 'Error ocurred while trying to access database.',
        'server_not_available' : 'Service is not available',
        #-------------------------PLAYER-----------------------------------
        'missing_schema' : 'The server encontered a problem while trying to validate schema',
    },
    
    
    
#--------------------headers----------------------------


    'headers' : {
        'content-type' : 'application/json'
    },

    #-------------------------PLAYER-----------------------------------
    'headers_audio' : {
        'content-type' : 'audio/wav'
    }    
}


#caracter limit
caracter_limit = {
    #-------------------------PLAYER-----------------------------------
    'playlist_name' : 44,
    #----------------------LINK_LIBRARY--------------------------------
    'link_name' : 44,
    'link_description' : 255,
    'tag_title' : 20,
    'list_title' : 20,
    'list_description' : 255,
}



#-------------------------PLAYER-----------------------------------
#help navigate through db.xml
xml_navegation = {   
    'GET_Tracks' : './/track',
    'GET_TracksOfArtist' : 'albums/album/tracks/track',
    'GET_TracksOfAlbum' : 'tracks/track',  
    'GET_Albums' : 'artists/artist/albums/album',
    'GET_SinglesOfArtist' : 'singles',
    'GET_AlbumsOfArtist' : 'albums/album', 
    'GET_Artists' : 'artists/artist',
    'GET_Playlists' : 'playlists/playlist',
    'GET_TracksOfPlaylist' : 'track_id'
}


#defaults
defaults = {
    'link_description' : 'No description',
    'list_description' : 'No description',
    'tag_color' : '#383838',
    'tag_sec_color' : '#b3b1b1'
}


#auth_server

auth_server = {
    'validate_session' : 'http://localhost:100/auth/validate_session'
}

#folder paths
folder_path = {
    'tag_img_folder' : 'C:/Users/catar/OneDrive/Documentos/olive/api/link_library/imgs/tags/',
    'music_folder' : 'C:/Users/catar/Music/'
}

#auth
keys_and_passw = {
    'k_file' : '../key_.ini',
    'p_file' : '../passw_.txt',
    's_file' : '../session',
    'CONFIG_KEY' : 'CONFIDENTIAL',
    'KEY_KEY' : 'KEY'
}

