import sys
from db_connect import new_session
from sqlalchemy import and_, or_

sys.path.append('../domain')
from linkClass import link_class
from tagClass import tag_class

sys.path.append('../factories')
from linkfactory import linktodict


#returns links by tags
#returns -1 in case error while trying to connect to database
#returns -2 in case link does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case no links found
def links_by_tags_query(tag_ids):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        links = session.query(link_class).filter(link_class.tags.any(tag_class.id.in_(tag_ids)))
        if not links:
            return -2
    except:
        return -3
        
    links_to_json = []
    for link in links:
        links_to_json.append(linktodict(link))
    
    if len(links_to_json) == 0:
        return -4
    
    return links_to_json
    


#returns links by date
#returns -1 in case error while trying to connect to database
#returns -2 in case links does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case no links found  
def links_by_date_query(start_date, end_date):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        links = None
        if start_date and not end_date:
            links = session.query(link_class).filter(link_class.last_changed >= start_date)
        if end_date and not start_date:
            links = session.query(link_class).filter(link_class.last_changed <= end_date)
        if start_date and end_date:
            links = session.query(link_class).filter(and_(link_class.last_changed <= end_date, link_class.last_changed >= start_date))
        if not links:
            return -2
    except:
        return -3

    links_to_json = []
    for link in links:
        links_to_json.append(linktodict(link))
    
    if len(links_to_json) == 0:
        return -4
    
    return links_to_json
    


#returns links by the search
#returns -1 in case error while trying to connect to database
#returns -2 in case link does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case no links found      
def links_search_query(search):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        links = session.query(link_class).filter(or_(*[link_class.name.like('%'+it+'%') for it in search], *[link_class.description.like('%'+it+'%') for it in search], *[link_class.url.like('%'+it+'%') for it in search], *[link_class.last_changed.like('%'+it+'%') for it in search]))
        if not links:
            return -2
    except:
        return -3
    
    links_to_json = []
    for link in links:
        links_to_json.append(linktodict(link))
    
    if len(links_to_json) == 0:
        return -4
    
    return links_to_json