#utils validations file
import sys, re, datetime

#validate if search is (anything - SINGLES) 
def validateSearchParameter_STRING_SINGLES(search):
    prog = re.compile(r'^.* - SINGLES$')
    result = prog.match(search)
    if result != None:
        return True
    else:
        return False

#validate if search is (anything - anything)    
def validateSearchParameter_STRING_STRING(search):
    prog = re.compile(r'^.* - [a-zA-Z]+$')
    result = prog.match(search)
    if result != None:
        return True
    else:
        return False

#validate if search is (anything - YEAR)    
def validateSearchParameter_STRING_YEAR(search):
    prog = re.compile(r'^.* - [0-9]{4}$')
    result = prog.match(search)
    if result != None:
        return result
    else:
        return False
        
#validate if search is (YEAR)    
def validateSearchParameter_YEAR(search):
    prog = re.compile(r'^[0-9]{4}$')
    result = prog.match(search)
    if result != None:
        return True
    else:
        return False
        

#validate format of color string    
def validateColorString(color):
    prog = re.compile(r'^#[0-f]{6}$')
    result = prog.match(color)
    if result != None:
        return True
    else:
        return False
        
#validate format of url string  
def validateURLString(url):
    prog = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    result = prog.match(url)
    if result != None:
        return True
    else:
        return False

#validate format of date string       
def validateDateString(date):
    date_ = ''
    try:
        date_ = datetime.datetime.strptime(date, '%Y-%m-%d')
    except:
        date_ = None
    return date_
    
#validate if string has special caracters
def validate_string(string):
    if not string.strip():
        return False
    return all(c.isalnum() or c == ' ' for c in string.strip())
