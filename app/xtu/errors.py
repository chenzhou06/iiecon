from flask import render_template

from . import xtu


@xtu.app_errorhandler(403)
def forbidden(e):
    return render_template("403.html")
