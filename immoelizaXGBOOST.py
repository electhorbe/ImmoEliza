import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import statsmodels.api as sm
import shap


class PropertyPricePredictor:
    """Class to train and evaluate a property price prediction model using XGBoost."""

    def __init__(self, data_path: str):
        """
        Initializes the PropertyPricePredictor class.

        Args:
            data_path (str): Path to the dataset.
        """
        self.data_path = data_path
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_and_clean_data(self) -> pd.DataFrame:
        """
        Loads and cleans the dataset.

        Returns:
            pd.DataFrame: Cleaned dataset.
        """
        df = pd.read_csv(self.data_path)

        # Log-transform the target variable
        df["price"] = np.log1p(df["price"])

        # Ensure categorical data is correctly typed
        df["top_names"] = df["top_names"].astype("category")

        return df

    def preprocess_data(self, df: pd.DataFrame):
        """
        Preprocesses the data by splitting into features and target and creating train-test splits.

        Args:
            df (pd.DataFrame): Dataframe to preprocess. Ignore the top_names parameter cause Shap doesnt work with categorical data.
        """
        X = df.drop(["price", "property_type", "top_names"], axis=1)
        y = df["price"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

    def initialize_model(self):
        """
        Initializes the XGBoost regression model.
        """
        self.model = XGBRegressor(
            objective="reg:squarederror",
            learning_rate=0.12,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.7,
            n_estimators=220,
            min_child_weight=10,
            enable_categorical=True,
        )

    def train_model(self):
        """
        Trains the XGBoost model on the training data.
        """
        if self.model is None:
            raise ValueError("Model is not initialized. Call `initialize_model` first.")
        self.model.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        """
        Evaluates the trained model and prints performance metrics.

        Returns:
            dict: A dictionary containing evaluation metrics (MAE, MSE, R-squared).
        """
        y_pred = self.model.predict(self.X_test)

        mae = mean_absolute_error(np.expm1(self.y_test), np.expm1(y_pred))
        mse = mean_squared_error(np.expm1(self.y_test), np.expm1(y_pred))
        r2 = r2_score(self.y_test, y_pred)

        print(f"Mean Absolute Error (MAE): {mae}")
        print(f"Mean Squared Error (MSE): {mse}")
        print(f"R-squared: {r2}")

        return {"MAE": mae, "MSE": mse, "R2": r2}

    def run_ols(self):
        """
        Fits an OLS (Ordinary Least Squares) regression model for interpretability.

        Returns:
            sm.OLS: Fitted OLS model summary.
        """
        X = sm.add_constant(self.X_train)
        ols_model = sm.OLS(self.y_train, X).fit()
        print(ols_model.summary())
        return ols_model

    def explain_with_shap(self):
        """
        Uses SHAP to explain the model's predictions and saves the SHAP plots.
        """
        explainer = shap.Explainer(self.model, self.X_train)
        shap_values = explainer(self.X_test)

        # Summary plot
        shap.summary_plot(shap_values, self.X_test, show=False)
        plt.savefig("shap_summary_plot.png")

        # Force plot for the first instance
        shap.initjs()
        shap.force_plot(
            shap_values[0], self.X_test.iloc[0], matplotlib=True, show=False
        )
        plt.savefig("shap_force_plot.png")


def main():
    """
    Main function to execute the workflow for property price prediction.
    """
    # Path to dataset
    data_path = "./Becode-Bouman-8/Properties.csv"

    # Initialize predictor
    predictor = PropertyPricePredictor(data_path)

    # Load, clean, and preprocess data
    df = predictor.load_and_clean_data()
    predictor.preprocess_data(df)

    # Train and evaluate the model
    predictor.initialize_model()
    predictor.train_model()
    metrics = predictor.evaluate_model()

    # Run OLS regression for interpretability
    predictor.run_ols()

    # Explain the model with SHAP
    predictor.explain_with_shap()


if __name__ == "__main__":
    main()
