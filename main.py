# itlyavhtmkmcxdcm

from flask import Flask
from flask import render_template, request, redirect, session
import pymysql
import flask
import random
import string
from flask_mail import Mail


app = Flask(__name__)
app.secret_key = 'ihyfhbhbfrfbiihrewuibwe5436889'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='<email>',
    MAIL_PASSWORD='<password>'
)
mail = Mail(app)


# conn = pymysql.connect(host='localhost',
#                        user='root',
#                        password='',
#                        db='betterworld')


def connect_to_database():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='betterworld')
    return conn


def insert_data(data):
    conn = connect_to_database()
    cursor = conn.cursor()

    sql = "INSERT INTO user(name, user_name,email,phone,address,skills,password) VALUES (%s, %s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, data)

    conn.commit()

    cursor.close()
    conn.close()

# class User(db.Model):
#     # sno,title ,slug, centent,date
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50),nullable=False)
#     user_name = db.Column(db.String(50),nullable=False)
#     email  = db.Column(db.String(50),nullable=False)
#     phone  = db.Column(db.String(15),nullable=False)
#     address = db.Column(db.String,nullable=False)
#     skills = db.Column(db.String(30),nullable=False)
#     profile = db.Column(db.String(30),nullable=False)
#     password = db.Column(db.String(225),nullable=False)
#     date_time = db.Column(db.String(20),nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    page = 'false'
    page = request.args.get("account_created")
    if page == 'true':
        page = 'true'
    else:
        page = 'false'
    return render_template('index.html', page1=page)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/causes')
def causes():
    return render_template('causes.html')


@app.route('/donate')
def donate():
    return render_template('donate.html')


@app.route('/event')
def event():
    conn = pymysql.connect(host='localhost', user='root',
                           password='', db='betterworld')
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = "SELECT * FROM events"
    cursor.execute(sql)
    rows = cursor.fetchall()

    return render_template('event.html', rows1=rows)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login')
def login():
    return render_template('login.html')


#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50),nullable=False)
#     user_name = db.Column(db.String(50),nullable=False)
#     email  = db.Column(db.String(50),nullable=False)
#     phone  = db.Column(db.String(15),nullable=False)
#     address = db.Column(db.String,nullable=False)
#     skills = db.Column(db.String(30),nullable=False)
#     profile = db.Column(db.String(30),nullable=False)
#     password = db.Column(db.String(225),nullable=False)
#     date_time = db.Column(db.String(20),nullable=False)


@app.route('/sign_up')
def sign_up():

    return render_template('sign_up.html')


@app.route('/sign_user', methods=['GET', 'POST'])
def sign_user():
    if request.method == 'POST':
        letters = string.ascii_letters
        myrandomeword = ''.join(random.choice(letters) for i in range(15))
        print(myrandomeword)
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        skill = request.form.get('skill')
        password = request.form.get('password')
        data = (name, username, email, phone, address, skill, password)
        insert_data(data)

    return redirect('/?account_created=true')


@app.route('/sign_organization', methods=['GET', 'POST'])
def sign_organization():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        password = request.form.get('password')

        data = (name, email, phone, address, password)

        conn = pymysql.connect(host='localhost', user='root',
                               password='', db='betterworld')
        conn = connect_to_database()

        cursor = conn.cursor()
        sql = "INSERT INTO organization(name,email,phone,address, password) VALUES (%s, %s,%s,%s,%s)"
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        conn.close()
        mail.send_message('Organization Permisson', sender='assistbetterworld@gmail.com', recipients=['assistbetterworld@gmail.com'], body=" Give permission to organization " +
                          name + " the phone number is " + phone + " The address is " + address + " Give permission " + "http://127.0.0.1:5000/grant_permisson?name=" + name)

    return redirect('/?account_created=true')


@app.route('/grant_permisson')
def grant_permisson():
    params = request.args.get('name')
    print(params)
    conn = connect_to_database()
    cursor = conn.cursor()
    id = (params)
    sql = "UPDATE `organization` SET `admin` = 1 WHERE name=%s"
    cursor.execute(sql, id)

    conn.commit()

    cursor.close()
    conn.close()

    return render_template('grantpermissionsuccessfull.html', params1=params)


