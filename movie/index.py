from random import randint
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from movie.auth import login_required
import requests, urllib, json

from movie.db import get_db


bp = Blueprint('index', __name__, url_prefix='/')
lst = []

@bp.route('/')
def index():
    # return render_template('index/index.html')
    user_id = session.get('user_id')

    if user_id is None:
        return render_template('index/index.html')
    else:
        return redirect(url_for("index.starter"))

@bp.route('/search/<string:genre>/<int:releaseYear>/<string:language>', methods=("GET", "POST"))
@login_required
def generate(genre, releaseYear, language):
    if request.method == 'POST':
        return starter()

    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&primary_release_year={releaseYear}&sort_by=popularity.desc&with_genres={genre}&with_original_language={language}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMmM1ODVmNjY4MjI1NzQwNjQ0Y2M2YzRlN2UxYTRlMiIsInN1YiI6IjY0YTA3YmE1ZDUxOTFmMDBmZjhiYTYwNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AQU63lkbX8brlddSJSib0ThxUYpLs6UL8EUKP7N3rFI"
    }

    response = requests.get(url, headers=headers)
    jsonData = response.json()["results"]
    
    randomIndex = randint(1, len(jsonData)-1)
    movieData = jsonData[randomIndex]
    lst.append(movieData)

    return render_template('form/display.html', movieData = movieData)

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def starter():
    if request.method == 'POST':
        genre = request.form['options']
        date = request.form['date']
        lang = request.form['language']
        error = None

        if not genre:
            error = "You must pick a genre!"
        if not date:
            error = "You must pick a date!"
        if not lang:
            error = "You must pick a language!"
        
        if error is not None:
            flash(error)
        else:
            if date == "1970s":
                date = randint(1970, 1979)
            elif date == "1980s":
                date = randint(1980, 1989)
            elif date == "1990s":
                date = randint(1990, 1999)
            elif date == "2000s":
                date = randint(2000, 2009)
            elif date == "2010s":
                date = randint(2010, 2019)
            elif date == "2020s":
                date = randint(2020, 2023)
            
            if lang == "Hindi":
                lang = "hi"
            elif lang == "English":
                lang = "en"
            elif lang == "French":
                lang = "fr"
            elif lang == "Russian":
                lang = "ru"
            
            return redirect(url_for('index.generate', genre=genre, releaseYear=date, language=lang))


    return render_template('form/search.html')

@bp.route('/learn')
@login_required
def learn():
    movieData = lst[-1]
    lst.clear
    return render_template('form/learn.html', movieData=movieData)

@bp.route('/create')
@login_required
def addToWishlist():
    movieData = lst[-1]
    lst.clear
    db = get_db()
    
    db.execute(
        'INSERT INTO wishlist (user_id, movietitle, posterPath, voteCount, overview)'
        'VALUES (?, ?, ?, ?, ?)',
        (g.user['id'], movieData['original_title'], movieData['poster_path'], movieData['vote_average'], movieData['overview'])
    )

    db.commit()
    return redirect(url_for('index.displayWishlist'))

@bp.route('/show')
@login_required
def displayWishlist():
    current_id = g.user['id']
    db = get_db()
    content = db.execute(
        'SELECT * FROM wishlist WHERE user_id = (?)', (current_id,)
    ).fetchall()

    return render_template('wishlist/show.html', content=content)

@bp.route('/<int:id>/delete')
@login_required
def delete(id):
    db = get_db()
    db.execute(
        'DELETE FROM wishlist WHERE id = ?',
        (id,)
    )
    db.commit()
    return redirect(url_for('index.displayWishlist'))

@bp.route('/learnmore/<int:id>')
@login_required
def learnmore(id):
    db = get_db()
    content = db.execute(
        'SELECT * FROM wishlist WHERE id = (?)', (id,)
    ).fetchone()
    return render_template('wishlist/learnmore.html', movie=content)

@bp.route('/addToWatch')
@login_required
def addToWatched():
    movieData = lst[-1]
    lst.clear
    db = get_db()
    
    db.execute(
        'INSERT INTO watched (user_id, movietitle, posterPath, voteCount, overview)'
        'VALUES (?, ?, ?, ?, ?)',
        (g.user['id'], movieData['original_title'], movieData['poster_path'], movieData['vote_average'], movieData['overview'])
    )

    db.commit()
    return redirect(url_for('index.showWatchedMovies'))

@bp.route('/showMovies')
@login_required
def showWatchedMovies():
    current_id = g.user['id']
    db = get_db()
    content = db.execute(
        'SELECT * FROM watched WHERE user_id = (?)', (current_id,)
    ).fetchall()

    return render_template('watchpage/showWatchedMovies.html', content=content)

@bp.route('/<int:id>/deleteMovie')
@login_required
def deleteFromWatched(id):
    db = get_db()
    db.execute(
        'DELETE FROM watched WHERE id = ?',
        (id,)
    )
    db.commit()
    return redirect(url_for('index.showWatchedMovies'))

@bp.route('/votepage/<int:id>')
@login_required
def displayVotePage(id):
    db = get_db()
    movieContent = db.execute(
        'SELECT * FROM watched WHERE id = (?)', (id,)
    ).fetchone()
    return render_template('watchpage/displayVotePage.html', movie=movieContent)

@bp.route('/upvote/<string:title>/<int:id>')
@login_required
def upvote(title, id):
    db = get_db()
    db.execute(
    'UPDATE watched SET upvoteCount = upvoteCount + 1 WHERE movietitle = (?)', (title,)
    )
    db.commit()

    return redirect(url_for('index.displayVotePage', id = id))

@bp.route('/downvote/<string:title>/<int:id>')
@login_required
def downvote(title, id):
    db = get_db()
    db.execute(
    'UPDATE watched SET downvotecount = downvotecount + 1 WHERE movietitle = (?)', (title,)
    )
    db.commit()

    return redirect(url_for('index.displayVotePage', id = id))