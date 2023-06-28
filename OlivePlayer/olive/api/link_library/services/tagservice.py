import os, sys

sys.path.append('../persistance')
from tagtransactions import *
from tagqueries import *

sys.path.append('../../utils')
from conversions import convertStringToInteger, convertStringToArray, convertArrayOfStringToArrayOfIntegers
from validations import validateDateString
from dictionary_library import folder_path

def new_tag_ts(title, color, sec_color, image):
    return new_tag_transac(title, color, sec_color, image)
    
def update_tag_ts(id, title_, color, sec_color, image):
    return update_tag_transac(id, title_, color, sec_color, image)
    
def get_tags_info():
    return get_tags_query()
    
def tags_search_info(search):
    array = convertStringToArray(search, separator=' ')
    if not array:      
        return tags_search_query([search])
    else:
        return tags_search_query(array)
    
def delete_tag_ts(id):
    return delete_tag_transac(id)
    
def get_tag_image_img(id):
    try:
        image_path = folder_path['tag_img_folder']+str(id)+'.png'
        if not os.path.exists(image_path):
            return -1
        return image_path
    except:
        return -1
        
def delete_tag_img_ts(id):
    return delete_tag_img_transac(id)