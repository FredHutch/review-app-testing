#!/usr/bin/env python3

from flask import Flask, request
app = Flask(__name__)

@app.route("/foo")
@app.route("/<branch_name>/foo")
def foo(branch_name=None):
    return "this is the foo endpoint"


@app.route("/cromwell-server")
@app.route("/<branch_name>/cromwell-server")
def crom(branch_name=None):
    return "this is the cromwell-server endpoint"


# this route should be defined last
@app.route('/')
@app.route('/<branch_name>/')
def hello(branch_name=None):
    if branch_name:
        return f"Hello World - (some content that was added in (dynamic) {branch_name} branch)"
    return "Hello World - (some content that was added in (static) review0 branch)"



@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    url = request.url
    return f"this is the 404 page (content added in review0 branch)<br/>url is {url}", 404

if __name__ == "__main__":
    app.run(port=5050, host="0.0.0.0", debug=True)
