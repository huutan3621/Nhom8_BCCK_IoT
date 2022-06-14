from firebase import firebase
from datetime import datetime
firebase = firebase.FirebaseApplication('https://test-1f0cf-default-rtdb.asia-southeast1.firebasedatabase.app/', None)
Temperature = firebase.get  ('/temperature', '')
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
            "value": value,
            "date": last_updated
        }
    Temperature_date_list.append(x)
    count_Temperature+=1

res_Temperature = sorted(Temperature_date_list, key=lambda sub: abs(sub['date'] - now))[:11]
count_Temperature = 0
for element in res_Temperature:
    Temperature_data.append(res_Temperature[count_Temperature]["value"])
    date = res_Temperature[count_Temperature]["date"]
    if len(Temperature_date_list_res) > 0: 
        print("Like")
        print(Temperature_date_list_res)
        Temperature_date = Temperature_date_list_res[len(Temperature_date_list_res)-1]
        if date.date() == Temperature_date.date():
            Temperature_date_list_res.append(date.time())
            print("Like.2")
        else: 
            Temperature_date_list_res.append(date)
            print(str(Temperature_date.date()))
            print("U.Like.2")
    else: 
        Temperature_date_list_res.append(date)
    count_Temperature+=1

