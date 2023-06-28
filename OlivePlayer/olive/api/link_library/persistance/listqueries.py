import sys
from db_connect import new_session
from sqlalchemy import and_, or_

sys.path.append('../domain')
from listClass import list_class

sys.path.append('../factories')
from listfactory import listtodict


#returns all lists
#returns -1 in case error while trying to connect to database
#returns -2 in case no lists
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case no lists found  
def get_lists_query():
    try:
        session = new_session()
    except:
        return -1
        
    try:
        lists = session.query(list_class).all()
        if not lists:
            return -2
    except:
        return -3
        
    lists_to_json = []
    for list in lists:
        lists_to_json.append(listtodict(list))
    
    if len(lists_to_json) == 0:
        return -4
    
    return lists_to_json
    

    
#returns lists matching the criteria
#returns -1 in case error while trying to connect to database
#returns -2 in case no lists
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case no lists found
def lists_search_query(search):
    try:
        session = new_session()
    except:
        return -1
        
    try:
        lists = session.query(list_class).filter(or_(*[list_class.title.like('%'+it+'%') for it in search], *[list_class.description.like('%'+it+'%') for it in search]))
        if not lists:
            return -2
    except:
        return -3
        
    lists_to_json = []
    for list in lists:
        lists_to_json.append(listtodict(list))
    
    if len(lists_to_json) == 0:
        return -4
    
    return lists_to_json