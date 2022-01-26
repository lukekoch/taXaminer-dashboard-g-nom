import json

import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table


class Layout:
    def get_layout(self, dropdowns, scatter_test, my_dataset):
        """
        Builds an returns a layout
        :param dropdowns: Dropdown options for dataset selection
        :param scatter_test: scatterplot
        :param my_dataset: initial dataset
        :return: dash.Layout component
        """

        # initial table variables
        variable_items = []

        with open("./static/glossary.json") as f:
            glossary = json.load(f)

        variables = my_dataset.get_data_original().columns.values.tolist()
        for variable in variables:
            if str(variable) in glossary:
                variable_items.append({"label": glossary[str(variable)]['short'],"value": str(variable)})
            else:
                variable_items.append(
                    {"label": str(variable), "value": str(variable)})

        layout = dbc.Container(fluid=True, children=[
            dbc.NavbarSimple(
                brand="MILTS",
                brand_href="#",
                color="primary",
                dark=True,
                fluid=True,
            ),
            dbc.Row(
                [
                    # wide scatterplot
                    dbc.Col(width=8, children=[
                        dcc.Graph(
                            id="scatter3d",
                            config={"displayModeBar": True},
                            animate=True,
                            className="plot"
                        )]),

                    # tabbed side menu
                    dbc.Col(width=4, children=[
                        dbc.Tabs(children=[
                            dbc.Tab(label='Overview',
                                    children=[
                                        # Dataset Selection
                                        html.Hr(),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Card([
                                                    dbc.CardHeader(
                                                        "Select Dataset"),
                                                    dcc.Dropdown(
                                                        id='dataset_select',
                                                        options=dropdowns,
                                                        value=dropdowns[0].get(
                                                            'value')
                                                    )
                                                ], className="m-2"),
                                                dbc.Card([
                                                    dbc.CardHeader(
                                                        "Dataset Summary"),
                                                    dcc.Textarea(
                                                        id='summary',
                                                        value='Textarea',
                                                        disabled=True,
                                                        style={'height': 150,
                                                               'width': 'fill',
                                                               "verticalAlign": "top",
                                                               'horizontalAlign': 'left'},
                                                    ),
                                                ], className="m-2"),
                                                dbc.Card([
                                                    dbc.CardHeader(
                                                        "Selected Gene"),
                                                    dcc.Textarea(
                                                        id='textarea-taxon',
                                                        value='Textarea content initialized\nwith multiple lines of text',
                                                        disabled=True,
                                                        style={'height': 200,
                                                               'width': 'fill',
                                                               "verticalAlign": "top",
                                                               'horizontalAlign': 'left'},
                                                    ),
                                                    html.Div([
                                                        dbc.Button(
                                                            "Find Best hit on NCBI",
                                                            id='NCBI',
                                                            href="https://www.ncbi.nlm.nih.gov/",
                                                            external_link=True,
                                                            color='primary',
                                                            target='_blank',
                                                        ),
                                                    ],
                                                        className="d-grid gap-2")
                                                ], className="m-2"),
                                                dbc.Card([
                                                    dbc.CardHeader(
                                                        "Amino Acid Sequence"),
                                                    dcc.Textarea(
                                                        id='textarea-as',
                                                        value='Select a datapoint',
                                                        disabled=True,
                                                        style={'height': 200,
                                                               'width': 'fill',
                                                               "verticalAlign": "top",
                                                               'horizontalAlign': 'left'},
                                                    ),
                                                ], className="m-2")
                                            ], align='center')
                                        ], align='end'),
                                        # display gene information
                                    ], className="m-2"),
                            dbc.Tab([
                                dbc.Card([
                                    dbc.CardHeader("Enable/Disable Filters"),
                                    dbc.Checkbox(label="Scatterplot legend",
                                                 className="m-1 form-switch"),
                                    dbc.Checkbox(label="e-value",
                                                 className="m-1 form-switch"),
                                    dbc.Checkbox(label="Ignore unassigned",
                                                 className="m-1 form-switch"),
                                    dbc.Checkbox(label="Ignore non-coding",
                                                 className="m-1 form-switch"),
                                    dbc.Checkbox(label="Filter by scaffolds",
                                                 className="m-1 form-switch"),
                                ], className="m-2"),
                                dbc.Card([
                                    dbc.CardHeader("e-value Filter"),
                                    dcc.Slider(
                                        id='evalue-slider',
                                        min=0,
                                        max=300,
                                        value=0,
                                        step=10,
                                        marks={0: {'label': 'e^0', 'style': {
                                            'color': '#77b0b1'}},
                                               100: {'label': 'e^-100',
                                                     'style': {
                                                         'color': '#77b0b1'}},
                                               200: {'label': 'e^-200',
                                                     'style': {
                                                         'color': '#77b0b1'}},
                                               300: {'label': 'e^-300',
                                                     'style': {
                                                         'color': '#77b0b1'}}},
                                        className="m-2",
                                    ),
                                ], className="m-2"),
                            ], label="Filter", className="m-2"),
                            dbc.Tab(label='PCA', children=[
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardHeader("PCA Data"),
                                            dcc.Graph(
                                                id="contribution"
                                            ),
                                            dcc.Graph(
                                                id="scree"
                                            )
                                        ])
                                    ])
                                ]),
                            ]),
                            # scatter matrix
                            dbc.Tab(label='Scatter Matrix', children=[
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Graph(id='scatter_matrix',
                                                  figure=scatter_test,
                                                  responsive=True),
                                    ])
                                ]),
                            ]),
                        ]),
                    ]),
                ]
            ),
            html.Hr(),
            dbc.NavbarSimple(
                brand="Data Selection",
                brand_href="#",
                color="primary",
                dark=True,
                fluid=True,
            ),
            dbc.Row([
                dbc.Col(width=8, children=[
                    dbc.Tabs([
                        dbc.Tab([
                            dbc.Row([
                                dbc.Col([
                                    dbc.ButtonGroup([
                                        dbc.Button(
                                            html.Span(["", html.I(
                                                className="fas fa-plus-circle")]),
                                            color="success",
                                            size="md",
                                            id="button_add"),
                                        dbc.Button(
                                            html.Span(["", html.I(
                                                className="fas fa-pause-circle")]),
                                            color="secondary",
                                            size="md",
                                            id="button_neutral"
                                        ),
                                        dbc.Button(
                                            html.Span(["", html.I(
                                                className="fas fa-minus-circle")]),
                                            color="danger",
                                            size="md",
                                            id="button_remove"
                                        )],
                                        className="d-flex m-2 radio-group"
                                                  " btn-block"
                                    ),
                                ]),
                                dbc.Col([
                                    dbc.Row([
                                        dbc.ButtonGroup([
                                            dbc.Button([
                                                html.Span(["", html.I(className="fas fa-eye"), html.Span(" Add all visible")])],
                                                color="success",
                                                id="button_add_legend_to_select",
                                            ),
                                            dbc.Button([
                                                html.Span(["", html.I(
                                                    className="fas fa-trash"),
                                                           html.Span(
                                                               " Reset selection")])],
                                                color="danger",
                                                id="button_reset"
                                            ),
                                            dbc.Button([
                                                html.Span(
                                                    ["", html.I(className="fas fa-arrow-alt-circle-down"),
                                                     html.Span(" Download selection")])],
                                                color="primary",
                                                id='btn-download'
                                            ),
                                        ], className="d-flex m-2 radio-group"
                                                     " btn-block"),
                                        dcc.Download(id="download-selection"),
                                    ]),
                                ]),
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Input(
                                            id='searchbar',
                                            placeholder="Enter Gene Name",
                                            invalid=True,
                                            className="d-flex m-2 radio-group"
                                        ),
                                    ])
                                ], width=2),
                                # table containing only selected assignments
                                dash_table.DataTable(
                                    id='table_selection',
                                    columns=[{"name": "Gene Name",
                                              "id": "g_name"},
                                             {"name": "Best Hit",
                                              "id": "best_hit"},
                                             {"name": "e-value",
                                              "id": "bh_evalue"}],
                                    data=my_dataset.get_data_original().to_dict(
                                        'records'),
                                ),
                            ], className="d-flex m-2"),
                        ], label="Download Selection"),

                        dbc.Tab([
                            dbc.Card([
                                # table containing all assignments
                                dash_table.DataTable(
                                    id='table_all',
                                    columns=[{"name": "Gene Name",
                                              "id": "g_name"},
                                             {"name": "Best Hit",
                                              "id": "best_hit"},
                                             {"name": "e-value",
                                              "id": "bh_evalue"}],
                                    data=my_dataset.get_data_original().to_dict(
                                        'records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                ),
                            ], className="m-2"),
                        ], label="Full Dataset"),

                        dbc.Tab([
                            dbc.Card([
                                # table containing only selected taxa
                                dash_table.DataTable(
                                    id='legend_selection',
                                    columns=[{"name": "Gene Name",
                                              "id": "g_name"},
                                             {"name": "Taxon",
                                              "id": "plot_label"},
                                             {"name": "e-value",
                                              "id": "bh_evalue"}],
                                    data=my_dataset.get_data_original().to_dict(
                                        'records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                ),
                            ], className="m-2"),
                        ], label="Taxa visible in plot"),
                    ]),
                ]),
                dbc.Col([
                    dbc.Tabs([
                        dbc.Tab([
                            dbc.Label("Select variables visible in tables:"),
                            dcc.Dropdown(
                                options=variable_items,
                                multi=True,
                                id='variable-selection',
                                # these are the initially displayed variables
                                value=['g_name', 'plot_label', 'bh_evalue']
                            ),
                        ], label="Variables"),
                        # Download Tab
                        dbc.Tab([
                            dbc.Card([
                                dbc.CardHeader("BLAST"),
                            ], className="m-2"),
                        ], label="Tools")
                    ]),
                ], width=4)
            ]),
        ])

        # finally, return out layout
        return layout