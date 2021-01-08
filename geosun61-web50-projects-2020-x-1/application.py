import os
import requests


from decimal import Decimal
from flask import Flask, session, render_template, request, redirect, url_for, abort, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")#load homepage

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == "GET":#if user first enters page
        if session.get("logged_in"):#if session exists bring to front page
            return redirect(url_for('search'))
        else:#if session does not exists bring to load login page
            return render_template("login.html")

    if request.method == "POST":#if login form is submitted
            userN=request.form.get("usernamelogin")#get login form
            passwd=request.form.get("passwordlogin")

            #checking login form data
            print(userN," ",passwd)

            #matching username and password
            loginData=db.execute('SELECT * FROM users WHERE username=:username AND password=:password',
                                {'username': userN, 'password': passwd}).fetchall()

            print(loginData)


            if not loginData:
                print(loginData)
                return render_template("error.html",msg="user does not exist")
            else:
                print(loginData)
                print("session get 1",session.get("logged_in"))
                session["logged_in"]=loginData[0][2]
                print("session get 2",session.get("logged_in"))
                session.modified = True
                return redirect("/search")


@app.route("/logout")
def logout():
    try:
        sessionLogin=session['logged_in']
        print(sessionLogin)
        session.pop("logged_in")
        return render_template("logout.html",session=sessionLogin)
    except Exception as e:
        print(e)

@app.route("/register", methods=['GET','POST'])
def reg():

    if request.method == "GET":#if user first enters page
            return render_template("register.html")

    if request.method == "POST":#if register form is submitted
        userReg=request.form.get("userReg")#get register form
        passReg1=request.form.get("passReg1")
        passReg2=request.form.get("passReg2")

        print(userReg," ",passReg1," ",passReg2)#checking register form data

        userDb=db.execute("SELECT * FROM users WHERE username=:userReg",
                            {"userReg": userReg}).fetchall()

        if passReg1 != passReg2:
            return render_template("error.html",msg="passwords do not match")

        if not userDb:
            try:
                db.execute("INSERT INTO users (username,password) VALUES (:username,:password)",  #insert data into reviews table
                            {"username": userReg, "password": passReg1})

                print(f"Registered {userReg} with password {passReg1}")

                db.commit()
                loginData=db.execute('SELECT * FROM users WHERE username=:username AND password=:password',
                                    {'username': userReg, 'password': passReg1}).fetchall()

                print(f"User is confirmed and Registered {loginData}")
                return render_template("success.html",msg="user successfully registered")

            except Exception as e:
                print(e)
                return render_template("error.html",msg="error registering user")

        else:
            return render_template("error.html",msg="user already exists")

@app.route("/search", methods=['GET','POST'])
def search():

    if request.method == "GET":
        if session.get("logged_in") is None:
            return redirect("/login")
        else:
            print("User logged in:")
            print(session.get("logged_in"))
            bookdata=db.execute("SELECT * FROM books").fetchall()
            return render_template("search.html",session=session.get("logged_in"),bookdata=bookdata)

    else:
        searchBar = request.form.get("searchBar")   #get value in search bar
        bookdata = db.execute("SELECT * FROM books").fetchall()

        try:
            if (request.form.get("optionradio") == "title"):                              #if radio button title is selected
                data = db.execute("SELECT * FROM books WHERE LOWER(title) LIKE LOWER(:title)",       #search title
                                    {'title': "%"+searchBar+"%"}).fetchall()

            elif (request.form.get("optionradio") == "author"):
                data = db.execute("SELECT * FROM books WHERE LOWER(author) LIKE LOWER(:author)",        #if radio button author is selected
                                    {'author': "%"+searchBar+"%"}).fetchall()               #search author

            elif (request.form.get("optionradio") == "isbn"):
                data = db.execute("SELECT * FROM books WHERE LOWER(isbn) LIKE LOWER(:isbn)",              #if radio button isbn is selected
                                    {'isbn': "%"+searchBar+"%"}).fetchall()

            elif (request.form.get("optionradio") == "id"):
                data = db.execute("SELECT * FROM books WHERE id=:id",              #if radio button isbn is selected
                                    {'id': int(searchBar)}).fetchall()               # search id

            else:
                data =[0,"matches","found"]
                return render_template("search.html",session=session["logged_in"],bookdata=data)

            return render_template("search.html",session=session["logged_in"],bookdata=data)

        except Exception as e:
            print(e)
            bookdata = []
            return render_template("search.html",session=session["logged_in"],bookdata="0 matches found")

