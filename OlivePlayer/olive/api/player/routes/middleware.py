from werkzeug.wrappers import Request, Response, ResponseStream
import base64, requests
import sys

sys.path.append('../../utils')
from dictionary_library import http_responses, auth_server

class middleware():

    def __init__(self, app):
        self.app = app
        
        
    def __call__(self, environ, start_response):
        request = Request(environ)
        try:
            res = requests.get(auth_server['validate_session'], cookies=request.cookies)
        except:
            res = Response(http_responses['ServiceUnavailable']['server_not_available'], mimetype= 'text/plain', status=http_responses['ServiceUnavailable']['code'])
            return res(environ, start_response)           
            
        if res.status_code == http_responses['OK']['code']:     
            return self.app(environ, start_response)
        else:
            res = Response(res.text, mimetype= 'text/plain', status=res.status_code)
            return res(environ, start_response)