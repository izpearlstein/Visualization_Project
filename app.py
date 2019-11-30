import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite"

db = SQLAlchemy(app)


# Create our database model
class Pitchfork(db.Model):
    __tablename__ = 'pitchfork_tb'

    reviewid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist = db.Column(db.String)
    url = db.Column(db.String)
    score = db.Column(db.Float)
    best_new_music = db.Column(db.Integer)
    author = db.Column(db.String)
    author_type = db.Column(db.String)
    pub_date = db.Column(db.String)
    pub_weekday = db.Column(db.Integer)
    pub_day = db.Column(db.Integer)
    pub_month = db.Column(db.Integer)
    pub_year = db.Column(db.Integer)
    genre = db.Column(db.String)
    content = db.Column(db.String)

    def __repr__(self):
        return '<pitchfork_tb %r>' % (self.name)


# Create database tables
@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()


@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")


@app.route("/artist_names")
def names():
    """Return a list of artists."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Pitchfork.artist).distinct().\
        filter(Pitchfork.artist != None).filter(Pitchfork.artist != '').order_by(Pitchfork.artist).statement
    print(str(stmt))
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (artist names)
    return jsonify(list(df.artist))

@app.route("/genres")
def genres():
    """Return a list of genres."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Pitchfork.genre).distinct().filter(Pitchfork.genre != None).order_by(Pitchfork.genre).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (artist names)
    return jsonify(list(df.genre))

@app.route("/artists/<artist>")
def artist_data(artist):
    """Return data"""

    stmt = db.session.query(Pitchfork.pub_year, Pitchfork.title, Pitchfork.url).\
         filter(Pitchfork.artist == artist).filter(Pitchfork.artist != None).filter(Pitchfork.artist != '').\
             order_by(Pitchfork.pub_year).statement
    artist_df = pd.read_sql_query(stmt, db.session.bind)
    data = artist_df.to_dict('records')

    return jsonify(data)


@app.route("/reviews/<artist>")
def reviews(artist):
    """Return data"""
    stmt = db.session.query(Pitchfork.title, Pitchfork.pub_year, Pitchfork.genre, Pitchfork.score).\
        filter(Pitchfork.artist == artist).filter(Pitchfork.artist != None).filter(Pitchfork.artist != '').\
            order_by(Pitchfork.pub_year).statement
    artist_df = pd.read_sql_query(stmt, db.session.bind)

    # Format the data to send as json
    data = {
        "album": artist_df.title.values.tolist(),
        "score": artist_df.score.values.tolist(),
        "pub_year": artist_df.pub_year.values.tolist(),
        "genre": artist_df.genre.values.tolist()
    }
    return jsonify(data)

@app.route("/themes/<genre>")
def themes(genre):
    """Return data"""
    stmt = db.session.query(Pitchfork.pub_year, func.avg(Pitchfork.score).label('score')).\
        filter(Pitchfork.genre == genre).filter(Pitchfork.genre != None).group_by(Pitchfork.pub_year).order_by(Pitchfork.pub_year).statement
    genre_df = pd.read_sql_query(stmt, db.session.bind)

    # Format the data to send as json
    data = {
        "pub_year": genre_df.pub_year.values.tolist(),
        "score": genre_df.score.values.tolist()
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
