import os, sys, json
import urllib.request
import http.client

from flask import Flask, Blueprint, request

sys.path.append('../services')
from artistservice import *
from albumservice import *
from trackservice import *
from playlistservice import *
from searchservice import *

sys.path.append('../../utils')
from dictionary_library import http_responses, caracter_limit

library_blueprint = Blueprint('library_blueprint', __name__)

#----------------------------------------------------------------------------------QUERIES----------------------------------------------------------------------------------------
#returns items matchin search criteria
@library_blueprint.route("/search", methods=['GET'])
def search():
    search_arg = request.args.get('search')   
    if search_arg is None:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_search_argm']
        return msg, code       

    artists_arg = request.args.get('artists')
    if artists_arg is None or (artists_arg != "True"):
        artists_arg = False

    albums_arg = request.args.get('albums')
    if albums_arg is None or (albums_arg != "True"):
        albums_arg = False

    tracks_arg = request.args.get('tracks')
    if tracks_arg is None or (tracks_arg != "True"):
        tracks_arg = False

    playlists_arg = request.args.get('playlists')
    if playlists_arg is None or (playlists_arg != "True"):
        playlists_arg = False

    res = search_info(search_arg, artists_arg, albums_arg, tracks_arg, playlists_arg)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['nothing_found']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers       


#returns artists
@library_blueprint.route("/artist/all", methods=['GET'])
def artists(): 
    res = all_artists_info()
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers        
    
    
#returns albums of artist
@library_blueprint.route("/artist/<int:artist>/albums", methods=['GET'])
def albums_of_artist(artist): 
    res = albums_of_artist_info(artist)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers

        
#returns albums of a list of artists
@library_blueprint.route("/artist/<string:artists>/albums", methods=['GET'])
def albums_of_artists(artists): 
    res = albums_of_artists_info(artists)
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_artists_array_parameter']
        return msg, code
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers

    
#returns tracks of artist
@library_blueprint.route("/artist/<int:artist>/tracks", methods=['GET'])
def tracks_of_artist(artist): 
    res = tracks_of_artist_info(artist)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers

        
#returns tracks of a list of artists
@library_blueprint.route("/artist/<string:artists>/tracks", methods=['GET'])
def tracks_of_artists(artists): 
    res = tracks_of_artists_info(artists)
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_artists_array_parameter']
        return msg, code
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#returns singles of artist
@library_blueprint.route("/artist/<int:artist>/singles", methods=['GET'])
def singles_of_artist(artist):
    res = singles_of_artist_info(artist)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
    
     
#returns tracks of album
@library_blueprint.route("/album/all", methods=['GET'])
def albums():
    res = all_albums_info()
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers   


#returns tracks of artist
@library_blueprint.route("/album/<int:album>/tracks", methods=['GET'])
def tracks_of_album(album): 
    res = tracks_of_album_info(album)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#returns tracks of a list of albums
@library_blueprint.route("/album/<string:albums>/tracks", methods=['GET'])
def tracks_of_albums(albums): 
    res = tracks_of_albums_info(albums)
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_albums_array_parameter']
        return msg, code
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#returns all tracks
@library_blueprint.route("/tracks/all", methods=['GET'])
def all_tracks(): 
    res = all_tracks_info()
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
  
  
#returns track by id
@library_blueprint.route("/tracks/<int:track>", methods=['GET'])
def tracks_by_id(track): 
    res = track_by_id_info(track)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code 
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#returns tracks by a list of ids
@library_blueprint.route("/tracks/<string:tracks>", methods=['GET'])
def tracks_by_listids(tracks): 
    res = tracks_by_listids_info(tracks)
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tracks_array_parameter']
        return msg, code
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers      


#returns tracks of album
@library_blueprint.route("/playlist/all", methods=['GET'])
def playlists():
    res = all_playlists_info()
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers  

#returns tracks of playlist
@library_blueprint.route("/playlist/<int:playlist>/tracks", methods=['GET'])
def tracks_of_playlist(playlist): 
    res = tracks_of_playlist_info(playlist)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
        
       
#returns tracks of a list of playlists
@library_blueprint.route("/playlist/<string:playlists>/tracks", methods=['GET'])
def tracks_of_playlists(playlists): 
    res = tracks_of_playlists_info(playlists)
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_playlists_array_parameter']
        return msg, code
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers

