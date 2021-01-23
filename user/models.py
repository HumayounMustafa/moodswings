from flask import Flask, jsonify, request, redirect, session, render_template
import uuid
from app import db


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

    def login(self):
        user= db.users.find_one({'email':request.form.get('username'),'password':request.form.get('password')})
        if user:
            return self.start_session(user)
        return "Invalid username or password"
