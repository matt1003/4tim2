from flask_wtf import Form

from wtforms import FloatField
from wtforms.validators import DataRequired


class RegistersForm(Form):
    value = FloatField('value', validators=[DataRequired()])
