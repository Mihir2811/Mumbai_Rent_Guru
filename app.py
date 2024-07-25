import flask
from flask import render_template, request, Flask
import pickle
import pandas as pd

model = pickle.load(open('Model.py', 'rb'))
info = pd.read_csv('cleaned_data.csv')

app = Flask(__name__)
@app.route('/')
def home():

    house_type = sorted(info['house_type'].unique()) 
    house_size = sorted(info['house_size'].unique()) 
    location = sorted(info['location'].unique())
    verificationDate = sorted(info['verificationDate'].unique())  
    Status = sorted(info['Status'].unique())

    return render_template('index.html', house_type= house_type, house_size = house_size , location= location,verificationDate= verificationDate, Status=Status)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method=='POST':

        house_type = request.form['house_type']
        house_size = request.form['house_size']
        location = request.form['location']
        numBathrooms = request.form['numBathrooms']
        numBalconies = request.form['numBalconies']
        verificationDate = request.form['verificationDate']
        SecurityDeposit = request.form['SecurityDeposit']
        Status = request.form['Status']

        input_data = pd.DataFrame([[house_type, house_size, location, numBathrooms, numBalconies,verificationDate, SecurityDeposit, Status 
                                    ]], columns=['house_type', 'house_size', 'location', 'numBathrooms', 'numBalconies', 'verificationDate', 'SecurityDeposit', 'Status' ])
        
        prediction = model.predict(input_data)

        if(prediction>=0):
            return render_template('index.html',prediction_result= 'Estimated Rent Price: ₹{:.2f}'.format(prediction[0]))
        else:
            print('false')

if __name__ == '__main__':
    app.run(debug=None)