from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class WebsiteForm(FlaskForm):
    address = StringField('address', validators=[DataRequired()])
