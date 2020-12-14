# Import required libraries
import requests
from flask import Flask, render_template,request,jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

# Imput team nums to monitor
teamnums = ["13-0562", "13-1243", "13-3301", "13-4790"]

# Allow CORS (don't remove)
app = Flask(__name__)
CORS(app)

# Grab information about teams
def get_team_scores(teamnums):
	# Create dictionary to store data
	data = {}
	# For each team number given
	for teamnum in teamnums:
		# Build the URL to scrape the data
		url="http://54.243.195.23/team.php?team="+teamnum
		# Get a response from the site
		response = requests.get(url)
		# Load the data into beautiful soup
		soup = BeautifulSoup(response.text, 'html.parser')
		# Retrieve the first table from the HTML source code
		div = soup.findAll("table", {"class": "CSSTableGenerator"})[0]
		# Get all talbe rows from the HTML source code
		rows = div.findAll('tr')[1]
		# Create a list to store the temp data
		listofdata = []
		# For each row in rows
		for row in rows:
			# Add the data to the list
			listofdata.append(row.text)
		# Set the dictionary key to the team number and the value to the rest of the data in the list {teamnum:[val1,val2,val3,etc.]}
		data[listofdata[0]] = listofdata[1:]
	# Return the data to the user
	return data

# Set a route of the home page
@app.route('/',methods = ['GET'])
def home():
	# Get the data result and store it in the result variable
	result = get_team_scores(teamnums)
	# Render the page for the user and pass the data to create the table
	return render_template('index.html', result=result)

# Host the site on the local machine
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, threaded=True)