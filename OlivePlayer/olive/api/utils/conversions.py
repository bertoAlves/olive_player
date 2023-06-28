#utils conversions file for servers
import sys, pathlib, base64

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

#split list in two
def split_list(list):
    half = ''
    if len(list) % 2 == 0: 
        half = len(list)//2
    else:
        half = (len(list)//2) + 1
    return list[:half], list[half:]
    
#encode string  
def encode(key, string):
    enc_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        enc_c = chr(ord(string[i]) + ord(key_c) % 256)
        enc_chars.append(enc_c)
    encoded_string = "".join(enc_chars)
    return encoded_string

#decode string    
def decode(key, string):
    dec_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        dec_c = chr(ord(string[i]) - ord(key_c) % 256)
        dec_chars.append(dec_c)
    decoded_string = "".join(dec_chars)
    return decoded_string