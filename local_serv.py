import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import visdcc
import api
from departements import departement_data

class CustomDash(dash.Dash):
    
    def setLayout(self, options):
        self.layout = html.Div([
                        html.H1('Analysis'),
                        dcc.Dropdown(
                            id='dropdown-1',
                            options=[{'label': i, 'value': i} for i in options],
                            value='',
                        ),
                        html.Div(id='depDropdown'),
                        html.Div(id='output'),
                        html.Button('Actualiser les données', id = 'button-1'),
                        visdcc.Run_js(id = 'javascript')
                    ])

options = ('Décés', 'Réanimations', 'Hospitalisations', 'Guéris')
# external JavaScript files
external_scripts = [
    "https://cdn.jsdelivr.net/npm/sweetalert2@10",
]

app = CustomDash(title='Analysis', external_scripts=external_scripts)
app.setLayout(options)




"""-----Callbacks functions----"""
@app.callback(
    Output('javascript', 'run'),
    [Input('button-1', 'n_clicks')]
)
def update(n_clicks): 
    if n_clicks:
        covid_data = api.Covid_rss()
        covid_data.updateDataFiles()
        return "Swal.fire({icon: 'success', title: 'Data Updated !', text: 'Now, charts are waiting you'})"

@app.callback(
    Output('depDropdown', 'children'),
    [Input('dropdown-1', 'value')]
)
def addDepDropdown(value):
    if value != '':
        return dcc.Dropdown(id='dropdown-2', 
                            options=[{'label': i, 'value': i[1]} for i in [[elt[0]+' ', elt[1]] for elt in departement_data]], 
                            value='',),
    else:
        return ""

@app.callback(
    Output('output', 'children'),
    [Input('dropdown-2', 'value'), Input('dropdown-2', 'value')]
)
def buildGraph(option, dep):
    print(option + dep)
    if option != '' and dep != '':
        return '{}'.format(dep)

app.run_server(debug = False)