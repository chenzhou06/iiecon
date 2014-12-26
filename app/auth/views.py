from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated() \
            and not current_user.confirmed \
            and request.endpoint[:5] != "auth.":
        return redirect(url_for("auth.unconfirmed"))

@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for("xtu.index"))
    return render_template("auth/unconfirmed.html")

@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email("auth/email/confirm",
                "验证账号", user, token=token)
    flash("新验证邮件已经发送")
    return redirect(url_for("xtu.index"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or url_for("xtu.index"))
        flash("用户名无效或密码错误")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("注销成功")
    return redirect(url_for("xtu.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, "邮箱验证",
                    "auth/email/confirm", user=user, token=token)
        flash("验证邮件已经发送到您的邮箱")
        return redirect(url_for("xtu.index"))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("xtu.index"))
    if current_user.confirm(token):
        flash("邮箱验证成功！")
    else:
        flash("验证连接已经失效")
    return redirect(url_for("xtu.index"))


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash("密码修改成功")
            return redirect(url_for("xtu.index"))
        else:
            flash("密码不正确")
    return render_template("auth/change_password.html",
                            form=form,)
