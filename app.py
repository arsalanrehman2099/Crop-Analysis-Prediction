from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import joblib

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoder = joblib.load('encoder.pkl')

@app.route('/py_server')
@cross_origin()
def index():
    return 'Running Python Flask Server'

def crop_prediction(data):
    if data == None:
        return {'error':1,'message':'No input data found'}
    elif ('N' in data) == False:
        return {'error':1,'message':'No Nitrogen Found'}
    elif ('P' in data) == False:
        return {'error':1,'message':'No Phosphorus Found'}
    elif ('K' in data) == False:
        return {'error':1,'message':'No Potassium Found'}
    elif ('temperature' in data) == False:
        return {'error':1,'message':'No Temperature Found'}
    elif ('humidity' in data) == False:
        return {'error':1,'message':'No Humidity Found'}
    elif ('ph' in data) == False:
        return {'error':1,'message':'No ph Found'}
    elif ('rainfall' in data) == False:
        return {'error':1,'message':'No Rainfall Found'}
    else:
        pred_data = [[data['N'],data['P'],data['K'],data['temperature'],
                        data['humidity'],data['ph'],data['rainfall']]]

        scaled_pred_data = scaler.transform(pred_data)
        prediction = model.predict(scaled_pred_data)
        prediction_text = label_encoder.inverse_transform(y=prediction)
        return {'error':0,'prediction':prediction_text[0]}


@app.route('/crop',methods=['POST'])
@cross_origin()
def crop_prediction_api():
    
    try:
        content = request.json
        response = crop_prediction(content)
        return jsonify(response)
       
    except:
        return jsonify({'error':1,'message':'Something went wrong'})


if __name__ == '__main__':
    app.run()