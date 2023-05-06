import pandas as pd
import requests
import time
import re

#inputRound=22
inputYear=2022

lapTimesDict = []

raceYear = ""
roundNum = ""
raceName = ""

for inputRound in range(1,22+1):
    limit = 500
    offset = 0
    end=False
    while not end:
        endpoint = f'http://ergast.com/api/f1/{inputYear}/{inputRound}/laps.json?limit={limit}&offset={offset}'
        print (endpoint)
        resp = requests.get(endpoint)
        time.sleep(1)
        if resp.status_code==200:
            respJson = resp.json()
            totalRecords = int(respJson["MRData"]["total"])
            raceYear = respJson["MRData"]["RaceTable"]["season"]
            roundNum = respJson["MRData"]["RaceTable"]["round"]
            raceName = respJson["MRData"]["RaceTable"]["Races"][0]["raceName"]
            lapsJson = respJson['MRData']['RaceTable']['Races'][0]['Laps']
            circuitName = respJson['MRData']['RaceTable']['Races'][0]['Circuit']['circuitName']
            circuitLat = respJson['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['lat']
            circuitLong = respJson['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['long']
            circuitCountry = respJson['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['country']
            circuitCity = respJson['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['locality']
            for lap in lapsJson:
                lapNum = lap["number"]
                for timing in lap["Timings"]:
                    lapTime = timing["time"] #get lap time string
                    lapTime = re.split('[.:]',lapTime) #split lap time into min, sec, ms parts
                    lapTime = int(lapTime[0])*60*1000+int(lapTime[1])*1000+int(lapTime[2]) #math to total the ms
                    timing["ms"] = lapTime
                    timing["lap"] = lapNum
                    timing["raceid"] = 1073 + int(roundNum)
                    timing["circuitName"] = circuitName
                    timing["circuitLat"] = circuitLat
                    timing["circuitLong"] = circuitLong
                    timing["circuitCountry"] = circuitCountry
                    timing["circuitCity"] = circuitCity
                    lapTimesDict.append(timing)
            if offset+limit>totalRecords:
                end=True
            else:
                offset=offset+limit
            print(str(len(lapTimesDict)))

lapTimesDf = pd.DataFrame(lapTimesDict)
lapTimesDf = lapTimesDf.rename({'driverId':'driverref'},axis=1)
filename = 'F12022.csv'
lapTimesDf.to_csv(filename,index=False)
