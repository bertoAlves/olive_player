import pickle
import sys

#queue
#list - queued tracks
class queue_class:
        def __init__(mysillyobject):
            mysillyobject.list = []
        
        def save(mysillyobject):    
            pickle.dump(mysillyobject, open("../queue", "wb"))
        
        
        #get next queued
        def next(mysillyobject):
            if len(mysillyobject.list) > 0:
                return mysillyobject.list.pop(0)
        
        
        #next track by id
        def next_by_id(mysillyobject, track):
            if len(mysillyobject.list) > 0:
                for queued in mysillyobject.list:
                    if queued['id'] == str(track):
                        mysillyobject.list.remove(queued)
                        return queued 
            return -1
        
        
        #find by id
        def find_by_id(mysillyobject, track):
            for queued in mysillyobject.list:
                if queued['id'] == str(track):
                    return True
            return False
        
        
        #add to queue
        def add_to_queue(mysillyobject, track):
            mysillyobject.list.append(track)


        #remove from queue		
        def remove_from_queue(mysillyobject, track):
            if len(mysillyobject.list) > 0:
                for queued in mysillyobject.list:
                    if queued['id'] == str(track):
                        mysillyobject.list.remove(queued)
                        return 1           
            return -1
            
        def clear(mysillyobject):
            mysillyobject.list.clear()