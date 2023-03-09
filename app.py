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
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation_scores = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= last_year).all()
    results_precipitation = dict(precipitation_scores)
    session.close()
    return jsonify(results_precipitation)

@app.route("/api/v1.0/stations")
def station():
    stations = session.query(Measurement.station, func.count(Measurement.date)).group_by(Measurement.station).order_by(func.count(Measurement.date).desc()).all()
    results_stations = dict(stations)
    session.close()
    return jsonify(results_stations)



if __name__ == '__main__':
    app.run(debug=True)

