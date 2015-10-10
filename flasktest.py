from flask import Flask
app=Flask(__name__)

@app.route("/")
def hello():
	print("this is ok")
	return "this sucks"
if __name__ == "__main__":
	app.run()