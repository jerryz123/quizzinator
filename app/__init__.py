from flask import Flask
from flask import *
app=Flask(__name__)
from app import views
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template("index.html",name=name)

