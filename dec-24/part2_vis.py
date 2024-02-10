from dash import Dash, html, dcc, Input, Output, callback
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

data = []

with open('input.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        pos, speed = line.strip().split('@')
        data.append((
            tuple(int(x) for x in pos.split(',')),
            tuple(int(x) for x in speed.split(',')),
        ))


n = len(data)


def plot(axis, mult, title):
    fig = go.Figure(layout_title_text=title)

    for idx in range(n):
        pos, vel = data[idx]

        x = []
        y = []

        xaxis, yaxis = axis

        x.append(pos[xaxis])
        y.append(pos[yaxis])

        x.append(pos[xaxis] + vel[xaxis] * mult)
        y.append(pos[yaxis] + vel[yaxis] * mult)

        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line={
            'width': 1,
        }))

    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', showlegend=False)
    fig.update_xaxes(gridcolor='rgba(0, 0, 0, 0.05)')
    fig.update_yaxes(gridcolor='rgba(0, 0, 0, 0.05)')

    return fig


@callback([
        Output(component_id='plot', component_property='figure'),
        Output(component_id='plot2', component_property='figure')
    ],
    Input(component_id='slider', component_property='value'),
)
def update(value):
    return (
        plot((0, 1), value, 'xy'),
        plot((0, 2), value, 'xz'),
    )


if __name__ == '__main__':
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div(children=[
        dcc.Slider(
            0, 10 ** 12,
            updatemode='drag',
            value=4 * 10**10,
            id='slider'),
        html.Div(children=[
            dbc.Row([
                dbc.Col(html.Div(children=[
                    dcc.Graph(
                        id='plot',
                        figure={
                            'layout': {
                                'height': '1000',
                            }
                        }
                    )])),
                dbc.Col([
                    dcc.Graph(
                        id='plot2',
                        figure={
                            'layout': {
                                'height': '1000',
                            }
                        }
                    )]),
                ]),
        ]),
    ])

    app.run(debug=True)
