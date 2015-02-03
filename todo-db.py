from flask import Flask, request, redirect, url_for, g
import sqlite3
app = Flask(__name__)

dbFile = 'c410-lab4-todo.db'
tasks = []

def get_conn():
	conn = getattr(g, 'dbFile', None)
	if conn is None:
		conn = g.dbFile = sqlite3.connect(dbFile) 		# remember to set g obj!
		conn.row_factory = sqlite3.Row
	return conn

# Tells python to run this function before it closes
# Ensures proper disconnect	
@app.teardown_appcontext
def close_conn(exception):
	conn = getattr(g, 'dbFile', None)
	if conn is not None:
		conn.close()

def query_db(query, args = (), one = False):
	cur = get_conn().cursor()
	cur = get_conn().execute(query, args)
	r = cur.fetchall() 		# returns a list of tuples (dictionaries)
	cur.close()
	return (r[0] if r else None) if one else r

@app.route('/add', methods = ['POST'])
def add_task():
	# POST:
	if request.method == 'POST':
		category = request.form['category']
		priority = request.form['priority']
		description = request.form['description']
		print category, priority, description
		# tasks.append({'category': category, 'priority': priority, 'description' : description})
		# return redirect('/task1')
				# 'task' method is called directly
		query_db('INSERT INTO task (category, priority, description) values(?, ?, ?)',
		 [category, priority, description], one = False)
		get_conn().commit()
	return redirect(url_for('task'))

@app.route('/')
def welcome():
	return '<h1>Welcome to Flask lab!</h1>'

@app.route('/task', methods = ['GET', 'POST'])
def task():
	# GET:
	resp = ''
	resp = resp + '''
	<!DOCTYPE html>
	<html>
	<head><title>Tasks</title></head>
	<body>
	<form action = "/add" method = "POST">
		<p>Category: <input type = text name = "category"></p>
		<p>Priority: <input type = number name = "priority"></p>
		<p>Description: <input type = text name = "description"></p>
		<p><input type = submit value = Add></p>
	</form>

	'''

	# Show table
	resp = resp + '''
	<table border = "1" cellpadding = "3">
		<tbody>
			<tr>
				<th>Category</th>
				<th>Priority</th>
				<th>Description</th>
			</tr>
	'''
	for task in query_db('SELECT * FROM task'):
		resp = resp + "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"%(task['category'], task['priority'], task['description'])
	resp = resp + '</tbody></table></body></html>'
	return resp

# def print_tasks():
# 	tasks = query_db('select * from tasks')
# 	for task in tasks:
# 		print("Task(category: %s " %task['category'])
# 	print("%d tasks in total." %len(tasks))


if __name__ == '__main__':
	# interpreter is using this file directly
	# query_db('delete from tasks')
	# print_tasks()
	# add_task('Shopping')
	# add_task('Friends')
	# add_task('TV')
	# print_tasks()

	app.debug = True
	app.run()