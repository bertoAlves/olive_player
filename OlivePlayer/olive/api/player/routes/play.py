import os, sys, json

from flask import Flask, Blueprint, request, Response

sys.path.append('../services')
from playsessionservice import *

sys.path.append('../../utils')
from dictionary_library import http_responses

play_blueprint = Blueprint('play_blueprint', __name__)


#create new playsession
@play_blueprint.route("/playsession/new", methods=['POST'])
def new_session():
    
    shuffle = False
    shuffle_arg = request.args.get('shuffle')
        
    if shuffle_arg == 'True':
        shuffle = True
    else:
        shuffle = False
              
    play_session = request.json
    
    start_session_ALBUMS = ''
    start_session_PLAYLISTS = ''
    start_session_TRACKS = ''
    try: 
        start_session_ALBUMS = play_session['start_session_ALBUMS']
    except:
        try:
            start_session_PLAYLISTS = play_session['start_session_PLAYLISTS']
        except:
            try:
                start_session_TRACKS = play_session['start_session_TRACKS']
            except:
                code = http_responses['BadRequest']['code']
                msg = http_responses['BadRequest']['no_play_session_given']
                return msg, code
      
    res = ''
    if start_session_ALBUMS and isinstance(start_session_ALBUMS,list) and not start_session_PLAYLISTS and not start_session_TRACKS:
        res = new_session_(start_session_ALBUMS, shuffle, type='ALBUMS')
    elif start_session_PLAYLISTS and isinstance(start_session_PLAYLISTS,list) and not start_session_ALBUMS and not start_session_TRACKS:
        res = new_session_(start_session_PLAYLISTS, shuffle, type='PLAYLISTS')
    elif start_session_TRACKS and isinstance(start_session_TRACKS,list) and not start_session_ALBUMS and not start_session_PLAYLISTS:
        res = new_session_(start_session_TRACKS, shuffle, type='TRACKS')
    else:
        code = http_responses['NotAcceptable']['code']
        msg = http_responses['NotAcceptable']['incomprehensible_request_for_play_session']
        return msg, code

    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_play_session_given']
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
        return Response(generate(res), mimetype="audio/x-wav")

#generate audio
def generate(res):
    with open(res, "rb") as fwav:
        data = fwav.read(1024)
        while data:
            yield data
            data = fwav.read(1024)

#next track
@play_blueprint.route("/playsession/next", methods=['GET'])
def next_track():
    
    shuffle_arg = request.args.get('shuffle')
    lasttrack = request.args.get('lasttrack')
        
    if shuffle_arg == 'True':
        shuffle = True
    else:
        shuffle = False
    
    try:
        lasttrack = int(lasttrack)
    except:
        lasttrack = None
        
    res = ''
    if lasttrack:        
        res = next_(shuffle, lasttrack = lasttrack)
    else:
        res = next_(shuffle)
    
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
        return Response(generate(res), mimetype="audio/x-wav")
    
    
#prev track
@play_blueprint.route("/playsession/prev", methods=['GET'])
def prev_track():
    res = prev_()
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    else:
        return Response(generate(res), mimetype="audio/x-wav")


#jump to track on playsession
@play_blueprint.route("/playsession/jumpto/<int:track>", methods=['GET'])
def playsession_next_by_id(track):
    res = playsession_next_by_id_(track)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    else:
        return Response(generate(res), mimetype="audio/x-wav")
 
    
#add to queue track
@play_blueprint.route("/queue/add", methods=['PUT'])
def add_to_queue():
    
    add_to_queue = request.json
    
    try:
        add__queue = add_to_queue['add__queue']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_queue_tracks_given']
        return msg, code
        
    if not isinstance(add__queue, list):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_queue_tracks_given']
        return msg, code
    
    res = add_to_queue_(add__queue)
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
        code = http_responses['OK']['code']
        msg = http_responses['OK']['tracks_added_to_queue']
        return msg, code


#remove from queue track
@play_blueprint.route("/queue/remove", methods=['PUT'])
def remove_from_queue():
    
    remove_from_queue = request.json
    
    try:
        remove__queue = remove_from_queue['remove__queue']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_queue_tracks_to_remove_given']
        return msg, code
        
    if not isinstance(remove__queue, list):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_queue_tracks_to_remove_given']
        return msg, code
    
    res = remove_from_queue_(remove__queue)
    if res == -1:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    else:
        code = http_responses['OK']['code']
        msg = http_responses['OK']['tracks_removed_from_queue']
        return msg, code
        

#clean queue
@play_blueprint.route("/queue/clear", methods=['PUT'])
def clean_queue():
    res = clean_queue_()
    if res == -1:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        code = http_responses['OK']['code']
        msg = http_responses['OK']['queue_cleared']
        return msg, code

        
#jump to track on queue
@play_blueprint.route("/queue/jumpto/<int:track>", methods=['GET'])
def queue_next_by_id(track):
    res = queue_next_by_id_(track)
    if res == -1:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    elif res == -2:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    else:
        return Response(generate(res), mimetype="audio/x-wav")
    
    
#jump to track on queue
@play_blueprint.route("/nextinline", methods=['GET'])
def see_next():
    res = get_next_in_line_()
    if res == -1:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    headers=http_responses['headers']
    return json.dumps(res), headers    
 