@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    conn = connect_to_database()
    cursor = conn.cursor()

    sql = "SELECT * FROM user WHERE email=%s AND password=%s"
    cursor.execute(sql, (email, password))
    result = cursor.fetchone()

    if result:
        # Create a session for the logged-in user
        session['email'] = email

        return redirect('/')
    else:
        return 'Invalid username or password'


@app.route('/user-admin', methods=['GET', 'POST'])
def user_admin():
    email = request.form['email']
    password = request.form['password']
    conn = connect_to_database()
    cursor = conn.cursor()

    sql = "SELECT * FROM organization WHERE email=%s AND password=%s"
    cursor.execute(sql, (email, password))
    result = cursor.fetchone()
    if result:
        if result[8] == 0:
            return render_template('access_denied.html')
        elif result[8] == 1:
            session['email'] = email

            return redirect('dashboard_admin')

    else:
        return redirect('sign_up')

    return redirect('login.html')


@app.route('/dashboard_admin', methods=['GET', 'POST'])
def dashboard_admin():
    if ((session['email'] != None) or (session['email'] != '')):
        conn = pymysql.connect(host='localhost', user='root',
                               password='', db='betterworld')
        conn = connect_to_database()
        cursor = conn.cursor()
        data = (session['email'])
        sql = "SELECT * FROM events WHERE copy_email=%s"
        cursor.execute(sql, data)
        rows = cursor.fetchall()

        conn = pymysql.connect(host='localhost', user='root',
                               password='', db='betterworld')
        conn = connect_to_database()
        cursor = conn.cursor()
        data = (session['email'])
        sql = "SELECT * FROM organization WHERE email=%s"
        cursor.execute(sql, data)
        organization_details = cursor.fetchone()

        if request.method == 'POST':
            title = request.form['title']
            date = request.form['date']
            time = request.form['time']
            venue = request.form['venue']
            description = request.form['description']
            skills = request.form['skills']
            name = request.form['name']

            data = (name, date, title, time, venue,
                    description, skills, session['email'])

            conn = pymysql.connect(
                host='localhost', user='root', password='', db='betterworld')
            conn = connect_to_database()

            cursor = conn.cursor()
            sql = "INSERT INTO events(organization,date, title,time, venue, description,skills,copy_email) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            conn = pymysql.connect(
                host='localhost', user='root', password='', db='betterworld')
            conn = connect_to_database()
            data = (session['email'])

            cursor = conn.cursor()
            sql = "SELECT * FROM events WHERE copy_email=%s"
            cursor.execute(sql, data)
            rows = cursor.fetchall()

            conn = pymysql.connect(
                host='localhost', user='root', password='', db='betterworld')
            conn = connect_to_database()
            data = (session['email'])

        return render_template('dashboard_admin.html', rows1=rows, organization_details1=organization_details)
    else:
        return render_template('login.html')



@app.route('/delete')
def delete():
    param1 = request.args.get('id')
    # param1 = request.form['id']

    conn = pymysql.connect(host='localhost', user='root',
                           password='', db='betterworld')
    conn = connect_to_database()
    data = (param1)

    cursor = conn.cursor()
    sql = "DELETE FROM `events` WHERE `id` = %s"
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

    return render_template('dashboard_admin.html')


# @app.route('/update', methods=['GET', 'POST'])
# def update():
#     conn = pymysql.connect(host='localhost', user='root',
#                                password='', db='betterworld')
#     conn = connect_to_database()
#     cursor = conn.cursor()
#     data = (session['email'])
#     sql = "SELECT * FROM organization WHERE email=%s"
#     cursor.execute(sql, data)
#     organization_details = cursor.fetchone()


#     if request.method == 'POST':
#         name = request.form['name']
#         phone = request.form['phone']
#         address = request.form['address']
#         conn = connect_to_database()
#         cursor = conn.cursor()
#         id = (name, phone, address, session['email'])
#         sql = "UPDATE `organization` SET `name` = %s, `phone` = %s ,`address` = %s WHERE email=%s"
#         cursor.execute(sql, id)

#         conn.commit()

#         cursor.close()
#         conn.close()

#     return render_template('/dashboard_admin')


@app.route('/logout')
def logout():
    session.pop("email", None)

    return redirect('/')


app.run(debug=True)
