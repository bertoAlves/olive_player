import os, sys, datetime, shutil, subprocess, configparser
from lxml import etree
from pathlib import Path

sys.path.append('utils')
from dictionary_library import folder_navegation

#script start/update database
def start():
    config = configparser.ConfigParser()
    todaysDate = datetime.datetime.today()
    
    #check if dbversions folder exists
    if not os.path.exists(folder_navegation['DBVERSION_FOLDER']):
        Path(folder_navegation['DBVERSION_FOLDER']).mkdir(parents=True, exist_ok=True)
    
    #check if database folder exists
    if not os.path.exists(folder_navegation['DB_FOLDER']):
        Path(folder_navegation['DB_FOLDER']).mkdir(parents=True, exist_ok=True)
      
    #check if config file exists
    conf_exts = False
    last_run = ''
    if os.path.exists(folder_navegation['CONFIG_FILE']):       
        config.read(folder_navegation['CONFIG_FILE'])
        last_run = config['LAST_RUN_SUCCESS']
        if last_run['Date']:
            conf_exts = True
    
    #get parser for db.xml file
    schema_root = etree.parse(folder_navegation['SCHEMA_FILE']).getroot()
    schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema = schema)
    
    #get modified date of music folder
    modifiedDateMusicFolder = ''
    if os.path.exists(folder_navegation['MUSIC_FOLDER']):
        modifiedDateMusicFolder = datetime.datetime.fromtimestamp(os.path.getmtime(folder_navegation['MUSIC_FOLDER']))
    else:
        sys.exit('No Music folder found')
    
    #get modified date of playlists folder
    modifiedDatePlaylistFolder = ''
    if os.path.exists(folder_navegation['PLAYLISTS_FOLDER']):
        modifiedDatePlaylistFolder = datetime.datetime.fromtimestamp(os.path.getmtime(folder_navegation['PLAYLISTS_FOLDER']))
    else:
        sys.exit('No Playlists folder found')
    
    
    startDatabase = False
    updateDatabase = False
    updatePlaylists = False
    
#---check if db.xml file exists. If not, inicialize database.
    if not os.path.exists(folder_navegation['DB_FILE']):
        print('Initializing database')
        subprocess.call('python data_scripts/init.py',shell=True)
        if os.path.exists(folder_navegation['DB_FILE']):
            try:
                etree.parse(folder_navegation['DB_FILE'], parser)
            except:
                shutil.copy2(folder_navegation['DB_FILE'], 'db_versions/INVALIDdb_'+ str(todaysDate).replace(":", "h",1).replace(":", "m",1) +'s.xml')            
                os.remove(folder_navegation['DB_FILE'])
                sys.exit('db.xml in wrong format')
            startDatabase = True
        else:
            sys.exit('Failed to initialize')
            
#---check if music folder was modified after the last time the script ran. If so, run updates.py and delets.py to check for updates.   
    elif conf_exts and modifiedDateMusicFolder > datetime.datetime.strptime(last_run['Date'], '%Y-%m-%d %H:%M:%S.%f'): 
        try:
            etree.parse(folder_navegation['DB_FILE'], parser)
        except:
            sys.exit('db.xml is in wrong format. Impossible to run updates')
            
        print('Updating database')   
        subprocess.call('python data_scripts/updts.py',shell=True)
        try:
            etree.parse(folder_navegation['DB_FILE'], parser)
        except:
            shutil.copy2(folder_navegation['DB_FILE'], 'db_versions/INVALIDdb_'+ str(todaysDate).replace(":", "h",1).replace(":", "m",1) +'s.xml')
            shutil.copy2('db_versions/db_'+ str(last_run['Date']).replace(":", "h",1).replace(":", "m",1) +'s.xml', folder_navegation['DB_FILE'])
            sys.exit('db.xml in wrong format')        
        subprocess.call('python data_scripts/delets.py',shell=True)
        updateDatabase = True
    
#---if changes were made, or if the playlist folder was modified after the last time the script ran. If so, run pls.py to check for updates in playlists
    if (startDatabase or updateDatabase) or (modifiedDatePlaylistFolder > datetime.datetime.strptime(last_run['Date'], '%Y-%m-%d %H:%M:%S.%f')):
        try:
            etree.parse(folder_navegation['DB_FILE'], parser)
        except:
            sys.exit('db.xml is in wrong format. Impossible to run updates to playlists')
            
        print('Updating playlists in database')
        subprocess.call('python data_scripts/pls.py',shell=True)
        try:
            etree.parse(folder_navegation['DB_FILE'], parser)
        except:
            shutil.copy2(folder_navegation['DB_FILE'], 'db_versions/INVALIDdb_'+ str(todaysDate).replace(":", "h",1).replace(":", "m",1) +'s.xml')
            shutil.copy2('db_versions/db_'+ str(last_run['Date']).replace(":", "h",1).replace(":", "m",1) +'s.xml', folder_navegation['DB_FILE'])
            sys.exit('db.xml in wrong format')           
        updatePlaylists = True
        
    if not startDatabase and not updateDatabase and not updatePlaylists:
        sys.exit('No changes made to the database')
    
    #clarify current db.xml file
    subprocess.call('python data_scripts/clarify.py',shell=True)
    #save new date for LAST_RUN_SUCCESS in start.ini and save db_DATE.xml
    shutil.copy2(folder_navegation['DB_FILE'], 'db_versions/db_'+ str(todaysDate).replace(":", "h",1).replace(":", "m",1) +'s.xml')
    
    #save the current date in config file
    with open(folder_navegation['CONFIG_FILE'], 'w') as configfile:
        config['LAST_RUN_SUCCESS'] = {'Date': todaysDate}
        config.write(configfile)
    

if __name__ == '__main__':
    start()