from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired

class xSearchForm(FlaskForm):
    search = StringField('XDCC Search',
                         render_kw={"class": "form-control me-2", "placeholder": "XDCC Search", "aria-label": "Search for files"},
                         validators=[DataRequired()])
    search_button = SubmitField('Search', render_kw={"class": "btn btn-outline-success button-search", "type": "submit"})
