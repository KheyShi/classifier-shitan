import flask
import io
from flask import Flask, render_template, request
from joblib import dump, load
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
clf = load('dtree.joblib')
clf2=load('nb.joblib')

app= flask.Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods = ["GET","POST"])
def index():
    
    return render_template('index.html')
    
@app.route('/', methods = ["GET","POST"])
@app.post("/response.html")
def response_page():
    inputs = []
    prediction = ''

    input_file = request.files.get('input_file', None)
    has_input_file = input_file is not None and input_file.content_type == 'text/csv'

    if has_input_file:
        input_file = request.files.get('input_file')
        input_file.stream.seek(0)
        input_data = io.StringIO(input_file.stream.read().decode("UTF8"))
        csv_reader = csv.DictReader(input_data, delimiter=',', quotechar='"')
        for row in csv_reader:
            inputs = [
                row['ct'],
                row['travel'],
                row['class'],
                row['comfort'],
                row['food'],
                row['ent'],
                row['ease']
            ]

    else:
        data = request.form
        inputs = [
            data.get('ct'),
            data.get('travel'),
            data.get('class'),
            data.get('comfort'),
            data.get('food'),
            data.get('ent'),
            data.get('ease')
        ]

    classifier = request.form.get('classifier')

    return render_template('response.html', 
        inputs=inputs,
        classifier=classifier,
        prediction=prediction
    )
@app.route('/', methods = ["GET","POST"])
def indexs():
	if(request.method == "POST"):
		#city = request.form['city']
		ins = request.form['class']
		ins2 = find_features(ins)
		prediction =  clf.classify_many(ins2)
		x = ""
		if(prediction[0] == 'satisfied'):
			x = "customer is satisfied"
		else:
			x = "customer is disatisfied" 
		return render_template('response.html',prediction = x)
	else:
		return render_template('response.html')

if __name__=="__main__":
    app.run(debug=False)
