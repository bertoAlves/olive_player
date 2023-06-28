import os, sys

from flask import Flask
from middleware import middleware

sys.path.append('../../utils')
from dictionary_library import http_responses

from play import play_blueprint
from library import library_blueprint

app = Flask(__name__)

app.wsgi_app = middleware(app.wsgi_app)

app.register_blueprint(play_blueprint)
app.register_blueprint(library_blueprint)

if __name__ == '__main__':
    app.run(debug=True)