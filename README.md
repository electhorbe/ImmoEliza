
# Property Data Enrichment and Price Prediction

This repository contains two Python scripts for working with real estate data:
1. **Property Data Enrichment**: Combines property datasets with demographic and top-name data.
2. **Property Price Prediction**: Predicts property prices using machine learning (XGBoost) and provides interpretability through SHAP and OLS regression.

## Description

### Script 1: **Property Data Enrichment**
This script processes and enriches real estate data by:
- Adding demographic data (population, wealth index, density) based on postal codes.
- Formatting and cleaning postal codes.
- Combining the property dataset with the top five most common first names per postal code.

### Script 2: **Property Price Prediction**
This script trains a machine learning model (XGBoost) to predict property prices using the enriched dataset. Key features include:
- Automatic log-transformation of target variables for improved accuracy.
- Model evaluation with metrics such as MAE, MSE, and R-squared.
- Interpretability using SHAP for feature importance and OLS regression.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Package dependencies listed in `requirements.txt`

### Install Required Packages
Install the dependencies using pip:
```bash
pip install -r requirements.txt
```

### Key Libraries
- `pandas` for data manipulation
- `numpy` for numerical operations
- `xgboost` for machine learning
- `statsmodels` for regression analysis
- `matplotlib` and `shap` for visualization

---

## Usage

### Step 1: **Property Data Enrichment**

#### Run the Enrichment Script
```bash
python property_data_enrichment.py
```

#### Overview
The script performs the following:
1. Reads raw property and demographic data from CSV, Excel, and JSON files.
2. Maps postal codes to demographic information (population, wealth index, density).
3. Formats and cleans postal codes in the names dataset.
4. Identifies the top 5 most common names per postal code and combines this data with property data.

#### Input Files
- `Step_1_Pre_Dataset.csv`: Raw property data.
- `Step_1_Postal_Data.xlsx`: Demographic data (population, wealth index, density).
- `Step_0_Code_INS_to_Postal.json`: Mapping of postal codes to demographic codes.
- `names.csv`: Names data with frequency per postal code.

#### Output Files
- `Step_2_Dataset.csv`: Enriched property dataset with demographic features.
- `Properties.csv`: Final merged dataset with top names per postal code.

---

### Step 2: **Property Price Prediction**

#### Run the Prediction Script
```bash
python property_price_prediction.py
```

#### Overview
The script performs the following:
1. Loads and cleans the enriched dataset (`Properties.csv`).
2. Splits the data into training and testing sets.
3. Trains an XGBoost model to predict property prices.
4. Evaluates the model using:
   - **Mean Absolute Error (MAE)**
   - **Mean Squared Error (MSE)**
   - **R-squared**
5. Runs OLS regression for interpretability.
6. Explains predictions using SHAP and saves visualizations (`shap_summary_plot.png` and `shap_force_plot.png`).

#### Input File
- `Properties.csv`: Enriched dataset from Step 1.

#### Output Files
- **Evaluation Metrics**: Displayed in the console (MAE, MSE, R-squared).
- **SHAP Visualizations**:
  - `shap_summary_plot.png`: Summary of feature importance.
  - `shap_force_plot.png`: Force plot for an individual prediction.

---

## Example Workflow

### Enrichment Workflow
1. Prepare the input files (`Step_1_Pre_Dataset.csv`, `Step_1_Postal_Data.xlsx`, etc.).
2. Run the enrichment script:
   ```bash
   python property_data_enrichment.py
   ```
3. Use the output file `Properties.csv` for price prediction.

### Prediction Workflow
1. Run the price prediction script:
   ```bash
   python property_price_prediction.py
   ```
2. Review the evaluation metrics and SHAP visualizations.

---

## Notes
- Make sure file paths in the scripts are updated to your local environment.
- For large datasets, consider optimizing memory usage (e.g., using `dtype` for specific columns in pandas).

---

## Authors
- **Electhorbe**: and the help of the bouman_8 Sudents/coach


--- 
