from flask import Flask, render_template
import json
import sys
import os
app = Flask(__name__)

def read_json(file_path):
	with open(file_path) as file:
		data = json.load(file)
	return data

@app.route('/')

def index():
	listings = read_json("listings.json").values()
	stock_summaries = []
	for listing in listings:
		try:
			stock = read_json(f'static/{listing}_summary.json')
			stock_summaries.append(stock)
			if os.path.isfile(f'static/6_month_data_{listing}.png'):

				stock["IMG"] = f'6_month_data_{listing}.png'
				stock["has_image"] = True
			else:
				stock["has_image"] = False
		except:
			print(f'Cannot find stock: {listing}')

	return render_template('index.html', data=stock_summaries)

if __name__ == '__main__':
	debug = '--debug' in sys.argv
	app.run(host='0.0.0.0', port=5000, debug=debug)