#-------------------------------------------------------------------------------TRANSACTIONS--------------------------------------------------------------------------------------
#change current playlist name   
@library_blueprint.route("/playlist/new", methods=["POST"])
def create_playlist():
    new_playlist_request = request.json
    
    new_playlist_dict = ''
    try: 
        new_playlist_dict = new_playlist_request['new_playlist']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_playlist']
        return msg, code
        
    if not isinstance(new_playlist_dict, dict):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_playlist']
        return msg, code
   
    name = ''  
    try:
        name = new_playlist_dict['name']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_playlist_name']
        return msg, code
    
    if not isinstance(name, str) or len(name) > caracter_limit['playlist_name'] or not name.strip():
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_playlist_name']
        return msg, code
    
    tracks = None
    try:
        tracks = new_playlist_dict['tracks']
    except:
        tracks = None
        
    if not isinstance(tracks, list):
        tracks = None  
    
    res = ''
    if tracks:
        res = create_playlist_ts(name, tracks=tracks)
    else:
        res = create_playlist_ts(name)
     
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tracks_array_parameter']
        return msg, code
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['database_conflict']
        return msg, code
    elif res == -4:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['missing_schema']
        return msg, code
    elif res == -5:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['no_repetitions']
        return msg, code
    elif res == -6:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['playlist_name_must_be_unique']
        return msg, code   
    elif res == -7:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code   
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#change current playlist name   
@library_blueprint.route("/playlist/<int:playlist>/<string:current_playlist_name>", methods=["PUT"])
def change_playlist_name(playlist, current_playlist_name):
    new_playlist_name = request.json
    
    playlist_name = ''
    try: 
        playlist_name = new_playlist_name['new_playlist_name']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_playlist_name']
        return msg, code
    finally:
        if playlist_name == '' or not playlist_name.split():
            code = http_responses['BadRequest']['code']
            msg = http_responses['BadRequest']['no_new_playlist_name']
            return msg, code
    
    if not isinstance(playlist_name, str) or len(playlist_name) > caracter_limit['playlist_name'] or not playlist_name.strip() or len(current_playlist_name) > caracter_limit['playlist_name'] or not current_playlist_name.strip():
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_playlist_name']
        return msg, code
    
    res = change_playlist_name_ts(playlist, current_playlist_name, playlist_name)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    elif res == -4:
        code = http_responses['NotAcceptable']['code']
        msg = http_responses['NotAcceptable']['invalid_playlist_name']
        return msg, code
    elif res == -5:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['missing_schema']
        return msg, code
    elif res == -6:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['playlist_name_must_be_unique']
        return msg, code
    elif res == -7:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#add track to playlist  
@library_blueprint.route("/playlist/<int:playlist>/add/<int:track>", methods=["PUT"])
def add_track_to_playlist(playlist, track): 
    res = add_track_to_playlist_ts(playlist, track)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    elif res == -4:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['missing_schema']
        return msg, code
    elif res == -5:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['no_repetitions']
        return msg, code
    elif res == -6:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code   
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#add tracks to playlist   
@library_blueprint.route("/playlist/<int:playlist>/add/", methods=["PUT"])
def add_tracks_to_playlist(playlist):
    new_playlist_tracks = request.json
    
    playlist_tracks = ''
    try: 
        playlist_tracks = new_playlist_tracks['new_playlist_tracks']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_playlist_tracks']
        return msg, code
    finally:
        if not isinstance(playlist_tracks, list) or len(playlist_tracks) == 0:
            code = http_responses['BadRequest']['code']
            msg = http_responses['BadRequest']['no_new_playlist_tracks']
            return msg, code 
            
    res = add_tracks_to_playlist_ts(playlist, playlist_tracks)
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tracks_array_parameter']
        return msg, code
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    elif res == -3:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['playlist_name_must_be_unique']
        return msg, code
    elif res == -4:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['missing_schema']
        return msg, code
    elif res == -5:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['no_repetitions']
        return msg, code
    elif res == -6:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code   
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#remove track from playlist  
@library_blueprint.route("/playlist/<int:playlist>/remove/<int:track>", methods=["PUT"])
def remove_track_from_playlist(playlist, track): 
    res = remove_track_from_playlist_ts(playlist, track)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    elif res == -4:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#remove tracks from playlist   
@library_blueprint.route("/playlist/<int:playlist>/remove/", methods=["PUT"])
def remove_tracks_from_playlist(playlist):
    delete_playlist_tracks = request.json
    
    playlist_tracks = ''
    try: 
        playlist_tracks = delete_playlist_tracks['delete_playlist_tracks']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_playlist_tracks_to_remove']
        return msg, code
    finally:
        if not isinstance(playlist_tracks, list) or len(playlist_tracks) == 0:
            code = http_responses['BadRequest']['code']
            msg = http_responses['BadRequest']['no_playlist_tracks_to_remove']
            return msg, code 
            
    res = remove_tracks_from_playlist_ts(playlist, playlist_tracks)
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tracks_array_parameter']
        return msg, code
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    elif res == -4:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#delete playlist   
@library_blueprint.route("/playlist/delete/<int:playlist>", methods=["DELETE"])
def delete_playlist(playlist):
    res = delete_playlist_ts(playlist)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    elif res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    elif res == -4:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        code = http_responses['OK']['code']
        msg = http_responses['OK']['playlist_deleted']
        return msg, code