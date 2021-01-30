from flask import Flask, render_template, session, redirect
from functools import wraps
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import pymongo

app = Flask(__name__)
#app.config.from_pyfile('config.cfg')
app.secret_key='12345'


mail = Mail(app)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'projectmoodswings@gmail.com'
app.config['MAIL_PASSWORD'] = 'Moodswings@1'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])



#msg = Message()
#msg.subject = "Email Subject"
#msg.recipients = ['alishahkhan943@gmail.com']
#msg.sender = 'projectmoodswings@gmail.com'
#msg.body = 'Email body'mail.send(msg)
#Thread(target=send_email, args=(app, msg)).start()

#Database configuration
client = pymongo.MongoClient('localhost', 27017)
db = client.moodswings

#Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kargs):
    if 'logged_in' in session:
      return f(*args, **kargs)
    else:
      return redirect('/user/login')
  return  wrap


def admin_login_required(f):
  @wraps(f)
  def wrap(*args, **kargs):
    if 'logged_in' in session and session['role'] == 'Admin':
      return f(*args, **kargs)
    else:
      return redirect('/admin/login')
  return  wrap

from user import routes
from admin import routes


@app.route('/')
def index():
    return render_template('index.html')




