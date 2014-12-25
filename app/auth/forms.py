from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length

class LoginForm(Form):
    email = StringField("电子邮件", validators=[Required(), Length(1,64),
                                            Email()])
    password = PasswordField("密码", validators=[Required()])
    remember_me = BooleanField("保持登录")
    submit = SubmitField("登录")
