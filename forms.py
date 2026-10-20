from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

from models import AdminUser, User
from validators import MatchesText, SimpleEmail, UniqueValue


class BookForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired(), Length(max=255)])
    author = StringField("著者", validators=[DataRequired(), Length(max=255)])
    genre = StringField("ジャンル", validators=[DataRequired(), Length(max=100)])
    stock = IntegerField("在庫数", default=0, validators=[
        InputRequired(), NumberRange(min=0, message="在庫数は0以上です。")
    ])
    submit = SubmitField("保存")


class UserForm(FlaskForm):
    name = StringField("名前", validators=[DataRequired(), Length(max=255)])
    email = StringField("メール", validators=[DataRequired(), Length(max=255), SimpleEmail()])
    submit = SubmitField("保存")

    def __init__(self, *args, current_user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.email.validators.append(UniqueValue(
            User, "email", "このメールアドレスは登録済みです。",
            current_id=current_user_id, id_column="user_id"
        ))


class BorrowForm(FlaskForm):
    user_id = SelectField("利用者", coerce=int, validators=[DataRequired()])
    book_id = SelectField("本", coerce=int, validators=[DataRequired()])
    submit = SubmitField("貸出")


class DeleteForm(FlaskForm):
    confirm = StringField("確認", validators=[
        DataRequired(), MatchesText("DELETE", "DELETE と入力してください。")
    ])
    submit = SubmitField("削除")


class LoginForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField("ログイン")


class SignupForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("管理者を追加")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username.validators.append(
            UniqueValue(AdminUser, "username", "このユーザー名は登録済みです.")
        )
