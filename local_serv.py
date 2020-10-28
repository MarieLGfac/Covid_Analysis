import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import visdcc
import analytics
import api
from departements import departement_data

class CustomDash(dash.Dash):
    
    def setLayout(self, options):
        self.layout = html.Div([
                        html.Header([
                            html.A(html.Img(src='assets/hexa.png', id='logo')),
                            html.H1('ANALYSIS'),
                            dcc.Dropdown(
                                id='dropdown-1',
                                options=[{'label': i, 'value': i} for i in options],
                                value='',
                            ),
                            html.Div(id='depDropdown'),
                            html.Button('Actualiser les données', id = 'button-1'),
                        ]),
                        html.Div(id='output'),
                        visdcc.Run_js(id = 'javascript'),
                        html.Footer([
                            html.Nav([
                                html.Ul([
                                    html.Li(html.P(' ')),
                                    html.Li(html.P(' ')),
                                    html.Li(html.P(' '))
                                ])
                            ])
                        ])
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
    [Input('dropdown-1', 'value'), Input('dropdown-2', 'value')]
)
def buildGraph(option, dep):
    if option is not None and dep != '':
        print(option)
        graph = analytics.Analytics()
        return dcc.Graph(figure=graph.DeathDepGraph(option, dep)) 

app.run_server(debug = False)