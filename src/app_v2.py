import kagglehub

# Download latest version
path = kagglehub.dataset_download("rohankayan/years-of-experience-and-salary-dataset")
print("Path to dataset files:", path)
filename = "Salary_Data.csv"

import pandas as pd
import numpy as np

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.linear_model import LinearRegression


# ========================================
# 1. Chargement des données
# ========================================

df = pd.read_csv(f"{path}/{filename}")

X = df[["YearsExperience"]].values
Y = df["Salary"].values


# ========================================
# 2. Entraînement du modèle
# ========================================

model = LinearRegression()
model.fit(X, Y)

# Droite de régression
x_line = np.linspace(X.min(), X.max(), 200)
y_line = model.predict(x_line.reshape(-1, 1))


# ========================================
# 3. Application Dash
# ========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("Régression linéaire + Histogramme interactif",
            style={"textAlign": "center"}),

    dcc.Graph(
        id="main-graph",
        style={"height": "600px"}
    ),

    html.Div(
        id="prediction-text",
        style={
            "textAlign": "center",
            "fontSize": "18px",
            "marginTop": "15px"
        }
    ),

    # Stockage de la valeur x sélectionnée
    dcc.Store(id="selected-x", data=float(X.mean()))

])


# ========================================
# 4. Callback principal
# ========================================

@app.callback(
    Output("main-graph", "figure"),
    Output("prediction-text", "children"),
    Output("selected-x", "data"),

    Input("main-graph", "clickData"),
    State("selected-x", "data")
)
def update_graph(clickData, stored_x):

    # ---------------------------
    # Gestion du clic
    # ---------------------------

    x_value = stored_x

    if clickData is not None:

        # Vérifie si le clic vient de l'histogramme
        # if clickData is not None:
        point = clickData["points"][0]

        # Si un x est disponible (cas de l'histogramme)
        if "x" in point:
            x_value = float(point["x"])

    # ---------------------------
    # Prédiction
    # ---------------------------

    y_pred = model.predict([[x_value]])[0]


    # ========================================
    # Création des sous-graphiques
    # ========================================

    fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.65, 0.35],
        subplot_titles=(
            "Données et régression",
            "Histogramme de X (cliquer)"
        )
    )


    # ========================================
    # Graphe 1 : Régression
    # ========================================

    # Nuage
    fig.add_trace(
        go.Scatter(
            x=X.flatten(),
            y=Y,
            mode="markers",
            name="Données"
        ),
        row=1, col=1
    )

    # Droite
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Régression"
        ),
        row=1, col=1
    )

    # Point prédit
    fig.add_trace(
        go.Scatter(
            x=[x_value],
            y=[y_pred],
            mode="markers",
            marker=dict(size=12, color="red"),
            name="Prédiction"
        ),
        row=1, col=1
    )


    # ========================================
    # Graphe 2 : Histogramme
    # ========================================

    fig.add_trace(
        go.Histogram(
            x=X.flatten(),
            nbinsx=12,
            name="Distribution X",
            opacity=0.7
        ),
        row=1, col=2
    )


    # Ligne verticale sur X sélectionné
    fig.add_vline(
        x=x_value,
        line_dash="dash",
        line_color="red",
        row=1,
        col=2
    )


    # ========================================
    # Mise en page
    # ========================================

    fig.update_layout(
        template="plotly_white",
        showlegend=True,
        title="Sélection via histogramme → prédiction",
        clickmode="event+select"
    )

    fig.update_xaxes(
        title_text="Années d'expérience",
        row=1, col=1
    )

    fig.update_yaxes(
        title_text="Salaire",
        row=1, col=1
    )

    fig.update_xaxes(
        title_text="Années d'expérience",
        row=1, col=2
    )

    fig.update_yaxes(
        title_text="Effectif",
        row=1, col=2
    )


    # ========================================
    # Texte
    # ========================================

    text = (
        f"Valeur sélectionnée : x = {x_value:.2f}  →  "
        f"Salaire prédit ≈ {y_pred:.2f}"
    )

    return fig, text, x_value


# ========================================
# 5. Lancement
# ========================================

if __name__ == "__main__":
    app.run_server(debug=True)
