import dash
from dash import Input, Output
from layout import create_layout, index_string
from carte import register_carte_callbacks

app = dash.Dash(__name__)
app.index_string = index_string
app.layout = create_layout()

register_carte_callbacks(app)


@app.callback(
    Output("sidebar", "className"),
    Input("btn-toggle-sidebar", "n_clicks"),
    prevent_initial_call=True
)
def toggle_sidebar(n):
    return "sidebar collapsed" if n % 2 == 1 else "sidebar"


if __name__ == '__main__':
    app.run(debug=True, port=5003)