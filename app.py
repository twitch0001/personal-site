import sys

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

if sys.platform != "win32":
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/blog")
def blog_page():
    return render_template("page.html")


@app.route("/projects")
def projects_page():
    return render_template("projects.html")
