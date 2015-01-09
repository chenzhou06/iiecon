from flask import render_template, redirect, url_for, abort, \
        flash, request, current_app, make_response

from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import xtu
from ..models import User, Role
from .forms import EditProfileForm, EditProfileAdminForm, \
                   PostForm, CommentForm
from .. import db
from ..models import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required

import random


gmsg = [
    {'author': "Ralph Waldo Emerson, Poet",
    "text": "Do not go where the path may lead, go instead where there is no path and leave a trail."},

    {"author": "Napoleon Hill, Motivational Writer",
    "text": "If you cannot do great things, do small things in a great way."},

    {"author": "John Lennon, Musician",
    "text": "When I was 5 years old, \
            my mother always told me that happiness was the key to life. \
            When I went to school, \
            they asked me what I wanted to be when I grew up. \
            I wrote down ‘happy.’ \
            They told me I didn’t understand the assignment, \
            and I told them they didn’t understand life."},

    {"author": "Mike Todd, Film Producer",
    "text": "I’ve never been poor, only broke. Being poor is a frame of mind."}
]

@xtu.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for(".index"))
    greetingMessage = gmsg[random.randint(0, len(gmsg)-1)]
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["IIECON_POSTS_PER_PAGE"],
        error_out=False)
    posts = pagination.items
    return render_template("xtu/index.html", form=form, posts=posts,
                           pagination=pagination, greetingMessage=greetingMessage)

@xtu.route("/newpost", methods=["GET", "POST"])
def newpost():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for(".index"))
    return render_template("xtu/newpost.html", form=form)

@xtu.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("user.html", user=user, posts=posts)

@xtu.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("个人资料保存成功")
        return redirect(url_for(".user", username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", form=form)

@xtu.route("/edit-profile/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash("资料更新成功")
        return redirect(url_for(".user", username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template("edit_profile.html", form=form, user=user)


@xtu.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash("评论成功")
        return redirect(url_for(".post", id=post.id, page=-1))
    page = request.args.get("page", 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
                current_app.config ["IIECON_COMMENTS_PER_PAGE"] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config["IIECON_COMMENTS_PER_PAGE"],
        error_out=False)
    comments = pagination.items
    return render_template("xtu/post.html", posts=[post], form=form, comments=comments, pagination=pagination,
                            post=post)


@xtu.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash("文章修改成功")
        return redirect(url_for(".post", id=post.id))
    form.body.data = post.body
    return render_template("xtu/edit_post.html", form=form)

@xtu.route("/moderate")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get("page", 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config["IIECON_COMMENTS_PER_PAGE"],
        error_out=False)
    comments = pagination.items
    return render_template("xtu/moderate.html", comments=comments,
                            pagination=pagination, page=page)


@xtu.route("/moderate/enable/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for(".moderate",
                            page=request.args.get("page", 1, type=int)))


@xtu.route("/moderate/disable/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for(".moderate",
            page=request.args.get("page", 1, type=int)))