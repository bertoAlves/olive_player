import random


#shuffles list randomly
def shuffle_algorithm(list_of_tracks):
    list_of_tracks_ = list_of_tracks.copy()
    shuffled_tracks = []
    
    while len(list_of_tracks_) != 0:
        trck = list_of_tracks_.pop(random.randint(0,len(list_of_tracks_)-1))
        shuffled_tracks.append(trck)
        
    return shuffled_tracks