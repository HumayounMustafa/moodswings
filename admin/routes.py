from flask import Flask, render_template
from app import app
from admin.models import Admin
from app import admin_login_required


@app.route('/admin/signout', methods=['GET'])
def signoutAdmin():
    return Admin().signout()

@app.route('/admin/login',  methods=['GET'])
def loginAdmin():
    return render_template('adminlogin.html')

@app.route('/admin/login',  methods=['POST'])
def loginPostAdmin():
    return Admin().login()


@app.route('/admin/profile')
@admin_login_required
def profileAdmin():
    return render_template('AdminProfile.html')