@app.route("/api/<isbn>") #api handler
def api(isbn):
    try:
        isbnSql=db.execute("SELECT * FROM books WHERE isbn like :isbn",
                            {"isbn": isbn}).fetchall()
    except Exception as e:
        abort(404,"ISBN not found in database")


    if isbnSql == [] or isbnSql is None:
        abort(404,description="ISBN not found in database")

    print(isbnSql)
    bookID=db.execute("SELECT id FROM books WHERE isbn like :isbn",
                      {"isbn":isbn}).fetchall()
    bookData={}
    bookData['title']=isbnSql[0][1]
    bookData['author']=isbnSql[0][2]
    bookData['year']=isbnSql[0][3]
    bookData['isbn']=isbnSql[0][0]

    #count number of reviews for a book
    revCount= db.execute("SELECT COUNT(*) FROM reviews WHERE book_id=:bid",
                        {"bid":bookID[0][0]}).fetchall()

    bookData['review_count']= revCount[0][0]

    #get average rating for a book
    avgSc=db.execute("SELECT AVG(rating) FROM reviews WHERE book_id=:bid",
                        {"bid":bookID[0][0]}).fetchall()
    bookData['average_score']= avgSc[0][0]

    return render_template("apiresp.html",data=bookData);

@app.errorhandler(404)# error handler for api
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route("/book/<bookid>", methods=['GET','POST'])        #individual book page with bookID
def book(bookid):             #details book page information
    book = db.execute("SELECT * FROM books WHERE id=:bookid",
                    {"bookid": bookid}).fetchone()         #getting book information

    user_id = session["logged_in"] #saving current user_id logged in

    curUbwRev = db.execute("SELECT * FROM reviews WHERE user_id=:user_id AND book_id=:book_id", #current user logged in checking if user reviewed the book
                            {"user_id":int(str(user_id)), "book_id":int(bookid)}).fetchone()

    bwReviews = db.execute("SELECT * FROM reviews WHERE book_id=:book_id", #fetching all book reviews for the specified the book
                            {"book_id":int(bookid)}).fetchall()

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "lkMQATRjzVYHEypSgA2g", "isbns": book.isbn}) #goodreads api request for individual book
    print(res.json())

    bwUserRev = False   # bookworm current User review for book is false
    bwRev = False

    if res.status_code==200: #good reads request was OK
        requesttest=res.json() #save response request
        grAvgR=requesttest["books"][0]["average_rating"] # average rating for goodreads book
        grRevNo=requesttest["books"][0]["work_ratings_count"] # total number of reviews on good reads
    else:
        grAvgR="error getting score"
        grRevNo="error getting review"

    if request.method == 'GET':
        if bwReviews == []:   # if bookworm reviews is empty then send boolean and return no reviews
            bwUserRev = False   # bookworm current User review for book is false
            bwRev = False       # bookworm all reviews for book is false
        else:   # if there are reviews for the book display
            bwRev = True    #set bwRev to true
            if curUbwRev is None:# if bookworm current User does not have review for book set bwUserRev false
                bwUserRev = False
            else:#if there is a review for the book from the current user set bwUserRev to true
                bwUserRev = True

        return render_template("book.html",book=book,grAvgR=grAvgR,grRevNo=grRevNo,bwUserRev=bwUserRev,bwRev=bwRev,curUbwRev=curUbwRev,bwReviews=bwReviews)
    else: #if method is post get form data
        ratingNum = request.form.get("rating_num") # get user rating number
        userRevText = request.form.get("reviewText") # get review Text

        try:
            db.execute("INSERT INTO reviews (user_id,book_id,rating,review_text) VALUES (:user_id,:book_id,:rating,:review_text)",  #insert data into reviews table
                        {"user_id": user_id, "book_id": bookid, "rating": ratingNum, "review_text": userRevText})
            print(f"Added review for user: {user_id} on book: {bookid} user rated the book {ratingNum}/5 described the book '{userRevText}'")
            db.commit()
            return render_template("success.html",msg="Book review added",book=book)
        except Exception as e:
            print(e)


    return render_template("book.html",book=book,grAvgR=grAvgR,grRevNo=grRevNo,bwUserRev=bwUserRev,bwRev=bwRev,curUbwRev=curUbwRev,bwReviews=bwReviews)
