import os, sys, json

from flask import Flask, request, send_file
from middleware import middleware

sys.path.append('../services')
from linkservice import *
from tagservice import *
from listservice import *

sys.path.append('../../utils')
from dictionary_library import http_responses, caracter_limit, defaults
from validations import *

app = Flask(__name__)

app.wsgi_app = middleware(app.wsgi_app)

#create new link
@app.route("/link/new", methods=['POST'])
def new_link():
    
    link_json = request.json 
    try:
        new_link = link_json['link']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_link']
        return msg, code
    
    if not isinstance(new_link, dict):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_link_given']
        return msg, code
    
    try:
        name = new_link['name']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_link_name']
        return msg, code        
        
    if not isinstance(name, str) or len(name) > caracter_limit['link_name']:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_link_name_given']
        return msg, code
    
    description = ''
    try:
        description = new_link['description']
    except:
        description = defaults['link_description']
        
    if not isinstance(description, str) or len(description) > caracter_limit['link_description']:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_link_description_given']
        return msg, code
        
    try:
        url = new_link['url']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_link_url']
        return msg, code
        
    if not isinstance(url, str) or not validateURLString(url):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_link_url_given']
        return msg, code
        
    try:
        tags = new_link['tags']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_tags']
        return msg, code
        
    if not isinstance(tags, list):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tags_parameter']
        return msg, code
        
    res = new_link_ts(name, description, url, tags)    
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['link_url_must_be_unique']
        return msg, code
    if res == -5:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['link_name_must_be_unique']
        return msg, code
    if res == -6:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
    
    
#update link
@app.route("/link/<int:id>/update", methods=['PUT'])
def change_link(id):
    
    link_json = request.json 
    try:
        new_link = link_json['link']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_link']
        return msg, code
    
    if not isinstance(new_link, dict):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_link_given']
        return msg, code
    
    try:
        name_ = new_link['name']
    except:
        name_ = None
    
    if name_: 
        if not isinstance(name_, str) or len(name_) > caracter_limit['link_name']:
            code = http_responses['BadRequest']['code']
            msg = http_responses['BadRequest']['wrong_link_name_given']
            return msg, code
    
    try:
        description = new_link['description']
    except:
        description = None   
    
    if description:
        if not isinstance(description, str) or len(description) > caracter_limit['link_description']:
            code = http_responses['BadRequest']['code']
            msg = http_responses['BadRequest']['wrong_link_description_given']
            return msg, code
        
    try:
        url = new_link['url']
    except:
        url = None
        
    if url:
        if not isinstance(url, str) or not validateURLString(url):
            code = http_responses['BadRequest']['code']
            msg = http_responses['BadRequest']['wrong_link_url_given']
            return msg, code
        
    if not name_ and not description and not url:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_attributes_for_link']
        return msg, code
    
    res = update_link_ts(id, name_, description, url)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['link_url_must_be_unique']
        return msg, code
    if res == -5:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['link_name_must_be_unique']
        return msg, code
    if res == -6:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers

    
#add tag to link
@app.route("/link/<int:id>/update/add", methods=['PUT'])
def add_tag_to_link(id):
    tagid = request.args.get('tagid')
    tagids = request.args.get('tagids')
    
    if not tagid and not tagids:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_tag']
        return msg, code
        
    if tagid and tagids:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['array_or_string']
        return msg, code
        
    res = ''
    if tagid:
        res = add_tag_to_link_ts(id, tagid, single=True)
    else:
        res = add_tag_to_link_ts(id, tagids, single=False)
    
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_ids_given']
        return msg, code  
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['tag_must_not_be_repited_in_link']
        return msg, code
    if res == -5:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
        
        
#remove tag from link
@app.route("/link/<int:id>/update/remove", methods=['PUT'])
def remove_tag_from_link(id):
    tagid = request.args.get('tagid')
    tagids = request.args.get('tagids')
    
    if not tagid and not tagids:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_tag']
        return msg, code
        
    if tagid and tagids:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['array_or_string']
        return msg, code
        
    res = ''
    if tagid:
        res = remove_tag_from_link_ts(id, tagid, single=True)
    else:
        res = remove_tag_from_link_ts(id, tagids, single=False)
        
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_ids_given']
        return msg, code  
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['link_has_no_tags']
        return msg, code
    if res == -5:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['tag_not_found_in_link']
        return msg, code
    if res == -6:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
    

