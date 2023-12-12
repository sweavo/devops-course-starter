import flask
import http
import werkzeug.exceptions as wz_exceptions

from todo_app.flask_config import Config
from todo_app.data import storage_trello as persistence
from todo_app.ViewModel import ViewModel


def exceptions_dict(codes_enum, exceptions):
    """Tame the intEnum of HTTPStatus and werkzeug default exceptions into a dict keyed on status code"""
    return_dict = {}
    for code in codes_enum:
        is_exception = code in wz_exceptions.default_exceptions
        flask_api = ["response", "abort"][is_exception]
        return_dict[code.value] = {
            "code": code.value,
            "text": code.description or code.name,
            "api": flask_api,
            "is_exception": is_exception,
        }
    return return_dict


HTTP_STATUSES = exceptions_dict(http.HTTPStatus, wz_exceptions.default_exceptions)


def error_menu():
    """Generator function to make a clickable menu of status codes"""
    yield "<html><head><title>Error menu</title></head><body><ul>"
    for key in HTTP_STATUSES:
        status_info = HTTP_STATUSES[key]
        yield f"<li><a href='/error/{status_info['code']}'>flask.{status_info['api']}({status_info['code']})</a>: {status_info['text']}</li>"
    yield "</ul></body></html>"


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object(Config())

    @app.route("/test")
    def test():
        """Used by check-connectivity.sh to verify the network path to the flask
        server in the face of wonk from corporate IT, VPN, and the desire to
        run under WSL.
        """
        return "Hello World!"

    @app.route("/")
    def index():
        """Main screen of the app"""
        try:
            todo_items = ViewModel(persistence.get_items())
        except persistence.HTTP401Exception as e:
            return flask.render_template(
                "bootstrap.html",
                bootstrap_instructions=persistence.BOOTSTRAP_INSTRUCTIONS,
            )
        return flask.render_template("index.html", view_model=todo_items)

    @app.route("/error")
    @app.route("/error/<which>")
    def return_error(which=None):
        if which:
            status = int(which)
            if status in wz_exceptions.default_exceptions:
                flask.abort(status)
            else:
                return flask.Response(
                    response=f"app.py wrote: {HTTP_STATUSES[status]['text']}",
                    status=status,
                )
        else:
            return "".join(error_menu())

    @app.route("/additem", methods=["POST"])
    def add_item():
        """
        Add a TODO item to the database

        This URL transitions state and redirects back to the main screen

        An example of reading posted form data
        """
        item_title = flask.request.form.get("title")
        if item_title:  # don't add empty items
            persistence.add_item(item_title)
        return flask.redirect("/")  # discourage revisiting this URL

    @app.route("/completeitem/<id>", methods=["POST"])
    def complete_item(id):
        """Transition the given todo item to Done state.

        This URL transitions state and redirects back to the main screen
        An example of reading path parameters in flask.
        """
        card = persistence.get_item(id)
        card.status = "Done"
        persistence.save_item(card)
        return flask.redirect("/")  # discourage revisiting this URL

    return app
