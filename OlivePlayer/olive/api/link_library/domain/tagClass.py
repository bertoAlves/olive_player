import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, CheckConstraint
from sqlalchemy.orm import backref, relationship

sys.path.append('../persistance')
from db_connect import model

sys.path.append('C:/Users/catar/OneDrive/Documentos/olive/api/utils')
from dictionary_library import caracter_limit, defaults

class tag_class(model):

    __tablename__ = "_tags"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(caracter_limit['tag_title']), nullable=False, unique=True)
    color = Column(String, nullable=False, default=defaults['tag_color'])
    sec_color = Column(String, nullable=False, default=defaults['tag_sec_color'])
    has_image =  Column(String, unique=False, default=False)
    
    def __init__(mysillyobject, title, color, sec_color, has_image=False):
        mysillyobject.title = title
        mysillyobject.color = color
        mysillyobject.sec_color = sec_color
        mysillyobject.has_image = has_image
               
    __table_args__ = (CheckConstraint("color GLOB('#[0-f][0-f][0-f][0-f][0-f][0-f]')", name='color_check'),)