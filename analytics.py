import api
import plotly.graph_objects as go

class Analytics:

    def __init__(self, x1 = ..., xn = ...):
        """Définition du constructeur de l'objet Analytics"""

    def DeathDepGraph(self, option, name):
        try:
            with open('CovidData.dat', 'r') as file:
                file.readline()
                data = file.readlines()
                Dep_data = [{'dep': name, 'value': int(dep.split(', ')[2]), 'date': elt.split(' | ')[1]} for elt in data for dep in elt.split(' | ')[0].split('; ') if(dep.find(name) != -1)]
                return self.createGraph(Dep_data)

        except FileNotFoundError as file_e:
            covid_data = api.Covid_rss()
            covid_data.updateDataFiles()
            return self.DeathDepGraph(option, name)


    def createGraph(self, data):
        print(data[1])
        fig = go.Figure(data=go.Bar(x=[elt['date'] for elt in data], y=[elt['value'] for elt in data]))
        print(fig)
        return fig

    def my_function(self, test = ...): 
        """'self' signifie que l'on va chercher une fonction ou un champs dans la class même et ne 
        s'utilise n'uniquement dans le bloc class (self signifie l'objet courant)

        Definition d'une méthode dans une class"""



"""
mon_objet_analytics = Analytics(...) --> Création d'un objet de la class Analytics
mon_objet_analytics.my_function(...) --> faire appel à une fonction de l'objet"""