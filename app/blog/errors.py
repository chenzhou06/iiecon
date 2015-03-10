from flask import render_template

from . import blog


@blog.app_errorhandler(403)
def forbidden(e):
    return render_template("blog/403.html")


@blog.app_errorhandler(404)
def notfound(e):
    return render_template("blog/404.html")
