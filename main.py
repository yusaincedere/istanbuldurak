import json
from flask import Flask,request
import wsdlOperations
from datetime import datetime
from random import  randint



app = Flask(__name__)
now = datetime.now()
datestr = now.strftime("%Y-%m-%dT")




@app.route('/hatlar', methods=['GET'])
def hatlar():
    return json.dumps(wsdlOperations.HatXmlToJson(wsdlOperations.getHatXml("")),ensure_ascii=False).encode('utf-8')


@app.route('/durakDetay', methods=['GET'])
def durakDetay():
    return json.dumps(wsdlOperations.HatXmlToJson(wsdlOperations.getHatXml("")), ensure_ascii=False).encode('utf-8')

@app.route('/duraklar', methods=['GET'])
def duraklar():

    output_dict = json.loads(wsdlOperations.getDuraklar(""))

    for x in output_dict:
        x["XKOORDINATI"] = x["KOORDINAT"][7:21]
        x["YKOORDINATI"] = x["KOORDINAT"][23:38]

    output_json = json.dumps(output_dict, ensure_ascii=False).encode('utf-8')
    return output_json


@app.route('/rotalar', methods=['GET'])
def rotalar():
    output_dict = json.loads(durakDetay())

    for x in output_dict:
        if(x["YON"] == "D"):
            x["YON"] = "1"
        else:
            x["YON"] = "2"
        x["Distance"] = "5.2"
    output_json = json.dumps(output_dict, ensure_ascii=False).encode('utf-8')
    return  output_json


@app.route('/seferzaman', methods=['GET','POST'])
def seferSaat():
    args = request.args.get('SDURAKKODU')
    input_dict = json.loads(durakDetay())
    output_dict = [x for x in input_dict if x['SDURAKKODU']== args and x["YON"] =="D"]

    for x in output_dict:
        h = randint(0,24)
        m = randint(0,60)
        d = randint(1,2)
        x["NextBus"] = {
            "OriginCode": "208031",
            "DestinationCode": "213562",
            "YON": "{}".format(d),
            "EstimatedArrival": "{}{}:{}:00+03:00".format(datestr,h,m),
            "Latitude": "40.997944",
            "Longitude": "29.090555",
            "VisitNumber": "1",
            "Load": "SDA",
            "Feature": "WAB",
            "Type": "SD"
        }
        h = randint(0, 24)
        m = randint(0, 60)
        x["NextBus2"] ={
            "OriginCode": "208031",
            "DestinationCode": "213562",
            "YON": "{}".format(d),
            "EstimatedArrival": "{}{}:{}:00+03:00".format(datestr, h, m),
            "Latitude": "40.997944",
            "Longitude": "29.090555",
            "VisitNumber": "1",
            "Load": "SDA",
            "Feature": "WAB",
            "Type": "SD"
        }
        h = randint(0, 24)
        m = randint(0, 60)
        x["NextBus3"] = {
            "OriginCode": "208031",
            "DestinationCode": "213562",
            "YON": "{}".format(d),
            "EstimatedArrival": "{}{}:{}:00+03:00".format(datestr, h, m),
            "Latitude": "40.997944",
            "Longitude": "29.090555",
            "VisitNumber": "1",
            "Load": "SDA",
            "Feature": "WAB",
            "Type": "SD"
        }

    output_json = json.dumps(output_dict,ensure_ascii=False).encode('utf-8')
    return output_json




@app.route('/seferler', methods=['GET'])
def seferKonum():
    return wsdlOperations.getSeferKonum("10A")


@app.route('/filosefer', methods=['GET'])
def seferKonumFilo():
    return wsdlOperations.FiloSeferKonum()






if __name__ == "__main__":
    app.run(debug=True)
