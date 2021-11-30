# Environment used: dash1_8_0_env
import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.0)
import plotly.express as px

import dash  # (version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# print(px.data.gapminder()[:15])

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        dcc.Dropdown(
            id='dropdown_state',
            options=[
                {'label': 'World Happiness', 'value': 'Score'},
                {'label': 'GDP Per Capita', 'value': 'GDP per capita'},
                {'label': 'Social Support', 'value': 'Social support'},
                {'label': 'Healthy Life Expectancy',
                    'value': 'Healthy life expectancy'},
                {'label': 'Freedom to Make Life Choices',
                    'value': 'Freedom to make life choices'},
                {'label': 'Generosity', 'value': 'Generosity'},
                {'label': 'Perceptions of Corruption',
                    'value': 'Perceptions of corruption'},
            ],
            value='Score',
            style={'width': '50%', 'margin-left': '25%', 'margin-right': '25%'}
        ),
        html.Button(id='submit_button', n_clicks=0, children='Update', style={
                    'margin-top': '8px', 'margin-bottom': '8px'}),
        html.Div(id='output_state'),
    ], style={'text-align': 'center', 'align-items': 'center', 'justify-content': 'center'}),

])

# ---------------------------------------------------------------


@app.callback(
    [Output('output_state', 'children'),
     Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='dropdown_state', component_property='value')]
)
def update_output(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        df = pd.read_csv("whr2019.csv")

        # update range on side of graph according to each column
        key_range = [0, 2]
        if val_selected == "Score":
            key_range = [3, 8]
        elif val_selected == "Healthy life expectancy":
            key_range = [0, 1.1]
        elif val_selected == 'Freedom to make life choices':
            key_range = [0, 0.7]
        elif val_selected == 'Generosity' or val_selected == 'Perceptions of corruption':
            key_range = [0, 0.5]

        fig = px.choropleth(df, locations="Alpha-3 code",
                            color=val_selected,
                            hover_name="Country or region",
                            hover_data={'Overall rank': True, 'Country or region': True, 'Score': True, 'GDP per capita': True, 'Social support': True,
                                        'Healthy life expectancy': True, 'Freedom to make life choices': True, 'Generosity': True, 'Perceptions of corruption': True, 'Alpha-3 code': True},
                            projection='natural earth',
                            title='World Happiness Rating',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            range_color=key_range)

        fig.update_layout(title=dict(font=dict(size=28), x=0.5, xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))

        return ('Current Map: {}'.format(val_selected), fig)


if __name__ == '__main__':
    app.run_server(debug=True)
