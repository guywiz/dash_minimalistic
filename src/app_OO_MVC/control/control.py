from dash import callback
from dash.dependencies import Input, Output, State

class ControlManager:
    def __init__(self, data_manager, view_manager):
        self.data_manager = data_manager
        self.view_manager = view_manager

    def register_callbacks(self):
        # =====================================================
        # Update histograms
        # =====================================================
        @callback(
            [Output(f"hist-{i}", "figure") for i in range(len(self.data_manager.get_feature_names()))],
            Input("selected-values", "data"),
        )
        def update_histograms(selected_values):
            return self.view_manager.update_histograms(selected_values)

        # =====================================================
        # Click handling
        # =====================================================
        @callback(
            Output("selected-values", "data"),
            [Input(f"hist-{i}", "clickData") for i in range(len(self.data_manager.get_feature_names()))],
            State("selected-values", "data"),
            prevent_initial_call=True,
        )
        def update_selected_values(*args):
            return self.view_manager.update_selected_values(*args)

        # =====================================================
        # Prediction
        # =====================================================
        @callback(
            Output("prediction-output", "children"),
            Output("proba-output", "children"),
            Input("selected-values", "data"),
        )
        def update_prediction(selected_values):
            return self.view_manager.update_prediction(selected_values)
