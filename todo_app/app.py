import flask

from todo_app.flask_config import Config

from todo_app.data import session_items 

app = flask.Flask(__name__)
app.config.from_object(Config())

@app.route('/test')
def test():
    return 'Hello World!'

@app.route('/')
def index():
    todo_items = session_items.get_items()
    return flask.render_template('index.html',items=todo_items)

@app.route('/additem', methods=['POST'] )
def additem():
    return flask.make_response("Add not implemented",501) //TODO
