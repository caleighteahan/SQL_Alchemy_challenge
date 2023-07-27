# Import the dependencies.
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
import datetime as dt

#################################################
# Database Setup
#################################################

engine=create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
base=automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement=base.classes.measurement
station=base.classes.station
# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_query = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= query_date).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in prcp_query}
    
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    # Perform a query to retrieve the last 12 months of temperature observation data for the most active station
    station_data = session.query(station.station).all()

    # Extract the temperatures from the query result
    stations = [result[0] for result in station_data]

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    # Perform a query to retrieve the last 12 months of temperature observation data for the most active station
    query_date2 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature_data = session.query(measurement.tobs).\
    filter(measurement.station == "USC00519281").\
    filter(measurement.date >= query_date2).all()

    # Extract the temperatures from the query result
    temperatures = [result[0] for result in temperature_data]

    return jsonify(temperatures)


@app.route("/api/v1.0/<start>")
def start(start):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    temperature_stats = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start_date).all()

    all_names = list(np.ravel(temperature_stats))

    return jsonify(all_names)


@app.route("/api/v1.0/<start2>/<end>")
def startend(start2,end):
    start_date2 = dt.datetime.strptime(start2, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    temperature_stats2 = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start_date2).\
    filter(measurement.date <= end_date).all()

    all_names2 = list(np.ravel(temperature_stats2))

    return jsonify(all_names2)


if __name__ == '__main__':
    app.run(debug=True)