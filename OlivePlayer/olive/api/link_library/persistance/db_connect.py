from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///C:\\sqlite\\gui\\SQLiteStudio-3.2.1\\SQLiteStudio\\link_library.db')

model = declarative_base()
model.metadata.bind = eng

def new_session():
    Session = sessionmaker(eng)
    session = Session()
    return session