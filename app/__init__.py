from flask import Flask
from flask import *
app=Flask(__name__)
from app import views



@app.route('/')
def start():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form():
    text = request.form['text']
    processed_text = text.upper()
    return render_template("results.html")