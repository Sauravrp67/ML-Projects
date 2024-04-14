from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from training_Validation_Insertion import train_validation
from trainingModel import trainModel
import flask_monitoringdashboard as dashboard
from prediction_validation_Insertion import pred_validation
from predictFromModel import prediction
import json



os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/", methods = ["GET"])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train",methods = ["POST"])
@cross_origin()

def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            train_valObj = train_validation(path) # object initialization

            #What happens during this step:
            # : First we validate if the names of the csv files are in accord with the naming scheme
            # : Second we check if the number of columns of each training csv match the schema
            # : We then check if any columns in the training csv files have all values NULL
            # : In each of the validation step, we put the files that agrees with the schema into GoodData Folder and those which don't into BadData Folder
            # : We then perform data transformation in the csv files that are present in the GoodData Folder
            # : Next task is to put all the Data Instances present inside each training CSV files in GoodData Folder Into a database
            # : Then we extract all the values from the database into a single csv file which is used for training
            # : After all the data have been moved to the, we delete the GoodData Folder
            # : We move BadData Folder into BadData Archive folder, and then delete the BadData Folder
                
            train_valObj.train_validation() #calling the training_validation function
            
            trainModelObj = trainModel() #object initialization

            trainModelObj.trainingModel()



    except ValueError:
        return Response("Error Occured! %s" %ValueError)
    except KeyError:
        return Response("Error Occured! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)
    return Response("Training Successful!!!")



@app.route("/predict", methods=["POST"])
@cross_origin

def predictRouteClient():
    try:
        if request.json is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json.loads(json_predictions) ))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)

port = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    host = '0.0.0.0'
    #port =5000

    httpd = simple_server.make_server(host,port,app)

    #print("Serving on %s %d % (host,port)")
    httpd.serve_forever()