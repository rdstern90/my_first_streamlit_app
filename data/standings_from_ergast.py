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
        endpoint = f'http://ergast.com/api/f1/{inputYear}/{inputRound}/driverStandings.json?limit={limit}&offset={offset}'
        print (endpoint)
        resp = requests.get(endpoint)
        time.sleep(1)
        if resp.status_code==200:
            respJson = resp.json()
            totalRecords = int(respJson["MRData"]["total"])
            raceYear = respJson["MRData"]["StandingsTable"]["season"]
            roundNum = respJson["MRData"]["StandingsTable"]["round"]
            resultsJson = respJson["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            for result in resultsJson:
                record = {}
                record['roundNum'] = roundNum
                record['driverref'] = result['Driver']['driverId']
                record['points'] = result['points']
                record['wins'] = result['wins']
                record['nationality'] = result['Driver']['nationality']
                record['dob'] = result['Driver']['dateOfBirth']
                record['constructorId'] = result['Constructors'][0]['constructorId']

                resultsList.append(record)
            if offset+limit>totalRecords:
                end=True
            else:
                offset=offset+limit
            print(str(len(resultsList)))

resultsDf = pd.DataFrame(resultsList)
filename = 'F12022-Standings.csv'
resultsDf.to_csv(filename,index=False)
