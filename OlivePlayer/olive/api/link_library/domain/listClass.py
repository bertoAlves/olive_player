import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import backref, relationship

sys.path.append('../persistance')
from db_connect import model

sys.path.append('C:/Users/catar/OneDrive/Documentos/olive/api/utils')
from dictionary_library import caracter_limit, defaults

#association table between link - tag (many to many)
association_table = Table('_LINKS_OF_LIST', model.metadata,
    Column('list_id', Integer, ForeignKey('_lists.id')),
    Column('link_id', Integer, ForeignKey('_links.id'))
)

class list_class(model):

    __tablename__ = "_lists"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(caracter_limit['list_title']), nullable=False, unique=True)
    description = Column(String, nullable=False, default=defaults['list_description'])
    
    links = relationship('link_class', secondary = association_table, backref=backref('_lists'))

    def __init__(mysillyobject, title, description):
        mysillyobject.title = title
        mysillyobject.description = description