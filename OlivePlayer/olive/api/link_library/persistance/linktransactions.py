import sys
from db_connect import new_session

sys.path.append('../domain')
from linkClass import link_class
from tagClass import tag_class

sys.path.append('../factories')
from linkfactory import linktodict


#returns the new link created
#returns -1 in case error while trying to connect to database
#returns -2 in case tag does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case unique url constraint is broken
#returns -5 in case unique name constraint is broken
#returns -6 in case impossible to insert link
def new_link_transac(name, description, url, tags):
    try:
        session = new_session()
    except:
        return -1
        
    new_link = link_class(name, description, url)
    
    for tag in tags:
        try:
            tag_object = session.query(tag_class).filter_by(title=tag).scalar()
            if tag_object:
                new_link.tags.append(tag_object)
            else:
                return -2
        except:
            return -3
    
    try:
        session.add(new_link)
        session.commit()
    except Exception as ex:
        if ex.__class__.__name__ == 'IntegrityError':
            if 'UNIQUE constraint failed: _links.url' in str(ex):
                return -4
            if 'UNIQUE constraint failed: _links.name' in str(ex):
                return -5
            else:
                return -6
        else:
            return -6
            
    return linktodict(new_link)



#returns the changed link
#returns -1 in case error while trying to connect to database
#returns -2 in case link to update does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case unique url constraint is broken
#returns -5 in case unique name constraint is broken
#returns -6 in case impossible to change link  
def update_link_transac(id, name_, description, url):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        link = session.query(link_class).get(id).scalar()
        if not link:
            return -2
    except:
        return -3
    
    if name_:
        link.name = name_
    if description:
        link.description = description
    if url:
        link.url = url
    
    try:
        link.change()
        session.commit()
    except Exception as ex:
        if ex.__class__.__name__ == 'IntegrityError':
            if 'UNIQUE constraint failed: _links.url' in str(ex):
                return -4
            if 'UNIQUE constraint failed: _links.name' in str(ex):
                return -5
            else:
                return -6
        else:
            return -6
            
    return linktodict(link)
    


#returns the changed link
#returns -1 in case error while trying to connect to database
#returns -2 in case link or tag does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case tag already exists in link
#returns -5 in case impossible to change link     
def add_tag_to_link_transac(id, tagid):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        link = session.query(link_class).get(id)
        if not link:
            return -2
    except:
        return -3
    
    try:
        tag = session.query(tag_class).get(tagid)
        if not tag:
            return -2
    except:
        return -3
        
    if tag in link.tags:
        return -4
    
    link.tags.append(tag)  
    try:
        link.change()
        session.commit()
    except Exception as ex:
        return -5
            
    return linktodict(link)    
    


#returns the changed link
#returns -1 in case error while trying to connect to database
#returns -2 in case link or tag does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case tag already exists in link
#returns -5 in case impossible to change link    
def add_tags_to_link_transac(id, tagids):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        link = session.query(link_class).get(id)
        if not link:
            return -2
    except:
        return -3
    
    tags_to_add = []   
    for tagid in tagids:
        try:
            tag = session.query(tag_class).get(tagid)
            if not tag:
                return -2
            else:
                tags_to_add.append(tag)
        except:
            return -3
    
    for tag in tags_to_add:
        if tag in link.tags:
            return -4
        else:
            link.tags.append(tag)

    try:
        link.change()
        session.commit()
    except Exception as ex:
        return -5
            
    return linktodict(link)
    
    
    
#returns the changed link
#returns -1 in case error while trying to connect to database
#returns -2 in case link or tag does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case link has no tags
#returns -5 in case tag does not exist in link
#returns -6 in case impossible to change link
def remove_tag_from_link_transac(id, tagid):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        link = session.query(link_class).get(id)
        if not link:
            return -2
    except:
        return -3
    
    if len(link.tags) == 0:
        return -4
    
    removed = False
    for tag in link.tags:
        if str(tag.id) == tagid:
            link.tags.remove(tag)
            removed = True
    
    if not removed:
        return -5
    
    try:
        link.change()
        session.commit()
    except Exception as ex:
        return -6
            
    return linktodict(link)



#returns the changed link
#returns -1 in case error while trying to connect to database
#returns -2 in case link or tag does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case link has no tags
#returns -5 in case tag does not exist in link
#returns -6 in case impossible to change link
def remove_tags_from_link_transac(id, tagids):
    try:
        session = new_session()
    except:
        return -1
    
    try:
        link = session.query(link_class).get(id)
        if not link:
            return -2
    except:
        return -3
    
    if len(link.tags) == 0:
        return -4
    
    for tagid in tagids:
        removed = False
        for tag in link.tags:
            if tag.id == tagid:
                link.tags.remove(tag)
                removed = True
        if not removed:
            return -5
    
    try:
        link.change()
        session.commit()
    except Exception as ex:
        return -6
            
    return linktodict(link)



#returns 1 if link deleted
#returns -1 in case error while trying to connect to database
#returns -2 in case link does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case impossible to save changes
def delete_link_transac(id):
    try:
        session = new_session()
    except:
        return -1
        
    try:
        link = session.query(link_class).get(id)
        if not link:
            return -2
    except:
        return -3
        
    session.delete(link)   
    try:
        session.commit()
    except Exception as ex:
        return -4
        
    return link.name