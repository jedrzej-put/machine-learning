from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
import plac
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


@plac.opt("prepared_dir", "Directory with prepared data", Path, "d")
@plac.opt("n_estimators", "Number of estimators", int, "e")
def main(prepared_dir: Path, n_estimators: int = 50):

    assert prepared_dir, "Please provide a directory with prepared data"

    train_df, test_df = pd.read_csv(prepared_dir / "train.csv"), pd.read_csv(prepared_dir / "test.csv")

    X_train = train_df.drop(['remainder__Price'], axis=1)
    X_test = test_df.drop(['remainder__Price'], axis=1)
    y_train = train_df['remainder__Price']
    y_test = test_df['remainder__Price']

    with mlflow.start_run():
        random_forest = RandomForestRegressor(n_estimators=n_estimators)
        random_forest.fit(X_train, y_train)

        y_pred = random_forest.predict(X_test)

        rmse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        print(f"RandomForest(n_estimators={n_estimators}): RMSE={rmse}, MAE={mae}")

        mlflow.log_param('n_estimators', n_estimators)
        mlflow.log_metric('rmse', rmse)
        mlflow.log_metric('mae', mae)

        mlflow.sklearn.log_model(random_forest, "model")

        mlflow.set_tags({
            "authors": "Sebastian Szczepaniak, Jakub Garus, Jedrzej Smok",
            "date": "11.06.2023"
        })


if __name__ == "__main__":
    plac.call(main)