# KAIM Week 8 and 9 Challenge

## Improved Detection of Fraud Cases for E-commerce and Bank Transactions - Adey Innovetions Inc.

Fraud detection is an essential aspect of financial technology, especially within the e-commerce and banking sectors, where the potential for fraudulent activity is ever-present. As transactions continue to migrate to online platforms, these industries face unique challenges in preventing financial fraud. E-commerce platforms handle a high volume of transactions daily, and fraudulent transactions can lead to financial losses, compromised data security, and decreased customer trust. Banking institutions, too, must continually monitor and secure online and card transactions against fraud, which can involve tactics ranging from identity theft to unauthorized withdrawals. 

Adey Innovations Inc. has prioritized the development of a robust fraud detection system to combat these challenges. This project aims to build a reliable detection framework to secure e-commerce and banking transactions, protecting customers and reducing potential losses for financial institutions. This solution will contribute not only to enhanced financial security but also to reinforcing the trust of customers in digital financial services. 


### Project Overview

This fraud detection project aims to meet several key objectives that align with Adey Innovations’ commitment to secure financial technology. The objectives include: 

- **Creating Accurate Fraud Detection Models** 
- **Geolocation Analysis**
- **Transaction Pattern Recognition** 

Each of these objectives aligns with Adey Innovations’ mission of providing secure and trustworthy financial services, as they collectively enhance the detection and prevention of fraudulent transactions in real time. 

### Project Task Breakdown

The project will be completed in a series of well-defined tasks, each crucial to the overall success of the fraud detection solution:

1. **Data Analysis and Preprocessing:**

    - Analyze historical transaction data to identify patterns and inconsistencies.
    - Clean and preprocess the data, handling missing values, outliers, and standardizing features, making the data suitable for model training.

2. **Feature Engineering:**

    - Create features that capture important signals, such as transaction frequency, amount variations, geolocation discrepancies, and historical transaction comparisons.
    - Generate new features based on time, location, and user behavior to better represent patterns that may indicate fraud.

3. **Model Building and Evaluation:**

    - Use machine learning algorithms such as Logistic Regression, Decision Trees, and Gradient Boosting to build predictive models.
    - Evaluate model performance using metrics like accuracy, precision, recall, and F1-score, ensuring the model can accurately identify fraudulent transactions while minimizing false positives.

4. **Explainability:**

    - Utilize SHAP (SHapley Additive exPlanations) and LIME (Local Interpretable Model-agnostic Explanations) to explain model decisions, providing insight into why certain transactions are flagged as fraudulent.
    - Model explainability is key for transparency, helping stakeholders understand and trust the model’s output.

5. **Model Deployment:**

    - Develop a RESTful API using Flask to deploy the model in a production environment, allowing real-time fraud detection for transactions.
    - Ensure the API is secure, reliable, and can handle high transaction volumes with low latency.

6. **Dashboard Development:**

    - Create an interactive dashboard using Dash to visualize trends, monitor the model’s performance, and provide real-time insights into detected fraud patterns.
    - The dashboard will give stakeholders a user-friendly interface to understand the system’s effectiveness and explore transaction data in detail.

Each task will contribute to building a comprehensive fraud detection system that meets the needs of both Adey Innovations and its customers.

### Project Structure

```bash

  ├── app/
  │   ├── static/   
  │   ├── templates/ 
  │   ├── __init__.py               
  │   └── database.py
  │   ├── data.py
  │   ├── xgb_model.py                
  │   └── model.py
  │   ├── dashboard.py     
  │   ├── schema.sql       
  │   ├── tailwind.config.js                           
  ├── data/
  ├── lime_explanations/
  ├── models/
  ├── plots/
  ├── notebooks/
  │   ├── kaim-week-8=9-task1.ipynb 
  │   ├── kaim-week-8=9-task2.ipynb
  │   ├── kaim-week-8=9-task3.ipynb   
  ├── scripts/
  │   ├── __init__.py     
  │   ├── main.py                      
  ├── src/
  │   ├── __init__.py     
  │   ├── data_loader.py                
  │   ├── data_cleaning.py
  │   ├── data_preprocessing.py
  │   ├── eda.py
  │   ├── feature_engineering.py
  │   ├── merge_fraud_and_ip_data.py
  │   ├── mlflow_logger.py
  │   ├── model_definition.py
  │   ├── scaling_encoding.py
  │   ├── utils.py            
  ├── tests/
  │   ├── __init__.py     
  │   ├── test_data_loader.py 
  ├── .env                             
  ├── .gitignore       
  ├── Dockerfile
  ├── docker-compose.yml        
  ├── requirements.txt
  └── README.md                   #

```

## **Steps to follow**

* Clone the repository

```python

git clone https://github.com/tedoaba/KAIM-W8-9.git
cd KAIM-W8-9

```

* Create a virtual environment

```python

python -m venv .venv

```

* Create .env file and add the following

```python

ENVIRONMENT="Development"
FLASK_SECRET_KEY='your secret key'

DATABASE_URL=postgresql://database:password@host:port/db_name

```

* Install all the requirements

```python

# install dependencies
pip install -r requirements.txt

```

* Install tailwindcss in the `app` directory

```python

# go to fraud directory
cd app

# Tailwind CSS
npm install tailwindcss

```

* Create `tailwind.config.js` file

```python
# create tailwind.config.js file
npx tailwindcss init

```

* Copy and add the following to `package.json` file so that your css will be updated every time you make a change

```python

"scripts": {
    "create-css": "npx tailwindcss -i ./static/src/input.css -o ./static/css/main.css --watch"
  }

```

* Initialize tailwindcss

```python

# Run the following every time you update tailwind css
npm run create-css

```

* In a separate terminal, in the parent directory, initialize the database

```python

# Initialize database
python -m flask --app app init-db

```

* Run Flask App

```python

# Run flask
python -m flask --app app run --port 8000 --debug

```

### Visualizations

#### MLflow

#### Model Comparison

![MLflow compare](plots/mlflow_compare.png)

#### Xgboost Model

![Xgboost model](plots/xgboost_mlflow.png)

### SHAP

#### Summary Plot

![XGBoost - Summary Plot for fraud data](plots/fraud_data_XGBClassifier_shap_summary.png)


#### Dependence Plot

![XGBoost - Shap Dependence](plots/fraud_data_XGBClassifier_shap_dependence.png)

### LIME

![XGBoost - Feature Importance](plots/fraud_data_XGBClassifier_lime_feature_importance.png)

### Flask App

![Correlation of the Dataset](plots/fraud_data_XGBClassifier_shap_summary.png)

[![Flask Demo](https://raw.githubusercontent.com/tedoaba/KAIM-W8-9/main/plots/thumbnail.png)](https://raw.githubusercontent.com/tedoaba/KAIM-W8-9/main/video/kaim-week-8-9-web.mp4)

### Dashboard

![Dash Summary](plots/dash-summary.png)

![Dash Summary](plots/dash-distribution.png)

![Dash Summary](plots/dash-other.png)
