import os, sys

sys.path.append('../persistance')
from playlistqueries import *
from playlisttransactions import *

sys.path.append('../../utils')
from conversions import convertStringToInteger, convertStringToArray, convertArrayOfStringToArrayOfIntegers


def all_playlists_info():
    return all_playlists_query()

def tracks_of_playlist_info(playlist):
    return tracks_of_playlist_query(playlist)

def tracks_of_playlists_info(playlists):
    playlists_array = ''
    if not isinstance(playlists, list):
        playlists_array = convertStringToArray(playlists)
        if not playlists_array:
            return 0
    else:
        playlists_array = playlists
    
    playlists_array_ints = convertArrayOfStringToArrayOfIntegers(playlists_array)
    if not playlists_array_ints:
        return 0
        
    return tracks_of_playlists_query(playlists_array_ints)
    
def change_playlist_name_ts(playlist, current_playlist_name, new_playlist_name):
    return change_playlist_name_transac(playlist, current_playlist_name, new_playlist_name)
    
def add_track_to_playlist_ts(playlist, track):
    return add_track_to_playlist_transac(playlist, track)

def add_tracks_to_playlist_ts(playlist, tracks):   
    tracks_array_ints = convertArrayOfStringToArrayOfIntegers(tracks)
    if not tracks_array_ints:
        return 0
        
    return add_tracks_to_playlist_transac(playlist, tracks_array_ints)
    
def remove_track_from_playlist_ts(playlist, track):
    return remove_track_from_playlist_transac(playlist, track)

def remove_tracks_from_playlist_ts(playlist, tracks):   
    tracks_array_ints = convertArrayOfStringToArrayOfIntegers(tracks)
    if not tracks_array_ints:
        return 0
        
    return remove_tracks_from_playlist_transac(playlist, tracks_array_ints)
    
def create_playlist_ts(name, tracks=''):
    tracks_array_ints = ''
    if tracks:
        tracks_array_ints = convertArrayOfStringToArrayOfIntegers(tracks)
        if not tracks_array_ints:
            return 0
        return create_playlist_transac(name, tracks_array_ints)
    else:
        return create_playlist_transac(name)

def delete_playlist_ts(playlist):
    return delete_playlist_transac(playlist)