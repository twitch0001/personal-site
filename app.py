
import sys
import json
import pathlib
from dataclasses import dataclass
from datetime import datetime

from flask import Flask, render_template
# noinspection PyPackageRequirements
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


@dataclass
class Blog:
    page: str  # url of page
    name: str
    description: str
    created_at: int

    @property
    def pretty_time(self):
        return datetime.fromtimestamp(self.created_at).strftime('%c')


with open("data/projects.json", "rb") as f:
    raw_projects: list[dict] = json.load(f)
    projects: dict = {}
    for p in raw_projects:
        p = Project(**p)
        projects[p.page] = p


with open("data/blogs.json", "rb") as f:
    raw_blogs: list[dict] = json.load(f)
    blogs: dict = {}
    for b in raw_blogs:
        b = Blog(**b)
        blogs[b.page] = b


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/socials")
def socials_page():
    return render_template("socials.html")


@app.route("/blog")
def blog_page():
    return render_template("blog.html", blogs=list(blogs.values()))


@app.route("/projects")
def projects_page():
    return render_template("projects.html", projects=list(projects.values()))


@app.route("/projects/<page>")
def project_view(page: str):
    project = projects.get(page)
    if project is None:
        return render_template("404.html")
    return render_template(f"projects/{page}.html", project=project)


@app.route("/blog/<page>")
def blog_view(page: str):
    blog = blogs.get(page)
    if blog is None:
        return render_template("404.html")
    return render_template(f"blogs/{page}.html", blog=blog)
