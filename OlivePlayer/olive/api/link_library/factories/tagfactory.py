import sys

sys.path.append('../domain')
from tagClass import tag_class

def tagtodict(tag):
    tag_json = {}
    tag_json['id'] = tag.id
    tag_json['title'] = tag.title
    tag_json['color'] = tag.color
    tag_json['sec_color'] = tag.sec_color
    tag_json['has_image'] = tag.has_image
    return tag_json