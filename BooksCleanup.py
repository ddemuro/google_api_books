import json
import requests
import os


#URL = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:emily+henry&printType=books&langRestrict=en&key=mykey'
URL = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:'
BOOKSAPI = '&key='
DIR_WITH_BOOKS = '/zraid/derek-data/docker/derek-docker-data/audiobookshelf/audiobooks/AudioBooks'
FILES_FOLDERS_TO_SKIP = ["Star", "star", "quantum"]


def get_author_information(author):
    """Get author information from google books api"""
    if not author or author == "":
        return None, None

    try:
        # Convert foldername to API format
        author = author.replace(" ", "+").lower()

        # send a request and get a JSON response
        url_to_send = f"{URL}{author}&printType=books{BOOKSAPI}"
        print(url_to_send)
        # Add referrer to request
        # req = urllib.request.Request(url_to_send, )
        resp = requests.get(url_to_send,
                            headers={'referer': 'dereksapp'}, timeout=60)
        # parse JSON into Python as a dictionary
        book_data = resp.json()
    except Exception as e:
        # Return error as json
        return None, json.dumps({"error": str(e)})
    return book_data, None


def calculate_average_of_books(books):
    """Calculate average of all books from an author passed as json from google books api
    """
    try:
        average_rating = []
        for book in books['items']:
            print(book['volumeInfo']['averageRating'])
            # Store average rating
            average_rating.append(book['volumeInfo']['averageRating'])

        # Calculate average rating
        average_rating = sum(average_rating) / len(average_rating)
        return average_rating
    except Exception as e:
        return -1, e.message


def lookup_in_folder():
    skip = False
    for subdir, dirs, files in os.walk(DIR_WITH_BOOKS):
        if len(dirs) > 0:
            print("Skipping subfolders")
            skip = True
            continue

        if len(files) == 0:
            print("Skipping empty folder")
            skip = True
            continue

        for d in dirs:
            if skip:
                continue
            if d in FILES_FOLDERS_TO_SKIP:
                print(f"Skipping {d}")
                continue
            else:
                print(f"Looking up {d}")
                book_data, error = get_author_information(d)
                if book_data:
                    average_rating = calculate_average_of_books(book_data)
                    print(f"Average rating for {d} is {average_rating}")
                    # Write rating to file in folder
                    with open(f"{subdir}/{d}_average_auth_rating.txt", "w",
                              encoding='utf-8') as f:
                        f.write(str(average_rating))
                    with open(f"{subdir}/{d}_book_data.json", "w",
                              encoding='utf-8') as f:
                        json.dump(book_data, f)
                else:
                    print(f"Could not find {d}")
