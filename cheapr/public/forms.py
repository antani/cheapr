from flask_wtf import Form
from wtforms import TextField, SelectField, PasswordField
from wtforms.validators import DataRequired

from cheapr.user.models import User

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False
        return True

class SearchForm(Form):
    searchterm = TextField('Search', validators=[DataRequired()])
    searchtype = SelectField('Type',choices=[('books', 'Books'), ('mobiles', 'Mobiles'),('electronics','Electronics'),('kitchen','Kitchen Appliances'),('tv','LED-LCD TVs'),
                            ('laptop','Laptops'),('computers','Computers')])


    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)