from skimage.transform import resize
import dash
import dash_daq as daq
from dash.exceptions import PreventUpdate
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash_canvas import DashCanvas
from base64 import b64encode
from dash_canvas.utils import parse_jsonstring

from serve_thermo import Simulation

app = dash.Dash(__name__, title='FEM Heat Conduction', 
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport', 
                            'content': 'width=device.width, initial_scale=1.0'}]
                )

server = app.server   

def serve_layout():
    layout = html.Div([
        
        html.Div([
            html.Div([
                html.H1('FINITE ELEMENTS HEAT PAINTER'),
                html.P('''
                    Use your mouse to draw curves on the canvas. When you press "Start",
                    temperature is computed using the curves as heat sources -  or heat sinks 
                    if your heart desires. Happy painting!
                ''')
            ], id="info-container"),
            
            html.Div([
                DashCanvas(
                    id='canvas', 
                    width=500,
                    height=500,
                    lineColor='white',
                    hide_buttons=['pencil', 'line', 'rectangle', 'zoom', 'pan', 'undo', 'redo', 'select']
                ),
                html.Div([
                    html.Button('Reset', id="reset-btn", n_clicks=0),
                    # html.Div([
                    #     html.P('Heat source', id="heat-label"),
                    #     daq.BooleanSwitch(id='sign', on=True),
                    # ], id='switch-container'),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Source', 'value': 1},
                            {'label': 'Sink', 'value': -1},
                        ], value=1, id="radio-items"),
                ], id="controls-container"),
            ], id="canvas-container"),
        ], id="main-wrapper"),

        html.Div([
            html.P('\u00a9 Mallory Wittwer, 2022', className="copyright"),
            html.A("View code", id="code", href="#", target="_blank"),
        ], id="footer-container"),
        
        dcc.Interval(id='interval', interval=200, n_intervals=0),
        html.Div(id="void", style={ 'display': 'none' }),
        html.Div(id="void2", style={ 'display': 'none' }),
    ], id="main")
    return layout

app.layout = serve_layout

SIMULATION = Simulation()

@app.callback(
    Output("canvas", "image_content"),
    Input('interval', 'n_intervals'),
)
def update_simulation(n):    
    SIMULATION.step()
    fig = SIMULATION.get_heatmap()
    im = "data:image/png;base64," + b64encode(fig.to_image(format="png")).decode()
    return im

@app.callback(
    # Output('heat-label', 'children'),
    Output('void2', 'children'),
    Input('canvas', 'json_data'),
    # Input("sign", "on"),
    Input("radio-items", "value"),
)
def update(data_string, sign):    
    mask = resize(
        parse_jsonstring(data_string), 
        (SIMULATION.n_x, SIMULATION.n_y)
    )
    SIMULATION.set_heat_source_mask(mask, sign) #1 if sign else -1)
    return []#f"Heat {'source' if sign else 'sink'}"

@app.callback(
    Output('void', 'children'),
    Input("reset-btn", "n_clicks"),
)
def reset(_):
    SIMULATION.reset()
    return []

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
