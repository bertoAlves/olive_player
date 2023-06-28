import os, sys

sys.path.append('../persistance')
from listtransactions import *
from listqueries import *

sys.path.append('../../utils')
from conversions import convertStringToInteger, convertStringToArray, convertArrayOfStringToArrayOfIntegers
from validations import validateDateString


def new_list_ts(title, description):
    return new_list_transac(title, description)
    

def update_list_ts(id, title_, description):
    return update_list_transac(id, title_, description)
    
    
def add_link_to_list_ts(id, linkid, single):
    if single:     
        return add_link_to_list_transac(id, linkid)
    else:
        try:
            linkid = convertStringToArray(linkid)
            if not linkid:
                return 0
            linkid = convertArrayOfStringToArrayOfIntegers(linkid)
            if not linkid:
                return 0
        except:
            return 0
        return add_links_to_list_transac(id, linkid)        
    
    
def remove_link_from_list_ts(id, linkid, single):
    if single:     
        return remove_link_from_list_transac(id, linkid)
    else:
        try:
            linkid = convertStringToArray(linkid)
            if not linkid:
                return 0
            linkid = convertArrayOfStringToArrayOfIntegers(linkid)
            if not linkid:
                return 0
        except:
            return 0   
        return remove_links_from_list_transac(id, linkid)
        

def delete_list_ts(id):
    return delete_list_transac(id)
    

def get_lists_info():
    return get_lists_query()
    

def lists_search_info(search):
    array = convertStringToArray(search, separator=' ')
    if not array:      
        return lists_search_query([search])
    else:
        return lists_search_query(array)