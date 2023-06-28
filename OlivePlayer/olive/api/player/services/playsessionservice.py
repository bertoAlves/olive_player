import os, sys

sys.path.append('../services')
from albumservice import *
from playlistservice import *
from trackservice import *

sys.path.append('../algorithms')
from play_algorithms import *

sys.path.append('../../utils')
from conversions import convertStringToInteger, convertStringToArray, convertArrayOfStringToArrayOfIntegers

def new_session_(list_of_ids, shuffle, type=''):        
    tracks_array_ints = convertArrayOfStringToArrayOfIntegers(list_of_ids)
    if not tracks_array_ints and (shuffle != False and shuffle != True):
        return 0
    
    tracks = []
    if type == 'ALBUMS':
        albums_tracks = tracks_of_albums_info(tracks_array_ints)
        if isinstance(albums_tracks, list):
            for album in albums_tracks:
                for track in album['tracks']:
                    tracks.append(track)
        else:
            return albums_tracks
            
    elif type == 'PLAYLISTS':
        playlists_tracks = tracks_of_playlists_info(list_of_ids)
        if isinstance(playlists_tracks, list):
            for playlist in playlists_tracks:
                for track in playlist['tracks']:
                    tracks.append(track)
        else:
            return playlists_tracks
            
    elif type == 'TRACKS':
        tracks = tracks_by_listids_info(list_of_ids)
        if not isinstance(tracks, list):
            return tracks
    else:
        return 0
         
    current = newplay_session(tracks, shuffle)
    
    return track_path_by_id(current['id'])
    

def next_(shuffle, lasttrack = ''):
    if lasttrack:
        ret = used_transac_ts(lasttrack)
        if ret != 1:
            return ret
              
    ret = next__(shuffle)
    if ret == -1:
        return ret
    return track_path_by_id(ret['id'])
    
    
def prev_():
    ret = prev__()
    if ret == -1:
        return ret
    return track_path_by_id(ret['id'])


def add_to_queue_(add__queue):  
    add__queue_ints = convertArrayOfStringToArrayOfIntegers(add__queue)
    if not add__queue_ints:
        return 0
    
    tracks = tracks_by_listids_info(add__queue_ints)
    if not isinstance(tracks, list):
        return tracks

    return add_to_queue__(tracks)

    
def remove_from_queue_(list_ids):
    return remove_from_queue__(list_ids)
    
    
def clean_queue_():
    return clean_queue__()
    
    
def queue_next_by_id_(track):
    ret = queue_next_by_id__(track)
    if ret == -1:
        return ret
    return track_path_by_id(ret['id'])

    
def playsession_next_by_id_(track):
    ret = playsession_next_by_id__(track)
    if ret == -1:
        return ret
    return track_path_by_id(ret['id'])
    

def get_next_in_line():
    return get_next_in_line_()