#!/usr/bin/env python3

# from itertools import islice

seed = __import__("seed")


# function that uses a generator to fetch rows one by one from the user_data table.
# You must use the Yield python generator
def stream_users():
    db = seed.connect_to_prodev()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM user_data")
    results = cursor.fetchall()

    for row in results:
        yield row

    cursor.close()
    db.close()


# for user in islice(stream_users(), 6):
#     print(user)
