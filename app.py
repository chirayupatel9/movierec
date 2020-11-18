from flask import Flask, render_template, request, redirect, url_for, session
import functions
import json
import functions2,music
app = Flask(__name__)
app.secret_key = "hello"
app.static_folder = 'static'


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "GET":
        if 'logged_in' in session:
            pass
        return render_template("homepage.html")
    else:
        return redirect(url_for('login', message="Login first"))

@app.route('/moviehome',methods=["POST","GET"])
def moviehome():
    if request.method == "GET":
        if 'logged_in' in session:
            pass
        return render_template("search_movies.html")
    else:
        return redirect(url_for('login', message="Login first"))


@app.route('/genre', methods=["POST", "GET"])
def search_by_genre():
    if request.method == "GET":
        if 'logged_in' not in session:
            return redirect(url_for('login', message="Login first"))
        return render_template("searchbygenre.html")

    else:
        gen = request.form["sbg"]
        bmg = functions.best_movies_by_genre(gen, 10)
        return render_template("index.html", data=bmg)


@app.route('/Relevant', methods=["POST", "GET"])
def search_by_relevant():
    if request.method == "GET":
        if 'logged_in' not in session:
            return redirect(url_for('login', message="Login first"))
        return render_template("searchbyrelvance.html")

    else:
        rel = request.form["sbr"]
        bmg = functions.get_other_movies(rel)
        return render_template("index.html", data=bmg)





@app.route('/content', methods=["POST", "GET"])
def search_by_content():
    if request.method == "GET":
            if 'logged_in' not in session:
                return redirect(url_for('login', message="Login first"))
            return render_template("searchbycontentbased.html")

    else:
        sbcc = request.form["sbc"]
        sbcn = request.form["sbc2"]
        sbcn = int(sbcn)
        movies = functions.get_similar_movies_content_based(sbcc, sbcn)
        return render_template("index.html", data=movies)
        # return sbcn + sbcc

@app.route('/bookcontent', methods=["POST", "GET"])
def search_by_bookscontent():
    if request.method == "GET":
        if 'logged_in' not in session:
            return redirect(url_for('login', message="Login first"))
        return render_template("searchbook.html")

    else:
        sb = request.form["sb"]
        sb2 = request.form["sb2"]
        sb2 = int(sb2)
        books = functions2.get_similar_books_content_based(sb, sb2)
        return render_template("index.html", data=books, movie_name=sb2, user_rating=sb2)

@app.route('/music', methods=["POST", "GET"])
def search_by_musiccontent():
    if request.method == "GET":
        if 'logged_in' not in session:
            return redirect(url_for('login', message="Login first"))
        return render_template("searchmusic.html")

    else:
        sb = request.form["sbm"]
        mus = music.getsomemusic(sb)
        return render_template("index.html", data=mus, song_name=sb)



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if 'logged_in' in session:
            return redirect(url_for('search'))
        return render_template("login.html")

    else:
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
        if username == "root" and password == "abc@123":
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template("login.html", message="Invalid user info.")


@app.route('/logout', methods=["POST", "GET"])
def logout():
    keys = list(session.keys())
    for key in keys:
        session.pop(key)
    return redirect(url_for('login', message="Logged out"))


if __name__ == '__main__':
    app.run(debug=True)
