import pickle
import sys

sys.path.append('../algorithms')
from shuffle import shuffle_algorithm

#playsession
#current - current playing track
#columnleft - play session left column
#columnright - play session right column
class play_session_class:
    def __init__(mysillyobject, current, columnleft = None, columnright = None, shuffled = False):
        mysillyobject.current = current
        mysillyobject.columnleft = columnleft
        mysillyobject.columnright = columnright
        mysillyobject.shuffled = shuffled
    
    
    #save play session
    def save(mysillyobject):
        pickle.dump(mysillyobject, open("../play_session", "wb"))
    
    
    #get next track by id
    def next_by_id(mysillyobject, track):       
        if mysillyobject.find_by_id(track):       
            while mysillyobject.current['id'] != str(track):
                mysillyobject.next()
            mysillyobject.save()
            return 0
        return -1
    
    
    #find track by id
    def find_by_id(mysillyobject, track):
        if mysillyobject.current['id'] == str(track):
            return True
        if mysillyobject.columnleft:
            for left in mysillyobject.columnleft:
                if left['id'] == str(track):
                    return True          
        if mysillyobject.columnright:
            for right in mysillyobject.columnright:
                if right['id'] == str(track):
                    return True
        return False
    
    
    #next track in playsession
    def next(mysillyobject, shuffle):
        if not shuffle:
            aux = mysillyobject.current  
            if mysillyobject.columnleft and not mysillyobject.columnright:
                mysillyobject.columnleft.append(aux)
            elif mysillyobject.columnleft and mysillyobject.columnright:
                mysillyobject.columnright.append(aux)
                aux = mysillyobject.columnright.pop(0)
                mysillyobject.columnleft.append(aux)
            if mysillyobject.columnleft or mysillyobject.columnright:
                aux = mysillyobject.columnleft.pop(0)
                mysillyobject.current = aux
        else:
            if mysillyobject.columnleft:
                shuffled_column_left = shuffle_algorithm(mysillyobject.columnleft)
                aux = mysillyobject.current
                current = shuffled_column_left.pop(0)
                mysillyobject.current = current
                mysillyobject.columnleft.remove(current)
                if mysillyobject.columnright:
                    mysillyobject.columnright.append(aux)
                else:
                    mysillyobject.columnleft.append(aux)
    
    
    #prev track in playsession
    def prev(mysillyobject):
        aux = mysillyobject.current  
        if mysillyobject.columnleft and not mysillyobject.columnright:
            mysillyobject.columnleft.append(aux)
            aux = mysillyobject.columnleft.pop(0)
            mysillyobject.current = aux
        elif mysillyobject.columnleft and mysillyobject.columnright:
            mysillyobject.columnleft.insert(0, aux)
            aux = mysillyobject.columnleft.pop()
            mysillyobject.columnright.insert(0, aux)
            aux = mysillyobject.columnright.pop()
            mysillyobject.current = aux