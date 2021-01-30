from flask import Flask, render_template, request
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

@app.route('/user/forget_password')
def forget_password():
    return render_template('forget password.html')


@app.route('/user/reset_email', methods=['POST'])
def send_email():
    return User().sendEmail()


@app.route('/user/confirm_email/<token>')
def confirm_email(token):
    return User().set_password(token)

@app.route('/user/reset_password', methods=['POST'])
def reset_password():
    return User().change_password()
