import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite"

db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# Reviews = Base.classes.reviews
# Genres = Base.classes.genres
# Content = Base.classes.content
# Labels = Base.classes.labels


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
    stmt = db.session.query(Pitchfork.artist).distinct().order_by(Pitchfork.artist).statement
    print(str(stmt))
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (artist names)
    return jsonify(list(df.artist))


@app.route("/artists/<artist>")
def artist_data(artist):
    """Return artist, album, pub_year, genre, score, url"""

    stmt = db.session.query(Pitchfork.title, Pitchfork.pub_year, Pitchfork.score, Pitchfork.url).\
         filter(Pitchfork.artist == artist).statement
    artist_df = pd.read_sql_query(stmt, db.session.bind)
    data = artist_df.to_dict('records')

    # results = db.session.query(Pitchfork.title, Pitchfork.pub_year, Pitchfork.genre, Pitchfork.score, Pitchfork.url).\
    #     filter(Pitchfork.artist == artist).\
    #     order_by(Pitchfork.pub_year).all()

    # album = [result[0] for result in results]
    # year = [result[1] for result in results]
    # genre = [result[2] for result in results]
    # score = [float(result[3]) for result in results]
    # url = [result[4] for result in results]

    # data = {
    #     "year": year,
    #     "album": album,
    #     "score": score,
    #     "url": url
    # }
    # data = {}
    # for result in results:
    #     data[result[0]] = result[1:]

    # sel = [
    #     Pitchfork.title,
    #     Pitchfork.pub_year,
    #     Pitchfork.genre,
    #     Pitchfork.score,
    #     Pitchfork.url
    #     # Pitchfork.content
    # ]

    # results = db.session.query(*sel).filter(Pitchfork.artist == artist).all()

    # # Create a dictionary entry for each row of metadata information
    # artist_metadata = {}
    # for result in results:
    #     artist_dict = {}
    #     artist_metadata["title"] = result[0]
    #     artist_metadata["pub_year"] = result[1]
    #     artist_metadata["genre"] = result[2]
    #     artist_metadata["score"] = result[3]
    #     artist_metadata["url"] = result[4]
    #     # artist_metadata["content"] = result[5]

    print(data)
    return jsonify(data)


@app.route("/reviews/<artist>")
def reviews(artist):
    """Return artist, album, year, and score"""
    stmt = db.session.query(Pitchfork.title, Pitchfork.pub_year, Pitchfork.genre, Pitchfork.score).\
        filter(Pitchfork.artist == artist).statement
    artist_df = pd.read_sql_query(stmt, db.session.bind)

    # # Filter the data based on the artist
    # artist_reviews_data = df.loc[df[artist], [artist, "title","pub_year","genre","score"]]

    # # Sort by sample
    # artist_reviews_data.sort_values(by=artist, ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "album": artist_df.title.values.tolist(),
        "score": artist_df.score.values.tolist(),
        "pub_year": artist_df.pub_year.tolist(),
        "genre": artist_df.genre.tolist()
    }
    return jsonify(data)


#     # # Query for artist discography and album scores
#     results = db.session.query(Pitchfork.title, Pitchfork.pub_year, Pitchfork.genre, Pitchfork.score).\
#         filter(Pitchfork.artist == artist).\
#         order_by(Pitchfork.pub_year).all()

#     # Create lists from the query results
#     album = [result[0] for result in results]
#     year = [result[1] for result in results]
#     genre = [result[2] for result in results]
#     score = [int(result[3]) for result in results]


    # # Generate the plot trace
    # trace = {
    #     "x": title,
    #     "y": scores,
    #     "type": "bar"
    # }
    # return jsonify(trace)


# @app.route("/title_id")
# def title_data():
#     """Return emoji score and emoji id"""

#     # Query for the emoji data using pandas
#     query_statement = db.session.query(Pitchfork).\
#         order_by(Pitchfork.score.desc()).\
#         limit(10).statement
#     df = pd.read_sql_query(query_statement, db.session.bind)

#     # Format the data for Plotly
#     trace = {
#         "x": df["title"].values.tolist(),
#         "y": df["score"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)


# @app.route("/artist_name")
# def emoji_name_data():
#     """Return emoji score and emoji name"""

#     # Query for the top 10 emoji data
#     results = db.session.query(Pitchfork.artist, Pitchfork.score).\
#         order_by(Pitchfork.score.desc()).\
#         limit(10).all()
#     df = pd.DataFrame(results, columns=['artist', 'score'])

#     # Format the data for Plotly
#     plot_trace = {
#         "x": df["artist"].values.tolist(),
#         "y": df["score"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(plot_trace)


if __name__ == '__main__':
    app.run(debug=True)
