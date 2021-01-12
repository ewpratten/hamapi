import flask
from webapputils import Webapp
import requests


from .callsign import doCallsignQuery

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)


@app.errorhandler(404)
def page_not_found(e):
    return "Error 404", 404
    # return flask.render_template('404.html'), 404


@app.route("/callsign/<callsign>")
def handleCallsign(callsign):

    result = doCallsignQuery(callsign)

    if type(result) != dict:
        return flask.jsonify(
            {
                "success": False,
                "error": result
            }
        )
    return flask.jsonify(
        {
            "success": True,
            "info": result
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
