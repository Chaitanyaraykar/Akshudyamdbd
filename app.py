# app.py
from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'chaitanyakr'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '9036744461'
app.config['MYSQL_DATABASE_DB'] = 'flasksql'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


class RLocation:
    def __init__(self, key, name, lat, lng):
        self.key = key
        self.name = name
        self.lat = lat
        self.lng = lng


class OLocation():
    def __init__(self, key, name, lat, lng, contact):
        self.key = key
        self.name = name
        self.lat = lat
        self.lng = lng
        self.contact = contact


class PLocation():
    def __init__(self, key, name, lat, lng, contact, foodq):
        self.key = key
        self.name = name
        self.lat = lat
        self.lng = lng
        self.contact = contact
        self.foodq = foodq


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
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

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

    # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts (fullname, username, password, email, gender, dateofbirth) VALUES(%s, %s, %s, %s, %s,%s)',
                           (fullname, username, password, email, gender, dateofbirth))
            conn.commit()

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
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

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
        elif not re.match(r'[0-9]+.[0-9]+', olocationlong):
            msg = 'longitude should be decimal!'
        elif not re.match(r'[0-9]+.[0-9]+', olocationlat):
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
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

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
        elif not re.match(r'[0-9]+.[0-9]+', plocationlong):
            msg = 'longitude should be decimal!'
        elif not re.match(r'[0-9]+.[0-9]+', plocationlat):
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
            if not re.match(r'[0-9]+.[0-9]+', rloclong):
                msg = 'longitude should be decimal!'
            elif not re.match(r'[0-9]+.[0-9]+', rlocationlat):
                msg = 'latitude should be decimal!'
            else:
                cursor.execute(
                    'INSERT INTO receiver (RECEIVERLAT,RECEIVERLONG,NAME) VALUES(%s,%s,%s)', (rlocationlat, rloclong, rname))
                conn.commit()

        return render_template('home.html', username=session['username'])

    if 'loggedin' in session and session.get('person') == 'orphanage':
        return render_template('orphanagehome.html', username=session['username'])

    if 'loggedin' in session and session.get('person') == 'producer':
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        msg = ''
        # User is loggedin show them the home page
        if request.method == 'POST' and 'foodquantity' in request.form:
            # Create variables for easy access
            foodq = request.form['foodquantity']
            pid = session['vid']
            if not re.match(r'[0-9]+', foodq):
                msg = 'Food quantiy should be number in kgs!'
            else:
                cursor.execute(
                    'UPDATE producer SET foodquantity = %s WHERE pid = %s', (foodq, pid))
                conn.commit()
        return render_template('producerhome.html', username=session['username'])
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


@app.route("/informer")
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
        if not re.match(r'[0-9]+.[0-9]+', rloclong):
            msg = 'longitude should besdecimal!'
        elif not re.match(r'[0-9]+.[0-9]+', rlocationlat):
            msg = 'latitude should be decimal!'
        else:
            cursor.execute('INSERT INTO receiver (RECEIVERLAT,RECEIVERLONG,NAME) VALUES(%s,%s,%s)', (rlocationlat, rloclong, rname))
            conn.commit()
    return render_template('informer.html', msg=msg)

# @app.route("/recivers")
# def index():
#     return render_template('reciver.html', schools=schools)


@app.route("/<school_code>")
def show_school(school_code):
    location_by_key = fetchalllist()
    location = location_by_key.get(school_code)
    if location:
        return render_template('map.html', school=location)
    else:
        return redirect(url_for('profile'))

# @app.route("/<orphan_code>")
# def show_orphanage(orphan_code):
#     recivers,location_by_key = fetchorphanage()
#     orphanageloc = location_by_key.get(orphan_code)
#     if orphanageloc:
#         return render_template('map.html', school=orphanageloc)
#     else:
#         return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
