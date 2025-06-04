from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class TicketForm(FlaskForm):
    equipment_id = SelectField('Equipment', coerce=int)
    description = TextAreaField('Issue Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class BookingForm(FlaskForm):
    equipment_id = SelectField('Equipment', coerce=int)
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M')
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M')
    submit = SubmitField('Book')