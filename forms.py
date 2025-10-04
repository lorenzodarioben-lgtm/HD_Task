from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Create account")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ListForm(FlaskForm):
    name = StringField("List name", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("Save")

class ItemForm(FlaskForm):
    name = StringField("Item", validators=[DataRequired(), Length(max=160)])
    quantity = IntegerField("Qty", validators=[NumberRange(min=1)], default=1)
    priority = SelectField("Priority", choices=[("low","Low"),("med","Medium"),("high","High")], default="med")
    submit = SubmitField("Add item")
