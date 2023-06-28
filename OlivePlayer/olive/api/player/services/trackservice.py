import os, sys

sys.path.append('../persistance')
from trackqueries import *
from tracktransactions import *

sys.path.append('../../utils')
from conversions import convertStringToInteger, convertStringToArray, convertArrayOfStringToArrayOfIntegers


def all_tracks_info():
    return all_tracks_query()
       
def track_by_id_info(track):
    return track_by_id(track)
    
def tracks_by_listids_info(tracks):
    tracks_array = ''
    if not isinstance(tracks, list):
        tracks_array = convertStringToArray(tracks)
        if not tracks_array:
            return 0
    else:
        tracks_array = tracks
        
    tracks_array_ints = convertArrayOfStringToArrayOfIntegers(tracks_array)
    if not tracks_array_ints:
        return 0
    
    return tracks_by_listids(tracks_array_ints)
   
def used_transac_ts(track):
    return used_transac(track)