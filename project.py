from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Region, Instrument, User

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///instruments.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all instruments
@app.route('/')
@app.route('/main/')
def showRegions():
    regions = session.query(Region).all()
    instruments = session.query(Instrument).all()
    users = session.query(User).all()
    print(users)
    return render_template('main.html', regions=regions, instruments=instruments, users=users)

@app.route('/asia/')
def showAsianInstruments():
    return render_template('asia.html')

@app.route('/africa/')
def showAfricanInstruments():
    return render_template('africa.html')

@app.route('/americas/')
def showAmericanInstruments():
    return render_template('americas.html')

@app.route('/europe/')
def showEuropeanInstruments():
    return render_template('europe.html')

@app.route('/oceania/')
def showOceaniaInstruments():
    return render_template('oceania.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
