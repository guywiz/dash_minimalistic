import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

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
