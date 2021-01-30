from flask import Flask, jsonify, request, redirect, session, render_template, url_for
from flask_mail import Mail, Message
import uuid
from app import db, serializer, mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


class User:
    def start_session(self, user):
        session['logged_in'] = True
       # session['username']= user.name
        session['role']= 'user'
        session['user']= user
        return render_template('profile.html')

    def signup(self):

        user = {
            "_id" : uuid.uuid4().hex,
            "name" : request.form.get('username'),
            "email" : request.form.get('email'),
            "password" : request.form.get('password')
        }

        #check for duplicate user
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email already exists"}), 400

        if db.users.insert_one(user):
            return self.start_session(user)
    def signout(self):
        session.clear()
        return redirect('/user/login')

    def sendEmail(self):
        email =  request.form.get('email')
        token = serializer.dumps(email, salt='email-confirm')
        msg = Message('Confirm Email To Reset Password', sender='projectmoodswings@gmail.com', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = 'Kindly follow the link to change your password {}'.format(link)
        
        mail.send(msg)

        return 'Kindly check your email <strong>{}</strong> to continue...'.format(email)

    def set_password(self, token):
        try:
            email = serializer.loads(token, salt='email-confirm', max_age=36000)
        except SignatureExpired:
            return '<h1>The token is expired!</h1>'
        user = db.users.find_one({'email': email})
        return render_template('reset_password.html', email=email)

    def login(self):
        user= db.users.find_one({'email':request.form.get('username'),'password':request.form.get('password')})
        if user:
            return self.start_session(user)
        return "Invalid username or password"

    def change_password(self):
        email =  request.form.get('email')
        password = request.form.get('password')
        try:
            user = db["users"].find_one({'email': email})
            user["password"] = password
            updated = db["users"].save(user)
        except SignatureExpired:
            return '<h1>An Error has occured</h1>'

        return redirect('/user/login')    
    