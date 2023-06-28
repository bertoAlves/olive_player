import os, sys, configparser
from subprocess import Popen

sys.path.append('../domain')
from sessionclass import session_class, load_session

sys.path.append('../../utils')
from conversions import encode
from dictionary_library import keys_and_passw


def login_(password): 
    session = load_session()
    if session:
        return -1
    
    config = configparser.ConfigParser()   
    try:
        config.read(keys_and_passw['k_file'])
        confid_key = config[keys_and_passw['CONFIG_KEY']]
    except:
        return -2
    
    lines = ""
    try:
        keys_file = open(keys_and_passw['p_file'], "r")
        lines = [line.rstrip('\n') for line in keys_file]
    except:
        return -2
        
    if len(lines) != 24:
        return -2
         
    session = session_class()
    if password == encode(confid_key[keys_and_passw['KEY_KEY']],lines[session.date.hour]):
        session.save()
        try:         
            Popen('python ../session_maintenance.py', shell=False)
        except:
            session.logout()
            return -2            
        return session
    else:
        return False
    
    
def validate_session_(cookies): 
    session = load_session()
    if not session:
        return -1
    
    if session.key == cookies.get('key') and session.string_date == cookies.get('date') and session.number < cookies.get('number'):
        session.number = cookies.get('number')
        session.save()
        return True
    else:
        return False
        
        
def logout_(cookies):
    valid_session = validate_session_(cookies)
    
    if valid_session == True:
        session = load_session()
        if session.logout():
            return True
        else:
            return -2
    else:
       return valid_session