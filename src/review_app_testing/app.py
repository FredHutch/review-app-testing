#!/usr/bin/env python3

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
@app.route("/review-app-testing-review0")
def hello():
    return "Hello World  - (some content that was added in review0 branch)"


@app.route("/foo")
@app.route("/review-app-testing-review0/foo")
def foo():
    return "this is the foo endpoint"


@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    url = request.url
    return f"this is the 404 page (content added in review0 branch)<br/>url is {url}", 404

if __name__ == "__main__":
    app.run(port=5050, host="0.0.0.0")
