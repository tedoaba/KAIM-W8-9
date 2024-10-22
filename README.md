# KAIM-W8-9
KAIM Weak 8 and 9 Challenge

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
