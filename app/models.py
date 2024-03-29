from app import db
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nickname = db.Column(db.String(64), index = True, unique = True)
  email = db.Column(db.String(120), index = True, unique = True)
  role = db.Column(db.SmallInteger, default = ROLE_USER)
  posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
  about_me = db.Column(db.String(140))
  firstname = db.Column(db.String(40))
  lastname = db.Column(db.String(40))
  last_seen = db.Column(db.DateTime)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<User %r>' % (self.nickname)

  def avatar(self, size):
    return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

  @staticmethod
  def make_unique_nickname(nickname):
    if User.query.filter_by(nickname = nickname).first() == None:
      return nickname
    version = 2
    while True:
      new_nickname = nickname + str(version)
      if User.query.filter_by(nickname = new_nickname).first() == None:
        break
      version += 1
    return new_nickname

class Post(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  vote = db.Column(db.Integer, default = 1)

  def __repr__(self):
    return '<Post %r>' % (self.body)
  @staticmethod
  def upvote(pid):
    post = Post.query.filter_by(id = pid).first()
    post.vote += 1
    db.session.add(post)
    db.session.commit()
    return post.vote

  @staticmethod  
  def downvote(pid):
    post = Post.query.filter_by(id = pid).first()
    if post.vote > 0:
      post.vote -= 1
    db.session.add(post)
    db.session.commit()
    return post.vote