from flask import Flask, render_template, jsonify, request
import numpy as np
import pandas as  pd
import sklearn 
import json
import pickle as p 
import requests 


app  = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/cancerprediction", methods = ['POST'])
def predictheart():
    data = request.get_json()
    prediction = np.array2string(model.predict(data))
    return jsonify(prediction)

@app.route("/cancerStatus", methods = ['POST'])
def heartcondition():
    url = "http://localhost:5000/cancerprediction"

    area_worst = float(request.form["area_worst"])
    area_se	= float(request.form["area_se"])
    perimeter_worst	= float(request.form["perimeter_worst"])
    perimeter_mean = float(request.form["perimeter_mean"])
    radius_worst = float(request.form["radius_worst"])
    radius_mean	= float(request.form["radius_mean"])
    perimeter_se = float(request.form["perimeter_se"])
    texture_worst = float(request.form["texture_worst"])
    texture_mean = float(request.form["texture_mean"])
    concavity_worst = float(request.form["concavity_worst"])
    radius_se = float(request.form["radius_se"])
    concavity_mean = float(request.form["concavity_mean"])
    compactness_worst =  float(request.form["compactness_worst"])
    concave_points_worst = float(request.form["concave_points_worst"])
    concave_points_mean = float(request.form["concave_points_mean"])
    compactness_mean = float(request.form["compactness_mean"])
    symmetry_worst = float(request.form["symmetry_worst"])
    concavity_se = float(request.form["concavity_se"]) 
    compactness_se = float(request.form["compactness_se"])
    smoothness_worst = float(request.form["smoothness_worst"])
    concave_points_se = float(request.form["concave_points_se"])
    symmetry_mean = float(request.form["symmetry_mean"])
    fractal_dimension_worst = float(request.form["fractal_dimension_worst"])
    area_mean = float(request.form["area_mean"])

    data = {"area_worst" : [area_worst], "area_mean": [area_mean], "area_se" : [area_se], "perimeter_worst":[perimeter_worst],
            "perimeter_mean":[perimeter_mean], "radius_worst" : [radius_worst], "radius_mean":[radius_mean], "perimeter_se" : [perimeter_se],
            "texture_worst":[texture_worst], "texture_mean" : texture_mean,"concavity_worst":[concavity_worst],"radius_se" : [radius_se],"concavity_mean" : [concavity_mean],
            "compactness_worst":[compactness_worst],
             "concave points_worst":[concave_points_worst],"concave points_mean":[concave_points_mean],"compactness_mean":[compactness_mean],
             "symmetry_worst":[symmetry_worst],"concavity_se":[concavity_se],"compactness_se":[compactness_se],"smoothness_worst":[smoothness_worst],
             "concave points_se" : [concave_points_se], "symmetry_mean":[symmetry_mean], "fractal_dimension_worst" : [fractal_dimension_worst]} 

    data = pd.DataFrame(data)
    cancer = pd.read_csv('cancer.csv')
    x = cancer.iloc[:,2:33]

    imp_col = ['area_worst', 'area_mean', 'area_se', 'perimeter_worst',
       'perimeter_mean', 'radius_worst', 'radius_mean', 'perimeter_se',
       'texture_worst', 'texture_mean', 'concavity_worst', 'radius_se',
       'concavity_mean', 'compactness_worst', 'concave points_worst',
       'concave points_mean', 'compactness_mean', 'symmetry_worst',
       'concavity_se', 'compactness_se', 'smoothness_worst',
       'concave points_se', 'symmetry_mean', 'fractal_dimension_worst']

    x = x[imp_col]       
    x = pd.concat([x,data],axis = 0)
    x = x.reset_index(drop = True) 
    x_new = x

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    x_new[imp_col] = scaler.fit_transform(x_new[imp_col]) 
    
    a = x_new.iloc[-1,:]
    new_data = []
     
    for i in range(len(a.index)):
        new_data.append(a[i])

    new_data = [new_data]
    j_data = json.dumps(new_data)

    headers = {'content-type':'application/json','Accept-Charset':'UTF-8'}
    r = requests.post(url, data = j_data, headers = headers)
    r1 = list(r.text)
    stat = ""
    print(stat)
    if r1[2] == str(0):
        stat = "Patient Cancer's is Benign"
    elif r1[2] == str(1):
        stat = "Patient Cancer's is Malign"
    else :
        stat = "Error"
        
    return render_template("result.html", result = stat)

if __name__ == '__main__':

    model_file='cancer.pickle'
    model=p.load(open(model_file,'rb'))
    app.run(debug = True, host = '0.0.0.0')

    