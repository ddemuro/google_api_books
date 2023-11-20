import os

DIR_WITH_BOOKS = '/home/ddemuro/google_api_books/test/'


def print_rating():
    for root, dirs, files in os.walk(DIR_WITH_BOOKS):
        if len(files) == 0:
            continue
        for d in dirs:
            rating = -1
            try:
                with open(f"{root}/{d}/average_auth_rating.txt", "r",
                            encoding='utf-8') as f:
                    rating = float(f.read())
            except:
                pass
            if rating != -1 and rating < 3:
                print(f"{d}, {rating}")
        break


print_rating()
