# Project 1

Web Programming with Python and JavaScript


## application.py
I will give code snippets and give descriptions of the snippets

## Database Structure
3 tables --> books, users, reviews

#### books data structure
  | Column    | Type              |
  |-----------|-------------------|
  | isbn      | text              |
  | title     | text              |
  | author    | text              |
  | year      | text              |
  | id        | int Auto Increment|  

#### users data structure
  | Column    | Type              |
  |-----------|-------------------|
  | username  | text              |
  | password  | varchar(20)       |
  | id        | int Auto Increment|  

#### reviews data structure
  | Column        | Type              |
  |---------------|-------------------|
  | user_id       | integer           |
  | book_id       | integer           |
  | rating        | integer           |
  | review_text   | text              |

### All pages
All html pages have a navbar made with Bootstrap, use jinja for loops and conditional statements to display certain content.

### / -- index(), index.html
  ```python
  return render_template("index.html")#load homepage
  ```
  Here I just initiate the first route with a homepage. The index.html is a simple page with a header welcoming users and two buttons with links one for login and the other for register.

### /login -- login(), login.html

```python
if request.method == "GET":#if user first enters page
    if session.get("logged_in"):#if session exists bring to front page
        # redirect to search url
    else:#if session does not exists bring to load login page
        #render template for login


if request.method == "POST":#if login form is submitted
  #first I get the form data for login for username and password

  loginData=db.execute('SELECT * FROM users WHERE username=:username AND password=:password',
                      {'username': userN, 'password': passwd}).fetchall()

  if not loginData:
    #print error for user not found
  else:
    #handle successful login
    #save session
```
In login route I first check if the request method is GET or POST. In GET requests I check if a session is logged_in locally and then redirect them to search if they are already logged in. If not then I render the template for login.html.

In POST requests I first get form data for login on the html page. Then  I use a select statement with sqlalchemy and compare them with the form data. If the login does not match with any values then I render an error template for in a user does not exist. If a user does exist I save the session from the loginData
and then redirect them to the search page.

### /register -- reg(), register.html
  ```python
      if request.method == "GET":#if user first enters page
              return render_template("register.html")

      if request.method == "POST":#if register form is submitted

          #GET user form data for registration

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
                  return render_template("success.html",msg="user successfully registered")

              except Exception as e:
                  print(e)
                  return render_template("error.html",msg="error registering user")

          else:
            return render_template("error.html",msg="user already exists")

  ```

  The python code on this page takes the information form a submit form that takes a username, password and a re-entered password which both passwords have to match. On GET requests render the register.html page.

  Now onto POST requests once the page receives the POST request for the form. It gets the data compares the passwords first if not an error.html page will appear. It will then check if the username exists or not in the database. If it does then display the error.html page. If the username does not exists in the database then the user will be registered into the database. An INSERT INTO statement will enter the new required information for the new user. Once registered the user can now login. 

### /logout -- logout(), logout.html
  ```python
  try:
      sessionLogin=session['logged_in']
      print(sessionLogin)
      session.pop("logged_in")
      return render_template("logout.html",session=sessionLogin)
  except Exception as e:
      print(e)
  ```
  Simple code but it will "pop" the current user session and log the user out. The user is then returned to a logout saying the user has logged out.

### /search -- search(), search.html
  ```python
      if request.method == "GET":
          if session.get("logged_in") is None:
            #if login session does not exist then redirect to login screen
          else:
            #if login session exists load search.html
      else:
          #get form data form text search bar
          try:
              if (request.form.get("optionradio") == "title"):
                #if radio clicked set this option and create
                #a PostgreSQL statement to select data searching title
              elif (request.form.get("optionradio") == "author"):
                #if radio clicked set this option and create
                #a PostgreSQL statement to select data searching author
              elif (request.form.get("optionradio") == "isbn"):
                #if radio clicked set this option and create
                #a PostgreSQL statement to select data searching isbn
              elif (request.form.get("optionradio") == "id"):
                #if radio clicked set this option and create
                #a PostgreSQL statement to select data searching id
              else:
                #zero matches found

              #return form data form PostgreSQL statements
              return render_template("search.html",session=session["logged_in"],bookdata=data)
          except Exception as e:
            #handle error 0 matches found
  ```
  In search route check for login session first and handle redirect to correct sites. In search.html I setup 4 radio buttons and a search bar, both are required to search for a book. Users logged in can search for ISBN, title, author name, or id of book. Books will appear in a table according to database select search. Book table displays Book ID #, ISBN, Title, Author and Year published. ISBN numbers have an anchor tag to link to the book page.

### /api/<isbn> -- api(isbn), apiresp.html, 404.html
```python
    #set isbnSql variable with a PostgreSQL select statement based on

    if isbnSql == [] or isbnSql is None:
        #isbnSql has no value handle 404.html error

    #set bookData json object based on PostgreSQL select values returned
    #create object according to requirement
    bookData={}
    bookData['title']=isbnSql[0][1]
    bookData['author']=isbnSql[0][2]
    bookData['year']=isbnSql[0][3]
    bookData['isbn']=isbnSql[0][0]

    #count number of reviews for a book
    #set bookData json
    bookData['review_count']= revCount[0][0]

    #get average rating for a book
    #set bookData json
    bookData['average_score']= avgSc[0][0]

    #return apiresp.html
    return render_template("apiresp.html",data=bookData);
```
  API responses are handled from PostgreSQL statements data and are constructed into a json object. Then are returned to apiresp.html page or if an object does not exist then a 404.html error is displayed.

### /book/<bookid> -- book(bookid), book.html

```python
    #initialize required variables, use sqlalchemy to get data and set variables    
  if res.status_code==200: #good reads request was OK
      #get request response from goodreads api
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
      try:
          return render_template("success.html",msg="Book review added",book=book)
      except Exception as e:
          print(e)

  return render_template("book.html",book=book,grAvgR=grAvgR,grRevNo=grRevNo,bwUserRev=bwUserRev,bwRev=bwRev,curUbwRev=curUbwRev,bwReviews=bwReviews)
```
  When a user clicks on a ISBN from the search page they are brought here. This is the last page it handles the books pages and displays the books data from the books table and reviews table as well as an Goodreads API response based on a books ISBN. If a book has reviews it will display them if not it will give the user an option to write a review. The book.html page is dynamic and uses jinja to display certain content for the user based on if the user has not reviewed the book or not or if there are reviews for it. The book.html page tells if a book has been reviewed or not from boolean variables set to false or true based on database values.

  The booleans are bwRev and curUbwRev, if bwRev is set to it will display a table of all the reviews for the book. If bwRev is set to false it will display a text response saying there is no reviews and considers the user to add a review. The boolean curUbwRev is used to check if the current logged in user has written for the current book on its page. If the variable is false the book.html page will display a 1-5 select rating, textarea review and submit button form. The user is required to select from 1-5 being bad-good based on the book, write a text review and click the submit button to submit the review. If the curUbwRev boolean is set to true it will tell the user they have already reviewed the book and display the current users review on the book.
