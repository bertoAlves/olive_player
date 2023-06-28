import os, sys, datetime

from flask import Flask, request, make_response, render_template, redirect, url_for, flash

sys.path.append('../services')
from sessionservice import login_, validate_session_, logout_

sys.path.append('../../utils')
from dictionary_library import http_responses

app = Flask(__name__)

#login  
@app.route("/auth/login", methods=['GET'])
def login():
    auth = ''
    try: 
        auth = request.authorization['password']
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_auth']
        return msg, code
    
    res = login_(auth)
    if res == -1:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['session_already_running']
        return msg, code
    elif res == -2:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['database_conflict']
        return msg, code
    elif res is not False:
        ret = make_response(http_responses['OK']['successful_login'])
        ret.set_cookie('date', res.string_date)        
        ret.set_cookie('key', res.key)
        ret.set_cookie('number', res.number)
        return ret
    else:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['failed_login']
        return msg, code   


#validate session
@app.route("/auth/validate_session", methods=['GET'])
def validate_session():
    cookies = ''
    try: 
        cookies = request.cookies
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_session_info']
        return msg, code
    
    res = validate_session_(cookies)
    if res == -1:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_session']
        return msg, code   
    elif res:
        code = http_responses['OK']['code']
        msg = http_responses['OK']['valid_session']
        return msg, code   
    else:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['invalid_session']
        return msg, code


#login  
@app.route("/auth/logout", methods=['DELETE'])
def logout():
    cookies = ''
    try: 
        cookies = request.cookies
    except:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_session_info']
        return msg, code
    
    res = logout_(cookies)
    if res == -1:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['no_session']
        return msg, code
    elif res == -2:
        code = http_responses['InternalServerError']['code']
        msg = http_responses['InternalServerError']['request_error']
        return msg, code 
    elif res:
        code = http_responses['OK']['code']
        msg = http_responses['OK']['logged_out']
        return msg, code   
    else:
        code = http_responses['BadRequest']['code']
        msg = http_responses['BadRequest']['invalid_session']
        return msg, code 


if __name__ == '__main__':
    app.run(debug=True)