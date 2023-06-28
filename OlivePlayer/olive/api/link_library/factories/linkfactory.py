import sys

sys.path.append('../domain')
from linkClass import link_class
from tagClass import tag_class

def linktodict(link):
    link_json = {}
    link_json['id'] = link.id
    link_json['name'] = link.name
    link_json['description'] = link.description
    link_json['url'] = link.url
    link_json['creation_date'] = str(link.created)
    link_json['last_changed_date'] = str(link.last_changed)

    tags_json = []
    for tag in link.tags:
        tag_json = {}
        tag_json['id'] = tag.id
        tag_json['title'] = tag.title
        tag_json['color'] = tag.color
        tag_json['sec_color'] = tag.sec_color
        tag_json['has_image'] = tag.has_image
        tags_json.append(tag_json)
        
    link_json['tags'] = tags_json
    return link_json