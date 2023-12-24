#!/usr/bin/python3
"""run flask server"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """states returned"""
    return render_template('9-states.html\
', states=storage.all("State"), state=None)


@app.route("/states/<id>", strict_slashes=False)
def id_state(id):
    """states returned"""
    states = storage.all("State")
    # if "State.{}".format(id) not in states:
    #     return render_template('9-states.html')
    state = storage.all("State").get("State.{}".format(id))
    return render_template('9-states.html\
', state=state, states=None)


@app.teardown_appcontext
def reset(error):
    """reload data"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
