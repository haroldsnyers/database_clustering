import pymongo

IP_ADDRESS='192.168.1.12'


def insert_multiple(collection, input):
    for i in range(len(input)):
        print(collection.insert_one(input[i]))

def insert_one(collection, input):
    print(collection.insert_one(input))

def find_one(collection, input):
    print(collection.find_one(input))

def delete_one(collection, input):
    print(collection.delete_one(input))

def generate_dict():
    my_query = []
    for i in range (50):
        my_dict = { "title" : "Harry Potter " + str(i), "language" : "French"}
        my_query.append(my_dict)
    return my_query


myclient = pymongo.MongoClient('mongodb://' + IP_ADDRESS + ':60000')  # ip_address:port of mongos instance

mydb = myclient['shardddemo']  # name of the database

my_col_books = mydb["books"]  # name of the collection inside that database
# sharded database
my_col_movies = mydb["movies"]  # name of the collection inside that database

query_multi = generate_dict()
query_one = { "title" : "Harry Potter 0", "language" : "French"}
query = {"title":"Harry Potter 0"}  # will find the first instance with such a title

# insert_multiple(my_col_books, query_multi)
# insert_multiple(my_col_movies, query_multi)

insert_one(my_col_books, query_one)
insert_one(my_col_movies, query_one)


# find_one(my_col_books, query)
# find_one(my_col_movies, query)

# delete_one(my_col_books, query)
# delete_one(my_col_movies, query)
