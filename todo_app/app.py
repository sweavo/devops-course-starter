import flask

from todo_app.flask_config import Config

from todo_app.data import storage_trello as persistence


app = flask.Flask(__name__)
app.config.from_object(Config())

@app.route('/test')
def test():
    return 'Hello World!'

@app.route('/')
def index():
    todo_items = persistence.get_items()
    return flask.render_template('index.html',items=todo_items)

@app.route('/additem', methods=['POST'])
def add_item():
    item_title = flask.request.form.get('title')
    if item_title: # don't add empty items
        persistence.add_item(item_title)
    return flask.redirect('/') # discourage revisiting this URL

@app.route('/completeitem/<id>', methods=['POST'])
def complete_item(id):
    card = persistence.get_item(id)
    card.status = 'Done'
    persistence.save_item(card)
    return flask.redirect('/') # discourage revisiting this URL

