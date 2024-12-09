
# Property Data Enrichment and Price Prediction

This repository contains two Python scripts for working with real estate data:
1. **immoelizaData**: Combines property datasets with demographic and top-name data.
2. **immoelizaXGBOOST**: Predicts property prices using machine learning (XGBoost) and provides interpretability through SHAP and OLS regression.

## Description

### Script 1: **immoelizaData**
This script processes and enriches real estate data by:
- Adding demographic data (population, wealth index, density) based on postal codes.
- Formatting and cleaning postal codes.
- Combining the property dataset with the top five most common first names per postal code.

### Script 2: **immoelizaXGBOOST**
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

### Step 1: **immoelizaData**

#### Run the Data Script
```bash
python immoelizaData.py
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

### Step 2: **immoelizaXGBOOST**

#### Run the Prediction Script
```bash
python immoelizaXGBOOST.py
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

Mean Absolute Error (MAE): 109476.77514740064
Mean Squared Error (MSE): 59667657350.90381
R-squared: 0.8222279579586299
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  price   R-squared:                       0.521
Model:                            OLS   Adj. R-squared:                  0.520
Method:                 Least Squares   F-statistic:                     847.7
Date:                Mon, 09 Dec 2024   Prob (F-statistic):               0.00
Time:                        15:27:51   Log-Likelihood:                -6773.0
No. Observations:               11724   AIC:                         1.358e+04
Df Residuals:                   11708   BIC:                         1.370e+04
Df Model:                          15                                         
Covariance Type:            nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const               10.8230      0.033    326.728      0.000      10.758      10.888
bedrooms             0.0797      0.004     21.641      0.000       0.072       0.087
postal_code      -6.345e-06   1.57e-06     -4.047      0.000   -9.42e-06   -3.27e-06
kitchen              0.0293      0.009      3.332      0.001       0.012       0.047
facades              0.0183      0.005      3.393      0.001       0.008       0.029
terrace              0.1253      0.009     14.221      0.000       0.108       0.143
terraceSurface       0.0002   5.64e-05      3.864      0.000       0.000       0.000
buildingState       -0.0176      0.003     -5.878      0.000      -0.023      -0.012
garden               0.0044      0.010      0.428      0.669      -0.016       0.025
gardenSurface     5.317e-06   2.56e-06      2.078      0.038    3.03e-07    1.03e-05
pool                 0.1975      0.025      7.851      0.000       0.148       0.247
livingArea           0.0018   4.49e-05     40.183      0.000       0.002       0.002
surfaceOfThePlot  1.388e-05   1.75e-06      7.925      0.000    1.04e-05    1.73e-05
INS Code         -3.507e-06   2.62e-07    -13.373      0.000   -4.02e-06   -2.99e-06
Population        5.385e-07   3.57e-08     15.067      0.000    4.68e-07    6.09e-07
Wealth Index         0.0138      0.000     55.460      0.000       0.013       0.014
==============================================================================
Omnibus:                     1540.012   Durbin-Watson:                   2.002
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            19550.894
Skew:                           0.056   Prob(JB):                         0.00
Kurtosis:                       9.325   Cond. No.                     1.28e+06
==============================================================================

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
- **Electhorbe**: and the help of the Becode bouman_8 Sudents/coach


--- 
