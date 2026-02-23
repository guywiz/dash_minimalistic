from dash import dcc, html

class LayoutManager:
    def __init__(self):
        pass

    def get_layout(self, data_manager):
        # =====================================================
        # Layout
        # =====================================================
        return html.Div(
                style={"padding": "20px"},
                children=[
                    html.H2("Prédiction – Random Forest (Iris)"),
                    html.Hr(),

                    dcc.Store(
                        id="selected-values",
                        data=data_manager.get_default_values(),
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
                                            for i in range(len(data_manager.get_feature_names()))
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

    def get_Ul_list(self, proba, target_names):
        return html.Ul([
            html.Li(f"{target_names[i]} : {proba[i]:.3f}")
            for i in range(len(target_names))
        ])