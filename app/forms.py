from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length

class LoginForm(Form):
	openid = TextField('openid',validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    firstname = TextField('firstname', validators = [Length(min = 0, max = 40)])
    lastname = TextField('lastname', validators = [Length(min = 0, max = 40)])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

    def __init__(self, original_nickname, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)
      self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

class Venture(Form):
    