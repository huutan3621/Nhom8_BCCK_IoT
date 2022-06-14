from flask import render_template, Flask, Markup, json,request, jsonify
app = Flask(__name__)
import numpy as np
import matplotlib.pyplot as plt
from firebase import firebase
import socket
from datetime import datetime
#xu ly khi ban vao host 127.0.0.1:5000
app = Flask(__name__, static_url_path='/static/')
firebase = firebase.FirebaseApplication('https://test-1f0cf-default-rtdb.asia-southeast1.firebasedatabase.app/', None)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    print("index")
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/', methods=['GET', 'POST'])
def index ():
    LastUpdateRaspi = firebase.get('/Last updated', '')
    LastUpdateRaspi = datetime.strptime(LastUpdateRaspi, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    print((now-LastUpdateRaspi).total_seconds()/60)
    if (now-LastUpdateRaspi).total_seconds()/60 <= 5:
        StateRaspi = 'bg-gradient-success'
    else:
        StateRaspi = 'bg-gradient-secondary'
    print(StateRaspi)

    LastUpdateESP826 = firebase.get('/WEMOSD1/last_updated', '')
    LastUpdateESP826 = datetime.strptime(LastUpdateESP826, '%Y-%m-%d %H:%M:%S')
    if (now-LastUpdateESP826).total_seconds()/60 <= 5:
        StateESP8266 = 'bg-gradient-success'
    else:
        StateESP8266 = 'bg-gradient-secondary'

    Humidity = firebase.get('/humidity', '')
    HumidityValue = list(Humidity.items())[-1][1]['value']
    LastUpdatedHumidityValue = list(Humidity.items())[-1][1]['last_updated']
    print(HumidityValue)
    print(LastUpdatedHumidityValue)

    Temperature = firebase.get  ('/temperature', '')
    TemperatureValue = list(Temperature.items())[-1][1]['value']
    LastUpdatedTemperatureValue = list(Temperature.items())[-1][1]['last_updated']
    print(TemperatureValue)
    print(LastUpdatedTemperatureValue)

    Light1Value = firebase.get('/WEMOSD1/BULB/DEN1/DEN1', '')
    if int(Light1Value) == 1:
        Light1Value = "checked"
    elif int(Light1Value) == 0:
        Light1Value = "not-checked"

    Light2Value = firebase.get('/WEMOSD1/BULB/DEN2/DEN2', '')
    if int(Light2Value) == 1:
        Light2Value = "checked"
    elif int(Light2Value) == 0:
        Light2Value = "not-checked"

    Light3Value = firebase.get('/WEMOSD1/BULB/DEN3/DEN3', '')
    if int(Light3Value) == 1:
        Light3Value = "checked"
    elif int(Light3Value) == 0:
        Light3Value = "not-checked"

    Light4Value = firebase.get('/WEMOSD1/BULB/DEN4/DEN4', '')
    if int(Light4Value) == 1:
        Light4Value = "checked"
    elif int(Light4Value) == 0:
        Light4Value = "not-checked"
    return render_template('index.html',StateRaspi=StateRaspi, LastUpdateRaspi=LastUpdateRaspi,
                            StateESP8266=StateESP8266, LastUpdateESP826=LastUpdateESP826,
                            HumidityValue=HumidityValue,LastUpdatedHumidityValue=LastUpdatedHumidityValue,
                            TemperatureValue = TemperatureValue, LastUpdatedTempuratureValue=LastUpdatedTemperatureValue,
                            Light1Value=Light1Value, Light2Value=Light2Value, Light3Value=Light3Value, Light4Value=Light4Value) #se hien ra giao dien la file index.html

@app.route('/charts', methods=['GET', 'POST'])
def charts ():
    Temperature = firebase.get  ('/temperature', '')
    Humidity = firebase.get('/humidity', '')
    now = datetime.now()
    Temperature_date_list = []  
    Temperature_date_list_res = [] 
    Temperature_data = [] 
    count_Temperature = 0
    for element in list(Temperature.items()):
        value = list(Temperature.items())[count_Temperature][1]['value']
        last_updated = list(Temperature.items())[count_Temperature][1]['last_updated']
        last_updated = datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S')
        x = {
            "date": last_updated,
            "value": float(value)
        }
        Temperature_date_list.append(x)
        count_Temperature+=1

    res_Temperature = sorted(Temperature_date_list, key=lambda sub: abs(sub['date'] - now))[:11]
    print("Nearest date from Temperature list : " + str(res_Temperature))
    count_Temperature = 0
    for element in res_Temperature:
        Temperature_data.append(res_Temperature[count_Temperature]["value"])
        date = res_Temperature[count_Temperature]["date"]
        Temperature_date_list_res.append(date)
        count_Temperature+=1

    Humidity_date_list = []
    Humidity_date_list_res = []
    Humidity_data = []
    count_Humidity = 0
    for element in list(Humidity.items()):
        value = list(Humidity.items())[count_Humidity][1]['value']
        last_updated = list(Humidity.items())[count_Humidity][1]['last_updated']
        last_updated = datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S')
        x = {
            "date": last_updated,
            "value": float(value),
            
        }
        Humidity_date_list.append(x)
        count_Humidity+=1
        # shorthand using lambda function for compact solution
    res_Humidity = sorted(Humidity_date_list, key=lambda sub: abs(sub['date'] - now))[:11]
    print("Nearest date from Humidity list : " + str(res_Humidity))
    count_Humidity = 0
    for element in res_Humidity:
        Humidity_data.append(res_Humidity[count_Humidity]["value"])
        date = res_Humidity[count_Humidity]["date"]
        Humidity_date_list_res.append(date)
        count_Humidity+=1

    # show the form, it wasn't submitted
    return render_template('charts.html',temp_data_average=Temperature_data,temp_data_average_label_0=Temperature_date_list_res[10],
                                        temp_data_average_label_1=Temperature_date_list_res[9],temp_data_average_label_2=Temperature_date_list_res[8],
                                        temp_data_average_label_3=Temperature_date_list_res[7],temp_data_average_label_4=Temperature_date_list_res[6],
                                        temp_data_average_label_5=Temperature_date_list_res[5],temp_data_average_label_6=Temperature_date_list_res[4],
                                        temp_data_average_label_7=Temperature_date_list_res[3],temp_data_average_label_8=Temperature_date_list_res[2],
                                        temp_data_average_label_9=Temperature_date_list_res[1],temp_data_average_label_10=Temperature_date_list_res[0],

                                        Humidity_data_average=Humidity_data,Humidity_data_average_label_0=Humidity_date_list_res[10],
                                        Humidity_data_average_label_1=Humidity_date_list_res[9],Humidity_data_average_label_2=Humidity_date_list_res[8],
                                        Humidity_data_average_label_3=Humidity_date_list_res[7],Humidity_data_average_label_4=Humidity_date_list_res[6],
                                        Humidity_data_average_label_5=Humidity_date_list_res[5],Humidity_data_average_label_6=Humidity_date_list_res[4],
                                        Humidity_data_average_label_7=Humidity_date_list_res[3],Humidity_data_average_label_8=Humidity_date_list_res[2],
                                        Humidity_data_average_label_9=Humidity_date_list_res[1],Humidity_data_average_label_10=Humidity_date_list_res[0])

@app.route('/logs', methods=['GET', 'POST'])
def logs ():
    # show the form, it wasn't submitted
    return render_template('logs.html')   
@app.route('/index_get_data', methods=['GET', 'POST'])
def stuff2():
  # Assume data comes from somewhere else
    Temperature = firebase.get  ('/temperature', '')
    count_Temperature = 0
    data=[]
    logs={}
    for element in list(Temperature.items()):
        value = list(Temperature.items())[count_Temperature][1]['value']
        last_updated = list(Temperature.items())[count_Temperature][1]['last_updated']
        last_updated = datetime. strptime(last_updated, '%Y-%m-%d %H:%M:%S')
        x = {
            "BName": "Raspberry Pi",
            "SName": "DHT22/Temperature",
            "Value": value,
            "Last updated": str(last_updated)
        }
        data.append(x)
        count_Temperature+=1

    Humidity = firebase.get('/humidity', '')
    count_Humidity=0
    for element in list(Humidity.items()):
        value = list(Humidity.items())[count_Humidity][1]['value']
        last_updated = list(Humidity.items())[count_Humidity][1]['last_updated']
        last_updated = datetime. strptime(last_updated, '%Y-%m-%d %H:%M:%S')
        x = {
            "BName": "Raspberry Pi",
            "SName": "DHT22/Humidity",
            "Value": value,
            "Last updated": str(last_updated)
        }
        data.append(x)
        count_Humidity+=1
    print(data)
    sorted_date = sorted(data, key=lambda x: datetime.strptime(x['Last updated'], '%Y-%m-%d %H:%M:%S'))
    sorted_date.reverse()
    logs['data'] = sorted_date
    print(sorted_date)
    return jsonify(logs)

@app.route("/postraspi", methods = ['POST','GET', 'OPTIONS'])
def postHandler_raspi():
    if request.method == 'POST':
        ip_address = request.remote_addr
        print("Client IP Address is:" + ip_address)
        print (request.form['temperature'])
        print (request.form['humidity'])
        now = datetime.now()
        last_updated = now.strftime("%Y-%m-%d %H:%M:%S")
        temperature_data =  {
            'value': request.form['temperature'],
            'last_updated': last_updated
        }
        humidity_data =  {
            'value': request.form['humidity'],
            'last_updated': last_updated
        }
        firebase.post('/temperature/',temperature_data)
        firebase.post('/humidity/',humidity_data)
        firebase.patch("/",{'Last updated': last_updated})
    return 'JSON posted'

@app.route("/postwemosd1", methods = ['POST','GET'])
def postJsonHandler_wemosd1():
    if request.method == 'POST':
        content = request.get_json()
        print (content["message"])
        print (str(content["data"]))
        lastupdated_wemos = datetime. strptime(str(content["data"]), '%Y-%m-%d %H:%M:%S')
        print (lastupdated_wemos)
        lastupdated = firebase.get('/WEMOSD1/last_updated', '')
        lastupdated_data = datetime. strptime(lastupdated, '%Y-%m-%d %H:%M:%S')
        if (lastupdated_wemos-lastupdated_data).total_seconds()/60 >= 5:
            firebase.patch('/WEMOSD1/',{'last_updated': str(lastupdated_wemos)})
    return 'JSON posted'
       
if __name__ == "__main__":
    app.run(host="192.168.235.94", debug=True)