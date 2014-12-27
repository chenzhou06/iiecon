from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField("电子邮件", validators=[Required(), Length(1,64),
                                            Email()])
    password = PasswordField("密码", validators=[Required()])
    remember_me = BooleanField("保持登录")
    submit = SubmitField("登录")


class RegistrationForm(Form):
    email = StringField("邮箱", validators=[Required(), Length(1,64),
                                            Email()])
    username = StringField("用户名", validators=[
        Required(), Length(1.64), Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                         "用户名只能包含字母、数字、小数点和下划线 "
                                         )])
    password = PasswordField("密码", validators=[
        Required(), EqualTo("password2", message="密码不一致")])
    password2 = PasswordField("重复密码", validators=[Required()])
    submit = SubmitField("注册")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已注册")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已注册")


class ChangePasswordForm(Form):
    old_password = PasswordField("旧密码", validators=[Required()])
    password = PasswordField("新密码", validators=[
        Required(), EqualTo("password2", message="密码不一致")])
    password2 = PasswordField("重复新密码", validators=[Required()])
    submit = SubmitField("修改密码")


class PasswordResetRequestForm(Form):
    email = StringField("邮箱", validators=[Required(), Length(1, 64),
                                            Email()])
    submit = SubmitField("重设密码")


class PasswordResetForm(Form):
    email = StringField("邮箱", validators=[Required(), Length(1, 64),
                                            Email()])
    password = PasswordField("新密码", validators=[
        Required(), EqualTo("password2", message="密码不一致")])
    password2 = PasswordField("重复新密码", validators=[Required()])
    submit = SubmitField("重设密码")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError("未知邮箱")