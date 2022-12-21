import sys
import json
import pathlib
from dataclasses import dataclass

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

if sys.platform != "win32":
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )


@dataclass
class Project:
    page: str  # url of page
    name: str
    description: str
    preview_image: str
    markdown: str  # pages/projects/*.md


with open("data/projects.json", "rb") as f:
    raw_projects: list[dict] = json.load(f)
    projects: dict = {}
    for p in raw_projects:
        p = Project(**p)
        projects[p.page] = p


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/blog")
def blog_page():
    return render_template("page.html")


@app.route("/projects")
def projects_page():
    return render_template("projects.html", projects=list(projects.values()))


@app.route("/projects/<page>")
def project_view(page: str):
    return render_template("notready.html", page=page)

