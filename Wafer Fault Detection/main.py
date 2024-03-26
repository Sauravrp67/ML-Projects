# This library is used for making simple HTTPs request by the web browsers to this framework.
from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from training_Validation_Insertion import train_validation
from trainingModel import trainModel
import flask_monitoringdashboard as dashboard

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/", methods = ["GET"])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/",methods = ["POST"])
@cross_origin()

def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            train_valObj = train_validation(path) # object initialization

            train_valObj.train_validation() #calling the training_validation function

            trainModelObj = trainModel() #object initialization

            trainModelObj.trainingModel()



    except ValueError:
        return Response("Error Occured! %s" %ValueError)
    except KeyError:
        return Response("Error Occured! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)

port = init(os.getenv("PORT", 5000))

if __name__ == "__main__":
    host = '0.0.0.0'
    #port =5000

    httpd = simple_server.make_server(host,port,app)

    #print("Serving on %s %d % (host,port)")
    httpd.serve_forever()