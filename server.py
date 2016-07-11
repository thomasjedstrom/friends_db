from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app, 'friendsdb')

@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    filename = 'static/img/friends.png'
    return render_template('index.html', all_friends=friends, filename=filename)

@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    data = {
             'first_name': request.form['first_name'], 
             'last_name':  request.form['last_name'],
             'email': request.form['email']
           }
    mysql.query_db(query, data)
    flash(u"User " + data['first_name'] + " " + data['last_name'] + " has been ADDED in the database", 'success')
    return redirect('/')

@app.route('/friends/<friend_id>/edit', methods=['GET', 'POST'])
def edit(friend_id):
    query = "SELECT * FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    friends = mysql.query_db(query, data)
    return render_template('edit.html', all_friends=friends)

@app.route('/friends/<friend_id>', methods=['GET', 'POST'])
def update(friend_id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id = :id"
    data = {
             'first_name': request.form['first_name'], 
             'last_name':  request.form['last_name'],
             'email': request.form['email'],
             'id': friend_id
           }
    mysql.query_db(query, data)
    flash(u"User " + friend_id + " has been UPDATED in the database", 'success')
    return redirect('/')

@app.route('/friends/<friend_id>/delete', methods=['POST'])
def delete(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    flash(u"User " + friend_id + " has been DELETED from the database", 'error')
    return redirect('/')


app.run(debug=True)