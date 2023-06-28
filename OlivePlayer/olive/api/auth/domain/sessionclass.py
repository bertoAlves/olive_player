import pickle, datetime, random
import sys, os

sys.path.append('../../utils')
from dictionary_library import keys_and_passw

#session
#date - start date of the session
#key - session key
#number - control number
class session_class:
        def __init__(mysillyobject):
            mysillyobject.date = datetime.datetime.now()
            mysillyobject.string_date = str(datetime.datetime.now())
            mysillyobject.key = generate_key()
            mysillyobject.number = "1"
        
        def save(mysillyobject):    
            pickle.dump(mysillyobject, open(keys_and_passw['s_file'], "wb"))
            
        def logout(mysillyobject):
            try:
                os.remove(keys_and_passw['s_file'])
                return True
            except:
                return False
            
            
#load session
def load_session():
    try:
        return pickle.load(open(keys_and_passw['s_file'], "rb"))
    except:
        return None


#generate key        
def generate_key(size = 24):
    chars = "ABCDEFGHIJKLMNOPQRSTVWUXYZ0123456789_!*,.><"
    generated_key = ""
    for i in range(size):
        generated_key += chars[random.randint(0,len(chars)-1)]
    return generated_key