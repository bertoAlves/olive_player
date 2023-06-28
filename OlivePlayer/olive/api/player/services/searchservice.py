import os, sys

sys.path.append('../persistance')
from searchqueries import *

sys.path.append('../../utils')
from validations import validateSearchParameter_STRING_SINGLES, validateSearchParameter_STRING_STRING, validateSearchParameter_STRING_YEAR, validateSearchParameter_YEAR
from conversions import convertStringToArray

def search_info(search, artists_arg, albums_arg, tracks_arg, playlists_arg):
    array = convertStringToArray(search, separator=' ')

    check_all = False
    if all(arg == False for arg in [artists_arg, albums_arg, tracks_arg, playlists_arg]):
        check_all = True
    
    if not array:
        if not check_all:
            return search_query([search], artists_arg, albums_arg, tracks_arg, playlists_arg)
        else:
            return search_query([search])
    else:
        if not check_all:
            return search_query(array, artists_arg, albums_arg, tracks_arg, playlists_arg)
        else:
            return search_query(array)
        