import kagglehub

# Download latest version
path = kagglehub.dataset_download("rohankayan/years-of-experience-and-salary-dataset")
print("Path to dataset files:", path)
filename = "Salary_Data.csv"

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# ========================================
# 1. Lecture des données depuis le CSV
# ========================================

df = pd.read_csv(f"{path}/{filename}")

# Colonnes : "YearsExperience" en abscisse, "Salary" en ordonnée
X = df[["YearsExperience"]].values
Y = df["Salary"].values

# ========================================
# 2. Entraînement du modèle
# ========================================

model = LinearRegression()
model.fit(X, Y)

# Obtenir les points de la droite de régression
x_line = pd.Series(X.flatten()).sort_values().values
y_line = model.predict(x_line.reshape(-1,1))

# ========================================
# 3. Application Dash
# ========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("Régression : Salaire vs Expérience"),

    dcc.Graph(id="graph"),

    html.Div([
        html.Label("Années d'expérience :"),
        dcc.Slider(
            id="x-slider",
            min=float(df["YearsExperience"].min()),
            max=float(df["YearsExperience"].max()),
            step=0.1,
            value=float(df["YearsExperience"].mean()),
            marks={round(val,1): str(round(val,1)) for val in df["YearsExperience"].unique()}
        )
    ],
    style={"width": "80%", "margin": "auto"}),

    html.Div(id="prediction-text",
             style={"textAlign": "center", "fontSize": "18px", "marginTop": "20px"})
])

# ========================================
# 4. Callback Dash
# ========================================

@app.callback(
    Output("graph", "figure"),
    Output("prediction-text", "children"),
    Input("x-slider", "value")
)
def update_graph(x_value):

    # Prédiction à partir du slider
    y_pred = model.predict([[x_value]])[0]

    fig = go.Figure()

    # Nuage de points
    fig.add_trace(go.Scatter(
        x=X.flatten(),
        y=Y,
        mode="markers",
        name="Données Salary"
    ))

    # Droite de régression
    fig.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode="lines",
        name="Droite de régression"
    ))

    # Point prédit pour la valeur slider
    fig.add_trace(go.Scatter(
        x=[x_value],
        y=[y_pred],
        mode="markers",
        marker=dict(size=12, color="red"),
        name="Prédiction"
    ))

    fig.update_layout(
        xaxis_title="Années d'expérience",
        yaxis_title="Salaire",
        title="Salaire prédit en fonction de l'expérience",
        template="plotly_white"
    )

    text = f"Prédiction : Salaire ≈ {y_pred:.2f} pour {x_value:.1f} années"

    return fig, text

# ========================================
# 5. Lancement
# ========================================

if __name__ == "__main__":
    app.run_server(debug=True)
