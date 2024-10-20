# Fraud Detection in Financial Transaction

## Dataset Description

A comprehensive resource designed for training and evaluating machine learning models in the context of financial fraud detection. It combines data from various sources, including transaction records, customer profiles, fraudulent patterns, transaction amounts, and merchant information, into a single dataset with the shape (1000, 14). This consolidated dataset facilitates the development of robust fraud detection models by providing rich, diverse features necessary for identifying and predicting fraudulent activities. It serves as an invaluable tool for researchers, data scientists, and analysts aiming to advance fraud detection methodologies.

**Kaggle Link:** https://www.kaggle.com/datasets/goyaladi/fraud-detection-dataset

## **Steps to follow**

* Clone the repository

```python

git clone https://github.com/Fraud-AI/fraud-detection-app.git

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

* Install tailwindcss in the `fraud` directory

```python

# go to fraud directory
cd fraud

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
python -m flask --app fraud init-db

```

* Run Flask App

```python

# Run flask
python -m flask --app fraud run --port 8000 --debug

```
