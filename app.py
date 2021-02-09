# app.py
from flask import Flask, request, session, redirect, url_for, render_template,make_response
from flaskext.mysql import MySQL
import pymysql
import re
from user.models import RLocation, OLocation, PLocation
import pymongo
import uuid
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pdfkit
import math
# import pbkdf2_sha256.encrypt()
#from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'chaitanyakr1'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '9036744461'
app.config['MYSQL_DATABASE_DB'] = 'flasksql'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

client = pymongo.MongoClient('localhost', 27017)
db = client.dbddatabase
# class RLocation:
#     def __init__(self, key, name, lat, lng):
#         self.key = key
#         self.name = name
#         self.lat = lat
#         self.lng = lng


# class OLocation():
#     def __init__(self, key, name, lat, lng, contact):
#         self.key = key
#         self.name = name
#         self.lat = lat
#         self.lng = lng
#         self.contact = contact


# class PLocation():
#     def __init__(self, key, name, lat, lng, contact, foodq):
#         self.key = key
#         self.name = name
#         self.lat = lat
#         self.lng = lng
#         self.contact = contact
#         self.foodq = foodq


def fetchreceiver():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from receiver')
    recivers = cursor.fetchall()

    # schools = (
    #     Schools('helo' ,  reciver['name']  ,float(reciver['receiverlat']), float(reciver['receiverlong'])),
    #     Schools('stanley', 'Stanley Middle',            37.8884474, -122.1155922),
    #     Schools('wci',     'Walnut Creek Intermediate', 37.9093673, -122.0580063)
    # )
    rlocations = ()
    for reciver in recivers:
        rlocations = rlocations + (RLocation(str(reciver['rid']),  reciver['NAME'], float(
            reciver['RECEIVERLAT']), float(reciver['RECEIVERLONG'])),)
    # float(reciver['receiverlat']), float(reciver['receiverlong'])

    return rlocations


def fetchorphanage():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from orphanage')
    orphanages = cursor.fetchall()

    # schools = (
    #     Schools('helo' ,  reciver['name']  ,float(reciver['receiverlat']), float(reciver['receiverlong'])),
    #     Schools('stanley', 'Stanley Middle',            37.8884474, -122.1155922),
    #     Schools('wci',     'Walnut Creek Intermediate', 37.9093673, -122.0580063)
    # )
    olocations = ()
    for orphanage in orphanages:
        olocations = olocations + (OLocation(str(orphanage['oid']), orphanage['oname'], float(
            orphanage['orphanagelat']), float(orphanage['orphanagelong']), orphanage['ocontact']), )
    # float(reciver['receiverlat']), float(reciver['receiverlong'])

    return olocations


def fetchproducer():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from producer')
    producers = cursor.fetchall()

    # schools = (
    #     Schools('helo' ,  reciver['name']  ,float(reciver['receiverlat']), float(reciver['receiverlong'])),
    #     Schools('stanley', 'Stanley Middle',            37.8884474, -122.1155922),
    #     Schools('wci',     'Walnut Creek Intermediate', 37.9093673, -122.0580063)
    # )
    plocations = ()
    for producer in producers:
        plocations = plocations + (PLocation(str(producer['pid']), producer['pname'], float(
            producer['platitude']), float(producer['plongitude']), producer['pcontact'], producer['foodquantity']), )
    # float(reciver['receiverlat']), float(reciver['receiverlong'])

    return plocations


def fetchalllist():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from receiver')
    recivers = cursor.fetchall()
    cursor.execute('select * from orphanage')
    orphanages = cursor.fetchall()
    cursor.execute('select * from producer')
    producers = cursor.fetchall()

    rlocations = ()
    for orphanage in orphanages:
        rlocations = rlocations + (OLocation(str(orphanage['oid']), orphanage['oname'], float(
            orphanage['orphanagelat']), float(orphanage['orphanagelong']), orphanage['ocontact']), )
    # float(reciver['receiverlat']), float(reciver['receiverlong'])
    for reciver in recivers:
        rlocations = rlocations + (RLocation(str(reciver['rid']),  reciver['NAME'], float(
            reciver['RECEIVERLAT']), float(reciver['RECEIVERLAT'])),)
    # float(reciver['receiverlat']), float(reciver['receiverlong'])
    for producer in producers:
        rlocations = rlocations + (PLocation(str(producer['pid']), producer['pname'], float(
            producer['platitude']), float(producer['plongitude']), producer['pcontact'], producer['foodquantity']), )
    # float(reciver['receiverlat']), float(reciver['receiverlong'])

    location_by_key = {orphan.key: orphan for orphan in rlocations}
    return location_by_key


# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        #check_password_hash(passwordfromsql,passwordentered)
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['person'] = 'volunteer'
            session['vid'] = account['vid']
            session['username'] = account['username']
            session['contact'] = account['email']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Account doesn\'t exist or Incorrect username/password!'

    return render_template('index.html', msg=msg)

# http://localhost:5000/register - this will be the registration page


@app.route('/register', methods=['GET', 'POST'])
def register():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        dateofbirth = request.form['dateofbirth']
        gender = request.form['gender']
        #hashedpassword = generate_password_hash(password,method='sha256')
    # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[A-Za-z]+', fullname):
            msg = 'Username must contain only characters'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts (fullname, username, password, email, gender, dateofbirth) VALUES(%s, %s, %s, %s, %s,%s)',
                           (fullname, username, password, email, gender, dateofbirth))
            conn.commit()
        #hashedpassword = generate_password_hash(password,method='sha256')
        #check_password_hash(passwordfromsql,passwordentered) use this condition to check if the password is correct or not in login system
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/orphanagelogin/', methods=['GET', 'POST'])
def ologin():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'oname' in request.form and 'opassword' in request.form:
        # Create variables for easy access
        username = request.form['oname']
        password = request.form['opassword']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM orphanage WHERE oname = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['person'] = 'orphanage'
            session['vid'] = account['oid']
            session['username'] = account['oname']
            session['contact'] = account['ocontact']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Account doesn\'t exist or Incorrect username/password!'

    return render_template('ologin.html', msg=msg)

# http://localhost:5000/register - this will be the registration page


@app.route('/oregister', methods=['GET', 'POST'])
def oregister():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'oname' in request.form and 'opassword' in request.form and 'ocontact' in request.form:
        # Create variables for easy access
        oname = request.form['oname']
        password = request.form['opassword']
        contact = request.form['ocontact']
        olocationlat = request.form['ollt']
        olocationlong = request.form['ollg']

    # Check if account exists using MySQL
        cursor.execute('SELECT * FROM orphanage WHERE oname = %s', (oname))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', oname):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$', olocationlong):
            msg = 'longitude should be decimal!'
        elif not re.match(r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$', olocationlat):
            msg = 'latitude should be decimal!'
        elif not re.match(r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}', contact):
            msg = 'give valid contact!'
        elif not oname or not password or not contact or not olocationlat or not olocationlong:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO orphanage (oname, password, ocontact, orphanagelat, orphanagelong) VALUES( %s, %s, %s, %s,%s)',
                           (oname, password, contact, olocationlat, olocationlong))
            conn.commit()

            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('oregister.html', msgo=msg)


# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/producerlogin/', methods=['GET', 'POST'])
def plogin():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'pname' in request.form and 'ppassword' in request.form:
        # Create variables for easy access
        username = request.form['pname']
        password = request.form['ppassword']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM producer WHERE pname = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['person'] = 'producer'
            session['vid'] = account['pid']
            session['username'] = account['pname']
            session['contact'] = account['pcontact']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Account doesn\'t exist or Incorrect username/password!'

    return render_template('plogin.html', msg=msg)

# http://localhost:5000/register - this will be the registration page


@app.route('/pregister', methods=['GET', 'POST'])
def pregister():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'pname' in request.form and 'ppassword' in request.form and 'pcontact' in request.form:
        # Create variables for easy access
        pname = request.form['pname']
        password = request.form['ppassword']
        contact = request.form['pcontact']
        plocationlat = request.form['pllt']
        plocationlong = request.form['pllg']

    # Check if account exists using MySQL
        cursor.execute('SELECT * FROM producer WHERE pname = %s', (pname))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', pname):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$', plocationlong):
            msg = 'longitude should be decimal!'
        elif not re.match(r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$', plocationlat):
            msg = 'latitude should be decimal!'
        elif not re.match(r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}', contact):
            msg = 'give valid contact!'
        elif not pname or not password or not contact or not plocationlat or not plocationlong:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO producer (pname, password, pcontact, platitude, plongitude) VALUES( %s, %s, %s, %s,%s)',
                           (pname, password, contact, plocationlat, plocationlong))
            conn.commit()

            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('pregister.html', msgp=msg)


# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session and session.get('person') == 'volunteer':
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        msg = ''
        # User is loggedin show them the home page
        if request.method == 'POST' and 'Receivername' in request.form and 'rllt' in request.form and 'rllg' in request.form:
            # Create variables for easy access
            rname = request.form['Receivername']
            rlocationlat = request.form['rllt']
            rloclong = request.form['rllg']

            if not re.match(r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$', rloclong):
                msg = 'Enter a valid longitude!'
            elif not re.match(r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$', rlocationlat):
                msg = 'Enter a valid latitude!'
            else:
                cursor.execute(
                    'INSERT INTO receiver (RECEIVERLAT,RECEIVERLONG,NAME) VALUES(%s,%s,%s)', (rlocationlat, rloclong, rname))
                conn.commit()

        return render_template('home.html', username=session,msg=msg)

    if 'loggedin' in session and session.get('person') == 'orphanage':
        return render_template('orphanagehome.html', username=session)

    if 'loggedin' in session and session.get('person') == 'producer':
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        msg = ''
        # User is loggedin show them the home page
        if request.method == 'POST' and 'foodquantity' in request.form and 'foodtype' in request.form:
            # Create variables for easy access
            foodq = request.form['foodquantity']
            foodtype = request.form['foodtype']
            pid = session['vid']
            if not re.match(r'[0-9]+', foodq):
                msg = 'Food quantiy should be number in kgs!'
            elif not re.match(r'[qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM]+',foodtype):
                msg = 'Enter a valid food type'
            else:
                msg = "Entered successfully"
                cursor.execute(
                    'UPDATE producer SET foodquantity = %s WHERE pid = %s', (foodq, pid))
                cursor.execute(
                    'UPDATE producer SET itemname = %s WHERE pid = %s', (foodtype, pid))
                conn.commit()
        return render_template('producerhome.html', username=session,msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/logout - this will be the logout page


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('vid', None)
    session.pop('username', None)
    session.pop('person', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users


@app.route('/profile')
def profile():
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session and session.get('person') == 'volunteer':
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accounts WHERE vid = %s',
                       [session['vid']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)

    if 'loggedin' in session and session.get('person') == 'orphanage':
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM orphanage WHERE oid = %s',
                       [session['vid']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('oprofile.html', account=account)

    if 'loggedin' in session and session.get('person') == 'producer':
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM producer WHERE pid = %s',
                       [session['vid']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('pprofile.html', account=account)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/recivers')
def recivers():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        # cursor.execute('SELECT * FROM accounts')
        # recivers = cursor.fetch()
        rlocations = fetchreceiver()
        return render_template('reciver.html', schools=rlocations)
        # return render_template('reciver.html',recivers = recivers)
    return redirect(url_for('login'))


@app.route("/orphanage")
def orphanage():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        # cursor.execute('SELECT * FROM accounts')
        # recivers = cursor.fetch()
        olocations = fetchorphanage()
        return render_template('orphanage.html', orphanage=olocations)
        # return render_template('reciver.html',recivers = recivers)
    return redirect(url_for('login'))


@app.route("/producer")
def producer():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        # cursor.execute('SELECT * FROM accounts')
        # recivers = cursor.fetch()
        plocations = fetchproducer()
        return render_template('producer.html', producers=plocations)
        # return render_template('reciver.html',recivers = recivers)
    return redirect(url_for('login'))


@app.route("/inform", methods=['GET', 'POST'])
def inform():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    # User is loggedin show them the home page
    if request.method == 'POST' and 'Receivername' in request.form and 'rllt' in request.form and 'rllg' in request.form:
        # Create variables for easy access
        rname = request.form['Receivername']
        rlocationlat = request.form['rllt']
        rloclong = request.form['rllg']
        if not re.match(r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$', rloclong):
            msg = 'longitude should besdecimal!'
        elif not re.match(r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$', rlocationlat):
            msg = 'latitude should be decimal!'
        elif not re.match(r'[qwertyuiopsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM]+', rname):
            msg = 'Username must contain only characters'
        else:
            cursor.execute(
                'INSERT INTO receiver (RECEIVERLAT,RECEIVERLONG,NAME) VALUES(%s,%s,%s)', (rlocationlat, rloclong, rname))
            conn.commit()
    return render_template('informer.html', msg=msg)

# @app.route("/recivers")
# def index():
#     return render_template('reciver.html', schools=schools)


@app.route("/<school_code>", methods=['GET', 'POST'])
def show_school(school_code):
    location_by_key = fetchalllist()
    location = location_by_key.get(school_code)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ""
    safety = 0
    if location:
        if int(school_code)< 8000 or int(school_code)>=15000 :
            if request.method == 'POST' and 'deletereceiver' in request.form:
                deletereceiver = request.form['deletereceiver']
                if deletereceiver == '1':
                    if int(school_code) < 8000:
                        cursor.execute('delete from receiver where rid = %s',int(school_code))
                        conn.commit()
                    elif int(school_code) >14999:
                        redirect(url_for('profile'))
                return redirect(url_for('profile'))
            return render_template('mapreceiver.html', school=location)
        else:
            if request.method == 'POST' and 'deletepvrecord' in request.form and 'safetycheck' in request.form and "quantityoffood" in request.form:
                safetycheck = request.form['safetycheck']
                foodcollected = request.form['deletepvrecord']
                pid = school_code
                vid = session['vid']
                foodquantity = request.form['quantityoffood']
                cursor.execute('select foodquantity from producer where pid = %s',(pid))
                currentfq = cursor.fetchone()
                currentfq = currentfq['foodquantity']
                if int(foodquantity) < int(currentfq):
                    msg = "Food collected is more than what is present"
                    return redirect(url_for('profile'))
                if safetycheck == 'true':
                    safety = 1
                    cursor.execute('select pid from pvtable where pid = %s and vid = %s',(pid,vid))
                    pvtrans1 = cursor.fetchone()
                    cursor.execute('select pid from optable where pid = %s and oid = %s',(pid,vid))
                    pvtrans2 = cursor.fetchone()
                    pvtrans = pvtrans1 or pvtrans2
                    if not pvtrans:
                        if session['person'] == 'orphanage':
                            cursor.execute('INSERT INTO optable (pid,oid,isSafetyo) VALUES(%s,%s,%s)', (pid, vid, safety))
                            msg = "database updated successfully"
                            conn.commit()
                        else:
                            cursor.execute('INSERT INTO pvtable (Pid,Vid,isSafety) VALUES(%s,%s,%s)', (pid, vid, safety))
                            msg = "database updated successfully"
                            conn.commit()
                    else:
                        cursor.execute('update pvtable set count = count + 1 where pid = %s and vid = %s',(pid,vid))
                        conn.commit()
                if safetycheck == 'false':
                    safety = 0
                    cursor.execute('select pid from pvtable where pid = %s and vid = %s',(pid,vid))
                    pvtrans1 = cursor.fetchone()
                    cursor.execute('select pid from optable where pid = %s and oid = %s',(pid,vid))
                    pvtrans2 = cursor.fetchone()
                    pvtrans = pvtrans1 or pvtrans2
                    if not pvtrans:
                        if session['person'] == 'orphanage':
                            cursor.execute('INSERT INTO optable (pid,oid,isSafetyo) VALUES(%s,%s,%s)', (pid, vid, safety))
                            msg = "database updated successfully"
                            conn.commit()
                        else:
                            cursor.execute('INSERT INTO pvtable (Pid,Vid,isSafety) VALUES(%s,%s,%s)', (pid, vid, safety))
                            msg = "database updated successfully"
                            conn.commit()
                    else:
                        if session['person'] == 'orphanage':
                            cursor.execute('update optable set count = count + 1 where pid = %s and oid = %s',(pid,vid))
                            conn.commit()
                        else:   
                            cursor.execute('update pvtable set count = count + 1 where pid = %s and vid = %s',(pid,vid))
                            conn.commit()
                if foodcollected == '1':
                    if session['person'] == 'volunteer':
                        cursor.execute(
                            'update accounts set credits = credits + 1 where vid = %s',(session['vid']))
                        conn.commit() 
                    cursor.execute("select pname from producer where pid = %s", (pid))
                    pname = cursor.fetchone()
                    pname = pname['pname']
                    cursor.execute("update producer set foodquantity = foodquantity - %s where pid = %s", (foodquantity, pid))
                    conn.commit()
                    # write a mongo code to make volunteer list in data base where it has his name, credit,contactno, list of producers with safe or not
                    # fetch_one(volunteer.vid) if exist then add producer to the producer list or add new volunteer
                    # add total
                    
                    pvtabledict = {"_id": uuid.uuid4().hex,
                        "vid": session['vid'],
                        "volunteer name":  session['username'],
                        "type of user": session['person'],
                        "contact": session['contact'],
                        
                             "producerarr": {"pid": pid,
                                            "producername": pname,
                                            "quantity of food": foodquantity,
                                            "isFoodsafe": safety}
                        
                    }
                    db.pvtable.insert_one(pvtabledict)
                    redirect(url_for('recivers'))
                    # volunteer = {"_id":vid,
                    #  "volunteer name" : "",
                    #  "type of user":"volunteer/orphanage",
                    #  "contact":"email/phonenumber"
                    # ,producers=[{"pid":"",
                    #               "producername":"",
                    #           "quantity of food":"",
                    #           "isFoodsafe":Bollean},]}
                    # add a admin account with all the list of recivers,volunteers ,producers,orphanages,
                    # report of a volunteer for every volunteer
                    # ,report of total food,
                    # report of all producers with total food provided
                    # add total food column in producer and add food to that when it is collected by orphanage or
            redirect(url_for('recivers'))
            return render_template('map.html', school=location , msg = msg)
    else:
        return redirect(url_for('profile'))


# @app.route("/show_school/<school_code>")
# def show_school(school_code):
#     location_by_key = fetchalllist()
#     location = location_by_key.get(school_code)
#     conn = mysql.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     msg = ""
#     if location:
#         if request.method == 'POST' and 'deletepvrecord' in request.form and 'safetycheckt' in request.form and 'safetycheckf' in request.form :
#             safetycheckt = request.form['safetycheckt']
#             safetycheckf = request.form['safetycheckf']
#             foodcollected = request.form['deletepvrecord']
#             pid = school_code
#             vid = session['vid']
#             if safetycheckt=='true':
#                 cursor.execute('INSERT INTO pvtable (Pid,Vid,isSafety) VALUES(%s,%s,%s)', (pid, vid, safetycheckt))
#                 msg = "database updated successfully"
#                 conn.commit()
#             if safetycheckf=='false':
#                 cursor.execute('INSERT INTO pvtable (Pid,Vid,isSafety) VALUES(%s,%s,%s)', (pid, vid, safetycheckf))
#                 msg = "database updated successfully"
#                 conn.commit()
#             if foodcollected == 'true':
#                 cursor.execute('DELETE FROM pvtable WHERE Pid = %s AND Vid = %s',(pid,vid))
#             conn.commit()


#         return render_template('map.html', school=location )
#     else:
#         return redirect(url_for('profile'))

# @app.route("/<orphan_code>")
# def show_orphanage(orphan_code):
#     recivers,location_by_key = fetchorphanage()
#     orphanageloc = location_by_key.get(orphan_code)
#     if orphanageloc:
#         return render_template('map.html', school=orphanageloc)
#     else:
#         return redirect(url_for('home'))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        if request.method == 'POST' and 'feedback' in request.form:
            # Create variables for easy access
            rname = request.form['feedback']
            nltk.downloader.download('vader_lexicon')
            feedbackofuser = rname
            sid = SentimentIntensityAnalyzer()
            ss = sid.polarity_scores(rname)
            feedbackdict = {}
            for k in ss:
                feedbackdict[k] = ss[k]
            feedbackdicttotal = {}
            feedbackdicttotal = {
                "_id": uuid.uuid4().hex,
                "user": session['username'],
                "userType": session['person'],
                "feedback": feedbackofuser,
                "feedbacksentiment": feedbackdict
            }
            db.userfeedback.insert_one(feedbackdicttotal)

        return render_template('feedback.html', usertype=session['person'])


@app.route("/adminreport",methods=['GET','POST'])
def adminreport():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select count(pid) from producer")
    producercount = cursor.fetchone()
    producercount = producercount['count(pid)']
    cursor.execute("select count(vid) from accounts")
    volunteercount = cursor.fetchone()
    volunteercount = volunteercount['count(vid)']
    cursor.execute("select count(oid) from orphanage")
    orphanagecount = cursor.fetchone()
    orphanagecount = orphanagecount['count(oid)']
    olocations = fetchorphanage()
    cursor.execute("select sum(count) from pvtable")
    pvcount = cursor.fetchone()
    pvcount1 = pvcount['sum(count)']
    return render_template('adminreport1.html', orphanage=olocations,pc = producercount,vc = volunteercount,oc = orphanagecount, pv = pvcount1)
    # pdf = pdfkit.from_string(rendered,False)
    # response = make_response(pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    


@app.route('/admin',methods=['GET','POST'])
def adminpage():
    msg = ""
    if request.method == 'POST' and 'password' in request.form:
        password = request.form['password']
        if password == '1234567890' :
            msg = 'Go to /adminreport'
        else:
            msg = "Incorrect Password"

    return render_template('admin.html',msg = msg)



@app.route("/adminreportpdf")
def adminreportpdf():
    rendered = adminreport()
    pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        if request.method == 'POST' and 'blog' in request.form and 'title' in request.form:
            # Create variables for easy access
            blogofuser = request.form['blog']
            title = request.form['title']
            blogdicttotal = {}
            blogdicttotal = {
                "_id": uuid.uuid4().hex,
                "user": session['username'],
                "title": title,
                "blog": blogofuser
            }
            db.userblog.insert_one(blogdicttotal)
        allblogs = list(db.userblog.find())
        # for doc in allblogs:
        #     bloglist = doc['blog']

        return render_template('blog.html', usertype=session['person'], blogs = allblogs)

if __name__ == '__main__':
    app.run(debug=True)
