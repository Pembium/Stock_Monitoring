from flask import Flask, render_template
import json
import sys

app = Flask(__name__)

@app.route("/")

def index():
	with open('stock_summaries/test.json', 'r') as f:
		data = json.load(f)
	return render_template('index.html', data=data)

if __name__ == '__main__':
	debug = '--debug' in sys.argv
	app.run(host='0.0.0.0', port=5000, debug=debug)
