import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# =============================
# 1. Génération de données
# =============================

np.random.seed(0)

X = np.linspace(0, 10, 30)
Y = 2.5 * X + 3 + np.random.normal(0, 3, size=len(X))

X = X.reshape(-1, 1)

# =============================
# 2. Entraînement du modèle
# =============================

model = LinearRegression()
model.fit(X, Y)

# Droite de régression
#x_line = np.linspace(0, 10, 100)
x_line = [0, 10]
#y_line = model.predict(x_line.reshape(-1, 1))
y_line = [model.predict([[0]])[0], model.predict([[10]])[0]]
# =============================
# 3. Application Dash
# =============================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("Régression linéaire interactive"),

    dcc.Graph(id="graph"),

    html.Div([
        html.Label("Valeur de x :"),

        dcc.Slider(
            id="x-slider",
            min=0,
            max=10,
            step=0.1,
            value=5,
            marks={i: str(i) for i in range(11)}
        )
    ],
    style={"width": "80%", "margin": "auto"}),

    html.Div(id="prediction-text",
             style={"textAlign": "center",
                    "fontSize": "18px",
                    "marginTop": "20px"})
])

# =============================
# 4. Callback
# =============================

@app.callback(
    Output("graph", "figure"),
    Output("prediction-text", "children"),
    Input("x-slider", "value")
)
def update_graph(x_value):

    # Prédiction
    y_pred = model.predict([[x_value]])[0]

    fig = go.Figure()

    # Nuage de points
    fig.add_trace(go.Scatter(
        x=X.flatten(),
        y=Y,
        mode="markers",
        name="Données"
    ))

    # Droite de régression
    fig.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode="lines",
        name="Régression"
    ))

    # Point prédit
    fig.add_trace(go.Scatter(
        x=[x_value],
        y=[y_pred],
        mode="markers",
        marker=dict(size=12),
        name="Prédiction"
    ))

    fig.update_layout(
        xaxis_title="x",
        yaxis_title="y",
        title="Nuage de points et droite de régression",
        template="plotly_white"
    )

    text = f"Valeur prédite : y = {y_pred:.2f}"

    return fig, text


# =============================
# 5. Lancement
# =============================

if __name__ == "__main__":
    app.run_server(debug=True)
