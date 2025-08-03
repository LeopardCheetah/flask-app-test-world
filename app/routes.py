from flask import render_template, flash, redirect, url_for, request

from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa 

from app.models import User 
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditAboutMeForm

from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': db.first_or_404(sa.select(User).where(User.username == 'admin')),
            'body': 'Beautiful day at Nettlecombe today!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


# updated login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))

        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password :(')
            return redirect(url_for('login'))
        
        login_user(user, remember=False)
        next_page = request.args.get('next')
        # second check is to make sure the path given is "relative"
        # against adversarial attacks
        if not next_page or urlsplit(next_page).netloc != '':
            # basic
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# ok but what if you wanted to leave
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you have now signed up!')
        return redirect(url_for('login'))
    
    return render_template('signup.html', title='Sign Up!', form=form)


@app.route('/edit_about_me', methods=['GET', 'POST'])
@login_required
def edit_about_me():
    form = EditAboutMeForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your about me changes have been saved.')
        # go back to index
        return redirect(url_for('index'))
        
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_about_me.html', title='Edit About Me',form=form)


# do something something here about being able to change their own little description/picture
# @app.route('/people/<username>')

# build a page to maybe list all the people
# @app.route('/people')

@app.route('/people/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)












@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html', title='SECRET!')

