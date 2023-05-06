import pandas as pd
import requests
import time
import re

inputYear=2022

resultsList = []

for inputRound in range(1,22+1):
    limit = 500
    offset = 0
    end=False
    while not end:
        endpoint = f'http://ergast.com/api/f1/{inputYear}/{inputRound}/results.json?limit={limit}&offset={offset}'
        print (endpoint)
        resp = requests.get(endpoint)
        time.sleep(1)
        if resp.status_code==200:
            respJson = resp.json()
            totalRecords = int(respJson["MRData"]["total"])
            raceYear = respJson["MRData"]["RaceTable"]["season"]
            roundNum = respJson["MRData"]["RaceTable"]["round"]
            resultsJson = respJson["MRData"]["RaceTable"]["Races"][0]["Results"]
            for result in resultsJson:
                result_details = {}
                result_details['roundNum'] = roundNum
                result_details['driverref'] = result['Driver']['driverId']
                result_details['grid_start'] = result['grid']
                result_details['position'] = result['position']
                result_details['points'] = result['points']
                result_details['status'] = result['status']
                try:
                    result_details['race_time_ms'] = result['Time']['millis']
                except:
                    result_details['race_time_ms'] = ''

                try:
                    fastest_lap_time = result['FastestLap']['Time']['time']
                    fastest_lap_time = re.split('[.:]',fastest_lap_time)
                    fastest_lap_time = int(fastest_lap_time[0])*60*1000+int(fastest_lap_time[1])*1000+int(fastest_lap_time[2])
                    result_details['fastest_lap_time'] = fastest_lap_time
                    result_details['fastest_lap_avg_speed'] = result['FastestLap']['AverageSpeed']['speed']
                except:
                    result_details['fastest_lap_time'] = ''
                    result_details['fastest_lap_avg_speed'] = ''

                resultsList.append(result_details)
            if offset+limit>totalRecords:
                end=True
            else:
                offset=offset+limit
            print(str(len(resultsList)))

resultsDf = pd.DataFrame(resultsList)
filename = 'F12022-Results.csv'
resultsDf.to_csv(filename,index=False)
