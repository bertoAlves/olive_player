import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

sys.path.append('../persistance')
from db_connect import model

sys.path.append('../../utils')
from dictionary_library import caracter_limit, defaults

#association table between link - tag (many to many)
association_table = Table('_TAGS_OF_LINK', model.metadata,
    Column('link_id', Integer, ForeignKey('_links.id')),
    Column('tag_id', Integer, ForeignKey('_tags.id'))
)

class link_class(model):

    __tablename__ = "_links"

    id = Column(Integer, primary_key=True)
    name = Column(String(caracter_limit['link_name']), nullable=False, unique=True)
    description = Column(String(caracter_limit['link_description']), nullable=False, unique=False, default=defaults['link_description'])
    url = Column(String, nullable=False, unique=True)
    created = Column(DateTime, nullable=False, server_default=func.now())
    last_changed = Column(DateTime, nullable=False, server_default=func.now())
    list_id = Column(Integer, ForeignKey('_lists.id'))
    
    tags = relationship('tag_class', secondary = association_table, backref=backref('_links'))
    
    def __init__(mysillyobject, name, description, url):
        mysillyobject.name = name
        mysillyobject.url = url
        mysillyobject.description = description
        
    def change(mysillyobject):
        mysillyobject.last_changed = func.now()