import os, sys

sys.path.append('../persistance')
from linktransactions import *
from linkqueries import *

sys.path.append('../../utils')
from conversions import convertStringToInteger, convertStringToArray, convertArrayOfStringToArrayOfIntegers
from validations import validateDateString

def new_link_ts(name, description, url, tags):
    return new_link_transac(name, description, url, tags)

    
def update_link_ts(id, name_, description, url):
    return update_link_transac(id, name_, description, url)
 
 
def add_tag_to_link_ts(id, tagid, single):
    if single:
        try:
            return add_tag_to_link_transac(id, int(tagid))
        except:
            return 0
    else:
        try:
            tagid = convertStringToArray(tagid)
            if not tagid:
                return 0
            tagid = convertArrayOfStringToArrayOfIntegers(tagid)
            if not tagid:
                return 0
        except:
            return 0
        return add_tags_to_link_transac(id, tagid)
        

def remove_tag_from_link_ts(id, tagid, single):
    if single:     
        return remove_tag_from_link_transac(id, tagid)
    else:
        try:
            tagid = convertStringToArray(tagid)
            if not tagid:
                return 0
            tagid = convertArrayOfStringToArrayOfIntegers(tagid)
            if not tagid:
                return 0
        except:
            return 0
        return remove_tags_from_link_transac(id, tagid)
        
        
def links_by_tags_info(tags_arg, single=False):
    if not single:
        try:
            tag_ids = convertStringToArray(tags_arg)
            if not tag_ids:
                return 0
            tag_ids = convertArrayOfStringToArrayOfIntegers(tag_ids)
            if not tag_ids:
                return 0
        except:
            return 0
    else:
        tag_ids = []
        tag_ids.append(tags_arg)       
    return links_by_tags_query(tag_ids)
    
    
def links_by_date_info(start_date_arg, end_date_arg):
    start_date = None
    end_date = None
    
    if start_date_arg:
        start_date = validateDateString(start_date_arg)
        if not start_date:
            return 0
    
    if end_date_arg:
        end_date = validateDateString(end_date_arg)
        if not end_date:
            return 0
                
    return links_by_date_query(start_date, end_date)
    
    
def links_search_info(search):
    array = convertStringToArray(search, separator=' ')
    if not array:      
        return links_search_query([search])
    else:
        return links_search_query(array)
    
    
def delete_link_ts(id):
    return delete_link_transac(id)