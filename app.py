# Import Dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# Database Setup
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
# Reflect existing database into a new model
Base = automap_base()
# Reflect tables
Base.prepare(engine, reflect=True)
# View all classes
Base.classes.keys()
# Save to each table
Measurement = Base.classes.measurement
Station = Base.classes.measurement
# Create link
session = Session(engine)
# Setup Flask
app = Flask(__name__)
# Setup Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"USE format: yyyy-mm-dd for API below.<br/>"
        f"/api/v1.0/startdate<br/>"
        f"USE format: yyyy-mm-dd/yyyy-mm-dd for API below.<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation_scores = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= last_year).all()
    results_precipitation = dict(precipitation_scores)
    session.close()
    return jsonify(results_precipitation)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    stations = session.query(Measurement.station, func.count(Measurement.date)).group_by(Measurement.station).order_by(func.count(Measurement.date).desc()).all()
    results_stations = dict(stations)
    session.close()
    return jsonify(results_stations)

@app.route("/api/v1.0/tobs")
def tobs():
   session = Session(engine)
   max_temperature = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
   results_tobs = dict(max_temperature)
   return jsonify(results_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    start_datetime = dt.datetime.strptime(start, '%Y-%m-%d')
    start_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_datetime).all()
    session.close()

 # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for min, max, avg in start_result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Max"] = max
        tobs_dict["Avg"] = avg
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    start_datetime = dt.datetime.strptime(start, '%Y-%m-%d')
    end_datetime = dt.datetime.strptime(end, "%Y-%m-%d")
    start_end_result =  session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_datetime).filter(Measurement.date <= end_datetime).all()
    session.close()

    start_end_tobs = []
    for min, max, avg in start_end_result:
        tobs_dict1 = {}
        tobs_dict1["Min"] = min
        tobs_dict1["Max"] = max
        tobs_dict1["Avg"] = avg
        start_end_tobs.append(tobs_dict1)
    
    return jsonify(start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)

