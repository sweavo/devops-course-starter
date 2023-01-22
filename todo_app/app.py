import flask

from todo_app.flask_config import Config
from todo_app.data import storage_trello as persistence

app = flask.Flask(__name__)
app.config.from_object(Config())

@app.route('/test')
def test():
    """ Used by check-connectivity.sh to verify the network path to the flask 
        server in the face of wonk from corporate IT, VPN, and the desire to 
        run under WSL.
    """
    return 'Hello World!'

@app.route('/')
def index():
    """ Main screen of the app """
    todo_items = persistence.get_items()
    return flask.render_template('index.html',items=todo_items)

@app.route('/additem', methods=['POST'])
def add_item():
    """
        Add a TODO item to the database
        
        This URL transitions state and redirects back to the main screen

        An example of reading posted form data
    """
    item_title = flask.request.form.get('title')
    if item_title: # don't add empty items
        persistence.add_item(item_title)
    return flask.redirect('/') # discourage revisiting this URL

@app.route('/completeitem/<id>', methods=['POST'])
def complete_item(id):
    """ Transition the given todo item to Done state.

        This URL transitions state and redirects back to the main screen

        An example of reading path parameters in flask.
    """
    card = persistence.get_item(id)
    card.status = 'Done'
    persistence.save_item(card)
    return flask.redirect('/') # discourage revisiting this URL
