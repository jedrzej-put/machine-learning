import sys
from pathlib import Path

import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

params = yaml.safe_load(open("params.yaml"))["prepare"]

split_param = params["split"]
random_param = params["seed"]

input_file = Path(sys.argv[1])
train_output = Path("data") / "prepared" / "train.csv"
test_output = Path("data") / "prepared" / "test.csv"

Path("data/prepared").mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

categorical_features = df.select_dtypes(include=["object"]).columns.tolist()

train_df, test_df = train_test_split(df, train_size=split_param)

categorical_preprocessor = Pipeline(steps=[
    ("encoder", OrdinalEncoder())
])

preprocessor = ColumnTransformer(transformers=[
    ("categorical_preprocessor", categorical_preprocessor, categorical_features)
], remainder="passthrough")

train_df = preprocessor.fit_transform(train_df)
test_df = preprocessor.transform(test_df)

train_df = pd.DataFrame(data=train_df, columns=preprocessor.get_feature_names_out())
test_df = pd.DataFrame(data=test_df, columns=preprocessor.get_feature_names_out())

train_df.to_csv(train_output, index=False)
test_df.to_csv(test_output, index=False)