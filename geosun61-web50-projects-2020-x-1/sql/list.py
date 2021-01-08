import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL")) # database engine object from SQLAlchemy that manages connections to the database
                                                    # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))    # create a 'scoped session' that ensures different users' interactions with the
                                                    # database are kept separate


def main():
    books = db.execute("SELECT isbn, title, author, year FROM books").fetchall() # execute this SQL command and return all of the results
    for book in books:
        print(f"Book ISBN: {book.isbn}, Title: {book.title}, Author:  {book.author}, Year Published: {book.year}") # for every flight, print out the flight info



if __name__ == "__main__":
    main()
