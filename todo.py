from flask import Flask, request, redirect, url_for
import sqlite3
app = Flask(__name__)

dbFile = 'c410-lab4-todo.db'
conn = None
tasks = []

def get_conn():
	global conn
	if conn is None:
		conn = sqlite3.connect('dbFile')
		conn.row_factory = sqlite3.Row
	return conn

def close_conn():
	global conn
	if conn is not None:
		conn.close()

def query_db(query, args = (), one = False):
	cur = get_conn().cursor()
	cur.execute(query, args)
	r = cur.fetchall() 		# returns a list of tuples (dictionaries)
	cur.close()
	return (r[0] if r else None) if one else r

def add_task(category):
	query_db('INSERT INTO tasks(category, priority, description) values(?)', [category, priority, description], one = True)
	get_conn().commit()

def print_tasks():
	tasks = query_db('select * from tasks')
	for task in tasks:
		print("Task(category: %s " %task['category'])
	print("%d tasks in total." %len(tasks))

@app.route('/')		# decorator; specifies URL
def welcome():
	return '<h1>Welcome to 410 - Flask lab!</h1>'

@app.route('/task', methods = ['GET', 'POST'])
def task():
	# POST:
	if request.method == 'POST':
		category = request.form['category']
		priority = request.form['priority']
		description = request.form['description']
		tasks.append({'category': category, 'priority': priority, 'description' : description})
		# return redirect('/task1')
		return redirect(url_for('task'))		# method is called directly
	# GET:
	resp = ''
	resp = resp + '''
	<form action = "" method = POST>
		<p>Category: <input type = text name = category></p>
		<p>Priority: <input type = number name = priority></p>
		<p>Description: <input type = text name = description></p>
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
	for task in tasks:
		resp = resp + "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"%(task['category'], task['priority'], task['description'])
	resp = resp + '</tbody></table>'
	return resp

if __name__ == '__main__':
	# interpreter is using this file directly
	app.debug = True
	app.run()