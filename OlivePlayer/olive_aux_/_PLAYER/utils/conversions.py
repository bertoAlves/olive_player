#utils conversions file
import sys, pathlib

#convert string to positive integer
#return false if string not integer
def convertStringToInteger(string):
    if str(string).isdigit():
        return int(string)
    else:
        return False

#convert string to array of strings
#return false if impossible to split string with separator or if empty string
def convertStringToArray(string, separator=';'):
    if string != None or string != '':
        string_array = string.split(separator)
        if len(string_array) == 1:
            return False
        else:
            return string_array
    else:
        return False

#convert array of strings to array of integers
#return false if array is empty or if any element cannot be converted
def convertArrayOfStringToArrayOfIntegers(strings):
    conversionToIntegers = []
    if len(strings) == 0:
        return False
        
    for string in strings:
        conversion = convertStringToInteger(string)
        if not conversion:
            return False
        else:
            conversionToIntegers.append(conversion)
    return conversionToIntegers

#segment folder in artist, album and year
def segment_album_folder(folder):   
    try:
        segmented_folder = []
        afi_artist = folder.split(' -')[0]
        afi_albumAndYear = folder.split('- ')[1]
        afi_year = afi_albumAndYear[-6:].replace("(","").replace(")","")
        afi_album_title = afi_albumAndYear[:-6]
        
        segmented_folder.append(afi_artist)
        segmented_folder.append(afi_album_title)
        segmented_folder.append(afi_year)
        return segmented_folder
    except:
        return None
        
#segment folder in artist, and SINGLES
def segment_singles_folder(folder):   
    try:
        segmented_folder = []
        afi_artist = folder.split(' -')[0]
        afi_singles= folder.split('- ')[1]
        
        segmented_folder.append(afi_artist)
        segmented_folder.append(afi_singles)
        return segmented_folder
    except:
        return None

#concatenate artist, album and year into folder
def create_folder_name(artist, album, year):
    folder = ''
    if isinstance(year, int) or isinstance(year, float):
        year = int(year)
        year_string = str(year)
        folder = artist + ' - ' + album + '(' + year_string + ')'
    else:
        folder = artist + ' - ' + album + '(' + year + ')'
    return folder
        
#seperate file from extension
def separate_file_from_extension(file):
    try:
        filename_and_extension = []
        filename_and_extension.append(pathlib.Path(file).stem)
        filename_and_extension.append(pathlib.Path(file).suffix)  
        if len(filename_and_extension) == 2:
            return filename_and_extension
        else:
            return None
    except:
        return None

#concatenate file with extension
def concatenate_file_and_extension(filename, extension):
    try:
        file = filename + extension
        return file
    except:
        return None

#concatenate folder and file into a path
def folder_file_path(folder = '', file = '', artist='', album='', year='', filename='', extension=''):
    if artist and album and year and filename and extension:
        folder = create_folder_name(artist, album, year)
        if folder:
            file = concatenate_file_and_extension(filename, extension)
            if not file:
                return None
        else:
           return None
           
    if folder and file:
        return folder + '/' + file
    return None

#split list in two
def split_list(list):
    half = ''
    if len(list) % 2 == 0: 
        half = len(list)//2
    else:
        half = (len(list)//2) + 1
    return list[:half], list[half:]