#get links by a search string
@app.route("/links/search", methods=['GET'])
def search_links():
    search = request.args.get('search')
    
    if not search:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_search_arg']
        return msg, code
            
    res = links_search_info(search)
        
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_ids_given']
        return msg, code  
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['no_links_found']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#get links by tags
@app.route("/links/bytags", methods=['GET'])
def links_by_tags():
    tags_arg = request.args.get('tagids')
    tag_arg = request.args.get('tagid')
    
    if not tags_arg and not tag_arg:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_tags']
        return msg, code
        
    if tags_arg and tag_arg:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['array_or_string']
        return msg, code
            
    res = ''
    if tags_arg: 
        res = links_by_tags_info(tags_arg, single=False)
    else:
        res = links_by_tags_info(tag_arg, single=True)
        
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_ids_given']
        return msg, code  
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['no_links_found']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#get links by date
@app.route("/links/bydate", methods=['GET'])
def links_by_date():
    start_date_arg = ''  
    try:
        start_date_arg = request.args.get('start_date')
    except:
        start_date_arg = None
     
    end_date_arg = ''  
    try:
        end_date_arg = request.args.get('end_date')
    except:
        end_date_arg = None
        
    if not start_date_arg and not end_date_arg:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_time_given']
        return msg, code

    res = links_by_date_info(start_date_arg, end_date_arg) 
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_date_given']
        return msg, code  
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['no_links_found']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#delete link
@app.route("/link/<int:id>/delete", methods=['DELETE'])
def delete_link(id):        
    res = delete_link_ts(id) 
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        code = http_responses['OK']['code']
        msg = http_responses['OK']['link_deleted']
        return res + ' - ' + msg, code


#create new tag
@app.route("/tag/new", methods=['POST'])
def new_tag(): 
    tag_json = request.form['tag']

    if not tag_json:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_tag']
        return msg, code
        
    try:
        tag_json = json.loads(tag_json)  
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_given']
        return msg, code
    
    try:
        title = tag_json['title']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_tag_title']
        return msg, code
        
    if not isinstance(title, str) or len(title) > caracter_limit['tag_title']:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_title_given']
        return msg, code
    
    has_color = False
    try:
        color = tag_json['color']
        has_color = True
    except:
        color = defaults['tag_color']
    
    if has_color:
        try:
            sec_color = tag_json['sec_color']
        except:
            sec_color = defaults['tag_sec_color']
    else:
        sec_color = defaults['tag_sec_color']    
    
    if not isinstance(color, str) or not validateColorString(color) or not isinstance(sec_color, str) or not validateColorString(sec_color):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_color_given']
        return msg, code
    
    try:
        image = request.files.get('tag_img')
    except:
        image = None
        
    res = new_tag_ts(title, color, sec_color, image)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['tag_title_must_be_unique']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#update tag
@app.route("/tag/<int:id>/update", methods=['PUT'])
def update_tag(id):    
    tag_json = request.form['tag']
    try:
        image = request.files.get('tag_img')
    except:
        image = None
        
    if not tag_json and not image:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_attributes_for_tag']
        return msg, code
        
    try:
        tag_json = json.loads(tag_json)  
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_given']
        return msg, code
    
    try:
        title_ = tag_json['title']
    except:
        title_ = None
    
    if title_ and (not isinstance(title_, str) or len(title_) > caracter_limit['tag_title']):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_title_given']
        return msg, code

    try:
        color = tag_json['color']
    except:
        color = None
    
    try:
        sec_color = tag_json['sec_color']
    except:
        sec_color = None
    
    if color and (not isinstance(color, str) or not validateColorString(color)):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_color_given']
        return msg, code
        
    if sec_color and (not isinstance(sec_color, str) or not validateColorString(sec_color)):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_color_given']
        return msg, code

    if not title_ and not color and not sec_color and not image:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_attributes_for_tag']
        return msg, code

    res = update_tag_ts(id, title_, color, sec_color, image)
    if res == -1:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tags_parameter']
        return msg, code
    if res == -2:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['tag_title_must_be_unique']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#get tags
@app.route("/tags", methods=['GET'])
def get_tags():
    res = get_tags_info()
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['no_tags']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
        
        
#get tags by search criteria
@app.route("/tags/search", methods=['GET'])
def search_tags():
    search = request.args.get('search')

    if not search:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_search_arg']
        return msg, code

    res = tags_search_info(search)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['no_tags_found']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
        

#get tag image
@app.route("/tag/<int:id>/img", methods=['GET'])
def get_tag_image(id):
    res = get_tag_image_img(id)
    if res == -1:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_img_not_found']
        return msg, code
    else:
        return send_file(res, mimetype='image/gif')


#update tag
@app.route("/tag/<int:id>/img/delete", methods=['DELETE'])
def delete_tag_img(id):
    res = delete_tag_img_ts(id)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    if res == -4:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['tag_has_no_img']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
        
        
