from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1("My Dashboard is Working!"),
    html.P("If you see this, everything is fine.")
])

if __name__ == '__main__':
    app.run(debug=True, port=8051)