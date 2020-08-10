# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


#########################
# Card for Output-folder
#########################

def dropdown_card(models):
    """
    Returns a dropdown card with output folders for analysing.

    :param models: The data model with the CASA images
    :return: Card: The card for the dropdown
    """
    options = []
    for key in models:
        options.append({'label': key, 'value': key})

    dropdown = dcc.Dropdown(
        id='dropdown',
        options=options,
        value=options[0]['value'],
        style={'width': '620px', 'height': '40px', 'fontSize': '12pt'}
    )
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4('Model Selection', style={'color': colors['text']}),
                dbc.Row(children=[
                    dbc.Col(
                        html.Div(["Select output folder: "]), width=3),
                    dbc.Col(
                        html.Div([dropdown]), width=9),
                ])
            ]), style={"width": "50%"}
    )


#########################
# Card for Observation
#########################

def observing_card(img_sky, img_psf):
    """
    Returns a card with sky-model and the psf-image for analysing.

    :param img_sky: The sky-model image
    :param img_psf: The psf image
    :return: Card: The card with the sky-model and psf images
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4('Output of Observation', style={'color': colors['text']}),
                dbc.Row(children=[
                    dbc.Col(
                        html.Div([
                            html.Img(src=img_sky)
                        ], className="six columns")),
                    dbc.Col(
                        html.Div([
                            html.Img(src=img_psf)
                        ], className="six columns")),
                ])
            ]), style={"width": "50%"}
    )


#########################
# Card for Analyzing
#########################

def analyze_card(casa_image):
    """
    Returns a card with casa images of flat-image, residual and fidelity and its histograms and statistical information.

    :param casa_image: The given casa image
    :return: Card: The card with the casa images
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4('Analysis of ' + casa_image.name + '-Image', style={'color': colors['text']}),
                dbc.Row([
                    # Image & Stats
                    dbc.Col([
                        dbc.Row([
                            dbc.Col(
                                html.Div([
                                    dcc.Graph(figure=casa_image.image, id=casa_image.name + "-image")
                                ], className="six columns"))
                        ]),
                        html.H4('Statistical information', style={'color': colors['text'], 'marginLeft': 70}),
                        dbc.Row([
                            dbc.Col(
                                html.Div([
                                    dcc.Markdown('maximum pixel value: ' + str(casa_image.stats['max'])),
                                    dcc.Markdown('minimum pixel value: ' + str(casa_image.stats['min'])),
                                    dcc.Markdown('mean pixel value: ' + str(casa_image.stats['mean'])),
                                    dcc.Markdown('median pixel value: ' + str(casa_image.stats['median']))
                                ], className="six columns", style={'marginLeft': 70})
                            ),
                            dbc.Col(
                                html.Div([
                                    dcc.Markdown('standard deviation about mean: ' + str(casa_image.stats['sigma'])),
                                    dcc.Markdown('sum of pixel values: ' + str(casa_image.stats['sum'])),
                                    dcc.Markdown('size of all pixel values: ' + str(casa_image.stats['size']))
                                ], className="six columns")
                            ),
                        ], className="six columns")
                    ]),
                    # Hists
                    dbc.Col([
                        html.Div([
                            dcc.Graph(figure=casa_image.hist, id=casa_image.name + "-hist")
                        ]),
                        html.Div([
                            dcc.Graph(figure=casa_image.hist_onsource, id=casa_image.name + 'onsource_hist')
                        ]),
                        html.Div([
                            dcc.Graph(figure=casa_image.hist_offsource, id=casa_image.name + 'offsource_hist')
                        ])
                    ],
                        className="six columns")
                ])
            ]), id=casa_image.name + '-card', style={"width": "100%"}
    )


#########################
# Further Templates
#########################

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

