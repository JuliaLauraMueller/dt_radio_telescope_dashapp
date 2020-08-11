import os.path
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pickle
import util.helpers
from util import datamodel
from util import components
import time

# Measurement time
start_time = time.time()

# data for data model
data_path = './Output/'
models = dict()
index = 0
for folder in os.listdir(data_path):
    if folder.startswith("vla_c"):
        with open(data_path + folder + "/sources.pkl", "rb") as inputfile:
            sources = pickle.load(inputfile)
            directions = []
            for source in sources:
                direction = (source['sp_direction_ra'], source['sp_direction_dec'])
                directions.append(direction)
        models.update({folder: datamodel.Datamodel(data_path + folder + "/FITS_Files/", directions, folder, index)})
        index += 1

model = models[next(iter(models))]
print("Time to create objects:")
print("--- %s seconds ---" % (time.time() - start_time))

# ****************************************************************************************

# CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#FFFFFF',
    'text': '#E9E9E9'
}

# Card for Dropdown
dropdownCard = components.dropdown_card(models)

# Card for observing images
img_sky = app.get_asset_url('Skymodel.png')
img_psf = app.get_asset_url('psf.png')
observeCard = components.observing_card(img_sky, img_psf)

# Card for analyzing plots
flatCard = components.analyze_card(model.flat)
residualCard = components.analyze_card(model.residual)
fidelityCard = components.analyze_card(model.fidelity)

# ****************************************************************************************

# Layout
app.layout = html.Div(style={'backgroundColor': '#F0F1F9', 'width': '100%', 'height': '100%'}, children=[

    html.Div(children=[
        html.H1(children='Simulated Radio Observation', style={'color': colors['text'], 'padding': '4rem',
                                                     'backgroundColor': '#18207A', 'font-size': '4.5em'}),
    ]),

    html.Div(children=[
        dbc.Row([
            # *************
            # Output folder dropdown
            dbc.Col([
                html.Div([dropdownCard],
                         className="row", style={'margin': '1.5rem'}),
            ], width=12),

            # *************
            # Observe output (Skymodel & PSF)
            dbc.Col([
                html.Div([observeCard],
                         className="row", style={'margin': '1.5rem'}),
            ], width=12)
        ], className="row"),

        # *************
        # Analysis
        html.Div([
            dbc.Row([flatCard], id='card_flat')
        ], className="row", style={'margin': '1.5rem'}),

        html.Div([
            dbc.Row([residualCard], id='card_residual')
        ], className="row", style={'margin': '1.5rem'}),

        html.Div([
            dbc.Row([fidelityCard], id='card_fidelity')
        ], className="row", style={'margin': '1.5rem'})
    ], style={'margin': '3em'}),
])


# ****************************************************************************************
@app.callback(
    [Output('card_flat', 'children'),
     Output('card_residual', 'children'),
     Output('card_fidelity', 'children')],
    [Input('dropdown', 'value')])
def load_data(folder):
    """
    Returns loaded data model image.

    :param folder: The given folder
    :return: image cards: All images card of flat, residual and fidelity
    """
    model = models[folder]
    flat_card = components.analyze_card(model.flat)
    residual_card = components.analyze_card(model.residual)
    fidelity_card = components.analyze_card(model.fidelity)
    return flat_card, residual_card, fidelity_card


@app.callback(
    Output(model.flat.name + "-hist", 'figure'),
    [Input(model.flat.name + "-image", 'relayoutData')])
def update_hist(relayoutData):
    """
    Updates histogram when specific region was selected on flat image.

    :param relayoutData: The re-layouted data
    :return: fig: Updated histogram figure
    """
    if relayoutData is None:
        fig = model.flat.hist
    else:
        if 'xaxis.range[0]' in relayoutData:
            x0 = int(round(relayoutData['xaxis.range[0]']))
            x1 = int(round(relayoutData['xaxis.range[1]']))
            y0 = int(round(relayoutData['yaxis.range[0]']))
            y1 = int(round(relayoutData['yaxis.range[1]']))
            data = model.flat.data[x0:x1, y0:y1]
            fig = util.helpers.create_hist(data, 'Flat Distribution')
        else:
            fig = model.flat.hist
    return fig


@app.callback(
    Output(model.residual.name + "-hist", 'figure'),
    [Input(model.residual.name + "-image", 'relayoutData')])
def update_hist(relayoutData):
    """
    Updates histogram when specific region was selected on residual image.

    :param relayoutData: The re-layouted data
    :return: fig: Updated histogram figure
    """
    if relayoutData is None:
        fig = model.residual.hist
    else:
        if 'xaxis.range[0]' in relayoutData:
            x0 = int(round(relayoutData['xaxis.range[0]']))
            x1 = int(round(relayoutData['xaxis.range[1]']))
            y0 = int(round(relayoutData['yaxis.range[0]']))
            y1 = int(round(relayoutData['yaxis.range[1]']))
            data = model.residual.data[x0:x1, y0:y1]
            fig = util.helpers.create_hist(data, 'Flat Distribution')
        else:
            fig = model.residual.hist
    return fig


@app.callback(
    Output(model.fidelity.name + "-hist", 'figure'),
    [Input(model.fidelity.name + "-image", 'relayoutData')])
def update_hist(relayoutData):
    """
    Updates histogram when specific region was selected on fidelity image.

    :param relayoutData: The re-layouted data
    :return: fig: Updated histogram figure
    """
    if relayoutData is None:
        fig = model.fidelity.hist
    else:
        if 'xaxis.range[0]' in relayoutData:
            x0 = int(round(relayoutData['xaxis.range[0]']))
            x1 = int(round(relayoutData['xaxis.range[1]']))
            y0 = int(round(relayoutData['yaxis.range[0]']))
            y1 = int(round(relayoutData['yaxis.range[1]']))
            data = model.fidelity.data[x0:x1, y0:y1]
            fig = util.helpers.create_hist(data, 'Flat Distribution')
        else:
            fig = model.fidelity.hist
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host='127.0.0.1')

