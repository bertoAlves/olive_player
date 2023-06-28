import os, sys

sys.path.append('../persistance')
from artistqueries import *

sys.path.append('../../utils')
from conversions import convertStringToInteger, convertStringToArray, convertArrayOfStringToArrayOfIntegers


def all_artists_info():
    return all_artists_query()

def albums_of_artist_info(artist):
    return albums_of_artist_query(artist)

def albums_of_artists_info(artists):
    artists_array = convertStringToArray(artists)
    if not artists_array:
        return 0
        
    artists_array_ints = convertArrayOfStringToArrayOfIntegers(artists_array)
    if not artists_array_ints:
        return 0
        
    return albums_of_artists_query(artists_array_ints)

def tracks_of_artist_info(artist):
    return tracks_of_artist_query(artist)

def tracks_of_artists_info(artists):
    artists_array = convertStringToArray(artists)
    if not artists_array:
        return 0
        
    artists_array_ints = convertArrayOfStringToArrayOfIntegers(artists_array)
    if not artists_array_ints:
        return 0
        
    return tracks_of_artists_query(artists_array_ints)
    
def singles_of_artist_info(artist):
    return singles_of_artist_query(artist)
