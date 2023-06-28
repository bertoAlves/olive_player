import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

sys.path.append('C:/Users/catar/OneDrive/Documentos/olive/api/link_library/persistance')
from db_connect import model, new_session

sys.path.append('C:/Users/catar/OneDrive/Documentos/olive/api/link_library/domain')
from listClass import list_class
from tagClass import tag_class
from linkClass import link_class


#model.metadata.drop_all()
#model.metadata.create_all()





