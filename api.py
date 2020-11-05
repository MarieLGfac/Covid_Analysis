import requests
import json
from datetime import date, datetime, timedelta
from departements import departement_data

class Covid_rss:

    def __init__(self):
        self.api_url = 'https://coronavirusapi-france.now.sh/LiveDataByDepartement?Departement='
        self.headers = {"Content-Type": "application/json"}
        self.content = []

    def nullData(self, data):
        if(data.find('null') != -1):
            return True
        else:
            return False

    def todayDepData(self):
        for elt in departement_data:
            self.content.append(json.loads((requests.get(self.api_url+elt[1], self.headers)).content))
            #print(self.content[len(self.content)-1]['LiveDataByDepartement'][0]['gueris'])
            #print(type(self.content[0]))

    def DataForChoosenDate(self, date):
        result = requests.get('https://coronavirusapi-france.now.sh/AllDataByDate?date=' + date, self.headers).content.decode('utf8')
        data = []
        if(self.nullData(result) == False):
            tamp = [elt for elt in json.loads(result)["allFranceDataByDate"] if elt["code"].find('REG') == -1 and elt["nom"] != 'France']
            #print(tamp)
            data = [[elt["nom"], elt["gueris"], elt["deces"], elt["reanimation"], elt["hospitalises"]] for elt in tamp]
        
        return data
        # print(self.content['allFranceDataByDate'][0])

    def updateDataFiles(self):
        #format : 2020-09-28
        data = []
        try:
            with open('covidData.dat', 'r+') as file:
                lines = file.readlines()
                last_date = lines[-1].split(' | ')[1].replace('\n', '')
                if(last_date != str(date.today())): #Recherche du | 2020-month-day
                    request_date = datetime.strptime(last_date, '%Y-%m-%d').date() + timedelta(days = 1)
                    while(request_date <= date.today()):
                        #self.content.append(json.loads((requests.get('https://coronavirusapi-france.now.sh/AllDataByDate?date=' + request_date.strftime("%Y-%m-%d"), self.headers)).content))
                        #tamp = [elt for elt in self.content[0]["allFranceDataByDate"] if elt["code"].find('REG') == -1 and elt["nom"] != 'France']
                        #data = [[elt["nom"], elt["gueris"], elt["deces"], elt["reanimation"], elt["hospitalises"]] for elt in tamp]
                        #print(request_date.strftime("%Y-%m-%d"))
                        if(self.DataForChoosenDate(request_date.strftime("%Y-%m-%d")) != []):
                            self.saveListOfData(self.DataForChoosenDate(request_date.strftime("%Y-%m-%d")), request_date)
                        request_date += timedelta(days = 1)
        
        except FileNotFoundError as file_e:
            with open('covidData.dat', 'a+') as new_file:
                new_file.write('Dep_nom\t Gueris\t Deces\t reanimation\t hospitalises\t | Date\n')
                data = self.DataForChoosenDate('2020-04-10')
                if(data != []):
                    new_file.write('; '.join([str(elem) for elem in data]) + ' | ' + '2020-04-10' + '\n')
                    new_file.close()
                    self.updateDataFiles()
        self.saveSumData()

    def listOfData(self):
        data = []
        for elt in self.content:
            #print(elt['LiveDataByDepartement'])
            if(elt['LiveDataByDepartement'] != []):
                #print(elt['LiveDataByDepartement'][0])
                data.append([elt['LiveDataByDepartement'][0]['nom'], elt['LiveDataByDepartement'][0]['gueris'], elt['LiveDataByDepartement'][0]['deces'], elt['LiveDataByDepartement'][0]['reanimation'], elt['LiveDataByDepartement'][0]['hospitalises']])

        return data

    def saveListOfData(self, dataList, dataDate):
        try:
            with open('covidData.dat', 'r+') as file:   
                if(len(file.readline()) == 0):
                    #print("go")
                    file.write('Dep_nom\t Gueris\t Deces\t reanimation\t hospitalises\t | Date\n')
                    data = '; '.join([str(elem) for elem in dataList])
                    file.write(data + ' | ' + dataDate.strftime('%Y-%m-%d') + '\n')
                else:
                    lines = file.readlines()
                    #print(len(lines))
                    last_line = lines[-1].split(' | ')
                    if(last_line[-1].rstrip() != dataDate.strftime('%Y-%m-%d')):
                        data = '; '.join([str(elem) for elem in dataList])
                        file.write(data + ' | ' + dataDate.strftime('%Y-%m-%d') + '\n')

        except FileNotFoundError as file_e:
            with open('covidData.dat', 'a+') as new_file:
                new_file.write('Dep_nom\t Gueris\t Deces\t reanimation\t hospitalises\t | Date\n')
                new_file.close()
            self.saveListOfData(dataList, dataDate)
            
    def saveSumData(self):
        try:
            with open('sumData.dat', 'r+') as fileSum:
                lines = fileSum.readlines()
                #print(len(lines))
                if(len(lines) > 0):
                    strDate = json.loads(lines[-1])["date"]
                    dateSum = datetime.strptime(strDate, '%Y-%m-%d').date()
                else:
                    dateSum = date(day=1, month=1, year=1900)
                
                with open('CovidData.dat', 'r') as fileCovid:
                    data = fileCovid.readlines()
                    i = 0
                    data.pop(i)
                    while(i < len(data) and datetime.strptime(data[i].split(' | ')[1].replace('\n', ''), '%Y-%m-%d').date() <= dateSum):
                        data.pop(i)
                        i += 1
                    data = [elt.split('; ') for elt in data]
                    #data = [json.loads(elt.split('; ')) for elt in data]
                    listOfData = []
                    for dateData in data:
                        date_rss = dateData[-1].split(' | ')[1].replace('\n', '')
                        listOfData.append({
                            "gueris": 0,
                            "deces": 0, 
                            "reanimation": 0, 
                            "hospitalises": 0,
                            "date": date_rss,
                        })
                        for elt in dateData:
                            tamp = elt.replace('[', '').replace(']', '').split(' | ')[0].split(', ')
                            #Dep_nom	 Gueris	 Deces	 reanimation	 hospitalises	 | Date
                            listOfData[-1]["gueris"] += int(tamp[1])
                            listOfData[-1]["deces"] += int(tamp[2])
                            listOfData[-1]["reanimation"] += int(tamp[3])
                            listOfData[-1]["hospitalises"] += int(tamp[4])

                        #print(listOfData[-1], 'length of data = ', len(listOfData), ' id = ', hex(id(listOfData[-1])))
                        fileSum.write(json.dumps(listOfData[-1]).replace('\'', '\"') + '\n')
            #else:
                #file.write(str(data_dict).replace('\'', '\"') + '\n')
        except FileNotFoundError as file_e:
            with open('sumData.dat', 'a') as new_file:
                new_file.close()
            self.saveSumData()


"""Covid_data = Covid_rss()
Covid_data.updateDataFiles()
Covid_data.saveSumData()
data = Covid_data.rattrapage()
Covid_data.request_all()
data = Covid_data.listOfData() #[[nom, gueris, deces, reanimation, hospitalises], ...]
Covid_data.saveListOfData(data)
Covid_data.saveSumData(data) 
Covid_data.sumReanimationFigure()
Covid_data.depDecesFigure()
fig = go.Figure(data=go.Bar(y=Covid_data.content[]))
fig.write_html('first_figure.html', auto_open=True)"""