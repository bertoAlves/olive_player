import sys
from db_connect import new_session
from sqlalchemy import or_

sys.path.append('../domain')
from tagClass import tag_class

sys.path.append('../factories')
from tagfactory import tagtodict


#returns all tags
#returns -1 in case error while trying to connect to database
#returns -2 in case link does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case no tags found  
def get_tags_query():
    try:
        session = new_session()
    except:
        return -1
        
    try:
        tags = session.query(tag_class).all()
        if not tags:
            return -2
    except:
        return -3
        
    tags_to_json = []
    for tag in tags:
        tags_to_json.append(tagtodict(tag))
    
    if len(tags_to_json) == 0:
        return -4
    
    return tags_to_json
    
    
#returns tags matching the criteria
#returns -1 in case error while trying to connect to database
#returns -2 in case link does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case no tags found  
def tags_search_query(search):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        tags = session.query(tag_class).filter(or_(*[tag_class.title.like('%'+it+'%') for it in search]))
        if not tags:
            return -2
    except:
        return -3
        
    tags_to_json = []
    for tag in tags:
        tags_to_json.append(tagtodict(tag))
    
    if len(tags_to_json) == 0:
        return -4
    
    return tags_to_json