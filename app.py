#import dependencies
from flask import Flask

#create app variable
app = Flask(__name__)

#root
@app.route('/')
def hello_world():
	return 'Hello world'