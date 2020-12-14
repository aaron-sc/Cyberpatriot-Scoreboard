import requests
from flask import Flask, render_template,request,jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

# Imput team nums to monitor
teamnums = ["13-0562", "13-1243", "13-3301", "13-4790"]

app = Flask(__name__)
CORS(app)

def get_team_scores(teamnums):
	data = {}
	for teamnum in teamnums:
		url="http://54.243.195.23/team.php?team="+teamnum
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		div = soup.findAll("table", {"class": "CSSTableGenerator"})[0]
		rows = div.findAll('tr')[1]
		listofdata = []
		for row in rows:
			listofdata.append(row.text)
		data[listofdata[0]] = listofdata[1:]
	return data

@app.route('/',methods = ['GET'])
def home():
	result = get_team_scores(teamnums)
	return render_template('index.html', result=result)



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, threaded=True)