#delete TAG
@app.route("/tag/<int:id>/delete", methods=['DELETE'])
def delete_tag(id):
    res = delete_tag_ts(id) 
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        code = http_responses['OK']['code']
        msg = http_responses['OK']['tag_deleted']
        return msg, code
        

#create new list
@app.route("/list/new", methods=['POST'])
def new_list(): 
    list_json = request.json 
    try:
        new_list = list_json['list']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_list']
        return msg, code
    
    if not isinstance(new_list, dict):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_list_given']
        return msg, code
    
    try:
        title = new_list['title']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_list_title']
        return msg, code
        
    if not isinstance(title, str) or len(title) > caracter_limit['list_title']:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_list_title_given']
        return msg, code
    
    description = ''
    try:
        description = new_list['description']
    except:
        description = defaults['list_description']
        
    if not isinstance(description, str) or len(description) > caracter_limit['list_description']:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_list_description_given']
        return msg, code
                  
    res = new_list_ts(title, description)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['list_title_must_be_unique']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#update list
@app.route("/list/<int:id>/update", methods=['PUT'])
def change_list(id):     
    list_json = request.json 
    try:
        new_list = list_json['list']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_list']
        return msg, code
    
    if not isinstance(new_list, dict):
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_list_given']
        return msg, code
    
    try:
        title_ = new_list['title']
    except:
        title_ = None
        
    if title_: 
        if not isinstance(title_, str) or len(title_) > caracter_limit['list_title']:
            code = http_responses['BadRequest']['code']
            msg = http_responses['BadRequest']['wrong_list_title_given']
            return msg, code
    
    try:
        description = new_list['description']
    except:
        description = None   
    
    if description:
        if not isinstance(description, str) or len(description) > caracter_limit['list_description']:
            code = http_responses['BadRequest']['code']
            msg = http_responses['BadRequest']['wrong_list_description_given']
            return msg, code
                  
    if not title_ and not description:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_attributes_for_list']
        return msg, code
    
    res = update_list_ts(id, title_, description)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['link_url_must_be_unique']
        return msg, code
    if res == -5:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['link_name_must_be_unique']
        return msg, code
    if res == -6:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#add link to list
@app.route("/list/<int:id>/update/add", methods=['PUT'])
def add_link_to_list(id):
    linkid = request.args.get('linkid')
    linkids = request.args.get('linkids')
    
    if not linkid and not linkids:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_link']
        return msg, code
        
    if linkid and linkids:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['array_or_string']
        return msg, code
    
    res = ''
    if linkid:
        res = add_link_to_list_ts(id, linkid, single=True)
    else:
        res = add_link_to_list_ts(id, linkids, single=False)
    
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_ids_given']
        return msg, code  
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['wrong_link_ids_given']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['Conflict']['code']
        msg = http_responses['Conflict']['link_must_not_be_repited_in_list']
        return msg, code
    if res == -5:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
        

#remove link from list
@app.route("/list/<int:id>/update/remove", methods=['PUT'])
def remove_link_from_list(id):
    linkid = request.args.get('linkid')
    linkids = request.args.get('linkids')
    
    if not linkid and not linkids:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_new_link']
        return msg, code
        
    if linkid and linkids:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['array_or_string']
        return msg, code
       
    res = ''
    if linkid:
        res = remove_link_from_list_ts(id, linkid, single=True)
    else:
        res = remove_link_from_list_ts(id, linkids, single=False)
    
    if res == 0:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['wrong_tag_ids_given']
        return msg, code  
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['wrong_link_ids_given']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['list_has_no_links']
        return msg, code  
    if res == -5:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers


#delete list
@app.route("/list/<int:id>/delete", methods=['DELETE'])
def delete_list(id):        
    res = delete_list_ts(id) 
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['couldt_save_changes']
        return msg, code
    else:
        code = http_responses['OK']['code']
        msg = http_responses['OK']['list_deleted']
        return msg, code
        

#get lists
@app.route("/lists", methods=['GET'])
def get_lists():
    res = get_lists_info()
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['no_lists']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers
        
        
#get lists by search criteria
@app.route("/lists/search", methods=['GET'])
def search_lists():
    search = request.args.get('search')
    
    if not search:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_search_arg']
        return msg, code

    res = lists_search_info(search)
    if res == -1:
        code = http_responses['ServiceUnavailable']['code']
        msg = http_responses['ServiceUnavailable']['database_access_error']
        return msg, code
    if res == -2:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['resource_does_not_exist']
        return msg, code
    if res == -3:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    if res == -4:
        code = http_responses['NotFound']['code']
        msg = http_responses['NotFound']['no_lists_found']
        return msg, code
    else:
        headers = http_responses['headers']
        return json.dumps(res), headers