#utils validations file
import sys, re

sys.path.append('../../')
from dictionary_library import audio_files_extensions

#validate if file as one of the pretended extensions
def validateAudioFileExtension(file):
    for extension in audio_files_extensions:
        if file.lower().endswith(extension):
            return True
    return False
    
#validate if file is a groove playlist
def validateGroovePlaylistFileExtension(file):
    if file.lower().endswith('.zpl'):
        return True
    return False

#validate format of folder name    
def validateAlbumFolder(folder):
    prog = re.compile(r'^.+ - .+ \(\d{4}\)$')
    result = prog.match(folder)
    if result != None:
        return True
    else:
        return False
        
#validate format of folder name    
def validateSinglesFolder(folder):
    prog = re.compile(r'^.+ - Singles$')
    result = prog.match(folder)
    if result != None:
        return True
    else:
        return False
