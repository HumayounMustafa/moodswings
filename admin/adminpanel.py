from flask import Flask, request, jsonify, render_template, json, redirect
from flask_mongoengine import \
    MongoEngine  #>pip install flask-mongoengine
#from datetime import datetime

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'ProjectDB',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)


class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    password = db.StringField()
    #pub_date = db.DateTimeField(datetime.now)


@app.route('/')
def query_records():
    user = User.objects.all()
    return render_template('useradmin.html', user=user)


@app.route('/updateuser', methods=['POST'])
def updateuser():
    pk = request.form['pk']
    namepost = request.form['name']
    value = request.form['value']
    user_rs = User.objects(id=pk).first()
    if not user_rs:
        return json.dumps({'error': 'data not found'})
    else:
        if namepost == 'name':
            user_rs.update(name=value)
        elif namepost == 'email':
            user_rs.update(email=value)
        elif namepost == 'password':
            user_rs.update(password=value)
    return json.dumps({'status': 'OK'})


@app.route('/add', methods=['GET', 'POST'])
def create_record():
    txtname = request.form['txtname']
    txtemail = request.form['txtemail']
    txtpassword = request.form['txtpassword']
    usersave = User(name=txtname, email=txtemail, password=txtpassword,)
    usersave.save()
    return redirect('/')


@app.route('/delete/<string:getid>', methods = ['POST','GET'])
def delete_user(getid):
    print(getid)
    userrs = User.objects(id=getid).first()
    if not userrs:
        return jsonify({'error': 'data not found'})
    else:
        userrs.delete()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

