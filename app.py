import numpy as np
import os
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)



#################################################
# Flask Setup
#################################################
app = Flask(__name__)

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
 
    
    precipitation = session.query(Measurement)
    
    precip_df = pd.read_sql(precipitation.statement, con=engine)
    precip_df.set_index('date', inplace = True)

    precip_df.index = precip_df.index.astype('str')
    precip_dict = precip_df.to_dict()
    return jsonify(precip_dict)
    
 


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)    
    latestdate = dt.date.fromisoformat(session.query(Measurement).order_by(desc(Measurement.date)).first().date)
    oneyearago = latestdate-dt.timedelta(days=365)
    

    tobs = session.query(Measurement).filter(oneyearago<Measurement.date)
    tobs_df = pd.read_sql(tobs.statement, con=engine)
    tobs_df.set_index('date', inplace = True)

    tobs_df.index = tobs_df.index.astype('str')
    tobs_df = tobs_df.to_dict()

    return jsonify(tobs_df)

    
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    station = session.query(Measurement.station).group_by(Measurement.station)
    station_df = pd.read_sql(station.statement, con=engine)
    
    return jsonify(station_df.to_dict())

if __name__ == '__main__':
    app.run(debug=True)