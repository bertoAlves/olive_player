import sys,os

from db_connect import new_session

sys.path.append('../domain')
from tagClass import tag_class

sys.path.append('../factories')
from tagfactory import tagtodict

sys.path.append('../../utils')
from dictionary_library import folder_path

#returns the new tag created
#returns -1 in case error while trying to connect to database
#returns -2 in case unique title constraint is broken
#returns -3 in case impossible to insert tag
def new_tag_transac(title, color, sec_color, image):
    try:
        session = new_session()
    except:
        return -1
    
    new_tag = ''
    
    if image:
        new_tag = tag_class(title, color, sec_color, True)
    else:
        new_tag = tag_class(title, color, sec_color)

    try:
        session.add(new_tag)
        session.commit()
    except Exception as ex:
        if ex.__class__.__name__ == 'IntegrityError':
            if 'UNIQUE constraint failed: _tags.title' in str(ex):
                return -2
            else:
                return -3
        else:
            return -3
    
    if image:
        try:
            if not os.path.exists(folder_path['tag_img_folder']+str(new_tag.id)+'.png'):
                image.save(folder_path['tag_img_folder']+str(new_tag.id)+'.png')
            else:
                session.delete(new_tag)   
                try:
                    session.commit()
                except Exception as ex:
                    return -4
                return -2
        except:
            session.delete(new_tag)   
            try:
                session.commit()
            except Exception as ex:
                return -4
            return -3

    return tagtodict(new_tag)


#returns the changed tag
#returns -1 in case error while trying to connect to database
#returns -2 in case unique title constraint is broken
#returns -3 in case impossible to change tag
def update_tag_transac(id, title_, color, sec_color, image):
    try:
        session = new_session()
    except:
        return -1
        
    try:
        tag = session.query(tag_class).get(id)
        if not tag:
            return -2
    except:
        return -3
         
    if title_:
        tag.title = title_
    if color:
        tag.color = color
    if image:
        try:
            image.save(folder_path['tag_img_folder']+str(id)+'.png')
            tag.has_image = True
        except:
            return -3
    
    try:
        session.commit()
    except Exception as ex:
        if ex.__class__.__name__ == 'IntegrityError':
            if 'UNIQUE constraint failed: _tags.title' in str(ex):
                return -2
            else:
                return -3
        else:
            return -3
            
    return tagtodict(tag)
    


#returns the changed tag
#returns -1 in case error while trying to connect to database
#returns -2 in case impossible to delete image
def delete_tag_img_transac(id):
    try:
        session = new_session()
    except:
        return -1
        
    try:
        tag = session.query(tag_class).get(id)
        if not tag:
            return -2
    except:
        return -3
         
    if tag.has_image:
        try:
            os.remove(folder_path['tag_img_folder']+str(id)+'.png')
            tag.has_image = False
        except:
            return -4
    else:
        return -4
    
    try:
        session.commit()
    except Exception as ex:
        if ex.__class__.__name__ == 'IntegrityError':
            if 'UNIQUE constraint failed: _tags.title' in str(ex):
                return -2
            else:
                return -3
        else:
            return -3
            
    return tagtodict(tag)


    
#returns 1 if tag deleted
#returns -1 in case error while trying to connect to database
#returns -2 in case tag does not exist
#returns -3 in case strange behaviour is encontered in database
#returns -4 in case impossible to save changes
def delete_tag_transac(id):
    try:
        session = new_session()
    except:
        return -1
        
    try:
        tag = session.query(tag_class).get(id)
        if not tag:
            return -2
    except:
        return -3
    
    if tag.has_image:
        try:
            os.remove(folder_path['tag_img_folder']+str(id)+'.png')
        except:
            pass
        
    session.delete(tag)   
    try:
        session.commit()
    except Exception as ex:
        return -4
        
    return 1