import sys
from db_connect import new_session

sys.path.append('../domain')
from listClass import list_class
from linkClass import link_class

sys.path.append('../factories')
from listfactory import listtodict


#returns the new created list
#returns -1 in case error while trying to connect to database
#returns -2 in case unique title constraint is broken
#returns -3 in case impossible to insert link
def new_list_transac(title, description):
    try:
        session = new_session()
    except:
        return -1
        
    new_list = list_class(title, description)
    
    try:
        session.add(new_list)
        session.commit()
    except Exception as ex:
        if ex.__class__.__name__ == 'IntegrityError':
            if 'UNIQUE constraint failed: _lists.title' in str(ex):
                return -2
            else:
                return -3
        else:
            return -3
            
    return listtodict(new_list)


#returns the changed list
#returns -1 in case error while trying to connect to database
#returns -2 in case list to update does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case unique title constraint is broken
#returns -5 in case impossible to change list  
def update_list_transac(id, title_, description):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        list = session.query(list_class).get(id)
        if not list:
            return -2
    except:
        return -3
    
    if title_:
        list.title = title_
    if description:
        list.description = description
    
    try:
        session.commit()
    except Exception as ex:
        if ex.__class__.__name__ == 'IntegrityError':
            if 'UNIQUE constraint failed: _links.title' in str(ex):
                return -4
            else:
                return -5
        else:
            return -5
            
    return listtodict(list)


#returns the changed list
#returns -1 in case error while trying to connect to database
#returns -2 in case list or link does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case link already exists in list
#returns -5 in case impossible to change list   
def add_link_to_list_transac(id, linkid):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        list = session.query(list_class).get(id)
        if not list:
            return -2
    except:
        return -3
    
    try:
        link = session.query(link_class).get(linkid)
        if not link:
            return -2
    except:
        return -3
    
    if link in list.links:
        return -4
    
    list.links.append(link)  
    try:
        session.commit()
    except Exception as ex:
        return -5
            
    return listtodict(list)
    

#returns the changed list
#returns -1 in case error while trying to connect to database
#returns -2 in case list or link does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case link already exists in list
#returns -5 in case impossible to change list   
def add_links_to_list_transac(id, linkids):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        list = session.query(list_class).get(id)
        if not list:
            return -2
    except:
        return -3
    
    links_to_add = []   
    for linkid in linkids:
        try:
            link = session.query(link_class).get(linkid)
            if not link:
                return -2
            else:
                links_to_add.append(link)
        except:
            return -3
    
    for link in links_to_add:
        if link in list.links:
            return -4
        else:
            list.links.append(link)

    try:
        session.commit()
    except Exception as ex:
        return -5
            
    return listtodict(list)
    

#returns the changed list
#returns -1 in case error while trying to connect to database
#returns -2 in case list does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case list has no links
#returns -5 in case link does not exist in list
#returns -6 in case impossible to change list
def remove_link_from_list_transac(id, linkid):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        list = session.query(list_class).get(id)
        if not list:
            return -2
    except:
        return -3
    
    if len(list.links) == 0:
        return -4
    
    removed = False
    for link in list.links:
        if str(link.id) == linkid:
            list.links.remove(link)
            removed = True
            break
    
    if not removed:
        return -5
    
    try:
        session.commit()
    except Exception as ex:
        return -6
            
    return listtodict(list)


#returns the changed list
#returns -1 in case error while trying to connect to database
#returns -2 in case list does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case list has no links
#returns -5 in case link does not exist in list
#returns -6 in case impossible to change list
def remove_links_from_list_transac(id, linkids):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        list = session.query(list_class).get(id)
        if not list:
            return -2
    except:
        return -3
    
    if len(list.links) == 0:
        return -4
    
    for linkid in linkids:
        removed = False
        for link in list.links:
            if link.id == linkid:
                list.links.remove(link)
                removed = True
        if not removed:
            return -5
    
    if not removed:
        return -5
    
    try:
        session.commit()
    except Exception as ex:
        return -6
            
    return listtodict(list)
    

#returns 1 if list deleted
#returns -1 in case error while trying to connect to database
#returns -2 in case list does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case impossible to save changes
def delete_list_transac(id):
    try:
        session = new_session()
    except:
        return -1
        
    try:
        list = session.query(list_class).get(id)
        if not list:
            return -2
    except:
        return -3
        
    session.delete(list)    
    try:
        session.commit()
    except Exception as ex:
        return -4
        
    return 1