import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# =====================================================
# DataManager
# =====================================================

class DataManager:

    def __init__(self):
        iris = load_iris()
        self._data = iris.data # X as often denoted by sklearn
        self._target = iris.target # y as often denoted by sklearn

        self._target_names = iris.target_names
        self._feature_names = iris.feature_names

        # also store data into a dataframe used for histograms
        self.iris_df = pd.DataFrame(self._data, columns=self._feature_names)
        self.iris_df["target"] = self._target

        self.model = RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )
        self.model.fit(self._data, self._target)

        # Default = mean values
        self.default_values = self.iris_df[self._feature_names].mean().to_dict()

    def get_data(self):
        return self._data

    def get_target(self):
        return self._target

    def get_data_target_as_dataframe(self):
        return self.iris_df
    
    def get_feature_names(self):
        return self._feature_names

    def get_target_names(self):
        return self._target_names

    def get_default_values(self):
        return self.default_values

    def get_model_prediction(self, x_values):
        X_input = pd.DataFrame([x_values], columns=self.get_feature_names())
        return self.model.predict(X_input)[0]

    def get_model_proba(self, x_values):
        X_input = pd.DataFrame([x_values], columns=self.get_feature_names())
        return self.model.predict_proba(X_input)[0]