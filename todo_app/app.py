import flask

from todo_app.flask_config import Config

app = flask.Flask(__name__)
app.config.from_object(Config())

@app.route('/test')
def test():
    return 'Hello World!'

@app.route('/')
def index():
    return flask.render_template('index.html')
