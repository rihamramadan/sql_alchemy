from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, Date, cast, distinct
import numpy as np
import datetime as dt


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD/ **** FILL DATE IN LINK**** <br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD/ ****FILL IN START AND END DATE IN LINK**** <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitiation():
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    all_results = []
    for result in results:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["prcp"] = result.prcp
        all_results.append(result_dict)

    return jsonify(all_results)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    all_station_results = []
    for result in results:
        result_dict = {}
        result_dict["station_id"] = result.station
        result_dict["station"] = result.name
        all_station_results.append(result_dict)
    return jsonify(all_station_results)


@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23','2017-08-23')).order_by(Measurement.date).all()
    all_temp_results = []
    for result in results:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["temp"] = result.tobs
        all_temp_results.append(result_dict)
    return jsonify(all_temp_results)

@app.route('/api/v1.0/<start>/')
def given_date(start):
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    date_list = []
    for result in results:
        result_dict = {}
        result_dict['Average Temperature'] = round(result[0], 2)
        result_dict['Highest Temperature'] = result[1]
        result_dict['Lowest Temperature'] = result[2]
        date_list.append(result_dict)
    return jsonify(date_list)

@app.route('/api/v1.0/<start2>/<end>/')
def startandend_date(start2, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start2,end)).all()

    dates_list = []
    for result in results:
        result_dict = {}
        result_dict['Date Start'] = start2
        result_dict['Date End'] = end
        result_dict['Temperature Average'] = round(result[1], 2)
        result_dict['Highest Temperature'] = result[2]
        result_dict['Lowest Temperature'] = result[0]
        dates_list.append(result_dict)
    return jsonify(dates_list)


if __name__ == '__main__':
    app.run(debug=True)