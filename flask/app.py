from flask import Flask, render_template
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from pymongo import MongoClient


#app = Flask(__name__)
#app.config['MONGO_URI'] = 'mongodb://airflow:airflow@mongo:27017/admin'  
#now = datetime.now()
#mongo = PyMongo(app)
app = Flask(__name__)

# Configurações do MongoDB
now = datetime.now()


@app.route('/')
def index():
    client = MongoClient('mongodb://airflow:airflow@mongo:27017')
    db = client['admin']

    collection = db[f'notices_{now.year}_{now.month}'] 

    news = collection.find()

    return render_template('index.html', news=news)

if __name__ == '__main__':
    app.run(debug=True)