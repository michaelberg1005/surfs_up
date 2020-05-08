# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# create engine
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# table references
Measurement = Base.classes.measurement
Station = Base.classes.station

# session link
session = Session(engine)

# create flask app
app = Flask(__name__)

# define welcome route


@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br/>
    Available Routes:<br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/temp/start/end <br/>
    ''')
# precipitation route


@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# stations route


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# monthyl temperature route


@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()

    temps = list(np.ravel(results))
    return jsonify(temps)

# stats route
@app.route("/api/v1.0/temp/<start>")

@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
     # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
            results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
            temps = list(np.ravel(results))
            return jsonify(temps)
    
    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps)
