import numpy as np

from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify  #initializing for flask 


# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite") # to connect to sqlite database

# reflect an existing database into a new model
Base = automap_base() #to reflect tables into classses and save 

# reflect the tables
Base.prepare(engine, reflect=True)

# Save
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup

app = Flask(__name__)

# Flask route for the welcome and the rest of the routes will follow the same precedure with first being commented to say the function of the code
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#route for precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # linking the session from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value"""
    # Query all Precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    all()
    
    session.close()

    # Convert tuples to list
    all_prcp = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)
#next route for stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    results = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)
#for tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24").\
        filter(Measurement.station == 'USC00519281').all()
    session.close()
    all_tobs = []
    for date,tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)
#next route 
@app.route("/api/v1.0/<start>")
def Start(start):
    session = Session(engine)
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    results = session.query(func.min(Measurement.tobs),
              func.max(Measurement.tobs),
              func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    session.close()
    start_tobs = []
    for min, max, avg in results:
        start_tobs_dict = {}
        start_tobs_dict["min_tobs"] = min
        start_tobs_dict["max_tobs"] = max
        start_tobs_dict["avg_tobs"] = avg

        start_tobs.append(start_tobs_dict)
    print (start_tobs)
    return jsonify(start_tobs)
#next route
@app.route("/api/v1.0/<start>/<end>")
def Start_End(start,end):
    session = Session(engine)
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    results = session.query(func.min(Measurement.tobs),
              func.max(Measurement.tobs),
              func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    start_end_tobs = []
    for min, max, avg in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_tobs"] = min
        start_end_tobs_dict["max_tobs"] = max
        start_end_tobs_dict["avg_tobs"] = avg

        start_end_tobs.append(start_end_tobs_dict)
    return jsonify(start_end_tobs)
#most important for the app to run 
if __name__ == '__main__':
    app.run(debug=True)