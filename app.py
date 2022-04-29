import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Meas = Base.classes.measurement
Stations = Base.classes.station

session = Session(engine)
#################################################
# Flask Setup
app = Flask(__name__)

#################################################
# Flask Routes

@app.route("/")
def home_page():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
   
    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    # Query measurement tables 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    annual_prcp = session.query(Meas.date,Meas.prcp).filter(Meas.date >= year_ago).all()
    
    rain = []
    for date, prcp in annual_prcp:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        rain.append(rain_dict)

    # Return data as json
    return jsonify(rain)

@app.route("/api/v1.0/stations")
def stations():
   
    """Return a JSON list of stations from the dataset"""
    all_stations = session.query(Stations.station).all()

    st_list = []
    for station in all_stations:
        st_dic = {}
        st_dic["station"] = station
        st_list.append(st_dic)

    # Return data as json
    return jsonify(st_list)

@app.route("/api/v1.0/tobs")
def tobs():
    
    """Query the dates and temperature observations of the most active station for the last year of data."""
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_tobs = session.query(Meas.date, Meas.tobs).filter(Meas.station == 'USC00519281').filter(Meas.date >= year_ago).all()

    temp_obs_list = []
    for date, tobs in last_year_tobs:
        temp_obs_dic = {}
        temp_obs_dic["date"] = date
        temp_obs_dic["tobs"] = tobs
        temp_obs_list.append(temp_obs_dic)

    # Return data as json
    return jsonify(temp_obs_list)

@app.route("/api/v1.0/start")
def start():

    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""
    results = session.query(func.min(Meas.tobs), func.max(Meas.tobs), func.avg(Meas.tobs)).filter(Meas.date >= '2017-08-23').all()

    data = []
    for TMIN, TMAX, TAVG in results:
        data_dict = {}
        data_dict["TMIN"] = TMIN
        data_dict["TMAX"] = TMAX
        data_dict["TAVG"] = TAVG
        data.append(data_dict)
    
    # Return data as json
    return jsonify(data)

@app.route("/api/v1.0/start-end")
def start_end():
    
    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    period_results = session.query(func.min(Meas.tobs), func.max(Meas.tobs), func.avg(Meas.tobs)).filter(Meas.date >= year_ago).all()

    period_data = []
    for TMIN, TMAX, TAVG in period_results:
        period_data_dict = {}
        period_data_dict["TMIN"] = TMIN
        period_data_dict["TMAX"] = TMAX
        period_data_dict["TAVG"] = TAVG
        period_data.append(period_data_dict)

    # Return data as json
    return jsonify(period_data)

if __name__ == '__main__':
    app.run(debug=True)