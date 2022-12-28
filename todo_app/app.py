import flask

from todo_app.flask_config import Config

app = flask.Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    return flask.render_template('index.html')
