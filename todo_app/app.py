import flask
import http
import werkzeug.exceptions as wz_exceptions

from todo_app.flask_config import Config

from todo_app.data import session_items 


app = flask.Flask(__name__)
app.config.from_object(Config())

def error_menu():
    """ Generator function to make a clickable menu of status codes"""
    yield "<html><head><title>Error menu</title></head><body><ul>"
    for code in http.HTTPStatus:
        is_exception = code in wz_exceptions.default_exceptions
        flask_api = ['response','abort'][is_exception]
        yield f"<li><a href='/error/{code.value}'>flask.{flask_api}({code.value})</a>: {code.description or code.name}</li>"
    yield "</ul></body></html>"

@app.route('/test')
def test():
    return 'Hello World!'

@app.route('/')
def index():
    todo_items = session_items.get_items()
    return flask.render_template('index.html',items=todo_items)

@app.route('/error')
@app.route('/error/<which>')
def return_error(which=None):
    if which:
        status=int(which)
        if status in wz_exceptions.default_exceptions:
            flask.abort(status)
        else:
            return flask.Response(status=status)
    else:
        return ''.join(error_menu())


@app.route('/additem', methods=['POST'])
def additem():
    item_title = flask.request.form.get('title')
    if item_title: # don't add empty items
        session_items.add_item(item_title)
    return flask.redirect('/')
