import flask
from webapputils import Webapp
import requests


from .callsign import doCallsignQuery
from .propagation import doPropagationReport

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
    res = flask.make_response(flask.jsonify(
        {
            "success": True,
            "info": result
        }
    ))
    res.headers.set('Cache-Control', 's-maxage=60, stale-while-revalidate')
    return res
    
@app.route("/callsign/<callsign>/badges/lookups")
def handleCallignLookupBadge(callsign):

    result = doCallsignQuery(callsign)

    if type(result) != dict:
        return flask.jsonify(
            {
                "success": False,
                "error": result
            }
        ), 404
    
    
    res = flask.make_response("",302)
    lookups = result["lookups"]
    res.headers["Location"] = f"https://img.shields.io/badge/lookups-{lookups}-green"
    res.headers.set('Cache-Control', 's-maxage=60, stale-while-revalidate')
    return res

@app.route("/propagation")
def handlePropagation():
    
    # Fetch propagation data
    data = doPropagationReport()
    
    res = flask.make_response(flask.jsonify(
        {
            "success": True,
            "info": data
        }
    ))
    res.headers.set('Cache-Control', 's-maxage=60, stale-while-revalidate')
    return res

if __name__ == "__main__":
    app.run(debug=True)
