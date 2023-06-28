import sys, time, os
import pickle

from shuffle import shuffle_algorithm

sys.path.append('../domain')
from play_sessionClass import play_session_class
from queueClass import queue_class

sys.path.append('../../utils')
from conversions import split_list


#load play session
def load_playsession():
    return pickle.load(open("../play_session", "rb"))
 
 
#load play session
def load_queue():
    return pickle.load(open("../queue", "rb"))


#create new playsession
def newplay_session(list_of_tracks, shuffle):
    if shuffle:
        list_of_tracks = shuffle_algorithm(list_of_tracks)

    if len(list_of_tracks) == 0:
        return None
    
    if len(list_of_tracks) == 1:
        return play_session_class(current = list_of_tracks[0])
        
    if len(list_of_tracks) == 2:
        split_left = []
        split_left.append(list_of_tracks[1])
        return play_session_class(current = list_of_tracks[0], columnleft = split_left)
        
    columnleft, columnright = split_list(list_of_tracks)
    
    p_session = play_session_class(current = columnleft[0], columnleft = columnleft[1:], columnright = columnright, shuffled = shuffle)
    p_session.save()
    
    if not os.path.exists("../queue"): 
        n_queue = queue_class()
        n_queue.save()
    
    return p_session.current


#next track
def next__(shuffle):
    play_session = ''
    queue = ''
    try:
        play_session = load_playsession()
        queue = load_queue()
    except:
        return -1
    
    if len(queue.list) > 0:
        current = queue.next()
        queue.save()
        return current
    else:
        if not play_session.shuffled and shuffle:
            play_session.next(True)
        else:
            play_session.next(False)
            
        play_session.save()
        return play_session.current


#roll back track 
def prev__():
    play_session = ''
    try:
        play_session = load_playsession()
    except:
        return -1
    play_session.prev()
    play_session.save()
    return play_session.current


#next queue track by id 
def queue_next_by_id__(track):
    queue = ''
    try:
        queue = load_queue()
    except:
        return -1
    
    current = queue.next_by_id(track) 
    if current == -1:
        return -1
        
    queue.save()
    return current
    
    
#next track by id 
def playsession_next_by_id__(track):
    play_session = ''
    try:
        play_session = load_playsession()
    except:
        return -1
    
    current = play_session.next_by_id(track) 
    if current == -1:
        return -1
        
    return play_session.current


#add tracks to queue
def add_to_queue__(list_of_tracks):
    queue = ''
    try:
        queue = load_queue()
    except:
        return -1
        
    for track in list_of_tracks:
        queue.add_to_queue(track)
        
    queue.save()
    return 1


#remove tracks from queue
def remove_from_queue__(list_of_tracks):
    queue = ''
    try:
        queue = load_queue()
    except:
        return -1
        
    for track in list_of_tracks:
        if queue.find_by_id(track) == False:
            return -1
    
    for track in list_of_tracks:
        if queue.remove_from_queue(track) == -1:
            return -1
        
    queue.save()
    return 1
    

#remove tracks from queue
def clean_queue__():
    queue = ''
    try:
        queue = load_queue()
    except:
        return -1
        
    queue.clear()
    queue.save()
    return 1
    

#get next in line
def get_next_in_line_():
    queue = ''
    play_session = ''
    try:
        play_session = load_playsession()
        queue = load_queue()
    except:
        return -1
    
    next_in_line = []
    track_from_queue = {}
    
    for track in queue.list:
        track_from_queue = track
        track_from_queue['Queued'] = 'TRUE'
        next_in_line.append(track_from_queue)
    
    if play_session.columnleft:
        for track in play_session.columnleft:
            track_from_queue = track
            track_from_queue['Queued'] = 'FALSE'
            next_in_line.append(track_from_queue)
        
    if play_session.columnright:
        for track in play_session.columnright:
            track_from_queue = track
            track_from_queue['Queued'] = 'FALSE'
            next_in_line.append(track_from_queue)
   
    return next_in_line    
