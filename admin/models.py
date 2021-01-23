from flask import Flask, jsonify, request, redirect, session, render_template
import uuid
from app import db


class Admin:
    def start_session(self, admin):
        session['logged_in'] = True
       # session['username']= user.name
        session['role']= 'Admin'
        session['admin']= admin
        return render_template('AdminProfile.html')

    def signout(self):
        session.clear()
        return redirect('/admin/login')

    def login(self):
        admin=  db.admins.find_one({'email':request.form.get('adminname'),'password':request.form.get('password')})
       # return jsonify(admin)
        if admin:
            return self.start_session(admin)
        return "Invalid username or password"