from flask import render_template, redirect, url_for, abort, \
        flash, request, current_app, make_response

from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import xtu
from ..models import User
# from .forms import EditProfileForm, EditProfileAdminForm, PostForm,
#         CommentForm
# from .. import db
# from .models import Permission, Role, User, Post, Comment
# from .decorators import admin_required, permission_required

@xtu.route("/")
def index():
    return render_template("xtu/index.html")

@xtu.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template("user.html", user=user)