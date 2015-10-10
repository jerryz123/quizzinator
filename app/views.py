from app import app
from flask import *


def index():
	return return_template("index.html")