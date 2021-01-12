import flask
from webapputils import Webapp
import requests

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)

@app.errorhandler(404)
def page_not_found(e):
    return "Error 404", 404
    # return flask.render_template('404.html'), 404
    
if __name__ == "__main__":
    app.run(debug=True)
