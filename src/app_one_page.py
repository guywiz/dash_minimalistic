import dash
from dash import dcc, html, Input, Output, State, callback

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go

# =====================================================
# App
# =====================================================
app = dash.Dash(__name__)

server = app.server


# =====================================================
# Data
# =====================================================
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

iris_df = pd.DataFrame(X, columns=feature_names)
iris_df["target"] = y

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X, y)

# Default = mean values
default_values = iris_df[feature_names].mean().to_dict()

# =====================================================
# Layout
# =====================================================
app.layout = html.Div(
        style={"padding": "20px"},
        children=[
            html.H2("Prédiction – Random Forest (Iris)"),
            html.Hr(),

            dcc.Store(
                id="selected-values",
                data=default_values,
            ),

            html.Div(
                style={"display": "flex"},
                children=[

                    # ================= Left panel =================
                    html.Div(
                        style={"width": "60%"},
                        children=[
                            html.H4("Sélection des variables"),

                            html.Div(
                                children=[
                                    dcc.Graph(
                                        id=f"hist-{i}",
                                        config={"displayModeBar": False},
                                    )
                                    for i in range(len(feature_names))
                                ]
                            ),
                        ],
                    ),

                    # ================= Right panel =================
                    html.Div(
                        style={
                            "width": "40%",
                            "paddingLeft": "30px",
                            "textAlign": "center",
                        },
                        children=[
                            html.H4("Résultat"),

                            html.Div(
                                id="prediction-output",
                                style={"fontSize": "22px", "marginTop": "20px"},
                            ),

                            html.Br(),

                            html.Div(
                                id="proba-output",
                                style={"fontSize": "16px"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

# =====================================================
# Histogram helper
# =====================================================

def make_histogram(feature, selected_value):

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=iris_df[feature],
            nbinsx=20,
            opacity=0.7,
        )
    )

    # Selected value
    fig.add_vline(
        x=selected_value,
        line_dash="dash",
        line_width=2,
    )

    fig.update_layout(
        title=feature,
        height=230,
        margin=dict(l=40, r=20, t=40, b=40),
        showlegend=False,
    )

    return fig


# =====================================================
# Update histograms
# =====================================================
@callback(
    [Output(f"hist-{i}", "figure") for i in range(len(feature_names))],
    Input("selected-values", "data"),
)
def update_histograms(selected_values):

    figs = []

    for i, f in enumerate(feature_names):
        val = selected_values[f]
        figs.append(make_histogram(f, val))

    return figs


# =====================================================
# Click handling
# =====================================================
@callback(
    Output("selected-values", "data"),
    [Input(f"hist-{i}", "clickData") for i in range(len(feature_names))],
    State("selected-values", "data"),
    prevent_initial_call=True,
)
def update_selected_values(*args):

    *clicks, current = args

    new_vals = current.copy()

    for i, click in enumerate(clicks):
        if click:
            x = click["points"][0]["x"]
            new_vals[feature_names[i]] = float(x)

    return new_vals


# =====================================================
# Prediction
# =====================================================
@callback(
    Output("prediction-output", "children"),
    Output("proba-output", "children"),
    Input("selected-values", "data"),
)
def update_prediction(selected_values):

    x = [selected_values[f] for f in feature_names]

    X_input = pd.DataFrame([x], columns=feature_names)

    pred = model.predict(X_input)[0]
    proba = model.predict_proba(X_input)[0]

    pred_name = target_names[pred]

    proba_list = html.Ul([
        html.Li(f"{target_names[i]} : {proba[i]:.3f}")
        for i in range(len(target_names))
    ])

    return f"Classe prédite : {pred_name}", proba_list

# =====================================================
# Run
# =====================================================
if __name__ == "__main__":
    app.run_server(debug=True)
