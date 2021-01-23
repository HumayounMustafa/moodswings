from flask import Flask, render_template
from app import app
from user.models import User
from app import login_required

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


@app.route('/user/signup', methods=['GET'])
def signupGet():
    return render_template('signup.html')

@app.route('/user/signout', methods=['GET'])
def signout():
    return User().signout()

@app.route('/user/login',  methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/user/login',  methods=['POST'])
def loginPost():
    return User().login()


@app.route('/user/profile')
@login_required
def profile():
    return render_template('profile.html')
