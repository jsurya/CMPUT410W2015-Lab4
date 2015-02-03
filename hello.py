from flask import Flask
app = Flask(__name__)

@app.route('/hello')		# decorator; specifies URL
def hello():
	return '<h1>Hello Flask!</h1>'

@app.route('/bye')		# decorator; specifies URL
def bye():
	return '<h1>Goodbye Flask!</h1>'

if __name__ == '__main__':
	# interpreter is using this file directly
	app.run()