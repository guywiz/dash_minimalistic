import plotly.graph_objects as go

# =====================================================
# Histogram factory
# =====================================================

class HistogramFactory:
    def __init__(self):
        pass

    def make_histogram(self, feature, selected_value, data_manager):

        fig = go.Figure()

        fig.add_trace(
            go.Histogram(
                x=data_manager.get_data_target_as_dataframe()[feature],
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
            height=200,
            margin=dict(l=40, r=20, t=40, b=40),
            showlegend=True,
        )

        return fig
