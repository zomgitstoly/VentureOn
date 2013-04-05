from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, EditForm
from app import app, db, lm, oid
from models import User, ROLE_USER, ROLE_ADMIN, Post
from datetime import datetime


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
  user = g.user
  posts = Post.query.order_by(Post.vote.desc())
  return render_template("index.html",
    title = 'Home',
    user = user,
    posts = posts)

@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
  return render_template("login.html",
		title = 'Sign In',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
  user = User.query.filter_by(nickname = nickname).first()
  if user is None:
    flash("User " + nickname + " is not found")
    redirect(url_for('index'))
  posts = Post.query.filter_by(author = user).all()
  return render_template("user.html",
    user = user,
    posts = posts)

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@oid.after_login
def after_login(resp):
  if resp.email is None or resp.email == "":
    flash("Invalid login. Please try again")
    redirect(url_for('login'))
  user = User.query.filter_by(email = resp.email).first()
  if user is None:
    nickname = resp.nickname
    if nickname is None or nickname == "":
      nickname = resp.email.split('@')[0]
    nickname = User.make_unique_nickname(resp.nickname)
    user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('edit'))
  remember_me = False
  if 'remember_me' in session:
    remember_me = session['remember_me']
    session.pop('remember_me', None)
  login_user(user, remember = remember_me)
  return redirect(request.args.get('next') or url_for('index'))

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
  form = EditForm(g.user.nickname)
  if form.validate_on_submit():
    g.user.nickname = form.nickname.data
    g.user.about_me = form.about_me.data
    g.user.firstname = form.firstname.data
    g.user.lastname = form.lastname.data
    db.session.add(g.user)
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('edit'))
  else:
    form.nickname.data = g.user.nickname
    form.about_me.data = g.user.about_me
    form.firstname.data = g.user.firstname
    form.lastname.data = g.user.lastname
  return render_template('edit.html',
    form = form)  

@app.route('/vote', methods = ['POST'])
@login_required
def vote():
  direction = request.form['direction']
  postId = request.form['postId']
  newVote = 0
  if (direction == 'up'):
    newVote = Post.upvote(int(postId))
  elif (direction == 'down'):
    newVote = Post.downvote(int(postId))
  return str(newVote)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
      g.user.last_seen = datetime.utcnow()
      db.session.add(g.user)
      db.session.commit()

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
