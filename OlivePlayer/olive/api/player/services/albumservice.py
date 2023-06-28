import os, sys

sys.path.append('../persistance')
from albumqueries import *

sys.path.append('../../utils')
from conversions import convertStringToInteger, convertStringToArray, convertArrayOfStringToArrayOfIntegers


def all_albums_info():
    return all_albums_query()

def tracks_of_album_info(album):
    return tracks_of_album_query(album)

def tracks_of_albums_info(albums):
    
    albums_array = ''
    if not isinstance(albums, list):
        albums_array = convertStringToArray(albums)
        if not albums_array:
            return 0
    else:
        albums_array = albums
        
    albums_array_ints = convertArrayOfStringToArrayOfIntegers(albums_array)
    if not albums_array_ints:
        return 0
        
    return tracks_of_albums_query(albums_array_ints)