from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'

def connect_db():
    connect = sqlite3.connect('database.db')
    connect.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER primary key autoincrement, name TEXT, location TEXT)')
    connect.close()
   

def insert_db(name, location):
    connect = sqlite3.connect('database.db')
    connect.execute('''INSERT INTO users(name,location) VALUES (?, ?)''', [name, location])
    connect.commit()
    return connect



@app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def index(name):
    session['name'] = name
    return render_template('index.html', name=name, display=False, myList=[1,2,3,4], listOfDicts=[{'name': 'Zach'}, {'name':'Zoey'}])

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinSession!'
    return jsonify({'key' : 'value', 'key2' : [1,2], 'name' : name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>You are on {} page and his location is {}</h1>'.format(name,location)

@app.route('/theform', methods=['POST','GET'])
def theform():

    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        #location = request.form['location'] 
        #return '<h1>Hello, {} you are from {}. You submitted the form successfully!</h1>'.format(name, location)

        return redirect(url_for('index', name=name))

@app.route('/view')
def view():
    connect_db()
    connect = sqlite3.connect('database.db')
    connect = insert_db('P', 'FL')
    
    cursor = connect.execute("SELECT * FROM users")
    #cursor = connect.execute("Select id, name, location from users")
    
    result = cursor.fetchall()
    print(result)
    

    id = 0
    name = ''
    location =''
    for row in cursor:
        id = row[0]
        name = row[1]
        location = row[2]
    connect.close()
    return render_template('index.html', result=result)
    #return "{}, {}, {}".format(id, name, location)



     
'''
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return '<h1>Hello, {} you are from {}. You submitted the form successfully!</h1>'.format(name, location)
'''